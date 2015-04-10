import sys
from PyQt4 import QtGui

N = 3
# Total goods
M = 1
# Number of goods that are perishable
M_perishable = 0
perish_factor = 0
# stable at prodcution_time = M * perish_factor
production_time = 0
value = 1

class Input(QtGui.QWidget):
    
    def __init__(self):
        super(Input, self).__init__()
        self.N = 3
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

        nr_goods = QtGui.QSpinBox(self)
        nr_goods.setGeometry(15, 90, 100, 25)
        nr_goods.setMaximum(10000)


        self.setGeometry(200, 200, 440, 640)
        self.setWindowTitle('Input') 
        self.show()

    def setAgents(self, value):
    	global N 
    	N = self.nr_agents.value()
    	print(N)
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Input()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 