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

Perhaps this extrapolated version is easier to see that there is a common tangent:

![Data flow](https://github.com/DavidCdeB/Common_Tangent/blob/master/Images_for_README_md/plots_extrap.png)

2) I have implemented this in python (`Common_tangent.py` file) but unfortunately no solution is found
