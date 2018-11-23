import numpy as np
import pickle
import math
import copy
class Robber:

	def __init__(self, gamma):
		self.s = {'A': [0,0], 'B': [3,3]}
		self.S = self.get_all_states()
		self.gamma = gamma
		self.A = ['up', 'down', 'left', 'right', 'still']
		self.policy = None
		self.policy_file_path = 'policy_v.pkl'
		self.get_enc()
		self.Q = self.load_q()

	def get_enc(self):
		encoder_s = {}
		decoder_s = {}
		for i, s in enumerate(self.S):
			encoder_s[((s['A'][0], s['A'][1]),(s['B'][0], s['B'][1]))] = i
			decoder_s[i] = s
		decoder_a = {0:'up', 1:'right', 2:'down', 3:'left', 4:'still'}
		encoder_a = {'up':0, 'right':1, 'down':2, 'left':3, 'still':4}
		return encoder_s, decoder_s, encoder_a, decoder_a


	def load_q(self, filename = 'q.pkl'):
		with open(filename, 'rb') as f:
			q = pickle.load(f)

		return q

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
		if (s['A'] == [1,1]) and (s['A'] != s['B']):
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
		if  self.adjacent_states(s1, s2, a) and self.fixed_cop(s1, s2):
			n = self.n_minotaur_neighbours(s1)
			return 1/(n)
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


		if (abs(s1[0] - s2[0]) == 1) and (s1[1] - s2[1] == 0):
			return True
		elif (abs(s1[1] - s2[1]) == 1) and (s1[0] - s2[0] == 0):
			return True
		else:
			return False

	def n_minotaur_neighbours(self, s):
		s = s['B']
		if (s[0] == 0 and s[1] == 0) or (s[0] == 3 and s[1] == 0) or (s[0] == 0 and s[1] == 3) or (s[0] == 3 and s[1] == 3):
			return 2
		elif (s[0] == 0) or (s[0] == 3) or (s[1] == 0) or (s[1] == 3):
			return 3
		else:
			return 4
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

	def update_state(self, a, minotaor = False):
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

	def get_exp(self):
		"""
		Returns (st, at, rt, st+1)
		"""
		s = copy.deepcopy(self.s)
		a = np.random.choice(self.A, 1, p = [0.2, 0.2, 0.2, 0.2, 0.2])[0]
		r = self.reward(self.s)
		self.update_state(a, minotaor = False)
		self.update_state(a, minotaor = True)
		s_next = copy.deepcopy(self.s)
		return {'s':s, 'a':a, 'r':r, 's_next':s_next}

	def get_policy_from_q(self, Q):
		policy = {}
		encoder_s, decoder_s, encoder_a, decoder_a = self.get_enc()
		for ind, s in enumerate(self.S):
			a_star = np.argmax(Q[ind,:])
			a_star = decoder_a[a_star]
			print(s, a_star)
			policy[((s['A'][0], s['A'][1]), (s['B'][0], s['B'][1]))] = a_star
			print(ind)
		with open('policy2.pkl', 'wb') as f:
			pickle.dump(policy, f)
		return policy

	def Q_learn(self):
		"""
		Todo: decoder and encoder for state
		"""
		Q = np.zeros([16*16,5])
		counter = np.zeros([16*16, 5])
		encoder_s, decoder_s, encoder_a, decoder_a = self.get_enc()
		g = self.gamma
		down = []
		still = []
		for i in range(10000000):
			exp = self.get_exp()
			key = ((exp['s']['A'][0], exp['s']['A'][1]), (exp['s']['B'][0], exp['s']['B'][1]))
			key_next = ((exp['s_next']['A'][0], exp['s_next']['A'][1]), (exp['s_next']['B'][0], exp['s_next']['B'][1]))
			i_s = encoder_s[key]
			i_s_next = encoder_s[key_next]
			i_a = encoder_a[exp['a']]
			counter[i_s, i_a] += 1
			a = 1/(counter[i_s, i_a]**(2/3))
			Q[i_s, i_a] += a*(exp['r'] + g*max(Q[i_s_next,:]) - Q[i_s, i_a])
			if exp['s'] == {'A':[0,0], 'B':[3,3]} and exp['a'] == 'down':
				down.append(Q[240,2])
			if exp['s'] == {'A':[0,0], 'B':[3,3]} and exp['a'] == 'still':
				still.append(Q[240,4])
			if i % 100000 == 0:
				print(i)
		self.Q = Q
		with open('q.pkl', 'wb') as f:
			pickle.dump(Q, f)
		policy = self.get_policy_from_q(Q)
		with open('still.pkl', 'wb') as f:
			pickle.dump(still, f)
		with open('down.pkl', 'wb') as f:
			pickle.dump(down, f)





if __name__ == '__main__':
	a = Robber(0.8)
	a.Q_learn()

