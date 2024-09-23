import traceback as tb
import os

class Device:
	def __init__(self, device_fd: int):
		self.device_fd = device_fd
		self.manufacture, self.product_number, self.serial_number, self.firmware_version = self.get_idn().rstrip().split(", ")
		if sum(map(len, [self.manufacture, self.product_number, self.serial_number, self.firmware_version])) == 0:
			raise SystemError("Got empty answer")
		self.check_idn()

	def get_idn(self):
		self.write("*idn?\n")
		ans = self.read()
		return ans

	def check_idn(self):
		"""Call self.get_idn() and check device model: raise SystemError if something wrong"""
		pass

	def read(self, nbyte=1000):
		s = os.read(self.device_fd, nbyte)
		if len(s) == 0:
			print("Couldn't read")
		return s.decode()

	def write(self, string: str):
		if len(string) > 0:
			r = os.write(self.device_fd, string.encode())
			#self.dev_fd.flush()
			if r == 0:
				raise SystemError("Couldn't write")
		else:
			raise ValueError("Cannot write an empty string")


class Ins2636B(Device):
	def check_idn(self):
		if self.manufacture != "Keithley Instruments Inc." or self.product_number != "Model 2636B":
			raise SystemError("Wrong /usbtmc fd connected")

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
		self.prepare()
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

	def unprepare(self):
		self.write("smua.source.output = smua.OUTPUT_OFF\n")
		self.write("smub.source.output = smub.OUTPUT_OFF\n")

	def set_current_limit_A(self, Imax):
		self.write(f"smua.source.limiti = {Imax}\n")

	def set_current_limit_B(self, Imax):
		self.write(f"smub.source.limiti = {Imax}\n")

	def measure_A(self): # blocking function
		self.write("i, v = smua.measure.iv()\n");
		self.write("print(i, v)\n");
		ans = self.read();
		return ans.split()

	def measure_B(self): # blocking function
		self.write("i, v = smub.measure.iv()\n");
		self.write("print(i, v)\n");
		ans = self.read();
		return ans.split()

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
	def check_idn(self):
		if self.manufacture != "Hantek" or self.product_number != "DSO4254C":
			raise SystemError("Wrong /usbtmc fd connected")

	def prepare(self):
		self.oscil.light_off()

	def light_on(self):
		self.write("dds:switch on\n")

	def light_off(self):
		self.write("dds:switch off\n")


if __name__ == '__main__':
	instr_fd = os.open("/dev/usbtmc0", os.O_RDWR)
	instr = Device(instr_fd)
	print(instr.get_idn())
