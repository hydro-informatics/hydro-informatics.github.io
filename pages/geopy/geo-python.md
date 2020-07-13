---
title: Geospatial analysis
tags: [python, gdal, arcpy, QGIS, raster, shapefile]
keywords: geo-python gdal QGIS
sidebar: mydoc_sidebar
permalink: geo-python.html
folder: geopy
---

*Python* is connected with several libraries providing many open-source and commercial (proprietary) functions for the analyses of geospatial data. This section introduces both, open-source and (briefly) the commercial `arcpy` package. The goal of this section is to provide an understanding of how geospatial data can be used and manipulated with *Python* code. The file manipulation involves logical and algebraic operations, and conversion from and to other geospatial file formats.

{% include requirements.html content="Make sure you understand the basics of *Python*, especially [data types](hypy_pybase.html#var), [error handling](hypy_pyerror.html), [functions](hypy_pyfun.html), and working with external libraries [(modules and packages)](hypy_pckg.html)." %}

{% include tip.html content="<br>1. Start with reading the [Geospatial data](geospatial-data.html) page to understand the underpinnings of any geospatial analysis.<br>2. Use [QGIS](geo_software.html#qgis) to display geospatial data and to create maps in *PDF* or image formats (e.g., *tif*, *png*, *jpg*)." %}

The descriptions of open source packages for geospatial data handling build on explanations from [Michael Diener's *Python Geospatial Analysis Cookbook*](https://github.com/mdiener21/python-geospatial-analysis-cookbook) (open access under MIT license). Therefore, if you want to learn more details about any here information provided, take a look at this comprehensive e-book.

Another excellent source of inspiration with many open-sourced examples is [*pcjericks* github repository *py-gdalogr-cookbook*](https://pcjericks.github.io/py-gdalogr-cookbook/).



