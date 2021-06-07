(qgis-prepro-tm)=
# Pre-processing

```{admonition} Requirements
:class: attention
Before diving into this tutorial make sure to:

* Follow the installation instructions for {ref}`qgis-install` in this eBook.
* Read (or watch) and understand this eBook's {ref}`qgis-tutorial`.
```

The first steps in numerical modeling of a river consist in the conversion of a Digital Elevation Model (**{term}`DEM`**) into a computational mesh. This tutorial guides through the creation of a QGIS project for converting a {term}`DEM` ({term}`GeoTIFF`) into a computational mesh that can be used with various numerical modeling software featured in this eBook. At the end of this tutorial, {ref}`chpt-telemac` users will have generated a computational mesh in the SELAFIN format.

```{admonition} Platform compatibility
:class: tip
All software applications featured in this tutorial can be run on *Linux*, *Windows*, and *macOS* (in theory - not tested) platforms. Note that some numerical models, such as {ref}`chpt-basement`, will not work on *macOS* platforms.
```

(tm-qgis-prepro)=
## QGIS

### Create a New Project
Launch QGIS and {ref}`create a new QGIS project <qgis-project>` to get started with this tutorial. As featured in the {ref}`qgis-tutorial`, set up a coordinate reference system (CRS) for the project. This example uses data of a river in Bavaria (UTM zone 33N), which requires the following CRS:

* In the QGIS top menu go to **Project** > **Properties**.
* Activate the **CRS** tab.
* Enter `UTM zone 33N` and select the CRS shown in {numref}`Fig. %s <qgis-crs-utm33n>`.
* Click **Apply** and **OK**.

Note that the CRS used with TELEMAC differs from the one used with BASEMENT to enable the compatibility of geospatial data products from QGIS with {ref}`Blue Kenue <bluekenue>`.

```{figure} ../img/qgis/crs-utm-33n.png
:alt: qgis set coordinate reference system crs germany utm zone 33n Inn river
:name: qgis-crs-utm33n

Define UTM zone 33N (WGS84) as project CRS.
```

```{admonition} Save the project...
:class: tip
Save the QGIS project (**Project** > **Save As...**), for example, under the name **prepro-tutorial.qgz**.
```

(get-dem-xyz)=
### Load DEM.xyz

This tutorial uses height information that is stored in an `*.xyz` file derived from the {term}`GeoTIFF` {term}`DEM` used in the {ref}`pre-processing for BASEMENT <qgis-prepro-bm>`. The `*.xyz` file can be [downloaded here](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/dem.xyz) and it was created using the workflow described in the {ref}`QGIS tutorial <make-xyz>`. Since the underlying raster file was created in the coordinate system `Germany_Zone_4`, the DEM must be imported into QGIS as follows:

* From QGIS top menu open **Layer** > **Add Layer** > **Add Delimited Text Layer...**
* In the opening **Data Source Manager** window (see {numref}`Fig. %s <qgis-import-xyz>`) make the following definitions:
  * Select the downloaded `dem.xyz` file in the **file name** field.
  * In the **File Format** frame make sure to select **Custom delimiters** and check the **Space** delimiter box.
  * In the **Record and Fields Options** frame, set the **Number of header lines to discard** to `13` and check the **First record has field names** box.
  * In the **Geometry Definition** frame, select `:EndHeader` as **X field**, `field_2` as **Y field**, and `field_3` as **Z field**. Select `ESRI:31494 - Germany_Zone_4` as **Geometry CRS**.
  * Click **Add** and **Close** the *Data Source Manager* window.

```{figure} ../img/qgis/import-dem-xyz.png
:alt: qgis import XYZ point cloud file dem
:name: qgis-import-xyz

Import the `*.xyz` point cloud as QGIS layer.
```

The **dem** (`*.xyz`) file should now be visible in the form of a point cloud in the viewport and be listed in the **Layers** panel. **Right-click** on the **dem** layer and select **Zoom to Layer(s)** to view the layer.

