import argparse
import sys
import os

from PySide6.QtWidgets import QApplication
import PySide6.QtAsyncio as QtAsyncio

from device import Ins2636B, InsDSO4254C
from measure import MeasurementManager
from ui import MainWindow

INS_DEV_FILE = "./dev/usbtmc2"
OSC_DEV_FILE = "./dev/usbtmc1"

def args_parsing():
	parser = argparse.ArgumentParser(description="FET4P -- a program for measuring of charge carrier mobility of "
												"thin films in field effect transistor structure with the use of "
												"four probe method")
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = args_parsing()
	with open("test.dat", "w+") as output_file:
		instr_fd = os.open(INS_DEV_FILE, os.O_RDWR)
		oscil_fd = os.open(OSC_DEV_FILE, os.O_RDWR)
		instrument = Ins2636B(instr_fd)
		oscilloscope = InsDSO4254C(oscil_fd)
		app = QApplication(sys.argv)
		window = MainWindow()
		with MeasurementManager(instrument, oscilloscope, window, output_file) as manager:
			EXIT = QtAsyncio.run()
		os.close(instr_fd)
		os.close(oscil_fd)
	sys.exit(EXIT)
