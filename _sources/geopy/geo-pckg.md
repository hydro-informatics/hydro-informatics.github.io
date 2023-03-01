# Geospatial Open Source Python Libraries

This section lists open-source packages for geospatial file manipulation with Python. The necessary packages are already installed {{ ft_url }}. In addition, the following paragraphs provide explanations of relevant and optional packages for this eBook and how those can be installed.

```{admonition} arcpy / ArcGIS
:class: attention
The proprietary license-requiring `arcpy` package is briefly described in the chapter on the commercial {ref}`arcpy library <chpt-arcpy>`. However, this eBook strongly recommends using the open-source libraries, such as `gdal`.
```

```{admonition} Watch this Section on YouTube
:class: tip, dropdown
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/iQaJztGhp7w" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Watch this section as a video on the <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics channel on YouTube</a>.</p>
```

(gdal)=
## OSGeo and GDAL Including ogr and osr

The [gdal](https://gdal.org/) library for {ref}`raster data handling <raster>` comes along with [ogr](https://gdal.org/faq.html?highlight=ogr) for {ref}`vector data handling <vector>`, and [osr](https://gdal.org/python/osgeo.osr-module.html) for geospatial referencing. GDAL and OGR are managed and developed by the [OSGeo Project](http://www.osgeo.org/), which is part of the Open Source Geospatial Foundation - the developers of {ref}`qgis-install`.

The tutorials in this eBook build on `gdal` and `ogr` (including `osr` for spatial referencing), which is why it is important to get the installation of `GDAL` right:

* **Linux** users may follow the instructions for installing `gdal` and {{ ft_url }} with {ref}`pip and venv <pip-env>`.
* **Windows** users preferably install `gdal` and {{ ft_url }} in a {ref}`conda environment <conda-env>` through Anaconda.


Select your platform for more specific installation instructions:

````{tabbed} Linux / pip

GDAL requires sudo-installation. Find more details in the {ref}`Python installation instructions <pip-env>` of this eBook.

````

````{tabbed} Windows / conda
To install `GDAL` for Python through {ref}`Anaconda Prompt <install-pckg>` enter:

```python
conda install -c conda-forge gdal
```
````

````{admonition} Import GDAL, ogr, and osr from OSGeo
:class: important

Importing `gdal`, `ogr`, and `osr` directly (e.g., `import gdal`) is deprecated since GDAL v3. Therefore, `gdal`, `ogr`, and `osr` must be imported from `osgeo`:

```python
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
```
````

(geojson-pckg)=
## geojson
The [geojson](https://pypi.org/project/geojson/) library is the most direct option for handling {ref}`geojson` data and is also already installed along with {{ ft_url }}.

````{tabbed} Linux / pip
To install `geojson`, open *Terminal* and type:

```python
pip install geojson
```
````

````{tabbed} Windows / conda
To install `geojson` for Python Anaconda, open {ref}`Anaconda Prompt <install-pckg>` and type:

```python
conda install -c conda-forge geojson
```
````

(descartes)=
## Descartes Labs
Even though of proprietary origin, the [`descarteslabs`](https://docs.descarteslabs.com/api.html) library (developed and maintained by [Descartes Labs](https://www.descarteslabs.com/)) comes with many open-sourced functions. Moreover, Descartes Labs hosts the showcase platform [GeoVisual Search](https://search.descarteslabs.com/) with juicy illustrations of artificial intelligence (AI) applications in geoscience. Note that `descarteslabs` is not installed along with {{ ft_url }}.

````{tabbed} Linux / pip
To install `descarteslabs`, open Terminal and type:

```python
pip install descarteslabs
```
````

````{tabbed} Windows / conda
To install `descarteslabs` for Python, open {ref}`Anaconda Prompt <install-pckg>` and type:

```python
conda install -c conda-forge descartes
```

If the installation fails, try the following:

```python
conda install shapely
pip install descarteslabs
```
````

## Python Imaging Library (PIL) / pillow
Processing images with Python is enabled with the *Python Imaging Library* (*PIL*). *PIL* supports many image file formats and has efficient graphics processing capabilities. The `pillow` library is a user-friendly *PIL* fork and provides `Image*` modules (e.g., `Image`, `ImageDraw`, `ImageMath`, and many more). If {{ ft_url }} is installed, no further action is required for working with the *PIL*/*pillow*-related contents of this eBook.

Note that the `conda base` environment includes `PIL` (test with `import PIL`), which needs to be uninstalled before installing `pillow`. For installing *PIL*/*pillow*, refer to [https://pillow.readthedocs.io](https://pillow.readthedocs.io/en/stable/installation.html).

## shapely

A preferable and very well documented package for {ref}`shp` handling is [`shapely`](https://shapely.readthedocs.io/). `shapely` is already installed along with {{ ft_url }}.

````{tabbed} Linux / pip
To install `shapely`, open Terminal and type:

```python
pip install Shapely
```
````

````{tabbed} Windows / conda
To install `shapely` for Python Anaconda, open {ref}`Anaconda Prompt <install-pckg>` and type:

```python
conda install -c conda-forge shapely
```
````


## pyshp
[pyshp](https://pypi.org/project/pyshp/) is another {ref}`shapefile <shp>` handling package, which builds on pure Python code (rather than wrappers) to simplify direct dealing with shapefiles in Python. `pyshp` is already installed along with {{ ft_url }}.

````{tabbed} Linux / pip
To install `pyshp`, open Terminal and type:

```python
pip install pyshp
```
````

````{tabbed} Windows / conda
To install `pyshp` for Python Anaconda, open {ref}`Anaconda Prompt <install-pckg>` and type:

```python
conda install -c conda-forge pyshp
```
````

(other-geo-pckgs)=
## Other packages

Besides the above-mentioned packages, there are other useful libraries for geospatial analyses with Python (**`Packages in bold red font`** are installed along with {{ ft_url }}):

 * [**`alphashape`**](https://pypi.org/project/alphashape/) creates bounding polygons containing a set of points.
 * [django](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/) as a geographic web frame and for database connections.
 * [**`geopandas`**](https://geopandas.org/) enables the application of {ref}`pandas` data frame operations to geospatial datasets.
 * [NetworkX](https://networkx.github.io/documentation/stable/index.html) for network analyses such as finding a least-cost / shortest path between two points.
 * [owslib](http://geopython.github.io/OWSLib/) to connect with *Open Geospatial Consortium* (OGC) web services.
 * [postgresql](https://www.postgresqltutorial.com/postgresql-python/) for SQL database connections.
 * [**`rasterio`**](https://rasterio.readthedocs.io/en/latest/) for processing raster data as {ref}`numpy` arrays.
 * [**`rasterstats`**](https://pythonhosted.org/rasterstats/) produces zonal statistics of rasters and can interact with {ref}`geojson` files.
 * [**`sckit-image`**](https://scikit-image.org/) for machine learning applied to georeferenced images.
