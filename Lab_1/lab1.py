import numpy as np

class Maze:
	def __init__(self):
		self.s = {'A': [0,0], 'B': [4,4]}
		self.S = self.get_all_states()
		self.u = np.zeros([5, 6])
		self.A = ['up', 'down', 'left', 'right', 'still']
		self.T = 15
	def reward(self, s):
		if s['A'] == [4,4]:
			return 100
		#elif s['A'] == s['B']:
		#	return -100
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
			if s1[0] - s2[0] == -1 and a == 'up':
				return True
			elif s1[0] - s2[0] == 1 and a == 'down':
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




	def no_wall(self, s1, s2):
		"""
		returns True if there is no wall obstructing the action a 
		"""
		valid = True

		s1 = s1['A']
		s2 = s2['A']
		#vertical walls
		wall_1 = [[[0,1], [0, 2]], [[1,1], [1, 2]], [[2, 1], [2,2]]]
		wall_2 = [[[1,3], [1,4]], [[2, 3], [2, 4]]]
		wall_3 = [[[4, 3], [4,4]]]

		#Horizontal walls
		wall_4 = [[[1,4], [2,4]], [[1,5], [2,5]]]
		wall_5 = [[[3,1], [4,1]], [[3,2], [4,2]], [[3,3], [4, 3]], [[3,4], [4,4]]]

		walls = wall_1+wall_2+wall_3+wall_4+wall_5
		

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
		
		if self.adjacent_states(s1, s2, a) and self.no_wall(s1, s2):
			return 1
		
		else:
			return 0

	def get_all_states(self):
		state_list = []
		for i in range(5):
			for j in range(6):
				for k in range(5):
					for l in range(6):
						state_list.append({'A': [i, j], 'B': [k, l]})
		state_list = []
		for i in range(5):
			for j in range(6):
				state_list.append({'A': [i,j]})
		return state_list

	def get_n_states(self, s):
		"""
		Returns a list of possible neighbour states to s
		"""
		neighbours = []
		s = s['A']
		if s in [[0,0], [4,0], [0,5], [4,5]]:
			if s == [0,0]:
				neighbours = [{'A': state} for state in [[0,1], [1,0]]]
			elif s == [4,0]:
				neighbours = [{'A': state} for state in [[4,1], [3,0]]]
			elif s == [0, 5]:
				neighbours = [{'A': state} for state in [[1,5], [0,4]]]
			elif s == [4, 5]:
				neighbours = [{'A': state} for state in [[3,5], [1,0]]]
		
		elif s[0] == 0:
			neighbours = [{'A': state} for state in [[s[0]+1,s[1]], [s[0],s[1]+1], [s[0], s[1]-1]]]
		elif s[0] == 4:
			neighbours = [{'A': state} for state in [[s[0]-1,s[1]], [s[0],s[1]+1], [s[0], s[1]-1]]]
		elif s[1] == 0:
			neighbours = [{'A': state} for state in [[s[0]+1,s[1]], [s[0]-1,s[1]], [s[0], s[1]+1]]]
		elif s[1] == 5:
			neighbours = [{'A': state} for state in [[s[0]+1,s[1]], [s[0]-1,s[1]], [s[0], s[1]-1]]]
		else:
			neighbours = [{'A': state} for state in [[s[0]+1,s[1]], [s[0]-1,s[1]], [s[0],s[1]+1], [s[0], s[1]-1]]]
		

		for state in neighbours:
			if not self.no_wall(state, {'A': s}):
				neighbours.remove(state)




		return neighbours


	def bellman(self):
		U = np.zeros((15, 5*6))

		for ind, j in enumerate(self.S):
			U[self.T-1, ind] = self.reward(j)

		for t in range(self.T-2, -1, -1):
			for ind, j in enumerate(self.S):
				pu = []

				for a in self.A:
					pi = 0
					for ind2, j2 in enumerate(self.S):
						pi += self.p(j, j2, a)*U[t+1, ind2]
					pu.append(pi)
				U[t, ind] = self.reward(j) + max(pu)
		
		self.u = U






s1 = {'A': [3,0], 'B': [4,4]}
s2 = {'A': [3,3], 'B': [4,4]}

s3 = {'A': [1,1], 'B': [4,4]}

s4 = {'A': [0,0], 'B': [4,4]}
s5 = {'A': [4,4], 'B': [4,4]}

a = Maze()
a.T = 15

a.bellman()

print(np.reshape(a.u[0], (5,6)))


print('hej')
