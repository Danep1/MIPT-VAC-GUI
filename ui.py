from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import *
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6 import QtCore

import numpy as np
import pyqtgraph as pg
import sys, time
from enum import Enum, unique
from dataclasses import dataclass, asdict

from design import Ui_MainWindow

_translate = QCoreApplication.translate

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
	def __init__(self):
		super(MeasureTypeButton, self).__init__()
		self.state = MeasureType.none
		self.setMinimumSize(37, 24)
		self.setText(" ")
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
				self.setDown(False)
				self.setStyleSheet('QPushButton')
				self.setText(" ")

			case MeasureType.dark:
				self.setDown(True)
				self.setStyleSheet('QPushButton {background-color: blue}')
				self.setText("D")

			case MeasureType.light:
				self.setDown(True)
				self.setStyleSheet('QPushButton {background-color: red}')
				self.setText("L")

			case MeasureType.done:
				self.setDown(True)
				self.setStyleSheet('QPushButton {background-color: green}')
				self.setText("Done")


class DefaultDiodeSegmentWidget(QWidget):
	def __init__(self, name: str, min_index: int, max_index: int, scheme_path: str):
		super(DefaultDiodeSegmentWidget, self).__init__()
		self.scheme_path = scheme_path
		self.name = name
		self.main_channel = 1

		self.toggle_segment_flag = False
		self.toggle_COM_flag = False
		self.toggle_main_channel_flag = False

		self.layout = QGridLayout(self)

		self.segment_label = QLabel("Сегмент:")
		self.COM_label = QLabel("COM:")
		self.main_channel_label = QLabel("Канал прибора:")

		self.segment_A_button = QPushButton("A")
		self.segment_B_button = QPushButton("B")
		self.segment_A_button.setCheckable(True)
		self.segment_B_button.setCheckable(True)
		self.segment_A_button.setChecked(True)
		self.segment_A_button.toggled.connect(self.segment_A_button_slot)
		self.segment_B_button.toggled.connect(self.segment_B_button_slot)

		self.COM_A_button = QPushButton("A")
		self.COM_B_button = QPushButton("B")
		self.COM_A_button.setCheckable(True)
		self.COM_B_button.setCheckable(True)
		self.COM_A_button.setChecked(True)
		self.COM_A_button.toggled.connect(self.COM_A_button_slot)
		self.COM_B_button.toggled.connect(self.COM_B_button_slot)

		self.segment_spin = QSpinBox()
		self.segment_spin.setRange(min_index + 1, max_index - 1)
		self.segment_spin.setValue(min_index + 1)
	
		self.COM_spin = QSpinBox()
		self.COM_spin.setRange(min_index, max_index)
		self.COM_spin.setSingleStep(max_index - min_index)
		self.COM_spin.setValue(max_index)

		self.main_channel_1_button = QPushButton("1")
		self.main_channel_2_button = QPushButton("2")
		self.main_channel_1_button.setCheckable(True)
		self.main_channel_2_button.setCheckable(True)
		self.main_channel_1_button.setChecked(True)
		self.main_channel_1_button.toggled.connect(self.main_channel_1_button_slot)
		self.main_channel_2_button.toggled.connect(self.main_channel_2_button_slot)

		self.layout.addWidget(self.segment_label, 0, 0)
		self.layout.addWidget(self.COM_label, 1, 0)
		self.layout.addWidget(self.main_channel_label, 2, 0)
		self.layout.addWidget(self.segment_A_button, 0, 1)
		self.layout.addWidget(self.segment_B_button, 0, 2)
		self.layout.addWidget(self.segment_spin, 0, 3)
		self.layout.addWidget(self.COM_A_button, 1, 1)
		self.layout.addWidget(self.COM_B_button, 1, 2)
		self.layout.addWidget(self.COM_spin, 1, 3)
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

	def segment_A_button_slot(self, checked: bool):
		if self.toggle_segment_flag is False:
			self.toggle_segment_flag = True
			self.segment_B_button.toggle()
		else:
			self.toggle_segment_flag = False

	def segment_B_button_slot(self, checked: bool):
		if self.toggle_segment_flag is False:
			self.toggle_segment_flag = True
			self.segment_A_button.toggle()
		else:
			self.toggle_segment_flag = False

	def COM_A_button_slot(self, checked: bool):
		if self.toggle_COM_flag is False:
			self.toggle_COM_flag = True
			self.COM_B_button.toggle()
		else:
			self.toggle_COM_flag = False

	def COM_B_button_slot(self, checked: bool):
		if self.toggle_COM_flag is False:
			self.toggle_COM_flag = True
			self.COM_A_button.toggle()
		else:
			self.toggle_COM_flag = False
	
	def main_channel_1_button_slot(self, checked: bool):
		if self.toggle_main_channel_flag is False:
			self.main_channel = 1
			self.toggle_main_channel_flag = True
			self.main_channel_2_button.toggle()
		else:
			self.toggle_main_channel_flag = False

	def main_channel_2_button_slot(self, checked: bool):
		if self.toggle_main_channel_flag is False:
			self.main_channel = 2
			self.toggle_main_channel_flag = True
			self.main_channel_1_button.toggle()
		else:
			self.toggle_main_channel_flag = False


