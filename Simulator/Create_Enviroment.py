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

# List of agents that produce specific product
producing_agents = []

# Balance matrix
#balance_matrix = np.zeros(0)

def create_agents(N):
	# Create N agents by calling the __init__() from the Agents Class
	for x in range(N):
		agent = Agent(x, N)
		agents_list.append(agent)

def create_goods(M, value, perish_factor, production_time):
	# Create M product by calling the __init_() from the Goods Class
	for x in range(M):
		good = Goods(x, value, perish_factor, production_time)
		goods_list.append(good)
	pass

def produce_goods(selectionrule, N):
	for agent in producing_agents:
		good = agent[1]
		# A transaction has taken place, lower the time until the production
		good.time_until_production -= 1

		# Check if it is time to start a new production
		if good.time_until_production == 0:
			# Create a new good
			new_good = Goods(good.id, good.value, good.perish_factor, good.production_time)
			# Select a agent to hold the product, or use the producing agent
			current_agents.append((selectionrule(N), new_good))
			# Add the new good to the list
			goods_list.append(new_good)
			# Reset the time until the next production
			good.time_until_production = good.production_time
	pass

def transaction(P, Q, good):
	# P gives good to Q
	agents_list[P].give(Q, good)
	# Q recieves good from P
	agents_list[Q].receive(P, good)

	if good.perish_factor > 0:
			good.life -= 1

def create_balancematrix(N):
	return np.zeros((N,N))

def update_balancematrix(balance_matrix, P, Q):
	# Update the balance matrix after every transaction
	balance_matrix[P][Q] -= 1.0
	balance_matrix[Q][P] += 1.0
	
	return balance_matrix

def select_agent(selectionrule, N, current_agent):
	# Call the right seletion rule to select the agent

	next_agent = selectionrule(N)
	while(current_agent == next_agent):
		next_agent = selectionrule(N)

	return next_agent

def select_start_agents(N):
	for good in goods_list:
		agent = randint(0, N-1)
		current_agents.append((agent, good))
		producing_agents.append((agent, good))
	pass

def simulate(nr_iterations, N, balance_matrix):
	for x in range(nr_iterations):
		for agent in current_agents[:]:
			current_agent = agent[0]
			good = agent[1]

			# Select next agent with selection rule
			next_agent = select_agent(sl.random_rule, N, current_agent)

			# Do the transaction
			transaction(current_agent, next_agent, good)

			# Update the balance matrix
			update_balancematrix(balance_matrix, current_agent, next_agent)

			# Set the selected agent as the current agent if the good is still alive.
			if good.perish_factor == 0 or good.life > 0:
				current_agents[current_agents.index(agent)] = (next_agent, good)
			else:
				# Remove the perished product and the agent holding it from the list
				current_agents.remove(agent)
				goods_list.remove(good)
			
			# Produce goods after every transaction, if it is time to produce.
			produce_goods(sl.random_rule, N)

		print(x)
		
	return balance_matrix


def main():
	# Variables which should be set by the user
	N = 10
	M = 2
	perish_factor = 3
	production_time = 6
	value = 1

	# Create the agents
	create_agents(N)

	# Create the products
	create_goods(M, value, perish_factor, production_time)

	# Create the balance matrix
	balance_matrix = np.zeros((N,N))
	#balance_matrix = create_balancematrix(N)
	print(balance_matrix)

	# Select random agents to start with
	select_start_agents(N)

	print(goods_list)
	# Start the simulation
	balance_matrix = simulate(100, N, balance_matrix)

	for agent in agents_list:
		print(agent.position, agent.given_received, agent.listoftransactions)
	print(balance_matrix)
	print(goods_list)

if __name__ == '__main__':
    main()
