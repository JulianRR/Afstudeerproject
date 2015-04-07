from Agent import Agent
from Goods import Goods
import Selection_rules as sl
import numpy as np
from random import randint
# A different file should contain all the functions for the selectio rules.
# Each selection rule will have one function, this function is called before
# every transaction.
#import Selectionrules

# Agents and Goods
agents_list = []
goods_list = []

# Current agents with a good [(agent, good)]
current_agents = []

# Balance matrix
balance_matrix = np.zeros(0)


def create_agents(N):
	# Create N agents by calling the __init__() from the Agents Class
	for x in range(N):
		agent = Agent(x, N)
		agents_list.append(agent)

def create_goods(M, value, perish_factor):
	# Create M product by calling the __init_() from the Goods Class
	for x in range(M):
		good = Goods(x, value, perish_factor)
		goods_list.append(good)
	pass

def transaction(P, Q):
	# Start a transaction between P and Q by calling give() and receive() 
	# from the Agents Class 
	# P give to Q
	#P.give(Q)
	# Q reveives from P
	#Q.receive(P)
	pass

def create_balancematrix(N):
	return np.zeros((N,N))

def update_balancematrix(balance_matrix):
	# Update the balance matrix after every transaction
	pass

def select_agent(selectionrule):
	# Call the right seletion rule to select the agent
	pass

def select_start_agents(N):
	for good in goods_list:
		agent = randint(0, N-1)
		current_agents.append((agent, good.id))

def simulate(nr_iterations, N, balancematrix):
	for x in range(nr_iterations):
		for agent in current_agents:
			current_agent = agent[0]
			good = agent[1]

			# Select next agent with selection rule
			next_agent = sl.random_rule(N)
			while(current_agent == next_agent):
				next_agent = sl.random_rule(N)

			# Do the transaction
			agents_list[current_agent].give(next_agent, goods_list[good])
			agents_list[next_agent].receive(current_agent, goods_list[good])

			# Update the balance matrix
			balancematrix[current_agent][next_agent] -= 1.0
			balancematrix[next_agent][current_agent] += 1.0

			# Set the selected agent as the current agent.
			current_agents[current_agents.index(agent)] = (next_agent, good)
	return balancematrix

	pass


def main():
	# Variables which should be set by the user
	N = 10
	M = 2
	perish_factor = 0
	value = 1

	# Create the agents
	create_agents(N)
	for agent in agents_list:
		#agent.given_received[1][0] += 1
		print(agent.position, agent.given_received[1])

	# Create the products
	create_goods(M, value, perish_factor)
	for good in goods_list:
		print(good.id, good.value)

	# Create the balance matrix
	balance_matrix = np.zeros((N,N))
	#balance_matrix = create_balancematrix(N)
	print(balance_matrix)

	# Select random agents to start with
	select_start_agents(N)

	# Start the simulation
	balance_matrix = simulate(10, N, balance_matrix)

	for agent in agents_list:
		#agent.given_received[1][0] += 1
		print(agent.position, agent.given_received, agent.listoftransactions)
	print(balance_matrix)

if __name__ == '__main__':
    main()
