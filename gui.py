import sys
import logging
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
    # send_initial_value = QtCore.pyqtSignal(np.float64, np.float64, np.float64, name='send_initial_value')

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # cid_up = fig.canvas.mpl_connect('button_press_event', self.OnClick)
        # cid_down = fig.canvas.mpl_connect('button_release_event', self.OnRelease)

    def plot_data(self, data_x, data_y, exp_y):
        self.axes.clear()
        self.axes.hold(True)
        self.axes.plot(data_x, data_y, label='Fitted Data')
        if exp_y is not None:
            self.axes.plot(data_x, exp_y, label='Experimental Data')
        # self.canvas.legend()
        self.axes.hold(False)
        self.draw()


class SpectraAnalyzer(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SpectraAnalyzer, self).__init__(parent)
        self.setupUi(self)
        # Connect "add" button with a custom function (addInputTextToListbox)
        self.pushButton_fit.clicked.connect(self.fit)
        self.pushButton_browse.clicked.connect(self.get_address)
        v_box = QVBoxLayout(self.canvas)
        self.static_canvas = MyMplCanvas(self.canvas)
        v_box.addWidget(self.static_canvas)
        self.mouse_click_x = 0
        self.mouse_click_y = 0
        self.mouse_release_x = 0
        self.mouse_release_y = 0
        self.initial_guess_center = 0
        self.initial_guess_height = 0
        self.initial_guess_width = 0
        # self.static_canvas.send_initial_value.connect(self, self.set_initial_value(center, height, width))
        # QtCore.QObject.connect(self,SIGNAL('clicked()'),self.set_initial_value)
        cid_button_press = self.static_canvas.mpl_connect('button_press_event', self.on_click)
        cid_button_release = self.static_canvas.mpl_connect('button_release_event', self.on_release)

    def plot_data(self, data_x, data_y, exp_y=None):
        self.static_canvas.plot_data(data_x, data_y, exp_y)

    # @QtCore.pyqtSlot(np.float64, np.float64, np.float64, name='set_initial_value')
    def set_initial_value(self):
        self.lineEdit_gaussian.setText(str(self.initial_guess_width))
        self.lineEdit_lorentzian.setText(str(0))
        self.lineEdit_center.setText(str(self.initial_guess_center))
        self.lineEdit_height.setText(str(self.initial_guess_height))

    def on_click(self, event):
        logger.debug('Clicked X: ', event.xdata)
        logger.debug('Clicked Y: ', event.ydata)
        self.mouse_click_x = event.xdata
        self.mouse_click_y = event.ydata
        self.initial_guess_center = event.xdata

    def on_release(self, event):
        logger.debug('Released X: ', event.xdata)
        logger.debug('Released Y: ', event.ydata)
        self.mouse_release_x = event.xdata
        self.mouse_release_y = event.ydata
        self.initial_guess_height = abs(self.mouse_release_y - self.mouse_click_y)
        self.initial_guess_width = abs(self.mouse_release_x - self.mouse_click_x)
        self.set_initial_value()

    def fit(self):
        data = self.read_data()
        if data is None:
            return
        binding_energy = data[:, 0]
        counts = data[:, 1]
        # binding_energy = np.linspace(-10, 10, 1000)
        gaussian = float(self.lineEdit_gaussian.text())
        lorentzian = float(self.lineEdit_lorentzian.text())
        center = float(self.lineEdit_center.text())
        height = float(self.lineEdit_height.text())
        #y = lmfit.models.voigt(binding_energy, height, center, gaussian, lorentzian)
        params = lmfit.Parameters()

        # Select peak model type
        if self.comboBox_peak.currentText() == "Voigt":
            peak_model = lmfit.models.VoigtModel(prefix='voigt_')
            params.add('voigt_amplitude', value=height, min=0, vary=True)
            params.add('voigt_center', value=center, min=0, vary=True)
            params.add('voigt_sigma', value=gaussian, min=0, vary=True)
            params.add('voigt_gamma', value=lorentzian, min=0, vary=True)
            logger.debug("Voigt selected")
        elif self.comboBox_peak.currentText() == "Gaussian":
            peak_model = lmfit.models.GaussianModel(prefix='gauss_')
            params.add('gauss_amplitude', value=height, min=0, vary=True)
            params.add('gauss_center', value=center, min=0, vary=True)
            params.add('gauss_sigma', value=gaussian, min=0, vary=True)
            logger.debug("Gaussian selected")
        elif self.comboBox_peak.currentText() == "Lorentzian":
            peak_model = lmfit.models.LorentzianModel(prefix='lorentz_')
            params.add('lorentz_amplitude', value=height, min=0, vary=True)
            params.add('lorentz_center', value=center, min=0, vary=True)
            params.add('lorentz_sigma', value=lorentzian, min=0, vary=True)
            logger.debug("Lorentzian selected")
        else :
            peak_model = lmfit.models.VoigtModel(prefix='voigt_')
            logger.debug("None selected")

        total_model = peak_model

        # Select background model
        if self.checkBox_constant_background.isChecked():
            background_model1 = lmfit.models.ConstantModel(prefix='const_')
            params += background_model1.make_params(c=10)
            total_model += background_model1

        if self.checkBox_linear_background.isChecked():
            background_model2 = lmfit.models.LinearModel(prefix='linear_')
            params += background_model2.make_params(slope=0, intercept=0)
            total_model += background_model2

        if self.checkBox_polynomial_background.isChecked():
            background_model3 = lmfit.models.PolynomialModel(prefix='poly_', degree=7)
            params += background_model3.make_params(c0=0, c1=0, c2=0, c3=0, c4=0, c5=0, c6=0, c7=0)
            total_model += background_model3

        if self.checkBox_step_background.isChecked():
            background_model4 = lmfit.models.StepModel(form='erf', prefix='step_')
            params += background_model4.make_params(amplitude = 0, center = center, sigma = gaussian)
            total_model += background_model4

        # print(total_model)
        # print('Before fitting',params)

        logger.info("Fitting started")
        out = total_model.fit(counts, params, x=binding_energy)
        logger.info("Fitting finished")
        fitted_params = lmfit.Parameters.valuesdict(out.params)
        out_height = fitted_params['voigt_amplitude']
        out_gaussian = fitted_params['voigt_sigma']
        out_lorentzian = fitted_params['voigt_gamma']
        out_center = fitted_params['voigt_center']
        self.lineEdit_gaussian.setText(str(out_gaussian))
        self.lineEdit_lorentzian.setText(str(out_lorentzian))
        self.lineEdit_center.setText(str(out_center))
        self.lineEdit_height.setText(str(out_height))
        logger.debug("Fit report is")
        logger.debug(out.fit_report())
        self.plot_data(binding_energy, counts, out.best_fit)

    def get_address(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file')
        self.lineEdit_address.setText(file_name)
        data = self.read_data()
        binding_energy = data[:, 0]
        counts = data[:, 1]
        self.plot_data(binding_energy,counts)

    def read_data(self):
        try:
            path = self.lineEdit_address.text()
            data = np.loadtxt(path, delimiter="\t")
            return data[:, 1:3]
        except IOError:
            logger.error("Error in reading file.")
            return None


if __name__ == '__main__':
    logger = logging.getLogger("SpectraAnalyzer")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("logfile.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    logger.info("Program started")

    app = QApplication(sys.argv)
    program = SpectraAnalyzer()

    program.show()
    sys.exit(app.exec_())