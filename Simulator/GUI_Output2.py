import sys, time
import matplotlib.pyplot as plt
import random
import numpy as np

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from vispyTest import Canvas

class Output(QtGui.QMainWindow):
    
    def __init__(self):
        super(Output, self).__init__()

        self.initUI()
        

    def initUI(self):

        # Menu bar
        self.menubar = QtGui.QMenuBar()
        
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction('test')

        self.setMenuBar(self.menubar)

        # Frames
        self.splitter_widget = GUI()
        self.setCentralWidget(self.splitter_widget)
        
        self.setGeometry(300, 50, 1100, 800)
        self.setWindowTitle('Menubar')    
        self.show()
        

class Grid(QtGui.QWidget):
    def __init__(self):
        super(Grid, self).__init__()
        grid = QtGui.QGridLayout(self)

        subgrid = QtGui.QGridLayout()

        test = QtGui.QVBoxLayout()

        left = GeneralResults()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        

        sub_bottomleft = QtGui.QTextEdit()
 
        sub_bottomright = QtGui.QTextEdit()

        sub_top = ControlPanel()

        grid.addWidget(left, 0, 0, 1, 2)
        grid.addLayout(subgrid, 0, 2)

        #left.setBackground(brush)

        subgrid.addWidget(sub_bottomleft, 2, 0)
        subgrid.addWidget(sub_bottomright, 2, 1, 1, 2)
        subgrid.addWidget(sub_top, 0, 0, 2, 3)

        grid.setColumnMinimumWidth(0, 200)
        subgrid.setRowMinimumHeight(0, 100)

        #self.setStyleSheet("QWidget { background-color: Red }")


class GeneralResults(QtGui.QWidget):
    def __init__(self):
        super(GeneralResults, self).__init__()

        layout      = QtGui.QVBoxLayout(self)
        #self.setStyleSheet("QWidget { background-color: Red }")

        self.nr_agents   = QtGui.QLabel('None')
        self.nr_goods    = QtGui.QLabel('None')
        self.nr_goods1    = QtGui.QLabel('None')
        self.nr_goods2    = QtGui.QLabel('None')
        self.nr_goods3    = QtGui.QLabel('None')
        self.nr_goods4    = QtGui.QLabel('None')
        self.nr_goods5    = QtGui.QLabel('None')
        self.nr_goods6    = QtGui.QLabel('None')
        self.nr_goods7    = QtGui.QLabel('None')
        self.textBox = QtGui.QTextEdit()

        layout.addWidget(self.nr_agents)
        layout.addWidget(self.nr_goods)
        layout.addWidget(self.nr_goods1)
        layout.addWidget(self.nr_goods2)
        layout.addWidget(self.nr_goods3)
        layout.addWidget(self.nr_goods4)
        layout.addWidget(self.nr_goods5)
        layout.addWidget(self.nr_goods6)
        layout.addWidget(self.nr_goods7)
        layout.addWidget(self.textBox)

        #layout.addWidget(self.textBox)
        #layout.setColumnMinimumWidth(0, 200)
        layout.addStretch(1)

    def setValues(env):

        self.nr_agents.setText(str(env.N))
        self.nr_goods.setText(str(env.M))

class ControlPanel(QtGui.QWidget):
    def __init__(self):
        super(ControlPanel, self).__init__()

        layout      = QtGui.QVBoxLayout(self)
        #self.setStyleSheet("QWidget { background-color: Red }")

        self.nr_agents   = QtGui.QLabel('None')
        self.nr_goods    = QtGui.QLabel('None')

        layout.addWidget(self.nr_agents)
        layout.addWidget(self.nr_goods)

        layout.addStretch(1)

class GUI(QtGui.QWidget):
    def __init__(self):
        super(GUI, self).__init__() 

        self.groupBox = QtGui.QGroupBox(self)
        self.groupBox2 = QtGui.QGroupBox(self)
        self.groupBox3 = QtGui.QGroupBox(self)
        self.groupBox4 = QtGui.QGroupBox(self)
        
        self.groupBox2.setMaximumWidth(200)
        self.groupBox4.setMaximumHeight(200)
        self.groupBox.setMaximumWidth(300)

        main_layout = QtGui.QHBoxLayout(self)
        left_layout = QtGui.QVBoxLayout()
        right_layout = QtGui.QVBoxLayout()

        top_layout = QtGui.QVBoxLayout()
        bottom_layout = QtGui.QHBoxLayout()

        bottom_left_layout = QtGui.QVBoxLayout()
        bottom_right_layout = QtGui.QVBoxLayout()

        self.nr_agents   = QtGui.QLabel('None')
        self.nr_goods    = QtGui.QLabel('None')

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        right_layout.addLayout(top_layout)
        right_layout.addLayout(bottom_layout)

        bottom_layout.addLayout(bottom_left_layout)
        bottom_layout.addLayout(bottom_right_layout)

        bottom_right_layout.addWidget(self.groupBox)
        bottom_left_layout.addWidget(self.groupBox3)
        top_layout.addWidget(self.groupBox4)
        left_layout.addWidget(self.groupBox2)

        hbox = QtGui.QHBoxLayout(self.groupBox)
        hbox.addWidget(self.nr_agents)
        self.nr_agents.setAlignment(QtCore.Qt.AlignTop)

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.groupBox = QtGui.QGroupBox(self)
        hbox = QtGui.QHBoxLayout(self.groupBox)
        length = 3
        for index in range(length):
            hbox.addWidget(Widget(u'H\u2082O', self))
            if index < length - 1:
                hbox.addWidget(Label(u'+', self))
            else:
                hbox.addWidget(Label(u'\u2192', self))
        hbox.addWidget(Widget(u'4 H\u2082O', self))
        hbox.addWidget(Label(u'+', self))
        hbox.addWidget(Widget(u'H\u2084O\u2082', self))
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.groupBox)
        vbox.addStretch()

class Label(QtGui.QLabel):
    def __init__(self, label, parent=None):
        QtGui.QLabel.__init__(self, label, parent)
        self.setAlignment(QtCore.Qt.AlignCenter)

class Widget(QtGui.QWidget):
    def __init__(self, label, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setMaximumWidth(100)
        layout = QtGui.QGridLayout(self)
        self.label = QtGui.QLabel(label, self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label, 0, 0, 1, 2)
        self.lineEdit = QtGui.QLineEdit(self)
        layout.addWidget(self.lineEdit, 1, 0, 1, 2)
        self.toolButton = QtGui.QToolButton(self)
        layout.addWidget(self.toolButton, 2, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self)
        layout.addWidget(self.comboBox, 2, 1, 1, 1)

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Output()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 



