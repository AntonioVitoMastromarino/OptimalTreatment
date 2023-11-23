import control
from control import NonlinearIOSystem
from control import optimal
from matplotlib import pyplot
import numpy

def model_1(t,x,u,params):
    dS=params['s']*(1-u[0])*(1-(x[0]+x[1])/params['k'])*x[0]-u[0]*x[0]
    dR=params['r']*(1-(params['c']*x[0]+x[1])/params['k'])*x[1]
    return numpy.array([dS,dR])

def model_2(t,x,u,params):
    dS=(params['s']*(1-u[0])*(1-(x[0]+x[1])/params['K'])-u[0]-params['a'])*x[0]+params['b']*x['1']
    dR=(params['r']*(1-(x[0]+x[1])/params['k'])-params['b'])*x[1]+params['a']*x[0]
    return numpy.array([dS,dR])

def outpar(t,x,u,params):
    return x

def terminal_cost(x,u):
    return 1000*(x[0]+x[1])

def lagrange_cost(x,u):
    return 0

Tf=64
Ts=256
timepts=numpy.linspace(0, Tf, Ts, endpoint=True)
x0=numpy.array([0.25,0.25]),

def solve(params):
    if 'c' in params: model = model_1
    else: model = model_2
    cancer=NonlinearIOSystem(model,
                             outpar,
                             states=2,
                             inputs=('d',),
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
    return control.input_output_response(cancer,
                                         timepts,
                                         result.inputs,
                                         x0,
                                         t_eval=numpy.linspace(0, Tf, Ts))

def plotsolution(params):
    
    outresponse=solve(params)
    t, x, u = outresponse.time, outresponse.outputs, outresponse.inputs

    pyplot.subplot(2, 1, 1)
    pyplot.plot(x[0], x[1])
    pyplot.xlabel("S")
    pyplot.ylabel("R")

    pyplot.subplot(2, 1, 2)
    pyplot.plot(t, u[0])
    pyplot.axis([0, Tf, -0.1, 1.1])
    pyplot.xlabel("t")
    pyplot.ylabel("delta")

    pyplot.show()