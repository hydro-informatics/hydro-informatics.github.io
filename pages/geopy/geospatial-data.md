---
title: Geospatial data
tags: [geo, geospatial, shapefile, raster, json, qgis, basement, tin]
keywords: geo-python gdal QGIS
summary: "Vector and gridded geospatial data types constitute the baseline of geospatial analyses."
sidebar: mydoc_sidebar
permalink: geospatial-data.html
folder: geopy
---


{% include tip.html content="Use [*QGIS*](geo_software.html#qgis) to display geospatial data and to create maps in *PDF* or image formats (e.g., *tif*, *png*, *jpg*)." %}

## Geodata sources
Geospatial data can be retrieved for various purposes from different sources. Here are some of them:

* Geographical, atlas map-like data are provided by [naturalearthdata.com](hhttps://www.naturalearthdata.com) (e.g., with their 227-mb [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip)). 
* Satellite imagery is available at
    - [USGS' Earth Explorer](https://earthexplorer.usgs.gov/).
    - [eesa's copernicus open access hub](https://scihub.copernicus.eu/dhus/#/home) (Sentinel-2)
* [LiDAR](https://oceanservice.noaa.gov/facts/lidar.html) data can be found at [opentopography.org](https://opentopography.org/). 
* Climatological data are provided by [NASA Earth Observation](https://neo.sci.gsfc.nasa.gov/).
* Data on land use (including canopy cover), socioeconomic characteristics, and global change are available at the [FAO GeoNetwork](http://www.fao.org/geonetwork/srv/en/main.home) or the archived ISCGM Global Map portal ([go to their github archive](https://globalmaps.github.io/)).


## Geodatabase
A geodatabase (also known as *spatial database*) can store, query (e.g., using [Structured Query Language *SQL*](https://en.wikibooks.org/wiki/Structured_Query_Language)), or modify data with geographic references (*geospatial data*). Primarily, geospatial data consist of vector data (see shapefiles), but raster data can also be implemented. A geodatabase links these data with attribute tables and geographic coordinates. The special aspect of geodatabases is that these data can be queried and manipulated by users via a (web or local) GIS (geographic information system) server. With software like [*QGIS*](geo_software.html#qgis) (or *ArcGIS Pro*), for example, queries can be made on a kind of local server using locally stored geodata. The typical geodatabase format is `.gdb`, which works actually like a directory in *QGIS* or *ArcGIS*, and the maximum size of a `.gdb` file is 1 terabyte.

{% include image.html file="geo-database.png" alt="gdb" caption="Functional skeleton of a geodatabase." %}

## Vector data

Vector data are visually smooth and efficient for overlay operations, especially regarding shape-driven geo-information such as roads or surface delineations. Vector data are typically less storage-intensive, easier to scale, and more compatible with relational environments. Common formats are `.shp`, `JSON` or `TIN`.
 
 The shapefile format was invented by *Esri* ([download their PDF documentation](http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf)) and information contained in shapefiles can be:

* Polygons (surface patches).
* Points with x-y-z coordinates and an *m* field containing point data.
* (Poly) lines consisting of lines defined by start points and endpoints.


### Shapefile
A shapefile is not just one file and consists of three essential parts:
* a `.shp` file, where geometries are stored,
* a `.shx` file, where indices of the geometries are stored, 
* a `.prj` file that stores the projection, and
* a `.dbf` file containing attribute information (constitutes the attribute table).

These three files need to be in the same folder - otherwise, the shapefile does not work. A couple of other files may occur when we manipulate a shapefile (e.g., `.atx`, `.sb*`, `.shp.xml`, `.cpg`, `.mxs`, `.ai*`, or `.fb*`), but we can ignore those files.

Shapefile vector data typically has an attribute table (just like any other geodatabase) in which each polygon, line or point object can be assigned an attribute value. Attributes are defined by columns along with their names (column headers) and can have numeric (e.g., *float*, *double*, *int*, or *long*), text (*string*), or date/time (e.g. *yyyymmdd* or *HH:MM:SS*) formats.

{% include image.html file="geo-shp-illu.png" alt="shp-illu" caption="Illustration of point, (poly) line, and polygon shapefiles." %}

### Shapefile versus geodatabase
A shapefile can be understood as a concurring format to a geodatabase. Which file format is better? Strictly speaking, both a geodatabase and a shapefile can perform similar operations, but a shapefile requires more storage space to store similar contents, cannot store combinations of data and time, nor does it support raster files or *Null* (*not-a-number*) values. So basically we are better off with geodatabases, but the usage of shapefiles is popular and many geospatial operations focus on shapefile manipulations.

### Triangulated Irregular Network (TIN)

A triangulated irregular network (TIN) represents a surface consisting of multiple triangles. In hydraulic engineering and water resources research, one of the most important usage of TIN is the generation of computational meshes for numerical models (e.g., [on this website's BASEMENT tutorial](bm-pre.html)). In such models, a TIN consists of lines and nodes forming georeferenced, three-dimensionally sloped triangles of the surface, which represent a digital elevation model (DEM). TIN nodes have georeferenced coordinates and potentially more attribute information such as node IDs and elevation. The advantage of a TIN DEM over a raster DEM is that it requires less storage space. Alas, manipulating a TIN is not that easy like manipulating a raster. The below figure shows an example TIN created with [`matplotlib.tri.TriAnalyzer`](https://matplotlib.org/3.1.1/api/tri_api.html#matplotlib.tri.TriAnalyzer)), and based on a [showcase from the matplotlib docs](https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/tricontour_smooth_delaunay.html#sphx-glr-gallery-images-contours-and-fields-tricontour-smooth-delaunay-py). The file ending of a TIN is `.TIN`.

{% include image.html file="geo-tin.png" alt="tin-illu" caption="Illustration of a TIN." %}

### GeoJSON

[*GeoJSON*](https://geojson.org/) is an open format for representing geographic data with simple feature access standards, where *JSON* denotes *JavaScript Object Orientation* ([read more about *JSON* file manipulation in the *Python* intro on this website](hypy_xml.html#json)). The *GeoJSON* file name ending is `.geojson` and a file typically has the following structure:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [9.104028940200806, 48.74417005744522]
      },
      "properties": {
        "name": "IWS"
      }
    }
  ]
}
```

Visit [geojson.io](https://geojson.io/) to build a customized *GeoJSON* file. While *GeoJSON* metadata can provide height information (`z` values) as a `properties` value, there is a more suitable offspring to encode geospatial topology in the form of the still rather young [*TopoJSON*](https://github.com/topojson/topojson/wiki) format. 

## Gridded cell (raster) data 
Raster datasets store pixel values (*cells*), which require large storage space, but have a simple structure. A big advantage of rasters is the possibility to perform powerful geospatial and statistical analyses. Common Raster datasets are, among others, `.tif` (*GeoTIFF*), *GRID* (a folder with a `BND`, `HDR`, `STA`, `VAT`, and other files), `.flt` (floating points), *ASCII* (American Standard Code for Information Interchange), and many more image-like file types.

{% include tip.html content="Preferably use the [*GeoTIFF*](https://en.wikipedia.org/wiki/GeoTIFF) format in raster analyses. A *GeoTIFF* file, typically includes a `.tif` file (with heavy data) and a `.tfw` (a sixe-line plain text world file containing georeference information) file." %}

{% include image.html file="geo-raster-illu.png" alt="raster-illu" caption="Illustration of the Natural Earth's NE1_50M_SR_W.tif raster zoomed on Nepal, with point and line shapefiles indicating major cities and country borders, respectively. Take note of the tile-like appearance of the grid, where each tile corresponds to a 50m-x-50m raster cell." %}