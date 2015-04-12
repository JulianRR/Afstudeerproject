import sys
from PyQt4 import QtGui
import Simulate as sim

# N = 3
# # Total goods
# M = 1
# # Number of goods that are perishable
# M_perishable = 0
# perish_factor = 0
# # stable at prodcution_time = M * perish_factor
# production_time = 0
# value = 1

class Input(QtGui.QWidget):
    
    def __init__(self):
        super(Input, self).__init__()
        
        # Total agents
        self.N = 10
        # Total goods
        self.M = 3
        # Number of goods that are perishable
        self.M_perishable = 3
        self.perish_factor = 2
        # stable at prodcution_time = M * perish_factor
        self.production_time = 6
        self.value = 1

        self.initUI()
        

    def initUI(self):

        # Agents
        lbl_nr_agents = QtGui.QLabel('Number of Agents', self)
        lbl_nr_agents.move(15, 10)

        self.nr_agents = QtGui.QSpinBox(self)
        self.nr_agents.setGeometry(15, 30, 100, 25)
        self.nr_agents.setMaximum(10000)

        self.nr_agents.valueChanged.connect(self.setAgents)

        # Goods
        lbl_nr_goods = QtGui.QLabel('Number of Goods', self)
        lbl_nr_goods.move(15, 60)

        self.nr_goods = QtGui.QSpinBox(self)
        self.nr_goods.setGeometry(15, 80, 100, 25)
        self.nr_goods.setMaximum(10000)

        self.nr_goods.valueChanged.connect(self.setGoods)

        # Perishable Goods
        lbl_nr_perishable = QtGui.QLabel('Number of perishable goods', self)
        lbl_nr_perishable.move(15, 110)

        self.nr_perishable = QtGui.QSpinBox(self)
        self.nr_perishable.setGeometry(15, 130, 100, 25)
        self.nr_perishable.setMaximum(10000)

        self.nr_perishable.valueChanged.connect(self.setPerishable)

        # Perish factor
        lbl_perish_factor = QtGui.QLabel('Perish factor', self)
        lbl_perish_factor.move(15, 160)

        self.perish = QtGui.QSpinBox(self)
        self.perish.setGeometry(15, 180, 100, 25)
        self.perish.setMaximum(10000)

        self.perish.valueChanged.connect(self.setPerishFactor)

        # Production time
        lbl_production_time = QtGui.QLabel('Production time', self)
        lbl_production_time.move(15, 210)

        self.p_time = QtGui.QSpinBox(self)
        self.p_time.setGeometry(15, 230, 100, 25)
        self.p_time.setMaximum(10000)

        self.p_time.valueChanged.connect(self.setProductionTime)

        # Value of goods
        lbl_value = QtGui.QLabel('Value of the goods', self)
        lbl_value.move(15, 260)

        self.good_value = QtGui.QSpinBox(self)
        self.good_value.setGeometry(15, 280, 100, 25)
        self.good_value.setMaximum(10000)

        self.good_value.valueChanged.connect(self.setValue)

        self.start = QtGui.QPushButton('Simulate', self)
        self.start.setGeometry(100, 320, 100, 50)
        self.start.clicked.connect(self.startSimulation)

        self.setGeometry(200, 200, 300, 375)
        self.setWindowTitle('The Giving Game - Input') 
        self.show()

    def setAgents(self, value): 
        self.N = self.nr_agents.value()
        print('Number of agents: ', self.N)

    def setGoods(self, value): 
        self.M = self.nr_goods.value()
        print('Total goods: ', self.M)

    def setPerishable(self, value):
        self.M_perishable = self.nr_perishable.value()
        if self.M_perishable > self.M:
            print("Too many perishable goods, number of perishable goods set to 0")
            self.M_perishable = 0
        else:
            print('Number of perishable goods:', self.M_perishable)

    def setPerishFactor(self, value): 
        if self.M_perishable == 0:
            print('No goods are perishable, perish factor set to 0')
            self.perish_factor = 0
        else:
            self.perish_factor = self.perish.value()
        print('Perisch factor: ', self.perish_factor)

    def setProductionTime(self, value): 
        self.production_time = self.p_time.value()
        print('Production time: ', self.production_time)

    def setValue(self, value): 
        self.value = self.good_value.value()
        print('Value of the goods: ', self.value)

    def startSimulation(self):
        self.output = Output()
        sim.start_simulation(self.N, self.M, self.M_perishable, self.perish_factor, self.production_time, self.value, self.output)

class Output(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.initUI()
        

    def initUI(self):
        self.te = QtGui.QTextEdit()
        self.te.setReadOnly(True)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.te)
        self.setLayout(layout)

        self.setGeometry(500, 200, 400, 375)
        self.setWindowTitle('The Giving Game - Output')
        self.show()

    def print_transaction(self, P, Q, good):
        transaction = 'Agent_' + str(P) + ' --> ' + 'Agent_' + str(Q) + ' good: ' + str(good.id)
        self.te.append(transaction)

     
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Input()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 