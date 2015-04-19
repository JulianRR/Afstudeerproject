from Agent import Agent
from Goods import Goods
from Create_Enviroment import Enviroment
from GUI_Input import Input

import Selection_rules as sl
import numpy as np
from random import randint
import time

import sys, time
from PyQt4 import QtGui

def start_simulation(N, M, goods_list, M_perishable, perish_period, production_delay, value, output, env):
	#env = create_enviroment(N, M, goods_list, M_perishable, perish_period, production_delay, value)
	simulate(100, env, sl.random_rule, output)
	print(env.agents_list[0].given_received)

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
	env.running = True
	#output.setEnviroment(env)
	output.gui.tabs.updateV()
	#for x in range(nr_iterations):
	while not env.stop:
		for agent in env.current_agents[:]:
			if env.running:
				#time.sleep(env.delay)
				current_agent = agent[0]
				good = agent[1]

				#output.getList(env.agents_list)
				# Select next agent with selection rule
				next_agent = env.select_agent(selectionrule, current_agent)

				# Do the transaction
				env.transaction(current_agent, next_agent, good)
				total_transactions += 1
				output.gui.control_panel.setNrTransactions(total_transactions)

				env.calculate_comunnityeffect(total_transactions)

				#output.showPlot()
				#output.gui.tabs.showPlot()
				#output.plotTransactionPercentages()
				output.gui.tabs.plotTransactionPercentages()

				# exit = output.print_transaction(current_agent, next_agent, good)
				output.gui.tabs.print_transaction(current_agent, next_agent, good)
				# output.gui.tabs.updateV()
				# if exit:
				# 	break
				if env.stop:
					break

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
			else:
				time.sleep(0.1)
		# Produce goods after every transaction, if it is time to produce.
		if env.running:
			env.produce_goods(selectionrule)
		# if exit:
		# 	break
		# if env.stop:
		# 	break
	print(env.agents_list[0].grid_pos)
	env.calculate_comunnityeffect(total_transactions)


