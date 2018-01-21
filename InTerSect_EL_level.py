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
E0_init = -941.510817926696  # -1882.50963222/2.0 
V0_init = 63.54960592453 #125.8532/2.0 
B0_init = 76.3746233515232 #74.49 
B0_prime_init = 4.05340727164527 #4.15

#def BM(V, E0, V0, B0, B0_prime):
#        return  E0+ (2.293710449E+17)*(1E-21)*( (9.0/16.0)*(V0*B0) * (  (((V0/V)**(2.0/3.0)-1.0)**3.0)*B0_prime  + ((V0/V)**(2.0/3.0)-1)**2  *  (6.0-4.0*(V0/V)**(2.0/3.0))  ))

def BM(x, a, b, c, d):
#        return  (2.293710449E+17)*(1E-21)* (a + b*x + c*x**2 + d*x**3 )
         return  a + b*x + c*x**2 + d*x**3 

#def P(V, V0, B0, B0_prime):
#     f0=(3.0/2.0)*B0
#     f1=((V0/V)**(7.0/3.0))-((V0/V)**(5.0/3.0))
#     f2=((V0/V)**(2.0/3.0))-1
#     pressure= f0*f1*(1+(3.0/4.0)*(B0_prime-4)*f2)
#     return pressure

def P(x, b, c, d):
     return 4.3597482E+3 * (-b - 2*c*x - 3 *d*x**2) 

def devBM(x, b, c, d):
#   return (2.293710449E+17)*(1E-21)* (b + 2*c*x + 3 *d*x**2)
         return  b + 2*c*x + 3*d*x**2 

def H(x, a, b, c, d):
     return  a + b*x + c*x**2 + d*x**3


filefolder_Calcite_I_SG_167 = '/home/david/Trabajo/structures/Calcite_I_and_II/PBE-D3__SHRINK_8_8__bipolar_18_18__TOLINTEG_8_18__XXLGRID_TOLDEE_8/DEFINITIVE_ALL_QUANTITITES_FROM_SCELPHONO_OUTPUT/RAW_DATA_for_QHA/Calcite_II_SG_14/preparation/to_post/to_post_2/implementation_check_final_F_files/Application_to_all_calcite_II_SG_14/Result_of_QHA_step_script/Calcite_I_SG_167/9_volumes_CII_and_11_volumes_C_I/CI_SG_167_estable_scelphono_outputs' 

filefolder_Calcite_II_SG_14 = '/home/david/Trabajo/structures/Calcite_I_and_II/PBE-D3__SHRINK_8_8__bipolar_18_18__TOLINTEG_8_18__XXLGRID_TOLDEE_8/DEFINITIVE_ALL_QUANTITITES_FROM_SCELPHONO_OUTPUT/RAW_DATA_for_QHA/Calcite_II_SG_14/preparation/to_post/to_post_2/implementation_check_final_F_files/Application_to_all_calcite_II_SG_14/Result_of_QHA_step_script/Calcite_II_SG_14/9_volumes_CII_and_11_volumes_C_I/CII_SG_14_freqcalc_outputs'

#filefolder_Calcite_I_son_SG_161 = '' TO OBTAIN!!

filefolder_energetics = 'EL_vs_V'

# Calcite I (Red triangles): 
V_C_I, E_C_I = np.loadtxt(os.path.join(filefolder_Calcite_I_SG_167, filefolder_energetics, './EL_vs_V.dat'), skiprows = 1).T

# 14 (Empty grey triangles):
V_14, E_14 = np.loadtxt(os.path.join(filefolder_Calcite_II_SG_14, filefolder_energetics, './EL_vs_V.dat'), skiprows = 1).T

#V_161, E_161 = np.loadtxt(os.path.join(filefolder_Calcite_I_son_SG_161, filefolder_energetics, './EL_vs_V.dat'), skiprows = 1).T

init_vals = [E0_init, V0_init, B0_init, B0_prime_init]
popt_C_I, pcov_C_I = curve_fit(BM, V_C_I, E_C_I, p0=init_vals)
popt_14, pcov_14 = curve_fit(BM, V_14, E_14, p0=init_vals)
#popt_161, pcov_161 = curve_fit(BM, V_161, E_161, p0=init_vals)

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

