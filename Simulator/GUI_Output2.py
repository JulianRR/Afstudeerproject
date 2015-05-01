import sys, time
import matplotlib.pyplot as plt
import random
import numpy as np

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
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

        self.setMenuBar(self.menubar)

        # Frames
        self.gui = GUI(self.env)
        self.setCentralWidget(self.gui)
        
        self.setGeometry(300, 50, 1100, 800)
        self.setWindowTitle('Menubar')    
        self.show()

    def saveData(self, fname):
        f = open(fname, 'w')
        f.write('Number of agents: ' + str(self.env.N) + '\n')
        f.write('Number of goods: ' + str(self.env.M) + '\n')
        f.write('Balance matrix: ' + str(self.env.balance_matrix) + '\n')

        f.close()

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
        self.groupBox_bottom_left = QtGui.QGroupBox(self)
        self.groupBox_bottom_right = QtGui.QGroupBox(self)

        self.groupBox_left.setMinimumWidth(200)
        self.groupBox_top.setMinimumHeight(150)
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

        self.visualisation = Canvas(self.env)

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
        self.visualisation.createGrid()

    def moveV(self, Q, good):
        self.visualisation.move(Q, good)

    def colorV(self, P, Q):
        self.visualisation.updateColor(P, Q)

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

        self.lbl_selection_rule.setFont(font)
        self.lbl_simulation_type.setFont(font)
        self.lbl_nr_agents.setFont(font)
        self.lbl_nr_goods.setFont(font)



        self.selection_rule = QtGui.QLabel('')
        self.simulation_type = QtGui.QLabel('')
        self.nr_agents      = QtGui.QLabel('')
        self.nr_goods       = QtGui.QLabel('')

        layout.addWidget(self.lbl_selection_rule)
        layout.addWidget(self.selection_rule)
        layout.addWidget(self.lbl_simulation_type)
        layout.addWidget(self.simulation_type)
        layout.addWidget(self.lbl_nr_agents)
        layout.addWidget(self.nr_agents)
        layout.addWidget(self.lbl_nr_goods)
        layout.addWidget(self.nr_goods)

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

        self.initUI()

    def initUI(self): 
        # Layouts
        vbox              = QtGui.QVBoxLayout(self)
        hbox              = QtGui.QHBoxLayout()
        hbox2             = QtGui.QHBoxLayout()

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

        # Community effect
        self.lbl_communityeffect = QtGui.QLabel('Community effect')

        self.lbl_subgroup = QtGui.QLabel('Subgroup size:')

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


        # Add Widgets
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

        self.canvas.draw()

    def setGoods(self):
        for good in self.env.goods_list:
            name = 'Good_' + str(good.id)    
            self.combo_goods.addItem(name)

    def onSelected(self, text):
        id = text.strip('Good_')
        for good in self.env.goods_list:
            if good.id == int(id):
                #good.value += 1
                self.plotYieldCurve2(good)

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



