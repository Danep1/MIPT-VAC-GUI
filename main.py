import argparse
import sys
import os

from PySide6.QtWidgets import QApplication
import PySide6.QtAsyncio as QtAsyncio

from device import Ins2636B, InsDSO4254C
from measure import MeasurementManager
from ui import MainWindow

def args_parsing():
	parser = argparse.ArgumentParser(description="MIPT-VAC-GUI - programm to measure volt-ampere")
	parser.add_argument("-o",  "--output", default="vac", type=str, help="dir to save <time, sample, mode>/vac.dat")
	parser.add_argument("--instr", default="/dev/usbtmc1", type=str, help="path to measuring instrument")
	parser.add_argument("--oscil", default="/dev/usbtmc0", type=str, help="path to oscilloscope")
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = args_parsing()
	instr_fd = os.open(args.instr, os.O_RDWR)
	oscil_fd = os.open(args.oscil, os.O_RDWR)
	app = QApplication(sys.argv)
	window = MainWindow()
	with Ins2636B(instr_fd) as instrument, InsDSO4254C(oscil_fd) as oscilloscope,
		 MeasurementManager(instrument, oscilloscope, window, args.output) as manager:
		EXIT = QtAsyncio.run()
	os.close(instr_fd)
	os.close(oscil_fd)
	sys.exit(EXIT)
