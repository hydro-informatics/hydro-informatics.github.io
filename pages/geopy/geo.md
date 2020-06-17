---
title: Geospatial analysis
tags: [python, gdal, arcpy, QGIS, ]
keywords: geo-python gdal QGIS
sidebar: mydoc_sidebar
permalink: geo_overview.html
folder: geopy
---

The *Python* libraries provide many open-source and commercial (proprietary) packages for the analyses of geospatial data.

{% include tip.html content="Start with reading the [Geospatial data](geospatial-data.html) page to understand the underpinnings of any geospatial analysis." %}

Some of the most common open-source packages are:
 * [`gdal`](https://gdal.org/) of the [OSGeo Project](http://www.osgeo.org/) for processing rasters and shapefiles.
 * [`rasterio`](https://rasterio.readthedocs.io/en/latest/) for processing raster data as [`numpy`](https://numpy.org/) arrays ([read more about `numpy` arrays on this web site](hypy_pynum.html)).

In order to use proprietary packages, users often need to purchase licenses to activate (unlock) *Python* packages or functional parts of *Python packages. Some of the most popular propriertary packages are:
 * [`descarteslsbs`](https://docs.descarteslabs.com/api.html) with many free functions, provided by [Descartes Lab](https://www.descarteslabs.com/)
 * [`arcpy`](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy/what-is-arcpy-.htm) without any free functions and an [*ArcGIS Pro* license required from *Esri*](https://pro.arcgis.com/en/pro-app/get-started/about-licensing.htm).
 
 This page introduces the usage of `gdal` and illustrates basic functions of the commercial `arcpy` library.