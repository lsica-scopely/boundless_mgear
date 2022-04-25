# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsUI.ui',
# licensing of 'settingsUI.ui' applies.
#
# Created: Thu Mar 17 12:38:32 2022
#      by: pyside2-uic  running on PySide2 5.12.5
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(487, 563)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.skeleton_map_table = QtWidgets.QTableWidget(Form)
        self.skeleton_map_table.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.skeleton_map_table.sizePolicy().hasHeightForWidth())
        self.skeleton_map_table.setSizePolicy(sizePolicy)
        self.skeleton_map_table.setRowCount(0)
        self.skeleton_map_table.setColumnCount(4)
        self.skeleton_map_table.setObjectName("skeleton_map_table")
        self.skeleton_map_table.setColumnCount(4)
        self.skeleton_map_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.skeleton_map_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.skeleton_map_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.skeleton_map_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.skeleton_map_table.setHorizontalHeaderItem(3, item)
        self.skeleton_map_table.horizontalHeader().setVisible(True)
        self.skeleton_map_table.horizontalHeader().setHighlightSections(False)
        self.skeleton_map_table.horizontalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.skeleton_map_table, 5, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.skeleton_button = QtWidgets.QToolButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skeleton_button.sizePolicy().hasHeightForWidth())
        self.skeleton_button.setSizePolicy(sizePolicy)
        self.skeleton_button.setSizeIncrement(QtCore.QSize(0, 0))
        self.skeleton_button.setBaseSize(QtCore.QSize(0, 0))
        self.skeleton_button.setObjectName("skeleton_button")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.skeleton_button)
        self.skeleton_label = QtWidgets.QLabel(self.groupBox)
        self.skeleton_label.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skeleton_label.sizePolicy().hasHeightForWidth())
        self.skeleton_label.setSizePolicy(sizePolicy)
        self.skeleton_label.setText("")
        self.skeleton_label.setObjectName("skeleton_label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.skeleton_label)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 10, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_row_button = QtWidgets.QPushButton(Form)
        self.add_row_button.setObjectName("add_row_button")
        self.horizontalLayout.addWidget(self.add_row_button)
        self.rem_row_button = QtWidgets.QPushButton(Form)
        self.rem_row_button.setObjectName("rem_row_button")
        self.horizontalLayout.addWidget(self.rem_row_button)
        self.copy_selection_button = QtWidgets.QPushButton(Form)
        self.copy_selection_button.setObjectName("copy_selection_button")
        self.horizontalLayout.addWidget(self.copy_selection_button)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.skeleton_map_table.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("Form", "Joint Chain Start", None, -1))
        self.skeleton_map_table.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("Form", "Joint Chain End", None, -1))
        self.skeleton_map_table.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("Form", "Guide Start", None, -1))
        self.skeleton_map_table.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("Form", "Guide End", None, -1))
        self.skeleton_button.setText(QtWidgets.QApplication.translate("Form", "Set Skeleton", None, -1))
        self.add_row_button.setText(QtWidgets.QApplication.translate("Form", "Add Row", None, -1))
        self.rem_row_button.setText(QtWidgets.QApplication.translate("Form", "Remove Row", None, -1))
        self.copy_selection_button.setText(QtWidgets.QApplication.translate("Form", "Copy Selection", None, -1))

