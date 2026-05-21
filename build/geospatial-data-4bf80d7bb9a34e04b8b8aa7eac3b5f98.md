---
description: Geospatial data explained and with sources of rasters and shapefiles
---

(geospatial-data)=
# Geospatial Data

```{tip}
Use {ref}`qgis-install` to display geospatial data and to create maps in *PDF* or image formats (e.g., *tif*, *png*, *jpg*). In addition, the {ref}`qgis-tutorial` provides an easy and interactive walk through geospatial analyses.
```

```{admonition} Geodata explained on YouTube
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/lJUvZv5ts3U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Watch this section as a video on the <a href="https://www.youtube.com/@hydroinformatics">@Hydro-Morphodynamics channel on YouTube</a>.</p>
```

## Geodata Sources
Geospatial data can be retrieved for various purposes from different sources. Here are some of them:

* Geographical, atlas-style map data are provided by [naturalearthdata.com](https://www.naturalearthdata.com) (e.g., the ~230 MB [Natural Earth quick start kit](https://www.naturalearthdata.com/downloads/) bundled with pre-styled QGIS projects).
* {term}`DEM`s, oceanographic and more water-related maps are available at the US' [NOAA Geo-platform](https://noaa.maps.arcgis.com/home/search.html?q=owner%3Ancei_noaa&t=content&start=1&sortOrder=desc&sortField=modified&focus=layers) and its [TDS Catalog](https://www.ncei.noaa.gov/thredds/catalog/catalog.html)
* [OpenStreetMap](https://www.openstreetmap.org) data extractions are available at [https://download.geofabrik.de/](https://download.geofabrik.de/)
* Satellite imagery is available at
    - the [USGS' Earth Explorer](https://earthexplorer.usgs.gov/)
    - the [ESA's Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (Sentinel-1/2/3/5P; this replaced the former Copernicus Open Access Hub / *SciHub*, which was decommissioned on 2 November 2023)
    - [planet.com](https://www.planet.com/products/monitoring/) (commercial)
* [LiDAR](https://oceanservice.noaa.gov/facts/lidar.html) data can be found at [opentopography.org](https://opentopography.org/).
* Climatological data are provided by [NASA Earth Observations (NEO)](https://neo.gsfc.nasa.gov/).
* Meteorological (e.g., temperature or precipitation) and real-time satellite data are available at [wunderground.com](https://www.wunderground.com/) and its [wundermap](https://www.wunderground.com/wundermap).
* Climate and meteorological data and forecasts are available at [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu), including, for example, ERA5 monthly averaged temperature data
* Data on land use (including canopy cover), socioeconomic characteristics, and global change are available at the [FAO Map Catalog (GeoNetwork)](https://data.apps.fao.org/map/catalog/srv/eng/catalog.search) or the archived ISCGM Global Map portal ([go to their GitHub archive](https://globalmaps.github.io/)).
* Topographical data  (1 to 5-m resolution) from the state of Bavaria, Germany, can be found at [https://www.ldbv.bayern.de](https://www.ldbv.bayern.de/produkte/3dprodukte/gelaende.html).
* Topographical data from EU countries can be found at [https://www.mapsforeurope.org](https://www.mapsforeurope.org/datasets/euro-dem).

## Visualization
GIS software is needed to display geospatial data and many tools exist. This website primarily provides examples using {ref}`qgis-install`. Since the use of GIS software, especially *QGIS*, is necessary for several sections in this eBook, explanations on how to install *QGIS* are already included in the {ref}`chpt-geo-software`.

```{tip}
The {ref}`qgis-tutorial` features the basics of geospatial data handling with {ref}`qgis-install`.
```

(gdb)=
## Geodatabase
A geodatabase (also known as *spatial database*) can store, query (e.g., using [Structured Query Language SQL](https://en.wikibooks.org/wiki/Structured_Query_Language)), or modify data with geographic references (*geospatial data*). Primarily, geospatial data consist of vector data (see shapefiles), but raster data can also be implemented. A geodatabase links these data with attribute tables and geographic coordinates. A special feature of geodatabases is that they can be visualized and manipulated via a (web or local) GIS (geographic information system) server. For instance, software like {ref}`qgis-install` (or *ArcGIS Pro*) enables to create maps and make queries on a kind of local server using locally stored geodata. The typical geodatabase format is `.gdb`, which functions as a directory in {ref}`qgis-install` or *ArcGIS*, and the maximum size of a `.gdb` file is 1 terabyte.

```{figure} ../img/geo-database.png
:alt: gdb

The functional skeleton of a geodatabase.
```

(vector)=
## Vector Data

Vector data are visually smooth and efficient for overlay operations, especially regarding shape-driven geo-information such as roads or surface delineations. Vector data are characterized as being little storage-intensive, easy to scale, and compatible with relational environments. Common formats are `.shp`, `JSON` or `TIN`.

 The shapefile format was invented by *Esri* in the early 1990s (the original [shapefile technical description (PDF)](https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/shapefile.pdf) remains the authoritative reference) and information contained in a shapefile can be:

* Polygons (surface patches),
* Points with x-y-z coordinates and an *m* field containing point data, and
* (Poly) lines consisting of lines defined by start points and endpoints.

(shp)=
### Shapefile

```{note}
The `gdal.ogr` driver name for shapefile handling is `ogr.GetDriverByName('ESRI Shapefile')`.
```

A shapefile consists of multiple files on the disk with the following essential parts:

* a `.shp` file, where geometries are stored,
* a `.shx` file, where indices of the geometries are stored,
* a `.prj` file that stores the projection, and
* a `.dbf` file containing attribute information (constitutes the attribute table).

These files need to be in the same folder - otherwise, the shapefile is incomplete and does not work (correctly). A couple of other files may occur when we manipulate a shapefile (e.g., `.atx`, `.sb*`, `.shp.xml`, `.cpg`, `.mxs`, `.ai*`, or `.fb*`), but we can ignore those files.

Shapefile vector data typically has an attribute table (just like any other geodatabase) in which every polygon, line, or point object can be assigned an attribute value. Attributes are defined by columns along with their names (column headers) and can have numeric (e.g., *float*, *double*, *int*, or *long*), text (*string*), or date/time (e.g. *yyyymmdd* or *HH:MM:SS*) formats.

```{figure} ../img/geo-shp-illu.png
:alt: shp-illu

Illustration of point (red), (poly) line (green), and polygon (blue) shapefile features.
```

### Shapefile versus Geodatabase
A shapefile can be understood as a competing format to a geodatabase. Which file format is better? Strictly speaking, both a geodatabase and a shapefile can perform similar operations, but a shapefile requires more storage space to store similar contents, cannot store combined date-and-time fields, and does not support raster data or *Null* (*not-a-number*) values. Shapefiles are also limited to 2 GB per component file, attribute names of 10 characters or fewer, and text fields of 255 characters or fewer. Thus, geodatabases (and the more portable {ref}`GeoPackage <gpkg>` format) have a technical advantage over shapefiles, but the usage of shapefiles is still popular and many legacy geospatial workflows focus on shapefile manipulations.

(tin)=
### Triangulated Irregular Network (TIN)

A triangulated irregular network (TIN) represents a surface composed of multiple triangles. In hydraulic engineering and water resources research, one of the most important uses of a TIN is the generation of computational meshes for numerical models (read more in the {ref}`chpt-basement` tutorial, for example). In such models, a TIN consists of lines and nodes forming georeferenced, three-dimensionally sloped triangles of the surface, which represent a digital elevation model (DEM). TIN nodes have georeferenced coordinates and potentially more attribute information such as node IDs and elevation. The advantage of a TIN DEM over a raster (see below) DEM is that it requires less storage space. However, manipulating a TIN is not as straightforward as manipulating a raster. The below figure shows an example TIN created with [`matplotlib.tri.TriAnalyzer`](https://matplotlib.org/stable/api/tri_api.html#matplotlib.tri.TriAnalyzer), and based on a [showcase from the matplotlib docs](https://matplotlib.org/stable/gallery/images_contours_and_fields/tricontour_smooth_delaunay.html). The file ending of a TIN is `.tin`.

```{figure} ../img/geo-tin.png
:alt: tin-illu

Illustration of a TIN.
```

(geojson)=
### GeoJSON

```{note}
The `gdal.ogr` driver name for GeoJSON handling is `ogr.GetDriverByName('GeoJSON')`.
```

[GeoJSON](https://geojson.org/) is an open format for representing geographic data with simple feature access standards, where *JSON* denotes *JavaScript Object Notation* (read more about {ref}`json` file manipulation in the Python basics). GeoJSON is standardized as [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946). The GeoJSON file name ending is `.geojson` and a file typically has the following structure:

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

While GeoJSON metadata can provide height information (`z` values) as a `properties` value, there is a more suitable offspring to encode geospatial topology in the form of the [TopoJSON](https://github.com/topojson/topojson/wiki) format. To manipulate GeoJSON files with Python, go to the {ref}`geojson-pckg` section. To build a customized GeoJSON file, visit [geojson.io](https://geojson.io/).

(gpkg)=
## GeoPackage (GPKG)

```{note}
The `gdal.ogr` driver name for GeoPackage handling is `ogr.GetDriverByName('GPKG')`. The same `GPKG` driver in GDAL also exposes raster tiles (see the [GDAL GPKG vector](https://gdal.org/en/stable/drivers/vector/gpkg.html) and [GDAL GPKG raster](https://gdal.org/en/stable/drivers/raster/gpkg.html) docs).
```

[GeoPackage](https://www.geopackage.org/) (`.gpkg`) is an open, platform-independent, standards-based geospatial data format published by the [Open Geospatial Consortium (OGC)](https://www.ogc.org/) (OGC standard 12-128r19). Technically, a GeoPackage is a single [SQLite](https://www.sqlite.org/) 3 database file that follows the GeoPackage specification, which means it can be opened, queried, and modified with any SQLite-aware tool in addition to GIS software like {ref}`QGIS <qgis-install>`.

In contrast to a {ref}`shapefile <shp>` (which is really a small bundle of sidecar files), a GeoPackage is *one single file* that can simultaneously contain:

* Multiple **vector** layers (points, lines, polygons, mixed geometry) in one container,
* **Raster** tile pyramids (e.g., {term}`GeoTIFF`-style imagery or DEMs),
* **Attribute tables** without geometry,
* **Spatial indexes** (R-tree) for fast spatial queries,
* **Metadata** and styles.

### Why use a GeoPackage instead of a shapefile?

Compared to the legacy shapefile, the GeoPackage format removes most of the shapefile's well-known limitations:

| Property | Shapefile | GeoPackage |
|---|---|---|
| Number of files per dataset | At least 3 (`.shp`, `.shx`, `.dbf`, plus `.prj`, `.cpg`, ...) | 1 (`.gpkg`) |
| Number of layers per file | 1 | Many (vector and raster mixed) |
| Maximum size | 2 GB per component file | ~140 TB (SQLite limit) |
| Field name length | ≤ 10 characters | Unlimited (practically) |
| Text field length | ≤ 255 characters | Unlimited (TEXT) |
| Character encoding | Code-page dependent (`.cpg`) | UTF-8 (full Unicode) |
| Date/time data type | Date only | Full `DATETIME` |
| Null / NaN values | Not supported | Supported |
| Spatial index | External (`.sbn`/`.sbx`) | Built-in R-tree |
| Raster support | No | Yes (tiled) |
| Standardization | De-facto (Esri whitepaper) | Open OGC standard |

### Reading and writing a GeoPackage with Python

GeoPackage is natively supported by GDAL/OGR, [Fiona](https://fiona.readthedocs.io/), [geopandas](https://geopandas.org/), and [rasterio](https://rasterio.readthedocs.io/). A typical round trip with *geopandas* looks like:

```python
import geopandas as gpd

# Read a specific layer from a GeoPackage
gdf = gpd.read_file("rivers.gpkg", layer="centerlines")

# Write (or append) another layer into the same .gpkg
gdf.to_file("rivers.gpkg", layer="centerlines_buffered", driver="GPKG")
```

To list all layers contained in a GeoPackage:

```python
import fiona
print(fiona.listlayers("rivers.gpkg"))
```

Because a GeoPackage is a SQLite database, attribute queries can also be issued directly through SQL:

```python
import sqlite3
con = sqlite3.connect("rivers.gpkg")
for row in con.execute("SELECT name, length_m FROM centerlines WHERE length_m > 1000"):
    print(row)
```

```{tip}
For new projects in the {ref}`qgis-tutorial` and the {ref}`Geospatial Python tutorials <sec-geo-python>`, prefer **GeoPackage over shapefile**. QGIS even uses GeoPackage as its default save format when you create a new vector layer through *Layer* > *Create Layer* > *New GeoPackage Layer...*.
```

(raster)=
## Gridded Cell (Raster) Data
Raster datasets store pixel values (*cells*), which require large storage space, but have a simple structure. Another big advantage of rasters is the possibility to perform geospatial algebra and statistical analyses. Common raster dataset formats are, among others, `.tif` ({term}`GeoTIFF`), *GRID* (a folder with `BND`, `HDR`, `STA`, `VAT`, and other files), `.flt` (floating points), {term}`ASCII` (American Standard Code for Information Interchange), and many more image-like file types.

```{tip}
Preferably use the {term}`GeoTIFF` format for raster analyses. A GeoTIFF file typically includes a `.tif` file (with heavy data) and a `.tfw` (a six-line plain text world file containing georeference information) file.
```

```{note}
The `gdal` driver name for {term}`GeoTIFF` handling is `gdal.GetDriverByName('GTiff')`.
```

```{figure} ../img/geo-raster-illu.png
:alt: raster-illu

Illustration of the Natural Earth's NE1_50M_SR_W.tif raster zoomed on Nepal, with point and line shapefiles indicating major cities and country borders, respectively. Take note of the tile-like appearance of the grid, where every tile corresponds to a 50m-x-50m raster cell.
```

## Lidar and Underwater Digital Elevation Models (Bathymetries)

Terrain survey data are often delivered in the shape of an x-y-z point dataset along with point attribute parameters. Three-dimensional datasets of the bare Earth's topographic surface are referred to as a Digital Elevation Model (read more about **{term}`DEM`** terminology in the glossary), which represents the baseline for any physical analysis of a river ecosystem. The underwater topography is called the **bathymetry** of a river or other water body. Nowadays, x-y-z point clouds for generating a DEM mostly stem from {term}`Lidar` combined with {term}`Echo sounder` surveys. Older approaches rely on manual surveying (e.g., with a total station) of cross-sectional river profiles and interpolating the terrain between the profiles. The newer {term}`Lidar` technique employs light (laser) sources and provides bathymetry data up to 2-m deep water in the form of `*.las` or the zipped form `*.laz` files. Deeper waters are mapped with an {term}`Echo sounder` and the merged {term}`Lidar` and echo-sounding datasets produce seamless point clouds of river ecosystems, which may be stored in different file types.

{term}`Lidar` produces massive point clouds, which quickly overcharge even powerful computers. This is why in practice, {term}`Lidar` data may need to be broken down into smaller zones of less than 10<sup>6</sup> points each. Particular {term}`Lidar` processing software (e.g., [LAStools](http://lastools.org/)) is helpful in this task.


(prj)=
## Projections and Coordinate Systems
In geospatial data analyses, a projection represents an approach to flatten (a part of) the globe. In this flattening process, latitudinal (North/South) and longitudinal (West/East) coordinates of a location on the globe (three-dimensional - 3d) are projected onto the coordinates of a two-dimensional (2d) map. When 3d coordinates are projected onto 2d coordinates, distortions occur, and a variety of projection systems are used in geospatial analyses. In practice, this means that if we use geospatial data files with different projections, a distortion effect propagates into all subsequent calculations. It is crucial to avoid such distortion effects by ensuring that the same projection and coordinate reference system (CRS) is applied consistently to all geospatial data. This starts with the creation of a new geospatial layer (e.g., a point vector shapefile or {ref}`GeoPackage <gpkg>`) in {ref}`QGIS (get installation instructions) <qgis-install>` and should be used consistently in all program codes. To specify a CRS; for instance, in **QGIS** (tutorial in the {ref}`next section <qgis-tutorial>`), click on **Project** > **Properties** > **CRS** tab and select a `COORDINATE_SYSTEM`. For example, an appropriate coordinate system for central Europe is `ESRI:31493` (read more in the [QGIS docs](https://docs.qgis.org/latest/en/docs/user_manual/working_with_projections/working_with_projections.html)). Projected systems vary with region (*local coordinate systems*), which can be found, for example, at [epsg.io](https://epsg.io/) or [spatialreference.org](https://spatialreference.org/).

In **shapefiles**, information about the projection is stored in a `.prj` file (recall definitions in the {ref}`shapefile section <shp>`), which is a plain text file. The Open Geospatial Consortium (*OGC*) and Esri use [*Well-Known Text* (**WKT**)](https://docs.ogc.org/is/18-010r11/18-010r11.html) files for standard descriptions of coordinate systems, and a WKT-formatted `.prj` file is shown in the code block below. The units and measures defined in the WKT-formatted `.prj` file also determine the units of *WK**B*** (*Well-Known Binary*) definitions of geometries such as line length (e.g., in meters, feet, or many more), or polygon area (square meters, square kilometers, acres, and many more).


```python
PROJCS["unknown",GEOGCS["GCS_unknown",
                        DATUM["D_Unknown_based_on_GRS80_ellipsoid",SPHEROID["GRS_1980",6378137.0,298.257222101]],
                        PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
       PROJECTION["Lambert_Conformal_Conic"], PARAMETER["False_Easting",6561666.66666667],
       ..., UNIT["US survey foot",0.304800609601219]]
```

In {ref}`geojson` files, the default coordinate reference system is **WGS 84** (longitude/latitude, [EPSG:4326](https://epsg.io/4326)), as mandated by [RFC 7946 §4](https://datatracker.ietf.org/doc/html/rfc7946#section-4).


```{admonition} Use EPSG:3857
:class: tip

To ensure that all geometries are measured in meters and powers of meters, use [**EPSG:3857**](https://epsg.io/3857) (the *Web Mercator* projection used by most online map services; formerly known as `EPSG:900913` — *g00glE*) to define the WKT-formatted projection file.
```
