from Agent import Agent
from Goods import Goods
import Selection_rules as sl
import numpy as np
from random import randint
# A different file should contain all the functions for the selectio rules.
# Each selection rule will have one function, this function is called before
# every transaction.
#import Selectionrules

class Enviroment:
	def __init__(self, N, M, M_perishable, perish_period, production_delay, value):

		# Total agents
		self.N = N
		# Total goods
		self.M = M
		# Number of goods that are perishable
		self.M_perishable = M_perishable
		self.perish_period = perish_period
		# stable at prodcution_time = M * perish_period
		self.production_delay = production_delay
		self.value = value

		# Agents and Goods
		self.agents_list = []
		self.goods_list = []

		# Current agents with a good [(agent, good)]
		self.current_agents = []

		# List of agents that produce specific product
		self.producing_agents = []

		# Balance matrix
		self.balance_matrix = np.zeros((N,N))

		# Transaction percentage list
		self.transaction_percentages = []

		# Comunnity percentage
		self.comunnity_percentage = 0

		# Control variables
		self.stop = False
		self.running = False
		self.delay = 0

	def create_agents(self):
		# Create N agents by calling the __init__() from the Agents Class
		for x in range(self.N):
			agent = Agent(x, self.N)
			self.agents_list.append(agent)

	def create_goods(self, goods):
		# Create M product by calling the __init_() from the Goods Class
		if goods:
			for x in range(self.M):
				perish_period 	 = goods[x][0]
				production_delay = goods[x][1]
				nominal_value 	 = goods[x][2]

				good = Goods(x, nominal_value, perish_period, production_delay)
				self.goods_list.append(good)
		else:
			for x in range(self.M-self.M_perishable):
				good = Goods(x, self.value, 0, 0)
				self.goods_list.append(good)

			for y in range(self.M-self.M_perishable, self.M):
				good = Goods(y, self.value, self.perish_period, self.production_delay)
				self.goods_list.append(good)
		

	def update_balancematrix(self, P, Q):
		# Update the balance matrix after every transaction
		self.balance_matrix[P][Q] -= 1.0
		self.balance_matrix[Q][P] += 1.0

	def notify_producer(self, good):
		for producer in self.producing_agents:
			g = producer[1]
			if g.id == good.id:
				g.life = good.life

	def produce_goods(self, selectionrule):
		for producer in self.producing_agents:
			agent = producer[0]
			good = producer[1]
			# A transaction has taken place, lower the time until the production
			#good.time_until_production -= 1
			# if g.id == good.id:
			# 	good.life = g.life

			# Check if it is time to start a new production if the good has perished
			if good.time_until_production == 0 and good.life == 0:
				# Create a new good
				new_good = Goods(good.id, good.value, good.perish_period, good.production_delay)
				# Select a agent to hold the product, or use the producing agent
				self.current_agents.append((agent, new_good))
				# Add the new good to the list
				self.goods_list.append(new_good)
				# Reset the time until the next production
				good.time_until_production = good.production_delay
				good.life = good.perish_period

			# Reduce the time untill the production if only the good has perished
			elif good.life == 0:
				good.time_until_production -= 1

			

	def transaction(self, P, Q, good):
		# P gives good to Q
		self.agents_list[P].give(Q, good)
		# Q recieves good from P
		self.agents_list[Q].receive(P, good)

		if good.perish_period > 0:
				good.life -= 1

	def select_agent(self, selectionrule, current_agent):
		# Call the right seletion rule to select the agent

		next_agent = selectionrule(self.N)
		while(current_agent == next_agent):
			next_agent = selectionrule(self.N)

		return next_agent

	def select_start_agents(self):
		for good in self.goods_list:
			agent = randint(0, self.N-1)
			self.current_agents.append((agent, good))
			if good.perish_period > 0:
				self.producing_agents.append((agent, good))

	def calculate_comunnityeffect(self, total_transactions):
		self.transaction_percentages = []
		for agent in self.agents_list[:]:
			received = 0
			for x in agent.given_received:
				received += x[1]
			self.transaction_percentages.append(received / total_transactions)
