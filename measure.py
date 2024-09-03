import time
from dataclasses import dataclass, asdict
import numpy as np
import traceback as tb

from ui import MainWindow, QApplication
from device import Ins2636B, InsDSO4254C

@dataclass
class VAC:
	data: list

@dataclass
class MeasurementParameters:
	regime:	str
	V1_start:	float
	V1_stop:	float
	V1_step:	float
	I1_max:	float
	V2_start:	float
	V2_stop:	float
	V2_step:	float
	I2_max:	float
	delay:	float

@dataclass
class Point:
	idx:	int
	t: 	float
	V1: 	float
	I1: 	float
	V2: 	float
	I2: 	float

	def __str__(self):
		return '\t'.join(map(str, vars(self).values())) + '\n'

class MeasurementManager:
	def __init__(self, instr: Ins2636B, oscil: InsDSO4254C, window: MainWindow, output):
		self.instr = instr
		self.window = window
		self.oscil = oscil
		self.output_f = output


		self.window.m_ui.light_on_off_button.toggled.connect(self.light_on_off_button_slot)

		self.window.m_ui.manual_bias_1_spin.valueChanged.connect(self.manual_bias_1_spin_slot)
		self.window.m_ui.manual_bias_2_spin.valueChanged.connect(self.manual_bias_2_spin_slot)

		self.window.m_ui.manual_bias_reset_1_button.clicked.connect(self.manual_bias_reset_1_button_slot)
		self.window.m_ui.manual_bias_reset_2_button.clicked.connect(self.manual_bias_reset_2_button_slot)


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


	def single_channel_cycle(self, channel: int, start, stop, step, delay):
		data_x = []
		data_y = []
		if channel == 1:
			for idx, voltage in enumerate(np.arange(start, stop, step)):
				self.dev_obj.set_A(float(voltage))
				t = time.time() - self.start_time
				I, V = self.dev_obj.measure_A()
				data_x.append(round(float(V), 4))
				data_y.append(round(float(I), 4))
				p = Point(idx, t, V, I, 0, 0)
				self.output_f.write(str(p))
		return data_x, data_y

