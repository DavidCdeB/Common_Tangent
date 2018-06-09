#

# Table of Contents

<!-- - [What is the QHA program ?](#WhatisQHA)
- [What is the quasi-harmonic approximation ?](#Whatisquasi) -->
1. [What is the `Common_Tangent` program ?](#example)
2. [What is the quasi-harmonic approximation ?](#example2)
3. [Power of the quasi-harmonic approximation](#example3)
4. [Why is `QHA_2D` useful ?](#example4)
5. [Files needed for running `QHA_2D`](#example5)
6. [How to run `QHA_2D`](#example6)
7. [Test](#example7)
8. [How to cite](#example8)
9. [Contributing](#example9)


<a name="example"></a>
## What is the QHA program ?

 `Common_Tangent` is a program for computational chemistry and physics that
performs the quasi-harmonic approximation reading the frequencies at each volume calculated with [CRYSTAL](http://www.crystal.unito.it/index.php).

* Extracts all the frequencies within all the **k** points in the supercell for a given volume.

* Calculates the Helmholtz free energy.

* Evaluates the common tangent between two 
Helmholtz free energy curves corresponding to two different polymorphs: 
<a href="https://www.codecogs.com/eqnedit.php?latex=F^{I}(V;T)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F^{I}(V;T)" title="F^{I}(V;T)" /></a> and <a href="https://www.codecogs.com/eqnedit.php?latex=F^{II}(V;T)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F^{II}(V;T)" title="F^{II}(V;T)" /></a>

* Outputs the pressure-temperature phase diagram for the thermodynamic phase stability of both solid phases:

<!--<img  align="center" src="https://github.com/DavidCdeB/QHA_2D/blob/master/Images_for_README_md/PT_phase_Boundary_edit.png" width="256" height="256" title="Github Logo"> -->
<p align="center">
  <img src="https://github.com/DavidCdeB/Common_Tangent/blob/master/Images_for_README_md/common_tangent_presentatione.png">
</p>


* The underlying criteria for producing this phase boundary is
by evaluating common tangent between two Hemholtz free energy curves
<a href="https://www.codecogs.com/eqnedit.php?latex=F^{I}(V;T)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F^{I}(V;T)" title="F^{I}(V;T)" /></a> and <a href="https://www.codecogs.com/eqnedit.php?latex=F^{II}(V;T)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F^{II}(V;T)" title="F^{II}(V;T)" /></a>


# Statement of the problem

Say we have two curves `f(x)` and `g(x)`:

the slope of the common tangent can be obtained as:

```slope of common tangent = (f(x1) - g(x2)) / (x1 - x2) = f'(x1) = g'(x2)```

So that in the end we have a system of 2 equations with 2 unknowns:

```
f'(x1) = g'(x2) # Eqn. 1
(f(x1) - g(x2)) / (x1 - x2) = f'(x1) # Eqn. 2
```
We would have to solve this system of 2 non-linear equations and 2 unknowns.

The 1st answer in the following link solves this on Mathematica, for the case of `f(x)` and `g(x)` being quadratic:
https://stackoverflow.com/questions/8592200/mathematica-tangent-of-two-curves

1) Does this work for this case:

![Data flow](https://github.com/DavidCdeB/Common_Tangent/blob/master/Images_for_README_md/plots_names.png)

where `f(x)` and `g(x)` are cubic? (`1.dat` and `2.dat` Energy vs Volume files provided in this repository). 

It can be seen that you can draw a common tangent with a pen on the screen.

Perhaps in this extrapolated version is easier to see that there is a common tangent:

![Data flow](https://github.com/DavidCdeB/Common_Tangent/blob/master/Images_for_README_md/plots_extrap.png)

2) I have solved Eqn 1 and Eqn 2 in python (`Common_tangent.py` file): 

```
def BM(x, a, b, c, d):
         return  a + b*x + c*x**2 + d*x**3

def devBM(x, b, c, d):
         return  b + 2*c*x + 3*d*x**2

from scipy.optimize import fsolve
def equations(p):
    x1, x2 = p
    E1 = devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - devBM(x2, popt_14[1], popt_14[2], popt_14[3])
    E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
    return (E1, E2)

x1, x2 =  fsolve(equations, (50, 60))
print 'x1 = ', x1
print 'x2 = ', x2

```

and the following solution is found: 

```
x1 =  61.445411835
x2 =  59.9942936344
```
Now, the slope of the common tangent can be obtained going to Eqn 1:

```
slope_common_tangent = devBM(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
print 'slope_common_tangent = ', slope_common_tangent
slope_common_tangent_GPa = abs(slope_common_tangent * 4.3597482E+3)
print ' slope_common_tangent_GPa = ', slope_common_tangent_GPa
```
Which yields:

> slope_common_tangent =  -0.000438955769096

> slope_common_tangent_GPa =  1.91373662419

We know that the common tangent passes through the `x1` point, and we know its slope. Thus, we can use the following equation:

    y - y1 = m * (x -x1) # Eqn.3 

to sort out the common tangent equation (where `m` is the slope).

Since:

    y1 = f(x1)
    m = f'(x1) =  slope_common_tangent

then the common tangent equation is:

```
def comm_tangent(x, x1, slope_common_tangent):
   return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - slope_common_tangent * x1 + slope_common_tangent * x
```
```
x = var('x')
print comm_tangent(x, x1, slope_common_tangent)
```
> Common tangent equation: -0.000438955769095521*x - 941.227540709767

![Data flow](https://github.com/DavidCdeB/Common_Tangent/blob/master/Images_for_README_md/slope.png)

