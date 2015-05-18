import sys, time, os
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import numpy as np
from prettyplotlib import brewer2mpl
import prettyplotlib as ppl
import string
import csv

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from vispyTest import Canvas
from Visualisation import Canvas
import Simulate as sim

class Output(QtGui.QMainWindow):
    
    def __init__(self, env):
        super(Output, self).__init__()

        self.env = env
        self.initUI()
        

    def initUI(self):

        # Menu bar
        self.menubar = QtGui.QMenuBar()
        
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction('Save', lambda: self.saveData('untitled.txt'))
        fileMenu.addAction('Save As', lambda: self.showDialog())
        fileMenu.addAction('CSV test', lambda: self.save_data())
        fileMenu.addAction('Load', lambda: self.load_data())

        self.setMenuBar(self.menubar)

        # Frames
        self.gui = GUI(self.env)
        self.setCentralWidget(self.gui)
        
        # Window size
        screen = QtGui.QDesktopWidget().availableGeometry()
        width = screen.width() - 300
        height = screen.height()
        #print('width:', width)
        #print('height:', height)


        self.setGeometry(300, 50, width, height)
        self.setWindowTitle('The Giving Game - Simulation')    
        self.show()

    def saveData(self, fname):
        f = open(fname, 'w')
        f.write('Number of agents: ' + str(self.env.N) + '\n')
        f.write('Number of goods: ' + str(self.env.M) + '\n')
        f.write('Balance matrix: ' + str(self.env.balance_matrix) + '\n')

        f.close()
    def save_data(self):
        path = 'results/' + time.strftime("%d-%m-%Y") + '_' + time.strftime("%H:%M:%S")

        if not os.path.exists(path):
            os.makedirs(path)
            self.save_input(path)
            self.save_balance(path)

    def save_input(self, path):
        fname = 'input.csv'
        with open(os.path.join(path, fname), 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            data = [[str(self.env.N)],
                    [str(self.env.M)],
                    [str(self.env.parallel)],
                    [str(self.env.selection_rule)],
                    [str(self.env.goods_parameters)]]

            writer.writerows(data)
            # if self.env.goods_parameters:
            #     writer.writerows(self.env.goods_parameters)

    def save_balance(self, path):
        fname = 'balance.csv'
        with open(os.path.join(path, fname), 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            data = [['balance_matrix']]
            writer.writerows(data)
            writer.writerows(self.env.balance_matrix)

    def load_data(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Save file', 
        '/home')
        
        if fname != '':
            #self.saveData(fname)
            print(fname)

    def showDialog(self):

        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                '/home')
        
        if fname != '':
            self.saveData(fname)

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
        # self.groupBox_bottom_left = QtGui.QGroupBox(self)
        # self.groupBox_bottom_right = QtGui.QGroupBox(self)
        self.groupBox_bottom = QtGui.QGroupBox(self)

        self.groupBox_left.setMinimumWidth(300)
        self.groupBox_top.setMinimumHeight(150)
        # self.groupBox_bottom_left.setMinimumWidth(600)
        # self.groupBox_bottom_right.setMinimumWidth(300)
        self.groupBox_bottom.setMinimumWidth(800)

        # Widgets
        self.tabs = Tabs(self.env)
        self.general_results = GeneralResults()
        #self.general_results = Browser()
        self.general_results.setValues(self.env)
        self.control_panel = ControlPanel(self.env)
        self.results = Results(self.env)

        # Add layouts
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        right_layout.addLayout(top_layout)
        right_layout.addLayout(bottom_layout)

        # bottom_layout.addLayout(bottom_left_layout)
        # bottom_layout.addLayout(bottom_right_layout)

        # Add Widgets
        left_layout.addWidget(self.groupBox_left)
        # left_layout.addWidget(self.general_results)
        # self.general_results.setMinimumWidth(200)
        top_layout.addWidget(self.groupBox_top)

        # bottom_left_layout.addWidget(self.groupBox_bottom_left)
        # bottom_right_layout.addWidget(self.groupBox_bottom_right)
        bottom_layout.addWidget(self.groupBox_bottom)
        
        # Fill groupboxes
        vbox_left = QtGui.QVBoxLayout(self.groupBox_left)
        #vbox_left.addWidget(self.general_results)
        vbox_left.addWidget(self.results)

        vbox_top = QtGui.QVBoxLayout(self.groupBox_top)
        vbox_top.addWidget(self.control_panel)

        # vbox_bottom_left = QtGui.QVBoxLayout(self.groupBox_bottom_left)
        # vbox_bottom_left.addWidget(self.tabs)
        vbox_bottom = QtGui.QVBoxLayout(self.groupBox_bottom)
        vbox_bottom.addWidget(self.tabs)

        #vbox_bottom_right = QtGui.QVBoxLayout(self.groupBox_bottom_right)
        #vbox_bottom_right.addWidget(self.results)

class Tabs(QtGui.QTabWidget):
    def __init__(self, env):
        super(Tabs, self).__init__()

        self.env = env
        self.initUI()

    def initUI(self):
        self.tab1    = QtGui.QWidget()   
        self.tab2    = QtGui.QWidget()
        self.tab3    = QtGui.QWidget()
        self.tab4   = QtGui.QWidget()

        # Layout
        self.layout_tab1 = QtGui.QHBoxLayout()
        self.layout_tab2 = QtGui.QVBoxLayout()
        self.layout_tab3 = QtGui.QVBoxLayout()
        self.layout_tab4 = QtGui.QVBoxLayout()

        # Widgets
        self.figure = plt.figure()
        self.bar_plot = FigureCanvas(self.figure) 
        self.plot(self.figure, self.bar_plot)

        self.figure2 = plt.figure()
        self.balance_plot = FigureCanvas(self.figure2) 
        self.toolbar = NavigationToolbar(self.bar_plot, self)
        #self.plot(self.figure, self.bar_plot)
        self.plot_balance()

        self.figure3 = plt.figure(figsize=(3,8))
        self.color_bar = FigureCanvas(self.figure3)
        #self.color_bar.setMaximumWidth(100)
        self.plot_color_bar()

        self.visualisation = Canvas(self.env)

        self.textBox = QtGui.QTextEdit()
        self.textBox.setReadOnly(True)
        self.textBox.insertHtml("<FONT color=green >"+'fsdfdsfsdfdsfsdfsd'+"</FONT>")

        # Reset button
        self.reset = QtGui.QPushButton('Plot transaction percentages')
        # self.reset.clicked.connect(self.resetTransactions)
        self.reset.clicked.connect(self.plotGoodTransactionPercentages)
        

        # Set layout
        self.tab1.setLayout(self.layout_tab1)
        self.tab2.setLayout(self.layout_tab2) 
        self.tab3.setLayout(self.layout_tab3)
        self.tab4.setLayout(self.layout_tab4)  

        # Add Widgets
        self.layout_tab1.addWidget(self.visualisation.native)
        self.layout_tab1.addWidget(self.color_bar)
        self.layout_tab2.addWidget(self.reset)
        self.layout_tab2.addWidget(self.bar_plot)
        self.layout_tab2.addWidget(self.toolbar)
        self.layout_tab3.addWidget(self.textBox)
        self.layout_tab4.addWidget(self.balance_plot)


        
        # Add tabs
        self.addTab(self.tab1,"Visualisation")
        self.addTab(self.tab2,"Comunnity percentage")
        #self.addTab(self.tab3,"Transctions")
        #self.addTab(self.tab4,"Balance")

    def plot_color_bar(self):
        ax1 = self.figure3.add_axes([0.05, 0.05, 0.2, 0.9])
        # Set the colormap and norm to correspond to the data for which
        # the colorbar will be used.
        # cmap = mpl.cm.coolwarm
        # norm = mpl.colors.Normalize(vmin=0, vmax=1)

        # ColorbarBase derives from ScalarMappable and puts a colorbar
        # in a specified axes, so it has everything needed for a
        # standalone colorbar.  There are many more kwargs, but the
        # following gives a basic continuous colorbar with ticks
        # and labels.
        cmap = mpl.colors.ListedColormap([[0.0, 0.0, 1.], [0.1, 0., 0.9], [0.2, 0.0, 0.8], [0.3, 0.0, 0.7], [0.4, 0.0, 0.6], [0.5, 0.0, 0.5], [0.6, 0.0, 0.4], [0.7, 0.0, 0.3], [0.8, 0.0, 0.2], [0.9, 0.0, 0.1]])
        bounds = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


        # The second example illustrates the use of a ListedColormap, a
        # BoundaryNorm, and extended ends to show the "over" and "under"
        # value colors.
        # cmap = mpl.colors.ListedColormap(['r', 'g', 'b', 'c'])
        # cmap.set_over((1.0, 0.0, 0.0))
        # cmap.set_under((0.0, 0.0, 1.0))


        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                    norm=norm,
                                    spacing='proportional',
                                    ticks=bounds,
                                   orientation='vertical')

        cb1.set_label('Transaction percentage')

        self.figure3.set_facecolor('white')
        self.color_bar.draw()

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

        # Design
        #self.figure.tight_layout()
        self.figure.set_facecolor('white')

        self.bar_plot.draw()

    def plot_balance(self):
        time.sleep(self.env.delay)
        x = np.arange(10)
        ax = self.figure2.add_subplot(111)
        #fig = self.figure2.add_subplot(111)
        np.random.seed(10)

        ppl.pcolormesh(self.figure2, ax, np.random.randn(10,10))

        ax.set_title('transaction percentage of each good for each agent')
        xTickMarks = ['Agent'+str(i) for i in range(len(x))]
        ax.set_xticks(x+0.5)
        ax.set_yticks(x+0.5)
        xtickNames = ax.set_xticklabels( xTickMarks )
        ax.set_yticklabels( xTickMarks )
        plt.setp(xtickNames, rotation=90, fontsize=10)

        self.figure2.tight_layout()
        self.balance_plot.draw()

    def print_transaction(self, P, Q, good):
        time.sleep(self.env.delay)
        transaction = 'Agent_' + str(P.id) + ' --> ' + 'Agent_' + str(Q.id) + ' good: ' + str(good.id)
        self.textBox.append(transaction)
        QtGui.qApp.processEvents()

    def print_time_until_production(self, good):
        time.sleep(self.env.delay)
        time_until_production = 'Good_' + str(good.id) + ' --> Time until production: ' + str(good.time_until_production)
        self.textBox.append(time_until_production)
        QtGui.qApp.processEvents()

    def print_production(self, good):
        time.sleep(self.env.delay)
        production = 'Good_' + str(good.id) + ' is being produced.'
        self.textBox.append(production)
        QtGui.qApp.processEvents()

    def updateV(self):
        self.visualisation.createGrid()

    def moveV(self, Q, good):
        self.visualisation.move(Q, good)

    def colorV(self):
        self.visualisation.updateColor()

    def resetTransactions(self):
        for agent in self.env.agents_list:
            agent.nr_transactions = 0
            count = 0
            for good in agent.goods_transactions:
                good[1] = 0
                self.env.nr_good_transactions[count] = 0

        self.env.nr_transactions = 0


