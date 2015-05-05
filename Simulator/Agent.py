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

		self.like_factor = [random.uniform(-1.0, 0.0) for i in range(N)]

		self.grid_pos = [0, 0, 0]
	
	def update_listoftransactions(self, P, Q, good):
		self.listoftransactions.append((P, Q, good))

	def give(self, receiving_agent, good):
		#The current agent gives to the receiving_agent.
		self.given_received[receiving_agent.id][0] += 1
		self.listoftransactions.append(("Given", receiving_agent, good))
		self.nr_transactions += 1
		self.goods_transactions[good.id][1] += 1

		pass
	
	def receive(self, giving_agent, good):
		#The current agent receives from the giving_agent
		self.given_received[giving_agent.id][1] += 1
		self.listoftransactions.append(("Received", giving_agent, good))
		self.nr_transactions += 1
		self.goods_transactions[good.id][1] += 1
		pass
	
	def update_given_received(self, position, previous_transaction):
		# if previous_transaction == given:
		# 	self.given_received[position][0] += previous_transaction
		# elif previous_transaction == received:
		# 	self.given_received[position][1] += previous_transaction
		pass
