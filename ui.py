from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import *
from PySide6.QtGui import QPalette, QColor, QPixmap, QIcon, QTransform
from PySide6 import QtCore, QtGui

import numpy as np
import pyqtgraph as pg
import sys, time
from enum import Enum, unique
from dataclasses import dataclass, asdict

from design import Ui_MainWindow

_translate = QCoreApplication.translate

color_list = (	QColor("red"),
				QColor("green"),
				QColor("blue"),
				QColor(0, 204, 204),
				QColor(255, 0, 127),
				QColor(204, 204, 0),
				QColor(128, 128, 128),
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
		self.border_width = 3
		self.min_width = 15
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
				self.setStyleSheet(f"""	border: 1px outset grey;
										border-radius: {self.border_radius}px;
										min-width: {self.min_width}px;
										padding: {self.padding}px
										""")
				self.setText(" ")

			case MeasureType.dark:
				self.setText("D")
				self.setStyleSheet(f"""	font-style: bold;
										border: 1px outset {QColor_to_str(self.border_color)};
										border-radius: {self.border_radius}px;
										min-width: {self.min_width}px;
										padding: {self.padding}px
										""")

			case MeasureType.light:
				self.setText("L")
				self.setStyleSheet(f"""	font-style: bold;
										border: 1px outset {QColor_to_str(self.border_color)};
										border-radius: {self.border_radius}px;
										min-width: {self.min_width}px;
										padding: {self.padding}px
										""")

			case MeasureType.done:
				self.setText("Done")
				if borber_color:
					self.setStyleSheet(f"""	font-style: bold;
											background-color: green;
											border: {self.padding + 1}px outset {QColor_to_str(borber_color)};
											border-radius: {self.border_radius}px;
											min-width: {self.min_width}px;
											""")
				else:
					print("borber_color is None")

class DefaultDiodeSegmentWidget(QWidget):
	def __init__(self, name: str, min_index: int, max_index: int, scheme_path: str):
		super(DefaultDiodeSegmentWidget, self).__init__()
		self.scheme_path = scheme_path
		self.name = name
		self.main_channel = 1
		self.COM = f"A{min_index}"
		self.pixel = f"A{min_index + 1}"

		self.layout = QGridLayout(self)
		self.layout.setContentsMargins(5, 2, 5, 2)
		self.layout.setSpacing(2)

		self.pixel_label = QLabel("Пиксель:")
		self.COM_label = QLabel("COM:")
		self.main_channel_label = QLabel("Канал прибора:")

		self.pixel_A_button = QPushButton("A")
		self.pixel_B_button = QPushButton("B")
		self.pixel_A_button.setDown(True)
		self.pixel_A_button.clicked.connect(self.pixel_A_button_slot)
		self.pixel_B_button.clicked.connect(self.pixel_B_button_slot)

		self.pixel_spin = QSpinBox()
		self.pixel_spin.setRange(min_index, max_index)
		self.pixel_spin.setValue(min_index)
	
		self.COM_A_max_button = QPushButton(f"A{max_index}")
		self.COM_A_min_button = QPushButton(f"A{min_index}")
		self.COM_B_max_button = QPushButton(f"B{max_index}")
		self.COM_B_min_button = QPushButton(f"B{min_index}")

		for button, slot in zip([self.COM_A_max_button, self.COM_A_min_button, self.COM_B_max_button, self.COM_B_min_button],
								[self.COM_A_max_button_slot, self.COM_A_min_button_slot, self.COM_B_max_button_slot, self.COM_B_min_button_slot]
			):
			button.setMinimumWidth(10)
			button.clicked.connect(slot)
		self.COM_A_min_button.setDown(True)

		self.main_channel_1_button = QPushButton("1")
		self.main_channel_2_button = QPushButton("2")
		self.main_channel_1_button.setDown(True)
		self.main_channel_1_button.clicked.connect(self.main_channel_1_button_slot)
		self.main_channel_2_button.clicked.connect(self.main_channel_2_button_slot)

		self.layout.addWidget(self.pixel_label, 0, 0)
		self.layout.addWidget(self.COM_label, 1, 0)
		self.layout.addWidget(self.main_channel_label, 2, 0)
		self.layout.addWidget(self.pixel_A_button, 0, 1)
		self.layout.addWidget(self.pixel_B_button, 0, 2)
		self.layout.addWidget(self.pixel_spin, 0, 3)
		self.layout.addWidget(self.COM_A_min_button, 1, 1)
		self.layout.addWidget(self.COM_A_max_button, 1, 2)
		self.layout.addWidget(self.COM_B_min_button, 1, 3)
		self.layout.addWidget(self.COM_B_max_button, 1, 4)
		self.layout.addWidget(self.main_channel_1_button, 2, 1)
		self.layout.addWidget(self.main_channel_2_button, 2, 2)
        
	def show_scheme(self):
		self.scheme_window = QMainWindow()
		self.scheme_widget = QLabel()

		self.scheme_window.setWindowTitle("Схема подложки")
		self.scheme_window.setCentralWidget(self.scheme_widget)

		#self.scheme_widget.resize(500, 500)
		pixmapImage = QPixmap(self.scheme_path)
		pixmapImage = pixmapImage.scaled(pixmapImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
		self.scheme_widget.setFixedSize(pixmapImage.size() / 2)
		self.scheme_widget.setScaledContents(True)
		self.scheme_widget.setPixmap(pixmapImage)  
		self.scheme_window.show()

	def pixel_A_button_slot(self):
		if not self.pixel_A_button.isDown():
			self.pixel = 'A' + self.pixel[1:]
			self.pixel_B_button.setDown(False)
			self.pixel_A_button.setDown(True)
		else:
			self.pixel_A_button.setDown(True)

	def pixel_B_button_slot(self):
		if not self.pixel_B_button.isDown():
			self.pixel = 'B' + self.pixel[1:]
			self.pixel_A_button.setDown(False)
			self.pixel_B_button.setDown(True)
		else:
			self.pixel_B_button.setDown(True)

	def COM_A_min_button_slot(self):
		if not self.COM_A_min_button.isDown():
			self.COM = self.COM_A_min_button.text()
			for button in [	self.COM_A_max_button,
							self.COM_B_max_button,
							self.COM_B_min_button,
							]:
				if button.isDown():
					button.setDown(False)
			self.COM_A_min_button.setDown(True)
		else:
			self.COM_A_min_button.setDown(True)

	def COM_A_max_button_slot(self):
		if not self.COM_A_min_button.isDown():
			self.COM = self.COM_A_max_button.text()
			for button in [	self.COM_A_min_button,
							self.COM_B_max_button,
							self.COM_B_min_button,
							]:
				if button.isDown():
					button.setDown(False)
			self.COM_A_max_button.setDown(True)
		else:
			self.COM_A_max_button.setDown(True)

	def COM_B_min_button_slot(self):
		if not self.COM_B_min_button.isDown():
			self.COM = self.COM_B_min_button.text()
			for button in [	self.COM_A_max_button,
							self.COM_B_max_button,
							self.COM_A_min_button,
							]:
				if button.isDown():
					button.setDown(False)
			self.COM_B_min_button.setDown(True)
		else:
			self.COM_B_min_button.setDown(True)

	def COM_B_max_button_slot(self):
		if not self.COM_B_max_button.isDown():
			self.COM = self.COM_B_max_button.text()
			for button in [	self.COM_A_max_button,
							self.COM_A_min_button,
							self.COM_B_min_button,
							]:
				if button.isDown():
					button.setDown(False)
			self.COM_B_max_button.setDown(True)
		else:
			self.COM_B_max_button.setDown(True)

	def main_channel_1_button_slot(self):
		if not self.main_channel_1_button.isDown():
			self.main_channel = 1
			self.main_channel_2_button.setDown(False)
			self.main_channel_1_button.setDown(True)
		else:
			self.main_channel_1_button.setDown(True)

	def main_channel_2_button_slot(self):
		if not self.main_channel_2_button.isDown():
			self.main_channel = 2
			self.main_channel_1_button.setDown(False)
			self.main_channel_2_button.setDown(True)
		else:
			self.main_channel_2_button.setDown(True)


class PlotWidget(pg.PlotWidget):
	def __init__(self):
		super(PlotWidget, self).__init__()
		self.setBackground("w")
		self.setMinimumSize(500, 500)
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

		self.pause_icon = QIcon('resources/pause.png')
		self.play_icon = QIcon('resources/play.png')
		self.stop_icon = QIcon('resources/stop.png')
		self.reset_icon = QIcon('resources/reset.png')
		self.arrow_pixmap = QPixmap('resources/arrow.png')
		self.larrow_icon = QIcon(self.arrow_pixmap.transformed(QTransform().rotate(90)))
		self.rarrow_icon = QIcon(self.arrow_pixmap.transformed(QTransform().rotate(-90)))

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
		self.substrate_list.append(DefaultDiodeSegmentWidget("D500", 1, 10, "./resources/D500.png"))
		self.substrate_list.append(DefaultDiodeSegmentWidget("OP1", 1, 10, "./resources/OP1.png"))
		self.substrate_list.append(DefaultDiodeSegmentWidget("OP2", 1, 15, "./resources/OP2.png")) # must be modified!!!
		#self.substrate_list.append(DefaultDiodeSegmentWidget("MD1", 1, 10, "./resources/MD1.png"))
		self.substrate_list.append(DefaultDiodeSegmentWidget("MD2", 0, 14, "./resources/MD2.png"))

		for substrate_widget in self.substrate_list:
			self.m_ui.segment_stacked.addWidget(substrate_widget)
			self.m_ui.substrate_combo.addItem(substrate_widget.name)

		self.m_ui.substrate_scheme_button.clicked.connect(self.substrate_list[0].show_scheme)
		self.m_ui.substrate_combo.activated.connect(self.substrate_combo_slot)

		self.forward_direction_flag = True
		self.m_ui.forward_dir_button.setIcon(self.larrow_icon)
		self.m_ui.forward_dir_button.setIcon(self.rarrow_icon)
		self.m_ui.forward_dir_button.setDown(self.forward_direction_flag)
		self.m_ui.backward_dir_button.clicked.connect(self.backward_dir_button_slot)
		self.m_ui.forward_dir_button.clicked.connect(self.forward_dir_button_slot)

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
		self.m_ui.pixel_stacked.setCurrentIndex(index)
		self.m_ui.substrate_scheme_button.clicked.disconnect()
		self.m_ui.substrate_scheme_button.clicked.connect(self.substrate_list[index].show_scheme)

	def sample_edit_slot(self):
		self.sample_name = self.m_ui.sample_edit.text()

	def backward_dir_button_slot(self):
		if not self.m_ui.backward_dir_button.isDown():
			self.forward_direction_flag = True
			self.m_ui.forward_dir_button.setDown(False)
			self.m_ui.backward_dir_button.setDown(True)
		else:
			self.m_ui.backward_dir_button.setDown(True)

	def forward_dir_button_slot(self):
		if not self.m_ui.forward_dir_button.isDown():
			self.forward_direction_flag = False
			self.m_ui.backward_dir_button.setDown(False)
			self.m_ui.forward_dir_button.setDown(True)
		else:
			self.m_ui.forward_dir_button.setDown(True)

	
