from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import *
from PySide6.QtGui import QPalette, QColor, QPixmap, QIcon, QTransform
from PySide6 import QtCore, QtGui

import numpy as np
import pyqtgraph as pg
import sys, time, os
from enum import Enum, unique
from dataclasses import dataclass, asdict

from design import Ui_MainWindow

_translate = QCoreApplication.translate

color_list = (	QColor("black"),
				QColor("red"),
				QColor("green"),
				QColor("blue"),
				QColor(204, 204, 0),
				QColor(255, 0, 127),
				QColor(0, 204, 204),
				QColor(255, 128, 0)
				)

def QColor_to_str(color: QColor):
	return f"rgb({color.red()}, {color.green()}, {color.blue()})"

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


@unique
class MeasureType(Enum):
	none = 0
	dark = 1
	light = 2
	done = 3

class MeasureTypeButton(QPushButton):
	def __init__(self, border_color=QColor("black")):
		super(MeasureTypeButton, self).__init__()
		self.border_radius = 5
		self.border_width_none = 1
		self.border_width = 3
		self.min_width = 10
		self.padding = 2
		self.border_color = border_color

		self.set_state(MeasureType.none)
		self.clicked.connect(self.slot)

	def slot(self):
		match self.state:
			case MeasureType.none:
				self.set_state(MeasureType.dark)

			case MeasureType.dark:
				self.set_state(MeasureType.light)

			case MeasureType.light:
				self.set_state(MeasureType.none)

	def set_state(self, new_state: MeasureType):
		self.state = new_state
		match new_state:
			case MeasureType.none:
				self.setStyleSheet(f"""	border: {self.border_width_none}px outset grey;
										border-radius: {self.border_radius}px;
										min-width: {self.min_width}px;
										padding: {self.border_width - self.border_width_none}px
										""")
				self.setText(" ")

			case MeasureType.dark:
				self.setText("D")
				self.setStyleSheet(f"""	font-style: bold;
										border: {self.border_width}px outset {QColor_to_str(self.border_color)};
										border-radius: {self.border_radius}px;
										min-width: {self.min_width}px;
										""")

			case MeasureType.light:
				self.setText("L")
				self.setStyleSheet(f"""	font-style: bold;
										border: {self.border_width}px outset {QColor_to_str(self.border_color)};
										border-radius: {self.border_radius}px;
										min-width: {self.min_width}px;
										""")

			case MeasureType.done:
				self.setText("Done")
				self.setStyleSheet(f"""	font-style: bold;
										border: {self.border_width}px outset {QColor_to_str(self.border_color)};
										border-radius: {self.border_radius}px;
										min-width: {self.min_width}px;
										""")

