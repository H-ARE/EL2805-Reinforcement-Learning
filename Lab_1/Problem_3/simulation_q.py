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
	def __init__(self):
		
		self.s = {'A': [0,0], 'B': [3,3]}
		self.grid = self.update_grid()
		self.policy = self.get_policy()

	def get_policy(self, filename = 'policy.pkl'):
		"""
		Loads policy from filename.
		"""
		with open(filename, 'rb') as f:
			policy = pickle.load(f)
		return policy

	def update_state(self, a='still', minotaor = False):
		"""
		Updates the state. If minotaor == False, the minotaur's position
		is updated. Otherwise, the character state is updated.
		"""
		if not minotaor:
			if self.valid_move(a):
				state = self.s['A']
			else:
				a = 'still'
		else:
			state = self.s['B']
			a = self.get_minotaor_action()
		if a == 'up':
			state[0] -= 1
		elif a == 'down':
			state[0] += 1
		elif a == 'right':
			state[1] += 1
		elif a == 'left':
			state[1] -= 1
		elif a == 'still':
			pass
		else:
			pass

	def initialize_grid(self):
		"""
		Initializes the grid for the simulation
		"""
		grid = np.zeros((4, 4), dtype = object)
		grid[:] = '-'
		grid[0,0] = 'A'
		grid[3,3] = 'B'
		return grid

	def update_grid(self):
		"""
		Updates the grid given the states.
		"""
		ia, ja = self.s['A']
		ib, jb = self.s['B']
		self.grid = np.zeros((4, 4), dtype = object)
		self.grid[:] = '-'
		self.grid[ia, ja] = 'A'
		self.grid[ib, jb] = 'B'


	def get_minotaor_action(self):
		"""
		Returns the random action of the minotaur.
		"""
		a = np.random.choice(['up', 'down', 'left', 'right'], 1, p = [0.25, 0.25, 0.25, 0.25])[0]

		if a == 'up' and self.s['B'][0] == 0: # Upper Maze Wall
			a = self.get_minotaor_action()
		if a == 'down' and self.s['B'][0] == 3: # Lower Maze Wall
			a = self.get_minotaor_action()
		if a == 'left' and self.s['B'][1] == 0: # Western Maze Wall
			a = self.get_minotaor_action()
		if a == 'right' and self.s['B'][1] == 3: # Eastern Maze Wall
			a = self.get_minotaor_action()
		return a

	def valid_move(self, a):
		if a == 'up' and self.s['A'][0] == 0: # Upper Maze Wall
			return False
		elif a == 'down' and self.s['A'][0] == 3: # Lower Maze Wall
			return False
		elif a == 'left' and self.s['A'][1] == 0: # Western Maze Wall
			return False
		elif a == 'right' and self.s['A'][1] == 3: # Eastern Maze Wall
			return False
		else:
			return True




	def get_action_from_policy(self,state):
		"""
		Returns an action given a state.
		"""
		action = self.policy[((state['A'][0], state['A'][1]), (state['B'][0], state['B'][1]))]
		return action
		

	def run_simulation(self):
		"""
		Runs the maze simulation
		"""

		for i in range(40):

			print(self.grid)
			print('\n')
			a = self.get_action_from_policy(self.s)
			self.update_state(a, minotaor = False)
			self.update_grid()
			self.update_state(minotaor = True)
			self.update_grid()
			if self.s['A'] == self.s['B']:
				print('FÖRLUST')

			
if __name__ == '__main__':
	a = Simulation()
	a.run_simulation()