class GeneralResults(QtGui.QWidget):
    def __init__(self):
        super(GeneralResults, self).__init__()
        
        self.initUI()

    def initUI(self): 
        layout              = QtGui.QVBoxLayout(self)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(14)
        #self.setStyleSheet("QWidget { background-color: Red }")
        self.lbl_selection_rule = QtGui.QLabel('Selection rule:')
        self.lbl_simulation_type = QtGui.QLabel('Simulation type:')
        self.lbl_nr_agents      = QtGui.QLabel('Number of agents:')
        self.lbl_nr_goods       = QtGui.QLabel('Number of goods:')
        self.lbl_goods = QtGui.QLabel('Goods information')

        self.lbl_selection_rule.setFont(font)
        self.lbl_simulation_type.setFont(font)
        self.lbl_nr_agents.setFont(font)
        self.lbl_nr_goods.setFont(font)
        self.lbl_goods.setFont(font)



        self.selection_rule = QtGui.QLabel('')
        self.simulation_type = QtGui.QLabel('')
        self.nr_agents      = QtGui.QLabel('')
        self.nr_goods       = QtGui.QLabel('')
        self.goods = QtGui.QTextEdit()
        self.goods.setReadOnly(True)

        layout.addWidget(self.lbl_selection_rule)
        layout.addWidget(self.selection_rule)
        layout.addWidget(self.lbl_simulation_type)
        layout.addWidget(self.simulation_type)
        layout.addWidget(self.lbl_nr_agents)
        layout.addWidget(self.nr_agents)
        layout.addWidget(self.lbl_nr_goods)
        layout.addWidget(self.nr_goods)
        layout.addWidget(self.lbl_goods)
        layout.addWidget(self.goods)

        layout.addStretch(1)


    def setValues(self, env):
        if env.selection_rule == 0:
            self.selection_rule.setText('Random rule')
        elif env.selection_rule == 1:
            self.selection_rule.setText('Balance rule')
        elif env.selection_rule == 2:
            self.selection_rule.setText('Goodwill rule')

        if env.parallel:
            self.simulation_type.setText('Parallel')
        else:
            self.simulation_type.setText('One by one')

        self.nr_agents.setText(str(env.N))
        self.nr_goods.setText(str(env.M))
        count = 0
        for good in env.goods_parameters:
            text = 'Good_' + str(count) + '\n Perish time: ' + str(good[0]) + ',\n Production delay: ' + str(good[1]) + ',\n Nominal value: ' + str(good[2])
            self.goods.append(text)
            count += 1

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
        slider_delay = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider_delay.valueChanged.connect(self.setDelay)

        # Add Widgets
        hbox.addWidget(self.lbl_nr_transactions)
        hbox.addWidget(self.nr_transactions)
        hbox.addWidget(self.lbl_status)
        hbox.addWidget(self.status)
        hbox.setAlignment(QtCore.Qt.AlignTop)
        hbox.addStretch(1)

        hbox_controls.addWidget(self.startButton)
        hbox_controls.addWidget(self.pauseButton)
        hbox_controls.addWidget(slider_delay)
        hbox_controls.addWidget(self.lcd)
        hbox_controls.addStretch(1)
        

        # Add Layouts
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_controls)
        vbox.addStretch(1)

    def setNrTransactions(self, nr):
        self.nr_transactions.setText(str(nr))

    def pause(self):
        self.status.setText('Paused')
        self.env.running = False

    def start(self):
        self.status.setText('Running')
        self.env.running = True
        sim.continue_simulation(self.env, self.env.selection_rule, self.env.output, self.env.total_transactions)

    def setDelay(self, value):
        self.env.delay = value / 100
        self.lcd.display(value)

    def testSleep(self):
        #self.env.running = False
        self.status.setText('Paused')
        QtCore.QTimer.singleShot(2000, lambda: self.status.setText('Running'))
        self.env.running = True


