---
title: Python Basics - Plotting
keywords: python
summary: "Use matplotlib, pandas, and plotly to leverage Python's power of data visualization."
sidebar: mydoc_sidebar
permalink: hypy_pyplot.html
folder: python-basics
---

## Tools (packages) for plotting with *Python*

Several packages enable plotting in *Python*. The last page already introduced [*NumPy*](hypy_pynum.html#numpy) and [*pandas*](hypy_pynum.html#pandas) for plotting histograms. *pandas* plotting capacities go way beyond just plotting histograms and it relies on the powerful [*matplotlib*](https://matplotlib.org/) library. *SciPy*'s *matplotlib* is the most popular plotting library in *Python* (since its introduction in 2003) and not only *pandas*, but also other libraries (for example the abstraction layer [*Seaborn*](https://seaborn.pydata.org/)) use *matplotlib* with facilitated commands. This page introduces the following packages for data visualization:

* [*matplotlib*](#matplotlib) - the baseline for data visualization in *Python*
* [*pandas*](#pandas) - as wrapper API of *matplotlib*, with many simplified options for meaningful plots
* [*plotly*](#plotly) - for interactive plots, in which users can change and move plot scales 

## Matplotlib {#matplotlib}

Because of its complexity and the fact that all important functions can be used with *pandas* in a much more manageable way, we will only discuss *matplotlib* only briefly here. Yet it is important to know how *matplotlib* works in order to better understand the baseline of plotting with *Python* and to use more complex graphics or more plotting options when needed.

In 2003, the development of *matplotlib* was initiated in the field of neurobiology by [*John D. Hunter (&dagger;)*](https://en.wikipedia.org/wiki/John_D._Hunter) to emulate *The MathWork*'s *MATLAB&reg;* software. This early development is was constituted the `pylab` package, which is deprecated today for its bad practice of overwriting *Python* (in particular *NumPy*) `plot()` and `array()` methods/objects. Today, it is recommended to use:<br>
`import matplotlib.pyplot as plt`.

### Some terms and definitions
A `plt.figure` can be thought of as a box containing one or more axes, which represent the actual plots. Within the axes, there are smaller objects in the hierarchy such as markers, lines, legends, and text fields. Almost every element of a plot is a manipulable attribute and the most important attributes are shown in the following figure.

{% include image.html file="pyplot-defs.png" alt="pyplot-defs" max-width="500" caption="Python objects (attributes) of a pyplot figure." %} 

### 1D plots
The following code blocks illustrate plot and figure adaptations of [randomly drawn samples from a weibull dsitribution](https://numpy.org/doc/stable/reference/random/generated/numpy.random.RandomState.weibull.html#numpy.random.RandomState.weibull):<br>

<img src="https://render.githubusercontent.com/render/math?math=p(x) = {a}{\lambda}\left({x}{\lambda}\right)^{a-1}\cdot e^{-(x/\lambda)^a}"> <br>

where *a* is the distribution shape (if *a*=1, the Weibull distribution reduces to an exponential distribution), and *&lambda;* is the the scale.


The `seed` argument describes the source of randomness and `seed=None` makes *Python* use randomness from operating system variables.


```python
import matplotlib.pyplot as plt
x = np.arange(1, 100)
random_data = np.random.RandomState(seed=None)  # create 100 random data points
plt.plot(x, random_data.weibull(3., x.__len__()))
```




    [<matplotlib.lines.Line2D at 0x1d4f6e7fc08>]




![png](output_2_1.png)



```python

```

## Plotting with *pandas* {#pandas}

Plotting with *matplotlib* can be daunting, not because the library is poorly documented (the complete opposite is the case), but because *matplotlib* is very extensive. *pandas* brings remedy with simplified commands for high-quality plots.