x1, x2 =  fsolve(equations, (50, 60))
print 'x1 = ', x1
print 'x2 = ', x2

#def F(x):
#    x1, x2 = x[0], x[1]
#    E1 = devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - devBM(x2, popt_14[1], popt_14[2], popt_14[3])
#    E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
##   E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) - (x1 - x2)) * P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
#    return [E1, E2]
#
#print fsolve(F, [50, 60])    # some reasonable initial point
#
#solutions = fsolve(F, [50, 60])
#print 'solutions[0] = ', solutions[0]
#print 'solutions[1] = ', solutions[1]
#

slope_common_tangent = devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
print 'slope_common_tangent = ', slope_common_tangent
slope_common_tangent_GPa = abs(slope_common_tangent * 4.3597482E+3)
print ' slope_common_tangent_GPa = ', slope_common_tangent_GPa

#slope_common_tangent2 = devBM(solutions[0], popt_C_I[1], popt_C_I[2], popt_C_I[3])
#print 'slope_common_tangent2 = ', slope_common_tangent2

def comm_tangent(x, x1, slope_common_tangent):
#  return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) * x1 + slope_common_tangent * x 
   return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - slope_common_tangent * x1 + slope_common_tangent * x

#x = var('x')
#print comm_tangent(x, x1, slope_common_tangent)
#sys.exit()

# Linspace for plotting the fitting curves:
V_C_I_lin = np.linspace(V_C_I[0], V_C_I[-1], 10000)
V_14_lin = np.linspace(V_14[0], V_14[-1], 10000)
#V_161_lin = np.linspace(V_161[0], V_161[-1], 10000)

print ' shape.V_C_I_lin = ', np.shape(V_C_I_lin)
#sys.exit()

fig_handle = plt.figure()

# Plotting the fitting curves:
p2, = plt.plot(V_C_I_lin, BM(V_C_I_lin, *popt_C_I), color='black', label='Cubic fit Calcite I' )
p6, = plt.plot(V_14_lin, BM(V_14_lin, *popt_14), 'b', label='Cubic fit Calcite II')
#p161, = plt.plot(V_161_lin, BM(V_161_lin, *popt_161), 'brown', label='Cubic fit 161')

xp = np.linspace(54, 68, 100)
pcomm_tangent, = plt.plot(xp, comm_tangent(xp, x1, slope_common_tangent), 'green', label='Common tangent')

# Plotting the scattered points: 
p1 = plt.scatter(V_C_I, E_C_I, color='red', marker="^", label='Calcite I', s=100)
p5 = plt.scatter(V_14, E_14, color='grey', marker="^", facecolors='none', label='Calcite II', s=100)
#p7 = plt.scatter(V_7, E_7, color='magenta', marker="^", facecolors='none', label='S.G. 7', s=100)
#p8 = plt.scatter(V_161, E_161, color='green', marker="^", facecolors='none', label='S.G. 161', s=100)

fontP = FontProperties()
#fontP.set_size('small')
fontP.set_size('13')

#plt.legend((p1, p2, p5, p6, p8, p161), ("Calcite I", "Cubic fit Calcite I", "Calcite II", 'Cubic fit Calcite II', "S.G. 161", "Cubic fit S.G. 161"), prop=fontP)
plt.legend((p1, p2, p5, p6, pcomm_tangent), ("Calcite I", "Cubic fit Calcite I", "Calcite II", 'Cubic fit Calcite II', 'Common tangent'), prop=fontP)

print 'devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) = ', devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
 
