from numpy import *
import random

class Agent:
	def __init__(self, id, N):
		self.id = id
		self.N = N
		# List of transactions, for example: [(Action, Agent, Good)] 
		# Where Action is either given or received, Agent is the agent 
		# on the other side of the transaction and Good is de good that
		# has been transfered.
		self.listoftransactions = []
		# The number of goods given and goods received for each agent
		# are stored in the variable below. For example: array([(given, received)])
		# where given is the total number of goods given to the agent 
		# with the position equal to the index and received the total number
		# of goods received from the agent.
		self.given_received = array([(0.0, 0.0) for x in range(N)])
		self.nr_transactions = 0
		# [[good, number_transactionss]]
		self.goods_transactions = []

		# Yield curve variables
		self.like_factor = [-0.5 for i in range(N)]
		# The value of the next transaction, different for every agent pair and every good
		self.yield_values = []
		# The balance between this agent and all the other agents, different for every good.
		self.balance = []
		# Nominal values
		self.nominal_values = []
		

		self.grid_pos = [0, 0, 0]
	
	def update_listoftransactions(self, P, Q, good):
		self.listoftransactions.append((P, Q, good))

	def give(self, receiving_agent, good):
		#The current agent gives to the receiving_agent.
		self.given_received[receiving_agent.id][0] += 1
		#self.listoftransactions.append(("Given", receiving_agent, good))
		self.nr_transactions += 1
		self.goods_transactions[good.id][1] += 1

		# Yield calculations
		# self.balance[good.id][receiving_agent.id] += self.yield_values[good.id][receiving_agent.id]
		self.balance[receiving_agent.id] += self.yield_values[good.id][receiving_agent.id]
		# receiving_agent.balance[good.id][self.id] -= self.yield_values[good.id][receiving_agent.id]
		receiving_agent.balance[self.id] -= self.yield_values[good.id][receiving_agent.id]
		# print(str(self.id) + '-->' + str(receiving_agent.id))
		#print(self.balance[receiving_agent.id])
		#print(receiving_agent.balance[self.id])
		# self.yield_values[good.id][receiving_agent.id] = self.like_factor[receiving_agent.id] * self.balance[good.id][receiving_agent.id] + self.nominal_values[good.id]
		# self.yield_values[good.id][receiving_agent.id] = self.like_factor[receiving_agent.id] * (self.balance[receiving_agent.id] + self.nominal_values[good.id]) + self.nominal_values[good.id]
		#self.yield_values[good.id][receiving_agent.id] = self.like_factor[receiving_agent.id] * self.balance[receiving_agent.id] + self.nominal_values[good.id]

		#print('given yield:', self.yield_values[good.id][receiving_agent.id])

	
	def receive(self, giving_agent, good):
		#The current agent receives from the giving_agent
		self.given_received[giving_agent.id][1] += 1
		#self.listoftransactions.append(("Received", giving_agent, good))
		self.nr_transactions += 1
		self.goods_transactions[good.id][1] += 1

		# Yield calculations
		#self.balance[good.id][giving_agent.id] -= self.yield_values[good.id][giving_agent.id]
		#self.yield_values[good.id][giving_agent.id] = self.like_factor[giving_agent.id] * self.balance[good.id][giving_agent.id] + self.nominal_values[good.id]
		#self.yield_values[good.id][giving_agent.id] = self.like_factor[giving_agent.id] * self.balance[giving_agent.id] + self.nominal_values[good.id]
		#self.yield_values[good.id][giving_agent.id] = self.like_factor[giving_agent.id] * (self.balance[giving_agent.id] + self.nominal_values[good.id]) + self.nominal_values[good.id]

		#print('receive yield:', self.yield_values[good.id][giving_agent.id])

	def give_parallel(self, receiving_agent, good):
		self.given_received[receiving_agent.id][0] += 1
		self.nr_transactions += 1
		self.goods_transactions[good.id][1] += 1

		self.balance[receiving_agent.id] += self.yield_values[good.id][receiving_agent.id]

		receiving_agent.balance[self.id] -= self.yield_values[good.id][receiving_agent.id]

	def receive_parallel(self, giving_agent, good):
		self.given_received[giving_agent.id][1] += 1
		self.nr_transactions += 1
		self.goods_transactions[good.id][1] += 1