class Results(QtGui.QWidget):
    def __init__(self, env):
        super(Results, self).__init__()

        self.env = env
        self.count = 0

        self.initUI()

    def initUI(self): 
        # Layouts
        vbox              = QtGui.QVBoxLayout(self)
        hbox              = QtGui.QHBoxLayout()
        hbox2             = QtGui.QHBoxLayout()

        fontHeader = QtGui.QFont()
        fontHeader.setBold(True)
        fontHeader.setPointSize(16)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(14)

        self.lbl_data = QtGui.QLabel("Enviroment data")
        self.lbl_data.setFont(fontHeader)

        # Given Received
        self.lbl_agents = QtGui.QLabel("Agents:")
        self.lbl_agents.setFont(font)
        self.combo = QtGui.QComboBox() 
        self.setComboValues(self.combo)

        self.combo.activated[str].connect(self.onSelected) 

        # Yield Curve
        self.lbl_yield_curve = QtGui.QLabel("Yield Curve:")
        self.lbl_yield_curve.setFont(font)
        self.combo_P = QtGui.QComboBox() 
        self.setComboValues(self.combo_P)

        self.combo_Q = QtGui.QComboBox() 
        self.setComboValues(self.combo_Q)

        self.plot_yield_curve = QtGui.QPushButton("Plot Yield Curve")
        self.plot_yield_curve.clicked.connect(lambda: self.createYieldCurve(str(self.combo_P.currentText()), str(self.combo_Q.currentText())))

        # Community effect
        self.lbl_communityeffect = QtGui.QLabel('Community effect')
        self.lbl_communityeffect.setFont(fontHeader)

        self.lbl_subgroup = QtGui.QLabel('Subgroup size:')
        self.lbl_subgroup.setFont(font)

        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.display(2)
        self.slider_subgroup = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_subgroup.setMinimum(2)
        self.slider_subgroup.setMaximum(self.env.N)
        self.slider_subgroup.valueChanged.connect(self.setSubgroup)


        self.goods_combo = QtGui.QComboBox()
        self.setGoodComboValues(self.goods_combo)
        self.goods_combo.activated[str].connect(self.setIndex) 

        self.lbl_percentage = QtGui.QLabel('Transaction percentage:')
        self.percentage = QtGui.QLineEdit()
        # Read only
        self.percentage.setEnabled(False)

        self.lbl_transactions = QtGui.QLabel('Transactions')
        self.lbl_transactions.setFont(fontHeader)
        self.textBox = QtGui.QTextEdit()
        self.textBox.setReadOnly(True)
        #self.textBox.setText('Agent_0 -> Agent_1, Good_0')

        # Reset 
        self.reset = QtGui.QPushButton('Reset percentage')
        self.reset.clicked.connect(self.resetTransactions)



        # Add Widgets
        vbox.addWidget(self.lbl_data)
        vbox.addWidget(self.lbl_agents)
        vbox.addWidget(self.combo)
        vbox.addWidget(self.lbl_yield_curve)
        vbox.addWidget(self.combo_P)
        vbox.addWidget(self.combo_Q)
        vbox.addWidget(self.plot_yield_curve)
        vbox.addWidget(self.lbl_communityeffect)
        vbox.addWidget(self.lbl_subgroup)
        vbox.addLayout(hbox)

        hbox.addWidget(self.slider_subgroup)
        hbox.addWidget(self.lcd)

        vbox.addWidget(self.goods_combo)
        vbox.addLayout(hbox2)

        hbox2.addWidget(self.lbl_percentage)
        hbox2.addWidget(self.percentage)

        vbox.addWidget(self.reset)
        vbox.addWidget(self.lbl_transactions)
        vbox.addWidget(self.textBox, 10)

        vbox.addStretch(1)
        vbox.setAlignment(QtCore.Qt.AlignTop)


    def setComboValues(self, combo):
        for agent in self.env.agents_list:
            name = 'Agent_' + str(agent.id)
            combo.addItem(name)

    def setGoodComboValues(self, combo):
        for good in self.env.goods_list:
            name = 'Good_' + str(good.id)
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

    def setSubgroup(self, value):
        self.env.subgroup_size = value
        self.lcd.display(value)

    def setIndex(self, text):
        good_id = int(text.strip('Good_'))
        self.env.index = good_id
        #self.percentage.setText(text)

    def setPercentage(self, value):
        self.percentage.setText(str(round(value,2)))

    def print_transaction(self, P, Q, good):
        time.sleep(self.env.delay)
        if self.count == 100:
            self.textBox.clear()
            self.count = 0
        transaction = 'Agent_' + str(P.id) + ' --> ' + 'Agent_' + str(Q.id) + ', Good: ' + str(good.id)
        #self.textBox.append(transaction)
        self.textBox.insertHtml("<FONT color=black >"+transaction+"</FONT><br>")
        self.textBox.verticalScrollBar().setValue(self.textBox.verticalScrollBar().maximum())
        self.count += 1
        QtGui.qApp.processEvents()

    def print_time_until_production(self, good):
        time.sleep(self.env.delay)

        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("red")))

        time_until_production = 'Good_' + str(good.id) + ' --> Time until production: ' + str(good.time_until_production)
        #self.textBox.append(time_until_production)
        self.textBox.insertHtml("<FONT color=red >"+time_until_production+"</FONT><br>")
        self.textBox.verticalScrollBar().setValue(self.textBox.verticalScrollBar().maximum())
        QtGui.qApp.processEvents()

    def print_production(self, good):
        time.sleep(self.env.delay)
        production = 'Good_' + str(good.id) + ' is being produced.'
        #self.textBox.append(production)
        self.textBox.insertHtml("<FONT color=green >"+production+"</FONT><br>")
        self.textBox.verticalScrollBar().setValue(self.textBox.verticalScrollBar().maximum())
        QtGui.qApp.processEvents()

    def resetTransactions(self):
        for agent in self.env.agents_list:
            agent.nr_transactions = 0
            count = 0
            for good in agent.goods_transactions:
                good[1] = 0
                self.env.nr_good_transactions[count] = 0

        self.env.nr_transactions = 0


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

        self.toolbar = NavigationToolbar(self.canvas, self)

        vbox.addWidget(self.canvas)
        vbox.addWidget(self.toolbar)
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

        # Design
        self.figure.set_facecolor('white')

        self.canvas.draw()


