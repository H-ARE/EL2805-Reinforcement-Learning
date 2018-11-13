import numpy as np
from random import randint

class Maze:

    def __init__ (self, reward, A):
        self.S = self.get_states()
        self.r = reward
        self.A = A
        self.s = [0,0]
        self.sb = [4,4]

    def valid_move(self, a):
        valid = True
        if a == 'up' and self.s[0] == 0: # Upper Maze Wall
            valid = False
        elif a == 'down' and self.s[0] == 4: # Lower Maze Wall
            valid = False
        elif a == 'left' and self.s[1] == 0: # Western Maze Wall
            valid = False
        elif a == 'right' and self.s[1] == 5: # Eastern Maze Wall
            valid = False
    #Vertical Wall @ (0,1)   
        elif a == 'right' and self.s[1] == 1 and self.s[0] in [0,1,2]:   
            valid = False
        elif a == 'left' and self.s[1] == 2 and self.s[0] in [0,1,2]:
            valid = False
    # Horizontal Wall @ (3,1)    
        elif a == 'down' and self.s[0] == 3 and self.s[1] in [1,2,3,4]:
            valid = False
        elif a == 'up' and self.s[0] == 4 and self.s[1] in [1,2,3,4]:
            valid = False
    # Horizontal Wall @ (1,4)       
        elif a == 'down' and self.s[0] == 1 and self.s[0] in [4,5]:
            valid = False
        elif a == 'up' and self.s[0] == 2 and self.s[0] in [4,5]:
            valid = False   
    # Vertical Wall @(1,3) 
        elif a == 'right' and self.s[1] == 3 and self.s[0] in [1,2]:	
            valid = False
        elif a == 'left' and self.s[1] == 4 and self.s[0] in [1,2]:
            valid = False
    # Vertical Wall @(3,4)        
        elif a == 'right' and self.s[1] == 3 and self.s[0] == 4:
            valid = False
        elif a == 'left' and self.s[1] == 4 and self.s[0] == 4:
            valid = False
        return valid


    def get_minotaor_action(self):
        a = np.random.choice(['up', 'down', 'left', 'right'], 1, p = [0.25, 0.25, 0.25, 0.25])[0]

        if a == 'up' and self.sb[0] == 0: # Upper Maze Wall
            a = self.get_minotaor_action()
        if a == 'down' and self.sb[0] == 4: # Lower Maze Wall
            a = self.get_minotaor_action()
        if a == 'left' and self.sb[1] == 0: # Western Maze Wall
            a = self.get_minotaor_action()
        if a == 'right' and self.sb[1] == 5: # Eastern Maze Wall
            a = self.get_minotaor_action()
        return a


    def update_state(self, a, minotaor = False):
        if not minotaor:
            if self.valid_move(a):
                state = self.s
            else:
                a = 'still'
        else:
            state = self.sb
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
    def bellman(self):
        u = 0
        #if self.T > 1:
          #Nogonting rekursivt.
    def get_states(self):
        rows = 5
        columns = 6
        S = []
        for i in range(rows):
            for j in range(columns):
                S.append([i,j])
        self.S = S
    def get_actions(self):
        pass





reward = {'dead': -100, 'end': 100, 'step': -1}
A = ['up', 'down', 'left', 'right', 'still']

s = Maze(reward,A)
