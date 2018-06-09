#

import numpy as np
import matplotlib.pyplot as plt
import sys
from sympy import *
import sympy as sym


from sympy import solve
from sympy import var

### Example

def f(x):
   return x**2

def devf(x):
   return 2*x

def g(x):
   return (x - 2)**2 + 3

def devg(x):
   return 2*(x - 2) 

x1 = var('x1')
x2 = var('x2')

E1 = devf(x1) - devg(x2)
E2 = ((f(x1) - g(x2)) / (x1 - x2)) - devf(x1)

sols = solve([E1, E2], [x1, x2])

print 'sols = ', sols
print 'type(sols) = ', type(sols)

x1 = sols[0][0] 
x2 = sols[0][1] 

print "x1 = ", x1
print "x1 = ", x2

print 'devf(sols[0][0]) = ', devf(sols[0][0])
print 'devg(sols[0][1]) = ', devg(sols[0][1])
print 'f(sols[0][0]) - g(sols[0][1]) / (sols[0][0] - sols[0][1]) = ', (f(sols[0][0]) - g(sols[0][1])) / (sols[0][0] - sols[0][1])

slope_common_tangent = devf(sols[0][0])
print 'slope_common_tangent = ', slope_common_tangent

def comm_tangent(x, x1, slope_common_tangent):
   return f(x1) - devf(x1) * x1 + slope_common_tangent * x 

plt.figure()
xp = np.linspace(-2, 4, 100)
plt.plot(xp, f(xp), label='f(x)')
plt.plot(xp, g(xp), label='g(x)')
plt.plot(xp, comm_tangent(xp, x1, slope_common_tangent), label='Common tangent')
plt.legend()
plt.show()
