import sys,pickle,math,time,os,re,traceback
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

     
    clock = pygame.time.Clock()
    x = y = 0 
    verbosity = False
    pygame.key.set_repeat(500,50)
    background_image = pygame.image.load("everything.png").convert()
    jpeg = 0
    done = False
    strbuffer = ""
    points =[]
    while not done:
        clock.tick(10)
        try:
            pygame.display.set_caption(strbuffer)
        except Empty:
            pass
        disp = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    try:
                        everything.pop()
                    except IndexError:
                        pass
                elif event.key == pygame.K_r:
                    disp = not disp 
                elif event.key == pygame.K_l:
                    for thing in everything:
                        print "L",thing.label
                elif event.key == pygame.K_d:
                    everything[-1].distance()
                elif event.key == pygame.K_LEFT:
                    everything.rotate(-1)
                elif event.key == pygame.K_RIGHT:
                    everything.rotate(+1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons == (1,0,0):
                    everything[-1].points.append(event.pos)
                elif event.buttons == (0,0,0):
                    x,y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                everything[-1].fit_spline()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                everything.append(spline("%s" % time.time( )))
            else:
                pass
        # End of "for event in pygame.event.get()" loop,
        # dispatched by event.type
        try:
            screen.fill(WHITE)
            screen.blit(background_image, [0, 0])

            for thing in everything:
                if len(thing.points) < 4:
                    continue
                color = RED if thing is everything[-1] else BLACK
                try:
                    if disp:
                        points = thing.points
                    else:
                        points = list(thing.lines)
                    if len(points) > 0:
                        pygame.draw.lines(screen, color, False, points, 2)
                except:
                    traceback.print_exc()
                if (0 and thing.rect and
                    thing.rect.collidepoint(x,y)):
                    pygame.draw.rect(screen,BLUE,thing.rect,1)
                    text = font.render(thing.label, True, (0, 128, 0))
                    screen.blit(text,(x,y))
                    
            if jpeg:
                try:
                    os.mkdir("/tmp/everything")
                except:
                    pass
                pygame.image.save(screen,"/tmp/everything/%s.jpeg" % time.time())
                pygame.display.set_caption("Ok writing to /tmp/everything")

        except KeyboardInterrupt:
                done = True
        pygame.display.flip()
     
    pygame.quit()
    #pickle.dump(everything,open("everything.pickle","w"))

def main():
    global everything
    everything = deque()
    try:
        dirname = sys.argv[2]
    except:
        dirname = "/tmp/longhand"
    try:
        os.mkdir(dirname)
    except:
        pass
    try:
        for filename in os.listdir(dirname):
            thing = spline(filename)
            thing.load(dirname,filename)
            everything.append(thing)
        loop()
    except:
        traceback.print_exc()
    finally:
        for thing in everything:
            thing.save(dirname,thing.label)

if __name__  == "__main__":
    main()
    