plt.xlabel('$V$ / F.U. (Angstrom$^{3}$)', fontsize=20)
plt.ylabel(r'$E$ / F.U. (a.u.)', fontsize=20)
plt.suptitle("PBE-D3, pob-TZVP, SHRINK 8 8, Bipolar 18 18, TOLINTEG 8 18, XXLGRID, TOLDEE 8")
plt.title("(0.87 - 0.98)$V_{eq}$ and (0.98 - 1.08)$V_{eq}$", fontsize=10)
plt.ticklabel_format(useOffset=False)
ax = fig_handle.add_subplot(111)
ax.annotate('Slope\nCommon tangent:\nP= %g GPa' %slope_common_tangent_GPa, xy=(56, comm_tangent(56, x1, slope_common_tangent)), xytext=(54, comm_tangent(56, x1, slope_common_tangent) - 0.005), fontsize=15,           arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='purple'),
            )
plt.savefig('calcite_I_and_II_all_2_summary_better_plot.pdf', bbox_inches='tight')
pl.dump(fig_handle,file('sinus.pickle_calcite_I_and_II_all_2_summary_better_plot','w'))

T_folder = 0.0

output_array_2 = np.vstack((T_folder, slope_common_tangent_GPa)).T
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

#global V0_161, B0_161, B0_prime_161
#E0_161   =     popt_161[0] 
#V0_161   =     popt_161[1]
#B0_161   =     popt_161[2]
#B0_prime_161 = popt_161[3]


#pressures_per_F_unit_161 = P(V_161, V0_161, B0_161, B0_prime_161)
#output_array_3 = np.vstack((E_161, V_161, pressures_per_F_unit_161)).T
#np.savetxt('Volumes_and_pressures_161.dat', output_array_3, header="Energy / FU (a.u.) \t Volume / FU (A^3) \t Pressures (GPa)", fmt="%0.13f")


plt.show()
sys.exit()


#plt.figure()
fig_handle = plt.figure()

# Plotting the fitting curves:
p2, = plt.plot(V_C_I_lin, BM(V_C_I_lin, *popt_C_I), color='black', label='Cubic fit Calcite I' )

# Plotting the scattered points: 
p1 = plt.scatter(V_C_I, E_C_I, color='red', marker="^", label='Calcite I', s=100)
fontP = FontProperties()
#fontP.set_size('small')
fontP.set_size('15')

plt.legend((p1, p2), ("Calcite I", "Cubic fit Calcite I"), prop=fontP)

plt.xlabel('$V$ / F.U. (Angstrom$^{3}$)', fontsize=20)
plt.ylabel(r'$E$ / F.U. (a.u.)', fontsize=20)
plt.suptitle("PBE-D3, pob-TZVP, SHRINK 8 8, Bipolar 18 18, TOLINTEG 8 18, XXLGRID, TOLDEE 8")
plt.title("(0.87 - 0.98)$V_{eq}$ and (0.98 - 1.08)$V_{eq}$", fontsize=10)
plt.ticklabel_format(useOffset=False)
plt.savefig('calcite_I_summary_better_plot.pdf', bbox_inches='tight')
pl.dump(fig_handle,file('sinus.pickle_calcite_I_summary_better_plot','w'))


# Plotting P vs V:
#fig = plt.figure()
fig_handle = plt.figure()

p2, = plt.plot(V_C_I_lin, P(V_C_I_lin, V0, B0, B0_prime), color='black', label='Cubic fit Calcite I' )
p6, = plt.plot(V_14_lin, P(V_14_lin, V0_14, B0_14, B0_prime_14), 'b', label='Cubic fit Calcite II')

#p161, = plt.plot(V_161_lin, P(V_161_lin, V0_161, B0_161, B0_prime_161), 'brown', label='Cubic fit 161')


# Plotting the scattered points: 
p1 = plt.scatter(V_C_I, pressures_per_F_unit_C_I, color='red', marker="^", label='Calcite I', s=100)
p5 = plt.scatter(V_14, pressures_per_F_unit_14, color='grey', marker="^", facecolors='none', label='Calcite II', s=100)
#p7 = plt.scatter(V_7, E_7, color='magenta', marker="^", facecolors='none', label='S.G. 7', s=100)

#p8 = plt.scatter(V_161, pressures_per_F_unit_161, color='green', marker="^", facecolors='none', label='S.G. 161', s=100)

fontP = FontProperties()
#fontP.set_size('small')
fontP.set_size('13')

