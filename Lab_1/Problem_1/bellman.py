import numpy as np
import pickle
import math
class Bellman:
	def __init__(self, T = 15, still_minotaur = False):
		self.s = {'A': [0,0], 'B': [4,4]}
		self.S = self.get_all_states()
		self.A = ['up', 'down', 'left', 'right', 'still']
		self.T = T
		self.policy = {}
		self.policy_file_path = 'policy_v.pkl'
		self.still_minotaur = still_minotaur
	
	def save_policy(self, filename):
		"""
		Saves policy.
		"""
		with open(filename, 'wb') as f:
			pickle.dump(self.policy, f)

	def load_u(self, filename):
		"""
		Loads utility.
		"""
		with open(filename, 'rb') as f:
			u = pickle.load(f)
		return u

	def reward(self, s):
		"""
		Returns reward from being in state s.
		"""
		if s['A'] == [4,4]:
			return 100
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
			if (s1[0] - s2[0]) == -1 and (a == 'down'):
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

	def adjacent_minotaurs(self, s1, s2):
		"""
		Checks if minotaurs of two states are adjecent.
		Still is not allowed.
		"""
		s1 = s1['B']
		s2 = s2['B']
		
		if (abs(s1[0] - s2[0]) == 1) and (s1[1] - s2[1] == 0):
			return True
		elif (abs(s1[1] - s2[1]) == 1) and (s1[0] - s2[0] == 0):
			return True
		elif s1 == s2:
			if self.still_minotaur:
				return True
			else:
				return False
		else:
			return False
			


	def valid_move(self, s, a):
		"""
		Returns True if an action a is valid given a state s.
		"""
		valid = True
		if a == 'up' and s['A'][0] == 0: # Upper Maze Wall
			valid = False
		elif a == 'down' and s['A'][0] == 4: # Lower Maze Wall
			valid = False
		elif a == 'left' and s['A'][1] == 0: # Western Maze Wall
			valid = False
		elif a == 'right' and s['A'][1] == 5: # Eastern Maze Wall
			valid = False
		#Vertical Wall @ (0,1)   
		elif a == 'right' and s['A'][1] == 1 and s['A'][0] in [0,1,2]:   
			valid = False
		elif a == 'left' and s['A'][1] == 2 and s['A'][0] in [0,1,2]:
			valid = False
		# Horizontal Wall @ (3,1)    
		elif a == 'down' and s['A'][0] == 3 and s['A'][1] in [1,2,3,4]:
			valid = False
		elif a == 'up' and s['A'][0] == 4 and s['A'][1] in [1,2,3,4]:
			valid = False
		# Horizontal Wall @ (1,4)       
		elif a == 'down' and s['A'][0] == 1 and s['A'][1] in [4,5]:
			valid = False
		elif a == 'up' and s['A'][0] == 2 and s['A'][1] in [4,5]:
			valid = False   
		# Vertical Wall @(1,3) 
		elif a == 'right' and s['A'][1] == 3 and s['A'][0] in [1,2]:	
			valid = False
		elif a == 'left' and s['A'][1] == 4 and s['A'][0] in [1,2]:
			valid = False
		# Vertical Wall @(3,4)        
		elif a == 'right' and s['A'][1] == 3 and s['A'][0] == 4:
			valid = False
		elif a == 'left' and s['A'][1] == 4 and s['A'][0] == 4:
			valid = False

		return valid


	def no_wall(self, s1, s2):
		"""
		Returns True if there is no wall obstructing the action a
		from transferring state s1 to s2. 
		"""
		valid = True
		s1 = s1['A']
		s2 = s2['A']
		wall_1 = [[[0,1], [0, 2]], [[1,1], [1, 2]], [[2, 1], [2,2]]]
		wall_2 = [[[1,3], [1,4]], [[2, 3], [2, 4]]]
		wall_3 = [[[4, 3], [4,4]]]
		wall_4 = [[[1,4], [2,4]], [[1,5], [2,5]]]
		wall_5 = [[[3,1], [4,1]], [[3,2], [4,2]], [[3,3], [4, 3]], [[3,4], [4,4]]]
		walls = wall_1 + wall_2 + wall_3 + wall_4 + wall_5
		
		if [s1, s2] in walls:
			return False
		
		elif [s2, s1] in walls:
			return False
		
		else:
			return True

	def p(self, s1, s2, a):
		"""
		Returns transition probability of transferring 
		from state s1 to s2 with action a.
		"""
		if s1['A'] == [4,4]:
			return 0
		
		elif s1['A'] == s1['B']:
			return 0
		
		if self.adjacent_states(s1, s2, a) and self.adjacent_minotaurs(s1, s2) and self.no_wall(s1, s2):
			n = self.n_minotaur_neighbours(s1)
			if self.still_minotaur:
				n += 1
			return 1/(n)
		else:
			return 0

	def n_minotaur_neighbours(self, s):
		"""
		Returns the amount of neighbouring states of the minotaur.
		"""
		s = s['B']
		if (s[0] == 0 and s[1] == 0) or (s[0] == 4 and s[1] == 0)\
		 or (s[0] == 0 and s[1] == 5) or (s[0] == 4 and s[1] == 5):
			return 2
		elif (s[0] == 0) or (s[0] == 4) or (s[1] == 0) or (s[1] == 5):
			return 3
		else:
			return 4


	def get_all_states(self):
		"""
		Returns a list of all possible states.
		"""
		state_list = []
		for i in range(5):
			for j in range(6):
				for k in range(5):
					for l in range(6):
						state_list.append({'A': [k, l], 'B': [i, j]})
		return state_list


	def full_bellman(self):
		"""
		Saves the optimal policy of the Bellman
		dynamic programming algorithm
		"""
		U = np.zeros((self.T, 900))
		
		for ind, j in enumerate(self.S):
			U[self.T-1, ind] = self.reward(j)

		for t in range(self.T-2, -1, -1):
			print(t)
			for ind, j in enumerate(self.S):
				pu = []
				A = self.get_legal_actions(j)
				for a in A:
					pi = 0
					for ind2, j2 in enumerate(self.S):
						pi += self.p(j, j2, a)*U[t+1, ind2]
					pu.append(pi)
				U[t, ind] = self.reward(j) + max(pu)
			self.get_policy(U,t)
			print(np.reshape(U[t,28*30:29*30], (5,6)).astype(int))
		self.u = U
	
	def get_legal_actions(self, s):
		legal_actions = []
		for a in self.A:
			if self.valid_move(s, a):
				legal_actions.append(a)
		return legal_actions


	def get_policy(self,U, t):
		"""
		Retrieves the optimal policy from utility.
		"""
		policy = {}
		for ind, j in enumerate(self.S):
			pu = []
			for a in self.A:
				pi = 0
				for ind2, j2 in enumerate(self.S):
					pi += self.p(j, j2, a)*U[t+1, ind2]
				pu.append(pi)
				if pi == max(pu):
					a_star = a

			policy[((j['A'][0], j['A'][1]), (j['B'][0], j['B'][1]))] = a_star
		self.policy[t] = policy
		self.save_policy(self.policy_file_path)

	def value_iteration(self, gamma = 29/30, epsilon = 0.01, delta = 300):
		"""
		Value iteration algorithm
		"""
		V = np.zeros(900)
		V_old = np.array(V)

		crit = epsilon*(1-gamma)/gamma
		while(delta > crit):
			for ind, s in enumerate(self.S):
				pu = []
				for a in self.A:
					pi = 0
					for ind2, j in enumerate(self.S):
						pi += gamma*self.p(s, j, a)*V[ind2]
					pu.append(pi)
				V[ind] = self.reward(s) + max(pu)
			delta = np.linalg.norm(V-V_old, ord = math.inf)
			V_old = np.array(V)
			print(np.reshape(V[0:30], [5,6]).astype(int))
			print(delta, crit)

		policy = {}
		for ind, s in enumerate(self.S):
			pu = []
			for a in self.A:
				pi = 0
				for ind2, j2 in enumerate(self.S):
					pi += self.reward(s) + self.p(s, j2, a)*V[ind2]
				pu.append(pi)
				if pi == max(pu):
					a_star = a
			policy[((s['A'][0], s['A'][1]), (s['B'][0], s['B'][1]))] = a_star
		self.policy = policy
		self.save_policy(self.policy_file_path)

if __name__ == '__main__':
	b = Bellman()
	b.value_iteration()








