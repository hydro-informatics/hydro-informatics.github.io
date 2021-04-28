# Geospatial Data

```{tip}
Use [*QGIS*](../get-started/geo.html#qgis) to display geospatial data and to create maps in *PDF* or image formats (e.g., *tif*, *png*, *jpg*).
```

## Geodata Sources
Geospatial data can be retrieved for various purposes from different sources. Here are some of them:

* Geographical, atlas map-like data are provided by [naturalearthdata.com](https://www.naturalearthdata.com) (e.g., with their 227-mb [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip)).
* Satellite imagery is available at
    - [USGS' Earth Explorer](https://earthexplorer.usgs.gov/).
    - [eesa's copernicus open access hub](https://scihub.copernicus.eu/dhus/#/home) (Sentinel-2)
    - [planet.com](https://www.planet.com/products/monitoring/) (commercial)
* [LiDAR](https://oceanservice.noaa.gov/facts/lidar.html) data can be found at [opentopography.org](https://opentopography.org/).
* Climatological data are provided by [NASA Earth Observation](https://neo.sci.gsfc.nasa.gov/).
* Meteorological (e.g., temperature or precipitation) and real-time satellite data are available at [wunderground.com](https://www.wunderground.com/) and its [wundermap](https://www.wunderground.com/wundermap).
* Data on land use (including canopy cover), socioeconomic characteristics, and global change are available at the [FAO GeoNetwork](http://www.fao.org/geonetwork/srv/en/main.home) or the archived ISCGM Global Map portal ([go to their github archive](https://globalmaps.github.io/)).

## Visualization
GIS software is needed to display geospatial data and many tools exist. This website primarily provides examples using [*QGIS*](../get-started/geo.html#qgis). Since the use of GIS software, especially *QGIS*, is necessary in several places on the website, explanations on how to install *QGIS* are already included on the [Get Started > Geospatial software](../get-started/geo) page.

```{tip}
The [*BASEMENT* pre-processing page](../numerics/basement) features the basics of geospatial data handling with *QGIS*. Therefore, this introduction to numerical modeling is also a good introduction to *QGIS*.
```

(gdb)=
## Geodatabase
A geodatabase (also known as *spatial database*) can store, query (e.g., using [Structured Query Language *SQL*](https://en.wikibooks.org/wiki/Structured_Query_Language), or modify data with geographic references (*geospatial data*). Primarily, geospatial data consist of vector data (see shapefiles), but raster data can also be implemented. A geodatabase links these data with attribute tables and geographic coordinates. The special aspect of geodatabases is that these data can be queried and manipulated by users via a (web or local) GIS (geographic information system) server. With software like [*QGIS*](../get-started/geo.html#qgis) (or *ArcGIS Pro*), for example, queries can be made on a kind of local server using locally stored geodata. The typical geodatabase format is `.gdb`, which works actually like a directory in *QGIS* or *ArcGIS*, and the maximum size of a `.gdb` file is 1 terabyte.

```{figure} ../img/geo-database.png
:alt: gdb

Functional skeleton of a geodatabase.
```

(vector)=
## Vector Data

Vector data are visually smooth and efficient for overlay operations, especially regarding shape-driven geo-information such as roads or surface delineations. Vector data are typically less storage-intensive, easier to scale, and more compatible with relational environments. Common formats are `.shp`, `JSON` or `TIN`.

 The shapefile format was invented by *Esri* ([download their PDF documentation](http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf) and information contained in shapefiles can be:

* Polygons (surface patches).
* Points with x-y-z coordinates and an *m* field containing point data.
* (Poly) lines consisting of lines defined by start points and endpoints.

(shp)=
### Shapefile

```{note}
The `gdal.ogr` driver name for shapefile handling is `ogr.GetDriverByName('ESRI Shapefile')`.
```

A shapefile is not just one file and consists of three essential parts:
* a `.shp` file, where geometries are stored,
* a `.shx` file, where indices of the geometries are stored,
* a `.prj` file that stores the projection, and
* a `.dbf` file containing attribute information (constitutes the attribute table).

These three files need to be in the same folder - otherwise, the shapefile does not work. A couple of other files may occur when we manipulate a shapefile (e.g., `.atx`, `.sb*`, `.shp.xml`, `.cpg`, `.mxs`, `.ai*`, or `.fb*`), but we can ignore those files.

Shapefile vector data typically has an attribute table (just like any other geodatabase) in which each polygon, line or point object can be assigned an attribute value. Attributes are defined by columns along with their names (column headers) and can have numeric (e.g., *float*, *double*, *int*, or *long*), text (*string*), or date/time (e.g. *yyyymmdd* or *HH:MM:SS*) formats.

```{figure} ../img/geo-shp-illu.png
:alt: shp-illu

Illustration of point, (poly) line, and polygon shapefiles.
```

### Shapefile versus Geodatabase
A shapefile can be understood as a concurring format to a geodatabase. Which file format is better? Strictly speaking, both a geodatabase and a shapefile can perform similar operations, but a shapefile requires more storage space to store similar contents, cannot store combinations of data and time, nor does it support raster files or *Null* (*not-a-number*) values. So basically we are better off with geodatabases, but the usage of shapefiles is popular and many geospatial operations focus on shapefile manipulations.

(tin)=
### Triangulated Irregular Network (TIN)

A triangulated irregular network (TIN) represents a surface consisting of multiple triangles. In hydraulic engineering and water resources research, one of the most important usage of TIN is the generation of computational meshes for numerical models (e.g., [in the BASEMENT tutorial](../numerics/basement)). In such models, a TIN consists of lines and nodes forming georeferenced, three-dimensionally sloped triangles of the surface, which represent a digital elevation model (DEM). TIN nodes have georeferenced coordinates and potentially more attribute information such as node IDs and elevation. The advantage of a TIN DEM over a raster DEM is that it requires less storage space. Alas, manipulating a TIN is not that easy like manipulating a raster. The below figure shows an example TIN created with [`matplotlib.tri.TriAnalyzer`](https://matplotlib.org/3.1.1/api/tri_api.html#matplotlib.tri.TriAnalyzer), and based on a [showcase from the matplotlib docs](https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/tricontour_smooth_delaunay.html#sphx-glr-gallery-images-contours-and-fields-tricontour-smooth-delaunay-py). The file ending of a TIN is `.TIN`.

```{figure} ../img/geo-tin.png
:alt: tin-illu

Illustration of a TIN.
```

(geojson)=
### GeoJSON

```{note}
The `gdal.ogr` driver name for shapefile handling is `ogr.GetDriverByName('GeoJSON')`.
```

[*GeoJSON*](https://geojson.org/) is an open format for representing geographic data with simple feature access standards, where *JSON* denotes *JavaScript Object Orientation* ([read more about *JSON* file manipulation in the *Python* intro on this website](../python-basics/pyxml.html#json)). The *GeoJSON* file name ending is `.geojson` and a file typically has the following structure:

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

(raster)=
## Gridded Cell (Raster) Data
Raster datasets store pixel values (*cells*), which require large storage space, but have a simple structure. A big advantage of rasters is the possibility to perform powerful geospatial and statistical analyses. Common Raster datasets are, among others, `.tif` (*GeoTIFF*), *GRID* (a folder with a `BND`, `HDR`, `STA`, `VAT`, and other files), `.flt` (floating points), *ASCII* (American Standard Code for Information Interchange), and many more image-like file types.

```{tip}
Preferably use the [*GeoTIFF*](https://en.wikipedia.org/wiki/GeoTIFF) format in raster analyses. A *GeoTIFF* file, typically includes a `.tif` file (with heavy data) and a `.tfw` (a six-line plain text world file containing georeference information) file.
```

```{note}
The `gdal` driver name for *GeoTIFF* handling is `gdal.GetDriverByName('GTiff')`.
```

```{figure} ../img/geo-raster-illu.png
:alt: raster-illu

Illustration of the Natural Earth's NE1_50M_SR_W.tif raster zoomed on Nepal, with point and line shapefiles indicating major cities and country borders, respectively. Take note of the tile-like appearance of the grid, where each tile corresponds to a 50m-x-50m raster cell.
```

(prj)=
## Projections and Coordinate Systems
In geospatial data analyses, a projection represents an approach to flatten (a part of) the globe. In this flattening process, latitudinal (North/South) and longitudinal (West/East) coordinates of a location on the globe (three-dimensional *3D*) are projected into the coordinates of a two-dimensional (*2D*) map. When 3D coordinates are projected onto 2D coordinates, distortions occur and there is a variety of projection systems used in geospatial analyses. In practice this means that if we use geospatial data files with different projections, a distortion effect propagates in all subsequent calculations. It is absolutely crucial to avoid distortion effects by ensuring that the same projections and coordinate systems are applied to all geospatial data used. This starts with the creation of a new geospatial layer (e.g., a point vector shapefile) in *QGIS* and should be used consistently in all program codes. To specify a projection or coordinate system in *QGIS*, click on `Project` > `Properties` > `CRS` tab and select a `COORDINATE_SYSTEM`. For example, an appropriate coordinate system for central Europe is `ESRI:31493` (read more in the [*QGIS* docs](https://docs.qgis.org/testing/en/docs/user_manual/working_with_projections/working_with_projections.html)). Projected systems may vary with regions (*local coordinate systems*), which can, for example, be found at [epsg.io](https://epsg.io/) or [spatialreference.org](https://spatialreference.org/).

In **shapefiles**, information about the projection is stored in a `.prj` file (recall definitions in the [geospatial data section](#vector), which is a plain text file. The Open Spatial Consortium (*OGC*) and *Esri* use [*Well-Known Text* (**WKT**)](http://docs.opengeospatial.org/is/18-010r7/18-010r7.html) files for standard descriptions of coordinate systemsa and such a *WKT*-formatted `.prj` file can look like this:


```python
PROJCS["unknown",GEOGCS["GCS_unknown",
                        DATUM["D_Unknown_based_on_GRS80_ellipsoid",SPHEROID["GRS_1980",6378137.0,298.257222101]],
                        PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
       PROJECTION["Lambert_Conformal_Conic"], PARAMETER["False_Easting",6561666.66666667],
       ..., UNIT["US survey foot",0.304800609601219]]
```

In [*GeoJSON*](#geojson) files, the standard coordinate system is [WGS84](https://www.unoosa.org/documents/pdf/icg/2018/icg13/wgd/wgd_12.pdf) according to the [developer's specifications](https://cran.r-project.org/web/packages/geojsonio/vignettes/geojson_spec.html).
The units and measures defined in the *WKT*-formatted `.prj` file also determine the units of *WK**B*** (*Well-Known Binary*) definitions of geometries such as line length (e.g., in meters, feet or many more), or polygon area (square meters, square kilometers, acres, and many more).

```{tip}
To ensure that all geometries are measures in meters and powers of meters, use [**EPSG:3857**](https://spatialreference.org/ref/sr-org/6864/) (former 900913 - g00glE) to define the *WKT*-formatted projection file.
```
