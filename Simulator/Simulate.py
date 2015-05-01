from Agent import Agent
from Goods import Goods
from Create_Enviroment import Enviroment
from GUI_Input import Input

import Selection_rules as sl
import numpy as np
from random import randint
import time

import sys, time
from PyQt4 import QtGui, QtCore

def start_simulation(N, M, goods_list, M_perishable, perish_period, production_delay, value, output, env, selectionrule):
	#env = create_enviroment(N, M, goods_list, M_perishable, perish_period, production_delay, value)
	simulate(100, env, selectionrule, output)
	print(env.agents_list[0].given_received)

def create_enviroment(N, M, goods_list, M_perishable, perish_period, production_delay, value, parallel, selectionrule):

	enviroment = Enviroment(N, M, M_perishable, perish_period, production_delay, value, parallel, selectionrule)

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
	#
	# call this function when user pressed start
	# when user presses pause, exit the while, so function ends
	# when user presses start again, call this function again
	#
	#
	#

	while not env.stop:
		if env.parallel:
			total_transactions = parallel(env, selectionrule, output, total_transactions)
		else:
			total_transactions = onebyone(env, selectionrule, output, total_transactions)
		# for agent in env.current_agents[:]:
		# 	if env.running:
		# 		#time.sleep(env.delay)
		# 		current_agent = agent[0]
		# 		good = agent[1]

		# 		#output.getList(env.agents_list)
		# 		# Select next agent with selection rule
		# 		next_agent = env.select_agent(selectionrule, current_agent)

		# 		# Do the transaction
		# 		env.transaction(current_agent, next_agent, good)
		# 		total_transactions += 1
		# 		env.nr_transactions += 1
		# 		env.nr_good_transactions[good.id] += 1
		# 		output.gui.control_panel.setNrTransactions(total_transactions)

		# 		#env.calculate_transaction_percentages(env.nr_transactions)
		# 		env.calculate_good_transaction_percentages(env.nr_transactions)

		# 		#output.showPlot()
		# 		#output.gui.tabs.showPlot()
		# 		#output.plotTransactionPercentages()
		# 		#output.gui.tabs.plotTransactionPercentages()
		# 		output.gui.tabs.plotGoodTransactionPercentages()

		# 		# exit = output.print_transaction(current_agent, next_agent, good)
		# 		#output.gui.tabs.print_transaction(current_agent, next_agent, good)
		# 		QtGui.qApp.processEvents()
		# 		# output.gui.tabs.updateV()
		# 		# if exit:
		# 		# 	break
		# 		if env.stop:
		# 			break

		# 		# Update the balance matrix
		# 		env.update_balancematrix(current_agent, next_agent)

		# 		# Set the selected agent as the current agent if the good is still alive.
		# 		if good.perish_period == 0 or good.life > 0:
		# 			env.current_agents[env.current_agents.index(agent)] = (next_agent, good)
		# 		else:
		# 			# Remove the perished product and the agent holding it from the list
		# 			env.notify_producer(good)
		# 			env.current_agents.remove(agent)
		# 			env.goods_list.remove(good)
		# 	else:
		# 		time.sleep(0.1)
		# # Produce goods after every transaction, if it is time to produce.
		# if env.running:
		# 	env.produce_goods(selectionrule)
		# env.calculate_communityeffect(env.nr_good_transactions)
		# print(env.nr_good_transactions)
		# if exit:
		# 	break
		# if env.stop:
		# 	break
	# print(env.agents_list[0].grid_pos)
	# env.calculate_transaction_percentages(total_transactions)

def onebyone(env, selectionrule, output, total_transactions):
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

			output.gui.tabs.moveV(next_agent, good)

			total_transactions += 1
			env.nr_transactions += 1
			env.nr_good_transactions[good.id] += 1
			output.gui.control_panel.setNrTransactions(total_transactions)

			output.gui.tabs.colorV(current_agent, next_agent)

			#env.calculate_transaction_percentages(env.nr_transactions)
			env.calculate_good_transaction_percentages(env.nr_transactions)

			#output.showPlot()
			#output.gui.tabs.showPlot()
			#output.plotTransactionPercentages()
			#output.gui.tabs.plotTransactionPercentages()
			output.gui.tabs.plotGoodTransactionPercentages()

			# exit = output.print_transaction(current_agent, next_agent, good)
			output.gui.tabs.print_transaction(current_agent, next_agent, good)
			QtGui.qApp.processEvents()
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
			time.sleep(1)
# Produce goods after every transaction, if it is time to produce.
	if env.running:
		env.produce_goods(selectionrule)
	sum = env.calculate_communityeffect(env.nr_good_transactions)
	output.gui.results.setPercentage(sum)
	return total_transactions

def parallel(env, selectionrule, output, total_transactions):
	transactions = []
	if env.running:
		for agent in env.current_agents[:]:
				
			current_agent = agent[0]
			good = agent[1]

			# Select next agent with selection rule
			next_agent = env.select_agent(selectionrule, current_agent)
			transactions.append((current_agent, next_agent, good))

			output.gui.tabs.moveV(next_agent, good)

			total_transactions += 1
			env.nr_transactions += 1
			env.nr_good_transactions[good.id] += 1

			output.gui.tabs.colorV(current_agent, next_agent)

				
		env.current_agents = []

		for t in transactions[:]:
			current_agent 	= t[0]
			next_agent 		= t[1]
			good 			= t[2]
			# Do the transaction
			env.transaction(current_agent, next_agent, good)


			output.gui.control_panel.setNrTransactions(total_transactions)

			env.calculate_good_transaction_percentages(env.nr_transactions)

			output.gui.tabs.plotGoodTransactionPercentages()

			output.gui.tabs.print_transaction(current_agent, next_agent, good)
			QtGui.qApp.processEvents()

			if env.stop:
				break

			# Update the balance matrix
			env.update_balancematrix(current_agent, next_agent)

			# Set the selected agent as the current agent if the good is still alive.
			if good.perish_period == 0 or good.life > 0:
				#env.current_agents[env.current_agents.index(agent)] = (next_agent, good)
				env.current_agents.append((next_agent, good))
			else:
				# Remove the perished product and the agent holding it from the list
				env.notify_producer(good)
				#env.current_agents.remove(agent)
				env.goods_list.remove(good)

		env.produce_goods(selectionrule)
		sum = env.calculate_communityeffect(env.nr_good_transactions)
	else:
		time.sleep(1)
		#QtCore.QTimer.singleShot(2000)
		#output.gui.control_panel.testSleep()
		#time.sleep(10)
		#env.running = True
		#print('paused')
	return total_transactions