#plt.legend((p1, p2, p5, p6, p8, p161), ("Calcite I", "Cubic fit Calcite I", "Calcite II", 'Cubic fit Calcite II', "S.G. 161", "Cubic fit S.G. 161"), prop=fontP)
plt.legend((p1, p2, p5, p6), ("Calcite I", "Cubic fit Calcite I", "Calcite II", 'Cubic fit Calcite II'), prop=fontP)

plt.xlabel('$V$ / F.U. (Angstrom$^{3}$)', fontsize=20)
plt.ylabel(r'$P = -\frac{\partial E }{\partial V}$ (GPa)', fontsize=20)
plt.suptitle("PBE-D3, pob-TZVP, SHRINK 8 8, Bipolar 18 18, TOLINTEG 8 18, XXLGRID, TOLDEE 8")
plt.title("(0.87 - 0.98)$V_{eq}$ and (0.98 - 1.08)$V_{eq}$", fontsize=10)
plt.ticklabel_format(useOffset=False)

plt.savefig('calcite_I_and_II_all_2_summary_better_plot_P_vs_V.pdf', bbox_inches='tight')
pl.dump(fig_handle,file('sinus.pickle_calcite_I_and_II_all_2_summary_better_plot_P_vs_V','w'))


#000000000000000000

H_C_I = E_C_I + pressures_per_F_unit_C_I * V_C_I * (2.293710449E+17)*(1E-21) 
H_14 = E_14 + pressures_per_F_unit_14 * V_14 * (2.293710449E+17)*(1E-21)
#H_161 = E_161 + pressures_per_F_unit_161 * V_161 * (2.293710449E+17)*(1E-21)

output_array_3 = np.vstack((E_C_I, V_C_I, pressures_per_F_unit_C_I, H_C_I)).T
np.savetxt('E_V_P_H__C_I.dat', output_array_3, header="Energy / FU (a.u.) \t Volume / FU (A^3) \t Pressure / F.U. (GPa) \t Enthalpy (a.u.)", fmt="%0.13f") 

output_array_4 = np.vstack((E_14, V_14, pressures_per_F_unit_14, H_14)).T
np.savetxt('E_V_P_H__14.dat', output_array_4, header="Energy / FU (a.u.) \t Volume / FU (A^3) \t Pressure / F.U. (GPa) \t Enthalpy (a.u.)", fmt="%0.13f") 

#output_array_5 = np.vstack((E_161, V_161, pressures_per_F_unit_161, H_161)).T
#np.savetxt('E_V_P_H__161.dat', output_array_5, header="Energy / FU (a.u.) \t Volume / FU (A^3) \t Pressure / F.U. (GPa) \t Enthalpy (a.u.)", fmt="%0.13f") 

# Saving into variables:

P_lin_C_I = P(V_C_I_lin, V0, B0, B0_prime)
H_lin_C_I = BM(V_C_I_lin, *popt_C_I) +  P(V_C_I_lin, V0, B0, B0_prime) * V_C_I_lin * (2.293710449E+17)*(1E-21)

P_lin_14 = P(V_14_lin, V0_14, B0_14, B0_prime_14)
H_lin_14 = BM(V_14_lin, *popt_14) + P(V_14_lin, V0_14, B0_14, B0_prime_14) * V_14_lin * (2.293710449E+17)*(1E-21) 

#P_lin_161 = P(V_161_lin, V0_161, B0_161, B0_prime_161)
#H_lin_161 = BM(V_161_lin, *popt_161) + P(V_161_lin, V0_161, B0_161, B0_prime_161) * V_161_lin * (2.293710449E+17)*(1E-21) 


print ' P_lin_C_I = ', P_lin_C_I
print ' type(P_lin_C_I) = ', type(P_lin_C_I)
print ' H_lin_C_I = ', H_lin_C_I
print ' P_lin_14  = ', P_lin_14
print ' H_lin_14  = ', H_lin_14

output_array_1 = np.vstack((P_lin_C_I, H_lin_C_I)).T
np.savetxt('P_lin_C_I__H_lin_C_I.dat', output_array_1, header="P(GPa) \t   H per F unit (a.u)", fmt="%0.13f")

