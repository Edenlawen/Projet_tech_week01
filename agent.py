import torch
from uuid import uuid4


class basicAgent:
	def __init__(self, pos):
		self.pos=torch.tensor(pos)

	def move(self):
		return 0 if self.pos[0]<9 else 1


class randomAgent:
	def __init__(self, pos):
		self.pos=torch.tensor(pos)
		
	def move(self):
		return int(torch.randint(low=0, high=4, size=(1,)))


class RLAgent:
	def __init__(self, pos, size, alpha, gamma, epsilon):
		self.pos=torch.tensor(pos)
		self.origin=self.pos
		self.q_table = torch.rand(4, size, size)/100
		self.gamma=gamma
		self.alpha=alpha
		self.epsilon=epsilon

	def move(self):
		if torch.rand(1)<self.epsilon:
			return int(torch.randint(low=0,high=4, size=(1,)))
		return int(torch.argmax(self.q_table[:,self.pos[0], self.pos[1]]))
        	
	def update(self, action, reward, new_pos):
		self.q_table[action, self.pos[0], self.pos[1]]= \
		(1-self.alpha)*self.q_table[action,self.pos[0],self.pos[1]] + \
		self.alpha*(reward+self.gamma*torch.max(self.q_table[:,new_pos[0],new_pos[1]]))

	def save_q_table(self):
		torch.save(self.q_table, str(uuid4())+"_q_table.pt")
	
	def load_q_table(self):
		self.q_table = torch.load("q_table.pt")

class LRLAgent:
	def __init__(self, pos, size, alpha, gamma, epsilon):
		self.pos=torch.tensor(pos)
		self.size=size
		self.weights = torch.rand(4, size*size)/100
		self.bias = torch.rand(4)/100
		self.gamma=gamma
		self.alpha=alpha
		self.epsilon=epsilon
	
	def move(self):
		if torch.rand(1)<self.epsilon:
			return int(torch.randint(low=0,high=4, size=(1,)))
		return int(torch.argmax(self.weights[:,self.pos[0]*self.size+self.pos[1]]+self.bias))
	
	def update(self, action, reward, new_pos):
		return None


def setup(typeAgent, pos, size, alpha, gamma, epsilon):
	if typeAgent=='basic':
		return basicAgent(pos)
	elif typeAgent=='random':
		return randomAgent(pos)
	elif typeAgent=='rl':
		return RLAgent(pos, size, alpha,gamma,epsilon)
	else:
		raise Exception("Invalid agent choice")
