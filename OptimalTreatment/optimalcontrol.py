import control
from control import NonlinearIOSystem
from control import optimal
from matplotlib import pyplot
import numpy
from files import save, load
import os

def model_1(t,x,u,params):
    drug=numpy.clip(u[0],0,1)
    dS=params['s']*(1-drug)*(1-(x[0]+x[1])/params['k'])*x[0]-drug*params['d']*x[0]
    dR=params['r']*(1-(params['c']*x[0]+x[1])/params['k'])*x[1]
    if x[0]+x[1]<params['threshold']: return numpy.array([dS,dR])
    else: return numpy.array([0,0])

def model_2(t,x,u,params):
    drug=numpy.clip(u[0],0,1)
    dS=(params['s']*(1-drug)*(1-(x[0]+x[1])/params['k'])-drug-params['a'])*x[0]+params['b']*x[1]
    dR=(params['r']*(1-(x[0]+x[1])/params['k'])-params['b'])*x[1]+params['a']*x[0]
    if x[0]+x[1]<params['threshold']: return numpy.array([dS,dR])
    else: return numpy.array([0,0])

def outpar(t,x,u,params):
    return x

def solve(params,epsilon=1):

    def terminal_cost(x,u):
        if x[0]+x[1]>=params['threshold']: return (x[0]+x[1])/params['threshold']-1
        else: return 0

    def lagrange_cost(x,u):
        if x[0]+x[1]<params['threshold']: return -1
        else: return 0

    timepts=numpy.linspace(0, params['Tfinal'], params['Tsteps'], endpoint=True)
    x0=numpy.array(params['initial']),
    if 'c' in params: model = model_1
    else: model = model_2

    cancer=NonlinearIOSystem(model,
                             outpar,
                             states=2,
                             inputs=('u',),
                             outputs=('S','R'),
                             params=params)

    constraint=[optimal.input_range_constraint(cancer,[0],[1])]

    result=optimal.solve_ocp(cancer,
                             timepts,
                             x0,
                             lagrange_cost,
                             constraint,
                             terminal_cost=terminal_cost,
                             initial_guess=load('data/'+params['id']+'/u'))

    response=control.input_output_response(cancer,
                                           timepts,
                                           result.inputs,
                                           x0,
                                           t_eval=timepts)

    t, x, u = response.time, response.outputs, response.inputs
    save(t,'data/'+params['id']+'/t')
    save(x,'data/'+params['id']+'/x')
    save(u,'data/'+params['id']+'/u')
    plotsolution((t, x, u),params['id'])
    return (t, x, u)

def plotsolution(solution,id):
    
    t,x,u=solution
    pyplot.plot(x[0], x[1])
    pyplot.xlabel("S")
    pyplot.ylabel("R")
    pyplot.savefig('data/'+id+'/size_traj.png')
    pyplot.close()
    pyplot.plot(t, numpy.clip(u[0],0,1))
    pyplot.axis([0, t[-1], -0.1, 1.1])
    pyplot.xlabel("t")
    pyplot.ylabel("delta")
    pyplot.savefig('data/'+id+'/drug_dose.png')
    pyplot.close()