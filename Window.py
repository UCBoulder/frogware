# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gui_Window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1025, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setMaximumSize(QtCore.QSize(234, 428))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btn_start_cnt_update = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_start_cnt_update.setObjectName("btn_start_cnt_update")
        self.horizontalLayout_2.addWidget(self.btn_start_cnt_update)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_11.addLayout(self.horizontalLayout_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_step_left = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_step_left.setObjectName("btn_step_left")
        self.horizontalLayout_4.addWidget(self.btn_step_left)
        self.btn_step_right = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_step_right.setObjectName("btn_step_right")
        self.horizontalLayout_4.addWidget(self.btn_step_right)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.le_step_size_um = QtWidgets.QLineEdit(self.groupBox_3)
        self.le_step_size_um.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_step_size_um.setObjectName("le_step_size_um")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_step_size_um)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.le_step_size_fs = QtWidgets.QLineEdit(self.groupBox_3)
        self.le_step_size_fs.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_step_size_fs.setObjectName("le_step_size_fs")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_step_size_fs)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_11.addWidget(self.groupBox_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.btn_home_stage = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_home_stage.setObjectName("btn_home_stage")
        self.horizontalLayout_5.addWidget(self.btn_home_stage)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_11.addLayout(self.horizontalLayout_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem5)
        self.btn_move_to_pos = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_move_to_pos.setObjectName("btn_move_to_pos")
        self.horizontalLayout_12.addWidget(self.btn_move_to_pos)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_12)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.le_pos_um = QtWidgets.QLineEdit(self.groupBox_4)
        self.le_pos_um.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_pos_um.setObjectName("le_pos_um")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_pos_um)
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.le_pos_fs = QtWidgets.QLineEdit(self.groupBox_4)
        self.le_pos_fs.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_pos_fs.setObjectName("le_pos_fs")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_pos_fs)
        self.verticalLayout_4.addLayout(self.formLayout_2)
        self.verticalLayout_11.addWidget(self.groupBox_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_17 = QtWidgets.QLabel(self.groupBox_2)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_5.addWidget(self.label_17)
        self.lcd_cnt_update_current_pos_um = QtWidgets.QLCDNumber(self.groupBox_2)
        self.lcd_cnt_update_current_pos_um.setObjectName("lcd_cnt_update_current_pos_um")
        self.verticalLayout_5.addWidget(self.lcd_cnt_update_current_pos_um)
        self.horizontalLayout_10.addLayout(self.verticalLayout_5)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.verticalLayout_11.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem9)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_19 = QtWidgets.QLabel(self.groupBox_2)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_6.addWidget(self.label_19)
        self.lcd_cnt_update_current_pos_fs = QtWidgets.QLCDNumber(self.groupBox_2)
        self.lcd_cnt_update_current_pos_fs.setObjectName("lcd_cnt_update_current_pos_fs")
        self.verticalLayout_6.addWidget(self.lcd_cnt_update_current_pos_fs)
        self.horizontalLayout_15.addLayout(self.verticalLayout_6)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem10)
        self.verticalLayout_11.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem11)
        self.btn_set_T0 = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_set_T0.setObjectName("btn_set_T0")
        self.horizontalLayout_14.addWidget(self.btn_set_T0)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem12)
        self.verticalLayout_11.addLayout(self.horizontalLayout_14)
        self.verticalLayout_13.addWidget(self.groupBox_2)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem13)
        self.horizontalLayout_16.addLayout(self.verticalLayout_13)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.le_cont_upd_ymax = QtWidgets.QLineEdit(self.groupBox)
        self.le_cont_upd_ymax.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_cont_upd_ymax.setObjectName("le_cont_upd_ymax")
        self.verticalLayout_7.addWidget(self.le_cont_upd_ymax)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem14)
        self.le_cont_upd_ymin = QtWidgets.QLineEdit(self.groupBox)
        self.le_cont_upd_ymin.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_cont_upd_ymin.setObjectName("le_cont_upd_ymin")
        self.verticalLayout_7.addWidget(self.le_cont_upd_ymin)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gv_cont_upd_spec = PlotWidget(self.groupBox)
        self.gv_cont_upd_spec.setMinimumSize(QtCore.QSize(620, 439))
        self.gv_cont_upd_spec.setObjectName("gv_cont_upd_spec")
        self.verticalLayout_2.addWidget(self.gv_cont_upd_spec)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_cont_upd_xmin = QtWidgets.QLineEdit(self.groupBox)
        self.le_cont_upd_xmin.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_cont_upd_xmin.setObjectName("le_cont_upd_xmin")
        self.horizontalLayout.addWidget(self.le_cont_upd_xmin)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem15)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.le_cont_upd_xmax = QtWidgets.QLineEdit(self.groupBox)
        self.le_cont_upd_xmax.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_cont_upd_xmax.setObjectName("le_cont_upd_xmax")
        self.horizontalLayout.addWidget(self.le_cont_upd_xmax)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.horizontalLayout_16.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_14.addItem(spacerItem16)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_5.setMaximumSize(QtCore.QSize(234, 233))
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem17 = QtWidgets.QSpacerItem(37, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem17)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_6.setMinimumSize(QtCore.QSize(91, 51))
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_9.addWidget(self.pushButton_6)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem18)
        self.verticalLayout_12.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_13 = QtWidgets.QLabel(self.groupBox_5)
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_13.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_13)
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setObjectName("label_14")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_14.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_14)
        self.horizontalLayout_8.addLayout(self.formLayout_4)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_15 = QtWidgets.QLabel(self.groupBox_5)
        self.label_15.setObjectName("label_15")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_15.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_15)
        self.label_16 = QtWidgets.QLabel(self.groupBox_5)
        self.label_16.setObjectName("label_16")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_16.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_16)
        self.horizontalLayout_8.addLayout(self.formLayout_3)
        self.verticalLayout_12.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem19)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_18 = QtWidgets.QLabel(self.groupBox_5)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_9.addWidget(self.label_18)
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.groupBox_5)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.verticalLayout_9.addWidget(self.lcdNumber_2)
        self.horizontalLayout_11.addLayout(self.verticalLayout_9)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem20)
        self.verticalLayout_12.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem21)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_10.addWidget(self.label_20)
        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.groupBox_5)
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.verticalLayout_10.addWidget(self.lcdNumber_4)
        self.horizontalLayout_13.addLayout(self.verticalLayout_10)
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem22)
        self.verticalLayout_12.addLayout(self.horizontalLayout_13)
        self.verticalLayout_14.addWidget(self.groupBox_5)
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_14.addItem(spacerItem23)
        self.horizontalLayout_17.addLayout(self.verticalLayout_14)
        self.groupBox1 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox1.setObjectName("groupBox1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox1)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_8.addWidget(self.label_9)
        self.le_spectrogram_ymax = QtWidgets.QLineEdit(self.groupBox1)
        self.le_spectrogram_ymax.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_spectrogram_ymax.setObjectName("le_spectrogram_ymax")
        self.verticalLayout_8.addWidget(self.le_spectrogram_ymax)
        spacerItem24 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem24)
        self.le_spectrogram_ymin = QtWidgets.QLineEdit(self.groupBox1)
        self.le_spectrogram_ymin.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_spectrogram_ymin.setObjectName("le_spectrogram_ymin")
        self.verticalLayout_8.addWidget(self.le_spectrogram_ymin)
        self.label_10 = QtWidgets.QLabel(self.groupBox1)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.horizontalLayout_7.addLayout(self.verticalLayout_8)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gv_Spectrogram = PlotWidget(self.groupBox1)
        self.gv_Spectrogram.setMinimumSize(QtCore.QSize(620, 439))
        self.gv_Spectrogram.setObjectName("gv_Spectrogram")
        self.verticalLayout_3.addWidget(self.gv_Spectrogram)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.le_spectrogram_xmin = QtWidgets.QLineEdit(self.groupBox1)
        self.le_spectrogram_xmin.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_spectrogram_xmin.setObjectName("le_spectrogram_xmin")
        self.horizontalLayout_3.addWidget(self.le_spectrogram_xmin)
        self.label_11 = QtWidgets.QLabel(self.groupBox1)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem25)
        self.label_12 = QtWidgets.QLabel(self.groupBox1)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_3.addWidget(self.label_12)
        self.le_spectrogram_xmax = QtWidgets.QLineEdit(self.groupBox1)
        self.le_spectrogram_xmax.setMaximumSize(QtCore.QSize(91, 16777215))
        self.le_spectrogram_xmax.setObjectName("le_spectrogram_xmax")
        self.horizontalLayout_3.addWidget(self.le_spectrogram_xmax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.horizontalLayout_17.addWidget(self.groupBox1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        self.gridLayout_5.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Open/open_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Save/save_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setObjectName("actionSave")
        self.actionStop = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Stop/stop_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon2)
        self.actionStop.setObjectName("actionStop")
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionStop)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_start_cnt_update.setText(_translate("MainWindow", "Start \n"
" Continous Update"))
        self.btn_step_left.setText(_translate("MainWindow", "step left"))
        self.btn_step_right.setText(_translate("MainWindow", "step right"))
        self.label.setText(_translate("MainWindow", "step size (um)"))
        self.label_2.setText(_translate("MainWindow", "step size (fs)"))
        self.btn_home_stage.setText(_translate("MainWindow", "home the stage"))
        self.btn_move_to_pos.setText(_translate("MainWindow", "move to position"))
        self.label_3.setText(_translate("MainWindow", "position (um)"))
        self.label_4.setText(_translate("MainWindow", "position (fs)"))
        self.label_17.setText(_translate("MainWindow", "Current Position (um)"))
        self.label_19.setText(_translate("MainWindow", "Current Position (fs)"))
        self.btn_set_T0.setText(_translate("MainWindow", "set T0"))
        self.groupBox.setTitle(_translate("MainWindow", "Spectrum"))
        self.label_5.setText(_translate("MainWindow", "y max"))
        self.label_6.setText(_translate("MainWindow", "y min"))
        self.label_8.setText(_translate("MainWindow", "x min"))
        self.label_7.setText(_translate("MainWindow", "x max"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Spectrum Continuous Update"))
        self.pushButton_6.setText(_translate("MainWindow", "Collect \n"
" Spectrogram"))
        self.label_13.setText(_translate("MainWindow", "start (um)"))
        self.label_14.setText(_translate("MainWindow", "start (fs)"))
        self.label_15.setText(_translate("MainWindow", "end(um)"))
        self.label_16.setText(_translate("MainWindow", "end(fs)"))
        self.label_18.setText(_translate("MainWindow", "Current Position (um)"))
        self.label_20.setText(_translate("MainWindow", "Current Position (fs)"))
        self.groupBox1.setTitle(_translate("MainWindow", "Spectrogram"))
        self.label_9.setText(_translate("MainWindow", "y max"))
        self.label_10.setText(_translate("MainWindow", "y min"))
        self.label_11.setText(_translate("MainWindow", "x min"))
        self.label_12.setText(_translate("MainWindow", "x max"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Spectrogram"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Integration Time"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Settings"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Upper Limit"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Lower Limit"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Units"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("MainWindow", "ms"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Settings"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
from PlotAndTableFunctions import PlotWidget
import QRC_file_rc
