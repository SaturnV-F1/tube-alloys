##Slow code that plots things slowly## formatting - all spaces no tabs
##Relies on sense hat chip or sense hat emulator
#Stlyes so I dont forget them -> 'bb10dark', 'bb10bright', 'cleanlooks', 'gtk2', 'cde', 'motif', 'plastique', 'qt5ct-style', 'Windows', 'Fusion'
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout, QGroupBox, QGridLayout, QLabel
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtCore
import time
from sense_hat import SenseHat
from time import sleep
import numpy as np
from multiprocessing import Pool

####-----------------Pry the data from sense hat's cold dead hands--------------------####
class DataThread(QThread):
    # Create sensor data thread
    change_value = pyqtSignal(tuple)
    def run(self):
        sense=SenseHat()
        while True:
            h=int(sense.get_humidity()) #decimals? who needs em. Also tuple is loathe to pass a float it seems.
            t=int(sense.get_temperature())
            p=int(sense.get_pressure())
            data=(h,t,p)
            time.sleep(0.01)
            self.change_value.emit(data)

####-----------------Create main window class--------------------####
class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Sense Hat Display"
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 800
        self.InitWindow()
                
    def InitWindow(self):
        ####-----------------Set window parameters--------------------####
        self.setWindowTitle(self.title)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet('background-color:black')
        
        ####-----------------Initialize display elements--------------------####
        self.Displays()
        self.UiComponents()
        
        ####-----------------Arrange Layout--------------------####        
        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addWidget(self.displayBox)
        self.setLayout(vbox)
        self.show()
        
        ####-----------------GUI Button--------------------#### 
    def UiComponents(self):
        self.button = QPushButton("Start Data Display")
        self.button.clicked.connect(self.startMainThread)
        self.button.setStyleSheet('background-color:yellow')
        
        #Trigger warning: Code abuse follows.
    def Displays(self):
        self.displayBox = QGroupBox()
        self.displayBox.setStyleSheet('border:none')
        gridLayout = QGridLayout()
        ####-----------------Humidity Bar--------------------####
        self.humidity = QProgressBar()  #Yes, its a progress being encouraged to behave badly. Bet you didn't see this coming Qt
        self.humidity.setOrientation(QtCore.Qt.Vertical)
        self.humidity.setMaximum(100)
        self.humidity.setTextVisible(False)
        gridLayout.addWidget(self.humidity, 0,0)
        
        self.h_label= QLabel()
        self.h_label.setFont(QtGui.QFont("Glass Guage",20))
        gridLayout.addWidget(self.h_label,1,0)
        self.displayBox.setLayout(gridLayout)
        
        ####-----------------Temperature Bar--------------------####
        self.temperature = QProgressBar()
        self.temperature.setOrientation(Qt.Vertical)
        self.temperature.setMaximum(100)
        self.temperature.setTextVisible(False)
        gridLayout.addWidget(self.temperature, 0,1)
        self.displayBox.setLayout(gridLayout)
        
        self.t_label= QLabel()
        self.t_label.setFont(QtGui.QFont("this doesnt work ",20))
        gridLayout.addWidget(self.t_label,1,1)
        self.displayBox.setLayout(gridLayout)
        
        ####-----------------Pressure Bar--------------------####
        self.pressure = QProgressBar()
        self.pressure.setOrientation(Qt.Vertical)
        self.pressure.setMaximum(1000)
        self.pressure.setTextVisible(False)
        gridLayout.addWidget(self.pressure, 0,2)
        self.displayBox.setLayout(gridLayout)
        
        self.p_label= QLabel()
        self.p_label.setFont(QFont("change the font, damn you",20))
        gridLayout.addWidget(self.p_label, 1,2)
        self.displayBox.setLayout(gridLayout)
 
        ####-----------------Start *all* the threads, so many threads--------------------####
    def startMainThread(self):
        self.thread = DataThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.change_value.connect(self.setLabelVal)
        self.thread.change_value.connect(self.setHumidityColors)
        self.thread.change_value.connect(self.setTemperatureColors)
        self.thread.change_value.connect(self.setPressureColors)
        self.thread.start()

        ####-----------------Send values to the progress bars--------------------####
    def setProgressVal(self, data):
        self.humidity.setValue(data[0])
        self.temperature.setValue(data[1])
        self.pressure.setValue(data[2])
        
        ####-----------------Give the progress bars labels-------------------####
    def setLabelVal(self, data):
        self.h_label.setText(str(data[0]))
        self.t_label.setText(str(data[1]))
        self.p_label.setText(str(data[2]))
        
        ####-----------------Slowly and painfully force prog bars to look how I want them to look--------------------####
        ####-----------------This section increases proc. usage 10 fold.---------------------------------------------####
    def setHumidityColors(self, data):
        if data[0] <50:
            self.h_label.setStyleSheet('color:green')
            self.humidity.setStyleSheet("QProgressBar {border: 1px solid green;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:green; height:1px}")            
        elif 51 < data[0] < 60:
            self.h_label.setStyleSheet('color:yellow')
            self.humidity.setStyleSheet("QProgressBar {border: 1px solid yellow;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:yellow; height:1px}")
        elif 61 < data[0] < 100:
            self.h_label.setStyleSheet('QLabel {color:red; border: 1px solid red}')
            self.humidity.setStyleSheet("QProgressBar {border: 1px solid red;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:red; height:1px}")

    def setTemperatureColors(self, data):
        if data[1] <30:
            self.t_label.setStyleSheet('color:green')
            self.temperature.setStyleSheet("QProgressBar {border: 1px solid green;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:green; height:1px}")            
        elif 31 < data[1] < 55:
            self.t_label.setStyleSheet('color:yellow')
            self.temperature.setStyleSheet("QProgressBar {border: 1px solid yellow;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:yellow; height:1px}")
        elif 56 < data[1] < 100:
            self.t_label.setStyleSheet('QLabel {color:red; border: 1px solid red}')
            self.temperature.setStyleSheet("QProgressBar {border: 1px solid red;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:red; height:1px}")

    def setPressureColors(self, data):
        if data[2] <750:
            self.p_label.setStyleSheet('color:green')
            self.pressure.setStyleSheet("QProgressBar {border: 1px solid green;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:green; height:1px}")            
        elif 751 < data[2] < 800:
            self.p_label.setStyleSheet('color:yellow')
            self.pressure.setStyleSheet("QProgressBar {border: 1px solid yellow;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:yellow; height:1px}")
        elif 801 < data[2] < 1000:
            self.p_label.setStyleSheet('QLabel {color:red; border: 1px solid red}')
            self.pressure.setStyleSheet("QProgressBar {border: 1px solid red;border-radius:0px;padding:0px}"
                                    "QProgressBar::chunk {background:red; height:1px}")

####-----------------Do the thing--------------------####
if __name__ == "__main__":
    App = QApplication(sys.argv)
    App.setStyle('cleanlooks')
    window = Window()
    sys.exit(App.exec())
    