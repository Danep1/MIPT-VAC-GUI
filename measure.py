import time
from dataclasses import dataclass, asdict
import numpy as np
import traceback as tb

import PySide6.QtAsyncio as QtAsyncio
import asyncio
from enum import Enum, unique
import os

from ui import MainWindow, QApplication, MeasureType, Point, color_list, QColor, QColor_to_str, Qt
from device import Ins2636B, InsDSO4254C

@unique
class Status(Enum):
	ready = 0
	measuring = 1
	pause = 2
	stop = 3
	done = 4

class MeasurementManager:
	def __init__(self, instr: Ins2636B, oscil: InsDSO4254C, window: MainWindow, output_dir="test_vacs"):
		self.instr = instr
		self.window = window
		self.oscil = oscil
		self.output_dir = output_dir

		self.measure_type_list_saved = []
		self.status = Status.ready

		self.window.m_ui.light_on_off_button.toggled.connect(self.light_on_off_button_slot)

		self.window.m_ui.manual_bias_1_spin.valueChanged.connect(self.manual_bias_1_spin_slot)
		self.window.m_ui.manual_bias_2_spin.valueChanged.connect(self.manual_bias_2_spin_slot)

		self.window.m_ui.manual_bias_reset_1_button.clicked.connect(self.manual_bias_reset_1_button_slot)
		self.window.m_ui.manual_bias_reset_2_button.clicked.connect(self.manual_bias_reset_2_button_slot)

		self.window.m_ui.start_button.clicked.connect(lambda: asyncio.ensure_future(self.start_button_slot()))
		self.window.m_ui.stop_button.clicked.connect(self.stop_button_slot)

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

	def gen_diode_folder_name(self, sample, pixel, COM, state):
		match state:
			case MeasureType.dark:
				meas_t = "dark"
			case MeasureType.light:
				meas_t = "light"
			case _:
				raise SystemError("Wrong state!")
		return "_".join([time.strftime("%Y-%m-%d_%H-%M-%S"), sample, pixel, COM, meas_t])


	async def start_button_slot(self):
		match self.status:
			case Status.ready:
				if self.window.m_ui.sample_edit.text() == "":
					self.window.show_critical_error_box("Не указано название образца!")
					return None
				self.status = Status.measuring
				self.window.m_ui.start_button.setIcon(self.window.pause_icon)
				self.window.m_ui.stop_button.setIcon(self.window.stop_icon)
				self.instr.prepare()
				for widget in [	self.window.m_ui.sample_frame, 
								self.window.m_ui.segment_stacked, 
								self.window.m_ui.meas_setup_widget,
								self.window.m_ui.meas_orber_box,
								self.window.m_ui.manual_panel_box,
								]:
					widget.setEnabled(False)
				i = 0
				for meas_button, color in zip(self.window.measure_type_button_list, color_list):
					self.measure_type_list_saved.append(meas_button.state)
					match meas_button.state, self.status:
						case _, Status.stop:
							break
						case MeasureType.dark | MeasureType.light, _:
							i += 1
							if meas_button.state is MeasureType.dark:
								self.oscil.light_off()
								legend_name = f"{i}: dark"
								style = Qt.SolidLine
							else:
								self.oscil.light_on()
								legend_name = f"{i}: light"
								style = Qt.DotLine
							await asyncio.sleep(2)
							vac_dir = os.path.join(self.output_dir, self.gen_diode_folder_name(self.window.m_ui.sample_edit.text(),
																							self.window.m_ui.segment_stacked.currentWidget().pixel,
																							self.window.m_ui.segment_stacked.currentWidget().COM,
																							meas_button.state))
							if not os.path.exists(self.output_dir):
								os.mkdir(self.output_dir)
							os.mkdir(os.path.join(vac_dir))
							with open(os.path.join(vac_dir, "vac.dat"), mode="w+") as output_f:
								await self.diode_cycle(	output_f, 
														self.window.m_ui.segment_stacked.currentWidget().main_channel,
													 	self.window.m_ui.limit_right_spin.value(), 
														self.window.m_ui.limit_left_spin.value(), 
														self.window.m_ui.step_spin.value(), 
														self.window.m_ui.delay_spin.value(),
														color=color,
														width=3,
														style=style,
														legend_name=legend_name,
														)
							meas_button.set_state(MeasureType.done)
				else:
					self.status = Status.done
				self.oscil.light_off()
				self.window.m_ui.start_button.setIcon(self.window.play_icon)
				self.window.m_ui.stop_button.setIcon(self.window.reset_icon)
				self.instr.unprepare()
			case Status.measuring:
				self.status = Status.pause
				self.window.m_ui.start_button.setIcon(self.window.play_icon)
			case Status.pause:
				self.status = Status.measuring
				self.window.m_ui.start_button.setIcon(self.window.pause_icon)
				pass
			case Status.stop:
				pass
			case Status.done:
				pass

	def stop_button_slot(self):
		match self.status:
			case Status.ready: ### Cброс кнопок режима измерения в none ###
				for meas_button in self.window.measure_type_button_list:
					meas_button.set_state(MeasureType.none)
			case Status.measuring | Status.pause:
				self.status = Status.stop
				self.window.m_ui.stop_button.setIcon(self.window.reset_icon)
				self.window.m_ui.start_button.setIcon(self.window.play_icon)
			case Status.done | Status.stop: ### Cброс кнопок режима измерения в состояние при нажатии Старт, разблокируются виджеты, очищаем графики ###
				self.status = Status.ready
				self.window.plot_widget
				for item in self.window.plot_widget.listDataItems():
					self.window.plot_widget.removeItem(item)
				for meas_button, prev_state in zip(self.window.measure_type_button_list, self.measure_type_list_saved):
					meas_button.set_state(prev_state)
				for widget in [	self.window.m_ui.sample_frame, 
								self.window.m_ui.segment_stacked, 
								self.window.m_ui.meas_setup_widget,
								self.window.m_ui.meas_orber_box,
								self.window.m_ui.manual_panel_box,
								]:
					widget.setEnabled(True)

	async def diode_cycle(self, output_f, channel: int, right_limit, left_limit, step, delay, color="black", width=2, style=Qt.SolidLine, legend_name=""):
		data_x = []
		data_y = []
		start_time = time.time()
		line = self.window.plot_widget.plotting(data_x, data_y, color, legend_name)
		x_grid = np.concatenate((	np.arange(0.0, right_limit, step),
									np.arange(right_limit, left_limit, -step),
									np.arange(left_limit, step, step)), axis=0)
		line.setPen(color=color, width=2, style=style)
		if self.window.forward_direction_flag is False:
			pass #np.flip(x_grid)
		for idx, voltage in enumerate(x_grid):
			self.window.m_ui.statusbar.clearMessage()
			match self.status:
				case Status.measuring:
					await asyncio.gather( asyncio.to_thread(self.instr.set_A, float(voltage)))
					self.window.m_ui.statusbar.showMessage(f"V = {V} V")
					t = time.time() - start_time
					if channel == 1:
						ans = await asyncio.gather( asyncio.to_thread(self.instr.measure_A))
						I, V = map(float, ans[0])
						p = Point(idx, t, V, I, 0, 0)
					elif channel == 2:
						ans = await asyncio.gather( asyncio.to_thread(self.instr.measure_A))
						I, V = map(float, ans[0])
						p = Point(idx, t, V, I, 0, 0)
					else:
						raise ValueError("channel must equal 1 or 2")
					if delay != 0:
						await asyncio.sleep(delay)
					data_x.append(V)
					data_y.append(I)
					r = await asyncio.gather( asyncio.to_thread(output_f.write, str(p)))
					if r == 0:
						raise SystemError("Couldn't write into file")
					line.setData(data_x, data_y)
				case Status.pause:
					while self.status == Status.pause:
						await asyncio.sleep(0.01)
				case Status.stop:
					break
				case _:
					pass

