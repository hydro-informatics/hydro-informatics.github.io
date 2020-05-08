---
title: Geospatial software
keywords: QGIS, ArcGIS, SAGA
summary: "Software tools for geospatial analyses."
sidebar: mydoc_sidebar
permalink: geo_software.html
folder: get-started
---

Geospatial analyses (or analytics) use, manipulate and illustrate data from geographic information systems (GIS). GIS data contain  geographically referenced and spatially explicit information of for example gauging stations, terrain elevation, or land use. Efficient processing of geospatial data involves programming methods, where *Python* is an efficient tool. This page presents Desktop software for manual geospatial analyses and the illustration of geospatial data. For geospatial programing, please refer to the section [*Python (geospatial)*](geo_overview.html).

{% include note.html content="Geospatial data are either geographically referenced, pixel-based [rasters](https://en.wikipedia.org/wiki/Raster_graphics) data or vector-based *Esri* [shapefiles](https://en.wikipedia.org/wiki/Shapefile)." %}

## QGIS
For the visualization of geodata (`.shp` and `.tif` files) a GIS software is required and the analyses described on these pages refer to the usage of [*QGIS* ](https://www.qgis.org/en/site/forusers/download.html). This web site uses *QGIS* within the sections on [geospatial programming with *Python*](geo_overview) and [numerical modelling with the ETH Zurich's BASEMENT](bm-pre.html) software.

## ArcGIS Pro
The proprietary software *ArcGIS Pro* represents a powerful tool for any kind of geospatial analysis including web applications. *ArcGIS Pro* is maintained by [ESRI](https://www.esri.com/) and comes with an own [*Python conda Environments*](hypy_install.html).
With the focus on freely available software, the usage of *ArcGIS Pro* and its *Python* environment including the `arcpy` package is just mentioned on this website. 

## Others
There are many other tools for geospatial analyses, which all deserve much more than just being mentioned here. Alas, for practical reasons, this website focuses on the usage of *QGIS*. This is why there is just a absolutely-not-complete list of other GIS tools here:

* [SAGA (System for Automated Geoscientific Analyses)](http://www.saga-gis.org/en/index.html)
* [Mapline](https://mapline.com/)
* [Mapbox](https://www.mapbox.com/)
* [uDig](http://udig.refractions.net/)