class PlotWidget(pg.PlotWidget):
	def __init__(self):
		super(PlotWidget, self).__init__()

		self.setBackground("w")
		self.setMinimumSize(500, 500)
		styles = {"color": "black", "font-size": "18px", "font": "Calibri"}
		#self.setTitle("vac", color="b", size="20pt")
		self.setLabel("left", "Current, A", **styles)
		self.setLabel("bottom", "Bias, V", **styles)
		self.addLegend()
		self.showGrid(x=True, y=True)
		self.setXRange(-1, 1)
		self.setYRange(0, 1)
		self.getPlotItem().enableAutoRange(axis=pg.ViewBox.YAxis)


	def plotting(self, x, y, color, label=" "):
		pen = pg.mkPen(color=color, width=5)
		return self.plot(x, y, pen=pen, name=label)


class OutputWidget(QLabel):
	def __init__(self):
		super(OutputWidget, self).__init__()

		self.setText("TEST")


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.m_ui = Ui_MainWindow()
		self.m_ui.setupUi(self)
		
		palette = QtGui.QGuiApplication.palette()
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(120, 120, 120))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, QtGui.QColor(240, 240, 240))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(120, 120, 120))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(120, 120, 120))
		palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, QtGui.QColor(240, 240, 240))
		self.setPalette(palette)

		self.plot_widget = PlotWidget()
		self.output_widget = OutputWidget()
		self.vsplitter = QSplitter(Qt.Orientation.Vertical)

		self.move(20, 20)

		self.vsplitter.addWidget(self.plot_widget)
		self.vsplitter.addWidget(self.output_widget)
		self.m_ui.main_splitter.insertWidget(0, self.vsplitter)

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

		self.m_ui.accurate_meas_box.setEnabled(False)
		self.m_ui.accurate_meas_check.stateChanged.connect(self.accurate_meas_check_slot)

		self.forward_direction_flag = True
		self.toggle_flag = False
		self.m_ui.backward_dir_button.toggled.connect(self.backward_dir_button_slot)
		self.m_ui.forward_dir_button.toggled.connect(self.forward_dir_button_slot)

		self.m_ui.limit_left_spin.valueChanged.connect(self.limit_left_spin_slot)
		self.m_ui.limit_right_spin.valueChanged.connect(self.limit_right_spin_slot)

		self.measure_type_button_number = 8
		self.measure_type_button_list = []
		for i in range(self.measure_type_button_number):
			measure_type_button = MeasureTypeButton()
			self.measure_type_button_list.append(measure_type_button)
			self.m_ui.horizontalLayout_5.addWidget(measure_type_button)
	
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

	def accurate_meas_check_slot(self):
		self.m_ui.accurate_meas_box.setEnabled(self.m_ui.accurate_meas_check.checkState() is Qt.CheckState.Checked)

	def backward_dir_button_slot(self, checked: bool):
		if self.toggle_flag is False:
			self.forward_direction_flag = not checked
			self.toggle_flag = True
			self.m_ui.forward_dir_button.toggle()
		else:
			self.toggle_flag = False

	def forward_dir_button_slot(self, checked: bool):
		if self.toggle_flag is False:
			self.forward_direction_flag = checked
			self.toggle_flag = True
			self.m_ui.backward_dir_button.toggle()
		else:
			self.toggle_flag = False

	
