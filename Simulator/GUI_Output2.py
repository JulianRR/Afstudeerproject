import sys, time
import matplotlib.pyplot as plt
import random
import numpy as np

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from vispyTest import Canvas

class Output(QtGui.QMainWindow):
    
    def __init__(self, env):
        super(Output, self).__init__()

        self.env = env
        self.initUI()
        

    def initUI(self):

        # Menu bar
        self.menubar = QtGui.QMenuBar()
        
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction('test')

        self.setMenuBar(self.menubar)

        # Frames
        self.gui = GUI(self.env)
        self.setCentralWidget(self.gui)
        
        self.setGeometry(300, 50, 1100, 800)
        self.setWindowTitle('Menubar')    
        self.show()

    def closeEvent(self,event):
        result = QtGui.QMessageBox.question(self,
                      "Confirm Exit...",
                      "Are you sure you want to exit ?",
                      QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
        event.ignore()

        if result == QtGui.QMessageBox.Yes:
            self.env.stop = True
            event.accept()

class GUI(QtGui.QWidget):
    def __init__(self, env):
        super(GUI, self).__init__() 

        self.env = env
        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QtGui.QHBoxLayout(self)
        left_layout = QtGui.QVBoxLayout()
        right_layout = QtGui.QVBoxLayout()

        top_layout = QtGui.QVBoxLayout()
        bottom_layout = QtGui.QHBoxLayout()

        bottom_left_layout = QtGui.QVBoxLayout()
        bottom_right_layout = QtGui.QVBoxLayout()

        # Groupboxes
        self.groupBox_left = QtGui.QGroupBox(self)
        self.groupBox_top = QtGui.QGroupBox(self)
        self.groupBox_bottom_left = QtGui.QGroupBox(self)
        self.groupBox_bottom_right = QtGui.QGroupBox(self)

        self.groupBox_left.setMinimumWidth(200)
        self.groupBox_top.setMinimumHeight(150)
        #self.groupBox_top.setMaximumHeight(200)
        self.groupBox_bottom_left.setMinimumWidth(600)
        self.groupBox_bottom_right.setMinimumWidth(300)

        # Widgets
        self.tabs = Tabs(self.env)
        self.general_results = GeneralResults()
        self.general_results.setValues(self.env)
        self.control_panel = ControlPanel(self.env)
        self.results = Results(self.env)

        # Add layouts
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        right_layout.addLayout(top_layout)
        right_layout.addLayout(bottom_layout)

        bottom_layout.addLayout(bottom_left_layout)
        bottom_layout.addLayout(bottom_right_layout)

        # Add Widgets
        left_layout.addWidget(self.groupBox_left)
        top_layout.addWidget(self.groupBox_top)

        bottom_left_layout.addWidget(self.groupBox_bottom_left)
        bottom_right_layout.addWidget(self.groupBox_bottom_right)
        
        # Fill groupboxes
        vbox_left = QtGui.QVBoxLayout(self.groupBox_left)
        vbox_left.addWidget(self.general_results)

        vbox_top = QtGui.QVBoxLayout(self.groupBox_top)
        vbox_top.addWidget(self.control_panel)
        # self.nr_agents.setAlignment(QtCore.Qt.AlignTop)

        vbox_bottom_left = QtGui.QVBoxLayout(self.groupBox_bottom_left)
        vbox_bottom_left.addWidget(self.tabs)

        vbox_bottom_right = QtGui.QVBoxLayout(self.groupBox_bottom_right)
        vbox_bottom_right.addWidget(self.results)

class Tabs(QtGui.QTabWidget):
    def __init__(self, env):
        super(Tabs, self).__init__()

        self.env = env
        self.initUI()

    def initUI(self):
        self.tab1    = QtGui.QWidget()   
        self.tab2    = QtGui.QWidget()
        self.tab3    = QtGui.QWidget()

        # Layout
        self.layout_tab1 = QtGui.QVBoxLayout()
        self.layout_tab2 = QtGui.QVBoxLayout()
        self.layout_tab3 = QtGui.QVBoxLayout()

        # Widgets
        self.figure = plt.figure()
        self.bar_plot = FigureCanvas(self.figure) 
        self.plot(self.figure, self.bar_plot)

        self.visualisation = Canvas()

        self.textBox = QtGui.QTextEdit()
        self.textBox.setReadOnly(True)

        # Reset button
        self.reset = QtGui.QPushButton('Reset')
        self.reset.clicked.connect(self.resetTransactions)

        # Set layout
        self.tab1.setLayout(self.layout_tab1)
        self.tab2.setLayout(self.layout_tab2) 
        self.tab3.setLayout(self.layout_tab3) 

        # Add Widgets
        self.layout_tab1.addWidget(self.visualisation.native)
        self.layout_tab2.addWidget(self.reset)
        self.layout_tab2.addWidget(self.bar_plot)
        self.layout_tab3.addWidget(self.textBox)

        
        # Add tabs
        self.addTab(self.tab1,"Visualisation")
        self.addTab(self.tab2,"Comunnity percentage")
        self.addTab(self.tab3,"Transctions")

    def plot(self, figure, canvas):
        data = [random.random() for i in range(10)]
        ax = figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        canvas.draw()

    def showPlot(self):
        given_received = self.env.agents_list[0].given_received
        given = [given_received[i][0] for i in range(len(given_received))]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(given, '*-')
        self.bar_plot.draw()

    def plotTransactionPercentages(self):
        time.sleep(self.env.delay)
        data = self.env.transaction_percentages
        x = np.arange(self.env.N)
        width = 0.35

        ax = self.figure.add_subplot(111)
        #ax.hold(False)
        ax.bar(x, data)

        ax.set_ylabel('Percentage')
        ax.set_title('transaction percentage for each agent')
        #ax.set_xticks(x+width)
        #ax.set_xticklabels( ('Agent' + x for x in range(self.env.N)) )

        #ax.legend( (bars[0]), ('Agent') )
        # ax.plot(bars)
        self.bar_plot.draw()

    def plotGoodTransactionPercentages(self):
        time.sleep(self.env.delay)
        #loop through transpose
        x = np.arange(self.env.N)
        width = 0.25
        count = 0
        #plt.cla()
        self.figure.clf()

        self.ax = self.figure.add_subplot(111)

        # y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # y2 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        # self.ax.bar(x, y1, width, color='blue')
        # self.ax.bar(x+width, y2, width, color='red')

        goods_transaction_percentages = np.array(self.env.goods_transaction_percentages)
        for goods in goods_transaction_percentages.T:

            data = []
            for percentage in goods:
                data.append(percentage)
            self.ax.bar(x+(width * count), data, width, color=(0, 1.0/(count+1), 1.0/(count+1)))
            count += 1
        self.ax.set_ylabel('Percentage')
        self.ax.set_title('transaction percentage of each good for each agent')

        #self.ax.set_xlim(-width,len(x)+width)
        xTickMarks = ['Agent'+str(i) for i in range(len(x))]
        self.ax.set_xticks(x+width)
        xtickNames = self.ax.set_xticklabels( xTickMarks )
        plt.setp(xtickNames, rotation=45, fontsize=10)
        self.ax.hold(True)

        self.bar_plot.draw()

    def print_transaction(self, P, Q, good):
        time.sleep(self.env.delay)
        transaction = 'Agent_' + str(P) + ' --> ' + 'Agent_' + str(Q) + ' good: ' + str(good.id)
        self.textBox.append(transaction)
        QtGui.qApp.processEvents()

    def updateV(self):
        self.visualisation.createGrid(self.env.agents_list, self.env.current_agents)

    def resetTransactions(self):
        for agent in self.env.agents_list:
            agent.nr_transactions = 0
        self.env.nr_transactions = 0

class GeneralResults(QtGui.QWidget):
    def __init__(self):
        super(GeneralResults, self).__init__()
        
        self.initUI()

    def initUI(self): 
        layout              = QtGui.QVBoxLayout(self)
        #self.setStyleSheet("QWidget { background-color: Red }")

        self.lbl_nr_agents      = QtGui.QLabel('Number of agents')
        self.lbl_nr_goods       = QtGui.QLabel('Number of goods')

        self.nr_agents      = QtGui.QLabel('')
        self.nr_goods       = QtGui.QLabel('')


        layout.addWidget(self.lbl_nr_agents)
        layout.addWidget(self.nr_agents)
        layout.addWidget(self.lbl_nr_goods)
        layout.addWidget(self.nr_goods)

        layout.addStretch(1)


    def setValues(self, env):

        self.nr_agents.setText(str(env.N))
        self.nr_goods.setText(str(env.M))

class ControlPanel(QtGui.QWidget):
    def __init__(self, env):
        super(ControlPanel, self).__init__()
        
        self.env = env

        self.initUI()

    def initUI(self): 
        # Layouts
        vbox              = QtGui.QVBoxLayout(self)
        hbox              = QtGui.QHBoxLayout()
        hbox_controls     = QtGui.QHBoxLayout()

        # Widgets
        self.lbl_nr_transactions   = QtGui.QLabel('Nr transactions:')
        self.lbl_status    = QtGui.QLabel('Status:')

        self.nr_transactions = QtGui.QLineEdit()
        self.nr_transactions.setReadOnly(True)

        self.status = QtGui.QLabel('Running')

        self.startButton = QtGui.QPushButton("Start")
        self.startButton.clicked.connect(self.start)
        self.pauseButton = QtGui.QPushButton("Pause")
        self.pauseButton.clicked.connect(self.pause)

        self.lcd = QtGui.QLCDNumber(self)
        slider_subgroup = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider_subgroup.valueChanged.connect(self.setDelay)

        # Add Widgets
        hbox.addWidget(self.lbl_nr_transactions)
        hbox.addWidget(self.nr_transactions)
        hbox.addWidget(self.lbl_status)
        hbox.addWidget(self.status)
        hbox.setAlignment(QtCore.Qt.AlignTop)
        hbox.addStretch(1)

        hbox_controls.addWidget(self.startButton)
        hbox_controls.addWidget(self.pauseButton)
        hbox_controls.addWidget(slider_subgroup)
        hbox_controls.addWidget(self.lcd)
        hbox_controls.addStretch(1)
        

        # Add Layouts
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_controls)
        vbox.addStretch(1)

    def setNrTransactions(self, nr):
        self.nr_transactions.setText(str(nr))

    def pause(self):
        self.status.setText('Pauses')
        self.env.running = False

    def start(self):
        self.status.setText('Running')
        self.env.running = True

    def setDelay(self, value):
        self.env.delay = value / 100
        self.lcd.display(value)


