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



### Step-by-step recipe for 1D (line) plots {#plotxy}

1. Import *matplolib*'s `pyplot` package with `import matplotlib.pyplot as plt`
1. Create a figure with `plt.figure(figsize=(width_inch, height_inch), dpi=int, facecolor=str, edgecolor=str)`
1. Add axes to the figure with `axes=fig.add_subplot(row=int, column=int, index=int, label=str)
1. Generate a [color map](http://matplotlib.org/users/colormaps.html); `plt.cm.getcmap()` generates an array of colors as explained with the [*NumPy* instructions](hypy_pynum.html#colors). For example `colormap=([255, 0, 0])` creates a color map with just one color (red).
1. Plot the data (finally!) to plot  
    * lines with `axes.plot(x, y, linestyle=str, marker=str, color=Colormap(int), label=str)` and many more `**kwargs` can be defined ([go the *matplotlib* docs](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D)).
    * points (markers) with `axes.scatter(x, y, MarkerStyle=str, cmap=Colormap, label=str)` and many more `**kwargs` can be defined ([go the *matplotlib* docs](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.scatter.html))
1. Manipulate the axis ticks
    * `plt.xticks(list)` define x-axis ticks
    * `plt.yticks(list)` define y-axis ticks
    * `axes.set_xlim(tuple(min, max))` sets the x-axis minimum and maximum
    * `axes.set_ylim(tuple(min, max))` sets the y-axis minimum and maximum
    * `axes.set_xlabel(str)` sets the x-axis label
    * `axes.set_ylabel(str)` sets the y-axis label
1. Add legend (optionally) with `axes.legend(loc=str, facecolor=str, edgecolor=str, framealpha=float_between_0_and_1)` and many more `**kwargs` can be defined ([go the *matplotlib* docs](https://matplotlib.org/3.1.1/api/legend_api.html#matplotlib.legend.Legend)).
1. Optional: Save figure with `plt.savefig(fname=str, dpi=int)` with many more `**kwargs` available ([go the *matplotlib* docs](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html)).

The following code block illustrates the plot recipe using [randomly drawn samples from a *Weibull* distribution](https://numpy.org/doc/stable/reference/random/generated/numpy.random.RandomState.weibull.html#numpy.random.RandomState.weibull) with a the distribution shape factor *a* (for *a*=1, the *Weibull* distribution reduces to an exponential distribution). The `seed` argument describes the source of randomness and `seed=None` makes *Python* use randomness from operating system variables.

The code block below makes use of a function called `plot_xy` that requires `x` and `y` arguments and accepts the following optional keyword arguments:
* `plot_type=str` defines if a line or scatter plot should be produced,
* `label=str` sets the legend,
* `save=str` defines a path where the figure should be saved (the figure is not saved if nothing provided). To activate saving a figure write for example `save='C:/temp/weibull.png'`.


```python
import matplotlib.pyplot as plt
import matplotlib.cm as cm
x = np.arange(1, 100)
y = np.random.RandomState(seed=None).weibull(3., x.__len__())

def plot_xy(x, y, plot_type="1D-line", label="Rnd. Weibull", save=""):
    fig = plt.figure(figsize=(6.18, 3.82), dpi=100, facecolor='w', edgecolor='gray')  # figsize in inches
    axes = fig.add_subplot(1, 1, 1, label=label)  # row, column, index, label
    colormap = cm.plasma(np.linspace(0, 1, len(y)))  # more colormaps: http://matplotlib.org/users/colormaps.html
    if plot_type == "1D-line":
        ax = axes.plot(x, y, linestyle="-", marker="o", color=colormap[0], label=label)  # play with the colormap index
    if plot_type == "scatter":
        ax = axes.scatter(x, y, marker="x", color=colormap, label=label)
    if not "ax" in locals():
        print("ERROR: No valid input data provided.")
        return -1
    plt.xticks(list(np.arange(0, x.__len__() + 10, (x.__len__() + 1) / 5.)))
    plt.yticks(list(np.arange(0, np.ceil(y.max()), 0.5)))
    axes.set_xlim((0,100))
    axes.set_ylim((0,2))
    axes.set_xlabel("Linear x data")
    axes.set_ylabel("Scale of " + str(label))
    axes.legend(loc='upper right', facecolor='y', edgecolor='k', framealpha=0.5)
    if save:
        plt.savefig(save)

