from bellman import Bellman
import pickle
import numpy as np
"""
Simulation of the maze.

Initial state:
[['A' '-' '-' '-' '-' '-']
 ['-' '-' '-' '-' '-' '-']
 ['-' '-' '-' '-' '-' '-']
 ['-' '-' '-' '-' '-' '-']
 ['-' '-' '-' '-' 'B' '-']]

 Goal state:
 [['-' '-' '-' '-' '-' '-']
 ['-' '-' '-' '-' '-' '-']
 ['-' 'B' '-' '-' '-' '-']
 ['-' '-' '-' '-' '-' '-']
 ['-' '-' '-' '-' 'A' '-']]

 Get 'A' to element (4,4) of the matrix without touching 'B'
 which moves randomly.
 """

class Simulation:
	def __init__(self, T = 15, still_minotaur = False):
		self.grid = self.initialize_grid()
		self.T = T
		self.s = {'A': [0,0], 'B': [4,4]}
		self.policy = self.get_policy()
		self.still_minotaur = still_minotaur


	def get_policy(self, filename = 'policy_still_v.pkl'):
		"""
		Loads policy from filename.
		"""
		with open(filename, 'rb') as f:
			policy = pickle.load(f)
		return policy

	def update_state(self, a):
		"""
		Updates the state. If minotaor == False, the minotaur's position
		is updated. Otherwise, the character state is updated.
		"""
		if self.valid_move(a):
			s1 = self.s['A']
			if a == 'up':
				s1[0] -= 1
			elif a == 'down':
				s1[0] += 1
			elif a == 'right':
				s1[1] += 1
			elif a == 'left':
				s1[1] -= 1
			else:
				pass
		else:
			pass
		s2 = self.s['B']
		a = self.get_minotaor_action()
		if a == 'up':
			s2[0] -= 1
		elif a == 'down':
			s2[0] += 1
		elif a == 'right':
			s2[1] += 1
		elif a == 'left':
			s2[1] -= 1
		else:
			pass
		return(a)

	def initialize_grid(self):
		"""
		Initializes the grid for the simulation
		"""
		grid = np.zeros((5, 6), dtype = object)
		grid[:] = '-'
		grid[0,0] = 'A'
		grid[4,4] = 'B'
		return grid

	def update_grid(self):
		"""
		Updates the grid given the states.
		"""
		ia, ja = self.s['A']
		ib, jb = self.s['B']
		self.grid = np.zeros((5, 6), dtype = object)
		self.grid[:] = '-'
		self.grid[ia, ja] = 'A'
		self.grid[ib, jb] = 'B'


	def get_minotaor_action(self):
		"""
		Returns the random action of the minotaur.
		"""
		if self.still_minotaur:
			a = np.random.choice(['up', 'down', 'left', 'right', 'still'], 1, p = [0.2, 0.2, 0.2, 0.2, 0.2])[0]
		else:
			a = np.random.choice(['up', 'down', 'left', 'right'], 1, p = [0.25, 0.25, 0.25, 0.25])[0]

		if a == 'up' and self.s['B'][0] == 0: # Upper Maze Wall
			a = self.get_minotaor_action()
		if a == 'down' and self.s['B'][0] == 4: # Lower Maze Wall
			a = self.get_minotaor_action()
		if a == 'left' and self.s['B'][1] == 0: # Western Maze Wall
			a = self.get_minotaor_action()
		if a == 'right' and self.s['B'][1] == 5: # Eastern Maze Wall
			a = self.get_minotaor_action()
		return a

	def valid_move(self, a):
		"""
		Returns True if an action a is valid given a state s.
		"""
		valid = True
		if a == 'up' and self.s['A'][0] == 0: # Upper Maze Wall
			valid = False
		elif a == 'down' and self.s['A'][0] == 4: # Lower Maze Wall
			valid = False
		elif a == 'left' and self.s['A'][1] == 0: # Western Maze Wall
			valid = False
		elif a == 'right' and self.s['A'][1] == 5: # Eastern Maze Wall
			valid = False
		#Vertical Wall @ (0,1)   
		elif a == 'right' and self.s['A'][1] == 1 and self.s['A'][0] in [0,1,2]:   
			valid = False
		elif a == 'left' and self.s['A'][1] == 2 and self.s['A'][0] in [0,1,2]:
			valid = False
		# Horizontal Wall @ (3,1)    
		elif a == 'down' and self.s['A'][0] == 3 and self.s['A'][1] in [1,2,3,4]:
			valid = False
		elif a == 'up' and self.s['A'][0] == 4 and self.s['A'][1] in [1,2,3,4]:
			valid = False
		# Horizontal Wall @ (1,4)       
		elif a == 'down' and self.s['A'][0] == 1 and self.s['A'][1] in [4,5]:
			valid = False
		elif a == 'up' and self.s['A'][0] == 2 and self.s['A'][1] in [4,5]:
			valid = False   
		# Vertical Wall @(1,3) 
		elif a == 'right' and self.s['A'][1] == 3 and self.s['A'][0] in [1,2]:	
			valid = False
		elif a == 'left' and self.s['A'][1] == 4 and self.s['A'][0] in [1,2]:
			valid = False
		# Vertical Wall @(3,4)        
		elif a == 'right' and self.s['A'][1] == 3 and self.s['A'][0] == 4:
			valid = False
		elif a == 'left' and self.s['A'][1] == 4 and self.s['A'][0] == 4:
			valid = False
		return valid




	def get_action_from_policy(self,state,t):
		"""
		Returns an action given a state.
		"""
		if type(self.policy) == list:
			action = self.policy[t][((state['A'][0], state['A'][1]), (state['B'][0], state['B'][1]))]
		else:
			action = self.policy[((state['A'][0], state['A'][1]), (state['B'][0], state['B'][1]))]
		return action
		

	def evaluate_policy(self, N = 10000, t1 = 10, t2 = 15):
		P = []
		for time in range(t1,t2):
			print(time)
			p = 0
			for i in range(N):
				pi = self.run_simulation(time)
				p+=pi
				#if pi == 0:
					#print('hej')
			p = p/N
			P.append(p)
		print(P)

	def evaluate_policy_geometric(self, N = 100000):
		p = 0
		for i in range(N):
			T = np.random.geometric(1/29)
			pi = self.run_simulation(T)
			p+=pi
		p = p/N
		print(p)





	def run_simulation(self, SIM_TIME):
		"""
		Runs the maze simulation
		"""
		A = []
		self.s = {'A': [0,0], 'B': [4,4]}
		for i in range(SIM_TIME):

			#print(self.grid)
			#print('\n')
			if self.s['A'] == [4,4]:
				#print('You won in', i, 'steps!')
				#print(A)
				return 1
			elif self.s['A'] == self.s['B']:
				#print('You lost after', i, 'steps') 
				#print(A)
				return 0
				
			action = self.get_action_from_policy(self.s, i+15-SIM_TIME-1)
			
			ra = self.update_state(action)
			A.append(ra)
			self.update_grid()
		#print(self.grid)
		if self.s['A'] != [4,4]:
			#print('You did not make it to the end.')
			#print(A)
			return 0
		else:
			#print('You won in', i+1, 'steps')
			#print(A)
			#print('bla')
			return 1


#d = Simulation()

#s = {'A':[3,2], 'B':[4,5]}
#print(d.get_action_from_policy(s))

if __name__ == '__main__':
	a = Simulation()
	#a.run_simulation(12)
	a.evaluate_policy_geometric()
