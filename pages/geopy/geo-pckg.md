---
title: Geospatial Python - Open Source Packages
tags: [python, gdal, pandas, geo, geospatial, shapefile, raster, anaconda, descartes]
keywords: geo-python gdal QGIS
sidebar: mydoc_sidebar
permalink: geo-pckg.html
folder: geopy
---


This section lists open-source packages for geospatial file manipulation with *Python*. Except for `gdal` these packages are neither installed in the [`hypy`](hypy_install.html#create-and-install-conda-environments) nor in the *conda* `base` environment. The following sections explain relevant packages for this course and how those can be installed.

{% include callout.html content="The proprietary license-requiring `arcpy` package is described on the [Commercial software](geo-arcpy.html) page." %}

## gdal {#gdal}
[`gdal`](https://gdal.org/) and `ogr` of the [OSGeo Project](http://www.osgeo.org/) stem from the *GDAL* project, which is part of the Open Source
Geospatial Foundation ([*OSGeo*](https://www.osgeo.org)) -  the developers of *QGIS*. `gdal` provides many methods to convert geospatial data (file types, projections, derive geometries), where `gdal` itself handels [raster data](geospatial-data.html#raster) and its `ogr` module handles [vector data](geospatial-data.html#vector). This page primarily uses `gdal` and `ogr`; so it is important to get the installation of `gdal` right.

To install `gdal` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge gdal
```

{% include note.html content="If you **cannot `import gdal`**, for some apparently arbitrary reasons (e.g., `Error: Arbitrary-like stuff is missing.`), the problem probably lies in the definition of environmental variables. The problem can be trouble-shot in *PyCharm* with the following solution<br><br>
 1. Go to *File* > *Settings ...*  > *Build, Execution, Deployment* > *Console* > *Python Console* > *Environment variables* <br>
 2. Set the following `environment_variables`<br> 
     `setx GDAL_DATA 'C:\Program Files\GDAL\gdal-data'`<br>
     `setx GDAL_DRIVER_PATH 'C:\Program Files\GDAL\gdalplugins'`<br>
     `setx PROJ_LIB 'C:\Program Files\GDAL\projlib'`<br>
     `setx PYTHONPATH 'C:\Program Files\GDAL\'`<br><br>
 Wait a couple of moments until *PyCharm* adapted (*building skeleton ...*) the new `environment_variables` and `import gdal` - should work now." %}

{% include unix.html content="In general, the installation of `gdal` in only an environment can be *tricky*. Therefore, *Linux* users may want to make a global installation with:<br>
 1. `sudo apt-get install -y build-essentiallibxml2-dev libxslt1-dev` (install build and *XML* tools) <br>
 2. `sudo apt-get install libgdal-dev` (install `gdal` development files) <br>
 3. `sudo apt-get install python-gdal` (install `gdal` itself) <br>
 4. To enable `gdal` in a virtual environment:<br>
     - run virtual wrapper: `toggleglobalsitepackages` <br>
     - activate environment with `conda activate ENVIRONMENT` <br>
     - activate global site packages for the current environment: `toggleglobalsitepackages enable global site-packages`" %}

## geojson
[`geojson`](https://pypi.org/project/geojson/) is the most direct option for handling [*GeoJSON*](geospatial-data.html#geojson) data.
To install `geojson` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge geojson
```

## descartes
Even though of proprietary origin, the [`descartes`](https://docs.descarteslabs.com/api.html) package (developed and maintained by [*Descartes Labs*](https://www.descarteslabs.com/)) comes with many open-sourced functions. Moreover, *Decartes Labs* hosts the showcase platform [*GeoVisual Search*](https://search.descarteslabs.com/) with juicy illustrations of aritificial intelligence (*AI*) applications in geoscience. To install `descartes` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge descartes 
```

## Python Imaging Library (PIL) / *pillow*
Processing images with *Python* is enabled with the *Python Imaging Library* (*PIL*). *PIL* supports many image file formats, and has efficient graphics processing capabilities.
The `pillow` library is a user-friendly *PIL* fork and provides `Image*` modules (e.g., `Image`, `ImageDraw`, `ImageMath`, and many more).

The comprehensive `pillow` documentation is available at [readthedocs.io](https://pillow.readthedocs.io/en/stable/). To install `pillow` in a *conda* environment  open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:

```python
conda install -c anaconda pillow 
```


## pyshp and (or) shapely
For [shapefile](geospatial-data.html#shp) handling, [`pyshp`](https://pypi.org/project/pyshp/) provides pure *Python* code (rather than wrappers), which simplifies direct dealing with shapefile in *Python*. To install `pyshp` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge pyshp
```

However, the latest release of `pyshp` is from February 2019, which is a good reason to look for a currently maintained alternative. Another good and very well documented option for shapefile handling is [`shapely`](https://shapely.readthedocs.io/). To install `shapely` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge shapely
```

## Other packages
Besides the above mentioned packages there are other useful libraries for geospatial analyses in *Python*:
 * [`rasterio`](https://rasterio.readthedocs.io/en/latest/) for processing raster data as [`numpy`](hypy_pynum.html#numpy) arrays install in *Anaconda Prompt* with `conda install -c conda-forge rasterio`). 
 * [`rasterstats`](https://pythonhosted.org/rasterstats/) produces zonal statistics of rasters and can interact with *GeoJSON* files (install in *Anaconda Prompt* with `conda install -c conda-forge rasterstats`).
 * [`sckit-image`](https://scikit-image.org/) for machine learning applied to georeferenced images.
 * [`django`](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/) as a geographic web frame and for database connections (install in *Anaconda Prompt* with `conda install -c anaconda django`).
 * [`postgresql`](https://www.postgresqltutorial.com/postgresql-python/) for SQL database connections (install in *Anaconda Prompt* with `conda install -c anaconda postgresql`).
 * [`owslib`](http://geopython.github.io/OWSLib/) to connect with *Open Geospatial Consortium* (*OGC*) web services (install in *Anaconda Prompt* with `conda install -c conda-forge owslib`)
