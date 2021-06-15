(ex-geco)=
# Script a Habitat Suitability Map

```{admonition} Goals
This exercise guides through the creation of rasters (`osgeo.gdal.Dataset`), the usage of georeferences, raster array calculations, as well as the conversion of a raster to a polygon shapefile and modifications to the shapefile's *Attribute Table* to calculate usable (physical) habitat area. For this purpose, a `Raster` class is written, which enables mathematical operations between its instances through the implementation of magic methods. The exercise also shows how {{ ft_url }} can be used to leverage complex challenges with just a few lines of code.
```

```{admonition} Requirements
:class: attention
*Python* libraries: {ref}`numpy`, {ref}`pandas`, {ref}`gdal`, *geopandas*, *alphashape*, *shapely*, and {ref}`json`. Understand how {ref}`ooc` work as well as {ref}`sec-geo-python`. To visualize results, make sure to install {ref}`qgis-install` and do the {ref}`qgis-tutorial`.
```

Get ready by cloning the exercise repository:

```
git clone https://github.com/Ecohydraulics/Exercise-geco.git
```

```{figure} https://github.com/Ecohydraulics/media/raw/master/jpg/yuba-fish.jpg
:alt: fish Sacramento succer south yuba river
:name: fish

Sacramento suckers in the South Yuba River (source: Sebastian Schwindt 2019).
```


## What is Habitat Suitability?

Fish and other aquatic species rest, orient, and reproduce in a fluvial environment that represents their physical habitat. Throughout their different life stages, different fish have specific physical habitat preferences which are defined, for instance, as a function of water depth, flow velocity, and grain size of the riverbed. The so-called *Habitat Suitability Index *$HSI$** can be calculated for hydraulic (water depth or flow velocity) and morphological (e.g., grain size or cover in the form of large wood) parameters individually to describe the quality of physical habitat for a fish and at a specific life stage. The figure below shows exemplary $HSI$ curves for the fry, juvenile, and adult life stages of rainbow trout as a function of water depth. The $HSI$ curves look different in every river and should be established individually by an aquatic ecologist.

```{figure} https://github.com/Ecohydraulics/media/raw/master/png/hsi-curves.png
:alt: HSI curves examples trout
:name: hsi-image

Habitat Suitability Index $HSI$ curves for the fry, juvenile, and adult life stages of rainbow trout in a cobble-bed river. Take care: HSI curves look different in any river and need to be established by an aquatic ecologist.
```

The $HSI$ concept also accounts for the so-called cover habitat in the form of the *cover Habitat Suitability Index* $HSI_{cov}$. Cover habitat is the result of local turbulence caused by roughness elements such as wood, boulders, or bridge piers. However, in this exercise, we will only deal with hydraulic habitat characteristics (not cover habitat).

