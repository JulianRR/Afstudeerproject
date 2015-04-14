from Agent import Agent
from Goods import Goods
from Create_Enviroment import Enviroment
from GUI_Input import Input

import Selection_rules as sl
import numpy as np
from random import randint

import sys
from PyQt4 import QtGui

def create_enviroment(N, M, goods_list, M_perishable, perish_period, production_delay, value):

	enviroment = Enviroment(N, M, M_perishable, perish_period, production_delay, value)

	# Create the agents
	enviroment.create_agents()

	# Create the products
	enviroment.create_goods(goods_list)

	# Select random agents to start with
	enviroment.select_start_agents()

	return enviroment

def simulate(nr_iterations, env, selectionrule, output):
	total_transactions = 0
	for x in range(nr_iterations):
		for agent in env.current_agents[:]:
			current_agent = agent[0]
			good = agent[1]

			# Select next agent with selection rule
			next_agent = env.select_agent(selectionrule, current_agent)

			# Do the transaction
			env.transaction(current_agent, next_agent, good)
			#print(good.life)
			total_transactions += 1
			output.print_transaction(current_agent, next_agent, good)

			# Update the balance matrix
			env.update_balancematrix(current_agent, next_agent)

			# Set the selected agent as the current agent if the good is still alive.
			if good.perish_period == 0 or good.life > 0:
				env.current_agents[env.current_agents.index(agent)] = (next_agent, good)
			else:
				# Remove the perished product and the agent holding it from the list
				env.notify_producer(good)
				env.current_agents.remove(agent)
				env.goods_list.remove(good)
			
			# Produce goods after every transaction, if it is time to produce.
		env.produce_goods(selectionrule)

	env.calculate_comunnityeffect(total_transactions)
	# output.te.append(str(env.transaction_percentages))
	# sum = 0
	# for x in env.transaction_percentages:
	# 	sum += x
	# output.te.append(str(sum))
	# output.te.append(str(total_transactions))

def start_simulation(N, M, goods_list, M_perishable, perish_period, production_delay, value, output):
	# Variables which should be set by the user
	# N = 10
	# # Total goods
	# M = 3
	# # Number of goods that are perishable
	# M_perishable = 3
	# perish_period = 2
	# # stable at prodcution_time = M * perish_period
	# production_delay = 6
	# value = 1
	#app = QtGui.QApplication(sys.argv)
	#output = Output()
	#output.show()
	#output.exec_()
	#output.te.append('dsgdsgfdgdfgdf')
	env = create_enviroment(N, M, goods_list, M_perishable, perish_period, production_delay, value)
	simulate(100, env, sl.random_rule, output)
	
	# for agent in env.agents_list:
	# 	print(agent.position, agent.given_received, agent.listoftransactions)
	# print(env.balance_matrix)
	# print(env.goods_list)
	#return output
