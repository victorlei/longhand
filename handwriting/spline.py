import pickle
import time,traceback
#from multiprocessing import Process
from scipy.stats import pearsonr,linregress
from collections import deque
from scipy.interpolate import UnivariateSpline
#from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
import numpy as np
#import threading
import sys,os
#import math
from itertools import count
import pygame

class spline(object):
    def __init__(self, label=""):
        self.points = [] # list of pairs
        self.lines = []
        self.deriv = []
        self.rect  = None
        self.label = label

    def load(self,dirname,filename):
        try:
            path ="%s/%s" % (dirname,filename)
            x0,y0,x1,y1 = np.loadtxt(path).T
            self.lines = np.array([x0,y0]).T
            self.deriv = np.array([x1,y1]).T
        except:
            traceback.print_exc()

    def save(self,dirname,filename):
        try:
            x0,y0 = np.array(self.lines).T
            x1,y1 = np.array(self.deriv).T
            path = "%s/%s" % (dirname,filename)
            np.savetxt(np.array([x0,y0,x1,y1]).T,
                      filename)
        except:
            traceback.print_exc()
        
    def distance(self):
        """Measure distance from this spline to everybody
        else.  Return K Nearest Neighbours  """
        try:
            import pdb
            pdb.set_trace()
            s = []
            x0,y0 = self.deriv.T
            for thing in everything:
                x1,y1 = thing.deriv.T
                r,p = pearsonr(y0,y1)
                s.append(( p,thing.label ))
            s.sort()
            #print s[-5:]
            print s
        except:
            return np.inf

    def dist_old(self,other):
        if self is other:
            return 0
        try:
            x0,y0 = np.array(other.deriv, dtype=np.float).T
            x1,y1 = np.array(self.deriv, dtype=np.float).T
#            plt.plot(y0)
#            plt.plot(y1)
#            plt.show()
            r,p = pearsonr(y0,y1)
            return p
        except:
            return np.inf

    def fit_spline(self,sfactor=200):
        n = len(self.points)
        if n < 4:
            return

        x,y = np.array(self.points).T
        x_min,x_max,y_min,y_max = (x.min(),x.max(),
                                   y.min(),y.max())
        if x_min == x_max or y_min == y_max:
            return

        x -= x_min
        y -= y_min
        i = np.arange(n)
        fx = UnivariateSpline(i,x[i],s=sfactor)
        fy = UnivariateSpline(i,y[i],s=sfactor)
       
        t = np.linspace(0,n,100)
        x = fx(t)+x_min
        y = fy(t)+y_min
        self.lines = np.array([x,y]).T
        self.deriv = np.array([fx(t,1),fy(t,1)]).T

        x,y = self.lines.T 
        x_min,x_max,y_min,y_max = (x.min(),x.max(),
                                   y.min(),y.max())
        self.rect = pygame.Rect(x_min,
                                y_min,
                                x_max-x_min,
                                y_max-y_min)


def main():
    everything = pickle.load(open(sys.argv[1]))
    print len(everything)
    for i in range(len(everything)):
        x,y = np.array(everything[i].lines,dtype=np.float).T
        plt.plot(x)
        plt.plot(y)
        plt.plot(x,-y)
    plt.show()

def main():
    everything = pickle.load(open(sys.argv[1]))
    for i in range(len(everything)):
        xi,yi = np.array(everything[i].lines,dtype=np.float).T
        for j in range(i+1,len(everything)):
            xj,yj = np.array(everything[j].lines,dtype=np.float).T

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


