import control
from control import NonlinearIOSystem
from control import optimal
from matplotlib import pyplot
import numpy

def model_1(t,x,u,params):
    dS=params['s']*(1-u[0])*(1-(x[0]+x[1])/params['k'])*x[0]-u[0]*params['d']*x[0]
    dR=params['r']*(1-(params['c']*x[0]+x[1])/params['k'])*x[1]
    if x[0]+x[1]<params['threshold']: return numpy.array([dS,dR])
    else: return numpy.array([0,0])

def model_2(t,x,u,params):
    dS=(params['s']*(1-u[0])*(1-(x[0]+x[1])/params['k'])-u[0]-params['a'])*x[0]+params['b']*x['1']
    dR=(params['r']*(1-(x[0]+x[1])/params['k'])-params['b'])*x[1]+params['a']*x[0]
    if x[0]+x[1]<params['threshold']: return numpy.array([dS,dR])
    else: return numpy.array([0,0])

def outpar(t,x,u,params):
    return x

def solve(params,epsilon=0.1):

    def terminal_cost(x,u):
        return epsilon*(x[0]+x[1])

    def lagrange_cost(x,u):
        if x[0]+x[1]<params['threshold']: return epsilon*u[0]*(1-u[0])-1
        else: return epsilon*u[0]*(1-u[0])

    timepts=numpy.linspace(0, params['Tfinal'], params['Tsteps'], endpoint=True)
    x0=numpy.array([params['S0'],params['R0']]),
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
                             initial_guess=numpy.array([0.5]))

    response=control.input_output_response(cancer,
                                           timepts,
                                           result.inputs,
                                           x0,
                                           t_eval=timepts)

    t, x, u = response.time, response.outputs, response.inputs

    return (t, x, u)

def plotsolution(solution):
    
    t,x,u=solution
    
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x[0], x[1])
    pyplot.xlabel("S")
    pyplot.ylabel("R")

    pyplot.subplot(2, 1, 2)
    pyplot.plot(t, u[0])
    pyplot.axis([0, t[-1], -0.1, 1.1])
    pyplot.xlabel("t")
    pyplot.ylabel("delta")

    pyplot.show()