```{admonition} What are QGIS panels and how can I order layers?
:class: tip
Learn more in the *QGIS* tutorial on {ref}`qgis-tbx-install`.
```

The DEM should now be displayed on the map (if not: right-click on the DEM layer and click on **Zoom to Layer(s)** in the context menu) as shown in {numref}`Fig. %s <qgis-dem-basemap>`.

```{figure} ../img/qgis/dem-basemap.png
:alt: qgis import raster DEM basemap
:name: qgis-dem-xyz

The imported DEM on a Google Satellite imagery basemap (source: Google / GeoBasis-DEBKG 2019). The flow direction is from left to right following the **Q** arrow.
```

```{admonition} From LiDAR point clouds to a Raster DEM
:class: tip
Terrain survey data are mostly delivered in the shape of an x-y-z point dataset. LiDAR produces massive point clouds, which quickly overcharge even powerful computers. Therefore, LiDAR data may need to be broken down into smaller zones of less than approximately 106 points and special LiDAR point processing software (e.g., [LAStools](http://lastools.org/)) may be helpful in this task. The range of possible data products and shapes from terrain survey is board and this tutorial exemplary uses a set of x-y-z points stored within a text file.
```

(make-tm-lines)=
### Create and Draw Lines

Create and draw

* {ref}`Line Shapefile <create-line-shp>` containing model boundaries and internal breaklines between model regions with different characteristics (section on {ref}`boundary`);
* {ref}`Line Shapefile <create-line-shp>` containing model boundaries for assigning inflow and outflow conditions (section on {ref}`liquid-boundary`); and a
* {ref}`Point Shapefile <create-point-shp>` containing markers for the definition of characteristics of model regions (section on {ref}`regions`).

