import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as FigureCanvas
from matplotlib.figure import Figure
from MainWindow import Ui_MainWindow
import lmfit
import numpy as np
import time


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot_data(self, data_x, data_y, exp_y):
        self.axes.clear()
        self.axes.hold(True)
        self.axes.plot(data_x, data_y, label='Fitted Data')
        self.axes.plot(data_x, exp_y, label='Experimental Data')
        # self.canvas.legend()
        self.axes.hold(False)
        self.draw()


class SpectraAnalyzer(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SpectraAnalyzer, self).__init__(parent)
        self.setupUi(self)
        # Connect "add" button with a custom function (addInputTextToListbox)
        self.pushButton.clicked.connect(self.fit)
        self.pushButton_2.clicked.connect(self.get_address)
        v_box = QVBoxLayout(self.canvas)
        self.static_canvas = MyMplCanvas(self.canvas)
        v_box.addWidget(self.static_canvas)

    def plot_data(self, data_x, data_y, exp_y):
        self.static_canvas.plot_data(data_x, data_y, exp_y)

    def fit(self):
        data = self.read_data()
        binding_energy = data[:, 0]
        counts = data[:, 1]
        # binding_energy = np.linspace(-10, 10, 1000)
        gaussian = float(self.lineEdit.text())
        laurentzian = float(self.lineEdit_2.text())
        center = float(self.lineEdit_3.text())
        height = float(self.lineEdit_4.text())
        y = lmfit.models.voigt(binding_energy, height, center, gaussian, laurentzian)

        self.plot_data(binding_energy, counts, y)

    def get_address(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file')
        self.lineEdit_5.setText(file_name)

    def read_data(self):
        path = self.lineEdit_5.text()
        data = np.loadtxt(path, delimiter="\t")
        return data[:, 1:3]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = SpectraAnalyzer()

    program.show()
    sys.exit(app.exec_())
