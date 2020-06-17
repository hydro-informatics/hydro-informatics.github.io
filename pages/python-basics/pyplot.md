---
title: Python Basics - Plotting
tags: [python, matplotlib, pandas, plotting, plotly, matlab]
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

{% include tip.html content="Most of the below illustrated `matplotlib` features are embedded in a plotter script, which is available at the [course repository](https://github.com/hydro-informatics/material-py-codes/raw/master/plotting/plotter.py) (only when the lecture is active)." %}

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
    


![png](images/output_3_1.png)



![png](images/output_3_2.png)


{% include challenge.html content="The `plot_xy` function has some weaknesses. For example if more arguments are provided or `y` data are an array that should produce multiple lines. How can you optimize the `plot_xy` function, to make it more robust and enable multi-line plotting?" %}

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


![png](images/output_6_0.png)


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
    


![png](images/output_8_1.png)


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
    


![png](images/output_10_1.png)


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


![png](images/output_12_0.png)


{% include challenge.html content="The above code blocks involve many repetitive statements such as `import ...` - `rcParams.update(rcParamsDefault)`, and `plot.show()` at the end. Can you write a [wrapper function](hypy_pyfun.html#wrappers) to decorate any other *matplotlib* plot function?" %}

## Plotting with *pandas* {#pandas}

Plotting with *matplotlib* can be daunting, not because the library is poorly documented (the complete opposite is the case), but because *matplotlib* is very extensive. *pandas* brings remedy with simplified commands for high-quality plots. The simplest way to plot a *pandas* data frame is [`pd.DataFrame.plot(x="col1", y="col2")`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html). The following example illustrates this fundamentally simple usage with a river discharge series stored in a workbook.


```python
flow_df = pd.read_excel('data/USGS_11421000_MRY_flows.xlsx', sheet_name='Mean Monthly CMS')
print(flow_df.head(3))
flow_df.plot(x="Date (mmm-jj)", y="Flow (CMS)", kind='line')
```

      Date (mmm-jj)  Flow (CMS)
    0    1997-04-01   59.905234
    1    1997-05-01   33.529035
    2    1997-06-01   19.058182
    3    1997-07-01   28.577362
    4    1997-08-01   53.454656
    




    <matplotlib.axes._subplots.AxesSubplot at 0x1c17af5cfc8>




![png](images/output_15_2.png)


### Pandas and matplotlib

Because *pandas* plot functionality roots in the *matplotlib* library, it can be easily combined, for example to create subplots:


```python
import matplotlib.pyplot as plt
from matplotlib import cm

flow_ex_df = pd.read_excel('data/USGS_11421000_MRY_flows.xlsx', sheet_name='FlowDuration')

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 2.5), dpi=150)
flow_ex_df.plot(x="Relative exceedance", y="Flow (CMS)", kind='area', color='DarkBlue', grid=True, title="Blue area plot", ax=axes[0])
flow_ex_df.plot(x="Relative exceedance", y="Flow (CMS)", kind='scatter', color="DarkGreen", title="Green scatter", marker="x", ax=axes[1])
```




    <matplotlib.axes._subplots.AxesSubplot at 0x26709c37d48>




![png](images/output_17_1.png)


