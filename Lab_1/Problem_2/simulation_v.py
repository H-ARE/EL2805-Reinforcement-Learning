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
    def __init__(self, still_minotaur = False):
        self.grid = self.initialize_grid()
        self.s = {'A': [0,0], 'B': [1,2]}
        self.policy = self.get_policy()
        self.still_minotaur = still_minotaur


    def get_policy(self, filename = 'policy_v.pkl'):
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
        grid = np.zeros((3, 6), dtype = object)
        grid[:] = '-'
        grid[0,0] = 'A'
        grid[1,2] = 'B'
        return grid

    def update_grid(self):
        """
        Updates the grid given the states.
        """
        ia, ja = self.s['A']
        ib, jb = self.s['B']
        self.grid = np.zeros((3, 6), dtype = object)
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

        if (a == 'up' and self.s['B'][0] == 0)\
        or (a == 'up' and self.s['B'][0] < self.s['A'][0])\
        or (a == 'up' and self.s['B'][0] == 2 and self.s['A'] == 2): # Upper Maze Wall
            a = self.get_minotaor_action()
        
        if (a == 'down' and self.s['B'][0] == 2)\
        or (a == 'down' and self.s['B'][0] > self.s['A'][0])\
        or (a == 'down' and self.s['B'][0] == 0 and self.s['A'] == 0): # Lower Maze Wall
            a = self.get_minotaor_action()
        
        if (a == 'left' and self.s['B'][1] == 0)\
        or (a == 'left' and self.s['B'][1] < self.s['A'][1])\
        or (a == 'left' and self.s['B'][0] == 5 and self.s['A'] == 5): # Western Maze Wall
            a = self.get_minotaor_action()
        
        if (a == 'right' and self.s['B'][1] == 5)\
        or (a == 'right' and self.s['B'][1] > self.s['A'][1])\
        or (a == 'right' and self.s['B'][0] == 0 and self.s['A'] == 0): # Eastern Maze Wall
            a = self.get_minotaor_action()
        return a

    def valid_move(self, a):
        """
        Returns True if an action a is valid given a state s.
        """
        valid = True
        if a == 'up' and self.s['A'][0] == 0: # Upper Maze Wall
            valid = False
        elif a == 'down' and self.s['A'][0] == 2: # Lower Maze Wall
            valid = False
        elif a == 'left' and self.s['A'][1] == 0: # Western Maze Wall
            valid = False
        elif a == 'right' and self.s['A'][1] == 5: # Eastern Maze Wall
            valid = False
        return valid




    def get_action_from_policy(self,state):
        """
        Returns an action given a state.
        """
        action = self.policy[((state['A'][0], state['A'][1]), (state['B'][0], state['B'][1]))]
        return action
        

    def run_simulation(self, SIM_TIME):
        """
        Runs the maze simulation
        """
        self.s = {'A': [0,0], 'B': [1,2]}
        for i in range(SIM_TIME):
            print(self.grid)
            print('\n')
            action = self.get_action_from_policy(self.s)
            self.update_state(action)
            self.update_grid()
            

if __name__ == '__main__':
    a = Simulation()
    a.run_simulation(20)
