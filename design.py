# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSplitter,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(533, 708)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.main_splitter = QSplitter(self.centralwidget)
        self.main_splitter.setObjectName(u"main_splitter")
        self.main_splitter.setOrientation(Qt.Horizontal)
        self.control_panel_widget = QWidget(self.main_splitter)
        self.control_panel_widget.setObjectName(u"control_panel_widget")
        self.verticalLayout = QVBoxLayout(self.control_panel_widget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sample_frame = QFrame(self.control_panel_widget)
        self.sample_frame.setObjectName(u"sample_frame")
        self.gridLayout_3 = QGridLayout(self.sample_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(2)
        self.substrate_label = QLabel(self.sample_frame)
        self.substrate_label.setObjectName(u"substrate_label")

        self.gridLayout_3.addWidget(self.substrate_label, 1, 0, 1, 1)

        self.sample_label = QLabel(self.sample_frame)
        self.sample_label.setObjectName(u"sample_label")

        self.gridLayout_3.addWidget(self.sample_label, 0, 0, 1, 1)

        self.substrate_combo = QComboBox(self.sample_frame)
        self.substrate_combo.setObjectName(u"substrate_combo")

        self.gridLayout_3.addWidget(self.substrate_combo, 1, 1, 1, 1)

        self.sample_edit = QLineEdit(self.sample_frame)
        self.sample_edit.setObjectName(u"sample_edit")
        self.sample_edit.setMaxLength(20)
        self.sample_edit.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.sample_edit, 0, 1, 1, 2)

        self.substrate_scheme_button = QPushButton(self.sample_frame)
        self.substrate_scheme_button.setObjectName(u"substrate_scheme_button")

        self.gridLayout_3.addWidget(self.substrate_scheme_button, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.sample_frame)

        self.segment_stacked = QStackedWidget(self.control_panel_widget)
        self.segment_stacked.setObjectName(u"segment_stacked")

        self.verticalLayout.addWidget(self.segment_stacked)

        self.accurate_meas_check = QCheckBox(self.control_panel_widget)
        self.accurate_meas_check.setObjectName(u"accurate_meas_check")

        self.verticalLayout.addWidget(self.accurate_meas_check)

        self.meas_setup_widget = QWidget(self.control_panel_widget)
        self.meas_setup_widget.setObjectName(u"meas_setup_widget")
        self.gridLayout_5 = QGridLayout(self.meas_setup_widget)
        self.gridLayout_5.setSpacing(2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 2, 0, 2)
        self.direction_box = QGroupBox(self.meas_setup_widget)
        self.direction_box.setObjectName(u"direction_box")
        self.horizontalLayout_6 = QHBoxLayout(self.direction_box)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.backward_dir_button = QPushButton(self.direction_box)
        self.backward_dir_button.setObjectName(u"backward_dir_button")
        self.backward_dir_button.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.backward_dir_button)

        self.forward_dir_button = QPushButton(self.direction_box)
        self.forward_dir_button.setObjectName(u"forward_dir_button")
        self.forward_dir_button.setCheckable(True)
        self.forward_dir_button.setChecked(True)

        self.horizontalLayout_6.addWidget(self.forward_dir_button)


        self.gridLayout_5.addWidget(self.direction_box, 3, 1, 1, 1)

        self.common_meas_box = QGroupBox(self.meas_setup_widget)
        self.common_meas_box.setObjectName(u"common_meas_box")
        self.gridLayout_6 = QGridLayout(self.common_meas_box)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(5)
        self.gridLayout_6.setContentsMargins(5, 5, 5, 5)
        self.limit_left_label = QLabel(self.common_meas_box)
        self.limit_left_label.setObjectName(u"limit_left_label")
        self.limit_left_label.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_6.addWidget(self.limit_left_label, 0, 0, 1, 1)

        self.limit_left_spin = QDoubleSpinBox(self.common_meas_box)
        self.limit_left_spin.setObjectName(u"limit_left_spin")
        self.limit_left_spin.setMinimum(-20.000000000000000)
        self.limit_left_spin.setMaximum(20.000000000000000)
        self.limit_left_spin.setValue(-1.000000000000000)

        self.gridLayout_6.addWidget(self.limit_left_spin, 0, 1, 1, 1)

        self.limit_right_label = QLabel(self.common_meas_box)
        self.limit_right_label.setObjectName(u"limit_right_label")

        self.gridLayout_6.addWidget(self.limit_right_label, 1, 0, 1, 1)

        self.limit_right_spin = QDoubleSpinBox(self.common_meas_box)
        self.limit_right_spin.setObjectName(u"limit_right_spin")
        self.limit_right_spin.setMinimum(-20.000000000000000)
        self.limit_right_spin.setMaximum(20.000000000000000)
        self.limit_right_spin.setValue(1.000000000000000)

        self.gridLayout_6.addWidget(self.limit_right_spin, 1, 1, 1, 1)

        self.step_label = QLabel(self.common_meas_box)
        self.step_label.setObjectName(u"step_label")

        self.gridLayout_6.addWidget(self.step_label, 2, 0, 1, 1)

        self.step_spin = QDoubleSpinBox(self.common_meas_box)
        self.step_spin.setObjectName(u"step_spin")
        self.step_spin.setDecimals(3)
        self.step_spin.setMinimum(0.001000000000000)
        self.step_spin.setMaximum(1.000000000000000)
        self.step_spin.setSingleStep(0.005000000000000)
        self.step_spin.setValue(0.100000000000000)

        self.gridLayout_6.addWidget(self.step_spin, 2, 1, 1, 1)

        self.delay_label = QLabel(self.common_meas_box)
        self.delay_label.setObjectName(u"delay_label")

        self.gridLayout_6.addWidget(self.delay_label, 3, 0, 1, 1)

        self.delay_spin = QDoubleSpinBox(self.common_meas_box)
        self.delay_spin.setObjectName(u"delay_spin")
        self.delay_spin.setMaximum(30.000000000000000)
        self.delay_spin.setSingleStep(0.100000000000000)

        self.gridLayout_6.addWidget(self.delay_spin, 3, 1, 1, 1)


        self.gridLayout_5.addWidget(self.common_meas_box, 0, 0, 1, 1)

        self.accurate_meas_box = QGroupBox(self.meas_setup_widget)
        self.accurate_meas_box.setObjectName(u"accurate_meas_box")
        self.gridLayout = QGridLayout(self.accurate_meas_box)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.limit_left_accurate_label = QLabel(self.accurate_meas_box)
        self.limit_left_accurate_label.setObjectName(u"limit_left_accurate_label")

        self.gridLayout.addWidget(self.limit_left_accurate_label, 0, 1, 1, 1)

        self.delay_accurate_label = QLabel(self.accurate_meas_box)
        self.delay_accurate_label.setObjectName(u"delay_accurate_label")

        self.gridLayout.addWidget(self.delay_accurate_label, 4, 1, 1, 1)

        self.limit_right_accurate_label = QLabel(self.accurate_meas_box)
        self.limit_right_accurate_label.setObjectName(u"limit_right_accurate_label")

        self.gridLayout.addWidget(self.limit_right_accurate_label, 1, 1, 1, 1)

        self.limit_left_accurate_spin = QDoubleSpinBox(self.accurate_meas_box)
        self.limit_left_accurate_spin.setObjectName(u"limit_left_accurate_spin")
        self.limit_left_accurate_spin.setMinimum(-20.000000000000000)
        self.limit_left_accurate_spin.setMaximum(20.000000000000000)
        self.limit_left_accurate_spin.setValue(-0.500000000000000)

        self.gridLayout.addWidget(self.limit_left_accurate_spin, 0, 3, 1, 1)

        self.delay_accurate_spin = QDoubleSpinBox(self.accurate_meas_box)
        self.delay_accurate_spin.setObjectName(u"delay_accurate_spin")
        self.delay_accurate_spin.setMaximum(30.000000000000000)
        self.delay_accurate_spin.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.delay_accurate_spin, 4, 3, 1, 1)

        self.limit_right_accurate_spin = QDoubleSpinBox(self.accurate_meas_box)
        self.limit_right_accurate_spin.setObjectName(u"limit_right_accurate_spin")
        self.limit_right_accurate_spin.setMinimum(-20.000000000000000)
        self.limit_right_accurate_spin.setMaximum(20.000000000000000)
        self.limit_right_accurate_spin.setValue(-0.500000000000000)

        self.gridLayout.addWidget(self.limit_right_accurate_spin, 1, 3, 1, 1)

        self.step_accurate_spin = QDoubleSpinBox(self.accurate_meas_box)
        self.step_accurate_spin.setObjectName(u"step_accurate_spin")
        self.step_accurate_spin.setDecimals(3)
        self.step_accurate_spin.setMinimum(0.001000000000000)
        self.step_accurate_spin.setMaximum(1.000000000000000)
        self.step_accurate_spin.setSingleStep(0.005000000000000)
        self.step_accurate_spin.setValue(0.050000000000000)

        self.gridLayout.addWidget(self.step_accurate_spin, 2, 3, 1, 1)

        self.step_accurate_label = QLabel(self.accurate_meas_box)
        self.step_accurate_label.setObjectName(u"step_accurate_label")

        self.gridLayout.addWidget(self.step_accurate_label, 2, 1, 1, 1)


        self.gridLayout_5.addWidget(self.accurate_meas_box, 0, 1, 1, 1)

        self.max_current_box = QGroupBox(self.meas_setup_widget)
        self.max_current_box.setObjectName(u"max_current_box")
        self.gridLayout_4 = QGridLayout(self.max_current_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(2)
        self.gridLayout_4.setContentsMargins(11, 2, 11, 2)
        self.max_current_1_label = QLabel(self.max_current_box)
        self.max_current_1_label.setObjectName(u"max_current_1_label")

        self.gridLayout_4.addWidget(self.max_current_1_label, 0, 0, 1, 1)

        self.max_current_1_spin = QDoubleSpinBox(self.max_current_box)
        self.max_current_1_spin.setObjectName(u"max_current_1_spin")
        self.max_current_1_spin.setMaximum(5.000000000000000)
        self.max_current_1_spin.setValue(0.010000000000000)

        self.gridLayout_4.addWidget(self.max_current_1_spin, 0, 1, 1, 1)

        self.max_current_2_label = QLabel(self.max_current_box)
        self.max_current_2_label.setObjectName(u"max_current_2_label")

        self.gridLayout_4.addWidget(self.max_current_2_label, 0, 2, 1, 1)

        self.max_current_2_spin = QDoubleSpinBox(self.max_current_box)
        self.max_current_2_spin.setObjectName(u"max_current_2_spin")
        self.max_current_2_spin.setMaximum(5.000000000000000)
        self.max_current_2_spin.setValue(0.010000000000000)

        self.gridLayout_4.addWidget(self.max_current_2_spin, 0, 4, 1, 1)


        self.gridLayout_5.addWidget(self.max_current_box, 1, 0, 1, 2)

        self.direction_label = QLabel(self.meas_setup_widget)
        self.direction_label.setObjectName(u"direction_label")

        self.gridLayout_5.addWidget(self.direction_label, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.meas_setup_widget)

        self.meas_orber_box = QGroupBox(self.control_panel_widget)
        self.meas_orber_box.setObjectName(u"meas_orber_box")
        self.meas_orber_box.setEnabled(True)
        self.horizontalLayout_5 = QHBoxLayout(self.meas_orber_box)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")

        self.verticalLayout.addWidget(self.meas_orber_box)

        self.meas_control_box = QGroupBox(self.control_panel_widget)
        self.meas_control_box.setObjectName(u"meas_control_box")
        self.horizontalLayout_4 = QHBoxLayout(self.meas_control_box)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 2, -1, 2)
        self.start_button = QPushButton(self.meas_control_box)
        self.start_button.setObjectName(u"start_button")

        self.horizontalLayout_4.addWidget(self.start_button)

        self.stop_button = QPushButton(self.meas_control_box)
        self.stop_button.setObjectName(u"stop_button")

        self.horizontalLayout_4.addWidget(self.stop_button)

        self.pause_button = QPushButton(self.meas_control_box)
        self.pause_button.setObjectName(u"pause_button")
        self.pause_button.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.pause_button)

        self.U__button = QPushButton(self.meas_control_box)
        self.U__button.setObjectName(u"U__button")
        self.U__button.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.U__button)

        self.next_button = QPushButton(self.meas_control_box)
        self.next_button.setObjectName(u"next_button")
        self.next_button.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.next_button)

        self.reset_button = QPushButton(self.meas_control_box)
        self.reset_button.setObjectName(u"reset_button")

        self.horizontalLayout_4.addWidget(self.reset_button)


        self.verticalLayout.addWidget(self.meas_control_box)

        self.manual_panel_box = QGroupBox(self.control_panel_widget)
        self.manual_panel_box.setObjectName(u"manual_panel_box")
        self.gridLayout_2 = QGridLayout(self.manual_panel_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(-1, 2, -1, 2)
        self.light_on_off_button = QPushButton(self.manual_panel_box)
        self.light_on_off_button.setObjectName(u"light_on_off_button")
        self.light_on_off_button.setCheckable(True)

        self.gridLayout_2.addWidget(self.light_on_off_button, 0, 0, 1, 1)

        self.manual_1_box = QGroupBox(self.manual_panel_box)
        self.manual_1_box.setObjectName(u"manual_1_box")
        self.verticalLayout_2 = QVBoxLayout(self.manual_1_box)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 2, -1, 2)
        self.manual_bias_1_spin = QDoubleSpinBox(self.manual_1_box)
        self.manual_bias_1_spin.setObjectName(u"manual_bias_1_spin")

        self.verticalLayout_2.addWidget(self.manual_bias_1_spin)

        self.manual_bias_reset_1_button = QPushButton(self.manual_1_box)
        self.manual_bias_reset_1_button.setObjectName(u"manual_bias_reset_1_button")

        self.verticalLayout_2.addWidget(self.manual_bias_reset_1_button)


        self.gridLayout_2.addWidget(self.manual_1_box, 1, 0, 1, 1)

        self.manual_2_box = QGroupBox(self.manual_panel_box)
        self.manual_2_box.setObjectName(u"manual_2_box")
        self.verticalLayout_3 = QVBoxLayout(self.manual_2_box)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 2, -1, 2)
        self.manual_bias_2_spin = QDoubleSpinBox(self.manual_2_box)
        self.manual_bias_2_spin.setObjectName(u"manual_bias_2_spin")

        self.verticalLayout_3.addWidget(self.manual_bias_2_spin)

        self.manual_bias_reset_2_button = QPushButton(self.manual_2_box)
        self.manual_bias_reset_2_button.setObjectName(u"manual_bias_reset_2_button")

        self.verticalLayout_3.addWidget(self.manual_bias_reset_2_button)


        self.gridLayout_2.addWidget(self.manual_2_box, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.manual_panel_box)

        self.main_splitter.addWidget(self.control_panel_widget)

        self.horizontalLayout_2.addWidget(self.main_splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 533, 26))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0438\u0437\u043c\u0435\u0440\u0438\u0442\u0435\u043b\u044c", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0441\u0446\u0438\u043b\u043b\u043e\u0433\u0440\u0430\u0444", None))
        self.substrate_label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u043b\u043e\u0436\u043a\u0430:", None))
        self.sample_label.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0437\u0435\u0446:", None))
        self.sample_edit.setText("")
        self.substrate_scheme_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0445\u0435\u043c\u0430 \u043f\u043e\u0434\u043b\u043e\u0436\u043a\u0438", None))
        self.accurate_meas_check.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u0435 \u0441 \u0434\u0438\u0430\u043f\u0430\u0437\u043e\u043d\u043e\u043c \u043c\u0435\u043d\u044c\u0448\u0435\u0433\u043e \u0448\u0430\u0433\u0430", None))
        self.direction_box.setTitle("")
        self.backward_dir_button.setText(QCoreApplication.translate("MainWindow", u"\u2190", None))
        self.forward_dir_button.setText(QCoreApplication.translate("MainWindow", u"\u2192", None))
        self.common_meas_box.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0449\u0438\u0439 \u0434\u0438\u0430\u043f\u0430\u0437\u043e\u043d", None))
        self.limit_left_label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u0435\u043b \u0441\u043b\u0435\u0432\u0430:", None))
        self.limit_left_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.limit_right_label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u0435\u043b \u0441\u043f\u0440\u0430\u0432\u0430:", None))
        self.limit_right_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.step_label.setText(QCoreApplication.translate("MainWindow", u"\u0428\u0430\u0433:", None))
        self.step_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.delay_label.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0434\u0435\u0440\u0436\u043a\u0430:", None))
        self.delay_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0441", None))
        self.accurate_meas_box.setTitle(QCoreApplication.translate("MainWindow", u"\u0414\u0438\u0430\u043f\u0430\u0437\u043e\u043d \u0441 \u043c\u0435\u043d\u044c\u0448\u0438\u043c \u0448\u0430\u0433\u043e\u043c", None))
        self.limit_left_accurate_label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u0435\u043b \u0441\u043b\u0435\u0432\u0430:", None))
        self.delay_accurate_label.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0434\u0435\u0440\u0436\u043a\u0430:", None))
        self.limit_right_accurate_label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u0435\u043b \u0441\u043f\u0440\u0430\u0432\u0430:", None))
        self.limit_left_accurate_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.delay_accurate_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0441", None))
        self.limit_right_accurate_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.step_accurate_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.step_accurate_label.setText(QCoreApplication.translate("MainWindow", u"\u0428\u0430\u0433:", None))
        self.max_current_box.setTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u043e \u0434\u043e\u043f\u0443\u0441\u0442\u0438\u043c\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0441\u0438\u043b\u044b \u0442\u043e\u043a\u0430:", None))
        self.max_current_1_label.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043d\u0430\u043b 1:", None))
        self.max_current_1_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0410", None))
        self.max_current_2_label.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043d\u0430\u043b 2:", None))
        self.max_current_2_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0410", None))
        self.direction_label.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435:", None))
        self.meas_orber_box.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u0439:", None))
        self.meas_control_box.setTitle(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u0435\u043c:", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u043e\u043f", None))
        self.pause_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0443\u0437\u0430", None))
        self.U__button.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0437\u0432\u043e\u0440\u043e\u0442", None))
        self.next_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u043b\u0435\u0435", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441", None))
        self.manual_panel_box.setTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0443\u0447\u043d\u043e\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435:", None))
        self.light_on_off_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0432\u0435\u0442: \u0412\u042b\u041a\u041b", None))
        self.manual_1_box.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043d\u0430\u043b 1", None))
        self.manual_bias_1_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.manual_bias_reset_1_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441", None))
        self.manual_2_box.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043d\u0430\u043b 2", None))
        self.manual_bias_2_spin.setSuffix(QCoreApplication.translate("MainWindow", u" \u0412", None))
        self.manual_bias_reset_2_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u0431\u043e\u0440\u044b", None))
    # retranslateUi