output_array_2 = np.vstack((P_lin_14, H_lin_14)).T
np.savetxt('P_lin_14__H_lin_14.dat', output_array_2, header="P(GPa) \t    H per F unit (a.u)", fmt="%0.13f")

#output_array_3 = np.vstack((P_lin_161, H_lin_161)).T
#np.savetxt('P_lin_14__H_lin_161.dat', output_array_3, header="P(GPa) \t    H per F unit (a.u)", fmt="%0.13f")
plt.show()
sys.exit()
print 'Performing the collisions program....'

def within_tolerance(p1, p2):
    tol = 1e-3 # enough for the exact H fit 
#   tol = 1e-3  

    P_lin_C_I, H_lin_C_I = p1
    P_lin_14, H_lin_14 = p2

    return abs(H_lin_C_I - H_lin_14) < tol and abs(P_lin_C_I - P_lin_14) < tol

points_1 = list(zip(P_lin_C_I, H_lin_C_I))
points_2 = list(zip(P_lin_14, H_lin_14))


collisions_2 = []

for p1 in points_1:
    matches = [p2 for p2 in points_2 if within_tolerance(p1, p2)]
    collisions_2.append(matches)

collisions_1 = []

for p2 in points_2:
    matches = [p1 for p1 in points_1 if within_tolerance(p1, p2)]
    collisions_1.append(matches)


#print 'collisions_1 = ', collisions_1

#print 'collisions_2 = ', collisions_2

collisions_1 = [i for i in chain.from_iterable(collisions_1)]
#print  'collisions in calcite 1 = ', collisions_1

collisions_2 = [i for i in chain.from_iterable(collisions_2)]
#print 'collisions in calcite 2 = ', collisions_2

output_array_1 = np.vstack((collisions_1))
np.savetxt('collisions_1.dat', output_array_1, header="P(GPa) \t   H per F unit (a.u)", fmt="%0.13f")

output_array_2 = np.vstack((collisions_2))
np.savetxt('collisions_2.dat', output_array_2, header="P(GPa) \t   H per F unit (a.u)", fmt="%0.13f")

Intersection = max(collisions_1, key=lambda item:item[1])
#print ' Intersection = ', Intersection


# Plotting and fitting to the exact expression of Delta_H:
#********* Exact expression of Delta_H:

#fig = plt.figure()
fig_handle = plt.figure()

EnergyCI, VolumeCI, PressureCI, EnthalpyCI  = np.loadtxt('./E_V_P_H__C_I.dat', skiprows = 1).T

print 'PressureCI[0] = ', PressureCI[0]
print 'PressureCI[-1] = ', PressureCI[-1]

Energy14, Volume14, Pressure14, Enthalpy14  = np.loadtxt('./E_V_P_H__14.dat', skiprows = 1).T

print 'Pressure14[0] = ', Pressure14[0]
print 'Pressure14[-1] = ', Pressure14[-1]

#xp_C_I = np.linspace(PressureCI[-1], PressureCI[0], 100)
xp_C_I = np.linspace(PressureCI[0], PressureCI[-1], 100)
#xp_14 = np.linspace(Pressure14[-1], Pressure14[0], 100)
xp_14 = np.linspace(Pressure14[0], Pressure14[-1], 100)

# Plotting the fitting curves:

print 'np.shape(V_C_I_lin) = ', np.shape(V_C_I_lin)
print 'np.shape(P(V_C_I_lin, V0, B0, B0_prime))  = ', np.shape(P(V_C_I_lin, V0, B0, B0_prime))

# IOBE suggestion:
p2, = plt.plot(P(V_C_I_lin, V0, B0, B0_prime), ( BM(V_C_I_lin, *popt_C_I) + P(V_C_I_lin, V0, B0, B0_prime) * V_C_I_lin * (2.293710449E+17)*(1E-21)), color='black', label='H fit Data' )

