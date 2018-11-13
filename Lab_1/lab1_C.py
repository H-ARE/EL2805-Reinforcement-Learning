import numpy as np
from random import randint

class Maze:

    def __init__ (self, S, reward, A):
        self.S = S
        self.r = reward
        self.A = A
        self.s = [0,0]
        self.a = self.A[randint(0,3)]

    def valid_move(self):
        valid = True
        if self.a == 'up' and self.s[0] == 0: # Upper Maze Wall
            valid = False
        elif self.a == 'down' and self.s[0] == 4: # Lower Maze Wall
            valid = False
        elif self.a == 'left' and self.s[1] == 0: # Western Maze Wall
            valid = False
        elif self.a == 'right' and self.s[1] == 5: # Eastern Maze Wall
            valid = False
    #Vertical Wall @ (0,1)   
        elif self.a == 'right' and self.s[1] == 1 and self.s[0] in [0,1,2]:   
            valid = False
        elif self.a == 'left' and self.s[1] == 2 and self.s[0] in [0,1,2]:
            valid = False
    # Horizontal Wall @ (3,1)    
        elif self.a == 'down' and self.s[0] == 3 and self.s[1] in [1,2,3,4]:
            valid = False
        elif self.a == 'up' and self.s[0] == 4 and self.s[1] in [1,2,3,4]:
            valid = False
    # Horizontal Wall @ (1,4)       
        elif self.a == 'down' and self.s[0] == 1 and self.s[0] in [4,5]:
            valid = False
        elif self.a == 'up' and self.s[0] == 2 and self.s[0] in [4,5]:
            valid = False   
    # Vertical Wall @(1,3) 
        elif self.a == 'right' and self.s[1] == 3 and self.s[0] in [1,2]:	
            valid = False
        elif self.a == 'left' and self.s[1] == 4 and self.s[0] in [1,2]:
            valid = False
    # Vertical Wall @(3,4)        
        elif self.a == 'right' and self.s[1] == 3 and self.s[0] == 4:
            valid = False
        elif self.a == 'left' and self.s[1] == 4 and self.s[0] == 4:
            valid = False
        return valid

    def update_state(self):
        if Maze.valid_move(self):
            if self.a == 'up':
                self.s[0] -= 1
            elif self.a == 'down':
                self.s[0] += 1
            elif self.a == 'right':
                self.s[1] += 1
            elif self.a == 'left':
                self.s[1] -= 1
            elif self.a == 'still':
                pass
            else:
                pass
    def bellman(self):
        u = 0
        #if self.T > 1:
          #Nogonting rekursivt.  

def create_states():
	rows = 5
	columns = 6
	S = []
	for i in range(rows):
		for j in range(columns):
			S.append([i,j])
	return S

S = create_states()
reward = {'dead': -100, 'end': 100, 'step': -1}
A = ['up', 'down', 'left', 'right', 'still']

s = Maze(S,reward,A)
