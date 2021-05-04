# Shapefile (vector dataset) handling

Summary: Geospatial analysis of shapefile with gdal, ogr and osr.

```{admonition} Requirements
Make sure to understand [shapefiles](geospatial-data.html#shp) and [vector data](geospatial-data.html#vector) before reading this section.
```

```{tip}
The core functions used in this e-book are introduced with the raster and vector data handling explanations and additionally implemented in the {{ ft_url }} package.
```

## Load an existing shapefile

`gdal`'s `ogr` module is an excellent source for handling shapefiles. To open a shapefile in *Python*, we need to instantiate the correct driver (`"ESRI Shapefile"` for shapefiles) first. With the driver object (`ogr.GetDriverByName("SHAPEFILE")`), we can then open (instantiate) a shapefile (object with `shp_driver.Open("SHAPEFILE")`), which contains layer information. It is precisely this layer information (i.e., references to shapefile attributes) that we want to work with. Therefore we have to instantiate a shapefile layer object with `shp_dataset.GetLayer()`.

from gdal import ogr
shp_driver = ogr.GetDriverByName("ESRI Shapefile")
shp_dataset = shp_driver.Open("geodata/shapefiles/cities.shp")
shp_layer = shp_dataset.GetLayer()

```{tip}
To get a full list of supported `ogr` drivers (e.g., for `DXF`, `ESRIJSON`, `GPS`, `PDF`, `SQLite`, `XLSX`, and many more), [download the script `get_ogr_drivers.py`](https://github.com/hydro-informatics/material-py-codes/raw/master/geo/get_ogr_drivers.py) from the course repository (script available during courses only).
```

(create-shp)=
## Create a New Shapefile 