class Results(QtGui.QWidget):
    def __init__(self, env):
        super(Results, self).__init__()

        self.env = env

        self.initUI()

    def initUI(self): 
        # Layouts
        vbox              = QtGui.QVBoxLayout(self)

        # Given Received
        self.lbl_agents = QtGui.QLabel("Agents:")
        self.combo = QtGui.QComboBox() 
        self.setComboValues(self.combo)

        self.combo.activated[str].connect(self.onSelected) 

        # Yield Curve
        self.lbl_yield_curve = QtGui.QLabel("Yield Curve:")
        self.combo_P = QtGui.QComboBox() 
        self.setComboValues(self.combo_P)

        self.combo_Q = QtGui.QComboBox() 
        self.setComboValues(self.combo_Q)

        self.plot_yield_curve = QtGui.QPushButton("Plot Yield Curve")
        self.plot_yield_curve.clicked.connect(lambda: self.createYieldCurve(str(self.combo_P.currentText()), str(self.combo_Q.currentText())))

        # Add Widgets
        vbox.addWidget(self.lbl_agents)
        vbox.addWidget(self.combo)
        vbox.addWidget(self.lbl_yield_curve)
        vbox.addWidget(self.combo_P)
        vbox.addWidget(self.combo_Q)
        vbox.addWidget(self.plot_yield_curve)
        vbox.addStretch(1)
        vbox.setAlignment(QtCore.Qt.AlignTop)

    def setComboValues(self, combo):
        for agent in self.env.agents_list:
            name = 'Agent_' + str(agent.id)
            combo.addItem(name)

    def onSelected(self, text):
        id = text.strip('Agent_')
        for agent in self.env.agents_list:
            if agent.id == int(id):
                dialog = AgentInfo(agent)
                print('found:', agent.id)

    def createYieldCurve(self, P, Q):
        P_id = P.strip('Agent_')
        Q_id = Q.strip('Agent_')
        for agent in self.env.agents_list:
            if agent.id == int(P_id):
                agent_P = agent
            elif agent.id == int(Q_id):
                agent_Q = agent
        
        if agent_Q != agent_P:
            YieldCurve(agent_P, agent_Q, self.env)


