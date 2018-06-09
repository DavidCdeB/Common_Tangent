#

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import sys
from sympy import *
import sympy as sym
import os
from itertools import chain
import pickle as pl


# Intial candidates for fit, per FU: - thus, the E vs V input data has to be per FU
E0_init = -941.510817926696   
V0_init = 63.54960592453 
B0_init = 76.3746233515232 
B0_prime_init = 4.05340727164527 

def BM(x, a, b, c, d):
         return  a + b*x + c*x**2 + d*x**3 

def P(x, b, c, d):
     return 4.3597482E+3 * (-b - 2*c*x - 3 *d*x**2) 

def devBM(x, b, c, d):
         return  b + 2*c*x + 3*d*x**2 

def H(x, a, b, c, d):
     return  a + b*x + c*x**2 + d*x**3


filefolder_Calcite_I_SG_167 = '../../Files_Outputs/Calcite_I/G_PT'

filefolder_Calcite_II_SG_14 = '../../Files_Outputs/Calcite_II/G_PT'

filefolder_energetics = 'EL_vs_V'

# Calcite I (Red triangles): 
V_C_I, E_C_I = np.loadtxt(os.path.join(filefolder_Calcite_I_SG_167, filefolder_energetics, 'EL_vs_V.dat'), skiprows = 1).T

# 14 (Empty grey triangles):
V_14, E_14 = np.loadtxt(os.path.join(filefolder_Calcite_II_SG_14, filefolder_energetics, 'EL_vs_V.dat'), skiprows = 1).T

init_vals = [E0_init, V0_init, B0_init, B0_prime_init]
popt_C_I, pcov_C_I = curve_fit(BM, V_C_I, E_C_I, p0=init_vals)
popt_14, pcov_14 = curve_fit(BM, V_14, E_14, p0=init_vals)

x1 = var('x1')
x2 = var('x2')

E1 = devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - devBM(x2, popt_14[1], popt_14[2], popt_14[3])
print 'E1 = ', E1

E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
print 'E2 = ', E2

sols = solve([E1, E2], [x1, x2])
print 'sols = ', sols

from scipy.optimize import fsolve
def equations(p):
    x1, x2 = p
    E1 = devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - devBM(x2, popt_14[1], popt_14[2], popt_14[3])
    E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
    return (E1, E2)

#x1, x2 =  fsolve(equations, (50, 60))
#x1, x2 =  fsolve(equations, (60, 64))
#x1, x2 =  fsolve(equations, (61.5, 62))
x1, x2 =  fsolve(equations, (61.99, 62))

print 'x1 = ', x1
print 'x2 = ', x2

slope_common_tangent = devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
print 'slope_common_tangent = ', slope_common_tangent
slope_common_tangent_GPa = abs(slope_common_tangent * 4.3597482E+3)
print ' slope_common_tangent_GPa = ', slope_common_tangent_GPa

def comm_tangent(x, x1, slope_common_tangent):
   return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - slope_common_tangent * x1 + slope_common_tangent * x

# Linspace for plotting the fitting curves:
V_C_I_lin = np.linspace(V_C_I[0], V_C_I[-1], 10000)
V_14_lin = np.linspace(V_14[0], V_14[-1], 10000)

print ' shape.V_C_I_lin = ', np.shape(V_C_I_lin)

fig_handle = plt.figure()

# Plotting the fitting curves:
p2, = plt.plot(V_C_I_lin, BM(V_C_I_lin, *popt_C_I), color='black', label='Cubic fit Calcite I' )
p6, = plt.plot(V_14_lin, BM(V_14_lin, *popt_14), 'b', label='Cubic fit Calcite II')

xp = np.linspace(54, 68, 100)
pcomm_tangent, = plt.plot(xp, comm_tangent(xp, x1, slope_common_tangent), 'green', label='Common tangent')

