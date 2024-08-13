class Device:
	def __init__(self, path, args):
		self.dev_fd = open(path, "r+")
			# channel A - V1
		self.write("smua.source.output = smua.OUTPUT_OFF\n");
		self.write("smua.source.func = smua.OUTPUT_DCVOLTS\n");
		self.write("smua.source.autorangev = smua.AUTORANGE_ON\n");
		self.write("smua.source.levelv = 0.0\n");
		self.write(f"smua.source.limiti = {args.I1_max}\n");
			# channel B - V2
		self.write("smub.source.output = smub.OUTPUT_OFF\n");
		self.write("smub.source.func = smub.OUTPUT_DCVOLTS\n");
		self.write("smub.source.autorangev = smub.AUTORANGE_ON\n");
		self.write("smub.source.levelv = 0.0\n");
		self.write(f"smub.source.limiti = {args.I2_max}\n");

	def __del__(self):
		#self.set_A(0.0)
		#self.set_B(0.0)
		self.write("smua.source.output = smua.OUTPUT_OFF\n")
		self.write("smub.source.output = smub.OUTPUT_OFF\n");
		self.dev_fd.close()

	def write(self, string):
		self.dev_fd.write(string)
	
	def prepare(self):
		self.write("smua.source.output = smua.OUTPUT_ON\n");
		self.write("smub.source.output = smub.OUTPUT_ON\n");

	def measure_A(self):
		self.write(dev_fd, "i, v = smua.measure.iv()\n");
		self.write(dev_fd, "print(i, v)\n");
		dev_output = self.dev_fd.readline();
		return dev_output.split()

	def measure_B(self):
		self.write(dev_fd, "i, v = smub.measure.iv()\n");
		self.write(dev_fd, "print(i, v)\n");
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
	d = Device("usbtms0.a")
	