class YieldCurve(QtGui.QDialog):
    def __init__(self, P, Q, env):
        super(YieldCurve, self).__init__()

        self.P = P
        self.Q = Q
        self.good_id = 0 
        self.env = env 

        self.initUI()

    def initUI(self): 
        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()
        vbox2 = QtGui.QVBoxLayout()

        self.lbl_goods = QtGui.QLabel("Choose a good:")
        self.combo_goods = QtGui.QComboBox() 
        self.setGoods()

        self.combo_goods.activated[str].connect(self.onSelected) 

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.lbl_yield_value = QtGui.QLabel('Yield values')
        self.lbl_P_Q = QtGui.QLabel('Agent_' + str(self.P.id) + ' --> ' + 'Agent_' + str(self.Q.id))
        self.yield_value_PQ = QtGui.QLineEdit()
        self.lbl_Q_P = QtGui.QLabel('Agent_' + str(self.Q.id) + ' --> ' + 'Agent_' + str(self.P.id))
        self.yield_value_QP = QtGui.QLineEdit()


        self.lbl_like_factor = QtGui.QLabel('Like factors')
        self.lbl_like_factor_P_Q = QtGui.QLabel('Agent_' + str(self.P.id) + ' --> ' + 'Agent_' + str(self.Q.id))
        self.like_factor_PQ = QtGui.QLineEdit()
        self.lbl_like_factor_Q_P = QtGui.QLabel('Agent_' + str(self.Q.id) + ' --> ' + 'Agent_' + str(self.P.id))
        self.like_factor_QP = QtGui.QLineEdit()

        vbox.addWidget(self.lbl_goods)
        vbox.addWidget(self.combo_goods)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.toolbar)

        vbox2.addWidget(self.lbl_yield_value)
        vbox2.addWidget(self.lbl_P_Q)
        vbox2.addWidget(self.yield_value_PQ)
        vbox2.addWidget(self.lbl_Q_P)
        vbox2.addWidget(self.yield_value_QP)

        vbox2.addWidget(self.lbl_like_factor)
        vbox2.addWidget(self.lbl_like_factor_P_Q)
        vbox2.addWidget(self.like_factor_PQ)
        vbox2.addWidget(self.lbl_like_factor_Q_P)
        vbox2.addWidget(self.like_factor_QP)
        self.setValues()
        vbox2.addStretch(1)

        hbox.addLayout(vbox)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        self.setGeometry(150, 150, 800, 600)
        self.setWindowTitle('Yield Curve')
        self.exec_()

    def plotYieldCurve(self, like_factor, nominal_value):
        min_x = nominal_value / like_factor
        max_x = nominal_value / -like_factor
        min_x2 = 4 / -0.23
        max_x2 = 4 / 0.23
        x = np.arange(min(min_x, min_x2), max(max_x, max_x2), 0.01)
        y = like_factor * x + nominal_value
        y2 = 0.23 * x + 4
        z = -0.3 * x + 2
        ax = self.figure.add_subplot(111)
        ax.hold(True)
        ax.plot(x, y)
        ax.plot(x, y2, color='red')

        ax.spines['left'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        xTickMarks = ['Low Balance P/High Balance Q', 'Low Balance Q/High Balance P']
        ax.set_xticklabels( xTickMarks )
        ax.set_xticks([min_x, max_x])
        ax.set_ylim(ymin=0)

        self.canvas.draw()

    def plotYieldCurve2(self, good):
        self.figure.clf()
        # P
        P_likefactor = self.P.like_factor[self.Q.id]
        P_min_x = good.value / P_likefactor
        P_max_x = good.value / -P_likefactor
        # Q
        Q_likefactor = self.Q.like_factor[self.P.id]
        Q_min_x = good.value / Q_likefactor
        Q_max_x = good.value / -Q_likefactor
        print(P_likefactor, Q_likefactor)
        x = np.arange(min(P_min_x, Q_min_x), max(P_max_x, Q_max_x), 0.01)
        P_y = P_likefactor * x + good.value
        Q_y = -Q_likefactor * x + good.value

        ax = self.figure.add_subplot(111)
        
        ax.plot(x, P_y, color='blue')
        ax.plot(x, Q_y, color='red')

        ax.spines['left'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        xTickMarks = ['Low Balance P/High Balance Q', 'Low Balance Q/High Balance P']
        ax.set_xticklabels( xTickMarks )
        ax.set_xticks([min(P_min_x, Q_min_x), max(P_max_x, Q_max_x)])
        ax.set_ylim(ymin=0)
        ax.hold(True)

        self.figure.tight_layout()
        self.figure.set_facecolor('white')

        self.canvas.draw()

    def setGoods(self):
        for good in self.env.goods_list:
            name = 'Good_' + str(good.id)    
            self.combo_goods.addItem(name)

    def setValues(self):
        self.yield_value_PQ.setText("%.4f" % self.P.yield_values[self.good_id][self.Q.id])
        self.yield_value_QP.setText("%.4f" % self.Q.yield_values[self.good_id][self.P.id])
        self.like_factor_PQ.setText("%.4f" % self.P.like_factor[self.Q.id])
        self.like_factor_QP.setText("%.4f" % self.Q.like_factor[self.P.id])

    def onSelected(self, text):
        id = text.strip('Good_')
        for good in self.env.goods_list:
            if good.id == int(id):
                #good.value += 1
                self.plotYieldCurve2(good)
                self.good_id = good.id

class Browser(QtGui.QWidget):
    def __init__(self):
        super(Browser, self).__init__()

        self.initUI()

    def initUI(self): 

        self.resize(700, 500)
        self.treeView = QtGui.QTreeView()
        self.fileSystemModel = QtGui.QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)
        self.fileSystemModel.setRootPath( QtCore.QDir.currentPath() )
        root = self.fileSystemModel.setRootPath("/")
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(root)

        Layout = QtGui.QVBoxLayout(self)
        Layout.addWidget(self.treeView)
    

class SaveAs(QtGui.QDialog):
    def __init__(self, env):
        super(SaveAs, self).__init__()

        self.env = env 

        self.initUI()

    def initUI(self): 

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            print(data)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')

        self.exec_()

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Output()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 