class DefaultDiodeSegmentWidget(QWidget):
	def __init__(self, name: str, min_index: int, max_index: int, scheme_path: str, parent=None):
		super(DefaultDiodeSegmentWidget, self).__init__(parent)
		self.name = name

		self.scheme_window = self.init_scheme_window(scheme_path)

		self.main_channel_flag = ["1"]
		self.wire_1_flag = ["A"]
		self.wire_2_flag = ["A"]

		self.setStyleSheet("QPushButton {min-width: 15}")
		self.layout = QGridLayout(self)
		self.layout.setContentsMargins(5, 2, 5, 2)
		self.layout.setSpacing(2)

		self.wire_1_label = QLabel("Щуп 1:", self)
		self.wire_2_label = QLabel("Щуп 2:", self)
		self.main_channel_label = QLabel("Канал прибора:", self)

		self.wire_1_combo = QComboBox(self)
		self.wire_2_combo = QComboBox(self)
		for index in range(min_index, max_index + 1):
			self.wire_1_combo.addItem(str(index))
			self.wire_2_combo.addItem(str(index))

		wire_1_AB_btns_pair = ConnectedBtnsPair("A", "B", self.wire_1_flag, self)
		self.wire_1_A_button = wire_1_AB_btns_pair.btn_1
		self.wire_1_B_button = wire_1_AB_btns_pair.btn_2

		wire_2_AB_btns_pair = ConnectedBtnsPair("A", "B", self.wire_2_flag, self)
		self.wire_2_A_button = wire_2_AB_btns_pair.btn_1
		self.wire_2_B_button = wire_2_AB_btns_pair.btn_2

		main_channel_btns_pair = ConnectedBtnsPair("1", "2", self.main_channel_flag, self)
		self.main_channel_1_button = main_channel_btns_pair.btn_1
		self.main_channel_2_button = main_channel_btns_pair.btn_2

		self.layout.addWidget(self.wire_1_label, 0, 0)
		self.layout.addWidget(self.wire_2_label, 1, 0)
		self.layout.addWidget(self.main_channel_label, 2, 0)
		self.layout.addWidget(self.wire_1_A_button, 0, 1)
		self.layout.addWidget(self.wire_1_B_button, 0, 2)
		self.layout.addWidget(self.wire_1_combo, 0, 3)
		self.layout.addWidget(self.wire_2_A_button, 1, 1)
		self.layout.addWidget(self.wire_2_B_button, 1, 2)
		self.layout.addWidget(self.wire_2_combo, 1, 3)
		self.layout.addWidget(self.main_channel_1_button, 2, 1)
		self.layout.addWidget(self.main_channel_2_button, 2, 2)
        
	def init_scheme_window(self, scheme_path):
		scheme_window = QMainWindow()
		scheme_widget = QLabel()

		scheme_window.setWindowTitle("Схема подложки")
		scheme_window.setCentralWidget(scheme_widget)

		pixmapImage = QPixmap(scheme_path)
		pixmapImage = pixmapImage.scaled(pixmapImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
		scheme_widget.setFixedSize(pixmapImage.size() / 2)
		scheme_widget.setScaledContents(True)
		scheme_widget.setPixmap(pixmapImage)
		return scheme_window

	def show_scheme(self):
		self.scheme_window.show()


class PlotWidget(pg.PlotWidget):
	def __init__(self):
		super(PlotWidget, self).__init__()
		self.setBackground("w")
		self.setMinimumSize(700, 500)
		styles = {"color": "black", "font-size": "16px", "font": "Calibri"}
		#self.setTitle("vac", color="b", size="20pt")
		self.setLabel("left", "Current, A", **styles)
		self.setLabel("bottom", "Bias, V", **styles)
		self.addLegend()
		self.showGrid(x=True, y=True)
		self.setXRange(-1, 1)
		self.setYRange(0, 1)
		self.getPlotItem().enableAutoRange(axis=pg.ViewBox.YAxis)
		self.zero_axis_pen = pg.mkPen(color="black", width=1)
		self.v_line = pg.InfiniteLine(pos=0, angle=0, pen=self.zero_axis_pen)
		self.h_line = pg.InfiniteLine(pos=0, angle=90, pen=self.zero_axis_pen)
		self.addItem(self.v_line)
		self.addItem(self.h_line)

	def plotting(self, x, y, color, label=" "):
		pen = pg.mkPen(color=color, width=2)
		return self.plot(x, y, pen=pen, name=label)


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.m_ui = Ui_MainWindow()
		self.m_ui.setupUi(self)

		self.m_ui.centralwidget.resize(200, 200)

		self.pause_icon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), 'resources/pause.png'))
		self.play_icon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), 'resources/play.png'))
		self.stop_icon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), 'resources/stop.png'))
		self.reset_icon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), 'resources/reset.png'))
		self.arrow_pixmap = QPixmap(os.path.join(os.path.dirname(sys.argv[0]), 'resources/arrow.png'))
		self.rarrow_icon = QIcon(self.arrow_pixmap.transformed(QTransform().rotate(90)))
		self.larrow_icon = QIcon(self.arrow_pixmap.transformed(QTransform().rotate(-90)))

		self.setWindowTitle("MIPT VAC GUI")
		
		palette = QtGui.QGuiApplication.palette()
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(120, 120, 120))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, QtGui.QColor(240, 240, 240))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(120, 120, 120))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(120, 120, 120))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, QtGui.QColor(240, 240, 240))
		self.setPalette(palette)

		self.plot_widget = PlotWidget()

		self.move(20, 20)

		self.m_ui.main_splitter.insertWidget(0, self.plot_widget)

		self.sample_name = ""
		self.m_ui.sample_edit.setPlaceholderText(f"не более {self.m_ui.sample_edit.maxLength()} символов")
		self.m_ui.sample_edit.editingFinished.connect(self.sample_edit_slot)

		self.substrate_list = []
		self.substrate_list.append(DefaultDiodeSegmentWidget("D500", 1, 10, os.path.join(os.path.dirname(sys.argv[0]), "resources/D500.png"), self))
		self.substrate_list.append(DefaultDiodeSegmentWidget("OP1", 1, 10, os.path.join(os.path.dirname(sys.argv[0]), "resources/OP1.png"), self))
		self.substrate_list.append(DefaultDiodeSegmentWidget("OP2", 1, 15, os.path.join(os.path.dirname(sys.argv[0]), "resources/OP2.png"), self)) # must be modified!!!
		#self.substrate_list.append(DefaultDiodeSegmentWidget("MD1", 1, 10, "./resources/MD1.png"))
		self.substrate_list.append(DefaultDiodeSegmentWidget("MD2", 0, 14, os.path.join(os.path.dirname(sys.argv[0]), "resources/MD2.png"), self))

		for substrate_widget in self.substrate_list:
			substrate_widget.setPalette(palette)
			self.m_ui.segment_stacked.addWidget(substrate_widget)
			self.m_ui.substrate_combo.addItem(substrate_widget.name)

		self.m_ui.substrate_scheme_button.clicked.connect(self.substrate_list[0].show_scheme)
		self.m_ui.substrate_combo.activated.connect(self.substrate_combo_slot)

		self.m_ui.start_button.setIcon(self.play_icon)
		self.m_ui.stop_button.setIcon(self.stop_icon)
		#self.m_ui.stop_button.setIcon(self.stop_icon)

		self.forward_direction_flag = [True]
		self.m_ui.forward_dir_button.setIcon(self.rarrow_icon)
		self.m_ui.backward_dir_button.setIcon(self.larrow_icon)
		self.m_ui.backward_dir_button.clicked.connect(lambda checked: connected_btns_slot(self.m_ui.backward_dir_button, [self.m_ui.backward_dir_button, self.m_ui.forward_dir_button], self.forward_direction_flag, checked))
		self.m_ui.forward_dir_button.clicked.connect(lambda checked: connected_btns_slot(self.m_ui.forward_dir_button, [self.m_ui.backward_dir_button, self.m_ui.forward_dir_button], self.forward_direction_flag, checked))

		self.m_ui.limit_left_spin.setMinimumWidth(110)
		self.m_ui.limit_left_accurate_spin.setMinimumWidth(110)

		self.m_ui.max_current_1_label.setMaximumWidth(60)
		self.m_ui.max_current_2_label.setMaximumWidth(60)

		self.m_ui.limit_left_spin.valueChanged.connect(self.limit_left_spin_slot)
		self.m_ui.limit_right_spin.valueChanged.connect(self.limit_right_spin_slot)

		self.measure_type_button_number = len(color_list)
		self.measure_type_button_list = []
		for color in color_list:
			measure_type_button = MeasureTypeButton(color)
			self.measure_type_button_list.append(measure_type_button)
			self.m_ui.horizontalLayout_5.addWidget(measure_type_button)
	
	def show_critical_error_box(self, text="Ошибка!"):
		msg_box = QMessageBox()
		msg_box.setIcon(QMessageBox.Critical)
		msg_box.setText(text)
		msg_box.setWindowTitle("Ошибка!")
		msg_box.setStandardButtons(QMessageBox.Ok)
		res = msg_box.exec()

	def limit_left_spin_slot(self, value):
		old_xrange = self.plot_widget.getPlotItem().viewRange()[0]
		self.plot_widget.setXRange(value, old_xrange[1])

	def limit_right_spin_slot(self, value):
		old_xrange = self.plot_widget.getPlotItem().viewRange()[0]
		self.plot_widget.setXRange(old_xrange[0], value)

	def substrate_combo_slot(self, index: int):
		self.m_ui.segment_stacked.setCurrentIndex(index)
		self.m_ui.substrate_scheme_button.clicked.disconnect()
		self.m_ui.substrate_scheme_button.clicked.connect(self.substrate_list[index].show_scheme)

	def sample_edit_slot(self):
		self.sample_name = self.m_ui.sample_edit.text()


