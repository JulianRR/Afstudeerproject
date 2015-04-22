import numpy as np
from random import randint

def random_rule(N):
	return randint(0, N-1)


def balance_rule(balance_matrix, current_agent, N):
	next_agents = []
	highest_balance = balance_matrix[current_agent].min()
	for x in range(N):
		if x != current_agent:
			if balance_matrix[current_agent][x] > highest_balance:
				next_agents = [x]
				highest_balance = balance_matrix[current_agent][x]
			elif balance_matrix[current_agent][x] == highest_balance:
				next_agents.append(x)
	if len(next_agents) > 1:
		return next_agents[randint(0, len(next_agents)-1)]
	return next_agents[0]