### Boxplots and Error bars
A [box-plot](https://en.wikipedia.org/wiki/Box_plot) graphically represents the distribution of (statistical) scatter and parameters of a data series. Why are box-plots particularly mentioned within the *pandas* plot explanations? Well, the reason is that with *pandas* data frames, we typically load data series with certain statistical properties per column. For example if we run a steady-flow experiment in a hydraulic lab flume with ultrasonic probes for deriving flow depths, we will observe signal fluctuation, even though the flow was steady. By loading the signal data into a *pandas* data frame, we can use a box plot to observe the average flow depth and the noise in the measurement among different probes. Thus, probes with unexpected noise can be identified and repaired. This small example can be applied on a broader scale to many other sensors and for many other purposes (noise does not automatically mean that a sensor is broken). A box-plot has the following attributes:

* *boxes* represent the main body of the data with quartiles and confidence intervals around the median (if activated).
* *medians* are horizontal lines at the median (visually in the middle) of each box.
* *whiskers* are vertical lines that extend to the most extreme, non-outlier data points.
* *caps* are small horizontal line endings of whiskers.
* *fliers* are outlier points beyond whiskers.
* *means* are either points or lines of dataset means.

*pandas* data frames make use of [`matplotlib.pyplot.boxplot`](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.boxplot.html#matplotlib.pyplot.boxplot) to generate box-plots with [`df.boxplot()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.boxplot.html) or `df.plot.box()`. The following example features box-plots of flow depth measurements with ultrasonic probes (sensors 1, 2, 3, and 5) and manipulations of 


```python
us_sensor_df = pd.read_csv("data/FlowDepth009.csv", index_col=0, usecols=[0, 1, 2, 3, 5])
print(us_sensor_df.head(2))
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 2.5), dpi=150)
fontsize = 8.0
labels = ["S1", "S2", "S3", "S5"]

# make plot props dicts
diamond_fliers = dict(markerfacecolor='thistle', marker='D', markersize=2, linestyle=None)
square_fliers = dict(markerfacecolor='aquamarine', marker='+', markersize=3)
capprops = dict(color='deepskyblue', linestyle='-')
medianprops = {'color': 'purple', 'linewidth': 2}
boxprops = {'color': 'palevioletred', 'linestyle': '-'}
whiskerprops = {'color': 'darkcyan', 'linestyle': ':'}

us_sensor_df = us_sensor_df.rename(columns=dict(zip(list(us_sensor_df.columns), labels)))  # rename for plot conciseness
us_sensor_df.boxplot(fontsize=fontsize, ax=axes[0], labels=labels, widths=0.25, flierprops=diamond_fliers,
                     capprops=capprops, medianprops=medianprops, boxprops=boxprops, whiskerprops=whiskerprops)
us_sensor_df.plot.box(color="tomato", vert=False, title="Hz. box-plot", flierprops=square_fliers, 
                      whis=0.75, fontsize=fontsize, meanline=True, showmeans=True, ax=axes[1], labels=labels)
```

              Sensor 1 (m)  Sensor 2 (m)  Sensor 3 (m)  Sensor 5 (m)
    Time (s)                                                        
    0             0.044560      0.044661      0.045216      0.048882
    1             0.043914      0.044215      0.046862      0.049882
    




    <matplotlib.axes._subplots.AxesSubplot at 0x2670a06de08>




![png](images/output_19_2.png)


Box-plots represent the statistical assets of datasets, but box-plots can quickly become confusing when they are presented in technical reports for multiple measurement series. Yet it is state-of-the-art and good practice to present uncertainties in datasets in scientific and non-scientific publications, but somewhat more easily than, for example, with box-plots. To meet the standards of good practice, so-called [error bars](https://en.wikipedia.org/wiki/Error_bar) should be added to data bars. Error bars express the uncertainty of a data set graphically in a simple way by displaying only whiskers. Regardless of whether scatter or bar plot, error bars can easily be added to graphics with *matplotlib* ([read more in the developer's docs](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.errorbar.html)). The following example shows the application of error bars to bar plots of the above ultrasonic sensor data.


```python
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 2.5), dpi=150)
# calculate stats
means = us_sensor_df.mean()
errors = us_sensor_df.std()
# make error bar bar plots
means.plot.bar(yerr=errors, capsize=4, color='palegreen', title="Error bars", width=0.3, fontsize=fontsize, ax=axes[0])
means.plot.barh(xerr=errors, capsize=5, color="lightsteelblue", title="Horizontal error bars", fontsize=fontsize, ax=axes[1])
```




    <matplotlib.axes._subplots.AxesSubplot at 0x267080c7dc8>




![png](images/output_21_1.png)


{% include note.html content="In scatter plots, errors are present in both *x* and *y* directions. For example, the *x*-uncertainty may result from the measurement device precision and *y*-uncertainty can be a result of signal processing. The above error measure in terms of the standard deviation is just an example of error amplitude. To measure and represent uncertainty correctly, always refer to device descriptions and assess precision effects of multiple devices or signal processing by calculating the [propagation of errors](https://en.wikipedia.org/wiki/Propagation_of_uncertainty)." %}

More options for visualizing *pandas* data frame is provided in the [developer's visualization docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html) -  and keep in mind that *matplotlib* can always be well nested in *pandas* plots.

## Interactive plots with *plotly* {#plotly}

The above shown *matplotlib* and *pandas* packages are great for creating static graphs or click-able graphs on a desktop environment. Although interactive plots for web presentations can be created with *matplotlib* ([read more in the docs](https://matplotlib.org/3.1.1/users/interactive.html)), *plotly* leverages many more interactive web plot options within an easy-to-use API library. *plotly* can also handle JSON-like data (hosted somewhere in the internet) to create web applications with *Dash*. However, the company behind (*Plotly*) is a business-oriented 


### Installation
*plotly* is not a default package neither in the *geo-python.yml* environment file nor in the *conda base* environment. Therefore, it must be installed manually with *conda prompt* (or *Conda Navigator* if you prefer the Desktop version). So open *conda prompt* to install *plotly* for :

* *jupyter* usage type with the base environment activated: <br> `conda install plotly` (confirm installation when asked for it) <br> `jupyter labextension install jupyterlab-plotly@4.7.1` (change version `4.7.1` to latest version listed [here](https://github.com/plotly/plotly.py/releases)) <br> optional: `conda install -c plotly chart-studio` (good for other plots than featured on this page)
* *geo-python* (e.g., within *PyCharm*): <br> `conda activate geo-python` <br>  `conda install plotly` (confirm installation when asked for it)
* [Read the trouble shooting info to fix problems with jupyter or *Python*](https://plotly.com/python/troubleshooting/) (there may be some...).

Read more about installing packages within *conda environments* on the [*Python* installation page](https://hydro-informatics.github.io/hypy_install.html#install-pckg). 

### Usage (simple plots)

*plotly* comes with many datasets that can be queried online for showcases. The following example uses one of these datasets (find more at [plotly.com](https://plotly.com/python-api-reference/generated/plotly.express.data.html)).
{% include note.html content="The here used static documentation theme does not feature interactive graphs, which is why the shown *plotly* examples are static. Use the lecture *ipynb* jupyter notebooks to experience the full capacity of interactive *plotly* graphics." %}


```python
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
pyo.init_notebook_mode() 
df = px.data.gapminder().query("continent=='Europe'")
fig = px.line(df, x="year", y="pop", color='country')
# fig.show()
pyo.iplot(fig, filename='population')
```

{% include image.html file="plotly_pop.png" %}


In hydraulics, we often prefer to visualize data in locally stored text files, for example after processing data with *NumPy* or *pandas*. *plotly* works hand in hand with *pandas* and the following example features plotting *pandas* data frames, build from a *csv* file, with *ploty* (better solutions for *pandas* data frame sorting are shown in the [reshaping section](hypy_pynum.html#pd-reshape) of the data handling page). The example uses `plotly.offline` to plot the data in notebook mode (`pyo.init_notebook_mode()`) and `pyo.iplot()` can be used to write the plot functions to a local script for interactive plotting. The *csv* file comes from the *Food and Agriculture Organization of the United Nations* (FAO) data center [FAOSTAT](http://www.fao.org/faostat/en/#data/ET).


```python
import plotly.graph_objects as go
import plotly.offline as pyo
import pandas as pd
pyo.init_notebook_mode()  # activate to create local function script

df = pd.read_csv("data/faostat_temperature_change.csv")

# filter dataframe by country and month
country_filter = "France"  # available in the csv: Austria, Belgium, Finland, France, Germany
month_filter1 = "January"
month_filter2 = "July"

df_country = df[df.Area == country_filter]
df_country_month1 = df[df.Months == month_filter1]
df_country_month2 = df[df.Months == month_filter2]

# define plot type = go.Bar
bar_plots = [go.Bar(x=df_country_month1["Year"], y=df_country_month1["Value"], name=str(month_filter1), marker=go.bar.Marker(color='#86DCEB')),
             go.Bar(x=df_country_month2["Year"], y=df_country_month2["Value"], name=str(month_filter2), marker=go.bar.Marker(color='#EA9285'))]

# set layout
layout = go.Layout(title=go.layout.Title(text="Monthly average surface temperature deviation (ref. 1951-1980) in " + str(country_filter), x=0.5),
                   yaxis_title="Temperature (°C)")

fig = go.Figure(data=bar_plots, layout=layout)

# In local IDE use fig.show() - use iplot(fig) to procude local script for running figure functions
#fig.show(filename='basic-line2', include_plotlyjs=False, output_type='div')
pyo.iplot(fig, filename='temperature-evolution')
```


{% include image.html file="plotly_temp.png" %}


### Interactive map applications
*plotly* uses [*GeoJSON*](https://en.wikipedia.org/wiki/GeoJSON) data formats (an open standard for simple geospatial objects) to implement them into interactive maps. The developers provide many examples in their documentation and the below code block replicates a map representing unemployment rates in the United States. More examples are available at the [developer's web site](https://plotly.com/python/maps/).


```python
import plotly.offline as pyo
from urllib.request import urlopen
import json
import pandas as pd

pyo.init_notebook_mode()  # only necessary in jupyter
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})

import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=2, center = {"lat": 35.0, "lon": -90.0},
                           opacity=0.5,
                           labels={'unemp':'Unemployment rate (%)'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
```

{% include image.html file="plotly_unemp.png" %}

Many more maps are available and some of the require a *Mapbox* account and the creation of a public token (read more at [plotly.com](https://plotly.com/python/mapbox-layers/)).
