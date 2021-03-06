import numpy as np
import random

def random_rule(N):
	random.seed()
	return random.randint(0, N-1)


def balance_rule(balance_matrix, current_agent, N):
	next_agents = []
	highest_balance = balance_matrix[current_agent].min()
	random.seed()
	for x in range(N):
		if x != current_agent:
			if balance_matrix[current_agent][x] > highest_balance:
				next_agents = [x]
				highest_balance = balance_matrix[current_agent][x]
			elif balance_matrix[current_agent][x] == highest_balance:
				next_agents.append(x)
	if len(next_agents) > 1:
		return next_agents[random.randint(0, len(next_agents)-1)]
	return next_agents[0]

def goodwill_rule(current_agent, good, N):
	highest_yield = min(current_agent.yield_values[good.id])
	#print('yield:', current_agent.yield_values[good.id])
	#print('higest:', highest_yield)
	next_agents = []
	random.seed()
	for x in range(N):
		if x != current_agent.id:
			if current_agent.yield_values[good.id][x] > highest_yield:
				next_agents = [x]
				highest_yield = current_agent.yield_values[good.id][x]
			elif current_agent.yield_values[good.id][x] == highest_yield:
				next_agents.append(x)
	#print('next:', next_agents)
	if len(next_agents) > 1:
		return next_agents[random.randint(0, len(next_agents)-1)]
	# print(next_agents)
	return next_agents[0]