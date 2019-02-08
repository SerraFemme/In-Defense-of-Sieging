import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 30
fps_clock = pygame.time.Clock()

window_width = 800
window_height = 600

DISPLAYSURF = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('In Defense of Sieging')

WHITE = (255, 255, 255)

while True:  # main game loop
    DISPLAYSURF.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()
        fps_clock.tick(FPS)
