import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from spectraanalyzer_ui import Ui_SpectraAnalyzer


class spectraanalyzer(QMainWindow, Ui_SpectraAnalyzer):
    def __init__(self, parent=None):
        super(spectraanalyzer, self).__init__(parent)
        self.setupUi(self)

        # Connect "add" button with a custom function (addInputTextToListbox)
        self.pushButton_browse_1.clicked.connect(self.get_folder_name_1)
        self.pushButton_browse_2.clicked.connect(self.get_folder_name_2)
        self.pushButton_browse_3.clicked.connect(self.get_folder_name_3)
        self.pushButton_browse_4.clicked.connect(self.get_folder_name_4)
        self.pushButton_browse_5.clicked.connect(self.get_folder_name_5)
        self.pushButton_browse_6.clicked.connect(self.get_folder_name_6)
        self.pushButton_browse_7.clicked.connect(self.get_folder_name_7)
        self.pushButton_browse_8.clicked.connect(self.get_folder_name_8)
        self.pushButton_browse_9.clicked.connect(self.get_folder_name_9)
        self.pushButton_browse_10.clicked.connect(self.get_folder_name_10)
        self.pushButton_browse_11.clicked.connect(self.get_folder_name_11)
        self.pushButton_browse_12.clicked.connect(self.get_folder_name_12)
        self.pushButton_browse_13.clicked.connect(self.get_folder_name_13)
        self.pushButton_browse_14.clicked.connect(self.get_folder_name_14)
        self.pushButton_browse_15.clicked.connect(self.get_folder_name_15)
        self.pushButton_browse_16.clicked.connect(self.get_folder_name_16)

    def get_folder_name_1(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_1.setText(directory)

    def get_folder_name_2(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_2.setText(directory)

    def get_folder_name_3(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_3.setText(directory)

    def get_folder_name_4(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_4.setText(directory)

    def get_folder_name_5(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_5.setText(directory)

    def get_folder_name_6(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_6.setText(directory)

    def get_folder_name_7(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_7.setText(directory)

    def get_folder_name_8(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_8.setText(directory)

    def get_folder_name_9(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_9.setText(directory)

    def get_folder_name_10(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_10.setText(directory)

    def get_folder_name_11(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_11.setText(directory)

    def get_folder_name_12(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_12.setText(directory)

    def get_folder_name_13(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_13.setText(directory)

    def get_folder_name_14(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_14.setText(directory)

    def get_folder_name_15(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_15.setText(directory)

    def get_folder_name_16(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_project_Sample_16.setText(directory)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    program = spectraanalyzer()

    program.show()
    sys.exit(app.exec_())