print("Plot lines")    
plot_xy(x, y)
print("Scatter plot")
plot_xy(x, y, plot_type="scatter", label="Rand. Weibull scattered")
```

    Plot lines
    Scatter plot
    




{% include idea.html content="The `plot_xy` function has some weaknesses. For example if more arguments are provided or `y` data are an array that should produce multiple lines. How can you optimize the `plot_xy` function, to make it more robust and enable multi-line plotting?" %}

### Surface and contour plots

*matplotlib* provides multiple options to plot X-Y-Z data, for example (i.e., there are more options):

* Surface plots with color shades: [`axes.plot_surface(X, Y, Z)`](https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#surface-plots) 
* Contour plots: [`axes.contour(X, Y, Z)`](https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#contour-plots) 
* Contour plots with filled surfaces: [`axes.contourf(X, Y, Z)`](https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#filled-contour-plots) 
* Surface plots with triangulated mesh: [`axes.plot_trisurf(X, Y, Z)`](https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#tri-surface-plots) 
* Three-dimensional scatter plots: [`axes.scatter3D(X, Y, Z)`](https://matplotlib.org/3.1.1/gallery/mplot3d/scatter3d.html) 
* Streamplots (e.g., of velocity vectors): [`axes.streamplot(X, Y, U, V)`](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.streamplot.html) 
* Color-coded representation of gridded values with (annotated) heatmaps (e.g., for habitat suitability index maps): [`axes.imshow(data, **kwargs)`](https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html)

Only streamplots are discussed here, since they are a useful tool for the visualization of velocity vectors (flow fields) in rivers. To generate a streamplot:

1. Create an `X` - `Y` grid, for example with the [*NumPy*'s `mgrid` method](https://numpy.org/doc/stable/reference/generated/numpy.mgrid.html): `Y, X = np.mgrid[range, range]`
1. Assign stream field data (such data can be artificially generated for example as `U` and `V`) to the grid nodes as calculate a scalar value (e.g., `velocity` as a function of the 2-directional field data).
1. Generate figures as before in the `plot_xy` function example (see [above instructions](#plotxy)).

The below code block illustrates the generation of a streamplot (adapted from the [*matplotlib* docs](https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/plot_streamplot.html#sphx-glr-gallery-images-contours-and-fields-plot-streamplot-py)) and uses `import matplotlib.gridspec` to place the subplots in the figure.


```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# generate grid
w = 100
Y, X = np.mgrid[-w:w:10j, -w:w:10j]  # j creates complex numbers

# calculate U and V vector matrices on the grid
U = -2 - X**2 + Y
V = 0 + X - Y**2

fig = plt.figure(figsize=(6., 2.5), dpi=200)
fig_grid = gridspec.GridSpec(nrows=1, ncols=2)
velocity = np.sqrt(U**2 + V**2)  # calculate velocity vector 

#  Varying line width along a streamline
axes1 = fig.add_subplot(fig_grid[0, 0])
axes1.streamplot(X, Y, U, V, density=0.6, color='b', linewidth=3*velocity/velocity.max())
axes1.set_title('Line width variation', fontfamily='Tahoma', fontsize=8, fontweight='bold')

