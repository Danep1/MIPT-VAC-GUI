import time
from dataclasses import dataclass, asdict
import numpy as np
import traceback as tb

import PySide6.QtAsyncio as QtAsyncio
import asyncio
from enum import Enum, unique
import os

from ui import MainWindow, QApplication, MeasureType, Point, color_list, QColor, QColor_to_str
from device import Ins2636B, InsDSO4254C

@unique
class Status(Enum):
	ready = 0
	measuring = 1
	stop = 3
	done = 4

class MeasurementManager:
	def __init__(self, instr: Ins2636B, oscil: InsDSO4254C, window: MainWindow):
		self.instr = instr
		self.window = window
		self.oscil = oscil

		self.measure_type_list_saved = []
		self.status = Status.ready

		self.window.m_ui.light_on_off_button.toggled.connect(self.light_on_off_button_slot)

		self.window.m_ui.manual_bias_1_spin.valueChanged.connect(self.manual_bias_1_spin_slot)
		self.window.m_ui.manual_bias_2_spin.valueChanged.connect(self.manual_bias_2_spin_slot)

		self.window.m_ui.manual_bias_reset_1_button.clicked.connect(self.manual_bias_reset_1_button_slot)
		self.window.m_ui.manual_bias_reset_2_button.clicked.connect(self.manual_bias_reset_2_button_slot)

		self.window.m_ui.start_button.clicked.connect(lambda: asyncio.ensure_future(self.start_button_slot()))
		self.window.m_ui.stop_button.clicked.connect(self.stop_button_slot)
		self.window.m_ui.reset_button.clicked.connect(self.reset_button_slot)

	def __enter__(self):
		self.window.show()
		return self

	def __exit__(self, type, value, traceback):
		if type is not None:
			print(type, value)
			tb.print_tb(traceback)
			exit()

	def light_on_off_button_slot(self, checked: bool):
		if checked:
			self.window.m_ui.light_on_off_button.setText("СВЕТ: ВКЛ")
			self.oscil.light_on()
		else:
			self.window.m_ui.light_on_off_button.setText("СВЕТ: ВЫКЛ")
			self.oscil.light_off()

	def manual_bias_1_spin_slot(self, value):
		self.instr.set_A(value)

	def manual_bias_2_spin_slot(self, value):
		self.instr.set_B(value)

	def manual_bias_reset_1_button_slot(self):
		self.window.m_ui.manual_bias_1_spin.setValue(0.0)
		self.instr.set_A(0.0)

	def manual_bias_reset_2_button_slot(self):
		self.window.m_ui.manual_bias_2_spin.setValue(0.0)
		self.instr.set_B(0.0)

	def gen_folder_name(self, state):
		match state:
			case MeasureType.dark:
				return time.strftime("%Y-%m-%d_%H-%M-%S") + "_" + self.window.m_ui.sample_edit.text() + "_dark"
			case MeasureType.light:
				return time.strftime("%Y-%m-%d_%H-%M-%S") + "_" + self.window.m_ui.sample_edit.text() + "_light"
			case _:
				raise SystemError("Wrong state!")

	async def start_button_slot(self):
		self.status = Status.measuring
		self.instr.prepare()
		for widget in [	self.window.m_ui.sample_frame, 
						self.window.m_ui.segment_stacked, 
						self.window.m_ui.accurate_meas_check, 
						self.window.m_ui.meas_setup_widget,
						self.window.m_ui.meas_orber_box,
						self.window.m_ui.manual_panel_box,
						self.window.m_ui.reset_button,
						self.window.m_ui.start_button,
						]:
			widget.setEnabled(False)
		for meas_button, color in zip(self.window.measure_type_button_list, color_list):
			self.measure_type_list_saved.append(meas_button.state)
			if meas_button.state is MeasureType.none:
				pass
			if self.status == Status.stop:
				break
			if meas_button.state in (MeasureType.dark, MeasureType.light):
				if meas_button.state is MeasureType.dark:
					self.oscil.light_off()
				else:
					self.oscil.light_on()
				await asyncio.sleep(2)
				vac_dir = os.path.join(os.getcwd(), "test_vacs", self.gen_folder_name(meas_button.state))
				if not os.path.exists(os.path.join(os.getcwd(), "test_vacs")):
					os.mkdir(os.path.join(os.getcwd(), "test_vacs"))
				os.mkdir(vac_dir)
				with open(os.path.join(vac_dir, "vac.dat"), mode="w+") as output_f:
					await self.diode_cycle(	output_f, 
											self.window.m_ui.segment_stacked.currentWidget().main_channel,
										 	self.window.m_ui.limit_right_spin.value(), 
											self.window.m_ui.limit_left_spin.value(), 
											self.window.m_ui.step_spin.value(), 
											self.window.m_ui.delay_spin.value(),
											color)
				meas_button.set_state(MeasureType.done, color)
		else:
			self.status = Status.done
			self.window.m_ui.reset_button.setEnabled(True)
		self.instr.unprepare()


	def reset_button_slot(self):
		match self.status:
			case Status.done | Status.stop: ### Cброс кнопок режима измерения в состояние при нажатии Старт, разблокируются виджеты ###
				print(self.status.name)
				self.status = Status.ready
				for meas_button, prev_state in zip(self.window.measure_type_button_list, self.measure_type_list_saved):
					meas_button.set_state(prev_state)
				for widget in [	self.window.m_ui.sample_frame, 
								self.window.m_ui.segment_stacked, 
								self.window.m_ui.accurate_meas_check, 
								self.window.m_ui.meas_setup_widget,
								self.window.m_ui.meas_orber_box,
								self.window.m_ui.manual_panel_box,
								self.window.m_ui.start_button,
								]:
					widget.setEnabled(True)
			case Status.ready: ### Cброс кнопок режима измерения в none ###
				for meas_button in self.window.measure_type_button_list:
					meas_button.set_state(MeasureType.none)
			case _:
				print("Wrong status")

	def stop_button_slot(self):
		match self.status:
			case Status.measuring:
				self.status = Status.stop
			case Status.ready:
				pass

	async def diode_cycle(self, output_f, channel: int, right_limit, left_limit, step, delay, color):
		data_x = []
		data_y = []
		self.start_time = time.time()
		self.line = self.window.plot_widget.plotting(data_x, data_y, color, "TEST")
		for idx, voltage in enumerate(np.concatenate((	np.arange(0.0, right_limit, step), 
														np.arange(right_limit, left_limit, -step), 
														np.arange(left_limit, 0.0, step)), axis=0)):
			self.window.m_ui.statusbar.clearMessage()
			await asyncio.gather( asyncio.to_thread(self.instr.set_A, float(voltage)))
			t = time.time() - self.start_time
			if channel == 1:
				ans = await asyncio.gather( asyncio.to_thread(self.instr.measure_A))
				I, V = map(float, ans[0])
				V = round(V, 5)
				p = Point(idx, t, V, I, 0, 0)
			elif channel == 2:
				I, V = self.instr.measure_B()
				V = round(float(V), 5)
				p = Point(idx, t, 0, 0, V, I)
			else:
				raise ValueError("channel must equal 1 or 2")
			if delay != 0:
				await asyncio.sleep(delay)
			data_x.append(V)
			data_y.append(I)
			await asyncio.gather( asyncio.to_thread(output_f.write, str(p)))
			self.line.setData(data_x, data_y)
			self.window.m_ui.statusbar.showMessage(f"V = {V} V")
			if self.status is Status.stop:
				break

