# Statement of the problem

Say we have two curves `f(x)` and `g(x)`:

![Data flow](https://github.com/DavidCdeB/Common_Tangent/blob/master/Images_for_README_md/x1x2_small.png)

the slope of the common tangent can be obtained as:

```slope of common tangent = (f(x1) - g(x2)) / (x1 - x2) = f'(x1) = g'(x2)```

So that in the end we have a system of 2 equations with 2 unknowns:

```
f'(x1) = g'(x2) # Eq. 1
(f(x1) - g(x2)) / (x1 - x2) = f'(x1) # Eq. 2
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

2) I have solved Eqn 1 and E1n 2 in python (`Common_tangent.py` file): 

```
    def F(x):
        x1, x2 = x[0], x[1]
        E1 = P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3]) - P(x2, popt_14[1], popt_14[2], popt_14[3])
        E2 = ((BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - BM(x2, popt_14[0], popt_14[1], popt_14[2], popt_14[3])) / (x1 - x2)) - P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
        return [E1, E2]
    
    print fsolve(F, [50, 60])    # some reasonable initial point
```

and the following solution is found: 

    [ 62.96385617  62.89017591]

which are the values of `x1` and `x2`. Now, the slope of the common tangent can be obtained going to Eqn 1:

    slope_common_tangent = P(x1, popt_C_I[1], popt_C_I[2], popt_C_I[3])
    print 'slope_common_tangent = ', slope_common_tangent

this prints:

    slope_common_tangent =  -0.00528373464093

We know that the common tangent passes through the `x1` point, and we know its slope. Thus, we can use the following equation:

    y - y1 = m * (x -x1)

to sort out the common tangent equation (where `m` is the slope).

Since:

    y1 = f(x1)
    m = f'(x1) =  slope_common_tangent

then the common tangent equation is:

    def comm_tangent(x, x1, slope_common_tangent):
       return BM(x1, popt_C_I[0], popt_C_I[1], popt_C_I[2], popt_C_I[3]) - slope_common_tangent * x1 + slope_common_tangent * x         

If we plot it:

    xp = np.linspace(54, 68, 100)
    plt.plot(xp, comm_tangent(xp, x1, slope_common_tangent))
                    

Unfortunately this is not the common tangent:

![Data flow](https://github.com/DavidCdeB/Common_Tangent/blob/master/Images_for_README_md/plots_extrap.png)