The `ogr` module also enables creating a new point, line or polygon shapefile. The following code block defines a function for creating a shapefile, where the optional keyword argument `overwrite` is used to control whether an existing shapefile with the same name should be overwritten (default: `True`).
The command `shp_driver.CreateDataSource(SHP-FILE-DIR)` creates a new shapefile and the rest of the function adds a layer to the shapefile if the optional keyword arguments `layer_name` and `layer_type` are provided. Both optional keywords must be *string*s, where `layer_name` can be any name for the new layer. `layer_type` must be either `"point"`, `"line"`, or `"polygon"` to create a point, (poly)line, or polygon shapefile respectively. The function uses the `geometry_dict` dictionary to assign the correct `ogr.SHP-TYPE` to the layer. There are more options for extending the `create_shp(...)` function listed on [*pcjerick*'s github pages](https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html).


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
        except AttributeError:
            print("Error: Cannot access layer - opened in other program?")
    return new_shp

The `create_shp` function is also provided with the in the {{ ft_url }} package ([*flusstools.geotools.shp_mgmt.py*](https://flusstools.readthedocs.io/en/latest/geotools.html#module-flusstools.geotools.shp_mgmt)) and aids to create a new shapefile (make sure to get the directory right):

a_new_shp_file = create_shp(r"" + os.getcwd() + "/geodata/shapefiles/new_polygons.shp", layer_name="basemap", layer_type="polygon")

# release data source
a_new_shape_file = None

```{important}
A **shapefile name** may **not** have **more than 13 characters** and a **field name** may **not** have **more than 10 characters** (read more in [*Esri*'s shapefile docs](http://resources.arcgis.com/en/help/main/10.1/index.html#//005600000013000000)).
```

Shapefiles can also be created and drawn in [*QGIS*](../get-started/geo.html#qgis) and the following figures guide through the procedure of creating of a polygon shapefile. We will not need this shapefile on this page, but for the later on interaction with raster datasets. So the shapefile creation with *QGIS* is just a note here.

The first step to make a shapefile with *QGIS* is obviously to run *QGIS* and create a new project. The following example uses water depth and flow velocity raster data as background information to delineate a so-called [*morphological unit* of *slackwater*](https://www.sciencedirect.com/science/article/pii/S0169555X14000099). Both the water depth and flow velocity rasters are part of the [*River Architect* sample datasets](https://github.com/RiverArchitect/SampleData/archive/master.zip) (precisely located in  [`RiverArchitect/SampleData/01_Conditions/2100_sample/`](https://github.com/RiverArchitect/SampleData/tree/master/01_Conditions/2100_sample)). After downloading the sample data, they can be imported in *QGIS* by dragging the files from the *Browser* tab into the *Layers* tab. Then:

![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/qgis-create-shp.png)
![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/qgis-new-shp.png)
![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/qgis-toggle-editing.png)
![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/qgis-draw-polygon.png)

We will come back to these descriptions and use this shapefile on the *Raster handling* page.

(prj-shp)=
## Get and Set Shapefile Projections 

The terminology used in the `.prj` files of a shapefile corresponds to the defintions in the [geospatial data](geospatial-data.html#prj) section. In *Python*, information on the coordinate system is available through `shp_layer.GetSpatialRef()` of the `ogr` library:

shp_srs = shp_layer.GetSpatialRef()
print(shp_srs)

This `GEOGCS` definition of the above shapefile corresponds to *Esri*'s *well-known* text. Since the shapefile format was developed by *Esri*, *Esri*'s *WKT* (***esriwkt***) format must be used in `.prj` files. The *Open Geospatial Consortium* (*OGC*) uses a different well-known text as in their `EPSG:XXXX` definitions (e.g., available at [spatialreference.org](http://www.spatialreference.org)). 

```java
GEOGCS["WGS 84",
       DATUM["WGS_1984", SPHEROID["WGS84", 6378137, 298.257223563, AUTHORITY["EPSG", "7030"]], AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich", 0, AUTHORITY["EPSG", "8901"]],
       UNIT["degree",0.01745329251994328, AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]
```

To redefine or newly define the coordinate system of a shapefile we can use [spatialreference.org](http://www.spatialreference.org) within *Python* default `urllib` library.

```{note}
The following code block requires an internet connection.
```

import urllib

# function to get spatialreferences with epsg code
def get_esriwkt(epsg):    
    # usage get_epsg_code(4326)
    try:
        with urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/esriwkt/".format(epsg)) as response:
            return str(response.read()).strip("b").strip("'")
    except Exception:
        pass
    try:
        with urllib.request.urlopen("http://spatialreference.org/ref/sr-org/epsg{0}-wgs84-web-mercator-auxiliary-sphere/esriwkt/".format(epsg)) as response:
            return str(response.read()).strip("b").strip("'")
        # sr-org codes are available at "https://spatialreference.org/ref/sr-org/{0}/esriwkt/".format(epsg)
        # for example EPSG:3857 = SR-ORG:6864 -> https://spatialreference.org/ref/sr-org/6864/esriwkt/ = EPSG:3857
    except Exception:
        print("ERROR: Could not find epsg code on spatialreference.org. Returning default WKT(epsg=4326).")
        return 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'

This function can then be used to create a new projection file:

# open the hypy-area shapefile
shp_file = "hypy-area"

# create new .prj file for the shapefile (.shp and .prj must have the same name)
with open("geodata/shapefiles/{0}.prj".format(shp_file), "w") as prj:
    epsg_code = get_esriwkt(4326)
    prj.write(epsg_code)
    print("Wrote projection file : " + epsg_code)

An offline alternative for generating `.prj` files is the `osr` library that comes along with `gdal`.

from gdal import osr

def get_wkt(epsg, wkt_format="esriwkt"):
    default = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'
    spatial_ref = osr.SpatialReference()
    try:
        spatial_ref.ImportFromEPSG(epsg)
    except TypeError:
        print("ERROR: epsg must be integer. Returning default WKT(epsg=4326).")
        return default
    except Exception:
        print("ERROR: epsg number does not exist. Returning default WKT(epsg=4326).")
        return default
    if wkt_format=="esriwkt":
        spatial_ref.MorphToESRI()
    # return a nicely formatted WKT string (alternatives: ExportToPCI(), ExportToUSGS(), or ExportToXML())
    return spatial_ref.ExportToPrettyWkt()

## Transform (Re-project) a Shapefile

To apply a different projection to geometric objects of a shapefile it is not enough to simply rewrite the `.prj` file. A re-projection may be needed if, we want to use a shapefile in `EPSG:4326` (e.g., created wioth *QGIS*) onto `EPSG:3857` in order to use the shapefile in a web application. The following example shows the re-projection of the `countries.shp` shapefile (source: the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip)). For now, just look at the sequence of steps (the creation of fields an features follows in the sections below):
* The shapefile to transform is located in the subdirectory `geodata/shapefiles/countries.shp` and opened with as above described.
* Read and identify the spatial reference system used in the input shapefile 
    - Create a spatial reference object with `in_sr = osr.SpatialReference(str(shapefile.GetSpatialRef()))`.
    - Detect the spatial reference system in *EPSG* format with `AutoIdentifyEPSG()`.
    - Assign the *EPSG*-formatted spatial reference system to the spatial reference object of the input shapefile (`ImportFromEPSG(int(in_sr.GetAuthorityCode(None)))`).
* Create the output spatial reference with `out_sr = osr.SpatialReference()` and apply the target *EPSG* code (`out_sr.ImportFromEPSG(3857)`).
* Create a coordinate transformation object (`coord_trans = osr.CoordinateTransformation(in_sr, out_sr)`) that enables re-projecting geometry objects later.
* Create the output shapefile, which will correspond to a copy of input shapefile (use the above-defined `create_shp` function with `layer_name="basemap"` and `layer_type="line"`).
* Copy the field names and type of the input shapefile:
    - Read the attribute layer from the input file's layer definitions with `in_lyr_def = in_shp_lyr.GetLayerDefn()`
    - Iterate through the field definitions and append them to the output shapefile layer (`out_shp_lyr`)
* Iterate through the geometry features in the input shapefile:
    - Use the new (output) shapefile's layer definitions (`out_shp_lyr_def = out_shp_lyr.GetLayerDefn()`) to append transformed geometry objects later.
    - Define an iteration variable `in_feature` as an instance of `in_shp_lyr.GetNextFeature`.
    - In a `while` loop, instantiate every geometry (`geometry = in_feature.GetGeometryRef()`) in the input shapefile, transform the `geometry` (`geometry.Transform(coord_trans)`), convert it to an `ogr.Feature()` with the `SetGeometry(geometry)` method, copy field definitions (nested `for`-loop), and append the new feature to the output shapefile layer (`out_shp_lyr_def.CreateFeature(out_feature)`).
    - At the end of the `while`-loop, look for the next feature in the input shapefile's attributes with `in_feature = in_shp_lyr.GetNextFeature()`
* Unlock (release) all layers and shapefiles by overwriting the objects with `None` (nothing is literally written to any file as long as these variables exist!).
* Assign the new projection *EPSG:3857* using the above-defined `get_wkt` function.

from gdal import ogr
from gdal import osr

shp_driver = ogr.GetDriverByName("ESRI Shapefile")

# open input shapefile and layer
in_shp = shp_driver.Open(r"" + os.path.abspath('') + "/geodata/shapefiles/countries.shp")
in_shp_lyr = in_shp.GetLayer()

# get input SpatialReference
in_sr = osr.SpatialReference(str(in_shp_lyr.GetSpatialRef()))
# auto-detect epsg
in_sr.AutoIdentifyEPSG()
# assign input SpatialReference
in_sr.ImportFromEPSG(int(in_sr.GetAuthorityCode(None)))

# create SpatialReference for new shapefile
out_sr = osr.SpatialReference()
out_sr.ImportFromEPSG(3857)

# create a CoordinateTransformation object
coord_trans = osr.CoordinateTransformation(in_sr, out_sr)

# create output shapefile and get layer
out_shp = create_shp(r"" + os.path.abspath('') + "/geodata/shapefiles/countries-web.shp", layer_name="basemap", layer_type="line")
out_shp_lyr = out_shp.GetLayer()

# look up layer (features) definitions in input shapefile
in_lyr_def = in_shp_lyr.GetLayerDefn()
# copy field names of input layer attribute table to output layer
for i in range(0, in_lyr_def.GetFieldCount()):
    out_shp_lyr.CreateField(in_lyr_def.GetFieldDefn(i))

# instantiate feature definitions object for output layer (currently empty)
out_shp_lyr_def = out_shp_lyr.GetLayerDefn()

# iteratively append all input features in new projection
in_feature = in_shp_lyr.GetNextFeature()
while in_feature:
    # get the input geometry
    geometry = in_feature.GetGeometryRef()
    # re-project (transform) geometry to new system
    geometry.Transform(coord_trans)
    # create new output feature
    out_feature = ogr.Feature(out_shp_lyr_def)
    # assign in-geometry to output feature and copy field values
    out_feature.SetGeometry(geometry)
    for i in range(0, out_shp_lyr_def.GetFieldCount()):
        out_feature.SetField(out_shp_lyr_def.GetFieldDefn(i).GetNameRef(), in_feature.GetField(i))
    # add the feature to the shapefile
    out_shp_lyr.CreateFeature(out_feature)
    # prepare next iteration
    in_feature = in_shp_lyr.GetNextFeature()

# release shapefiles and layers
in_shp = None
in_shp_lyr = None
out_shp = None
out_shp_lyr = None

# create .prj file for  output shapefile for web application references
with open(r"" + os.path.abspath('') + "/geodata/shapefiles/countries-web.prj", "w+") as prj:
    prj.write(get_wkt(3857))

```{admonition} Challenge
Re-write the above code block into a `re_project(shp_file, target_epsg)` function.
```

The code sequence `in_sr.AutoIdentifyEPSG()` should return `0` for known `EPSG` numbers. Unfortunately, many EPSG numbers are not known to the `AutoIdentifyEPSG()` method. In the case that `AutoIdentifyEPSG()` did not function propperly, the method does not return the value `0`, but for example `7`. A workaround for the limited functionality of `srs.AutoIdentifyEPSG()` is `srs.FindMatches`. `srs.FindMatches` returns a *matching* `srs_match` from a larger database, which is somewhat nested, for example:<br>

```python
matches = srs.FindMatches()
```

Then, `matches` looks like this: `[(osgeo.osr.SpatialReference, INT)]`. Therefore, a complete workaround for `srs.AutoIdentifyEPSG()` (or `in_sr.AutoIdentifyEPSG()` in the code block above) looks like this:

# set epsg and create spatial reference object
epsg = 3857
srs = osr.SpatialReference()
srs.ImportFromEPSG(epsg)

# identify spatial reference
auto_detect = srs.AutoIdentifyEPSG()
if auto_detect is not 0:
    srs = srs.FindMatches()[0][0]  # Find matches returns list of tuple of SpatialReferences
    srs.AutoIdentifyEPSG()  # Re-perform auto-identification

(add-field)=
## Add Fields and Point Features to a Shapefile 

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

```{important}
The operations are literally not written to the shapefile if the `lyr` and `river_pts` objects are not overwritten with `None`.
```

shp_dir = r"" + os.path.abspath('') + "/geodata/shapefiles/rivers.shp"
river_pts = create_shp(shp_dir, layer_name="basemap", layer_type="point")

# create .prj file for the shapefile for web application references
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_esriwkt(3857))

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

The resulting `rivers.shp` shapefile can be imported in [*QGIS*](../get-started/geo.html#qgis) along with a DEM from the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip).

![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/qgis-rivers.png)

(line-create)=
## Multiline (Polyline) Shapefile 

Similar to the procedure for creating and adding points to a new point shapefile, a (multi) line (or polyline) can be added to a shapefile. The `create_shp` creates a multi-line shapefile when the layer type is defined as `"line"`. The coordinate system is created with the above-defined `get_gps_code` function.

```{tip}
The term *multi-line* is used in *OGC* and `ogr`, while *polyline* is used in *Esri* GIS environments.
The following code block uses the coordinates of cities along the *Rhine* stored in a *dictionary* named `station_names`. The city names are not used, and only the coordinates are appended with `line.AddPoint(X, Y)`. As before, a field is created to give the river a name. The actual line feature is again created as a child of the layer with `line_feature = ogr.Feature(lyr.GetLayerDefn())`. Running this code block produces a line that approximately follows the Rhine river between France and Germany.
```

shp_dir = r"" + os.path.abspath('') + "/geodata/shapefiles/rhine_proxy.shp"
rhine_line = create_shp(shp_dir, layer_name="basemap", layer_type="line")

# create .prj file for the shapefile for web application references
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_wkt(3857))

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

The resulting `rhine_proxy.shp` shapefile can be imported in [*QGIS*](../get-started/geo.html#qgis) along with a DEM and the cities point shapefile from the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip).

![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/qgis-rhine.png)

(poly-create)=
## Polygon Shapefile

Polygons are surface patches that can be created point-by-point, line-by-line, or from a `"Multipolygon"` *WKB* definition. When creating polygons from points or lines, we want to create a surface and this is why the corresponding geometry type is `wkbLinearRing` for building polygons from both point or lines (rather than `wkbPoint` or `wkbLine`, respectively). The following code block features an example for building a polygon shapefile delineating the hydraulic laboratory of the University of Stuttgart. The difference between the above example for creating a line shapefile are:

* The projection is `EPSG:4326`.
* The point coordinates are generated within an `ogr.wkbLinearRing` object step-by-step rather than in a loop over *dictionary* entries.
* File, variable, and field names.

shp_dir = r"" + os.path.abspath('') + "/geodata/shapefiles/iws_va.shp"
va_geo = create_shp(shp_dir, layer_name="basemap", layer_type="polygon")

# create .prj file for the shapefile for GIS map applications
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_wkt(4326))

# get basemap layer
lyr = va_geo.GetLayer()

# create polygon points
pts = ogr.Geometry(ogr.wkbLinearRing)
pts.AddPoint(9.103686, 48.744251)
pts.AddPoint(9.104689, 48.744198)
pts.AddPoint(9.104667, 48.743960)
pts.AddPoint(9.103557, 48.744009)

# create polygon geometry
poly = ogr.Geometry(ogr.wkbPolygon)
# build polygon geometry from points
poly.AddGeometry(pts)

# add field to classify building type
field = ogr.FieldDefn("building", ogr.OFTString)
lyr.CreateField(field)

poly_feature_defn = lyr.GetLayerDefn()
poly_feature = ogr.Feature(poly_feature_defn)
poly_feature.SetGeometry(poly)
poly_feature.SetField("building", "Versuchsanstalt")

lyr.CreateFeature(poly_feature)

lyr = None
va_geo = None

(json-create)=
## Build Shapefile from *JSON* 

Loading geometry data from a in-line defined variables is cumbersome in practice, where geospatial data are often provided on public platforms (e.g., land use or cover).  The following example uses a *JSON* file generated with map service data from the [Baden-Württemberg State Institute for the Environment, Survey and Nature Conservation *LUBW*](https://udo.lubw.baden-wuerttemberg.de/), where polygon nodes are stored in *WKB* polygon geometry format  (`"MultiPolygon (((node1_x node1_y, nodej_x, nodej_y, ... ...)))"`):

* The *JSON* file is read with [*pandas*](../python-basics/pynum.html#pandas) and the shapefile is created, as before, with the `create_shp` function.
* The projection is *EPSG:25832*.
* Two fields are added in the form of
    - `"tbg_name"` is the original string name of the polygons in the *LUBW* data,
    - `"area"` is a real number field, in which the polygon area is calculated in m<sup>2</sup> using `polygon.GetArea()`.
* The polygon geometries are derived from the *WKB*-formatted definitions in the `"wkb_geom"` field of the *pandas* data frame object `dreisam_inundation`.

# get data from json file
dreisam_inundation = pd.read_json(r"" + os.path.abspath('') + "/geodata/json/hq100-dreisam.json")

# create shapefile
shp_dir = r"" + os.path.abspath('') + "/geodata/shapefiles/dreisam_hq100.shp"
dreisam_hq100 = create_shp(shp_dir, layer_name="basemap", layer_type="polygon")

# create .prj file for the shapefile for GIS map applications
with open(shp_dir.split(".shp")[0] + ".prj", "w+") as prj:
    prj.write(get_wkt(25832))

# get basemap layer
lyr = dreisam_hq100.GetLayer()

# add string field "tbg_name"
lyr.CreateField(ogr.FieldDefn("tbg_name", ogr.OFTString))

# add string field "area"
lyr.CreateField(ogr.FieldDefn("area", ogr.OFTReal))

for wkt, tbg in zip(dreisam_inundation["wkt_geom"], dreisam_inundation["TBG_NAME"]):
    # create Feature as child of the layer
    feature = ogr.Feature(lyr.GetLayerDefn())
    # assign tbg_name
    feature.SetField("tbg_name", tbg)
    # use WKT format to add a polygon geometry to the Feature
    polygon = ogr.CreateGeometryFromWkt(wkt)
    # define default value of 0 to the area field
    feature.SetField("area", polygon.GetArea())

    feature.SetGeometry(polygon)
    # append the new feature to the basement layer
    lyr.CreateFeature(feature)

lyr = None
dreisam_hq100 = None

```{tip}
Open the new `dreisam_hq100.shp` in *QGIS* and explore the attribute table.
```

Also *GeoJSON* data can be used to create an `ogr.Geometry` with `ogr.createFromGeoJson(FILENAME)`:

from gdal import ogr
geojson_data = """{"type":"Point","coordinates":[1013452.282805,6231540.674235]}"""
point = ogr.CreateGeometryFromJson(geojson_data)
print("X=%d, Y=%d (EPSG:3857)" % (point.GetX(), point.GetY()))

(calc)=
## Calculate Geometric Attributes

The above code block illustrates the usage of `polygon.GetArea()` to calculate the polygon area n m<sup>2</sup>. The `ogr` library provides many more functions to calculate geometric attributes of features and here is a summary: 

* Unify multiple polygons <br>
    `wkt_... = ...`<br>
    `polygon_a = ogr.CreateGeometryFromWkt(wkt_1)`<br>
    `polygon_b = ogr.CreateGeometryFromWkt(wkt_2)`<br>
    `polygon_union = polygon_a.Union(polygon_b)`
* Intersect two polygons <br>
    `polygon_intersection = polygon_a.Intersection(polygon_b)`
* Envelope (minimum and maximum extents) of a polygon <br>
    `env = polygon.GetEnvelope()` <br>
    `print("minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0],env[2],env[1],env[3])`
* Convex hull (envelope surface) of multiple geometries (points, lines, polygons) <br>
    `all_polygons = ogr.Geometry(ogr.wkbGeometryCollection)`<br>
    `for feature in POLYGON-SOURCE-LAYER: all_polygons.AddGeometry(feature.GetGeometryRef())`<br>
    `convexhull = all_polygons.ConvexHull()`<br>
    Save `convexhull` to shapefile (use `create_shp` function as shown in the above examples or read more at [pcjerick's github pages](https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#save-the-convex-hull-of-all-geometry-from-an-input-layer-to-an-output-layer))<br>
    Tip: To create a tight hull (e.g., of a point cloud), look for `concavehull` functions.
* Length (of a line) <br>
    `wkt = "LINESTRING (415128.5 5320979.5, 415128.6 5320974.5, 415129.75 5320974.7)"`<br>
    `line = ogr.CreateGeometryFromWkt(wkt)`<br>
    `print("Length = %d" % line.Length())`
* Area (of a polygon):  `polygon.GetArea()` (see above example)
* Example to calculate [centroid coordinates of polygons](https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#quarter-polygon-and-create-centroids).


```{important}
The units of the geometric attribute (e.g., m<sup>2</sup>, U.S. feet, or others) are calculated based on the definitions in the {ref}`*.prj* file <prj-shp>` (recall also the definition of projections in *WKT* format in the {ref}`prj` section).
```

(export)=
## Export to Other Format

The above examples deal with `.shp` files only, but other formats can be useful (e.g., to create web applications or export to *Google Earth*). The following sections illustrate the creation of *GeoJSON* and *KML* files. Several other conversions can be performed, not only between file formats, but also between feature types. For example, polygons can be created from point clouds (among others with the `ConvexHull` method mentioned above). The interested reader can learn more about conversions in [Michael Diener's *Python Geospatial Analysis Cookbook*](https://github.com/mdiener21/python-geospatial-analysis-cookbook).




### GeoJSON
*GeoJSON* files can be easily created as before, even without activating a driver:

triangle = ogr.Geometry(ogr.wkbLinearRing)
triangle.AddPoint(-11717151.498691, 2356192.894805)
triangle.AddPoint(-11717120.446149, 2355586.175893)
triangle.AddPoint(-11719392.059083, 2354012.050842)

polygon = ogr.Geometry(ogr.wkbPolygon)
polygon.AddGeometry(triangle)

with open(r"" + os.path.abspath('') + "/geodata/geojson/pitillal-triangle.geojson", "w+") as gjson:
    gjson.write(polygon.ExportToJson())

For more robust file handling and defining a projection, activate the driver `ogr.GetDriverByName("GeoJSON")`. Thus, the creation and manipulation of *GeoJSON* files works similar to the shapefile handlers shown above. 

gjson_driver = ogr.GetDriverByName("GeoJSON")

# make spatial reference
sr = osr.SpatialReference()
sr.ImportFromEPSG(3857)

# create GeoJSON file
gjson = gjson_driver.CreateDataSource("pitillal-full.geojson")
gjson_lyr = gjson.CreateLayer("pitillal-full.geojson", geom_type=ogr.wkbPolygon, srs=sr)

# get layer feature definitions
feature_def = gjson_lyr.GetLayerDefn()
# create new feature
new_feature = ogr.Feature(feature_def)
# assign the triangle from the above code block
new_feature.SetGeometry(polygon)
# add new feature to Layer
gjson_lyr.CreateFeature(new_feature)

# close links to data sources
gjson = None
gjson_lyr = None

### KML (Google Earth)
To display point, line or polygon features in *Google Earth*, features can be plugged in to Google's [*KML*](https://developers.google.com/kml/documentation/kml_tut) (Keyhole Markup Language), similar to creation of *GeoJSON* files, with the simple function `geometry.ExportToKML`:

triangle = ogr.Geometry(ogr.wkbLinearRing)
triangle.AddPoint(-11717151.498691, 2356192.894805)
triangle.AddPoint(-11717120.446149, 2355586.175893)
triangle.AddPoint(-11719392.059083, 2354012.050842)

polygon = ogr.Geometry(ogr.wkbPolygon)
polygon.AddGeometry(triangle)

#geojson = poly.ExportToJson()
with open(r"" + os.path.abspath('') + "/geodata/pitillal-triangle.kml", "w+") as gjson:
    gjson.write(polygon.ExportToKML())

Similar to *GeoJSON* files and shapefiles, *KML* files can be generated more robustly (for example with a defined projection). All you need to do is load the *KML* driver (`kml_driver = ogr.GetDriverByName("KML")`) and define a *KML* data source (`kml_file = kml_driver.CreateDataSource(FILENAME.KML)`).

```{admonition} Exercise
Get more familiar with shapefile handling in the [geospatial ecohydraulics](../exercises/ex-geco) exercise.
```