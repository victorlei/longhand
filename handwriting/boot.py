import sys,pickle,math,time,os
from Queue import Empty,Full,PriorityQueue
from multiprocessing import Process,Queue
from scipy.interpolate import UnivariateSpline
from itertools import count
from collections import deque
import numpy as np
import cv2
import pygame
from math import pi
from spline import *
import readline

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def loop():
    pygame.init()
    size = [1024,512]
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("comicsansms", 72)

    everything = deque()
    thing = []
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500,50)
    background_image = pygame.image.load("everything.png").convert()
    done = False
    while not done:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    everything.pop()
                elif event.key == pygame.K_ESCAPE:
                    everything = [] 
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons == (1,0,0):
                    points.append(event.pos)
                elif event.buttons == (0,0,0):
                    pass #x,y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                everything.append(points)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                points = []
            else:
                pass
        # End of "for event in pygame.event.get()" loop,
        # dispatched by event.type
        try:
            screen.fill(WHITE)
            screen.blit(background_image, [0, 0])
            for points in everything:
                if len(points) > 1:
                    pygame.draw.lines(screen, BLACK, False, points, 2)
        except KeyboardInterrupt:
                done = True
        pygame.display.flip()
     
    pygame.quit()

def main():
    loop()
    
if __name__  == "__main__":
    main()
    
