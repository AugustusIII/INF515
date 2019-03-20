# Import libraries
import random
from math import *
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

# Set color constants for display
red = [(63,0,0), (127,0,0), (191,0,0), (255,0,0)]
green = (0,200,0)
black = (0,0,0)

# Set agent parameters
num_actions = 4

Episodes = 1000

gamma = 0.9
alpha = 0.1

# Set the DQN learning agent
class SARSA:

    def __init__(self):
        self.table = self.getTable()
        self.visit_counter = self.getTable()
        self.epsilon = 0.1
        self.epsilon_min = 0.01
        self.epsilon_decr = 0.0
        self.tao = 1
        self.tao_max = 100
        self.tao_incr = 0.1
        
    def getTable(self):
        table = np.zeros((26,26,26,25,4))
        return table
    
    def getAction_eps(self, S):
        if np.random.rand() <= self.epsilon:
            return random.randrange(num_actions)
        if self.epsilon > self.epsilon_min:
        	self.epsilon -= epsilon_decr
        
        q_vals = self.table[S[0],S[1],S[2],S[3],:]
        return np.argmax(q_vals)

    def getAction_softmax(self, S):
        q_vals = self.table[S[0],S[1],S[2],S[3],:] * self.tao
        probs = np.exp(q_vals) / np.sum(np.exp(q_vals), axis=0)
        sample = np.random.choice(4, p=probs)

        if self.tao > self.tao_max:
        	self.tao += self.tao_incr
        return sample

# Set up the game
class gridGame:
    def __init__(self):

        self.targets = None
        self.pos = None
        self.counter = 0
        self.gametime = 0
        self.grid = np.zeros((5,5))

        self.reset()

    def reset(self):
        S = np.full(4, 24)
        targets = np.random.randint(5, size=(3,2))
        pos = np.random.randint(5, size=(2))

        while(not np.array_equal(np.unique(targets, axis=0).shape, targets.shape)):
            targets = np.random.randint(5, size=(3,2))

        self.targets = targets
        self.pos = pos
        self.gametime = 0
        self.counter = 0
        self.grid = np.zeros((5,5))

        for i in range(3):
            self.grid[tuple(self.targets[i])] = i+1
            S[i] = self.targets[i][0] * 5 + self.targets[i][1]

        self.grid[tuple(self.pos)] = -1
        S[3] = self.pos[0] * 5 + self.pos[1]

        return S

    def update(self, move):
        S = np.full(4, 25)
        R = -0.1
        end = False
        self.gametime += 1

        if move == 0 and self.pos[0] != 0:
            self.grid[tuple(self.pos)] = 0
            self.pos[0] -= 1
        if move == 1 and self.pos[0] != 4:
            self.grid[tuple(self.pos)] = 0
            self.pos[0] += 1
        if move == 2 and self.pos[1] != 0:
            self.grid[tuple(self.pos)] = 0
            self.pos[1] -= 1
        if move == 3 and self.pos[1] != 4:
            self.grid[tuple(self.pos)] = 0
            self.pos[1] += 1

        if np.array_equal(self.targets[self.counter], self.pos):
            R = 1.0
            self.counter += 1
        for i in range(self.counter,3):
            self.grid[tuple(self.targets[i])] = i+1
            S[i] = self.targets[i][0] * 5 + self.targets[i][1]

        self.grid[tuple(self.pos)] = -1
        S[3] = self.pos[0] * 5 + self.pos[1]

        if self.counter == 3:
            R = 3.0
            end = True
        if self.gametime >= 200:
            end = True

        if end:
            self.reset()

        return S, R, end

# Stats keeping track of agent performance
matplotlib.style.use('ggplot')
stats_scores = np.zeros(Episodes)
stats_lengths = np.zeros(Episodes)

#clock = pygame.time.Clock()

# Initialize the game and the agents
gG = gridGame()
sarsa = SARSA()

S = None
A = None
R = None
A_p = None
S_p = None
end = None

for e in range(Episodes):
    S = gG.reset()
    A = sarsa.getAction_softmax(S)
    total_score = 0

    for t in range(1,300):
        #clock.tick(8)

        S_p, R, end = gG.update(A)
        total_score += R
        entry = np.append(S,A)

        #print(gG.grid)
        #print(S)
        #print(sarsa.table[S[0],S[1],S[2],S[3],S[4],:])

        if end:
            sarsa.table[tuple(entry)] = (1-alpha)*sarsa.table[tuple(entry)] + alpha*R
            print("Game:", e, "completed in:", t, ", earning:", "%.2f"%total_score, "points.")
            stats_scores[e] = total_score
            stats_lengths[e] = t
            break

        else:
            A_p = sarsa.getAction_softmax(S_p)
            target_entry = np.append(S_p, A_p)
            sarsa.table[tuple(entry)] = (1-alpha)*sarsa.table[tuple(entry)] + alpha * (R + gamma*sarsa.table[tuple(target_entry)])
            S = S_p
            A = A_p


