import numpy as np

maze = np.zeros([5, 6])


reward = {'dead': -100, 'end': 100, 'step': -1}
A = ['up', 'down', 'left', 'right', 'still']


def create_states():
	rows = 5
	columns = 6
	S = []
	for i in range(rows):
		for j in range(columns):
			S.append([i,j])
	return S

S = create_states()


def valid_move(s, a):
	valid = True
	if a == 'up' and s[0] == 0:
		valid = False
	elif a == 'down' and s[0] == 4:
		valid = False
	elif a == 'left' and s[1] == 0:
		valid = False
	elif a == 'right' and s[1] == 5:
		valid = False
	elif a == 'right' and s[1] == 1 and (s[0] == 0 or s[0] == 1 or s[0] == 2): # s[0] == [0,1,2]  
		valid = False
	return valid




def update_state(s, a):
	pass