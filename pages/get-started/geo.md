---
title: Geospatial software
tags: [qgis, gdal, arcpy, basement, geo, geospatial]
keywords: QGIS, ArcGIS, SAGA
summary: "Software tools for geospatial analyses."
sidebar: mydoc_sidebar
permalink: geo_software.html
folder: get-started
---

Geospatial analyses (or analytics) use, manipulate and illustrate data from geographic information systems (GIS). GIS data contain  geographically referenced and spatially explicit information of for example gauging stations, terrain elevation, or land use. Efficient processing of geospatial data involves programming methods, where *Python* is an efficient tool. This page presents Desktop software for manual geospatial analyses and the illustration of geospatial data. For geospatial programming, please refer to the section [*Python (applications) > GEOSPATIAL*](geo_overview.html).

{% include note.html content="Geospatial data are either geographically referenced, pixel-based [rasters](https://en.wikipedia.org/wiki/Raster_graphics) data or vector-based *Esri* [shapefiles](https://en.wikipedia.org/wiki/Shapefile) (read more on the [*Python (applications) > GEOSPATIAL*](geospatial-data.html) pages)." %}

## QGIS {#qgis}
For the visualization of geodata (`.shp` and `.tif` files) a GIS software is required and the analyses described on these pages refer to the usage of [*QGIS*](https://www.qgis.org). This web site uses *QGIS* within the sections on [geospatial programming with *Python*](geo_overview) and [numerical modelling with the ETH Zurich's BASEMENT](bm-pre.html) software.

### Install QGIS on Windows
Download and install the latest version of [*QGIS*](https://www.qgis.org/en/site/forusers/download.html) for Windows.

### Install QGIS on Linux
The *QGIS* developers provide detailed installation instructions for several *Linux* distributions, but the instructions will not satisfy all requirement for the use of *QGIS* described on *hydro-informatics.github.io*. Therefore, install *QGIS* as follows:

1. Install QGIS v3.12 either from the [*Flatpak* web site](https://flathub.org/apps/details/org.qgis.qgis) or using the *Linux* *Software Manager* (open *Software Manager*, search for *QGIS* and install the *QGIS Flatpak*). If *Software Manager* cannot find *QGIS*, make sure that *Flatpak* is added as repository (*Software Source*). The good repository for many Linux distributions can be found on the [*Flatpak web site*](https://flatpak.org/setup/)).
1. The *QGIS Flatpak* installation will most likely not include the important *scipy* module. In order to fix this issue, open  *Terminal* (standard Linux application) and type: 
<br>`flatpak run --command=pip3 org.qgis.qgis install scipy --user`

This solution has been tested on *Linux Ubuntu* and *Linux Mint*. It potentially also works with *Red Hat*, *openSUSE*, *Mac OS*, *Arch*, *Fedora*, *Android*, *Debian*, *Kubuntu* and [many more](https://flatpak.org/setup/). Read more about the *QGIS Flatpak* installation on the [*QGIS web site*](https://qgis.org/en/site/forusers/alldownloads.html#flatpak).


### Install QGIS on macOS
{% include warning.html content="If you plan to use BASEMENT for numerical modelling: BASEMENT will not run on macOS." %}

Download and install the latest version of [*QGIS*](https://www.qgis.org/en/site/forusers/download.html) for macOS. The integrity of using macOS for the applications on *hydro-informatics.github.io* is has not yet been tested. Possible trouble-shooting with *Python* is provided by [kyngchaos.com](https://www.kyngchaos.com/software/qgis/). 


## ArcGIS Pro {#agis}
{% include warning.html content="ArcGIS Pro is designed for Windows and will not run on macOS or Linux. In addition, a license needs to be purchased." %} 
The proprietary software *ArcGIS Pro* represents a powerful tool for any kind of geospatial analysis including web applications. *ArcGIS Pro* is maintained by [ESRI](https://www.esri.com/) and comes with an own [*Python conda Environments*](hypy_install.html).
With the focus on freely available software, the usage of *ArcGIS Pro* and its *Python* environment including the `arcpy` package is just mentioned on this website. 

## Others {#others]
There are many other tools for geospatial analyses, which all deserve much more than just being mentioned here. Alas, for practical reasons, this website focuses on the usage of *QGIS*. This is why there is just a absolutely-not-complete list of other GIS tools here:

* [SAGA (System for Automated Geoscientific Analyses)](http://www.saga-gis.org/en/index.html)
* [Mapline](https://mapline.com/)
* [Mapbox](https://www.mapbox.com/)
* [uDig](http://udig.refractions.net/)

## Geospatial data, file handling and analysis

Geospatial analyses involve efficient code practices (e.g. with *Python*) and this is why detailed descriptions of geospatial data handling are embedded in the [*Python* (advanced)](geo_overview.html) section of this website.