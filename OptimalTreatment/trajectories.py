import control
from control import NonlinearIOSystem
from control import optimal
from matplotlib import pyplot
import numpy
from OptimalTreatment import solve

def trajectories(param,initial):
    sol=map(lambda x:solve(param|{'S0':x[0],'R0':x[1]}),initial)
    return list(map(lambda x:x[1],sol))