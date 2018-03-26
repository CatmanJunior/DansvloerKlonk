import pygame
import os
import random

game_folder = os.path.dirname(__file__)

#colors
WHITE 	= 	(255,255,255)
BLACK 	= 	(0,0,0)

#GAME CONSTANTS
TITLE 	= 	"CATMAN GAME"
WIDTH 	= 	1536
HEIGHT 	= 	864

pygame.init()

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

pygame.key.set_repeat(True)
gameLoop = True

while gameLoop:
	
	for event in pygame.event.get():
		if (event.type==pygame.QUIT):
			gameLoop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pass
			if event.key == pygame.K_RIGHT:
				pass
			if event.key == pygame.K_SPACE:
				pass	
			if event.key == pygame.K_SLASH:
				pass


	window.fill(WHITE)


	pygame.display.flip()

	clock.tick (10)

pygame.quit()
