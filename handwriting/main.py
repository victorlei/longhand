import sys,pickle,math,time,os
from multiprocessing import Process
from scipy.interpolate import UnivariateSpline
from itertools import count
from collections import deque
import numpy as np
import cv2
import pygame
from math import pi
from spline import *

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def main():
    pygame.init()
    size = [1024,512]
    screen = pygame.display.set_mode(size)#,pygame.RESIZABLE)
     
    clock = pygame.time.Clock()
    ignore_mouse = True
    x = y = 0 
    try:
        sketchbook = pickle.load(open(".sketchpad.pickle","r"))
        #pygame.display.set_caption("Ok .sketchpad.pickle")
    except:
        sketchbook = deque()
    verbosity = False
    pygame.key.set_repeat(500,50)
    #background_image = pygame.image.load("sketchpad.png").convert()
    jpeg = 0
    done = False
    text = []
    while not done:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if mods == 0  or mods & pygame.KMOD_SHIFT:
                    text.append(event.unicode)
                elif mods & pygame.KMOD_CTRL:
                    if event.key == pygame.K_c:
                        sketchbook.clear()
                    elif event.key == pygame.K_s:
                        try:
                            pickle.dump(sketchbook,open(sys.argv[1],"w"))
                            print "Ok"
                        except:
                            print "Failed"
                    elif event.key == pygame.K_l:
                        try:
                            sketchbook = pickle.load(open(sys.argv[1]))
                            print "Ok"
                        except:
                            print "Failed"
                    elif event.key == pygame.K_BACKSPACE:
                        try:
                            sketchbook.pop()
                        except IndexError:
                            # empty workspace
                            pass
                    elif event.key == pygame.K_i:
                        try:
                            pygame.image.save(screen,sys.argv[1]+".jpeg")
                        except:
                            print "Failed"
                    elif event.key == pygame.K_j:
                        try:
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                jpeg = True
                            else:
                                jpeg = False
                                #if len(sketchbook) > 2:
                                #    s = sketchbook.pop()
                                #    sketchbook[-1].lines += s.lines
                        except:
                            print "Failed"
                    elif event.key == pygame.K_p:
                            pass
                    elif event.key == pygame.K_v:
                        verbosity = not verbosity
                    elif event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass
                    elif event.key == pygame.K_LEFT:
                        sketchbook.rotate(1)
                    elif event.key == pygame.K_RIGHT:
                        sketchbook.rotate(-1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons == (1,0,0):
                    sketchbook[-1].lines.append(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                sketchbook[-1].fit_spline()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sketchbook.append(Sketch())
            else:
                pass
        # End of "for event in pygame.event.get()" loop,
        # dispatched by event.type
        try:
            screen.fill(WHITE)
            #screen.blit(background_image, [0, 0])

            for sketch in sketchbook:
                if len(sketch.lines) < 4:
                    continue
                color = RED if sketch is sketchbook[-1] else BLACK
                pygame.draw.lines(screen, color, False, sketch.lines, 2)
                # if (sketch.rect and
                #     sketch.rect.collidepoint(pygame.mouse.get_pos())):
                #     pygame.draw.rect(screen,RED,sketch.rect,1)
            if jpeg:
                try:
                    os.mkdir("/tmp/sketchpad")
                except:
                    pass
                pygame.image.save(screen,"/tmp/sketchpad/%s.jpeg" % time.time())
                pygame.display.set_caption("Ok writing to /tmp/sketchpad")

        except KeyboardInterrupt:
                done = True
        pygame.display.flip()
     
    pygame.quit()
    pickle.dump(sketchbook,open(".sketchpad.pickle","w"))


if __name__ == "__main__":
    main()
