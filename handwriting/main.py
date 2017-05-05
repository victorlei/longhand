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
    font = pygame.font.SysFont("comicsansms", 72)

     
    clock = pygame.time.Clock()
    ignore_mouse = True
    x = y = 0 
    try:
        everything = pickle.load(open("everything.pickle","r"))
        #pygame.display.set_caption("Ok everything.pickle")
    except:
        everything = deque()
    verbosity = False
    pygame.key.set_repeat(500,50)
    #background_image = pygame.image.load(everything.png").convert()
    jpeg = 0
    done = False
    textbuffer = deque()
    strbuffer = ""
    while not done:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    try:
                        textbuffer.pop()
                        pygame.display.set_caption("".join(textbuffer))
                    except IndexError:
                        pass
                elif event.key == pygame.K_DELETE:
                    try:
                        everything.pop()
                    except IndexError:
                        pass
                #elif event.key == pygame.K_ESCAPE:
                #    textbuffer.clear()
                #    pygame.display.set_caption("".join(textbuffer))
                elif event.key == pygame.K_LEFT:
                    textbuffer.rotate(-1)
                    pygame.display.set_caption("".join(textbuffer))
                elif event.key == pygame.K_RIGHT:
                    textbuffer.rotate(+1)
                    pygame.display.set_caption("".join(textbuffer))
                elif event.key == pygame.K_RETURN:
                    textbuffer.clear()
                    pygame.display.set_caption("".join(textbuffer))
                else:
                    textbuffer.append(event.unicode)
                    pygame.display.set_caption("".join(textbuffer))
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons == (1,0,0):
                    everything[-1].lines.append(event.pos)
                elif event.buttons == (0,0,0):
                    x,y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                everything[-1].fit_spline()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                everything.append(spline())
            else:
                pass
        # End of "for event in pygame.event.get()" loop,
        # dispatched by event.type
        try:
            screen.fill(WHITE)
            #screen.blit(background_image, [0, 0])

            for thing in everything:
                if len(thing.lines) < 4:
                    continue
                color = RED if thing is everything[-1] else BLACK
                pygame.draw.lines(screen, color, False, thing.lines, 2)
                if (thing.rect and
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
    pickle.dump(everything,open("everything.pickle","w"))


if __name__ == "__main__":
    main()
    
"""
                # NO mods -- textbuffer manipulation
                # CTRL -- thing queue manipulation
                elif pygame.key.get_mods() == pygame.KMOD_CTRL:
                    if event.key == pygame.K_c:
                        everything.clear()
                    elif event.key == pygame.K_w:
                        try:
                            pickle.dump(everything,open(sys.argv[1],"w"))
                            print "Ok"
                        except:
                            print "Failed"
                    mytext.append(event.unicode)
                elif mods & pygame.KMOD_CTRL:
                    elif event.key == pygame.K_l:
                        try:
                            everything = pickle.load(open(sys.argv[1]))
                            print "Ok"
                        except:
                            print "Failed"
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
                                #if len(everything) > 2:
                                #    s = everything.pop()
                                #    everything[-1].lines += s.lines
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
                # NO mods -- textbuffer manipulation
                if event.key == pygame.K_BACKSPACE:
                    try:
                        textbuffer.pop()
                    except IndexError:
                        # empty text buffer
                        pass
                elif event.key == pygame.K_ESCAPE:
                    textbuffer.clear()
                elif event_key == pygame.K_LEFT:
                    textbuffer.rotate(-1)
                elif event_key == pygame.K_RIGHT:
                    textbuffer.rotate(+1)
                # CTRL -- thing queue manipulation
                elif pygame.key.get_mods() == pygame.KMOD_CTRL:
                    if event.key == pygame.K_c:
                        everything.clear()
                    elif event.key == pygame.K_w:
                        try:
                            pickle.dump(everything,open(sys.argv[1],"w"))
                            print "Ok"
                        except:
                            print "Failed"
                    mytext.append(event.unicode)
                elif mods & pygame.KMOD_CTRL:
                    elif event.key == pygame.K_l:
                        try:
                            everything = pickle.load(open(sys.argv[1]))
                            print "Ok"
                        except:
                            print "Failed"
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
                                #if len(everything) > 2:
                                #    s = everything.pop()
                                #    everything[-1].lines += s.lines
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
"""
