---
title: Geospatial Python - Open Source
tags: [python, gdal, pandas, geo, geospatial, shapefile, raster, anaconda, descartes]
keywords: geo-python gdal QGIS
summary: "Geospatial analysis with the open source software QGIS and the the gdal package."
sidebar: mydoc_sidebar
permalink: hypy_gdal.html
folder: geopy
---


The goal of this page is to provide an understanding of how geospatial data can be used and manipulated with *Python* code. The file manipulation involves logical and algebraic operations, and conversion from and to other geospatial file formats.

This page builds on explanations from [Michael Diener's *Python Geospatial Analysis Cookbook*](https://github.com/mdiener21/python-geospatial-analysis-cookbook) (open access under MIT license). So if you want to learn more details about any information provided in the following, take a look at this comprehensive ebook.

## Popular *Python packages*
This section lists open-source packages for geospatial file manipulation with *Python*. Except for `gdal` these packages are neither installed in the [`hypy`](hypy_install.html#create-and-install-conda-environments) nor in the *conda* `base` environment. The following sections explain relevant packages for this course and how those can be installed.

{% include callout.html content="The proprietary license-requiring `arcpy` package is described on the [Commercial software](hypy_arcpy.html) page." %}

### gdal
[`gdal`](https://gdal.org/) and `ogr` of the [OSGeo Project](http://www.osgeo.org/) stem from the *GDAL* project, which is part of the Open Source
Geospatial Foundation ([*OSGeo*](https://www.osgeo.org)) -  the developers of *QGIS*. `gdal` provides many methods to convert geospatial data (file types, projections, derive geometries), where `gdal` itself handels [raster data](geospatial-data.html#raster) and its `ogr` module handles [vector data](geospatial-data.html#vector). This page primarily uses `gdal` and `ogr`; so it is important to get the installation of `gdal` right.

To install `gdal` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge gdal
```

{% include warning.html content="If you **cannot `import gdal`**, for some apparently arbitrary reasons (e.g., `Error: Arbitrary-like stuff is missing.`), the problem probably lies in the definition of environmental variables. The problem can be trouble-shot in *PyCharm* with the following solution<br><br>
 1. Go to *File* > *Settings ...*  > *Build, Execution, Deployment* > *Console* > *Python Console* > *Environment variables* <br>
 2. Set the following `environment_variables`<br> 
     `setx GDAL_DATA 'C:\Program Files\GDAL\gdal-data'`<br>
     `setx GDAL_DRIVER_PATH 'C:\Program Files\GDAL\gdalplugins'`<br>
     `setx PROJ_LIB 'C:\Program Files\GDAL\projlib'`<br>
     `setx PYTHONPATH 'C:\Program Files\GDAL\'`<br><br>
 Wait a couple of moments until *PyCharm* adapted (*building skeleton ...*) the new `environment_variables` and `import gdal` - should work now." %}

{% include unix.html content="In general, the installation of `gdal` in only an environment can be *tricky*. Therefore, *Linux* user may want to make a global installation with:<br>
 1. `sudo apt-get install -y build-essentiallibxml2-dev libxslt1-dev` (install build and *XML* tools) <br>
 2. `sudo apt-get install libgdal-dev` (install `gdal` development files) <br>
 3. `sudo apt-get install python-gdal` (install `gdal` itself) <br>
 4. To enable `gdal` in a virtual environment:<br>
     - run virtual wrapper: `toggleglobalsitepackages` <br>
     - activate environment with `conda activate ENVIRONMENT` <br>
     - activate global site packages for the current environment: `toggleglobalsitepackages enable global site-packages`" %}

### geojson
[`geojson`](https://pypi.org/project/geojson/) is the most direct option for handling [*GeoJSON*](geospatial-data.html#geojson) data.
To install `geojson` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge geojson
```

### descartes
Even though of proprietary origin, the [`descartes`](https://docs.descarteslabs.com/api.html) package (developed and maintained by [*Descartes Labs*](https://www.descarteslabs.com/)) comes with many open-sourced functions. Moreover, *Decartes Labs* hosts the showcase platform [*GeoVisual Search*](https://search.descarteslabs.com/) with juicy illustrations of aritificial intelligence (*AI*) applications in geoscience. To install `descartes` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge descartes 
```

### pyshp and (or) shapely
For [shapefile](geospatial-data.html#shp) handling, [`pyshp`](https://pypi.org/project/pyshp/) provides pure *Python* code (rather than wrappers), which simplifies direct dealing with shapefile in *Python*. To install `pyshp` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge pyshp
```

However, the latest release of `pyshp` is from February 2019, which is a good reason to look for a currently maintained alternative. Another good and very well documented option for shapefile handling is [`shapely`](https://shapely.readthedocs.io/). To install `shapely` for *Python*, open [*Anaconda Prompt*](hypy_install.html#install-pckg) and type:


```python
conda install -c conda-forge shapely
```

### Other packages
Besides the above mentioned packages there are other useful libraries for geospatial analyses in *Python*:
 * [`rasterio`](https://rasterio.readthedocs.io/en/latest/) for processing raster data as [`numpy`](hypy_pynum.html#numpy) arrays.
 * [`rasterstats`](https://pythonhosted.org/rasterstats/) produces zonal statistics of rasters and can interact with *GeoJSON* files (install in *Anaconda Prompt* with `conda install -c conda-forge rasterstats`).
 * [`sckit-image`](https://scikit-image.org/) for machine learning applied to georeferenced images.
 * [`django`](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/) as a geographic web frame and for database connections (install in *Anaconda Prompt* with `conda install -c anaconda django`).
 * [`postgresql`](https://www.postgresqltutorial.com/postgresql-python/) for SQL database connections (install in *Anaconda Prompt* with `conda install -c anaconda postgresql`).
 * [`owslib`](http://geopython.github.io/OWSLib/) to connect with *Open Geospatial Consortium* (*OGC*) web services (install in *Anaconda Prompt* with `conda install -c conda-forge owslib`)


## Projections and coordinat systems {#prj}
In geospatial data analyses, a projection represents an approach to flatten (a part of) the globe. In this flattening process, latitudinal (North/South) and longitudinal (West/East) coordinates of a location on the globe (three-dimensional *3D*) are projected into the coordinates of a two-dimensional (*2D*) map. When 3D coordinates are projected onto 2D coordinates, distortions occur and there is a variety of projection systems used in geospatial analyses. In practice this means that if we use geospatial data files with different projections, a distortion effect propagates in all subsequent calculations. It is absolutely crucial to avoid distortion effects by ensuring that the same projections and coordinate systems are applied to all geospatial data used. This starts with the creation of a new geospatial layer (e.g., a point vector shapefile) in *QGIS* and should be used consistently in all program codes. To specify a projection or coordinate system in *QGIS*, click on `Project` > `Properties` > `CRS` tab and select a `COORDINATE_SYSTEM`. For example, an appropriate coordinate system for central Europe is `ESRI:31493` (read more in the [*QGIS* docs](https://docs.qgis.org/testing/en/docs/user_manual/working_with_projections/working_with_projections.html)). Projected systems may vary with regions (*local coordinate systems*), which can, for example, be found at [epsg.io](https://epsg.io/) or [spatialreference.org](https://spatialreference.org/).

In **shapefiles**, information about the projection is stored in a `.prj` file (recall definitions on the [geospatial data](geospatial-data.html#vector) page), which is a plain text file. The Open Spatial Consortium (*OGC*) and *Esri* are use [*Well-Known Text* (**WKT**)](http://docs.opengeospatial.org/is/18-010r7/18-010r7.html) files for standard descriptions of coordinate systemsa and such a *wkt*-based `.prj` file can look like this:


```python
PROJCS["unknown",GEOGCS["GCS_unknown",
                        DATUM["D_Unknown_based_on_GRS80_ellipsoid",SPHEROID["GRS_1980",6378137.0,298.257222101]],
                        PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
       PROJECTION["Lambert_Conformal_Conic"], PARAMETER["False_Easting",6561666.66666667], 
       ..., UNIT["US survey foot",0.304800609601219]]
```

In [*GeoJSON*](geospatial-data.html#geojson) files, the standard coordinate system is [WGS84](https://www.unoosa.org/documents/pdf/icg/2018/icg13/wgd/wgd_12.pdf) according to the [developer's specifications](https://cran.r-project.org/web/packages/geojsonio/vignettes/geojson_spec.html).

## Working with shapefiles
{% include note.html content="Make sure to understand [shapefiles](geospatial-data.html#shp) and [vector data](geospatial-data.html#vector) before reading this section." %}

### Load a shapefile
`gdal`'s `ogr` module is an excellent source for handling shapefiles. To open a shapefile in *Python*, we need to instantiate the correct driver (`"ESRI Shapefile"` for shapefiles) first. With the driver object (`ogr.GetDriverByName("SHAPEFILE")`), we can then open (instantiate) a shapefile (object with `shp_driver.Open("SHAEPEFILE")`), which contains layer information. It is precisely this layer information (i.e., references to shapefile attributes) that we want to work with. Therefore we have to instantiate a shapefile layer object with `shp_dataset.GetLayer()`.


```python
from gdal import ogr
shp_driver = ogr.GetDriverByName("ESRI Shapefile")
shp_dataset = shp_driver.Open("geodata/shapefiles/cities.shp")
shp_layer = shp_dataset.GetLayer()
```

{% include tip.html content="To get a full list of supported `ogr` drivers (e.g., for `DXF`, `ESRIJSON`, `GPS`, `PDF`, `SQLite`, `XLSX`, and many more), [download the script `get_ogr_drivers.py`](https://github.com/hydro-informatics/material-py-codes/raw/master/geo/get_ogr_drivers.py) from the course repository (script available during courses only)." %}

### Create a new shapefile
The `ogr` module also enables creating a new point, line or polygon shapefile. The following code block defines a function for creating a shapefile, where the optional keyword argument `overwrite` is used to control whether an existing shapefile with the same name should be overwritten (default: `True`).
The command `shp_driver.CreateDataSource(SHP-FILE-DIR)` creates a new shapefile and the rest of the function adds a layer to the shapefile if the optional keyword arguments `layer_name` and `layer_type` are provided. Both optional keywords must be *string*s, where `layer_name` can be any name for the new layer. `layer_type` must be either `"point"`, `"line"`, or `"polygon"` to create a point, (poly)line, or polygon shapefile respectively. The function uses the `geometry_dict` dictionary to assign the correct `ogr.SHP-TYPE` to the layer. There are more options for extending the `create_shp(...)` function listed on [*pcjerick*'s github pages](https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html).



```python
from gdal import ogr
import os


def create_shp(shp_file_dir, overwrite=True, *args, **kwargs):
    """
    :param shp_file_dir: STR of the (relative shapefile directory (ends on ".shp")
    :param overwrite: [optional] BOOL - if True, existing files are overwritten
    :kwarg layer_name: [optional] STR of the layer_name - if None: no layer will be created (max. 13 chars)
    :kwarg layer_type: [optional] STR ("point, "line", or "polygon") of the layer_name - if None: no layer will be created
    :output: returns an ogr shapefile layer
    """
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")

    # check if output file exists if yes delete it
    if os.path.exists(shp_file_dir) and overwrite:
        shp_driver.DeleteDataSource(shp_file_dir)

    # create and return new shapefile object
    new_shp = shp_driver.CreateDataSource(shp_file_dir)

    # create layer if layer_name and layer_type are provided
    if kwargs.get("layer_name") and kwargs.get("layer_type"):
        # create dictionary of ogr.SHP-TYPES
        geometry_dict = {"point": ogr.wkbPoint,
                         "line": ogr.wkbMultiLineString,
                         "polygon": ogr.wkbMultiPolygon}
        # create layer
        try:
            new_shp.CreateLayer(str(kwargs.get("layer_name")),
                                geom_type=geometry_dict[str(kwargs.get("layer_type").lower())])
        except KeyError:
            print("Error: Invalid layer_type provided (must be 'point', 'line', or 'polygon').")
        except TypeError:
            print("Error: layer_name and layer_type must be string.")

    return new_shp
```

A new shapefile can then be crated with (make sure to get the directory right):


```python
a_new_shp_file = create_shp(r"" + os.getcwd() + "/geodata/shapefiles/new_polygons.shp", layer_name="basemap", layer_type="polygon")

# release data source
a_new_shape_file = None
```

{% include important.html content="A **shapefile name** may **not** have **more than 13 characters** and a **field name** may **not** have **more than 10 characters** (read more in [esri's shapefile docs](http://resources.arcgis.com/en/help/main/10.1/index.html#//005600000013000000))." %}

### Get and set shapefile projections
Information on the coordinate system is avaible through `shp_layer.GetSpatialRef()` 


```python
shp_srs = shp_layer.GetSpatialRef()
print(shp_srs)
```

    GEOGCS["GCS_WGS_1984",
        DATUM["WGS_1984",
            SPHEROID["WGS_84",6378137.0,298.257223563]],
        PRIMEM["Greenwich",0.0],
        UNIT["Degree",0.0174532925199433]]
    

This `GEOGCS` definition of the above shapefile corresponds to *Esri*'s *well-known* text. The *Open Geospatial Consortium* (*OGC*) uses a different well-known text as in their `EPSG:XXXX` definitions (e.g., available at [spatialreference.org](http://www.spatialreference.org)):


```python
GEOGCS["WGS 84",
       DATUM["WGS_1984", SPHEROID["WGS84", 6378137, 298.257223563, AUTHORITY["EPSG", "7030"]], AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich", 0, AUTHORITY["EPSG", "8901"]],
       UNIT["degree",0.01745329251994328, AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]
```

To redefine or newly define the coordinate system of a shapefile we can use [spatialreference.org](http://www.spatialreference.org) within *Python* default `urllib` library.
{% include note.html content="This action requires an internet connection." %}


```python
import urllib

# function to get spatialreferences based on psg code
def get_epsg_code(epsg):    
    # usage get_epsg_code(4326)
    try:
        with urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/esriwkt/".format(epsg)) as response:
            return str(response.read()).strip("b").strip("'")
    except Exception:
        pass
    try:
        with urllib.request.urlopen("http://spatialreference.org/ref/sr-org/epsg{0}-wgs84-web-mercator-auxiliary-sphere/esriwkt/".format(epsg)) as response:
            return str(response.read()).strip("b").strip("'")
    except Exception:
        print("ERROR: Could not find epsg code on spatialreference.org. Returning default WKT(epsg=4326).")
        return 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
```

This function can then be used to create a new projection file:


```python
# open the hypy-area shapefile
shp_file = "hypy-area"

# create new .prj file for the shapefile (.shp and .prj must have the same name)
with open("geodata/shapefiles/{0}.prj".format(shp_file), "w") as prj:
    epsg_code = get_epsg_code(4326)
    prj.write(epsg_code)
    print("Wrote projection file : " + epsg_code)
```

    Wrote projection file : GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]
    

### Add fields and point features to a shapefile

A shapefile feature can be a point, a line, or a polygon, which has field attributes (e.g., `"id"=1` to describe that this is polygon number 1 or associated to an `id` block 1). Field attributes can be more than just an *ID*entifier and include for example the polygon area or city labels as in the example shown above (`shp_driver.Open("geodata/shapefiles/cities.shp")`). 

To **create a point shapefile**, we can use the above `create_shp` function and set its projection with the `get_epsg_code` function. The following code block shows the usage of both functions to create a `river.shp` point shapefile that contains three points located at three rivers in central Europe. The code block also illustrates the creation of a field in the attribute table and the creation of three point features.

* The shapefile is located in the `rivers_pts` variable. Note that the `layer_type` already determines the type of geometries that can be used in the shapefile. For example, adding a line or polygon feature to a `ogr.wkbPoint` layer will result in an `ERROR 1` message.
* The `basemap` (layer) is attributed to the variable `lyr = river_pts.GetLayer()`.
* A *string* type field is added an appended to the attribute table:
    - instantiate a new field with `field_gname = ogr.FieldDefn("FIELD-NAME", ogr.OFTString)` (the field name may not have more than 10 characters!)
    - append the new field to the shapefile with `lyr.CreateField(field_gname)` 
    - other field types than `OFTString` can be: `OFTInteger`, `OFTReal`, `OFTDate`, `OFTTime`, `OFTDateTime`, `OFTBinary`, `OFTIntegerList`, `OFTRealList`, or `OFTStringList`.
* Add three points stored in `pt_names = {RIVER-NAME: (x-coordinate, y-coordinate)}` in a loop over the dictionary keys:
    - for every new point, create a feature as a child of the layer defintions with `feature = ogr.Feature(lyr.GetLayerDefn())`
    - set the value of the field name for each point with `feature.SetField(FIELD-NAME, FIELD-VALUE)`
    - create a string of the new point in *WKT* format with `wkt = "POINT(X-COORDINATE Y-COORDINATE)"`
    - convert the *WKT* formatted point into a point-type geometry with `point = ogr.CreateGeometryFromWkt(wkt)`
    - set the new point as the new feature's geometry with `feature.SetGeometry(point)`
    - append the new feature to the layer with `lyr.CreateFeature(feature)`
* Unlock (release) the shapefile by overwriting the `lyr` and `river_pts` variable with `None`.


```python
shp_dir = r"" + os.getcwd() + "/geodata/shapefiles/rivers.shp"
# print(shp_dir)
river_pts = create_shp(shp_dir, layer_name="basemap", layer_type="point")

# create .prj file for the shapefile for web application references
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_epsg_code(3857))

# get basemap layer
lyr = river_pts.GetLayer()

# add string field "rivername"
field_gname = ogr.FieldDefn("rivername", ogr.OFTString)
lyr.CreateField(field_gname)

# names and coordinates of central EU rivers in EPSG:3857 WG84 / Pseudo-Mercator
pt_names = {"Aare": (916136.03, 6038687.72),
            "Ain": (623554.12, 5829154.69),
            "Inn": (1494878.95, 6183793.83)}

# add the three rivers as points to the basemap layer
for n in pt_names.keys():
    # create Feature as child of the layer
    pt_feature = ogr.Feature(lyr.GetLayerDefn())
    # define value n (river) in the rivername field
    pt_feature.SetField("rivername", n)
    # use WKT format to add a point geometry to the Feature
    wkt = "POINT(%f %f)" % (float(pt_names[n][0]), float(pt_names[n][1]))
    point = ogr.CreateGeometryFromWkt(wkt)
    pt_feature.SetGeometry(point)
    # append the new feature to the basement layer
    lyr.CreateFeature(pt_feature)
    
# release files
lyr = None
river_pts = None
```

The resulting `rivers.shp` shapefile can be imported in [*QGIS*](geo_software.html#qgis) along with a DEM from the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip).
{% include image.html file="qgis-rivers.png" alt="qgis-rivers" caption="The newly created rivers.shp shapefile shown in QGIS." %}

### Multiline (polyline) shapefile
Similar to the procedure for creating and adding points to a new point shapefile, a (multi) line (or polyline) can be added to a shapefile. The `create_shp` creates a multi-line shapefile when the layer type is defined as `"line"`. The coordinate system is created with the above-defined `get_gps_code` function.
{% include tip.html content="The term *multi-line* is used in *OGC* and `ogr`, while *polyline* is used in *Esri* GIS environments." %}
The following code block uses the coordinates of cities along the *Rhine* stored in a *dictionary* named `station_names`. The city names are not used, and only the coordinates are appended with `line.AddPoint(X, Y)`. As before, a field is created to give the river a name. The actual line feature is again created as a child of the layer with `line_feature = ogr.Feature(lyr.GetLayerDefn())`. Running this code block produces a line that approximately follows the Rhine river between France and Germany.


```python
shp_dir = r"" + os.getcwd() + "/geodata/shapefiles/rhine_proxy.shp"
# print(shp_dir)
rhine_line = create_shp(shp_dir, layer_name="basemap", layer_type="line")

# create .prj file for the shapefile for web application references
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_epsg_code(3857))

# get basemap layer
lyr = rhine_line.GetLayer()

# coordinates for EPSG:3857 WG84 / Pseudo-Mercator
station_names = {"Basel": (844361.68, 6035047.42),
                 "Kembs": (835724.27, 6056449.76),
                 "Breisach": (842565.32, 6111140.43),
                 "Rhinau": (857547.04, 6158569.58),
                 "Strasbourg": (868439.31, 6203189.68)}

# create line object and add points from station names
line = ogr.Geometry(ogr.wkbLineString)
for stn in station_names.values():
    line.AddPoint(stn[0], stn[1])

# create field named "rives"
field_name = ogr.FieldDefn("river", ogr.OFTString)
lyr.CreateField(field_name)

# create feature, geometry, and field entry
line_feature = ogr.Feature(lyr.GetLayerDefn())
line_feature.SetGeometry(line)
line_feature.SetField("river", "Rhine")

# add feature to layer
lyr.CreateFeature(line_feature)

lyr = None
rhine_line = None
```

The resulting `rhine_proxy.shp` shapefile can be imported in [*QGIS*](geo_software.html#qgis) along with a DEM and the cities point shapefile from the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip).
{% include image.html file="qgis-rhine.png" alt="qgis-rhine" caption="The newly created rhine_proxy.shp multiline (poly) shapefile shown in QGIS." %}

### Polygon shapefile


```python
pass
```

### Transform (re-project) a shapefile 
For whatever reason, sometimes we do not just want to rewrite a `.prj` file, but project all objects of a shapefile into another plane. For example, we may want to project a shapefile in `EPSG:4326` onto `EPSG:3857` in order to use the shapefile in a web application.



```python
pass
```

