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
	# This doesnt seem to work, because multiple agents will have the same product
	# for agent in producing_agents:
	# 	good = agent[1]
	# 	# After every transaction the time until the production needs to be decreased by 1
	# 	goods_list[good].time_until_production -= 1
	# 	# if not alive, if it is time to produce and if good is perishable (last one is not needed if producing agents only consist of perishable goods)
	# 	if goods_list[good].life == 0 and goods_list[good].time_until_production == 0 and goods_list[good].perish_factor > 0:
	# 		# Reset the life and the time until the next production
	# 		goods_list[good].life = goods_list[good].perish_factor
	# 		goods_list[good].time_until_production = goods_list[good].production_time

	# 		# Add the agent who produced the product to the list with agents holding a good.
	# 		current_agents.append(agent)
	for good in goods_list:
		good.time_until_production -= 1
		if good.life == 0 and good.time_until_production == 0 and good.perish_factor > 0:
			# Reset the life and the time until the next production
			new_good = Goods(good.id, good.value, good.perish_factor, good.production_time)
			current_agents.append((selectionrule(N), new_good))
			goods_list.pop(goods_list.index(good))
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
		for agent in current_agents:
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
				current_agents.pop(current_agents.index(agent))
				#goods_list.pop(good)

			# Produce goods after every transaction, if it is time to produce.
			produce_goods(sl.random_rule, N)

	return balance_matrix


def main():
	# Variables which should be set by the user
	N = 10
	M = 2
	perish_factor = 3
	production_time = 2
	value = 1

	# Create the agents
	create_agents(N)
	for agent in agents_list:
		print(agent.position, agent.given_received[1])

	# Create the products
	create_goods(M, value, perish_factor, production_time)
	for good in goods_list:
		print(good.id, good.value)

	# Create the balance matrix
	balance_matrix = np.zeros((N,N))
	#balance_matrix = create_balancematrix(N)
	print(balance_matrix)

	# Select random agents to start with
	select_start_agents(N)
	#producing_agents = current_agents

	# Start the simulation
	balance_matrix = simulate(100, N, balance_matrix)

	for agent in agents_list:
		print(agent.position, agent.given_received, agent.listoftransactions)
	print(balance_matrix)
	print(producing_agents)

if __name__ == '__main__':
    main()