# IOBE suggestion:
p6, = plt.plot(P(V_14_lin, V0_14, B0_14, B0_prime_14), ( BM(V_14_lin, *popt_14) + P(V_14_lin, V0_14, B0_14, B0_prime_14) * V_14_lin * (2.293710449E+17)*(1E-21)), color='blue', label='H fit Data' )


# Plotting the scattered points: 
p1 = plt.scatter(pressures_per_F_unit_C_I, H_C_I, color='red', marker="^", label='Calcite I', s=100)
p5 = plt.scatter(pressures_per_F_unit_14, H_14, color='grey', marker="^", facecolors='none', label='Calcite II', s=100)

fontP = FontProperties()
#fontP.set_size('small')
fontP.set_size('15')

plt.legend((p1, p2, p5, p6), ("Calcite I", 'Fit Calcite I', 'Calcite II', 'Fit Calcite II'), prop=fontP)

plt.xlabel('P / F.U. (GPa)', fontsize=20)
plt.ylabel(r'$(H = E + PV)$ / F.U. (a.u.)', fontsize=20)
plt.suptitle("PBE-D3, pob-TZVP, SHRINK 8 8, Bipolar 18 18, TOLINTEG 8 18, XXLGRID, TOLDEE 8")
plt.title("(0.87 - 0.98)$V_{eq}$ and (0.98 - 1.08)$V_{eq}$", fontsize=10)
plt.ticklabel_format(useOffset=False)
ax = fig_handle.add_subplot(111)
ax.annotate('Collisions Intersection\nP= %g GPa\nH = %g a.u.' %(Intersection[0], Intersection[1]), xy=(Intersection[0], Intersection[1]), xytext=(Intersection[0]+1.7, Intersection[1]-0.05), fontsize=15,
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='purple'),
            )
plt.savefig('calcite_I_and_II_all_2_summary_better_plot_delta_H_exact_expression_with_intersection.pdf', bbox_inches='tight')
pl.dump(fig_handle,file('sinus.pickle_calcite_I_and_II_all_2_summary_better_plot_delta_H_exact_expression_with_intersection','w'))

#plt.show()
#sys.exit()



print 'Performing the Analytic intersection....'

fig = plt.figure()

#  Obtaining a cubic expression for H(P):

# Reminder:
#H_C_I = E_C_I + pressures_per_F_unit_C_I * V_C_I * (2.293710449E+17)*(1E-21) 
#H_14 = E_14 + pressures_per_F_unit_14 * V_14 * (2.293710449E+17)*(1E-21)

init_vals = [E0_init, V0_init, B0_init, B0_prime_init]

popt_HofP_C_I, pcov_HofP_C_I = curve_fit(H, pressures_per_F_unit_C_I, H_C_I, p0=init_vals)
popt_HofP_14, pcov_HofP_14 = curve_fit(H, pressures_per_F_unit_14, H_14, p0=init_vals)
#popt_HofP_161, pcov_HofP_161 = curve_fit(H, pressures_per_F_unit_161, H_161, p0=init_vals)


#print " %%%%%%%%%%%%%%%%%%%%%% pressures_per_F_unit_161 = ", pressures_per_F_unit_161
#pressures_per_F_unit_161_sorted = np.sort(pressures_per_F_unit_161)
#print " np.sort(pressures_per_F_unit_161) ", pressures_per_F_unit_161_sorted
#pressures_per_F_unit_161_lin = pressures_per_F_unit_161_sorted 

print " %%%%%%%%%%%%%%%%%%%%%% pressures_per_F_unit_14 = ", pressures_per_F_unit_14
pressures_per_F_unit_14_sorted = np.sort(pressures_per_F_unit_14)
print " %%%%%%%%%%%%%%%%%%%%%% np.sort(pressures_per_F_unit_161) ", pressures_per_F_unit_14_sorted
pressures_per_F_unit_14_lin = pressures_per_F_unit_14_sorted


print " %%%%%%%%%%%%%%%%%%%%%% pressures_per_F_unit_C_I = ", pressures_per_F_unit_C_I
pressures_per_F_unit_C_I_sorted = np.sort(pressures_per_F_unit_C_I)
print " %%%%%%%%%%%%%%%%%%%%%% np.sort(pressures_per_F_unit_C_I) ", pressures_per_F_unit_C_I_sorted
pressures_per_F_unit_C_I_lin = pressures_per_F_unit_C_I_sorted

