import Agent
import Goods
# A different file should contain all the functions for the selectio rules.
# Each selection rule will have one function, this function is called before
# every transaction.
#import Selectionrules

agents_list = []
goods_list = []

def create_agents(N):
	# Create N agents by calling the __init__() from the Agents Class
	for x in xrange(0,N):
		agent = Agent(x, N)
		agents_list.append(agent)
	pass

def create_goods(M):
	# Create M product by calling the __init_() from the Goods Class
	pass

def transaction(P, Q):
	# Start a transaction between P and Q by calling give() and receive() 
	# from the Agents Class 
	# P give to Q
	#P.give(Q)
	# Q reveives from P
	#Q.receive(P)
	pass

def update_balancematrix(balancematrix):
	# Update the balance matrix after every transaction
	pass

def select_agent(selectionrule):
	# Call the right seletion rule to select the agent
	pass

def main():
	N = 30
	M = 5
	create_agents(N)
	print(agents_list)
	#create_agents(N)
	#create_goods(M)
	# Start the game 
	#P = current_agent #Choose a random agent
	#While(Start):
	#	Q = select_agent(selectionrule)
	#	transaction(P, Q, good)
	#	P = Q

if __name__ == '__main__':
    main()