These two shapefiles enable to {ref}`qualm`. Ultimately, height information is {ref}`interpolated to the quality mesh <qualm-interp>` and the resulting mesh is saved as {term}`SMS 2dm` file. The next sections walk through the procedure step by step with detailed explanations. Additional materials and intermediate data products are provided in the supplemental data repository ([materials-bm](https://github.com/hydro-informatics/materials-bm)) for this tutorial.



(tm-boundary)=
### Model Boundary and Breaklines

The model boundary defines the model extent and can be divided into regions with different characteristics (e.g., roughness values) through breaklines. Breaklines indicate, for instance, channel banks and the riverbed (main channel), and need to be inside the DEM extents. Boundary lines and breaklines a stored in a {ref}`Line Shapefile <create-line-shp>` that BASEmesh uses to find both model boundaries and internal breaklines between model regions. For this purpose, {ref}`create-line-shp` with **one Text Field** called **LineType** and call it **breaklines.shp** (**Layer** > **Create Layer** > **New Shapefile Layer**). Click on *QGIS*' **Layers** menu > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <tm-qgis-new-lyr>`).

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: tm-qgis-new-lyr

Create a new shapefile from QGIS' Layers menu.
```

It is important that the lines do not overlap to avoid ambiguous or missing definitions of regions and to ensure that all boundary lines form closed regions (areas). Therefore, activate snapping:

* Activate the *Snapping Toolbar*: **View** > **Toolbars** > **Snapping Toolbar**
* In the **Snapping toolbar** > **Enable Snapping** <img src="../img/qgis/snapping-horseshoe.png">
* Enable snapping for
  * **Vertex**, **Segment**, and **Middle of Segments** <img src="../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../img/qgis/snapping-intersection.png">.

Next, start to edit **breaklines.shp** by clicking on the yellow pen <img src="../img/qgis/yellow-pen.png"> and draw the lines indicated in {numref}`Fig. %s <tm-breaklines>` by activating **Add Line Feature** <img src="../img/qgis/sym-add-line.png">.

* **Boundaries of the** model at the left and the right **floodplain limits**:
  * Delineate the outer bounds of the floodplains.
  * Make sure that all points and lines are inside the {ref}`DEM layer <get-dem>`.
  * Do not cross the river (wetted area indicated by the satellite imagery basemap).
  * **Finalize** every line with a **right-click**.
  * For the **LineType** field use text values such as **boundary left/right floodplain**.
  * Refer to the **red lines in {numref}`Fig. %s <tm-breaklines>`**.
* **Breaklines of the left bank (LB) and right bank (RB)**:
  * Draw lines along the wetted main channel indicated in the satellite imagery basemap.
  * Make sure that line ends perfectly coincide with the before-created floodplain boundary lines (this is where snapping helps); thus, the main channel's hard breaklines and the floodplain boundary lines need to enclose the floodplains without any gap between the lines.
  * For the **LineType** field use text values such as **hardline LB/RB**.
  * Refer to the **yellow-orange lines in {numref}`Fig. %s <breaklines>`** (note the delineation of the small tributaries in the top left at the left bank and in the bottom right at the right bank).
* **Breaklines of gravel banks**:
  * Draw lines along the gravel banks that are visible in the satellite imagery basemap in the main channel.
  * Make sure that the line ends perfectly coincide with the before-created main channel breaklines (hardlines); thus, the main channel's hard breaklines and the gravel bank breaklines need to enclose the gravel banks without any gap between the lines.
  * For the **LineType** field use text values such as **hardline gravel bank**.
  * Refer to the **green-ish lines in {numref}`Fig. %s <breaklines>`**.
* Optional: **Breaklines of block ramps**:
  * Find the rough block ramps (effervescing waters) in the satellite imagery basemap and delineate them by drawing lines across the wetted main channel.
  * Make sure that the line ends perfectly coincide with the main channel breaklines; thus, the main channel's hard breaklines and the block ramp breaklines need to enclose the block ramps without any gap between the lines.
  * For the **LineType** field use text values such as **hardline sss** (or anything else - the example refers to the German word <u>S</u>chütt<u>s</u>tein<u>s</u>chwelle).
  * Refer to the **blue lines in {numref}`Fig. %s <breaklines>`**.
* Optional: **Breakline of a sandbank**:
  * Find the sandbank deposit in the upper left corner in {numref}`Fig. %s <breaklines>` on the satellite imagery basemap and delineate it by drawing a smoothly curved line.
  * Make sure that the line ends perfectly coincide with the main channel breaklines and embrace a closed area without any gap between the lines.
  * For the **LineType** field use text values such as **hardline sand**.
  * Refer to the **purple line** in the upper left corner **in {numref}`Fig. %s <breaklines>`**.

To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">. Finally, save the new lines (edits of **breaklines.shp**) by clicking on the **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.

```{figure} ../img/qgis/breaklines.png
:alt: qgis basement basemesh draw breaklines boundaries
:name: tm-breaklines

Boundary and breaklines to draw in **breaklines.shp**. Left and right banks and floodplains are orientated in the flow direction (**Q** arrow).
```

```{admonition} Troubles with drawing boundaries and breaklines?
:class: tip
Download the [zipped breaklines shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/breaklines.zip) shown in the above figure and unpack it into the project folder, for instance, `/Project Home/shapefiles/breaklines.[SHP]`.
```

The default layer style is **Single Symbol**. For better representation, double-click on the breaklines layer, go to the **Symbology** tab and select **Categorized** (or **Graduated**) instead of **Single Symbol** (at the very top of the **Layer Properties** window). In the **Value** field, select **LineType**, then click the **classify** button on the bottom of the **Layer Properties** window. The listbox will now show the *LineType* values.

```{admonition} Draw boundaries of complex DEMs...
:class: tip
Drawing boundaries manually around large {term}`DEM`s can be very time consuming, in particular, if the raw data are a point cloud and not yet converted to a {ref}`raster`.

If you are dealing with a point cloud, consider using *QGIS* [Convex Hull tool](https://docs.qgis.org/3.16/en/docs/training_manual/vector_analysis/spatial_statistics.html?highlight=convex%20hull#basic-fa-create-a-test-dataset) that draws a tight bounding polygon around points.

If you are dealing with a large {term}`GeoTIFF`, consider using QGIS' [Raster to Vector](https://docs.qgis.org/3.16/en/docs/training_manual/complete_analysis/raster_to_vector.html) tool.
```


(tm-liquid-boundary)=
### Liquid (Hydraulic) Boundaries

The liquid boundaries define where hydraulic conditions, such as a given discharge or stage-discharge relationship, apply at the model inflow (upstream) and outflow (downstream) limits. Thus, a functional river model requires at least one inflow boundary (line) where mass flow into the model and one outflow boundary (line) where mass fluxes leave the model. For this purpose, {ref}`create-line-shp` called **liquid-boundaries.shp** and define **two text data fields** named **type** and **stringdef**. Make sure that **snapping** is still **enabled** (as above explained in the {ref}`boundary` section) and **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **liquid-boundaries.shp**. Then draw two lines:

* Activate **Add Line Feature** <img src="../img/qgis/sym-add-line.png">.
* Draw an inflow boundary line (see also {numref}`Fig. %s <inflow-boundary>`):
  * Zoom to the inflow region of the DEM limits, where there is a **gap between** the above-created **floodplain boundary breaklines**.
  * Start drawing a line on the left bank (left side of the below figure) and moved Eastwards (i.e., to the right) to make seven more points across the river.
  * The **seventh point** needs to **coincide** with the end of the right bank's **floodplain boundary breakline**.
  * Thus, the upstream flow is coming from the right-hand side of the inflow boundary line (i.e., the upstream flow direction will be `right` for the numerical model).
  * **Finalize** the line with a **right-click**, and enter `Inflow` in the **type** field and `inflow` in the **stringdef** field (the case matters).
  * To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/inflow-boundary.png
:alt: qgis basemesh draw inflow boundary line
:name: tm-inflow-boundary

The inflow boundary line is drawn from the left to the right (i.e., the upstream flow is coming from the right-hand side of the inflow boundary line). The sequence of buttons to use is highlighted by the red boxes.
```

* Next, draw an outflow boundary line (see also {numref}`Fig. %s <outflow-boundary>`):
  * Zoom to the outflow region of the DEM limits, where there is a **gap between** the above-created **floodplain boundary breaklines**.
  * Start drawing a line on the left bank (top of the below figure) and move Southwestwards (i.e., to the bottom) to make seven more points across the river.
  * The **seventh point** needs to **coincide** with the end of the right bank's **floodplain boundary breakline**.
  * Thus, the upstream flow is coming from the right-hand side of the outflow boundary line (i.e., the upstream flow direction will be `right` for the numerical model).
  * **Finalize** the line with a **right-click**, and enter `Outflow` in the **type** field and `outflow` in the **stringdef** field (the case matters).
  * To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/outflow-boundary.png
:alt: qgis basemesh draw outflow boundary line
:name: tm-outflow-boundary

The outflow boundary line is drawn from the top to the bottom (i.e., the upstream flow is coming from the right hand-side of the outflow boundary line).
```

```{admonition} Constraints of inflow and outflow boundaries
:class: important
The inflow and outflow boundary lines must have the same number of nodes (here 7 plus 1) and no liquid boundary line may have more than 40 nodes.
```

Finally, save the liquid boundary lines (edits of **liquid-boundaries.shp**) by clicking on the **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.

```{admonition} Troubles with drawing the liquid boundary lines?
:class: tip
Download the [zipped liquid-boundaries shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/liquid-boundaries.zip) and unpack it into the project folder, for instance, `/Project Home/shapefiles/liquid-boundaries.[SHP]`.
```

## Blue Kenue

(submesh)=
### Create Sub-meshes

empty