# Linspace for plotting the fitting curves:
P_C_I_lin = np.linspace(pressures_per_F_unit_C_I_lin[0], pressures_per_F_unit_C_I_lin[-1], 10000)
P_14_lin = np.linspace(pressures_per_F_unit_14_lin[0], pressures_per_F_unit_14_lin[-1], 10000)
#P_161_lin = np.linspace(pressures_per_F_unit_161_lin[0], pressures_per_F_unit_161_lin[-1], 10000)

fig_handle = plt.figure()


# Plotting the fitting curves:
p2, = plt.plot(P_C_I_lin, H(P_C_I_lin, *popt_HofP_C_I), color='black', label='Cubic fit Calcite I' )
p6, = plt.plot(P_14_lin, H(P_14_lin, *popt_HofP_14), 'b', label='Cubic fit Calcite II')
#p7, = plt.plot(P_161_lin, H(P_161_lin, *popt_HofP_161), 'brown', label='Cubic fit S.G. 161')

# Plotting the scattered points: 
p1 = plt.scatter(pressures_per_F_unit_C_I, H_C_I, color='red', marker="^", label='Calcite I', s=100)
p5 = plt.scatter(pressures_per_F_unit_14, H_14, color='grey', marker="^", facecolors='none', label='Calcite II', s=100)
#p161 = plt.scatter(pressures_per_F_unit_161, H_161, color='green', marker="^", facecolors='none', label='Calcite II', s=100)


fontP = FontProperties()
#fontP.set_size('small')
fontP.set_size('13')

#plt.legend((p1, p2, p5, p6, p161, p7), ("Calcite I", "Cubic fit Calcite I", "Calcite II", 'Cubic fit Calcite II', 'S.G. 161', 'Cubic fit S.G. 161'), prop=fontP)
plt.legend((p1, p2, p5, p6), ("Calcite I", "Cubic fit Calcite I", "Calcite II", 'Cubic fit Calcite II'), prop=fontP)

global a0, a1, a2, a3
a0     =     popt_HofP_C_I[0] 
a1     =     popt_HofP_C_I[1]
a2     =     popt_HofP_C_I[2]
a3     =     popt_HofP_C_I[3]

global a0_s2, a1_s2, a2_s2, a3_s2
a0_s2        =     popt_HofP_14[0] 
a1_s2        =     popt_HofP_14[1]
a2_s2        =     popt_HofP_14[2]
a3_s2        =     popt_HofP_14[3]

print 'a0 = ', a0
print 'a1 = ', a1
print 'a2 = ', a2
print 'a3 = ', a3

print 'a0_s2 = ', a0_s2
print 'a1_s2 = ', a1_s2
print 'a2_s2 = ', a2_s2
print 'a3_s2 = ', a3_s2


print """ 
The equations are the following:
G_I (P) = a0 + a1*P + a2*P**2 + a3*P**3 
G_II (P) = a0_s2 + a1_s2*P + a2_s2*P**2 + a3_s2*P**3 
"""
print('G_I (P) = ({a0}) + ({a1})*P + ({a2})*P**2 + ({a3})*P**3 '.format(a0 = a0, a1 = a1, a2 = a2, a3 = a3, ))

print """
"""
print('G_II (P) = ({a0_s2}) + ({a1_s2})*P + ({a2_s2})*P**2 + ({a3_s2})*P**3 '.format(a0_s2 = a0_s2, a1_s2 = a1_s2, a2_s2 = a2_s2, a3_s2 = a3_s2))

print """
"""

print """
G_I (P) = G_II (P)
"""
# Set the boundaries for P here:
#P_C_I_lin
#P_14_lin

#z_fit = a0 + a1*P_C_I_lin + a2*P_C_I_lin**2 + a3*P_C_I_lin**3 		
#z_fit_2 = a0_s2 + a1_s2*P_14_lin + a2_s2*P_14_lin**2 + a3_s2*P_14_lin**3  

