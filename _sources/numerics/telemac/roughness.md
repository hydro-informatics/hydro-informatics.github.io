```{admonition} Contributors
:class: tip
This chapter was co-written and developed by {{ scolari }} <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="25" height="25"> and {{ schwindt }} <img src="../../img/authors/sebastian.jpg" alt="Sebastian Schwindt" width="25" height="25">.
```

(tm-friction-zones)=
# Roughness (Friction) Zones

Similar to the assignment of multiple friction coefficient values to multiple model regions featured in the {ref}`BASEMENT tutorial <bm-geometry>`, Telemac2d provides routines for domain-wise (i.e., zonal) friction area definitions in the geometry (`*.slf`) file. Specifically, if the study domain is characterized by regions of different roughness, it is not sufficient to define a global friction through a `FRICTION COEFFICIENT` keyword in the steering (`.cas`) file. To define roughness zones the geometry (`.slf`) file requires an additional layer called `BOTTOM FRICTION` on top of the `BOTTOM` elevation. To this end, roughness values can be define in a roughness `.xyz` file created with QGIS or *Closed Lines* `.i2s` file created with BlueKenue. While QGIS is recommended to delineate roughness zones with correct and possibly precise georeferences, BlueKenue is required for interpolating the roughness from the `.xyz` or `.i2s` file on the geometry `.slf` file in the last step.