class AgentInfo(QtGui.QDialog):
    def __init__(self, agent):
        super(AgentInfo, self).__init__()  
        self.agent = agent

        self.initUI()

    def initUI(self):
        vbox = QtGui.QVBoxLayout(self)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) 
        self.plotGiven()

        vbox.addWidget(self.canvas)
        self.setLayout(vbox)


        self.setGeometry(150, 150, 600, 600)
        self.setWindowTitle('Agent_' + str(self.agent.id) + ' Info')
        self.exec_()

    def plotGiven(self):
        given_received = self.agent.given_received
        given = [given_received[i][0] for i in range(len(given_received))]
        received = [given_received[i][1] for i in range(len(given_received))]
        x = np.arange(len(given_received))
        width = 0.35

        self.ax = self.figure.add_subplot(111)
        #ax2 = self.figure.add_subplot(121)
        self.ax.hold(True)
        rects1 = self.ax.bar(x, given, width, color='blue')
        rects2 = self.ax.bar(x+width, received, width, color='red')

        self.ax.set_xlim(-width,len(x)+width)
        self.ax.set_ylabel('# Given/Received')
        self.ax.set_title('Number of goods given and received to each agent')
        xTickMarks = ['Agent'+str(i) for i in range(len(given_received))]
        self.ax.set_xticks(x+width)
        xtickNames = self.ax.set_xticklabels( xTickMarks )
        plt.setp(xtickNames, rotation=45, fontsize=10)

        self.ax.legend( (rects1[0], rects2[0]), ('Given', 'Received') )
        #self.ax.hold(False)
        self.canvas.draw()

