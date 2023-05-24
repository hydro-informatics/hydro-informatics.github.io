(slf-prepro-tm)=
# Pre-processing

```{admonition} Requirements
:class: attention
This tutorial is designed for **advanced beginners** and before diving into this tutorial make sure to:

* Follow the installation instructions for {ref}`qgis-install` in this eBook.
* Read (or watch) and understand this eBook's {ref}`qgis-tutorial`.
* Install {ref}`BlueKenue <bluekenue>`.
```

The first steps in numerical modeling of a river with TELEMAC consist in the conversion of a Digital Elevation Model (**{term}`DEM`**) into a computational mesh. This tutorial guides through the creation of:

* A QGIS project for creating a computational mesh (similar to the {ref}`BASEMENT <qgis-prepro-bm>` pre-processing).
* Optionally, the mesh generation with the BlueKenue<sup>TM</sup> software is featured.
* A {ref}`BlueKenue <bluekenue>` workspace to interpolate terrain elevations from a {term}`DEM`, including the export of a mesh to the SELAFIN/SERAFIN (`*.slf`) geometry format for TELEMAC, and the definition boundary edges.

At the end of this tutorial, {ref}`chpt-telemac` users will have generated a computational mesh in the `*.slf` file format, which is ready to use for the {ref}`Telemac2d steady <telemac2d-steady>` simulation tutorial. Additional materials and intermediate data products are provided in this eBook's supplemental [telemac](https://github.com/hydro-informatics/telemac) data repository.

```{admonition} Platform compatibility
:class: tip
All software applications featured in this tutorial can be run on *Linux*, *Windows*, and also potentially *macOS* (not tested) platforms.
```

(tm-qgis-prepro)=
# QGIS

## Create and Setup a New Project
Launch QGIS and {ref}`create a new QGIS project <qgis-project>` to get started with this tutorial. As featured in the {ref}`qgis-tutorial`, set up a coordinate reference system ({term}`CRS`) for the project. This example uses data of a river in Bavaria (Germany, UTM zone 33N), which requires the following {term}`CRS`:

* In the QGIS top menu go to **Project** > **Properties**.
* Activate the **CRS** tab.
* Enter `UTM zone 33N` and select the CRS shown in {numref}`Fig. %s <qgis-crs-utm33n>`.
* Click **Apply** and **OK**.

Note that the CRS used with TELEMAC differs from the one used with BASEMENT to enable the compatibility of geospatial data products from QGIS with {ref}`BlueKenue <bluekenue>`.

```{figure} ../img/qgis/crs-utm-33n.png
:alt: qgis set coordinate reference system crs germany utm zone 33n Inn river
:name: qgis-crs-utm33n

Define UTM zone 33N (WGS84) as project CRS.
```

```{admonition} Save the project...
:class: tip
Save the QGIS project (**Project** > **Save As...**), for example, with the name **prepro-tutorial.qgz**.
```

(tm-qgis-plugins)=
## Third-party Plugins

The TELEMAC tutorials rely on the BASEmesh plugin and the *PostTelemac* plugin. To this end, **open** the **QGIS plugin manager** (**Plugins** menu > **Manage and Install Plugins**) to open the **Plugins** window ({numref}`Fig. %s <open-qgis-plugin-manager>`).

```{figure} ../img/qgis/plugin-manager-open.png
:alt: qgis basement telemac plugins manager
:name: open-qgis-plugin-manager

Open QGIS' Plugins Manager.
```

In the **Plugins** window, add both plugins as follows:

* BASEmesh requires to add the developer's plugin repository (more details are available in the {ref}`BASEMENT pre-processing <get-basemesh>` tutorial):
  * Go to the **Settings** tab.
  * Scroll to the bottom (**Plugin Repositories** listbox in {numref}`Fig. %s <qgis-plugins>`), click on **Add...**.
  * In the popup window enter:
    * a name for the new repository, for instance, `BASEmesh Plugin Repository`;
    * the repository address: [https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml).
  * Click **OK**. The new repository should now be visible in the **Plugin Repositories** listbox.
* Install the BASEmesh plugin:
  * Go to the **All** tab (still in the *Plugins* window) and enter `basemesh` in the search field.
  * Find the **newest BASEmesh** (i.e., **Available version** >= 2.0.0) plugin and click on **Install Plugin**.
