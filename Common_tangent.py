#

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import sys
from sympy import *
import sympy as sym


# Intial candidates for fit 
E0_init = -941.510817926696   
V0_init = 63.54960592453  
B0_init = 76.3746233515232  
B0_prime_init = 4.05340727164527

# Data 1 (Red triangles): 
V_C_I, E_C_I = np.loadtxt('./1.dat', skiprows = 1).T

# Data 14 (Empty grey triangles):
V_14, E_14 = np.loadtxt('./2.dat', skiprows = 1).T

def BM(x, a, b, c, d):
        return  (2.293710449E+17)*(1E-21)* (a + b*x + c*x**2 + d*x**3 )

def P(x, b, c, d):
    return -b - 2*c*x - 3 *d*x**2

init_vals = [E0_init, V0_init, B0_init, B0_prime_init]
popt_C_I, pcov_C_I = curve_fit(BM, V_C_I, E_C_I, p0=init_vals)
popt_14, pcov_14 = curve_fit(BM, V_14, E_14, p0=init_vals)

x1 = var('x1')
x2 = var('x2')

E1 = P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - P(x2, popt_14[1], popt_14[2], popt_14[3])
print 'E1 = ', E1

E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
print 'E2 = ', E2

sols = solve([E1, E2], [x1, x2])
print 'sols = ', sols
sys.exit()

from scipy.optimize import fsolve
def equations(p):
    x1, x2 = p
    E1 = P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - P(x2, popt_14[1], popt_14[2], popt_14[3])
    E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
    return (E1, E2)

x1, x2 =  fsolve(equations, (50, 60))
print 'x1 = ', x1
print 'x2 = ', x2

def F(x):
    x1, x2 = x[0], x[1]
    E1 = P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - P(x2, popt_14[1], popt_14[2], popt_14[3])
    E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
#   E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) - (x1 - x2)) * P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
    return [E1, E2] 

print fsolve(F, [50, 60])    # some reasonable initial point

# Linspace for plotting the fitting curves:
V_C_I_lin = np.linspace(V_C_I[0], V_C_I[-1], 10000)
V_14_lin = np.linspace(V_14[0], V_14[-1], 10000)

plt.figure()
# Plotting the fitting curves:
p2, = plt.plot(V_C_I_lin, BM(V_C_I_lin, *popt_C_I), color='black', label='Cubic fit data 1' )
p6, = plt.plot(V_14_lin, BM(V_14_lin, *popt_14), 'b', label='Cubic fit data 2')

# Plotting the scattered points: 
p1 = plt.scatter(V_C_I, E_C_I, color='red', marker="^", label='Data 1', s=100)
p5 = plt.scatter(V_14, E_14, color='grey', marker="^", facecolors='none', label='Data 2', s=100)

plt.ticklabel_format(useOffset=False)

slope_common_tangent = P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
print 'slope_common_tangent = ', slope_common_tangent

def comm_tangent(x, x1, slope_common_tangent):
#  return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) * x1 + slope_common_tangent * x 
   return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - slope_common_tangent * x1 + slope_common_tangent * x 

xp = np.linspace(54, 68, 100)

plt.plot(xp, comm_tangent(xp, x1, slope_common_tangent))



plt.show()
sys.exit()



print 'sols = ', sols
print 'type(sols) = ', type(sols)
#sys.exit()

#x1 = sols[0][0] 
#x2 = sols[0][1] 

#print "x1 = ", x1
#print "x1 = ", x2

#print 'devf(sols[0][0]) = ', devf(sols[0][0])
#print 'P(x1) = ', P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
#print 'devg(sols[0][1]) = ', devg(sols[0][1])
#print 'P(x2) = ', P(x2, popt_14[1], popt_14[2], popt_14[3])
#print 'f(sols[0][0]) - g(sols[0][1]) / (sols[0][0] - sols[0][1]) = ', (f(sols[0][0]) - g(sols[0][1])) / (sols[0][0] - sols[0][1])
#print 'P(x1) -   = ' 

#slope_common_tangent = devf(sols[0][0])
slope_common_tangent = P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
print 'slope_common_tangent = ', slope_common_tangent

def comm_tangent(x, x1, slope_common_tangent):
   return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) * x1 + slope_common_tangent * x 


#plt.figure()
xp = np.linspace(54, 68, 100)
#plt.plot(xp, f(xp))
#plt.plot(xp, g(xp))
#plt.plot(xp, comm_tangent(xp, x1, slope_common_tangent))
#plt.show()
###