class YieldCurve(QtGui.QDialog):
    def __init__(self, P, Q, env):
        super(YieldCurve, self).__init__()

        self.P = P
        self.Q = Q 
        self.env = env 

        self.initUI()

    def initUI(self): 
        vbox = QtGui.QVBoxLayout(self)

        self.lbl_goods = QtGui.QLabel("Choose a good:")
        self.combo_goods = QtGui.QComboBox() 
        self.setGoods()

        self.combo_goods.activated[str].connect(self.onSelected) 

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) 
        self.plotYieldCurve(-0.1, 3)

        vbox.addWidget(self.lbl_goods)
        vbox.addWidget(self.combo_goods)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)

        self.setGeometry(150, 150, 600, 600)
        self.setWindowTitle('Yield Curve')
        self.exec_()

    def plotYieldCurve(self, like_factor, nominal_value):
        min_x = nominal_value / like_factor
        max_x = nominal_value / -like_factor
        x = np.arange(-50, 50, 0.01)
        y = like_factor * x + nominal_value
        z = -0.3 * x + 2
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(x, y)

        ax.spines['left'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        xTickMarks = ['Low Balance', 'High Balance']
        ax.set_xticklabels( xTickMarks )
        ax.set_xticks([-50, 50])
        ax.set_ylim(ymin=0)

        self.canvas.draw()

    def setGoods(self):
        for good in self.env.goods_list:
            name = 'Good_' + str(good.id)    
            self.combo_goods.addItem(name)

    def onSelected(self, text):
        id = text.strip('Good_')
        for good in self.env.goods_list:
            if good.id == int(id):
                #dialog = AgentInfo(agent)
                print('found:', good.id)


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Output()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 



