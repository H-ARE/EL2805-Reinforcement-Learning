import numpy as np
import pickle
class Bellman:
	def __init__(self):
		self.s = {'A': [0,0], 'B': [4,4]}
		self.S = self.get_all_states()
		#self.u = self.load_u('b.pkl')
		self.A = ['up', 'down', 'left', 'right', 'still']
		self.T = 15
		self.policy = None
		self.policy_file_path = 'policy.pkl'
	
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
		elif s['A'] == s['B']:
			return -100
		#elif ((abs(s['A'][0] - s['B'][0]) == 1) and (s['A'][1] - s['B'][1] == 0)) or ((abs(s['A'][1] - s['B'][1]) == 1) and (s['A'][0] - s['B'][0] == 0)):
		#	return -5
		else:
			return -1

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

	def adjacent_minotaurs(self, s1, s2):
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
		"""
		if (abs(s1[0] - s2[0]) == 1) and (s1[1] - s2[1] == 0):
			return True
		elif (abs(s1[1] - s2[1]) == 1) and (s1[0] - s2[0] == 0):
			return True
		else:
			return False
		"""

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
			return 1
		
		else:
			return 0

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
		U = np.zeros((15, 900))
		
		for ind, j in enumerate(self.S):
			U[self.T-1, ind] = self.reward(j)
		
		for t in range(self.T-2, -1, -1):
			print(t)
			for ind, j in enumerate(self.S):
				pu = []
				for a in self.A:
					pi = 0
					for ind2, j2 in enumerate(self.S):
						pi += self.p(j, j2, a)*U[t+1, ind2]
					pu.append(pi)
				U[t, ind] = self.reward(j) + max(pu)
		
		self.u = U
		self.get_policy()
		

	def get_policy(self):
		"""
		Retrieves the optimal policy from utility.
		"""
		policy = {}
		for ind, j in enumerate(self.S):
			pu = []
			for a in self.A:
				pi = 0
				for ind2, j2 in enumerate(self.S):
					pi += self.p(j, j2, a)*self.u[1, ind2]
				pu.append(pi)
				if pi == max(pu):
					a_star = a
			policy[((j['A'][0], j['A'][1]), (j['B'][0], j['B'][1]))] = a_star
		self.policy = policy
		self.save_policy(self.policy_file_path)


if __name__ == '__main__':
	b = Bellman()
	b.full_bellman()








