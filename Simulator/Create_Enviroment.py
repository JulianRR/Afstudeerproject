from Agent import Agent
from Goods import Goods
import Selection_rules as sl
import numpy as np
from random import randint
import Selection_rules as sl
# A different file should contain all the functions for the selectio rules.
# Each selection rule will have one function, this function is called before
# every transaction.
#import Selectionrules

class Enviroment:
	def __init__(self, N, M, M_perishable, perish_period, production_delay, value, parallel, selectionrule, like_factors, balance, nominal_values):

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
		self.goods_parameters = []
		# Agents and Goods
		self.agents_list = []
		self.goods_list = []

		# Current agents with a good [(agent, good)]
		self.current_agents = []

		# List of agents that produce specific product
		self.producing_agents = []

		# Balance matrix balance rule
		self.balance_matrix = np.zeros((N,N))

		# Selection rule
		self.selection_rule = selectionrule

		# Excel input
		self.balance = balance
		self.like_factors = like_factors
		self.nominal_values = nominal_values

		# Transaction percentage list
		# [[percentage], [percentage]]
		self.transaction_percentages = []
		#[[good1 percentage, good2 percentage], [good1 percentage, good2 percentage]]
		self.goods_transaction_percentages = []
		self.nr_transactions = 0
		self.nr_good_transactions = [0 for i in range(M)]

		self.total_transactions = 0

		# Comunnity percentage
		self.subgroup_size = 2
		self.index = 0
		self.comunnity_percentage = 0

		# Control variables
		self.output = None
		self.stop = False
		self.running = False
		self.delay = 0
		self.parallel = parallel

	def create_agents(self):
		# Create N agents by calling the __init__() from the Agents Class
		for x in range(self.N):
			agent = Agent(x, self.N)
			self.agents_list.append(agent)

	def create_goods(self, goods):
		# Create M product by calling the __init_() from the Goods Class
		if goods:
			#print(goods)
			self.goods_parameters = goods
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

		# Notify the agents of the starting goods. This is needed for the calculations of the 
		# comunnity effect.
		self.notify_agents()

	def notify_agents(self):
		for agent in self.agents_list:
			for good in self.goods_list:
				agent.goods_transactions.append([good, 0])
				#agent.yield_values.append([good.value for x in range(self.N)])
			if self.balance:
				# agent.balance.append(self.balance[agent.id])
				agent.balance = self.balance[agent.id]
			else:
				# agent.balance.append([0.0 for x in range(self.N)])
				agent.balance = [0.0 for x in range(self.N)]
			#print('yield values:', agent.yield_values)
			#print('balance:', agent.balance)
			if self.like_factors:
				agent.like_factor = self.like_factors[agent.id]
			
			if self.nominal_values:
				agent.nominal_values = self.nominal_values[agent.id]
			# else:
			# 	agent.nominal_values = []
		self.setYieldValues()

	def setLikeFactors(self):
		pass

	def setBalance(self):
		pass

	def setYieldValues(self):
		for agent in self.agents_list:
			for good in self.goods_list:
				# agent.yield_values.append([agent.like_factor[x] * agent.balance[good.id][x] + agent.nominal_values[good.id] for x in range(self.N)])
				print(agent.like_factor[0])
				print(agent.balance[0])
				print(agent.nominal_values[good.id])
				agent.yield_values.append([agent.like_factor[x] * agent.balance[x] + agent.nominal_values[good.id] for x in range(self.N)])


	def update_balancematrix(self, P, Q):
		# Update the balance matrix after every transaction
		self.balance_matrix[P.id][Q.id] = P.given_received[Q.id][1] - P.given_received[Q.id][0]
		self.balance_matrix[Q.id][P.id] = Q.given_received[P.id][1] - Q.given_received[P.id][0]

	def notify_producer(self, good):
		for producer in self.producing_agents:
			g = producer[1]
			if g.id == good.id:
				g.life = good.life

	def produce_goods(self, selectionrule, output):
		for producer in self.producing_agents:
			agent = producer[0]
			good = producer[1]

			# Check if it is time to start a new production if the good has perished
			if good.time_until_production == 0 and good.life == 0:
				# Create a new good
				#new_good = Goods(good.id, good.value, good.perish_period, good.production_delay)
				#new_good.grid_pos = self.agents_list[agent].grid_pos
				# Select a agent to hold the product, or use the producing agent
				self.goods_list[good.id].life = good.perish_period
				self.current_agents.append((agent, self.goods_list[good.id]))
				# Add the new good to the list
				#self.goods_list.append(new_good)
				
				# Reset the time until the next production
				good.time_until_production = good.production_delay
				good.life = good.perish_period
				# output.gui.tabs.print_production(good)
				output.gui.results.print_production(good)
				output.gui.tabs.colorV()
				output.gui.tabs.moveV(agent, self.goods_list[good.id])
				#print(agent.grid_pos)
				
				

			# Reduce the time untill the production if only the good has perished
			elif good.life == 0:
				good.time_until_production -= 1
				#output.gui.tabs.print_time_until_production(good)
				output.gui.results.print_time_until_production(good)
				#output.gui.tabs.colorV()

			

	def transaction(self, P, Q, good):
		# P gives good to Q
		self.agents_list[P.id].give(Q, good)
		# Q recieves good from P
		self.agents_list[Q.id].receive(P, good)

		if good.perish_period > 0:
				good.life -= 1

	def select_agent(self, selectionrule, current_agent, good):
		# Call the right seletion rule to select the agent

		next_agent_id = current_agent.id
		while(current_agent.id == next_agent_id):
			if selectionrule == 0:
				next_agent_id = sl.random_rule(self.N)
			elif selectionrule == 1:
				next_agent_id = sl.balance_rule(self.balance_matrix, current_agent.id, self.N)
			elif selectionrule == 2:
				next_agent_id = sl.goodwill_rule(current_agent, good, self.N)
		return self.agents_list[next_agent_id]

	def select_start_agents(self):
		for good in self.goods_list:
			index = randint(0, self.N-1)
			self.current_agents.append((self.agents_list[index], good))
			if good.perish_period > 0:
				self.producing_agents.append((self.agents_list[index], good))

	def calculate_transaction_percentages(self, total_transactions):
		self.transaction_percentages = []
		for agent in self.agents_list[:]:
			# received = 0
			# for x in agent.given_received:
			# 	received += x[1]
			# self.transaction_percentages.append(received / total_transactions)
			#total_transactions * 2 because given and received are both used. Producer gives so that
			#needs to be taken into account, and perished good cannot be given, but are received.
			self.transaction_percentages.append(agent.nr_transactions / (total_transactions*2))

	def calculate_good_transaction_percentages(self, total_transactions):
		self.goods_transaction_percentages = []
		for agent in self.agents_list:
			percentages = []
			for goods in agent.goods_transactions:
				if total_transactions != 0:
					percentages.append(goods[1] / (total_transactions*2))
				else:
					percentages.append(0)
			self.goods_transaction_percentages.append(percentages)

	def calculate_communityeffect(self, goods_transactions):
		threshold = 0.8
		community_effect = []
		for agent in self.agents_list:
			percentages = []
			count = 0
			for goods in agent.goods_transactions:
				if goods_transactions[count] != 0:
					percentages.append(goods[1] / (goods_transactions[count]*2))
					print('goods_transactions:' + str(count), goods_transactions[count]*2)
					print('goods[1]:', goods[1])
				else:
					percentages.append(0)
				count += 1
			community_effect.append(percentages)

		#print('not sorted:', community_effect)

		np_community_effect = np.array(community_effect)
		np_community_effect = np.sort(np_community_effect.T)

		#print('sorted:', np_community_effect)
		sum = 0
		for x in range(self.subgroup_size):
			sum += np_community_effect[self.index][::-1][x]

			#print(x[::-1])
			#print(sum)
		return sum



			
