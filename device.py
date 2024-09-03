import traceback as tb

class Device:
	def __init__(self, dev_obj):
		self.dev_fd = dev_obj

	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		pass

	def write(self, string: str):
		if len(string) > 0:
			self.dev_fd.write(string)
			if self.dev_fd.flush() == 0:
				raise SystemError("Couldn't write to instrument")
		else:
			raise ValueError("Cannot write an empty string")


class Ins2636B(Device):
	def __enter__(self):
			# channel A - V1
		self.write("smua.source.output = smua.OUTPUT_OFF\n")
		self.write("smua.source.func = smua.OUTPUT_DCVOLTS\n")
		self.write("smua.source.autorangev = smua.AUTORANGE_ON\n")
		self.write("smua.source.levelv = 0.0\n")
			# channel B - V2
		self.write("smub.source.output = smub.OUTPUT_OFF\n")
		self.write("smub.source.func = smub.OUTPUT_DCVOLTS\n")
		self.write("smub.source.autorangev = smub.AUTORANGE_ON\n")
		self.write("smub.source.levelv = 0.0\n")
		return self

	def __exit__(self, type, value, traceback):
		if type is not None:
			tb.print_tb(traceback)
			exit()
		self.set_A(0.0)
		self.set_B(0.0)
		self.write("smua.source.output = smua.OUTPUT_OFF\n")
		self.write("smub.source.output = smub.OUTPUT_OFF\n")

	def prepare(self):
		self.write("smua.source.output = smua.OUTPUT_ON\n")
		self.write("smub.source.output = smub.OUTPUT_ON\n")

	def set_current_limit_A(self, Imax):
		self.write(f"smua.source.limiti = {Imax}\n")

	def set_current_limit_B(self, Imax):
		self.write(f"smub.source.limiti = {Imax}\n")

	def measure_A(self): # blocking function
		self.write("i, v = smua.measure.iv()\n");
		self.write("print(i, v)\n");
		dev_output = self.dev_fd.readline();
		return dev_output.split()

	def measure_B(self): # blocking function
		self.write("i, v = smub.measure.iv()\n");
		self.write("print(i, v)\n");
		dev_output = self.dev_fd.readline();
		return dev_output.split()

	def set_A(self, voltage):
		if type(voltage) == float:
			self.write(f"smua.source.levelv = {voltage}\n")
		else:
			raise ValueError("voltage must be float")

	def set_B(self, voltage):
		if type(voltage) == float:
			self.write(f"smub.source.levelv = {voltage}\n")
		else:
			raise ValueError("voltage must be float")

	def beep(self):
		self.write("beeper.beep(1, 440.0)\n")


class InsDSO4254C(Device):
	def light_on(self):
		self.write("dds:switch on\n")

	def light_off(self):
		self.write("dds:switch off\n")

if __name__ == '__main__':
	pass
