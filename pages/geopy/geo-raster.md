---
title: Geospatial Python - Raster (gridded) data handling
tags: [python, gdal, pandas, geo, geospatial, raster]
keywords: geo-python gdal QGIS
summary: "Geospatial analysis of raster (gridded) data with gdal."
sidebar: mydoc_sidebar
permalink: geo-raster.html
folder: geopy
---


The goal of this page is to provide an understanding of how geospatial data can be used and manipulated with *Python* code. The file manipulation involves logical and algebraic operations, and conversion from and to other geospatial file formats.

{% include note.html content="Make sure to understand [gridded raster data](geospatial-data.html#raster) before reading this section. Recall that we will mostly deal with the `.tif` (*GeoTIFF*) format for grid data and hat many other raster data types exist." %}
{% include tip.html content="While `gdal`'s `ogr` module is useful for shapefile handling, raster data are best handled by `gdal` itself." %}

## Open existing raster data
Raster data can be opened as a `gdal.Open("FILENAME")` object. The following code block provides a function to open any raster specified with the `file_name` input argument. One of the most important elements when dealing with raster data is the `RasterBand`, which takes on a similar data carrier role as `GetLayer` in shapefile handling.
To create this important object, the `open_raster` function:

1. Enables error and warning feedback with `gdal.UseExceptions()` (this step is absolutely vital when using raster data).
1. Opens the provided raster `file_name` embraced by `try` - `except` statements to inform if and why an error occurred while opening the raster.
1. Opens the raster band number stated in the optional `band_number` keyword argument with `raster_band = raster.GetRasterBand(band_number)` (the default value is `1`).
1. Returns the raster and raster band objects.



```python
import gdal


def open_raster(file_name, band_number=1):
    """
    Open a raster file and access its bands
    :param file_name: STR of a raster file directory and name
    :param band_number: INT of the raster band number to open (default: 1)
    :output: osgeo.gdal.Dataset, osgeo.gdal.Band objects
    """
    gdal.UseExceptions()
    # open raster file or return None if not accessible
    try:
        raster = gdal.Open(file_name)
    except RuntimeError as e:
        print("ERROR: Cannot open raster.")
        print(e)
        return None
    # open raster band or return None if corrupted
    try:
        raster_band = raster.GetRasterBand(band_number)
    except RuntimeError as e:
        print("ERROR: Cannot access raster band.")
        print(e)
        return None
    return raster, raster_band
```

To use the `open_raster` function just call it with a file name as shown in the following code block with the `h1000cfs.tif` raster. The script immediately closes the raster again by overwriting it with `None` to avoid that the file is locked afterwards.


```python
import os
file_name = r"" + os.getcwd() + "/geodata/rasters/h1000cfs.tif"
src, depth = open_raster(file_name)
print(src)
print(depth)
depth = None
```

    <osgeo.gdal.Dataset; proxy of <Swig Object of type 'GDALDatasetShadow *' at 0x0000021017DB5D20> >
    <osgeo.gdal.Band; proxy of <Swig Object of type 'GDALRasterBandShadow *' at 0x000002101806F990> >
    