# Varying color along a streamline
axes2 = fig.add_subplot(fig_grid[0, 1])
uv_stream = axes2.streamplot(X, Y, U, V, color=velocity, linewidth=2, cmap='Blues')
fig.colorbar(uv_stream.lines)
axes2.set_title('Color maps', fontfamily='Tahoma', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.show()

```




### Fonts and styles

The previous example already featured font type adjustment for the plot titles (`axes.set_title('title', font ...)`). The font and its characteristics (e.g., size, weight, style, or family) can be defined in a more coherent manner with `matplotlib.font_manager.FontProperties`, where plot font settings can be globally modified within a script.




```python
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rc

# create FontProperties object and set font characteristics
font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')
font.set_style('italic')
font.set_weight('normal')
font.set_size(10)
print("Needs to be converted to a dictionary: " + str(font))
# translate FontProperties to a dictionary
font_dict = {}
[font_dict.update({e.split("=")[0]: e.split("=")[1]}) for e in str(font).strip(":").split(":")]

# apply font properties to script
rc('font', **font_dict)

# make some plot data
x_lin = np.linspace(0.0, 10.0, 1000)  # evenly spaced numbers over a specific interval (start, stop, number-of-elements)
y_osc = np.cos(5 * np.pi * x_lin) * np.exp(-x_lin)

# plot
fig, axes = plt.subplots(figsize=(6.18, 1.8), dpi=150)
axes.plot(x_lin, y_osc, label="Oscillations")
axes.legend()
axes.set_xlabel("Time (s)")
axes.set_ylabel("Oscillation (V)")
plt.tight_layout()
plt.show()
```

    Needs to be converted to a dictionary: :family=Times New Roman:style=italic:variant=normal:weight=normal:stretch=normal:size=10.0
    



Instead of using `rc`, font characteristics can also be updated with *matplotlib*'s `rcParams` *dictionary*. In general, all font parameters can be accessed with `rcParams` along with many more parameters of plot layout options. The parametric options are stored in the [`matplotlibrc`](https://matplotlib.org/tutorials/introductory/customizing.html#customizing-with-matplotlibrc-files) file and can be accessed with `rcParams["matplotlibrc-parameter"]`. Read more about modification options (`"matplotlibrc-parameter"`) in the [*matplotlib* docs](https://matplotlib.org/tutorials/introductory/customizing.html#customizing-with-matplotlibrc-files). In order to modify a (font) style parameter use `rcParams.update({parameter-name: parameter-value})` (which does not always work - for example in [*jupyter*](https://github.com/jupyter/notebook/issues/3385)). 

In addition, many default plot styles are available through [`matplotlib.style`](https://matplotlib.org/api/style_api.html#matplotlib-style) with many [style templates](https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html). The following example illustrates the application of `rcParams` and `style` to the previously generated x-y oscillation dataset.


```python
from matplotlib import rcParams
from matplotlib import rcParamsDefault
from matplotlib import style
rcParams.update(rcParamsDefault)  # reset parameters in case you run this block multiple times
print("Some available serif fonts: " + ", ".join(rcParams['font.serif'][0:5]))
print("Some available sans-serif fonts: " + ", ".join(rcParams['font.sans-serif'][0:5]))
print("Some available monospace fonts: " + ", ".join(rcParams['font.monospace'][0:5]))
print("Some available fantasy fonts: " + ", ".join(rcParams['font.fantasy'][0:5]))

# change rcParams
rcParams.update({'font.fantasy': 'Impact'})  # has no effect here!

print("Some available styles: " + ", ".join(style.available[0:5]))
style.use('seaborn-darkgrid')

# plot
fig, axes = plt.subplots(figsize=(6.18, 1.8), dpi=150)
axes.plot(x_lin, y_osc, label="Oscillations")
axes.legend()
axes.set_xlabel("Time (s)")
axes.set_ylabel("Oscillation (V)")
plt.tight_layout()
plt.show()
```

    Some available serif fonts: DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman, New Century Schoolbook, Century Schoolbook L
    Some available sans-serif fonts: DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana
    Some available monospace fonts: DejaVu Sans Mono, Bitstream Vera Sans Mono, Computer Modern Typewriter, Andale Mono, Nimbus Mono L
    Some available fantasy fonts: Comic Sans MS, Chicago, Charcoal, Impact, Western
    Some available styles: bmh, classic, dark_background, fast, fivethirtyeight
    





### Annotations

Pointing out particularities in graphs is sometimes helpful to explain observations on graphs. Here are some options illustrated with a self-explaining code block.


```python
from matplotlib import rcParams
from matplotlib import rcParamsDefault
from matplotlib import style
rcParams.update(rcParamsDefault)  # reset parameters in case you run this block multiple times

fig, axes = plt.subplots(figsize=(10, 2.5), dpi=150)
style.use('fivethirtyeight')  #  let s just use still another style

fig.suptitle('This is the figure (super) title', fontsize=8, fontweight='bold')

axes.set_title('This is the axes (sub) title', fontsize=8)

axes.text(1, 0.8, 'B-boxed italic text with axis coords 1, 0.8', style='italic', fontsize=8, bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 5})
axes.text(5, 0.6, r'Annotation text with equation: $u=U^2 + V^2$', fontsize=8)
axes.text(7, 0.2, 'Color text with axis coords (7, 0.2)', verticalalignment='bottom', horizontalalignment='left', color='red', fontsize=8)

axes.plot([0.5], [0.2], 'x', markersize=7, color='blue')  #plot an arbitrary point
axes.annotate('Annotated point', xy=(0.5, 0.2), xytext=(2, 0.4), fontsize=8, arrowprops=dict(facecolor='blue', shrink=0.05))

axes.axis([0, 10, 0, 1])  # x_min, x_max, y_min, y_max

plt.show()
```




{% include idea.html content="The above code blocks involve many repetitive statements such as `import ...` - `rcParams.update(rcParamsDefault)`, and `plot.show()` at the end. Can you write a [wrapper function](hypy_pyfun.html#wrappers) to decorate any other *matplotlib* plot function?" %}

## Plotting with *pandas* {#pandas}

Plotting with *matplotlib* can be daunting, not because the library is poorly documented (the complete opposite is the case), but because *matplotlib* is very extensive. *pandas* brings remedy with simplified commands for high-quality plots.


```python

```
