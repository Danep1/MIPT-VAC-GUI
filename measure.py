import time
from dataclasses import dataclass, asdict
import numpy as np
import traceback as tb

from device import *

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

class MeasureManager:
	def __init__(self, device: Device, output, args):
		self.args = args
		self.dev_obj = device
		self.output_f = output


	def __enter__(self):
		self.dev_obj.prepare()
		self.start_time = time.time()
		return self

	def __exit__(self, type, value, traceback):
		if type is not None:
			print(type, value)
			tb.print_tb(traceback)
			exit()



	def single_channel_cycle(self, channel: str, start, stop, step, delay):
		data_x = []
		data_y = []
		if channel.upper() == "A":
			for idx, voltage in enumerate(np.arange(start, stop, step)):
				self.dev_obj.set_A(float(voltage))
				t = time.time() - self.start_time
				I, V = self.dev_obj.measure_A()
				data_x.append(round(float(V), 4))
				data_y.append(round(float(I), 4))
				p = Point(idx, t, V, I, 0, 0)
				self.output_f.write(str(p))

		return data_x, data_y