# Setting "P" to be symbolic:
P = sym.symbols('P') #, real=True)

def z_I(P):
        return   a0 + a1*P + a2*P**2 + a3*P**3 

def z_II(P):
        return   a0_s2 + a1_s2*P + a2_s2*P**2 + a3_s2*P**3 

#sol = sym.solve(z_I(P) - z_II(P) , P)
#print 'sol_ z_I(P) - z_II(P)  =', sol
#
#print 'sol[1] = ', sol[1]
#candidate = sol[2]
#P_real_intersection = re(candidate)
#print 'sol_ H_I(P) - H_II(P)[1]  =', P_real_intersection
#H_real_intersection = z_I(P_real_intersection)

# Crude intersection:
sol = sym.solve(z_I(P) - z_II(P) , P)
print 'sol_ H_I(P) - H_II(P)  =', sol

# Transform to complex notation, in order to
# better discard the complex root afterwards.
# Use of evalf to obtain better precision:

evalf_result_c = [complex(x.evalf()) for x in sol]
print 'evalf_result_c = ', evalf_result_c

#filtered = [i for i in evalf_result_c if i.imag <= 0]
#filtered = [i for i in evalf_result_c if not i.imag == 0]
#filtered = [i for i in evalf_result_c if i.imag == 0] # works
filtered = [i for i in evalf_result_c if i.imag <= 0 or i.imag >= 0] # works
print 'filtered = ', filtered

real_roots = [i.real for i in filtered]
print 'real_roots = ', real_roots

# Transform each element of the list to a numpy array:
real_roots = np.array(real_roots)

for i in real_roots:
 print type(i)

print 'real_roots = ', real_roots

# Let's grab the root located between 0.1GPa and 4GPa (true for CI-CII phase trans.)
real_roots_zero_to_four = real_roots[(real_roots >= 0.1) & (real_roots <= 4.0)]
print 'real_roots_zero_to_four = ', real_roots_zero_to_four

P_real_intersection = real_roots_zero_to_four[0]
H_real_intersection = z_I(real_roots_zero_to_four[0])

T_folder = 0.0

output_array_2 = np.vstack((T_folder, P_real_intersection, H_real_intersection)).T
np.savetxt('P_H_analytic_intersection_T_%sK.dat' %T_folder , output_array_2, header="Temperature (K) \t Pressure_Intersection (GPa) \t H_Intersection = E + PV (a.u.)", fmt="%0.13f")

output_array_3 = np.vstack((T_folder, Intersection[0], Intersection[1])).T
np.savetxt('P_H_collisions_intersection_T_%sK.dat' %T_folder, output_array_3, header="Temperature (K) \t Pressure_Intersection (GPa) \t H_Intersection = E + PV (a.u.)", fmt="%0.13f")

plt.xlabel(r'$P$ (GPa)', fontsize=20)
plt.ylabel(r'$(H = E + PV)$ / F.U. (a.u.)', fontsize=15)
plt.suptitle("PBE-D3, pob-TZVP, SHRINK 8 8, Bipolar 18 18, TOLINTEG 8 18, XXLGRID, TOLDEE 8")
plt.title("(0.87 - 0.98)$V_{eq}$ and (0.98 - 1.08)$V_{eq}$", fontsize=10)
plt.ticklabel_format(useOffset=False)
ax = fig_handle.add_subplot(111)
ax.annotate('Analytic\nIntersection\nP= %g GPa\nG = %g a.u.' %(P_real_intersection, H_real_intersection), xy=(P_real_intersection, H_real_intersection), xytext=(P_real_intersection+2.5767, H_real_intersection-0.05), fontsize=15,
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='purple'),
            )
plt.savefig('calcite_I_and_II_all_2_summary_better_plot_delta_H_exact_expression_with_analytic_intersection.pdf', bbox_inches='tight')
pl.dump(fig_handle,file('sinus.pickle_calcite_I_and_II_all_2_summary_better_plot_delta_H_exact_expression_with_analytic_intersection','w'))

#


plt.show()