# Plotting the scattered points: 
p1 = plt.scatter(V_C_I, E_C_I, color='red', marker="^", label='Calcite I', s=100)
p5 = plt.scatter(V_14, E_14, color='grey', marker="^", facecolors='none', label='Calcite II', s=100)

fontP = FontProperties()
fontP.set_size('13')

plt.legend((p1, p2, p5, p6, pcomm_tangent), ("Calcite I", "Cubic fit Calcite I", "Calcite II", 'Cubic fit Calcite II', 'Common tangent'), prop=fontP)

print 'devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) = ', devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])

# obtain the Temperature we are working at:
import subprocess
T = subprocess.check_output("basename `pwd`", shell=True)
print 'T = ', T

import string
new_T = string.replace(T, '_', ' ')
print 'new_T = ', new_T
T = T.rstrip()
new_T = new_T.rstrip()

print 'new_T = ', new_T

T_folder = string.replace(new_T, ' ', '')
print 'T_folder = ', T_folder
T_folder = string.replace(new_T, 'K', '')
print 'T_folder = ', T_folder

T_folder_float = float(T_folder)

plt.xlabel('$V$ / F.U. (Angstrom$^{3}$)', fontsize=20)
plt.ylabel(r'$(F = E + E_{ZP} + ET - TS)$ / F.U. (a.u.)', fontsize=20)
plt.suptitle("PBE-D3, pob-TZVP, SHRINK 8 8, Bipolar 18 18, TOLINTEG 8 18, XXLGRID, TOLDEE 8")
plt.title("(0.87 - 0.98)$V_{eq}$ and (0.98 - 1.08)$V_{eq}$. T = %s" %new_T, fontsize=10)
plt.ticklabel_format(useOffset=False)
ax = fig_handle.add_subplot(111)
ax.annotate('Slope\nCommon tangent:\nP= %g GPa' %slope_common_tangent_GPa, xy=(56, comm_tangent(56, x1, slope_common_tangent)), xytext=(54, comm_tangent(56, x1, slope_common_tangent) - 0.005), fontsize=15,           arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='purple'),
            )
plt.savefig('calcite_I_and_II_all_2_summary_better_plot.pdf', bbox_inches='tight')
pl.dump(fig_handle,file('sinus.pickle_calcite_I_and_II_all_2_summary_better_plot','w'))

output_array_2 = np.vstack((T_folder_float, slope_common_tangent_GPa)).T
np.savetxt('P_H_slope_common_tangent_T_%sK.dat' %T_folder , output_array_2, header="Temperature (K) \t Pressure_Intersection (GPa)", fmt="%0.13f")


global V0, B0, B0_prime
E0   =     popt_C_I[0] 
V0   =     popt_C_I[1]
B0   =     popt_C_I[2]
B0_prime = popt_C_I[3]

pressures_per_F_unit_C_I = P(V_C_I, V0, B0, B0_prime)
print 'popt_C_I = ', popt_C_I
print 'popt_C_I[1:] = ', popt_C_I[1:]
output_array_2 = np.vstack((E_C_I, V_C_I, pressures_per_F_unit_C_I)).T
np.savetxt('Volumes_and_pressures_C_I.dat', output_array_2, header="Energy / FU (a.u.) \t Volume / FU (A^3) \t Pressures (GPa)", fmt="%0.13f")

global V0_14, B0_14, B0_prime_14
E0_14   =     popt_14[0] 
V0_14   =     popt_14[1]
B0_14   =     popt_14[2]
B0_prime_14 = popt_14[3]


pressures_per_F_unit_14 = P(V_14, V0_14, B0_14, B0_prime_14)
output_array_2 = np.vstack((E_14, V_14, pressures_per_F_unit_14)).T
np.savetxt('Volumes_and_pressures_14.dat', output_array_2, header="Energy / FU (a.u.) \t Volume / FU (A^3) \t Pressures (GPa)", fmt="%0.13f")

#plt.show()
