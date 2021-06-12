(qgis-prepro-of)=
# Pre-processing with QGIS

```{admonition} Requirements
:class: attention
Before diving into this tutorial make sure to:

* Follow the installation instructions for {ref}`qgis-install` in this eBook.
* Read (or watch) and understand this eBook's {ref}`qgis-tutorial`.
```

The first steps in numerical modeling of a river consist in the conversion of a Digital Elevation Model (**{term}`DEM`**) into a computational mesh. This tutorial guides through the creation of a QGIS project for converting a {term}`DEM` ({term}`GeoTIFF`) into a computational mesh that can be used with various numerical modeling software featured in this eBook. At the end of this tutorial, {ref}`chpt-openfoam` modelers will have a exported the {term}`DEM` in {term}`STL` file format that still needs to be meshed as explained later in this eBook's *OpenFOAM* {ref}`of-mesh` section.

```{admonition} Platform compatibility
:class: tip
All software applications featured in this tutorial can be run on *Linux*, *Windows*, and *macOS* (in theory - not tested) platforms. Note that some numerical models, such as {ref}`chpt-basement`, will not work on *macOS* platforms.
```

(of-qgis)=
## QGIS Project Setup

Launch QGIS and {ref}`create a new QGIS project <qgis-project>` to get started with this tutorial.
As featured in the {ref}`qgis-tutorial`, set up a coordinate reference system (CRS) for the project. This example uses data of a river in Bavaria (Germany zone 4), which requires the following CRS:

* In the QGIS top menu go to **Project** > **Properties**.
* Activate the **CRS** tab.
* Enter `Germany_Zone_4` and select the CRS shown in {numref}`Fig. %s <of-qgis-crs>`.
* Click **Apply** and **OK**.

```{figure} ../img/qgis/inn-crs.png
:alt: qgis set coordinate reference system crs germany zone_4 Inn river
:name: of-qgis-crs

Define Germany_Zone_4 as project CRS.
```

```{admonition} Save the project...
:class: tip
Save the QGIS project (**Project** > **Save As...**), for example, under the name **prepro-tutorial.qgz**.
```

(of-get-dem)=
## Load DEM

A digital elevation model (**{term}`DEM`**) represents the baseline for any physical analysis of a river ecosystem. Nowadays, {term}`DEM`s often stem from light imaging, detection, and ranging ([LiDAR](https://en.wikipedia.org/wiki/Lidar)) combined with bathymetric surveys. Older approaches rely on manual surveying (e.g., with a total station) of cross-sectional profiles and interpolating the terrain between the profiles. The newer LiDAR technique employs lights sources and provides terrain assessments up to 2-m deep water. Bathymetric [echo sounding](https://en.wikipedia.org/wiki/Echo_sounding) is often necessary to map the ground of deeper waters. Thus, merged LiDAR and echo-sounding datasets produce seamless point clouds of river ecosystems, which may be stored in many different file types.

This tutorial uses an application-ready {term}`DEM` in {term}`GeoTIFF` {ref}`raster` format that stems from a LiDAR point cloud. The {term}`DEM` raster provides height (Z) information from a section of a gravel-cobble bed river in South-East Germany, which constitutes the baseline for the computational grids featured in the next sections. To get the provided DEM in the *QGIS* project:

* **Download the example DEM GeoTIFF**](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/dem.tif) and save it in the same folder (`/Project Home/` or a sub-directory) as the above-create **qgz** project.
* Add the downloaded DEM as a new raster layer in *QGIS*:
  * In *QGIS*' **Browser** panel find the **Project Home** directory where you downloaded the DEM *tif*.
  * Drag the DEM *tif* from the **Project Home** folder into QGIS' **Layer** panel.
* To facilitate delineating specific regions of the river ecosystem later, add a {ref}`satellite imagery basemap <basemap>` (XYZ tile) under the {term}`DEM` and customize the layer symbology.

```{admonition} What are QGIS panels again?
:class: tip
Learn more in the *QGIS* tutorial on {ref}`qgis-tbx-install`.
```

The DEM should now be displayed on the map (if not: right-click on the DEM layer and click on **Zoom to Layer(s)** in the context menu) as shown in {numref}`Fig. %s <of-qgis-dem-basemap>`.

```{figure} ../img/qgis/dem-basemap.png
:alt: qgis import raster DEM basemap
:name: of-qgis-dem-basemap

The imported DEM on a Google Satellite imagery basemap (source: Google / GeoBasis-DEBKG 2019). The flow direction is from left to right following the **Q** arrow.
```

```{admonition} From LiDAR point clouds to a Raster DEM
:class: tip
Terrain survey data are mostly delivered in the shape of an x-y-z point dataset. LiDAR produces massive point clouds, which quickly overcharge even powerful computers. Therefore, LiDAR data may need to be broken down into smaller zones of less than approximately 106 points and special LiDAR point processing software (e.g., [LAStools](http://lastools.org/)) may be helpful in this task. The range of possible data products and shapes from terrain survey is board and this tutorial exemplary uses a set of x-y-z points stored within a text file.
```



(dem2stl)=
## OpenFOAM: Export DEM to STL

```{admonition} Temporary solution
The export to {term}`STL` for modeling with OpenFOAM is a weak solution that will be substituted in future versions of this eBook by exporting a mesh with the [GMSH](http://geuz.org/gmsh) plugin.
```

The {term}`STL` (standard tessellation language) file format is native to CAD software and particularly used for the representation of three-dimensional (3d) structures in the form of unstructured triangulated surfaces. {term}`STL` files can be read by pre-processing software for OpenFOAM and this section explains how to convert a GeoTIFF DEM into an {term}`STL` file.

The export requires the **DEMto3D** plugin, which can be installed in *QGIS* as follows:

* Load the *QGIS* plugin manager: **Plugins** menu > **Manage and Install Plugins**.
* Make sure the **All** tab is active and enter `DEMto3D`.
* Click on **Install Plugin**.
* Close the Plugin Manager after the successful installation.

Following the instructions in the above section on importing {ref}`get-dem`, add the [example DEM GeoTIFF](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/dem-tif) as project layer in *QGIS*. Then export the DEM to {term}`STL` by opening the DEM 3D printing window from **Rasters** > **DEMto3D** > **DEM 3D printing**. In the popup window (see also {numref}`Fig. %s <qgis-dem3d>`):

* Select the `inn...` DEM as **Layer to print**
* For **Print extent** find the **Select layer extent** symbol and select the `inn...` DEM layer.
* In the **Model size** frame set (approximately - must not be exactly the same):
  * **Spacing** to 2.83 (mm)
  * **Width** to 2621.78 (mm)
  * **Length** to 2000 (mm)
* In the **Model height** frame set the **Height** to 367 (m).
* Click on **Export to STL** > **Yes** > define directory and name.

```{admonition} Troubleshoot *No visible raster loaded*
:class: warning
This error message indicates that the DEM GeoTIFF is not correctly loaded or not activated in the Layers Panel. Re-read or watch the tutorial on {ref}`qgis-tbx-install`.
```

```{figure} ../img/qgis/dem3d-printing.png
:alt: basement export stl demto3d printing dem raster
:name: qgis-dem3d

Setup the DEM 3D printing properties.
```

The export starts and will take approximately 1-2 minutes. The resulting **STL** file can be opened with CAD software such as {ref}`salome-install` modules or {ref}`freecad-install`. The result looks similar to {numref}`Fig. %s <qgis-stl-exported>` (depending on the **Height (m)** value used).

```{figure} ../img/qgis/stl-exported.png
:alt: basement export stl
:name: qgis-stl-exported

The resulting stl file of the DEM.
```


