from multiprocessing import Pool
from OptimalTreatment import solve_trajectories, manytrajectories, iteratedict, solve, classify_trajectory, save
import numpy
import os
from functools import reduce

if __name__ == '__main__':

    if not os.path.exists('data'):os.mkdir('data')
    param={'k':1,'r':1,'threshold':0.9,'Tfinal':2**6,'Tsteps':2**8}
    param['s'] = [0.05, 1, 2.5, 5]
    param['d'] = [0.6, 25, 55, 80]
    param['a'] = [0.01, 0.1, 0.2 , 0.3]
    param['b'] = [0.05, 0.5, 0.95]
    initial = list(zip(list(zip([0.1, 0.4, 0.75],[0.001, 0.02, 0.07])),range(3)))
    toll={'cured':0.1,'state':0.1,'orbit':0.1}
    newpar=iteratedict(param)
    param=list(map(lambda x: x[0]|{'id':str(x[1]),'initial':initial},zip(newpar,range(len(newpar)))))
    newpar=reduce(lambda x,y:x+y,map(iteratedict,param))
    for par in newpar:
        par['id']=str(par['id'])
        if not os.path.exists('data/'+par['id']):os.mkdir('data/'+par['id'])
        for parameter in par:save(par[parameter],'data/'+par['id']+'/'+parameter)
        par['id']+='/'+par['initial'][1]
        par['initial']=par['initial'][0]
        if not os.path.exists('data/'+par['id']):os.mkdir('data/'+par['id'])
    with Pool() as pool:sol=list(pool.map(solve,newpar))
    sols=list(zip(map(lambda x: x[1], sol),newpar))
    resp=list(map(lambda x:classify_trajectory(x[0], x[1]['threshold'], toll['cured'], toll['state'], toll['orbit']),sols))
    print(resp)