```{admonition} Requirements

* Understand geospatial data formats and be able to work with QGIS (see the {ref}`QGIS tutorial <qgis-tutorial>`).
* Complete the {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>`.
* An installation of {ref}`BlueKenue (also works on Linux, see the installation guide) <bluekenue>`
```


## Roughness.XYZ with QGIS (recommended)

The first step for delineating roughness zones in QGIS is to set up the coordinate reference system and save the project, analogous to the `QGIS pre-processing turorial <tm-qgis-prepro>`: 

* Open QGIS, and in the top menu go to **Project** > **Properties**.
* Activate the **CRS** tab.
* Set the CRS that your {ref}`basemap <basemap>` / {term}`DEM` data use; for this example, enter `UTM zone 33N` and select *UTM zone 33N (WGS84)* (EPSG 32633), which is basically not a great choice because of its low precision, but it will do the job for this tutorial.
* Click **Apply** and **OK**.
* Save the project into a new folder where all files for this tutorial will be stored.

It will be important to avoid overlapping that would lead to avoid ambiguous or missing definitions of regions. Therefore, activate snapping:

* Activate the *Snapping Toolbar*: **View** > **Toolbars** > **Snapping Toolbar**
* In the **Snapping toolbar** > **Enable Snapping** <img src="../../img/qgis/snapping-horseshoe.png">
* Enable snapping for
  * **Vertex**, **Segment**, and **Middle of Segments** <img src="../../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../../img/qgis/snapping-intersection.png">.
  * **Self Snapping** <img src="../../img/qgis/sym-self-snapping.png">.

This tutorial picks up the example from the {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>` to draw polygons along the [breaklines](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) and [liquid-boundaries](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles. The type of friction zones are inferred from a {ref}`Google Satellite basemap <basemap>`, and friction attributes are qualitatively estimated, which is just fine for a tutorial. In practice, we strongly recommend to perform field surveys on grain size distributions and high-precision differential GPS (DGPS) systems to delineate roughness zones on-site supported by drone imagery.

```{admonition} AI can do a better job
:class: tip
:name: ai-image-recognition-numerics

This tutorial shows how to manually draw polygons delineating particular roughness zones, such as *sand*, *gravel*, or *vegetation*. However, artificial intelligence (AI) has already been proven to do a great job in automatically recognizing similar terrain patches for consistent recognition of roughness zones. Examples can be found in {cite:t}`diazgomez_mapping_2022`, or [Kenny Larrieu's implementation of Segment Anything EO tools](https://github.com/klarrieu/segment-anything-eo).

What you need is:

* a modern drone (not too expensive anymore)
* ground truth: data on grain size distributions (> gravel: pebble counts, sand to gravel: bag & sieve, very fine sediment: freeze core/plate & sieve), object labels (i.e., DGPS points marking *vegetation/types*, *wood*, *reinforced banks*, *roads*, etc.)
* an algorithm that classifies any drone image after being trained on the ground truth; we are currently working on it and provide it here - stay tuned.
```

### Delineate Roughness Zone Polygons

The roughness zones can be described by attributes of a polygon shapefile. To create a new polygon shapefile, go to **Layer** > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <new-qgis-lyr-rough>`).

```{figure} ../../img/telemac/qgis-add-lyr.png
:alt: create polygon shapefile roughness zones telemac
:name: new-qgis-lyr-rough

Create a new polygon shapefile.
```

In the popup window enter the following definitions:

* **File name**: press on **...**, navigate to the project folder, and tap `friction-polygons`.
* **File encoding**: keep default (sample files use `UTF-8`).
* **Geometry type**: `Polygon`
* Below the *Additional dimensions* (not required), find and click on the **CRS** button to select the above-defined project coordinate system (example files: `EPSG:32633`).
* Add a **New Field**:
  * **Name**: `dMean`
  * **Type**: `Decimal (double)`
  * **Length**: `10`
  * **Precision**: `5`
  * Click **Add to Fields List**
* Add another **New Field**:
  * **Name**: `fricID`
  * **Type**: `Integer (32 bit)`
  * **Length**: `5`
  * Click **Add to Fields List**
* Press **OK** to create the new shapefile.

To follow this tutorial, import the [breaklines (download as zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) and [liquid-boundaries (download as zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles from the Telemac pre-processing. To draw polygons by editing fiction-polygons.shp along the breaklines and liquid boundaries, highlight **fiction-polygons** in the *Layers* panel, and enable editing by clicking on the yellow pen <img src="../../img/qgis/yellow-pen.png">. Activating **Add Polygon Feature** and draw polygons by snapping to points of the breaklines and liquid boundaries layers, according to {numref}`Fig. %s <tm-fricID-polygons>`. To **finalize each polygon** with a **right-click on the mouse** and **enter** the `fricID` and `dMean` values according to {numref}`Tab. %s <tab-tm-fricID-zones>` (qualitative grain sizes).

To **correct drawing errors** use the **Vertex Tool** <img src="../../img/qgis/sym-vertex-tool.png">. Finally, save the new polygons (edits of **friction-zones.shp**) by clicking on the **Save Layer Edits** <img src="../../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../../img/qgis/yellow-pen.png"> symbol.

**Alternatively, merge the breaklines and liquid boundaries, and use the *Polygonize* tool from the *Processing Toolbox* to convert the merged lines into a polygon shapefile.** However, the polygonization will miss some breaklines, which will require editing. Also, the `fricID` and `dMean` fields still need to be added through editing.

```{figure} ../../img/telemac/fricId-zones-overview.jpeg
:alt: qgis telemac roughness zone polygons
:name: tm-fricID-polygons

Example for describing roughness (friction) zones with polygons by four friction IDs (fricID) delineating (1) the riverbed, (2) block ramps, (3), gravel bars, and (4) floodplains. Background map: {cite:t}`googlesat` satellite imagery.
```

```{list-table} Four exemplary friction zones described by integer fricIDs and mean grain size diameters dMean.
:header-rows: 1
:name: tab-tm-fricID-zones

* - Zone name
  - Riverbed
  - Block ramps
  - Gravel banks
  - Floodplains
* - fricID
  - 1
  - 2
  - 3
  - 4
* - dMean (m)
  - 0.080
  - 0.300
  - 0.032
  - 1.000
```

```{admonition} Download the friction-polygons shapefile
:class: tip
Download the [zipped friction-polygons shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-polygons.zip) and unpack it into the project folder, for instance, `/ProjectHome/friction-polygons.[SHP]`.
```

### Generate Roughness Points

The next step on the pathway to creating the required XYZ file for assigning friction zones to a selafin geometry file is to generate (random) points inside the above-created polygons. To this end, **enter `random points inside polygons`** in the **search** field of the **Processing Toolbox**. In the **Random Points Inside Polygons** popup window ({numref}`Fig. %s <tm-fric-polygons2pts>`), enter the following:

* **Input layer**: `friction-polygons`
* **Sampling strategy**: `Points density`
* **Point count or density**: `0.25`  - use a smaller/larger value for fine/coarse meshes, but beware of potentially very large file sizes
* **Minimum distance between points**: `5.0`  - use a smaller/larger value for fine/coarse meshes
* **Random points**: click on **...** and define a target point shapefile name, such as `friction-pts.shp` to be stored in the project folder.
* Click **Run** to create the points shapefile. This process may take a while depending on the defined point density.

The resulting point shapefile is shown in {numref}`Fig. %s <tm-fric-pts>`

```{figure} ../../img/telemac/fric-zones-pts.png
:alt: random points polygons qgis telemac roughness zone
:name: tm-fric-polygons2pts

Settings in the Random Points Inside Polygons tool in QGIS. Carefully select the point count or density, which can cause very large output files. The minimum distance field may be used to reduce the number of points. 
```

```{figure} ../../img/telemac/fric-pts.jpg
:alt: random points roughness zone
:name: tm-fric-pts

The point shapefile resulting from using the Random Points Inside Polygons tool in QGIS. Background map: {cite:t}`googlesat` satellite imagery.
```

```{admonition} Download the friction-pts shapefile
:class: tip
Download the [zipped friction-pts shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts.zip) and unpack it into the project folder, for instance, `/ProjectHome/friction-pts.[SHP]`.
```


### Assign Friction Attributes to Points

Alas, the point generation does not automatically pick up the polygon attributes, which need to be interpolated to the points in this step. Depending on the targeted roughness law for use with Telemac, either the friction IDs or directly roughness coefficients can be added to the attribute table of the friction point shapefile. In this tutorial, a friction coefficient in the form of the Strickler roughness is interpolated and calculated using an empirical formula. A more complex case for calculating roughness values can be found in the BAW's Donau (*Danube*) case study (located in `/telemac/v8p4/examples/telemac2d/donau/`).

The transfer of the `dMean` and/or `fricID` attributes of the poylgons to the points is essentially an interpolation operation in which QGIS looks at every point and assigns it the `dMean` and/or `fricID` attributes of the closest polygon. To this end, click on to the **Vector** top menu > **Data Management Tools** > **Join Attributes by Location** (see {numref}`Fig. %s <fric-data-mgmt-join-attributes>`).


```{figure} ../../img/telemac/fric-data-mgmt-join-attributes.png
:alt: qgis friction points attribute table
:name: fric-data-mgmt-join-attributes


Open the Join Attributes by Location tool in QGIS.
```


```{figure} ../../img/telemac/fric-join-attributes-by-location.png
:alt: qgis friction join attributes by location
:name: fric-join-attributes-by-location
:scale: 75%
:align: right

Open the attribute table of the friction point table.
```

In the *Join Attributes by Location* popup window ({numref}`Fig. %s <fric-join-attributes-by-location>`) make the following settings:

* **Join to features in**: `friction-pts`
* **Features they (geometric predicate)**: check the `are within` box, deselect all others
* **By comparing to**: `friction-polygons`
* **Fields to add**: click on the **...** button to select `fricID` and/or `dMean` 
* **Join type**: `Take attributes of the first matching feature only (one-to-one)`
* **Joined layer**: click on the **...** button > **Save to file** > navigate to the **project folder** > **enter a filename, such as `friction-pts-at`**
* Click on **Run**.

The error message *No spatial index exists for input layer, performance will be severely degraded* can be ignored for this application. Still, to verify false output, it might be wise to also define the layer **Unjoinable features from first layer**.

As a result, the **friction-pts-at** is available in the **Layers** panel (see {numref}`Fig. %s <fric-pts-open-at>`).

To convert the mean grain sizes (`dMean`) into friction values, open the *Attribute Table* by **right-clicking** on the **friction-pts-at** layer in the **Layers** panel > **Open Attribute Table**.

```{figure} ../../img/telemac/fric-pts-open-at.png
:alt: qgis friction points attribute table
:name: fric-pts-open-at


Open the attribute table of the friction point shapefile with attribute table. Background map: {cite:t}`googlesat` satellite imagery.
```


Edit the attribute table ({numref}`Fig. %s <fric-pts-at-edit>`):

1. enable editing,
1. remove unnecessary columns, such as the `id` field, and potentially also the `fricID` field (this showcase will only use the `dMean` column),
1. open the **Field calculator**, which we will use in the next step to derive Strickler roughness values.


```{figure} ../../img/telemac/fric-pts-at-edit.png
:alt: friction points edit attribute table
:name: fric-pts-at-edit

The Attribute Table of the friction-pts-at layer with the highlighted (red rectangles) editing, remove columns, and field calculator buttons (from left to right).
```

````{admonition} Optional: derive x and y coordinates with Field Calculator
:class: dropdown

In the **Field Calculator**, add the $x$ and $y$ coordinates to the *Attribute Table*:

* check the box **Create a new field**
* **Output field name**: `x_coord`
* **Output field type**: `Decimal number (real)`
* **Output field length**: `10` and **Precision**: `10`
* Enter a formula by either selecting the x-value from the geometry in the scrollbox, or enter directly in the **Expression** field:

```
 x( @geometry ) 
```

**Analogously, add the `y_coord` with**:

```
 y( @geometry ) 
```

**Save** the edits in the *Attribute Table* by clicking on the disk symbol. 

````

According to {cite:t}`Meyer-Peter and Müller 1948 <meyer-peter_formulas_1948>`, the {cite:t}`strickler_beitrage_1923` roughness (friction) coefficient can be approximated with $k_{st}$ $\approx$ 26/$D_{90}^{1/6}$ based on the grain size $D_{90}$, where 90% of the surface sediment grains are smaller. In addition, we will assume that $D_{90} \approx 2.25 \cdot D_{mean}$ {cite:p}`rickenmann_evaluation_2011`. Thus, $k_{st} \approx 26 \cdot (2.25 \cdot D_{mean})^{-1/6}$. To run this calculation, go to the **Field Calculator** and (see {numref}`Fig. %s <fric-pts-open-at>`):

* check the box **Create a new field**
* **Output field name**: `k_st`
* **Output field type**: `Decimal number (real)`
* **Output field length**: `3` and **Precision**: `2`
* Enter a formula by either selecting `dMean` from `Fields and Values` in the scrollbox, or enter directly in the **Expression** field:

```
26 / ( ( 2.25 * "dMean" ) ^ ( 1 / 6 ) )
```

```{figure} ../../img/telemac/fric-field-calc-strickler.png
:alt: calculator strickler roughness qgis field attribute table
:name: fric-field-calc-strickler

Estimate the Strickler coefficient based on the mean grain size (dMean) with the Field Calculator in QGIS.
```



```{figure} ../../img/telemac/fric-at-final.png
:alt: x_coord y_coord coordinates strickler roughness qgis attribute table
:name: fric-at-final
:scale: 100%
:align: left

The finalized Attribute Table of the friction-pts-at layer with the optional x and y coordinates, and the estimated Strickler roughness coefficients.
```

Finally, **remove all remaining unnecessary fields** from the *Attribute Table* and **save** the edits by clicking on the disk symbol, and toggle (i.e., deactivate) editing.

```{admonition} Download the friction-pts-at shapefile
:class: tip
Download the [zipped friction-pts shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts-at.zip) and unpack it into the project folder, for instance, `/ProjectHome/friction-pts-at.[SHP]`.
```

### Export Points to XYZ

Start with opening the export dialogue with a right click on the friction-pts-at layer > Export > Save Features As... ({numref}`Fig. %s <fric-pts-export-as>`).


```{figure} ../../img/telemac/fric-pts-export-as.png
:alt: export friction points xyz qgis attribute table
:name: fric-pts-export-as
:scale: 100%

Open the export dialogue with a right click on the friction-pts-at layer > Export > Save Features As...
```

In the **Save Vector Layer as...** popup window, make the following settings ({numref}`Fig. %s <fric-export-xyz>`):

* **Format**: `Comma Separated Value [CSV`
* **File name**: click on **...**, navigate to the project folder, and enter `friction-pts.xyz` for file name (press **Save**).
* **Layer name**: keep clear
* **CRS**: make sure the CRS of the friction-pts-at layer is defined (in the showcase `EPSG:32633 - WGS 84 / UTM zone 33N`)
* **Encoding**: use default (in the showcase `UTF-8`)
* **Select** all relevant **fields**, that is, in the showcase, at least `k_st`. The optional `x_coord` and `y_coord` fields are only necessary if the geometry is not exported (for what ever reason).
* **Check** the **Persist layer metadata**
* **Geometry type**: `Automatic` (mostly default)
* **Scroll down** to the **Layer Options** and:
  * set the **GEOMETRY** to `AS_XY`
  * set the **SEPARATOR** to `TAB`
* **Uncheck** the **Add saved file to map** box at the bottom of the window.
* **Keep all other defaults** and click **OK**.

```{figure} ../../img/telemac/fric-export-xyz.png
:alt: xyz file export attribute table friction points
:name: fric-export-xyz

Settings in the Save Vector Layer as... popup window for exporting the friction points to an XYZ (tab-separated CSV) file.
```

QGIS will have exported the file with an `.xyz.csv` ending. **Rename the file** to **remove `.csv`** at the end. **Verify the correct formatting of the `.xyz` file** by opening it in a {ref}`text editor (e.g., Notepad++) <npp>`. Specifically, if you calculated and exported the `x_coord` and `y_coord` fields, and additionally the geometry, the `.xyz` file will hold two times the coordinates. In this case, import the `.xyz` file in a spreadsheet editor ({ref}`office application <lo>`), delete the `x_coord` and `y_coord` columns, and re-export the file as tab-separated CSV file. Read more about `.xyz` file conversion in the {ref}`QGIS tutorial <make-xyz>`.

````{admonition} Expand to see the correct header of the showcase friction-pts.xyz file
:class: dropdown

```
X Y k_st  
315976.648906296  5345616.71281044  40.30
315992.808134594  5345521.13037269  40.30
315983.283370604  5345655.68430873  40.30
315915.433790676  5345754.82689794  40.30
[...]
```
````

```{admonition} Download the showcase friction-pts.xyz file
:class: tip
Download [`friction-pts.xyz`](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts.xyz) and save it into the project folder, for instance, `/ProjectHome/friction-pts.xyz`.
```

## Zonal Bottom Friction Assignment in BlueKenue

This section walks through the interpolation of friction values on an existing selafin (`.slf`) geometry file. A showcase builds on the `.slf` file created in the {ref}`Telemac pre-processing tutorial <slf-prepro-tm>` ([download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf)). Start with **opening BlueKenue** and open the selafin `.slf` file: click on **File** > **Open...** > navigate to the directory where the `.slf` is stored, make sure to select **Telemac Selafin File (\*.slf)**, highlight `qgismesh.slf`, and press **Open**. Pull the `BOTTOM (BOTTOM)` layer from the work space data items to **Views** > **2D View (1)** to verify and visualize the correct import of the mesh ({numref}`Fig. %s <fric-bk-slf>`).


```{figure} ../../img/telemac/bk-slf.png
:alt: BlueKenue 2dmesh interpolated elevation
:name: fric-bk-slf

The showcase qgismesh.slf selafin file opened in BlueKenue.
```

### Import or Create Friction Zones

As an alternative to the creation of zonal friction values stored in an `.xyz`, generated with QGIS, such zones can also directly be drawn in BlueKenue through a series of *Closed lines*. However, because of BlueKenue's very limited capacities to deal with geospatial reference and coordinate systems (CRSs), **the preferable option** for creating friction zone input **is** the above-feature application of **QGIS**. 

`````{tab-set}
````{tab-item} Open the .xyz file in BlueKenue
To open the above-created `.xyz` file in BlueKenue:

* click on **File** > **Open...** 
* navigate to the project folder where the `.xyz` is stored
* make sure to select **All Files (\*.\*)** next to the **File name:** field
* highlight `qgismesh.slf`, and press **Open**.

```{figure} ../../img/telemac/bk-fric-xyz-properties.png
:alt: bluekenue roughness friction visualize coefficients
:name: bk-fric-xyz-properties
:scale: 100%
:align: left

Assign a friction (roughness) value (here: a Strickler roughness of 50) to the delineated area by the closed line.
```

**Ignore** the **warning** message (click **OK**). To verify and visualize the imported friction values **right-click** on the **friction-pts (X)** layer > **Properties** > go to the **Data** tab > **select Z(double)**, press **Apply**. Then, go to the **ColourScale** tab, press **Reset**, **Apply**, and **OK**.

Verify the correct representation of the friction values by pulling the `friction-pts (Z)` layer from the work space data items to **Views** > **2D View (1)** ({numref}`Fig. %s <bk-fric-pts>`).


```{figure} ../../img/telemac/bk-fric-pts.png
:alt: friction roughness coefficients bluekenue 
:name: bk-fric-pts


The imported friction-pts.xyz file (created with QGIS) visualized in BlueKenue.
```

````
````{tab-item} Create friction zones in BlueKenue

Start with creating new closed lines ({numref}`Fig. %s <bk-new-closed-lines>`), similar to polygons delineating roughness zones.

```{figure} ../../img/telemac/bk-new-closed-lines.png
:alt: bluekenue create closed line
:name: bk-new-closed-lines
:scale: 50%
:align: left

Settings in the Save Vector Layer as... popup window for exporting the friction points to an XYZ (tab-separated CSV) file.
```

```{figure} ../../img/telemac/bk-finalize-friction-cl.png
:alt: bluekenue roughness friction closed line
:name: bk-finalize-friction-cl
:scale: 100%
:align: right

Assign a friction (roughness) value (here: a Strickler roughness of 50) to the delineated area by the closed line.
```

After drawing of a *Closed line* is finished, press the `Esc` key and the window shown in {numref}`Fig. %s <bk-finalize-friction-cl>` will appear, where a roughness value can be assigned. The exemplary figure assigns a Strickler roughness of `50` in the **Value** field to a *Closed line* named `A-D_substrate`. Continue to assign names to all relevant roughness areas.
````
`````

### Interpolate Friction on the SLF Mesh

In BlueKenue, go to **File** > **New** > **2D Interpolator**, which will then occur in the **Work Space** > **Data Items**. **Drag & drop** either the **friction-pts** `.xyz` points or the *Closed line* objects delineating roughness zones **on the new 2D Interpolator** (see {numref}`Fig. %s <bk-fric-2d-interpolator>`).

```{figure} ../../img/telemac/bk-fric-2d-interpolator.png
:alt: bluekenue 2d interpolator roughness friction
:name: bk-fric-2d-interpolator
:scale: 100%


Drag & drop the friction-pts (or closed lines) on a new 2D Interpolator in BlueKenue.
```

```{figure} ../../img/telemac/bk-new-slf-variable.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable
:figclass: margin


Add a new Variable to the Selafin object.
```

Next, add a new Variable to the `qgismesh.slf` selafin file:

* In **Work Space** > **Data Items**, find the **Selafin `qgismesh`** object and **right-click** on it.
* Click on **Add Variable...** and enter the following in the popup window ({numref}`Fig. %s <bk-new-slf-variable>`):
  * **Mesh**: `BOTTOM`
  * **Name**: `BOTTOM FRICTION`
  * **Units**: `strickler` (or keep clear, irrelevant field)
  * **Default Node Value**: `30` (default Strickler value to use when no friction points can be found)
 

To interpolate the friction values to the mesh, highlight the new variable variable `BOTTOM FRICTION` of the `qgismesh` object in **Work Space** > **Data Items**. With this new mesh variable highlighted go to **Tools** > **Map Object...** (top menu in {numref}`Fig. %s <bk-map-2d-interpolator>`), select the **new 2D Interpolator**, and click **OK**, which opens the **Processing...** popup window. After the processing completed, click **OK**.

```{figure} ../../img/telemac/bk-map-2d-interpolator.png
:alt: map object  2dinterpolator roughness friction bluekenue
:name: bk-map-2d-interpolator
:scale: 100%

Map the friction value on the new 2D Interpolator in BlueKenue.
```

```{figure} ../../img/telemac/bk-fric-colourscale.png
:alt: bottom friction colourscale selafin bluekenue
:name: bk-fric-colourscale
:figclass: margin

Adjust the color scale for BOTTOM FRICTION.
```

Verify the correct interpolation:
* Define a relevant color scale:
  * In **Work Space** > **Data Items** > **qgismesh**, **right-click** on the new **BOTTOM FRICTION** variable > **Properties**.
  * In the properties, go to the **ColourScale** tab, and use, for example, a *Linear* scale with `10` *Levels*, a *Min* of `22`, and an *Interval* of `1.8`. The exemplary minima and interval are good choices for the showcase, but other settings might be preferable for other applications (e.g., prefer *Min* of `0` when using Manning's n).
  * Press **Apply** > **OK**.
* **Drag & drop** the **BOTTOM FRICTION** variable into **Views** > **2D View (1)** to verify the correct interpolation of friction values (e.g., see {numref}`Fig. %s <bk-fric-on-mesh>` for the showcase).

```{figure} ../../img/telemac/bk-fric-on-mesh.png
:alt: selfin slf mesh bottom friction bluekenue
:name: bk-fric-on-mesh

The correctly interpolated new BOTTOM FRICTION variable of the qgismesh.slf mesh.
```

To **save** the selafin **mesh** with interpolated the interpolated friction values, **highlight the selafin object** (e.g., `qgismesh`) and **click on the disk <img src="../../img/telemac/bk-sym-save.png"> symbol**. Click **Yes** to confirm replacing it the `.slf` file.


```{admonition} Download the qgismesh.slf with BOTTOM FRICTION
:class: tip
Download the updated [qgismesh-friction.slf with BOTTOM FRICTION](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf).
```

(zonal-fric-cas)=
## Implementation in the CAS File


````{admonition} Under construction - Incomplete instructions!
:class: error

The updated `qgismesh.slf` can be used just like in the {ref}`steady 2d tutorial <telemac2d-steady>`, but some keywords need to be added to make Telemac recognize the newly defined friction zones in the `BOTTOM FRICTION` variable. Previously, friction was defined as follows in the Telemac `.cas` steering file:

```fortran
/ steady 2d .cas steering file
/ Friction at the bed
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
```

With the pre-defined Strickler coefficients, use:

```fortran
/ steady 2d .cas steering file
/ Friction at the bed
LAW OF BOTTOM FRICTION : 3 / 3-Strickler
/ FRICTION COEFFICIENT : 30 / not use with zonal friction
FRICTION DATA : YES / default is NO
FRICTION DATA FILE : 'BOTTOM FRICTION'
MAXIMIM NUMBER OF FRICTION DOMAINS : 20 / default is 10
```
````


## Telemac Examples Cases

* The BAW's Donau case study that lives in `/telemac/v8p2/examples/telemac2d/donau/` features the usage of a `*.bfr` **ZONES FILE**, and a `roughness.tbl` **FRICTION DATA FILE**. Zonal friction values are enabled through the `FRICTION DATA : YES` keyword in the `t2d_donau.cas` file. The Donau example was also presented at the XXth Telemac-Mascaret user conference and the conference proceedings are available at the BAW's [HENRY portal](https://hdl.handle.net/20.500.11970/100418) (look for the contribution *Reverse engineering of initial & boundary conditions with TELEMAC and algorithmic differentiation*).
* Also, the [Baxter tutorial](http://www.opentelemac.org/index.php/component/jdownloads/summary/4-training-and-tutorials/185-telemac-2d-tutorial?Itemid=55) features friction zones.

In addition, Appendix E of the {{ tm2d }} provides explanations for the implementation of zonal friction values. Note that the proposed modification of the **FRICTION_USER** Fortran function (subroutine) is not mandatory. Here are some tips for when the FRICTION_USER subroutines must be enabled anyway (e.g., to implement a new roughness law, such as the {cite:t}`ferguson_flow_2007` equation):

* The FICTION_USER subroutine can be found in `/telemac/v8p2/sources/telemac2d/friction_user.f`.
* To use a modified version, copy `friction_user.f` to a new subfolder called `/user_fortran/` in your simulation case folder.
* Modify and save edits in `/your/simulation/case/user_fortran/friction_user.f`.
* Tell the steering (`*.cas`) file to use the modified FRICTION_USER Fortran file by adding the keyword `FORTRAN FILE : 'user_fortran'`, which makes Telemac2d look up Fortran files in the `/user_fortran/` subfolder.

