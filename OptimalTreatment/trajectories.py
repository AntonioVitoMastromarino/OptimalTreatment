import control
from control import NonlinearIOSystem
from control import optimal
from matplotlib import pyplot
import numpy
from optimalcontrol import solve
from classify import classify_trajectory
from multiprocess import Process, Queue
from multiprocessing import Pool
from functools import reduce

def iteratedict(params):
    for par in params:
        if type(params[par])==list:
            temp = list(map(lambda x:params|{par:x},params[par]))
            return reduce(lambda x,y: x+y,list(map(iteratedict,temp)))
    return [params]

def solve_trajectories(params,initial,toll={'cured':0.1,'state':0.1,'orbit':0.1}):
    sol=map(lambda x:solve(params|{'initial':x}),initial)
    res = list(map(lambda x:classify_trajectory(x[1], params['threshold'], toll['cured'], toll['state'], toll['orbit']),sol))
    if 'queue' in params: params['queue'].put(res)
    else: return res

def manytrajectories(params,initial,toll={'cured':0.1,'state':0.1,'orbit':0.1}):
    return list(map(lambda x: solve_trajectories(x,initial,toll=toll),iteratedict(params)))
    