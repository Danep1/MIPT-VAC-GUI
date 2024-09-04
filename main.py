import argparse
import sys

from PyQt6.QtWidgets import QApplication
from device import Ins2636B, InsDSO4254C
from measure import MeasurementManager
from ui import MainWindow

INS_DEV_FILE = "/dev/usbtmc0"
OSC_DEV_FILE = "/dev/usbtmc1"

def args_parsing():
	parser = argparse.ArgumentParser(description="FET4P -- a program for measuring of charge carrier mobility of "
												"thin films in field effect transistor structure with the use of "
												"four probe method")
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = args_parsing()
	with open(INS_DEV_FILE, "w+") as instr_file, open(OSC_DEV_FILE, "w+") as osc_file, open("test.dat", "w+") as output_file:
		instrument = Ins2636B(instr_file)
		oscilloscope = InsDSO4254C(osc_file)
		app = QApplication(sys.argv)
		window = MainWindow()
		with MeasurementManager(instrument, oscilloscope, window, output_file) as manager:
			EXIT = app.exec()
	sys.exit(EXIT)