![cover-habitat](https://github.com/Ecohydraulics/media/raw/master/jpg/neckar-fish-cover.jpg)<br>
*Adult trout swimming in cover habitat created by a bridge pier in the upper Neckar River.*

The combination of multiple $HSI$ values (e.g., water depth-related $HSI_{h}$, flow velocity-related $HSI_{u}$, grain size-related $HSI_{d}$, and/or cover $HSI_{cov}$) results in the **combined Habitat Suitability Index** $cHSI$. There are various calculation methods for combining different $HSI_{par}$ values into one $cHSI$ value, where the geometric mean and the product are the most widely used deterministic combination methods: <a name="combine-methods"></a>

* Geometric mean:  $cHSI = (\prod_{par} HSI_{par})^{1/n}$
  <br>For example, the combination of the water depth-related $HSI_{h}$ and flow velocity-related $HSI_{u}$ with the geometric mean method is: $cHSI = (HSI_{h} \cdot HSI_{u})^{1/2}$
* Product:  $cHSI = \prod_{par} HSI_{par}$
  <br>For example, the combination of the water depth-related $HSI_{h}$ and flow velocity-related $HSI_{u}$ with the product method is: $cHSI = (HSI_{h} \cdot HSI_{u})$

Therefore, if the pixel-based $HSI$ values for water depth and flow velocity are known from a two-dimensional (2d) hydrodynamic model, then for each pixel the $cHSI$ value can be calculated either as the product or geometric mean of the single-parameter $HSI_{par}$ rasters.

This habitat assessment concept was introduced by {cite:t}`bovee_development_1986` and {cite:t}`stalnaker_instream_1995` ([direct download](https://apps.dtic.mil/sti/pdfs/ADA322762.pdf)). However, these authors built their usable (physical) habitat assessment based on one-dimensional (1d) numerical models that were commonly used in the last millennium. Today, 2d numerical models are the state-of-the-art to determine physical habitat geospatially explicit based on pixel-based $cHSI$ values. There are two different options for calculating the usable habitat area ($UHA$) based on pixel-based $cHSI$ values (and even more options can be found in the scientific literature). <a name="uha-methods"></a>

1. Use a threshold value above which a pixel is classified as a usable habitat.
    * Typical values for the threshold value $cHSI_{crit}$ are between 0.4 (tolerant) and 0.75 (strict).
    * The usable habitat area $UHA$ results from the pixel size $px_{a}$ (e.g., in m$^2$) multiplied by the number of pixels ($px$) where $cHSI > cHSI_{crit}$:
      <br>$UHA = px_{a} \cdot \sum px_{i}(cHSI_{px_{i}} > cHSI_{crit})$
1. Multiply the pixel $cHSI$ value with the pixel size.
    * The pixel area is weighted by its habitat quality expressed by the $cHSI$ value:
    <br>$UHA = px_{a} \cdot \sum cHSI_{px_{i}}$

```{admonition} Weighted Usable Area (WUA) vs. UHA
:class: attention
Some authors (e.g., {cite:t}`yao_development_2018`, {cite:t}`tuhtan_estimating_2012`) incorrectly refer to this weighting as Weighted Usable Area (*WUA*), which conflicts with the original definition of *WUA* {cite:p}`bovee_development_1986`.

 The threshold method is preferable over the weighting method because the $HSI$  has the unit of *Index* and is therefore not dimensionless. As a result, unrealistic units of *Index* areas (e.g., *Index*-m$^2$) are created in the weighting method, which is also introducing non-measurable uncertainty.
```

An alternative to the deterministic calculation of the $HSI$ and $cHSI$ values of a pixel is a fuzzy logic approach {cite:p}`noack_ecohydraulics_2013`. In the fuzzy logic approach, pixels are classified, for instance, as *low*, *medium*, or *high* habitat quality as a function of the associated water depth or flow velocity using categorical (*low*, *medium*, or *high*), expert assessment-based $HSI$ curves. The $cHSI$ value results from the center of gravity of superimposed membership functions of considered parameters (e.g., water depth and flow velocity).

Sustainable river management involves the challenge of designing an aquatic habitat for target fish species at different life stages. The concept of usable physical habitat area represents a powerful tool to leverage the assessment of the ecological integrity of river management and engineering measures. For example, by calculating the usable habitat area before and after the implementation of measures, valuable conclusions can be drawn about the ecological integrity of restoration efforts.

This exercise demonstrates the use of 2d hydrodynamic modeling results to algorithmically evaluate usable habitat area based on the calculation of geospatially explicit $cHSI$ values.


## Available data and code structure

The following flow chart illustrates the provided code and data. Functions, methods, and files to be created in this exercise are highlighted in bold, italic, *YELLOW*-ish font.

```{figure} https://github.com/Ecohydraulics/Exercise-geco/raw/master/graphs/geo_eco_uml.png
:alt: HSI curves examples trout
:name: uml

Structure of the provided template file tree and their relations.
```

The provided QGIS project file `visualize_with_QGIS.qgz` helps to verify input raster datasets and results.

(ecox-2dm)=
### Two-dimensional (2d) Hydrodynamic Modelling (Folder: *BASEMENT*)

This exercise uses (hydraulic) flow velocity and water depth rasters ({term}`GeoTIFF`s) produced with the [ETH Zurich*s BASEMENT](https://basement.ethz.ch/) software. Read more about hydrodynamic modeling with BASEMENT in the {ref}`chpt-basement` chapter. The hydraulic rasters were produced with the BASEMENT developer's [example data from the *Flaz River*](http://people.ee.ethz.ch/~basement/baseweb/download/tutorials/Flaz_2d_v3.zip) in Switzerland ([read more on their website](https://basement.ethz.ch/download/tutorials/tutorials3.html)).
The water depth `water_depth.tif` and flow velocity `flow_velocity.tif` rasters are provided for this exercise in the folder `/basement/`.

(hsi-curves)=
### Habitat Suitability Index HSI Curves (folder: **habitat**)

The `/habitat/` folder in the exercise repository contains $HSI$ curves in the form of an *xlsx* workbook (`trout.xlsx`) and in the form of a {ref}`json` file (`trout.json`). Both files contain the same data for rainbow trout of a hypothetical cobble-bed river and this exercise only uses the {ref}`json` file (the workbook serves for visual verification only).

### Code

```{admonition} GEO_UTILS (Folder: geo_utils)
:class: tip
A couple of `gdal`-based functions for processing rasters and shapefiles were introduced in the lecture. This exercise re-uses some of these functions, which are available in the geo-processing code repository specifically for this ebook. The repository contains a functional block from {{ ft_url }}.geotools (in the `geo_utils` folder) that enables to better understand and modify the behavior of {{ ft_url }}.
Even though already provided in this exercise, make sure that the *geo_utils* repository is well implemented in the exercise directory (i.e., *geo_utils* scripts are stored in a folder tree like this: `Exercise-geco\geo_utils\`). The `\geo_utils\` folder corresponds to the `geo-utils\geo_utils\` directory when you clone the repository.

Make sure that in the `\geo_utils\geoconfig.py` file, the `nan_value` is defined as 0.0 (`nan_value = 0.0`).
```

````{admonition} CONFIG.PY
:class: tip
The code in this exercise uses a `config.py` file where all necessary libraries and global variables are loaded centrally.

```python
# This is config.py

import os
import logging
import random
import shutil
import string
import json

import numpy as np
import pandas as pd

import geo_utils as geo

cache_folder = os.path.abspath("") + "\\__cache__\\"
par_dict = {"velocity": "u",
            "depth": "h",
            "grain_size": "d"}
nan_value = 0.0
```
````

````{admonition} FUN.PY (FUNCTIONS)
:class: tip
At this point in the course, it is assumed that students are familiar with object orientation and especially with writing functions. Therefore, many basic functions for this exercise are already provided with the script `fun.py` (alphabetically ordered list):
<a name="funs"></a>

* `cache` is a wrapper for parent functions to enforce that intermediate geospatial datasets (e.g., the intermediate product of a sum of rasters) are stored in a temporary *cache* folder that is deleted after the script ran.
* `check_cache` verifies if the cache folder defined in `config.py` already exists. The function is automatically called by the `cache` wrapper.
* `create_random_string(length)` generates unique file names for temporary (cached) datasets, where `length` is an {ref}`integer <num>` value that determines the number of characters of the random string to be created.
* `interpolate_from_list(x_values, y_values, xi_values)` linearly interpolates $y_{i}$ values from two sorted lists containing paired *x* and *y* values for a {ref}`list` of given $x_{i}$ values (returns a `numpy.array` of the same length as `xi_values`). If one of the $x_{i}$ values is beyond the value range of `x_values`, the function appends the `nan_value` defined in `config.py` to the results array.
* `interpolate_y(x1, x2, y1, y2, xi)` is called by the `interpolate_from_list` function for paired lower and upper `x1`-`y1` and `x2`-`y2` {ref}`float <num>`s of the `x_values` and `y_values` {ref}`list`s (returns a {ref}`float <num>` number corresponding to the linearly interpolated `yi` value of the `xi`-`yi` pair between `x1`-`y1` and `x2`-`y2`). If `xi` is not numeric, or if the interpolation results in a `ZeroDivisionError`, the function returns the `nan_value` defined in `config.py`.
* `log_actions(fun)` wraps a function (`fun`), where actions should be written to a logfile. Logging is started with the `start_logging` function (see below) and logging is stopped with `logging.shutdown()`.
* `read_json` opens a {ref}`json` file and returns it as *Python* object. In this exercise, this function will be used to open the `/habitat/trout.json` file. The $HSI$ values can then be assessed from the {ref}`json` object, for example:

```python
trout = read_json("PATH/" + "trout.json")
print(trout["velocity"]["spawning"][0]["u"])

>>> 0.0198
```

* `remove_directory(directory)` removes a `directory` (*string* argument). Be careful, this function aggressively removes the `directory` and all its contents with little chance of data recovery.
* `start_logging()` starts logging to a logfile (`logfile.log`) and the *Python* console at the `logging.DEBUG` level.
````

```{admonition} RASTER.PY / RASTER_HSI.PY
:class: tip
The parent `Raster` class is stored in the `raster.py` script, where magic methods, a *pseudo* private `_make_raster`, and a `save` method will be created in this exercise.
The `HSIRaster` class in the `raster_hsi.py` script is a child of the `Raster` class. In this exercise, we will only look at how this child class is structured and what it produces (i.e., no modifications are necessary).
```

```{admonition} CREATE_HSI_RASTERS.PY / CALCULATE_HABITAT_AREA.PY
:class: tip
The two scripts `reate_hsi_rasters.py` and `calculate_habitat_area.py` represent the focal point of this exercise and make use of the provided data and *Python* scripts. Therefore, only the basic framework functions and imports are pre-existing in these two template scripts.
```

(py-raster-calculator)=
## Create and Combine HSI Rasters

(raster-class)=
### Complete the `__init__` Method of the `Raster` Class (`raster.py`)

The `raster.py` script imports the functions and libraries loaded in the `fun.py` script, and therefore, also the `config.py` script. For this reason, the {ref}`numpy` and {ref}`pandas` libraries are already available (`as` `np` and `pd`, respectively), and the *geo_utils* package is already imported as `geo` (`import geo_utils as geo` in `config.py`).

The `Raster` class will load any *GeoTIFF* file name as a geo-referenced array object that can be used with mathematical operators. First, we will complement the `__init__` method by a `Raster.name` (extract from the `file_name` argument), as well as georeferences and array datasets:

```python
    # __init__(...) of Raster class in raster.py
        self.name = file_name.split("/")[-1].split("\\")[-1].split(".")[0]
```

If the provided `file_name` does not exist, the `__init__` method creates a new raster with the `file_name` (this behavior is already implemented in the `if not os.path.exists(file_name)` statement.
Next, load the `osgeo.gdal.dataset`, the `np.array`, and the `geo_transformation` of the raster. For this purpose, use the {ref}`raster2array function <createarray>` from this ebook, which is also implemented in the exercise's *geo_utils* (`geo`) package:

```python
    # __init__(...) of Raster class in raster.py
        self.dataset, self.array, self.geo_transformation = geo.raster2array(file_name, band_number=band)
```

To identify the {ref}`EPSG number (Authority code) <prj>` of a raster, retrieve the spatial reference system (*SRS*) of the raster. Also for this purpose we have already developed a function in the lecture with the `get_srs` form the {ref}`theory section on reprojection <re-project>`. Load the *SRS* and the *EPSG* number using the *get_srs* function with the following two lines of code in the `__init__` method:

```python
    # __init__(...) of Raster class in raster.py
        self.srs = geo.get_srs(self.dataset)
        self.epsg = int(self.srs.GetAuthorityCode(None)
```

The `__init__` method of the `Raster` class is complete.

### Complete Magic Methods of the `Raster` Class (`raster.py`)

To enable mathematical operations between multiple instances of the `Raster` class, implement {ref}`magic` that tell the class what to do when two `Raster` instances are for example added (`+` sign), multiplied (`*` sign), or subtracted (`-` sign). For instance, implementing the magic methods `__truediv__` (for using the `/` operator), `__mul__` (for using the `*` operator), and `__pow__` (for using the `**` operator) will enable the usage of `Raster` instances like this:

```python
# example for Raster instances, when operators are defined through magic methods

# load GeoTIFF rasters from file directory
velocity = Raster("/usr/geodata/u.tif")
depth = Raster("/usr/geodata/h.tif")

# calculate the Froude number using operators defined with magic methods
Froude = velocity / (depth * 9.81) ** 0.5

# save the new raster
Froude.save("/usr/geodata/froude.tif")
```

The `Raster` class template already contains one exemplary magic method to enable division (`__truediv__`):

```python
    # Raster class in raster.py
    def __truediv__(self, constant_or_raster):
        try:
            self.array = np.divide(self.array, constant_or_raster.array)
        except AttributeError:
            self.array /= constant_or_raster
        return self._make_raster("div")
```

Here is what the `__truediv__` method does:

* The input argument `constant_or_raster` can be another `Raster` instance that has an `array` attribute or a numeric constant (e.g., 9.81).
* The method tries to invoke the array attribute of `constant_or_raster`.
    - If `constant_or_raster` is a raster object, then invoking `contant_or_raster.array` is successful. In this case `self.array` is overwritten with the element-wise division of the array by `contant_or_raster.array`. The element-wise division builds on {ref}`numpy`s built-in function [*np.divide*](https://numpy.org/doc/stable/reference/generated/numpy.divide.html), which is a computationally efficient wrapper of C/C++ code (much faster than a *Python* loop over array elements).
   - If `constant_or_raster` is a numeric value, then invoking `contant_or_raster.array` results in an `AttributeError` and the `__truediv__` method falls in the `except AttributeError` statement, where `self.array` is simply divided by `constant_or_raster`.
* The method returns the result of the pseudo private method `self._make_raster("div")` ([recall *PEP 8* {ref}`chpt-style`, which corresponds to a new `Raster` instance of the actual `Raster` instance divided by `constant_or_raster`. The new `Raster` instance is a temporary *GeoTIFF*  file in the *cache* folder ([recall the cache function](#funs)). This is how the pseudo-private method `_make_raster(self, file_marker)` looks like:<a name="make-raster"></a>

```python
    def _make_raster(self, file_marker):
        f_ending = "__{0}{1}__.tif".format(file_marker, create_random_string(4)
        geo.create_raster(cache_folder + self.name + f_ending, self.array, epsg=self.epsg,
                          nan_val=nan_value,
                          geo_info=self.geo_transformation)
        return Raster(cache_folder + self.name + f_ending)
```

This function:
* Uses the *string*-type argument `file_marker` to add it to the file name of the base *GeoTIFF* along with a random, four characters-long *string* (recall the [`create_random_string` function](#funs)). `file_marker` is unique for every implemented operator. For the `__truediv__` method use `file_marker="div"`. Thus, the temporary *GeoTIFF* file name is defined as `cache_folder + self.name + f_ending` (e.g. `"C:\Excercise-geco\__cache__\velocity__divhjev__.tif"`).
* Applies the {ref}`create-raster` function from `geo_utils` to write the temporary *GeoTIFF* to the `__cache__` folder with the original raster's spatial reference system.
* `return`s a new `Raster` instance of the temporary, cached *GeoTIFF* file.

````{admonition} If you find the _make_raster method confusing...
:class: tip, dropdown
Then you have a point. The above-described approach implements the `_make_raster` method to reuse the temporary *GeoTIFF*s later with both constants ({ref}`float <num>`) and arrays, but there is a more elegant way to return a new `Raster` instance. However, returning a new instance of the same class requires that the input argument must be an instance of the class itself (i.e., `Raster`) and not a numeric variable. The alternative solution for returning a `Raster` instance starts with a different implementation of the magic method (e.g., `__truediv__`) and requires importing *Python4*-style `annotations`. Therefore, the first line of the script must include (only works with *Python 3.7* and higher) the following import:

```python
from __future__ import annotations
```

Then we can rewrite the `__truediv__` method:

```python
    def __truediv__(self, other: Raster) -> Raster:
        f_ending = "__div%s__.tif" % create_random_string(4)
        return Raster(file_name=cache_folder + self.name + f_ending,
                      raster_array=np.divide(self.array, other.array),
                      epsg=self.epsg,
                      geo_info=self.geo_transformation)
```

In this case, the `_make_raster` method is obsolete. Read more about returning instances of the same class on [stack overflow](https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel).
````

When using the `_make_raster` method, add the following magic methods to the `Raster` class (function placeholders are already present in the `raster.py` template):

* `__add__` (`+` operator):
```python
        try:
            self.array += constant_or_raster.array
        except AttributeError:
            self.array += constant_or_raster
        return self._make_raster("add")
```

* `__mul__` (`*` operator):
```python
        try:
            self.array = np.multiply(self.array, constant_or_raster.array)
        except AttributeError:
            self.array *= constant_or_raster
        return self._make_raster("mul")
```

* `__pow__` (`**` operator):
```python
        try:
            self.array = np.power(self.array, constant_or_raster.array)
        except AttributeError:
            self.array **= constant_or_raster
        return self._make_raster("pow")
```

* `__sub__` (`-` operator):
```python
        try:
            self.array -= constant_or_raster.array
        except AttributeError:
            self.array -= constant_or_raster
        return self._make_raster("sub")
```

The last item to complete in the `Raster` class is the built-in `save` method that receives a `file_name` (*string*) argument defining the directory and save-as name of the `Raster` instance:

```python
        save_status = geo.create_raster(file_name, self.array, epsg=self.epsg, nan_val=0.0, geo_info=self.geo_transformation)
        return save_status
```
Why do we need the `save_status` variable? First, it states if saving the raster was successful (`save_status=0`), and second, this information could be used to delete the raster from the `__cache__` folder and flush the memory (feel free to do so for speeding up the code).


### Write HSI and cHSI Raster Creation Script
The provided `create_hsi_rasters.py` script already contains required package imports, an `if __name__ == '__main__'` stand-alone statement as well as the void `main`, `get_hsi_curve`, `get_hsi_raster`, and `combine_hsi_rasters` functions:<a name="chsi-template"></a>

```python
# create_hsi_rasters.py
from fun import *
from raster_hsi import HSIRaster, Raster
from time import perf_counter

def combine_hsi_rasters(raster_list, method="geometric_mean"):
    """...
    """
    pass


def get_hsi_curve(json_file, life_stage, parameters):
    """...
    """
    pass


def get_hsi_raster(tif_dir, hsi_curve):
    """...
    """
    pass


def main():
    pass


if __name__ == '__main__':
    # define global variables for the main() function
    parameters = ["velocity", "depth"]
    life_stage = "juvenile"
    fish_file = os.path.abspath("") + "\\habitat\\trout.json"
    tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
            "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
    hsi_output_dir = os.path.abspath("") + "\\habitat\\"

    # run code and evaluate performance
    t0 = perf_counter()
    main()
    t1 = perf_counter()
    print("Time elapsed: " + str(t1 - t0)

```

The `if __name__ == '__main__'` statement contains a time counter (`perf_counter`) that prompts how long the script takes to run (typically between 3 to 6 seconds). Make sure that

* the `parameters` list contains `"velocity"` and `"depth"` (as per the `par_dict` in the `config.py` script),
* the file paths are defined correctly, and
* a life stage is defined (i.e., either `"fry"`, `"juvenile"`, `"adult"`, or `"spawning"` as per the */habitat/fish.xlsx*  workbook).

The following paragraphs show step by step how to load the $HSI$ curves from the {ref}`json` file (`get_hsi_curve`), apply them to the `flow_velocity` and `water_depth` rasters (`get_hsi_raster`), and combine the resulting $HSI$ rasters into $cHSI$ rasters (`combine_hsi_rasters`).

The `get_hsi_curve` function will load the $HSI$ curve from the {ref}`json` file (*/habitat/trout.json*) in a dictionary for the two parameters `"velocity"` and `"depth"`. Thus, the goal is to create a `curve_data` dictionary that contains one {ref}`pandas` `DataFrame` object for all parameters (i.e., velocity and depth). For example, `curve_data["velocity"]["u"]` will be a {ref}`pandas` `Series` of velocity entries (in m/s) that corresponds to `curve_data["velocity"]["HSI"]`, which is a {ref}`pandas` `Series` of $HSI$ values. Similarly, `curve_data["depth"]["h"]` is a {ref}`pandas` `Series` of depth entries (in meters) that corresponds to `curve_data["depth"]["HSI"]`, which is a {ref}`pandas` `Series` of $HSI$ values (corresponds to the curves shown in the [$HSI$ graphs](#hsi-image) above). To extract the desired information from the {ref}`json` file, `get_hsi_curve` takes three arguments (`json_file`, `life_stage`, and `parameters`) in order to:

* Get the information stored in the {ref}`json` file with the `read_json` function ([see above](#funs)).
* Instantiate a void `curve_data` {ref}`dict` that will contain the {ref}`pandas` `DataFrame`s for `"velocity"` and `"depth"`.
* Run a loop over the (two) parameters (`"velocity"` and `"depth"`), in which it:
    - Creates a void `par_pairs` {ref}`list` for storing pairs of parameter (`par`) - $HSI$ values as nested lists.
    - Iterates through the length of provided curve data, where valid data pairs (e.g., `[u_value, HSI_value]`) are appended to the `par_pairs` {ref}`list`. This iteration is what actually creates the nested {ref}`list`.
    - Converts the final `par_pairs` list to a {ref}`pandas` `DataFrame` that it adds to the `curve_data` {ref}`dict`.
* `return` the `curve_data` {ref}`dict` with its {ref}`pandas` `DataFrame`s.

```python
# create_hsi_rasters.py
def get_hsi_curve(json_file, life_stage, parameters):
    # read the JSON file with fun.read_json
    file_info = read_json(json_file)
    # instantiate output dictionary
    curve_data = {}
    # iterate through parameter list (e.g., ["velocity", "depth"])
    for par in parameters:
        # create a void list to store pairs of parameter-HSI values as nested lists
        par_pairs = []
        # iterate through the length of parameter-HSI curves in the JSON file
        for i in range(0, file_info[par][life_stage].__len__():
            # if the parameter is not empty (i.e., __len__ > 0), append the parameter-HSI (e.g., [u_value, HSI_value]) pair as nested list
            if str(file_info[par][life_stage][i]["HSI"]).__len__() > 0:
                try:
                    # only append data pairs if both parameter and HSI are numeric (floats)
                    par_pairs.append([float(file_info[par][life_stage][i][par_dict[par]]),
                                      float(file_info[par][life_stage][i]["HSI"])])
                except ValueError:
                    logging.warning("Invalid HSI curve entry for {0} in parameter {1}.".format(life_stage, par)
        # add the nested parameter pair list as pandas DataFrame to the curve_data dictionary
        curve_data.update({par: pd.DataFrame(par_pairs, columns=[par_dict[par], "HSI"])})
    return curve_data
```

In the `main` function, call `get_hsi_curves` to get the $HSI$ curves as a {ref}`dict`. In addition, implement the `cache` and the `log_actions` wrappers  ([recall the descriptions of provided functions](#funs) for the `main` function:

```python
# create_hsi_rasters.py

...

@log_actions
@cache
def main():
    # get HSI curves as pandas DataFrames nested in a dictionary
    hsi_curve = get_hsi_curve(fish_file, life_stage=life_stage, parameters=parameters)

...
```

With the provided `HSIRaster` (`raster_hsi.py`) class, the $HSI$ rasters can be conveniently created in the `get_hsi_raster` function. Before using the `HSIRaster` class, make sure to understand how it works. The `HSIRaster` class inherits from the `Raster` class and initiates its parent class in its `__init__` method through `Raster.__init__(self, file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)`. Then, the class calls its `make_hsi` method, which takes an $HSI$ curve (nested {ref}`list`) of two equal {ref}`list` pairs ({ref}`list` of parameters and {ref}`list` of $HSI$ values) as argument. The `make_hsi` method:

* Extracts parameter values (e.g., depth or velocity) from the first element of the nested `hsi_curves` {ref}`list`, and $HSI$ values from the second element of the nested `hsi_curves` {ref}`list`.
* Uses {ref}`numpy`s built-in `np.nditer` function, which iterates through {ref}`numpy` arrays with high computational efficiency (read more about [`nditer`](https://numpy.org/doc/stable/reference/generated/numpy.nditer.html)).
    - The `nditer` loop passes the `par_values` as `x_values` {ref}`list` argument and the `hsi_values` as `y_values` {ref}`list` arguments to the `interpolate_from_list` function ([recall the function descriptions above](#funs)).
    - The array values (i.e., flow velocity or water depth) correspond to the `xi_values` {ref}`list` argument of the `interpolate_from_list` function.
    - The `interpolate_from_list` function then identifies for each element of the `xi_values` {ref}`list` the closest elements ($x_{i}$ values) in the `x_values` {ref}`list` and the corresponding positions in the `y_values` {ref}`list`.
    - The `interpolate_from_list` function passes the identified values to the `interpolate_y` function, which then linearly interpolates the corresponding `yi` value (i.e., an $HSI$ value).
    - Thus, the flow velocity or water depths in `self.array` are row-wise (row-by-row) replaced by $HSI$ values.
* `return`s a `Raster` instance using the pseudo-private `_make_raster` method ([recall its contents](#make-raster)).

```python
# raster_hsi.py
from raster import *

class HSIRaster(Raster):
    def __init__(self, file_name, hsi_curve, band=1, raster_array=None, geo_info=False):
        Raster.__init__(self, file_name=file_name, band=band, raster_array=raster_array, geo_info=geo_info)
        self.make_hsi(hsi_curve)

    def make_hsi(self, hsi_curve):
        par_values = hsi_curve[0]
        hsi_values = hsi_curve[1]
        try:
            with np.nditer(self.array, flags=["external_loop"], op_flags=["readwrite"]) as it:
                for x in it:
                    x[...] = interpolate_from_list(par_values, hsi_values, x)
        except AttributeError:
            print("WARNING: np.array is one-dimensional.")
        return self._make_raster("hsi")
```

Modify the `get_hsi_rasters` function to directly return a `HSIRaster` object:

```python
# create_hsi_rasters.py

...

def get_hsi_raster(tif_dir, hsi_curve):
    return HSIRaster(tif_dir, hsi_curve)
...

```

The `get_hsi_raster` function requires two arguments, which it must receive from the `main` function. For this reason, iterate over the `parameters` {ref}`list` in the `main` function and extract the corresponding raster directories from the `tifs` {ref}`dict` (recall the variable definition in the [standalone statement](#chsi-template)). In addition, save the `Raster` objects returned by the `get_hsi_raster` function in another {ref}`dict` (`eco_rasters`) to combine them in the next step into a $cHSI$ raster.

```python
# create_hsi_rasters.py

...

@log_actions
@cache
def main():
    # get HSI curves as pandas DataFrames nested in a dictionary
    hsi_curve = get_hsi_curve(fish_file, life_stage=life_stage, parameters=parameters)

        # create HSI rasters for all parameters considered and store the Raster objects in a dictionary
    eco_rasters = {}
    for par in parameters:
        hsi_par_curve = [list(hsi_curve[par][par_dict[par]]),
                         list(hsi_curve[par]["HSI"])]
        eco_rasters.update({par: get_hsi_raster(tif_dir=tifs[par], hsi_curve=hsi_par_curve)})
        eco_rasters[par].save(hsi_output_dir + "hsi_%s.tif" % par)
...
```

Of course, one can also loop over the parameters {ref}`list` directly in the `get_hsi_raster` function.

```{admonition} Test if the code works
:class: tip
This is a good moment to test if the code works. Run `create_hsi_rasters.py` and verify that the two *GeoTIFF* files (*/habitat/hsi_velocity.tif* and */habitat/hsi_depth.tif*) are created correctly. QGIS visualizes the *GeoTIFF*-products and the activated *Identify Features* button in QGIS enables to check if the linearly interpolated $HSI$ values agree with the $HSI$ curves in the provided workbook (*/habitat/trout.xlsx*). Thus, load both *GeoTIFF* pairs in QGIS: */habitat/hsi_velocity.tif* + */basement/flow_velocity.tif* and */habitat/hsi_depth.tif*  + */basement/water_depth.tif*.
```

Next, we come to the reason why we had to define magic methods for the `Raster` class: combine the $HSI$ rasters using both combination formulae presented above (recall the [product and geometric mean](#combine-methods) formulae), where `"geometric_mean"` should be used by default. The `combine_hsi_rasters` function accepts two arguments (a {ref}`list` of `Raster` objects corresponding to $HSI$ rasters and the `method` to use as *string*).

If the method corresponds to the default value `"geometric_mean"`, then the `power` to be applied to the product of the `Raster` {ref}`list` is calculated from the *n*th root, where *n* corresponds to the number of `Raster` objects in the `raster_list`. Otherwise (e.g., `method="product"`), the `power` is exactly 1.0.

The `combine_hsi_rasters` function initially creates an empty $cHSI$ `Raster` in the `cache_folder`, with each cell having the value `1.0` (filled through `np.ones`). In a loop over the `Raster` elements of the `raster_list`, the function multiplies each $HSI$ raster with the $cHSI$ raster.

Finally, the function returns the product of all $HSI$ rasters to the power of the previously determined `power` value.


```python
# create_hsi_rasters.py
def combine_hsi_rasters(raster_list, method="geometric_mean"):
    if method is "geometric_mean":
        power = 1.0 / float(raster_list.__len__()
    else:
        # supposedly method is "product"
        power = 1.0

    chsi_raster = Raster(cache_folder + "chsi_start.tif",
                         raster_array=np.ones(raster_list[0].array.shape),
                         epsg=raster_list[0].epsg,
                         geo_info=raster_list[0].geo_transformation)
    for ras in raster_list:
        chsi_raster = chsi_raster * ras

    return chsi_raster ** power
```

To finish the `create_hsi_rasters.py` script, implement the call to the `combine_hsi_rasters` function in the `main` function and save the result as $cHSI$ *GeoTIFF* raster in the `/habitat/` folder:

```python
# create_hsi_rasters.py

...

@log_actions
@cache
def main():
    ...

    for par in parameters:
        hsi_par_curve = [list(hsi_curve[par][par_dict[par]]),
                         list(hsi_curve[par]["HSI"])]
        eco_rasters.update({par: get_hsi_raster(tif_dir=tifs[par], hsi_curve=hsi_par_curve)})
        eco_rasters[par].save(hsi_output_dir + "hsi_%s.tif" % par)

    # get and save chsi raster
    chsi_raster = combine_hsi_rasters(raster_list=list(eco_rasters.values(),
                                      method="geometric_mean")
    chsi_raster.save(hsi_output_dir + "chsi.tif")
...
```

### Run the HSI and cHSI Code

A successful run of the script `create_hsi_rasters.py` should look like this (in *PyCharm*):

```{figure} https://github.com/Ecohydraulics/Exercise-geco/raw/master/graphs/run_create_chsi_rasters.png
:alt: run execute script calculation combined habitat suitability index raster map
:name: run-chsi

A Windows Python console running the above-created scripts.
```

Plotted in QGIS, the $cHSI$ {term}`GeoTIFF` raster should look like this:

```{figure} https://github.com/Ecohydraulics/Exercise-geco/raw/master/graphs/ex-chsi.png
:alt: chsi calculation
:name: chsi-results

The cHSI raster plotted in QGIS, where poor physical habitat quality (cHSI close to 0.0) is colored in red and high physical habitat quality (cHSI close to 1.0) is colored in green.
```

### Result Interpretation
The presentation of the $cHSI$ raster shows that preferred habitat areas for juvenile trout exist only close to the banks. Also, numerical artifacts of the triangular mesh used by {ref}`chpt-basement` are visible. Therefore, the question arises whether the calculated flow velocities and water depths, and in consequence also the $cHSI$ values, close to the banks can be considered representative.

## Calculate Usable Habitat Area UHA

### Write the Code
The $cHSI$ rasters enable the calculation of the available usable habitat area. The previous section featured examples using the fish species *trout* and its *juvenile* life stage, for which we will determine here the usable habitat area $UHA$ (in m$^2$) using a $cHSI$ threshold value (rather than the pixel area weighting approach). So we follow the [threshold formula described above](#uha-methods), using a threshold value of $cHSI_{crit} = 0.4$. Thus, every pixel that has a $cHSI$ value of 0.4 or greater counts as usable habitat area.

From a technical point of view, this part of the exercise is about converting a raster into a polygon shapefile as well as accessing and modifying the *Attribute Table* of the shapefile.

Similar to the creation of the $cHSI$ raster, there is a template script available for this part of the exercise, called `calculate_habitat_area.py`, which contains package and module imports, an `if __name__ == '__main__'` stand-alone statement, as well as the void `main` and `calculate_habitat_area` functions. The template script looks like this:<a name="uha-template"></a>

```python
# this is calculate_habitat_area.py (template)
from fun import *
from raster import Raster


def calculate_habitat_area(layer, epsg):
    pass


def main():
    pass


if __name__ == '__main__':
    chsi_raster_name = os.path.abspath("") + "\\habitat\\chsi.tif"
    chsi_threshold = 0.4

    main()
```

In the `if __name__ == '__main__'` statement, make sure that the global variable `chsi_raster_name` corresponds to the directory of the $cHSI$ raster created in the previous section. The other global variable (`chsi_threshold`) corresponds to the $cHSI_{crit}$ value of 0.4 that we will use with the [threshold formula](#uha-methods).

In the `main` function, start with loading the $cHSI$ raster (`chsi_raster`) as a [Raster object](#raster-class). Then, access the {ref}`numpy` array of the $cHSI$ raster and compare it with `chsi_threshold` using {ref}`numpy`s built-in [*greater_equal*](https://numpy.org/doc/stable/reference/generated/numpy.greater_equal.html) function. `np.greater_equal` takes an array as first argument and a second argument, which is the condition that can be a numeric variable or another {ref}`numpy` array. Then, `np.greater_equal` checks if the elements of the first array are greater than or equal to the second argument. In the case of the second argument being an array, this is an element-wise $\geq$ comparison. The result of `np.greater_equal` is a {ref}`bool` array (`True` where the greater-or-equal condition is fulfilled and `False` otherwise). However, to create an `osgeo.gdal.Dataset` object from the result of `np.greater_equal`, we need a numeric array. For this reason, multiply the result of `np.greater_equal` by 1.0 and assign it as a new {ref}`numpy` array of zeros (`False`) and ones (`True`) to a variable named `habitat_pixels` (see the code block below).

With the `habitat_pixels` array and the georeference of `chsi_raster`, create a new {ref}`integer <num>` *GeoTIFF* raster with the *create_raster* function (also available in [flusstools.geotools](https://flusstools.readthedocs.io/en/latest/geotools.html#module-flusstools.geotools.raster_mgmt)); here, use `geo.create_raster`. In the following code block the new raster is saved in the */habitat/* folder of the exercise as `habitat-pixels.tif`.

```python
# calculate_habitat_area.py
...

def main():
    # open the chsi raster
    chsi_raster = Raster(chsi_ras_name)
    # extract pixels where the physical habitat quality is higher than the user threshold value
    habitat_pixels = np.greater_equal(chsi_raster.array, chsi_threshold_value) * 1
    # write the habitat pixels to a binary array (0 -> no habitat, 1 -> usable habitat)
    geo.create_raster(os.path.abspath("") + "\\habitat\\habitat-pixels.tif",
                      raster_array=habitat_pixels,
                      epsg=chsi_raster.epsg,
                      geo_info=chsi_raster.geo_transformation)
...
```

In the next step, convert the habitat pixel raster into a polygon shapefile and save it in the */habitat/* folder as `habitat-area.shp`. The conversion of a raster into a polygon shapefile requires that the raster contains only {ref}`integer <num>` values, which is the case in the habitat pixel raster (only zeros and ones - recall {ref}`raster2polygon`). Use the `raster2polygon` function in the *geo_utils* folder (package) to create the new polygon shapefile, specify *habitat-pixels.tif* as `raster_file_name` to be converted, and `/habitat/habitat-area.shp` as output file name. The `geo.raster2polygon` function returns an `osgeo.ogr.DataSource` object and we can pass its layer including the information of the EPSG authority code (from `chsi_raster`) directly to the not-yet-written `calculate_habitat_area()` function:

```python
# calculate_habitat_area.py
...

def main():
    ... (create habitat pixels raster)

    # convert the raster with usable pixels to polygon (must be an integer raster!)
    tar_shp_file_name = os.path.abspath("") + "\\habitat\\habitat-area.shp"
    habitat_polygons = geo.raster2polygon(os.path.abspath("") + "\\habitat\\habitat-pixels.tif",
                                          tar_shp_file_name)

    # calculate the habitat area (will be written to the attribute table)
    calculate_habitat_area(habitat_polygons.GetLayer(), chsi_raster.epsg)
...
```

For the `calculate_habitat_area()` function to produce what its name promises, we need to populate this function as well. For this purpose, use the `epsg` {ref}`integer <num>` argument to identify the unit system of the shapefile.


```python
# calculate_habitat_area.py
...

def calculate_habitat_area(layer, epsg):
    # retrieve units
    srs = geo.osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    area_unit = "square %s" % str(srs.GetLinearUnitsName()
...
```

```{note}
In practice, many mistakes are made due to the incorrect use of area units, which is often not obvious at first because of the size of geospatial data (several gigabytes). There are many units of length and area (meters, feet, acre, hectare, km$^2$) and a difference of an order of magnitude is sometimes only noticed when a critical reviewer or a local expert becomes suspicious. In the application shown here, we use the information of the length units only to output the total area with a correct reference to the area units (m$^2$) on the console, but in practice, this information can save a career.
```

To determine the habitat area, the area of each polygon must be calculated. For this purpose, add a new field to the `layer` in the *Attribute Table*, name it `"area"`, and assign a `geo.ogr.OFTReal` (numeric) data type (recall how to [create a field an data types explained in the lecture notes](geopy/geo-shp.html#add-field)).
Then, create a void {ref}`list` called `poly_size`, in which we will write the area of all polygons that have a field value of `1`. To access the individual polygons (features) of the `layer`, iterate through all features using a `for` loop, which:

* Extracts the polygon of every `feature` using `polygon = feature.GetGeometryRef()`
* Appends the polygon's area size to the `poly_size` {ref}`list` if the field `"value"` of the `polygon` (at position 0: `feature.GetField(0)`) is 1 (`True`).
* Writes the polygon's area size to the *Attribute Table*  with `feature.SetField("area", polygon.GetArea()`.
* Saves the changes (calculated area) to the shapefile `layer` with `layer.SetFeature(feature)`.

```{admonition} C/C++ efficiency in Python
:class: attention
Looping through an attribute table is computationally expensive in *Python*. If a shapefile has many elements (points, lines, polygons), this loop can last for hours, days, or even weeks. Therefore, it can be useful to convert a shapefile into a raster and perform calculations using {ref}`numpy`s computationally efficient built-in functions (C/C++ wrappers), which are many times faster. A particular problem is the processing of large lidar datasets (several million points), where it may be necessary to use other software (read more at [earthdatascience.org](https://www.earthdatascience.org/courses/use-data-open-source-python/data-stories/what-is-lidar-data/explore-lidar-point-clouds-plasio/)).
```

The last information needed after the `for` loop is the total area of the `"value"=1` polygons, which we get by writing the `sum` of the `poly_size` {ref}`list` to the console. Therefore, the second and last part of the `calculate_habitat_area` function looks like this:

```python
# calculate_habitat_area.py
...
def calculate_habitat_area(layer, epsg):

    ... (extract unit system information)

    # add area field
    layer.CreateField(geo.ogr.FieldDefn("area", geo.ogr.OFTReal)

    # create list to store polygon sizes
    poly_size = []

    # iterate through geometries (polygon features) of the layer
    for feature in layer:
        # retrieve polygon geometry
        polygon = feature.GetGeometryRef()
        # add polygon size if field "value" is one (determined by chsi_treshold)
        if int(feature.GetField(0):
            poly_size.append(polygon.GetArea()
        # write area to area field
        feature.SetField("area", polygon.GetArea()
        # add the feature modifications to the layer
        layer.SetFeature(feature)

    # calculate and print habitat area
    print("The total habitat area is {0} {1}.".format(str(sum(poly_size), area_unit)

...
```

```{note}
To calculate other geometry attributes than the polygon area (e.g., envelope extents, derive a convex hull, or get the length of lines), refer to the {ref}`calc` section and use those functions in lieu of `polygon.GetArea()`.
```

### Run the Usable Habitat Area calculation code

A successful run of the script `calculate_habitat_area.py` should look like this (in *PyCharm*):

```{figure} https://github.com/Ecohydraulics/Exercise-geco/raw/master/graphs/run_habitat_area.png
:alt: calculate usable habitat area Python gdal
:name: ran-chsi

Successful run of the *calculate_habitat_area.py* script.
```

Plotted in QGIS, the *habitat-area* shapefile looks like this (use *Categorized* symbology):

```{figure} https://github.com/Ecohydraulics/Exercise-geco/raw/master/graphs/ex-uha.png
:alt: calculate usable habitat area Python gdal map raster QGIS
:name: uha-results

The habitat-area shapefile plotted in QGIS with Categorized symbology, where the usable habitat area $UHA$ ($cHSI >$ 0.4) is delineated by the hatched purple patches and their dashed outlines.
```

### Result interpretation
The $UHA$ of the analyzed river section represents a very small share of the total wetted area, which can be interpreted as an ecologically poor status of the river. However, a glance at a map and the simulation files of the Flaz example of BASEMENT suggests that at a discharge of 50 m$^3$/s, a flood situation can be assumed. As during floods, there are generally higher flow velocities, which are out-of-favor of juvenile fish, the small usable habitat area is finally not surprising.


```{attention}
Remember that the here presented habitat assessment assumes that fish prefer regions with high $cHSI$ values and that rivers with a high proportion of areas with high $cHSI$ values are ecologically particularly valuable. This approach represents an assessment of the physical habitat state with limited information on the functional habitat state.
```

```{admonition} Homework
HOMEWORK 1: Rewrite the magic methods of the `Raster` class by using `def __METHOD__(self, other: Raster) -> Raster:` instead of `def __METHOD__(self, constant_or_raster):` and the `_make_raster` method.

HOMEWORK 2: Abandon (delete) the *geo_utils* folder and replace the `import  geo_utils as geo` with `import flusstools.geotools as geo`
```
