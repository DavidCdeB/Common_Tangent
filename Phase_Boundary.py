#

import numpy as np
from scipy.optimize import curve_fit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import sys
from sympy import *
import sympy as sym
import os
from itertools import chain
import numpy.polynomial.polynomial as poly

filefolder_for_Theo_PBE_D3 = './'

# 1) Analytical:
filefolder_for_analytical = 'All_P_H_real_intersection_at_Ts'

T_theo_analytical_PBE_D3, P_theo_analytical_PBE_D3 = np.loadtxt(os.path.join(filefolder_for_Theo_PBE_D3, filefolder_for_analytical, 'All_TEMPERATS_P_H_slope_common_tangent.dat'), skiprows = 1).T

### Plotting:
plt.figure()

T_theo_analytical_PBE_D3 = T_theo_analytical_PBE_D3[:19]
P_theo_analytical_PBE_D3 = P_theo_analytical_PBE_D3[:19]

T_theo_analytical_PBE_D3 = T_theo_analytical_PBE_D3[:-1]
P_theo_analytical_PBE_D3 = P_theo_analytical_PBE_D3[:-1]
print 'T_theo_analytical_PBE_D3 = ', T_theo_analytical_PBE_D3
print 'P_theo_analytical_PBE_D3 = ', P_theo_analytical_PBE_D3

p_PBE_D3,  = plt.plot(P_theo_analytical_PBE_D3, T_theo_analytical_PBE_D3, color='green', ls='--', marker='o')


fontP = FontProperties()
fontP.set_size('9')

ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.legend((\
p_PBE_D3,\
),\
(\
"PBE-D3",\
),\
prop=fontP, loc='upper left', ncol=2) #, bbox_to_anchor=(1, 0.5))#  loc=4)
plt.xlabel(r'$P$ (GPa)', fontsize=20)
plt.ylabel(r'$T$ (K)', fontsize=20)
extraticks=[273.15+25]
#plt.yticks(list(plt.yticks()[0]) + extraticks)
#plt.gca().set_xlim(left=0, right=10)
plt.gca().set_xlim(left=0, right=4)
#plt.gca().set_ylim(bottom=0, top=1000)
plt.gca().set_ylim(bottom=0, top=350)
plt.grid()

plt.savefig('calcite_I_and_II_phase_boundary.pdf', bbox_inches='tight')

plt.show()

