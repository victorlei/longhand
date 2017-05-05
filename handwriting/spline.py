import pickle
import time
#from multiprocessing import Process
#from scipy.stats import pearsonr,linregress
from collections import deque
from scipy.interpolate import UnivariateSpline
#from scipy.interpolate import InterpolatedUnivariateSpline
#import matplotlib.pyplot as plt
#import numpy as np
#import threading
import sys
#import math
#import pygame

class spline(object):
    def __init__(self, label=""):
        self.lines = []
        self.rect = None
        self.label = label

    def fit_spline(self,sfactor=200):
        n = len(self.lines)
        if n < 4:
            return

        x,y = np.array(self.lines, dtype=np.float).T
        x0,x1,y0,y1 = x.min(),x.max(),y.min(),y.max()
        if x0 == x1 or y0==y1:
            return
        x -= x0
        y -= y0
        i = np.arange(n)
        fx = UnivariateSpline(i,x[i],s=sfactor)
        fy = UnivariateSpline(i,y[i],s=sfactor)
        
        t = np.linspace(0,n,100)
        x = fx(t)+x0
        y = fy(t)+y0
        self.lines = zip(x,y)

def get_rect(lines):
    x,y = np.array(lines, dtype=np.float).T 
    x0,x1,y0,y1 = x.min(),x.max(),y.min(),y.max()
    return pygame.Rect(x0,y0,x1-x0,y1-y0)


def main():
    tabletop = pickle.load(open(sys.argv[1]))
    for i in range(len(tabletop)):
        x,y = np.array(tabletop[i].lines,dtype=np.float).T
        plt.plot(x,-y)
    plt.show()

def main2():
    tabletop = pickle.load(open(sys.argv[1]))
    for i in range(len(tabletop)):
        xi,yi = np.array(tabletop[i].lines,dtype=np.float).T
        for j in range(i+1,len(tabletop)):
            xj,yj = np.array(tabletop[j].lines,dtype=np.float).T

            zi = np.hypot(xi,yi)
            zj = np.hypot(xj,yj)

            r,p = pearsonr(zi,zj)
            print r,p
            if p > 1e-10 or r <  0.7:
                print "DIFF"
            else:
                print "SAME"
            plt.plot(xi,-yi)
            plt.plot(xj,-yj)
            plt.show()

            #plt.plot(range(100),zi)
            #plt.plot(range(100),zj)
            #plt.show()

if __name__ == "__main__":
    main()


