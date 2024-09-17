import time
from dataclasses import dataclass, asdict
import numpy as np
import traceback as tb
import PySide6.QtAsyncio as QtAsyncio
import asyncio

from ui import MainWindow, QApplication, MeasureType, Point, color_list, QColor, QColor_to_str
from device import Ins2636B, InsDSO4254C


class MeasurementManager:
	def __init__(self, instr: Ins2636B, oscil: InsDSO4254C, window: MainWindow, output):
		self.instr = instr
		self.window = window
		self.oscil = oscil
		self.output_f = output

		self.stop_flag = False

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

	async def start_button_slot(self):
		self.stop_flag = False
		for widget in [	self.window.m_ui.sample_frame, 
						self.window.m_ui.segment_stacked, 
						self.window.m_ui.accurate_meas_check, 
						self.window.m_ui.meas_setup_widget,
						self.window.m_ui.meas_orber_box,
						self.window.m_ui.manual_panel_box]:
							widget.setEnabled(False)
		for meas_button, color in zip(self.window.measure_type_button_list, color_list):
			if meas_button.state is MeasureType.none:
				pass
			if self.stop_flag:
				break
			if meas_button.state in (MeasureType.dark, MeasureType.light):
				if meas_button.state is MeasureType.dark:
					self.oscil.light_off()
				else:
					self.oscil.light_on()
				await asyncio.sleep(2)
				await self.diode_cycle(self.window.m_ui.segment_stacked.currentWidget().main_channel,
											 	self.window.m_ui.limit_right_spin.value(), 
												self.window.m_ui.limit_left_spin.value(), 
												self.window.m_ui.step_spin.value(), 
												self.window.m_ui.delay_spin.value(),
												color)
				meas_button.set_state(MeasureType.done, color)



	def stop_button_slot(self):
		self.stop_flag = True
		for widget in [	self.window.m_ui.sample_frame, 
						self.window.m_ui.segment_stacked, 
						self.window.m_ui.accurate_meas_check, 
						self.window.m_ui.meas_setup_widget,
						self.window.m_ui.meas_orber_box,
						self.window.m_ui.manual_panel_box]:
							widget.setEnabled(True)

	async def diode_cycle(self, channel: int, right_limit, left_limit, step, delay, color):
		data_x = []
		data_y = []
		self.start_time = time.time()
		self.line = self.window.plot_widget.plotting(data_x, data_y, color, "TEST")
		for idx, voltage in enumerate(np.concatenate((	np.arange(0.0, right_limit, step), 
														np.arange(right_limit, left_limit, -step), 
														np.arange(left_limit, 0.0, step)), axis=0)):
			#self.instr.set_A(float(voltage))
			t = time.time() - self.start_time
			if channel == 1:
				I, V = voltage * 0.01, voltage
			elif channel == 2:
				I, V = voltage * 0.01, voltage
			else:
				raise ValueError("channel must equal 1 or 2")
			await asyncio.sleep(0.5)

			data_x.append(round(float(V), 5))
			data_y.append(round(float(I), 5))
			p = Point(idx, t, V, I, 0, 0)
			#self.output_f.write(str(p))
			self.line.setData(data_x, data_y)
			print(f"{voltage} V;") # change status bar
			if self.stop_flag is True:
				self.stop_flag = False
				break
