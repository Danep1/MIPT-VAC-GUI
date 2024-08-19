import traceback as tb

class Device:
	def __init__(self, dev_obj, args):
		self.dev_fd = dev_obj
		self.args = args

	def __enter__(self):
			# channel A - V1
		self.write("smua.source.output = smua.OUTPUT_OFF\n");
		self.write("smua.source.func = smua.OUTPUT_DCVOLTS\n");
		self.write("smua.source.autorangev = smua.AUTORANGE_ON\n");
		self.write("smua.source.levelv = 0.0\n");
		self.write(f"smua.source.limiti = {self.args.I1_max}\n");
			# channel B - V2
		self.write("smub.source.output = smub.OUTPUT_OFF\n");
		self.write("smub.source.func = smub.OUTPUT_DCVOLTS\n");
		self.write("smub.source.autorangev = smub.AUTORANGE_ON\n");
		self.write("smub.source.levelv = 0.0\n");
		self.write(f"smub.source.limiti = {self.args.I2_max}\n");
		return self

	def __exit__(self, type, value, traceback):
		if type is not None:
			tb.print_tb(traceback)
			exit()
		self.set_A(0.0)
		self.set_B(0.0)
		self.write("smua.source.output = smua.OUTPUT_OFF\n")
		self.write("smub.source.output = smub.OUTPUT_OFF\n");

	def write(self, string: str):
		if len(string) > 0:
			self.dev_fd.write(string)
			if self.dev_fd.flush() == 0:
				raise SystemError("Couldn't write to device")
		else:
			raise ValueError("Cannot write an empty string")
	
	def prepare(self):
		self.write("smua.source.output = smua.OUTPUT_ON\n");
		self.write("smub.source.output = smub.OUTPUT_ON\n");

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
		self.write("beeper.beep(1, 440.0)")



if __name__ == '__main__':
	pass
