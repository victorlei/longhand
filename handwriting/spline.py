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
        self.lines = []
        self.deriv = []
        self.rect = None
        self.label = label

    def load(self,filename):
        try:
            x0,y0,x1,y1 = np.loadtxt("graffiti/"+filename).T
            self.lines = np.array([x0,y0]).T
            self.deriv = np.array([x1,y1]).T
            print "Ok",filename
        except:
            traceback.print_exc()

    def save(self,filename):
        try:
            x0,y0 = np.array(self.lines).T
            x1,y1 = np.array(self.deriv).T
            np.savetxt("graffiti/"+filename,np.array([x0,y0,x1,y1]).T)
            print "Ok",filename
        except:
            traceback.print_exc()
        
    def distance(self):
        """Measure distance from this spline to everybody
        else.  Return K Nearest Neighbours  """
        try:
            s = []
            x1,y1 = np.array(self.deriv, dtype=np.float).T
            for k,(x0,y0) in vocab.iteritems():
                r,p = pearsonr(y0,y1)
                s.append(( p,k ))
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
        self.lines = np.array(self.lines)
        n = self.lines.shape[0]
        if n < 4:
            return

        x,y = self.lines.T
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
        self.lines = np.array([x,y]).T
        self.deriv = np.array([fx(t,1),fy(t,1)]).T

        x,y = self.lines.T 
        x0,x1,y0,y1 = x.min(),x.max(),y.min(),y.max()
        self.rect = pygame.Rect(x0,y0,x1-x0,y1-y0)


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


