import control
from control import NonlinearIOSystem
from control import optimal
from matplotlib import pyplot
import numpy
from optimalcontrol import solve
from classify import classify_trajectory

def trajectories(params,initial,toll={'cured':0.1,'state':0.1,'cycle':0.1}):
    sol=map(lambda x:solve(params|{'S0':x[0],'R0':x[1]}),initial)
    return list(map(lambda x:classify_trajectory(x[1], params['threshold'], toll['cured'], toll['state'], toll['cycle']),sol))

def manytrajectories(params,initial,toll={'cured':0.1,'state':0.1,'cycle':0.1}):
    return list(map(lambda x: trajectories(x,initial,toll=toll),params))