* To install the [**PostTelemac** plugin](https://github.com/Artelia/PostTelemac/wiki#T45) type `posttelemac` in the **All** tab and click on **Install Plugin**.
* After the successful installation **Close** the **Plugins** window.

Now, the *BASEmesh 2* plugin should be available in QGIS' *Plugins* menu and the [PostTelemac](https://github.com/Artelia/PostTelemac/wiki#T45) <img src="../img/qgis/sym-posttm.png"> symbol should be visible in QGIS' menu bar.

```{admonition} Why use BASEmesh for TELEMAC?
By using BASEmesh, this tutorial employs BASEMENT's efficient mesh generator to minimize the number of work steps to be made in BlueKenue<sup>TM</sup>. The rationale behind this approach is that QGIS is more stable and user-friendly than BlueKenue<sup>TM</sup>, for instance, to correct drawing errors of boundary lines.
```

(get-dem-xyz)=
## Load DEM

This tutorial uses height information that is stored in a {term}`DEM`. For the QGIS section, preferably use the {term}`GeoTIFF` {term}`DEM` with UTM zone 33N as {term} `CRS` as follows:

* [**Download the GeoTIFF DEM**](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem-utm33n.tif) and save it in the same folder (`/Project Home/` or a sub-directory) as the above-create **qgz** project.
* Add the downloaded DEM as a new raster layer in *QGIS*:
  * In *QGIS*' **Browser** panel find the **Project Home** directory where you downloaded the DEM *tif*.
  * Drag the DEM *tif* from the **Project Home** folder into QGIS' **Layer** panel.
* To facilitate delineating specific regions of the river ecosystem later, add a {ref}`satellite imagery basemap <basemap>` (XYZ tile) under the {term}`DEM` and customize the layer symbology.

```{admonition} What are QGIS panels, what is a basemap, and how can I re-order layers?
:class: tip
Learn more in the *QGIS* tutorial on {ref}`qgis-tbx-install`.
```

The **dem-utm33n** layer should now be visible in the viewport and listed in the **Layers** panel. **Right-click** on the **dem-utm33n** layer and select **Zoom to Layer(s)** to view the layer.

````{admonition} Alternatively work with a .xyz DEM pointcloud
:class: note, dropdown
This tutorial uses later in the section on BlueKenue<sup>TM</sup> a `*.xyz` file as {term}`DEM`, which was derived from the {term}`GeoTIFF` using the workflow described in the {ref}`QGIS tutorial <make-xyz>`. The `*.xyz` file can also be used with QGIS and it can be [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem.xyz). To **import** the **dem.xyz** file in QGIS, open the *Data Source Manager* from the **Layer** top menu, select **Add Layer** and **Add Delimited Text Layer...**. In the opening **Data Source Manager** window (see {numref}`Fig. %s <qgis-import-xyz>`) take the following actions:

* Select the downloaded `dem.xyz` file in the **file name** field.
* In the **File Format** frame, make sure to select **Custom delimiters** and check the **Space** delimiter box.
* In the **Record and Fields Options** frame, set the **Number of header lines to discard** to `13` and check the **First record has field names** box.
* In the **Geometry Definition** frame, select `:EndHeader` as **X field**, `field_2` as **Y field**, and `field_3` as **Z field**. Select `Project CRS: ESRI:32633 - WGS 84 / UTM zone 33N` as **Geometry CRS**.
* Click **Add** and **Close** the *Data Source Manager* window.

```{figure} ../img/qgis/import-dem-xyz.png
:alt: qgis import XYZ point cloud file dem
:name: qgis-import-xyz

Import the `*.xyz` point cloud as QGIS layer.
```
````


## Enable Snapping
It is important that the lines do not overlap to avoid ambiguous or missing definitions of regions and to ensure that boundary lines are closed. Therefore, activate snapping:

* Activate the *Snapping Toolbar*: **View** > **Toolbars** > **Snapping Toolbar**
* In the **Snapping toolbar** > **Enable Snapping** <img src="../img/qgis/snapping-horseshoe.png">
* Enable snapping for
  * **Vertex**, **Segment**, and **Middle of Segments** <img src="../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../img/qgis/snapping-intersection.png">.
  * **Self Snapping** <img src="../img/qgis/sym-self-snapping.png">.

(make-tm-shp)=
## Model Boundaries and Breaklines

This section resembles the instructions of the {ref}`BASEMENT pre-processing <make-2dm>` tutorial to generate an {term}`SMS 2dm` mesh file. The differences are that the shapefiles for the TELEMAC pre-processing use the *UTM zone 33N* {term}`CRS` and that the height (elevation) interpolation needs to be done with the BlueKenue<sup>TM</sup> software to generate liquid boundary lines and an `*.slf` geometry file for TELEMAC. The generation of the {term}`SMS 2dm` mesh relies on the {ref}`QGIS BASEmesh plugin <get-basemesh>` and requires drawing a

* {ref}`Line Shapefile <create-line-shp>` called *breaklines.shp* that contains model boundaries and internal breaklines between model regions with different characteristics;
* {ref}`Line Shapefile <create-line-shp>` called *liquid-boundaries.shp* that contains model boundaries for assigning inflow and outflow conditions;
* {ref}`Point Shapefile <create-point-shp>` called *region-pts.shp* that contains markers for the definition of characteristics of model regions.

{numref}`Figure %s <tm-shapefiles>` provides an overview of the shapefiles to be drawn for generating a quality mesh with the BASEmesh plugin.

```{figure} ../img/telemac/tm-prepro-illu.png
:alt: qgis telemac basemesh point line shapefiles
:name: tm-shapefiles

The breaklines, liquid boundaries, and region points shapefile to draw for creating a 2dm quality mesh with the BASEmesh plugin (background map: {cite:t}`googlesat` satellite imagery).
```

(tm-bm-breaklines)=
### Breaklines and Model Outline

The model boundary defines the model extent and can be divided into regions with different characteristics (e.g., roughness values) through **breaklines**. Breaklines indicate, for instance, channel banks and the riverbed (main channel), and need to be inside the DEM extents. Boundary lines and breaklines are stored in a {ref}`Line Shapefile <create-line-shp>` that BASEmesh uses to find both model boundaries and internal breaklines between model regions. For this purpose, {ref}`create-line-shp` and call it **breaklines.shp** (**Layer** > **Create Layer** > **New Shapefile Layer**). Click on QGIS' **Layers** menu > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <tm-qgis-new-lyr>`). Make sure to select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`CRS` <img src="../img/qgis/sym-crs.png">. Do not add any field.

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: tm-qgis-new-lyr

Create a new shapefile from QGIS' Layers menu.
```

Start editing **breaklines.shp** by clicking on the yellow pen <img src="../img/qgis/yellow-pen.png"> and draw the breaklines indicated in {numref}`Fig. %s <tm-shapefiles>` by activating **Add Line Feature** <img src="../img/qgis/sym-add-line.png">, which involves:

* The **boundaries of the** model at the left and the right **floodplain limits**:
  * Delineate the outer bounds of the floodplains.
  * Make sure that all points and lines are inside the {ref}`DEM layer <get-dem>`.
  * Do not cross the river (wetted area indicated by the satellite imagery basemap).
  * **Finalize** every line with a **right-click**.
* The **breaklines of the left bank (LB) and right bank (RB)**:
  * Draw lines along the wetted main channel indicated in the satellite imagery (basemap).
  * Make sure that line ends perfectly coincide with the before-created floodplain boundary lines (snapping is needed); thus, the main channel's breaklines and the floodplain boundary lines need to enclose the floodplains without any gap between the lines.
* **Breaklines of gravel banks**:
  * Draw lines along the gravel banks that are visible in the satellite imagery basemap in the main channel.
  * Make sure that the line ends perfectly coincide (use snapping) with the before-created main channel breaklines; thus, the main channel's hard breaklines and the gravel bank breaklines need to enclose the gravel banks without any gap between the lines.
* Optional: **Breaklines of block ramps**:
  * Find the rough block ramps (effervescing waters) in the satellite imagery basemap and delineate them by drawing lines across the wetted main channel.
  * Make sure that the line ends perfectly coincide with the main channel breaklines; thus, the main channel's hard breaklines and the block ramp breaklines need to enclose the block ramps without any gap between the lines.

To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">. Finally, save the new lines (edits of **breaklines.shp**) by clicking on the **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.


```{admonition} Troubles with drawing boundaries and breaklines?
:class: tip
Download the [zipped breaklines shapefile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) shown in the above figure and unpack it into the project folder, for instance, `/Project Home/shapefiles/breaklines.[SHP]`.
```

```{admonition} Draw boundaries of complex DEMs...
:class: tip
Drawing boundaries manually around large {term}`DEM`s can be very time consuming, in particular, if the raw data are a point cloud and not yet converted to a {ref}`raster`.

If you are dealing with a point cloud, consider using *QGIS* [Convex Hull tool](https://docs.qgis.org/3.16/en/docs/training_manual/vector_analysis/spatial_statistics.html?highlight=convex%20hull#basic-fa-create-a-test-dataset) that draws a tight bounding polygon around points.

If you are dealing with a large {term}`GeoTIFF`, consider using QGIS' [Raster to Vector](https://docs.qgis.org/3.16/en/docs/training_manual/complete_analysis/raster_to_vector.html) tool.
```

(tm-bm-liquid-boundaries)=
### Liquid Boundaries

The **liquid boundaries** define where hydraulic conditions, such as a given discharge or stage-discharge relationship, apply at the model inflow (upstream) and outflow (downstream) limits. Thus, a functional river model requires at least one inflow boundary (line) where mass fluxes enter the model and one outflow boundary (line) where mass fluxes leave the model. For this purpose, {ref}`create-line-shp` called **liquid-boundaries.shp**, select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`CRS` <img src="../img/qgis/sym-crs.png">, and define **two text data fields** named **type** and **stringdef**. Make sure that **snapping** is still **enabled** and **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **liquid-boundaries.shp**. Then draw two lines:

* Activate **Add Line Feature** <img src="../img/qgis/sym-add-line.png">.
* Draw an inflow boundary line (light blue line on the left of {numref}`Fig. %s <tm-shapefiles>`):
  * Zoom to the inflow region of the DEM limits, where there is a **gap between** the above-created **floodplain boundary breaklines**.
  * Start drawing a line on one bank (top of the below figure) and move to the other bank to make approximately seven more points across the river.
  * The **last point** needs to **coincide** with the end of the other bank's **floodplain boundary breakline**.
  * **Finalize** the line with a **right-click**, and enter `Inflow` in the **type** field and `inflow` in the **stringdef** field (the case matters).
* Draw an outflow boundary line (light blue line on the right of {numref}`Fig. %s <tm-shapefiles>`):
  * Zoom to the outflow region of the DEM limits, where there is a **gap between** the above-created **floodplain boundary breaklines**.
  * Start drawing a line on one bank (top of the below figure) and move to the other bank to make approximately seven more points across the river.
  * The **last point** needs to **coincide** with the end of the other bank's **floodplain boundary breakline**.
  * **Finalize** the line with a **right-click**, and enter `Outflow` in the **type** field and `outflow` in the **stringdef** field (the case matters).


To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">.

Finally, save the liquid boundary lines (edits of **liquid-boundaries.shp**) by clicking on the **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.

```{admonition} Troubles with drawing the liquid boundary lines?
:class: tip
Download the [zipped liquid-boundaries shapefile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) and unpack it into the project folder, for instance, `/Project Home/shapefiles/liquid-boundaries.[SHP]`.
```

### Region Point Markers

**Region point** markers are placed inside regions defined by boundary lines and breaklines. Every region marker (i.e., a point somewhere in the region area) assigns, for instance, a material identifier (MATIDs) and a maximum mesh cell area. The MATID is (currently) not needed for TELEMAC (BASEMENT only), but the entries in the **max_area** field will determine the cell size of the mesh regions and have major effects on the quality and efficiency of the TELEMAC simulation. To draw region points, {ref}`create a new point shapefile <create-point-shp>` named **raster-points.shp** with the following definitions (similar to {numref}`Fig. %s <qgis-reg-lyr>` in the BASEMENT pre-processing tutorial):

* Define the **File name** as **region-points.shp** (or similar)
* Ensure the **Geometry type** is **Point**
* Select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`CRS` <img src="../img/qgis/sym-crs.png">
* Add three **New Field**s (in addition to the default **Integer** type **ID** field):
  * **max_area** = **Decimal number** (**length** = 10, **precision** = 3)
  * **MATID** = **Whole number** (**length** = 3)
  * **type** = **Text data** (**length** = 20)
* Click **OK** to create the new point shapefile.

Consider to **deactivate snapping** for drawing the region markers because the points should not coincide with any line. Then, **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **region-points.shp** file and activate **Add Point Feature** <img src="../img/qgis/sym-add-point.png">. Draw one point in every area section that is enclosed by breaklines and (liquid) boundary lines (refer to the round and triangular-shaped points in {numref}`Fig. %s <tm-shapefiles>`). Depending on the apparent area type from the satellite imagery basemap, assign one of the four regions listed in {numref}`Tab. %s <tab-tm-region-defs>` to every point.

```{list-table} Region names and their **max_area**, **MATID**, and **type** field values.
:header-rows: 1
:name: tab-tm-region-defs

* - Region
  - Riverbed
  - Block ramps
  - Gravel banks
  - Floodplains
* - **max_area**
  -  25.0
  -  20.0
  -  25.0
  -  80.0
* - **MATID**
  - 1
  - 2
  - 3
  - 4
* - **type**
  - riverbed
  - block_ramp
  - gravel_bank
  - floodplain
```

After drawing a point in every closed area, save the region point markers (edits of **region-points.shp**) by clicking on the **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.

```{admonition} Troubles with drawing the region marker points?
:class: tip
Download the [zipped region-points shapefile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/region-points.zip) and unpack it into the project folder, for instance, `/Project Home/shapefiles/region-points.[SHP]`.
```

(tm-qualm)=
## Quality Meshing (*.2dm)

*BASEmesh*'s quality mesh tool creates a computationally efficient triangular mesh based on {cite:t}`shewchuk1996` and within the above-defined model boundaries. The tool associates mesh properties with the regions shapefile, but it does not include elevation data. Thus, after generating a quality mesh in {term}`SMS 2dm` format, elevation information needs to be added with the BlueKenue<sup>TM</sup> software. To generate the quality mesh, open BASEmesh's **QUALITY MESHING** tool (QGIS' **Plugins** > **BASEmesh 2** > **QUALITY MESHING**). Make the following settings in the popup window (see also {numref}`Fig. %s <fig-tm-qualm>`):

* Triangulation constraints frame:
  * **Breaklines** = **breaklines** (see {ref}`make-tm-shp`).
  * Keep all other defaults.
* Regions frame:
  * **Activate the Regions** checkbox.
  * **Region marker layer** = **regions-points** (see {ref}`make-tm-shp`).
  * **Activate the MATID field** checkbox and select the *regions-points* shapefile's **MATID field**.
  * **Activate the Maximum area field** checkbox and select the *regions-points* shapefile's **max_area field**.
* Mesh domain frame: keep defaults.
* String definitions frame:
  * **Activate the String definitions** checkbox.
  * **String definitions layer** = **liquid boundaries**.
  * **String definitions ID field** =  **stringdef**.
  * **Activate the Include in 2DM node strings (BASEMENT 3)** checkbox.
  * Ignore all BASEMENT 2.8 options.
* Settings frame: keep defaults.
* Output frame:
  * Click on the **Browse...** button and define a **2dm** file name in the `/Project Home/` directory, such as **prepro-tutorial_quality-mesh.2dm**.
* Click on the **Run** button to create the quality mesh.


```{figure} ../img/qgis/bm-quality-meshing-success.png
:alt: basement qgis quality mesh tin
:name: fig-tm-qualm

Definitions to be made in BASEmesh's Quality meshing tool.
```

Quality meshing may take a short while. After a successful mesh generation the file **prepro-tutorial_quality-mesh-interp.2dm** will have been generated and it automatically shows up in QGIS as a single-color surface with `0-0` **Bed Elevation**. The next section shows the interpolation of elevation data with the BlueKenue<sup>TM</sup> software.

```{admonition} Troubles with running the quality mesh generator?
:class: tip
Download the [tutorial quality mesh file](https://github.com/hydro-informatics/telemac/raw/main/meshes/prepro-tutorial_quality-mesh-utm33n.2dm) and save it in the project folder, for instance, `/Project Home/meshes/prepro-tutorial_quality-mesh-utm33n.2dm`.
```

(bk-tutorial)=
# BlueKenue

(bk-intro)=
## Get Started
This section features the {ref}`BlueKenue <bluekenue>` software to interpolate terrain elevations from a {term}`DEM`.xyz file on an {term}`SMS 2dm` mesh, export the mesh to the SELAFIN/SERAFIN (`*.slf`) geometry format for TELEMAC, and define boundary lines.

In addition, the {ref}`Meshing with BlueKenue <bk-meshing>` section explains the mesh generation with BlueKenue<sup>TM</sup>, which might be unstable because of program crashes and inflexible for correcting line drawing errors. Still, meshing with BlueKenue<sup>TM</sup> might be desirable to create a computational mesh with long triangular cells that approximately follow the river streamlines (i.e., using a channel sub-mesh).

To familiarize with BlueKenue<sup>TM</sup>, launch the software (more details in the {ref}`installation chapter <bluekenue>`) and locate

* the **WorkSpace** browser (on the left of the window),
* the **Data Items** entry in the **WorkSpace**, where file objects will be listed,
* the **Views** entry in the **WorkSpace**, where a **2D View (1)** entry appears by default and a *3D View* can be added from the **Window** top menu > **New 3D View**.

Have a look at the **File** menu, which enables to:

* Create **New** BlueKenue<sup>TM</sup> objects, such as SELAFIN, Conlim Boundary Condition, T3 Mesh Generator, or 2D Interpolator objects.
* **Open** file types such as `*.slf` geometry files or `*.xyz` point clouds.
* **Import** files such as:
  * an **ArcView Shapefile** (read more about {ref}`shapefiles <shp>`),
  * an {term}`SMS 2dm` Mesh like the one created in the above {ref}`pre-processing with QGIS <tm-qualm>`section, or
  * a {term}`GeoTIFF` raster, which will not work with many GeoTIFF rasters in practice because BlueKenue<sup>TM</sup> cannot handle Float32 or Float64 data in a GeoTIFF.

The **Edit** menu enables editing BlueKenue<sup>TM</sup> objects, such as lines, point sets, or meshes.

The **Tools** menu provides routines that can be applied to particular BlueKenue<sup>TM</sup> objects or for combining objects. In particular, this tutorial will make use of the **Map Objects...** tool.

(bk-files)=
## Files and Objects

BlueKenue<sup>TM</sup> saves every object in software specific file formats and this eBook refers to the following BlueKenue<sup>TM</sup> file objects (alphabetic order of file endings):

* `*.bc2` files contain Conlim Boundary Conditions.
* `*.cli` files contain ready-to-use boundary conditions for TELEMAC and can be produced with a `*.bc2` object.
* `*.i2s` files contain closed or open lines.
* `*.in2` files contain 2D Interpolators for mapping elevation (or other) data on a mesh.
* `*.slf` files contain ready-to-use TELEMAC meshes that stem from a BlueKenue<sup>TM</sup> SELAFIN object and a `*.t3s` mesh file.
* `*.t3c` files contain BlueKenue<sup>TM</sup> channel mesh generator objects.
* `*.t3m` files contain BlueKenue<sup>TM</sup> mesh generator objects to create a `*.t3s` mesh object.
* `*.t3s` files contain BlueKenue<sup>TM</sup> mesh objects that can either be imported (e.g., from an {term}`SMS 2dm` file) or created with a `*.t3m` mesh generator.

All files that are created with BlueKenue<sup>TM</sup> are based on the ASCII EnSim 1.0 file type standard. The EnSim Core builds on {term}`HDF` and it is documented in BlueKenue<sup>TM</sup>'s [user manual PDF](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/2011_UserManual.pdf) that comes along with the [BlueKenue installer](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) (in BlueKenue<sup>TM</sup> press the `F1` key to open the manual). Note that understanding the EnSim Core can significantly facilitate troubleshooting structural errors of BlueKenue<sup>TM</sup> files.

(bk-xyz)=
## Load XYZ Points

Download the provided [dem.xyz](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem.xyz) point cloud that contains EnSim-formatted 3d coordinates of the river ecosystem {term}`DEM` that will be modelled in this tutorial. The `*.xyz` file was derived from the {term}`GeoTIFF` {term}`DEM` used in the {ref}`QGIS pre-processing <get-dem-xyz>`.

 ```{margin} The .xyz file is not an XYZ tile
 The point cloud in the `*.xyz` file is different than the regular XYZ tile raster that constitutes the {ref}`satellite imagery basemap <basemap>`.
 ```

To load the **dem.xyz** file in BlueKenue<sup>TM</sup>, open it from the **File** menu (**File** > **Open...**) and take the following actions in the popup window:

* Navigate to the download folder.
* Next to the **File name:** field, locate the file type drop-down menu and **change the default from Telemac Selafin File (`*.slf`) to Point Sets (`*.pt2`, `*.xyz`, `*.pcl`)**.
* Click **Open** to finalize the import.

To verify if the point cloud was correctly imported, **drag** the new **dem (Z)** data items to the **2D View (1)** entry. {numref}`Figure %s <bk-import-xyz>` shows the imported XYZ point cloud in BlueKenue<sup>TM</sup>.

```{figure} ../img/telemac/bk-imported-pts.png
:alt: bluekenue import xyz point cloud DEM
:name: bk-import-xyz

The provided dem.xyz imported in BlueKenue<sup>TM</sup>.
```

To verify the {term}`CRS` of the point dataset, right-click on **dem (Z)**, select properties, go to the **Spatial** tab, and make sure that BlueKenue<sup>TM</sup> correctly identified **UTM Zone 33** in the **Coordinate System** frame and **WGS 84** as **Ellipsoid**.


(bk-meshing)=
## BlueKenue Meshing (Optional)

```{admonition} Skip this section if you created a *.2dm* quality mesh with BASEMESH
This is an optional section for users who do not want to use QGIS and the BASEmesh plugin for meshing. Generating a mesh with BlueKenue<sup>TM</sup> can be useful, for instance, to produce a computational grid that has triangular cells oriented parallel to the riverbanks (i.e., a channel sub-mesh). Otherwise, **if the `*.2dm` mesh file was created** with QGIS, **jump to the section on creating a {ref}`Selafin Object <bk-create-slf>`**.
```

This section features the basic mesh generation with BlueKenue<sup>TM</sup>, which also runs smoothly on Linux through the {ref}`PlayOnLinux <play-on-linux>` app. Additionall, the Baxter tutorial {cite:p}`baxter2013` provides more details for getting started with BlueKenue along with detailed screenshots.

### Draw Model Boundary (Closed Line)

Delineate the model boundary (outline) with a closed line object (see also {numref}`Fig. %s <bk-model-outline>`):

* Create a new **Closed Line** by clicking on the <img src="../img/telemac/bk-sym-cl.png"> symbol in the BlueKenue<sup>TM</sup> menu.
* **Draw** the new closed line:
  * Make points by clicking close to the outer extent of the **dem (Z)** layer in the **2D Views (1)** window. Ensure that no point lies outside the region where elevation data is available (i.e., tightly delineate **dem (Z)**).
* Finalize the closed line by pressing **Esc**.
* Name the closed line, for instance, `model-outline`.
* **Skip** **Adding a New Attribute** by just clicking **OK**.

```{figure} ../img/telemac/bk-model-outline.png
:alt: bluekenue draw closed line model boundary outline
:name: bk-model-outline

The Closed Line of the model boundaries in BlueKenue<sup>TM</sup>'s 2D View window.
```

To **save the model outline**, highlight the new Closed Line object in the **WorkSpace** browser and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Consider creating a new folder called `bk-mesh` that will contain all BlueKenue<sup>TM</sup> objects required for meshing. Thus, save the model outline (Closed Line), for example, as **/bk-mesh/model-outline.i2s**.

```{admonition} Troubles with drawing the model outline?
:class: tip
The outline can also be downloaded from the supplemental materials repository ([download model-outline.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/model-outline.i2s)). To open the Closed Line from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **Line Sets (`*.i2s`, `*.i3s`)** as file type and navigate to the download directory.
```

The current state of BlueKenue<sup>TM</sup> can be saved in the form of a **workspace.ews** file (**File** > **Save WorkSpace...** > define a name). Saving the workspace requires that all BlueKenue<sup>TM</sup> objects are saved on the disk. Optionally, download the [meshing-workspace.ews](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/meshing-workspace.ews) from the supplemental materials repository.

```{admonition} Loading a WorkSpace
:class: attention
In theory, the saved workspace can be loaded after closing BlueKenue<sup>TM</sup>, but the **Load WorkSpace...** operation often **fails** for apparently arbitrary reasons. This issue is one of the reasons that make QGIS a better option for meshing.
```

(bk-draw-ol)=
### Draw Open Lines of the Channel Banks

Similar to the {ref}`above-created breaklines in QGIS <make-tm-shp>`, the channel banks can be delineated with Open Line objects. For this purpose create two Open Line objects as follows:

* Create a new **Open Line** by clicking on the <img src="../img/telemac/bk-sym-ol.png"> symbol in the BlueKenue<sup>TM</sup> menu.
* **Draw** the new open line:
  * Make points by following the blue-ish-green areas as indicated in {numref}`Fig. %s <bk-lines-all>` **2D Views (1)** window (flow direction from left to right).
* Finalize the open line by pressing **Esc**.
* Name one open line `LeftBank` and the other `RightBank`.
* **Skip** **Adding a New Attribute to:** by just clicking **OK**.

```{figure} ../img/telemac/bk-lines-all.png
:alt: bluekenue draw open line channel river banks
:name: bk-lines-all

The finalized Open and Closed Line objects delineating the model boundaries and the channel banks. The RightBank Open Line is represented by the dashed black line and the LeftBank Open Line is represented in red.
```

```{admonition} Troubles with drawing the open lines of the channel banks?
:class: tip
Download the lines from the supplemental materials repository. Notably download [LeftBank.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/LeftBank.i2s) and [RightBank.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/RightBank.i2s). To open the Open Line objects from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **Line Sets (`*.i2s`, `*.i3s`)** as file type and navigate to the download directory.
```

### Generate Mesh(es)

BlueKenue<sup>TM</sup> provides mesh generators for creating regular or unstructured computational grids (meshes). This example features the **T3 Channel Mesher** to generate a triangular mesh, which involves first creating a channel mesh (sub-mesh) and second generating a compound mesh that embeds the channel sub-mesh in a coarser mesh of the floodplains. To this end, start with creating a new **T3 Channel Mesher** object (**File** > **New** > **T3 Channel Mesher**). In the popup window set:

* **CrossChannelNodeCount** to `20` and
* **AlongChannelInterval** to `15`.

Click **OK** (**not Run**) to close the new T3 Channel Mesh window. Next, drag and drop the above-created **LeftBank** and **RightBank** Open Line objects on their equivalent attributes of the **new T3 Channel Mesh** object in the WorkSpace browser as indicated in {numref}`Fig. %s <bk-channel-mesh>`. Next, generate the channel mesh by double-clicking on the **new T3 Channel Mesh** object and click **Run**. To visualize the resulting **Mesh**, drag it on the **2D View (1)** object.

```{figure} ../img/telemac/bk-channel-mesh.png
:alt: bluekenue create channel mesh
:name: bk-channel-mesh

Create and visualize the channel mesh after dragging the LeftBank and RightBank Open Line Objects on their name equivalents of the T3 Channel Mesh object.
```

```{admonition} Troubles with creating the channel mesh?
:class: tip
Download the [channel-mesh.t3c](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/channel-mesh.t3c) mesh generator and the [channel-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/channel-mesh.t3) mesh objects from the supplemental materials repository. To open the T3 Mesh object from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **2D T3 Mesh (`*.t...`)** as file type and navigate to the download directory.
```

Next, embed the channel mesh in a coarser floodplain mesh by creating a **new T3 Mesh Generator** object (**File** > **New** > **T3 Mesh Generator**). In the **T3 Mesh** popup window make the following settings (see also {numref}`Fig. %s <bk-t3-mesher>`):

* **Enable** the **Resample Outline** checkbox.
* Set the **Default Edge Length** to `20`.
* Keep all other defaults.
* Press **OK** (**not Run**).

```{figure} ../img/telemac/bk-t3-mesher.png
:alt: bluekenue create combined mesh generator
:name: bk-t3-mesher

Setup the properties of the new T3 Mesh Generator object.
```

Define the **Outline (Value)** by dragging (see also {numref}`Fig. %s <bk-mesh-compound>`):

* The above-created **model-outline** object on the **Outline (Value)** of the **new T3 Mesh**, and
* The channel **Mesh** on the **SubMeshes** attribute of the **new T3 Mesh**.

Generate the compound mesh by double-clicking on the **new T3 Mesh** object and single-clicking on **Run**. Confirm the question box (*Continue?* > **Yes**) and press **OK** after the mesh generator is finished (*Done...*). To visualize the resulting **Mesh**, drag it on the **2D View (1)**.

```{figure} ../img/telemac/bk-mesh-compound.png
:alt: bluekenue generate combined mesh drag and drop
:name: bk-mesh-compound

The compound mesh after dragging the model outline on the Outline (Value) and the channel Mesh on the SubMeshes attribute of the new T3 Mesh generator object.
```

```{admonition} What is the difference between the channel mesher and the mesh generator?
:class: note
{numref}`Figure %s <bk-mesh-compound>` shows that the channel mesh is streamline-adjusted following the channel banks. This kind of mesh is known to be advantageous for computation speed and model stability. Thus, the availability of the channel mesher in BlueKenue<sup>TM</sup> is a strength and the **best argument for not using BASEmesh** in QGIS for the mesh generation.
```

```{admonition} Troubles with creating the compound mesh?
:class: tip
Download the [compound-mesher.t3m](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesher.t3m) and the [compound-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesh.t3s) objects from the supplemental materials repository. To open the T3 Mesh object from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **2D T3 Mesh (`*.t...`)** as file type and navigate to the download directory.
```

(bk-slf)=
## SELAFIN

### Open and Import Ingredients
Whether the mesh was created with BlueKenue<sup>TM</sup> or QGIS (and the BASEmesh plugin), make sure to have now a BlueKenue<sup>TM</sup> workspace with only the XYZ point cloud loaded (see the {ref}`bk-xyz` section). Before a SELAFIN object can be created, the previously created mesh (i.e., either the [quality-mesh.2dm](https://github.com/hydro-informatics/telemac/raw/main/meshes/prepro-tutorial_quality-mesh-utm33n.2dm) or the [compound-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesh.t3s)) needs to be imported into the WorkSpace in addition to the point cloud. The following instructions show the import and use of the `*.2dm` file:

* In BlueKenue<sup>TM</sup> go to **File** > **Import** > **SMS 2DM Mesh**.
* In the import window, navigate to the folder where the `*.2dm` file lives, select the `*.2dm` file, and click **Open**.
* When the *Reading SMS 2d Mesh File* process is *Done...*, click **OK**.

```{admonition} How to load a BlueKenue .T3S mesh file?
:class: note, dropdown
In contrast to an {term}`SMS 2dm` (`*.2dm`) file that has to be *imported*, a `*.t3s` file has to be **opened** in BlueKenue<sup>TM</sup>. To this end, **open** the T3 Mesh (`*.t3s`) from **File** > **Open...** > select **2D T3 Mesh (`*.t...`)** as file type and navigate to the download directory. Select the `*.t3s` mesh file and click **Open**.
```

Ignore warning messages regarding the projection, but make sure that BlueKenue<sup>TM</sup> correctly read the mesh coordinates by **dragging** the imported (or opened) mesh onto the **2D View (1)**. The BlueKenue<sup>TM</sup> window should now look similar to {numref}`Fig. %s <bk-imported-mesh>`.

```{figure} ../img/telemac/bk-imported-mesh.png
:alt: bluekenue import open 2dm t3s mesh drag
:name: bk-imported-mesh

The imported mesh in the 2D View (1).
```

(bk-create-slf)=
### Create SELAFIN Object

With the open *dem.xyz* and the imported (or opened) mesh, all ingredients required by a BlueKenue<sup>TM</sup> SELAFIN object are available. Now, create a new SELAFIN object:

* Go to **File** > **New** > **SELAFIN Object...**

```{image} ../img/telemac/bk-create-selafin-object.png
```

* In the popup window (*Properties of:new Selafin*) click **OK** and a **new Selafin** object will appear in the WorkSpace's **Data Items**.
* **Right-click** on the **new Selafin** object and select **Add Variable...**
* Take the following action in the **Add New SELAFIN Variable** window:
  * In the **Mesh** field, select the above-imported (or opened) mesh (e.g., `prepro-tutorial_quality-mesh-utm33n.2dm`).
  * In the **Name** field, select **BOTTOM**.
  * In the **Units** field, select **M** (i.e., meters).
  * Keep all other defaults and click **OK**.
* Save the new Selafin object by highlighting it in the **Data Item** tree of the WorkSpace and clicking the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Give the mesh a meaningful and short name, such as `qgismesh.slf`.

(bk-2dinterp)=
### Create 2D Interpolator

A 2D Interpolator object is required to map elevation information onto the Selafin mesh. To this end, create a new 2D Interpolator object and map elevations onto the BOTTOM mesh:

* Go to **File** > **New** > **2D Interpolator...** and a **new 2D Interpolator** object will appear in the **Data Items** of the WorkSpace.

```{image} ../img/telemac/bk-create-2Dinterpolator.png
```

* **Drag dem (Z)** (i.e., the above-opened *dem.xyz* pointcloud) onto the **new 2D Interpolator** object (red arrow in {numref}`Fig. %s <bk-mesh-interpolated>`).
* **Highlight** (click on) the **BOTTOM (Anonymous Attribute)** mesh attribute of the above-created SELAFIN object (e.g., called `qgismesh`).
* With the mesh highlighted, go to the **Tools** top menu > **Map Object...**.
* In the opening **Available Objects** window select the **new 2D Interpolator** and click **OK**.
* Once the *Processing...* finished, click **OK**.
* Save the final meshes:
  * The BOTTOM mesh is a BlueKenue<sup>TM</sup> `*.t3s` mesh object; to save it, highlight it in the **Data Items** tree and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Then, save the mesh, for instance, as `BOTTOM.t3s` file.
  * To save the Selafin mesh in its current (with interpolated elevations) state, highlight the Selafin object (e.g., `qgismesh`) and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. This action overwrites the above-saved `*.slf` file (click **Yes** to confirm replacing it).

To verify if the 2D interpolator correctly interpolated the elevations on the BOTTOM mesh, drag the BOTTOM mesh onto the **2D View (1)**. Uncheck the visibility of dem (Z) and the imported (or opened) mesh with a right-click on these elements in the 2D View (1) tree and **deselect** the **Visible** entry. Thus, only the height-interpolated mesh should be visible now, as indicated in {numref}`Fig. %s <bk-mesh-interpolated>`. If the **interpolation has been successful, the mesh is displayed in a variety of (rainbow) colors**. Otherwise, **if the mesh is** completely, monotonously **monochrome (red)**, the elevation **interpolation** has **not** been **successful** and must be repeated (the numerical model cannot work properly without elevation information).

```{figure} ../img/telemac/bk-mesh-interpolated.png
:alt: bluekenue 2dm t3s mesh interpolate height elevation 2D interpolator map object
:name: bk-mesh-interpolated

The height-interpolated mesh in the 2D View (1) with indication of drag and drop actions for running the object mapping with a new 2D Interpolator object.
```

```{admonition} Troubles with creating the Selafin mesh and or the height interpolation?
:class: tip
Download the BOTTOM mesh and the SELAFIN object from the supplemental materials repository:

* [Download BOTTOM.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/BOTTOM.t3s);
* [Download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf) (**EPSG:6173** - ETRS 89 / UTM zone 33N).
```

(bk-bc)=
## Boundary Conditions (Conlim - CLI)

### Create Conlim Object
TELEMAC needs to know how to treat the outer edges of the model (mesh). For this purpose, boundary conditions have to be assigned to all nodes that constitute the `*.slf`mesh outline:

* Go to **File** > **New** > **Boundary Conditions (Conlim )...** and a **new 2D Interpolator** object will appear in the **Data Items** of the WorkSpace.

```{image} ../img/telemac/bk-create-bc.png
```

* In the opening popup window (**Available t3s Objects**), select the above-created **BOTTOM** mesh (i.e., the mesh with elevation information) and click **OK**. A new **BOTTOM_BC** object will occur in the **Data Items** tree of the WorkSpace.
* Drag the new **BOTTOM_BC** object onto the **2D View (1)**, which will **enable the *prescription* of boundary condition types** (details in the next section).

{numref}`Figure %s <bk-bc-types>` illustrates the new BOTTOM_BC object in the 2D View (1) and indicates where upstream and downstream liquid boundaries will be applied in the next section.

```{figure} ../img/telemac/bk-bc-types.png
:alt: bluekenue boundary conditions conlim create upstream downstream
:name: bk-bc-types

The new Boundary Conditions (Conlim) object (BOTTOM_BC) in the 2D View (1) with a qualitative overview of the position of upstream and downstream boundaries where prescribed flow (Q) and prescribed flow (Q) and Depth (H) will be applied later in the TELEMAC setup.
```

To **save the new BOTTOM_BC object**, highlight it in the **Data Items** tree and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Define a filename such as **`boundaries.bc2`**. As a result of saving the object, the BOTTOM_BC object takes on the new file name (e.g., **boundaries**).

(bk-liquid-bc)=
### Define Liquid Boundaries

The default boundary type of the **boundaries** object is **Closed boundary (wall)**. Therefore, to enable mass (i.e., water, sediment, and/or tracer) fluxes through the model, at least two openings must be drawn into the closed boundary. For this purpose, at least one inflow and one outflow open boundary for liquids must be defined. This tutorial uses this minimum number of required open boundaries (i.e., one upstream inflow and one downstream outflow boundary), which are indicated in {numref}`Fig. %s <bk-bc-types>`.

```{admonition} Liquid boundaries must be defined in BlueKenue
Even though the liquid boundaries are already defined in QGIS (see the {ref}`QGIS section on Liquid Boundaries <tm-bm-liquid-boundaries>`), it is always necessary to define the liquid boundaries in BlueKenue<sup>TM</sup> to fit the node numbers (IDs) of the Selafin mesh.
```

The upstream (inflow) liquid boundary will constitute an **Open boundary with prescribed Q** (discharge) and the downstream outflow (liquid) boundary will constitute an **Open boundary with prescribed Q and H** (i.e., prescribed {term}`Rating curve` / {term}`Stage-discharge relation`). These types of boundary conditions are commonly used in practice, with the downstream boundary typically chosen to be at a gauging station where a {term}`Stage-discharge relation` ({term}`Rating curve`) has been calibrated with historic data. To assign the two liquid boundary lines, zoom into the downstream and upstream regions indicated in  {numref}`Fig. %s <bk-bc-types>` and create both boundaries as follows (toggle tabs):

`````{tab-set}
````{tab-item} Upstream boundary
* Zoom into the **upstream** region indicated in  {numref}`Fig. %s <bk-bc-types>`.
* Locate the main channel banks corresponding to the breaklines drawn in QGIS ({ref}`see above <tm-bm-breaklines>`) or BlueKenue<sup>TM</sup> ({ref}`see above <bk-draw-ol>`).
* **Double-click** on a **node at one bank** of the model outline (no matter what bank), then **hold** the **Shift** key and **double-click** on a **node at the other bank** to highlight the inflow (purple) line (see {numref}`Fig. %s <bk-boundary-us>`).
* **Right-click** on the purple inflow line and select **Add Boundary Segment**.
* In the opening window (**CONLIM Boundary Segment Editor**) make the following settings:
  * Define **Boundary Name** as `upstream`.
  * In the **Boundary Code** field select `Open boundary with prescribed Q`.
  * Keep all other defaults and click **OK**.
* **Save** the **boundaries** object by clicking on the disk <img src="../img/telemac/bk-sym-save.png"> symbol and confirm overwriting `boundaries.bc2` (i.e., click **Yes**).

**Switch to** the **Downstream boundary tab** to define the outflow conditions according to {numref}`Fig. %s <bk-boundary-ds>`.

```{figure} ../img/telemac/bk-bm-boundary-us.png
:alt: bluekenue boundary conditions conlim create upstream prescribed discharge flow
:name: bk-boundary-us

The upstream boundary definition. Double-click on a node at one bank, then hold the **Shift** key and double-click on a node at the other bank to highlight the inflow (purple) line. Note that BOTTOM_BC might appear with the name *boundaries* if the object was saved as *boundaries.bc2*.
```
````

````{tab-item} Downstream boundary
* Zoom into the **downstream** region indicated in {numref}`Fig. %s <bk-bc-types>`.
* Locate the main channel banks corresponding to the breaklines drawn in QGIS ({ref}`see above <tm-bm-breaklines>`) or BlueKenue<sup>TM</sup> ({ref}`see above <bk-draw-ol>`), which are indicated by the red-dotted lines in {numref}`Fig. %s <bk-boundary-ds>`.
* **Double-click** on a **node at one bank** of the model outline (no matter what bank), then **hold** the **Shift** key and **double-click** on a **node at the other bank** to highlight the outflow (purple) line (see {numref}`Fig. %s <bk-boundary-ds>`).
* **Right-click** on the purple outflow line and select **Add Boundary Segment**.
* In the opening window (**CONLIM Boundary Segment Editor**) make the following settings:
  * Define **Boundary Name** as `downstream`.
  * In the **Boundary Code** field select `Open boundary with prescribed Q and H`.
  * Keep all other defaults and click **OK**.
* **Save** the **boundaries** object by clicking on the disk <img src="../img/telemac/bk-sym-save.png"> symbol and confirm overwriting `boundaries.bc2` (i.e., click **Yes**).

```{figure} ../img/telemac/bk-bm-boundary-ds.png
:alt: bluekenue boundary conditions conlim create upstream prescribed discharge depth flow
:name: bk-boundary-ds

The downstream boundary definition. Double-click on a node at one bank, then hold the **Shift** key and double-click on a node at the other bank to highlight the outflow (purple) line. Note that BOTTOM_BC might appear with the name *boundaries* if the object was saved as *boundaries.bc2*.
```
````
`````

Ultimately, TELEMAC will need a **`*.cli` file (*Conlim Table*)** that can be created by
* highlighting the **boundaries (LIHBOR)** entry of the **boundaries** (or BOTTOM_BC) object in the **Data Items** tree and
* pressing the disk <img src="../img/telemac/bk-sym-save.png"> symbol (see {numref}`Fig. %s <bk-bc-fin>`).

Save the boundaries file, for instance, as **boundaries.cli**.

```{figure} ../img/telemac/bk-bc-fin.png
:alt: bluekenue liquid boundary conditions conlim upstream inflow outflow downstream cli
:name: bk-bc-fin

The finalized boundary conditions are saved in a .CLI file by highlighting the **boundaries (LIHBOR)** entry of the **boundaries** (or BOTTOM_BC) object in the **Data Items** tree.
```

```{admonition} Troubles with creating and defining the liquid boundaries?
:class: tip
Download the **boundaries** (BOTTOM_BC) BlueKenue<sup>TM</sup> and TELEMAC boundaries (LIHBOR)-CLI objects from the supplemental materials repository:

* [Download boundaries.bc2](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.bc2);
* [Download boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli).
```

The here created Selafin/Serafin (`*.slf`) and boundary conditions (`*.cli`) files are the main products that are needed for running any other SELAFIN-based TELEMAC tutorial in this eBook. The {ref}`steady 2d <telemac2d-steady>` tutorial assigns a constant discharge at the upstream (inflow) and a constant discharge plus constant depth at the downstream (outflow) boundaries. To perform an unsteady calculation, the steady flow rates can be replaced with a `*.qsl` ASCII text file. To this end, the `*.cli` file can be easily adapted any time later with a basic text editor (e.g., {ref}`npp` on Windows or {ref}`Atom <install-atom>`).
