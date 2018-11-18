import numpy as np
import pickle
import math
class Robber:

	def __init__(self, gamma):
		self.s = {'A': [0,0], 'B': [3,3]}
		self.S = self.get_all_states()
		self.gamma = gamma
		self.A = ['up', 'down', 'left', 'right', 'still']
		self.policy = None
		self.policy_file_path = 'policy_v.pkl'

	def get_all_states(self):
		"""
		Returns a list of all possible states.
		"""
		state_list = []
		for i in range(4):
			for j in range(4):
				for k in range(4):
					for l in range(4):
						state_list.append({'A': [k, l], 'B': [i, j]})
		return state_list

	def reward(self, s):
		"""
		Returns reward from being in state s.
		"""
		if s['A'] == [1,1]:
			return 1
		elif s['A'] == s['B']:
			return -10
		else:
			return 0

	def prob(self, s1, s2, a):
		"""
		Returns transition probability of transferring 
		from state s1 to s2 with action a.
		"""
		if self.adjacent_states(s1, s2, a) and self.fixed_cop(s1, s2):
			return 1
		
		else:
			return 0

	def adjacent_states(self, s1, s2, a):
		"""
		Returns True if s1 and s2 are adjacent
		with appropriate action a.
		"""
		s1 = s1['A']
		s2 = s2['A']

		if (abs(s1[0] - s2[0]) == 1) and (s1[1] - s2[1] == 0):
			if s1[0] - s2[0] == -1 and a == 'down':
				return True
			elif s1[0] - s2[0] == 1 and a == 'up':
				return True
		elif (abs(s1[1] - s2[1]) == 1) and (s1[0] - s2[0] == 0):
			if s1[1] - s2[1] == -1 and a == 'right':
				return True
			elif s1[1] - s2[1] == 1 and a == 'left':
				return True
		elif s1 == s2 and a == 'still':
			return True
		else:
			return False	

	def fixed_cop(self, s1, s2):
		"""
		Checks if minotaurs of two states are adjecent.
		Still is not allowed.
		"""
		s1 = s1['B']
		s2 = s2['B']
		if s1 == s2:
			return True
		else:
			return False


	def get_optimal_action_Q(self, Q, eps, s):
		"""
		Returns epsilon optimal action
		"""
		eps_action = np.random.choice([True, False],1,p=[eps, 1-eps])[0]
		possible_actions = [0, 1, 2, 3, 4]
		action = np.argmax(Q[s,:])
		if eps_action:
			possible_actions.remove(action)
			action = np.random.choice(possible_actions, 1, p = [0.25, 0.25, 0.25, 0.25])[0]
			return action
		else:
			return action

	def update_state(self, s, a):
		s = s['A']
		if a == 'up':
			s[0] -= 1
		elif a == 'down':
			s[0] += 1
		elif a == 'right':
			s[1] += 1
		elif a == 'left':
			s[1] -= 1
		elif a == 'still':
			pass

	def valid_move(self, s, a):
		pass

	def get_exp(self, s):
		"""
		Returns tuple (st, at, rt, st+1)
		"""
		a = np.random.choice(self.A, 1, p = [0.2, 0.2, 0.2, 0.2, 0.2])[0]
		r = self.reward(s)
		if self.prob()
		s_next = 


	def Q_learn(self):
		Q = np.zeros(16*16,5)
		decoder = {0:'up', 1:'right', 2:'down', 3:'left', 4:'still'}
		encoder = {'up':0, 'right':1, 'down':2, 'left':3, 'still':4}
		a = 0.01





s1={'A': [0,0], 'B': [3,4]}
s2={'A': [0,1], 'B': [3,3]}

a = Robber(0.8)
print(a.prob(s1,s2,'right'))