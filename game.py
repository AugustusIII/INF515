import pygame
import sys
from math import *
import numpy as np

red = [(63,0,0), (127,0,0), (191,0,0), (255,0,0)]
green = (0,200,0)
black = (0,0,0)

class gridGame(object):

	def __init__(self, targets, pos):

		self.targets = targets
		self.counter = 0
		self.pos = pos
		self.end = False

		self.grid = np.zeros((8,8))

		for i in range(4):
			self.grid[tuple(self.targets[i])] = i+1

		self.grid[tuple(self.pos)] = 5

	def update(self, move):

		R = -0.1

		if move == "left" and self.pos[0] != 0:
			self.grid[tuple(self.pos)] = 0
			self.pos[0] -= 1
		if move == "right" and self.pos[0] != 7:
			self.grid[tuple(self.pos)] = 0
			self.pos[0] += 1
		if move == "up" and self.pos[1] != 0:
			self.grid[tuple(self.pos)] = 0
			self.pos[1] -= 1
		if move == "down" and self.pos[1] != 7:
			self.grid[tuple(self.pos)] = 0
			self.pos[1] += 1

		if np.array_equal(self.targets[self.counter], self.pos):
			R = 1.0
			self.counter += 1

		for i in range(self.counter,4):
			self.grid[tuple(self.targets[i])] = i+1

		self.grid[tuple(self.pos)] = 5

		if self.counter == 4:
			R = 3.0
			self.end = True

		I = self.genImage()

		return I, R

	def genImage(self):
		I = np.zeros((3,40,40))

		for i in range(8):
			for j in range(8):
				if self.grid[i,j] == 1:
					I[0,i*5:(i+1)*5,j*5:(j+1)*5] = 63 / 255
				if self.grid[i,j] == 2:
					I[0,i*5:(i+1)*5,j*5:(j+1)*5] = 127 / 255
				if self.grid[i,j] == 3:
					I[0,i*5:(i+1)*5,j*5:(j+1)*5] = 191 / 255
				if self.grid[i,j] == 4:
					I[0,i*5:(i+1)*5,j*5:(j+1)*5] = 255 / 255
				if self.grid[i,j] == 5:
					I[1,i*5:(i+1)*5,j*5:(j+1)*5] = 255 / 255

		return I


targets = np.random.randint(8, size=(4,2))
pos = np.random.randint(8, size=2)

while(np.unique(targets, axis=0).shape[0] < targets.shape[0]):
	targets = np.random.randint(8, size=(4,2))

gG = gridGame(targets, pos)

#initialize display
pygame.init()
screen = pygame.display.set_mode((40,40))

R = 0
I = gG.genImage()

while True:

	# Various drawing utilities to observe gameplay
	#screen.fill(black)
	#if gG.counter < 1:
	#	pygame.draw.rect(screen, red[0], (5*gG.targets[0,0],5*gG.targets[0,1],5,5), 0)
	#if gG.counter < 2:
	#	pygame.draw.rect(screen, red[1], (5*gG.targets[1,0],5*gG.targets[1,1],5,5), 0)
	#if gG.counter < 3:
	#	pygame.draw.rect(screen, red[2], (5*gG.targets[2,0],5*gG.targets[2,1],5,5), 0)
	#if gG.counter < 4:
	#	pygame.draw.rect(screen, red[3], (5*gG.targets[3,0],5*gG.targets[3,1],5,5), 0)
	#pygame.draw.rect(screen, green, (5*gG.pos[0],5*gG.pos[1],5,5), 0)

	#for i in range(40):
	#	for j in range(40):
	#		pygame.draw.rect(screen, (int(255*I[0,i,j]),0,0), (i,j,1,1), 0)

	# Interaction and Updating
	#Press left or right, Press ESC to quit
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

			if event.key == pygame.K_LEFT:
				I, R = gG.update("left")
			if event.key == pygame.K_RIGHT:
				I, R = gG.update("right")
			if event.key == pygame.K_UP:
				I, R = gG.update("up")
			if event.key == pygame.K_DOWN:
				I, R = gG.update("down")

			#print(gG.grid)
			print(R)

	pygame.display.update()
	if gG.end:
		pygame.quit()
		sys.exit()