def connected_btns_slot(btn, connected_btns, flag_cont, checked: bool):
	if checked:
		flag_cont[0] = btn.text()
		for other_btn in connected_btns:
			other_btn.setChecked(False) if other_btn != btn else None
	else:
		btn.setChecked(True)


class ConnectedBtnsPair:
	def __init__(self, label_1, label_2, flag_cont, parent=None):
		self.btn_1 = QPushButton(label_1, parent)
		self.btn_2 = QPushButton(label_2, parent)
		self.btn_1.setCheckable(True)
		self.btn_2.setCheckable(True)
		self.btn_1.setChecked(True)
		flag_cont[0] = label_1
		l = [self.btn_1, self.btn_2]
		self.btn_1.clicked.connect(lambda checked: connected_btns_slot(self.btn_1, l, flag_cont, checked))
		self.btn_2.clicked.connect(lambda checked: connected_btns_slot(self.btn_2, l, flag_cont, checked))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = QWidget()

	layout = QGridLayout()

	index = ["1"]
	Pair = ConnectedBtnsPair("1", "2", index)
	btn_3 = QPushButton("res")
	btn_3.clicked.connect(lambda: print(f"res: {index[0]}"))

	layout.addWidget(Pair.btn_1, 0, 0)
	layout.addWidget(Pair.btn_2, 0, 1)
	layout.addWidget(btn_3, 1, 0, 1, -1)

	window.setLayout(layout)

	window.show()
	app.exec()
