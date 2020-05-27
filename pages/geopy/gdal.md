---
title: Geo-Python - Open Source
keywords: geo-python gdal QGIS
summary: "Geospatial analysis with the open source software QGIS and the the gdal package."
sidebar: mydoc_sidebar
permalink: hypy_gdal.html
folder: geopy
---

## Installation

{% include warning.html content="If you **cannot `import gdal`**, for some apparently arbitrary reasons (e.g., `Error: Arbitrary stuff thing is missing.`), the problem probably lies in the definition of environmental variables. The problem can be trouble-shot in *PyCharm* with the following solution<br><br>
 1. Go to *File* > *Settings ...*  > *Build, Execution, Deployment* > *Console* > *Python Console* > *Environment variables* <br>
 2. Set the following `environment_variables`<br> 
     `setx GDAL_DATA 'C:\Program Files\GDAL\gdal-data'`<br>
     `setx GDAL_DRIVER_PATH 'C:\Program Files\GDAL\gdalplugins'`<br>
     `setx PROJ_LIB 'C:\Program Files\GDAL\projlib'`<br>
     `setx PYTHONPATH 'C:\Program Files\GDAL\'`<br><br>
 Wait a couple of moments until *PyCharm* adapted the new `environment_variables` and `import gdal` - should work now." %}
