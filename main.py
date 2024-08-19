import argparse
from dataclasses import dataclass, asdict
import pyqtgraph as pg
from PyQt6 import QtWidgets


from device import Device
from measure import *

INS_DEV_FILE = "usbtms0.a"

@dataclass
class args_min:
	V1_start:	float=-20.0
	V1_stop:	float=-20.0
	V1_step:	float=0.001
	I1_max:		float=0.00
	V2_start:	float=-20.0
	V2_stop:	float=-20.0
	V2_step:	float=0.001
	I2_max:		float=0.001
	delay:		float=0.0


@dataclass
class args_max:
	V1_start:	float=20.0
	V1_stop:	float=20.0
	V1_step:	float=1.0
	I1_max:		float=5.0
	V2_start:	float=20.0
	V2_stop:	float=20.0
	V2_step:	float=1.0
	I2_max:		float=5.0
	delay:		float=10.0

@dataclass
class args_default:
	V1_start:	float=0.0
	V1_stop:	float=0.0
	V1_step:	float=0.1
	I1_max:		float=0.01
	V2_start:	float=0.0
	V2_stop:	float=0.0
	V2_step:	float=0.1
	I2_max:		float=0.01
	delay:		float=0.1


def args_parsing():
	parser = argparse.ArgumentParser(description="FET4P -- a program for measuring of charge carrier mobility of "
												"thin films in field effect transistor structure with the use of "
												"four probe method")
	parser.add_argument("sample", 		type=str,	help="Sample name")
	parser.add_argument("--Chan", 		type=int,	default=1,	help="Scanning channel   (1 or 2, default 1 )")
	parser.add_argument("--V1_start",	type=float,	default=args_default.V1_start,	help=f"Start voltage, V   ({args_min.V1_start} - {args_max.V1_start}, default {args_default.V1_start} )")
	parser.add_argument("--V1_stop",	type=float,	default=args_default.V1_stop,	help=f"Stop voltage, V    ({args_min.V1_stop} - {args_max.V1_stop}, default {args_default.V1_stop} )")
	parser.add_argument("--V1_step",	type=float,	default=args_default.V1_step,	help=f"Voltage step, V    ({args_min.V1_step} - {args_max.V1_step}, default {args_default.V1_step} )")
	parser.add_argument("--I1_max",		type=float,	default=args_default.I1_max,	help=f"Maximum current, A ({args_min.I1_max} - {args_max.I1_max}, default {args_default.I1_max} )")
	parser.add_argument("--V2_start",	type=float,	default=args_default.V2_start,	help=f"Start voltage, V   ({args_min.V2_start} - {args_max.V2_start}, default {args_default.V2_start} )")
	parser.add_argument("--V2_stop",	type=float,	default=args_default.V2_stop,	help=f"Stop voltage, V    ({args_min.V2_stop} - {args_max.V2_stop}, default {args_default.V2_stop} )")
	parser.add_argument("--V2_step",	type=float,	default=args_default.V2_step,	help=f"Voltage step, V    ({args_min.V2_step} - {args_max.V2_step}, default {args_default.V2_step} )")
	parser.add_argument("--I2_max",		type=float,	default=args_default.I2_max,	help=f"Maximum current, A ({args_min.I2_max} - {args_max.I2_max}, default {args_default.I2_max} )")
	parser.add_argument("--delay",		type=float,	default=args_default.delay,		help=f"Scanning delay time, s ({args_min.delay} - {args_max.delay}, default {args_default.delay} )")
	args = parser.parse_args()
	return args

def args_check(args):
	if args.Chan not in [1, 2]:
		raise ValueError("<Chan> is out of range. See \"fet4p --help\"")
	for arg, value in vars(args).items():
		if arg not in ["sample", "Chan"] and (value < args_min.__dict__[arg] or value > args_max.__dict__[arg]):
			raise ValueError(f"<{arg}> is out of range. See \"fet4p --help\"")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)

    def plot(self, x, y):
        self.plot_graph.plot(x, y)

def main():
	args = args_parsing()
	args_check(args)
	app = QtWidgets.QApplication([])
	main = MainWindow()
	with open("/dev/usbtmc0", "w+") as dev_file, Device(dev_file, args) as device:
		with open("test.dat", "w+") as out_file, MeasureManager(device, out_file, args) as mm:
			x, y = mm.single_channel_cycle("A", 0.0, 1e-2, 1e-3, 0.0)
			main.plot(x, y)

	main.show()
	app.exec()


if __name__ == '__main__':
	main()
