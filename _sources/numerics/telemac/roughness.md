```{admonition} Contributors
:class: tip
This chapter was co-written and developed by {{ scolari }} <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="25" height="25"> and {{ schwindt }} <img src="../../img/authors/sebastian.jpg" alt="Sebastian Schwindt" width="25" height="25">.
```

(tm-friction-zones)=
# Friction (Roughness) Zones

Similar to the assignment of multiple friction coefficient values to multiple model regions featured in the {ref}`BASEMENT tutorial <bm-geometry>`, Telemac2d provides routines for domain-wise (i.e., zonal) friction area definitions in the geometry (`.slf`) mesh file. Specifically, if the study domain is characterized by regions of different roughness, it is not sufficient to define global friction through a `FRICTION COEFFICIENT` keyword in the steering (`.cas`) file. Defining roughness zones in the mesh (`.slf`) file requires an additional layer called `BOTTOM FRICTION` or `FRIC_ID` on top of the `BOTTOM` elevation. To this end, roughness values can be defined in a roughness `.xyz` file created with QGIS ({ref}`recommended <tm-friction-qgis>`) or *Closed Lines* `.i2s` created with BlueKenue ({ref}`see the meshing section <bk-import-friction>`). While QGIS is recommended to delineate roughness zones with correct and possibly precise georeferences, BlueKenue is still required for interpolating the roughness from the `.xyz` or `.i2s` file on the `.slf` file in the last step.


```{admonition} Requirements

* Understand geospatial data formats and know to work with QGIS (see the {ref}`QGIS tutorial <qgis-tutorial>`).
* Complete the {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>`.
* Installation of {ref}`BlueKenue (also works on Linux, see the installation guide) <bluekenue>`, and {ref}`Telemac <telemac-install>`.
```

(tm-friction-qgis)=
## Roughness.XYZ with QGIS (recommended)

The first step for delineating roughness zones in QGIS is to set up the coordinate reference system and save the project, analogous to the `QGIS pre-processing tutorial <tm-qgis-prepro>`: 

* Open QGIS, and in the top menu go to **Project** > **Properties**.
* Activate the **CRS** tab.
* Set the CRS that your {ref}`basemap <basemap>` / {term}`DEM` data use; for this example, enter `UTM zone 33N` and select *UTM zone 33N (WGS84)* (EPSG 32633), which is not a great choice because of its low precision, but it will do the job for this tutorial.
* Click **Apply** and **OK**.
* Save the project into a new folder where all files for this tutorial will be stored.

It will be important to avoid overlapping that would lead to ambiguous or missing definitions of regions. Therefore, activate snapping:

* Activate the *Snapping Toolbar*: **View** > **Toolbars** > **Snapping Toolbar**
* In the **Snapping toolbar** > **Enable Snapping** <img src="../../img/qgis/snapping-horseshoe.png">
* Enable snapping for
  * **Vertex**, **Segment**, and **Middle of Segments** <img src="../../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../../img/qgis/snapping-intersection.png">.
  * **Self Snapping** <img src="../../img/qgis/sym-self-snapping.png">.

This tutorial picks up the example from the {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>` to draw polygons along the [breaklines](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) and [liquid-boundaries](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles. The friction zones are inferred from a {ref}`Google Satellite basemap <basemap>` and friction attributes are qualitatively estimated, which is just fine for a tutorial. In practice, we strongly recommend performing field surveys on grain size distributions with high-precision differential GPS (DGPS) systems to delineate roughness zones on-site supported by drone imagery.

```{admonition} AI can do a better job
:class: tip
:name: ai-image-recognition-numerics

This tutorial shows how to manually draw polygons delineating particular roughness zones, such as *sand*, *gravel*, or *vegetation*. However, artificial intelligence (AI) has already been proven to do a great job in automatically recognizing similar terrain patches for consistent recognition of roughness zones. Examples can be found in {cite:t}`diazgomez_mapping_2022` or [Kenny Larrieu's implementation of Segment Anything EO tools](https://github.com/klarrieu/segment-anything-eo).

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

In the popup window, enter the following definitions:

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

To follow this tutorial, import the [breaklines (download as zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) and [liquid-boundaries (download as zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles from the Telemac pre-processing. To draw polygons by editing fiction-polygons.shp along the breaklines and liquid boundaries, highlight **fiction-polygons** in the *Layers* panel, and enable editing by clicking on the yellow pen <img src="../../img/qgis/yellow-pen.png">. Activating **Add Polygon Feature** and draw polygons by snapping to points of the *breaklines* and *liquid boundaries* layers, according to {numref}`Fig. %s <tm-fricID-polygons>`. To **finalize each polygon** with a **right-click on the mouse** and **enter** the `fricID` and `dMean` values according to {numref}`Tab. %s <tab-tm-fricID-zones>` (qualitative grain sizes).

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

The resulting point shapefile is shown in {numref}`Fig. %s <tm-fric-pts>`.

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

Alas, the point generation does not automatically pick up the polygon attributes, which need to be interpolated to the points. Depending on the targeted roughness law for use with Telemac, either the friction IDs or directly roughness coefficients can be added to the attribute table of the friction point shapefile. In this tutorial, a friction coefficient in the form of the Strickler roughness is interpolated and calculated using an empirical formula. A more complex case for calculating roughness values can be found in the BAW's Donau (*Danube*) case study (located in `HOMETEL/examples/telemac2d/donau/`).

The transfer of the `dMean` and/or `fricID` attributes of the polygons to the points is essentially an interpolation operation in which QGIS looks at every point and assigns it the `dMean` and/or `fricID` attributes of the closest polygon. To this end, click on the **Vector** top menu > **Data Management Tools** > **Join Attributes by Location** (see {numref}`Fig. %s <fric-data-mgmt-join-attributes>`).


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

Open the Attribute Table of the friction point table.
```

In the *Join Attributes by Location* popup window ({numref}`Fig. %s <fric-join-attributes-by-location>`) make the following settings:

* **Join to features in**: `friction-pts`
* **Features they (geometric predicate)**: check the `are within` box, deselect all others
* **By comparing to**: `friction-polygons`
* **Fields to add**: click on the **...** button to select `fricID` and/or `dMean` 
* **Join type**: `Take attributes of the first matching feature only (one-to-one)`
* **Joined layer**: click on the **...** button > **Save to file** > navigate to the **project folder** > **enter a filename, such as `friction-pts-at`**
* Click on **Run**.

The error message *No spatial index exists for input layer, performance will be severely degraded* can be ignored for this application. Still, to verify any false output, it might be wise to also define the layer **Unjoinable features from first layer**.

As a result, the **friction-pts-at** is available in the **Layers** panel (see {numref}`Fig. %s <fric-pts-open-at>`).

To convert the mean grain sizes (`dMean`) into friction values, open the *Attribute Table* by **right-clicking** on the **friction-pts-at** layer in the **Layers** panel > **Open Attribute Table**.

```{figure} ../../img/telemac/fric-pts-open-at.png
:alt: qgis friction points attribute table
:name: fric-pts-open-at


Open the Attribute Table of the friction point shapefile with attribute table. Background map: {cite:t}`googlesat` satellite imagery.
```


Edit the **Attribute Table** ({numref}`Fig. %s <fric-pts-at-edit>`):

1. enable editing,
1. remove unnecessary columns, such as the `id` field, and potentially also the `fricID` field (this showcase will only use the `dMean` column),
1. open the **Field calculator**, which we will use in the next step to derive Strickler roughness values.


```{figure} ../../img/telemac/fric-pts-at-edit.png
:alt: friction points edit attribute table
:name: fric-pts-at-edit

The Attribute Table of the friction-pts-at layer with the highlighted (red rectangles) editing, remove columns, and field calculator buttons (from left to right).
```

````{admonition} Optional: derive x and y coordinates with the Field Calculator
:class: dropdown

In the **Field Calculator**, add the $x$ and $y$ coordinates to the *Attribute Table*:

* check the box **Create a new field**
* **Output field name**: `x_coord`
* **Output field type**: `Decimal number (real)`
* **Output field length**: `10` and **Precision**: `10`
* Enter a formula by either selecting the x-value from the geometry in the scrollbox or entering directly in the **Expression** field:

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
* Enter a formula by either selecting `dMean` from `Fields and Values` in the scrollbox or directly entering the equation in the **Expression** field:

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
* **Select** all relevant **fields**, that is, in the showcase, at least `k_st`. The optional `x_coord` and `y_coord` fields are only necessary if the geometry is not exported (for whatever reason).
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

QGIS will have exported the file with a `.xyz.csv` ending. **Rename the file** to **remove `.csv`** at the end. **Verify the correct formatting of the `.xyz` file** by opening it in a {ref}`text editor (e.g., Notepad++) <npp>`. For instance, if you calculated and exported the `x_coord` and `y_coord` fields, and additionally the geometry, the `.xyz` file will hold two times the coordinates. In this case, import the `.xyz` file in a spreadsheet editor (i.e., {ref}`office application <lo>`), delete the `x_coord` and `y_coord` columns, and re-export the file as a tab-separated CSV file. Read more about `.xyz` file conversion in the {ref}`QGIS tutorial <make-xyz>`.

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

## Alternative: Draw Friction Zones in BlueKenue

This procedure is an imprecise alternative to the above-described `roughness.xyz` creation because of BlueKenue's weak geospatial referencing capacities, which is why the below {ref}`instruction box <bk-closed-fric-lines>` is only provided for completeness.

````{admonition} Unfold to read this non-recommended alternative
:class: note, dropdown
:name: bk-closed-fric-lines

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

After drawing a *Closed line* is finished, press the `Esc` key and the window shown in {numref}`Fig. %s <bk-finalize-friction-cl>` will appear, where a roughness value can be assigned. The exemplary figure assigns a Strickler roughness of `50` in the **Value** field to a *Closed line* named `A-D_substrate`. Continue to assign names to all relevant roughness areas.

Finally, **save** the *Closed line* objects as `.i2s` / `.i3s` files.
````


(bk-interpolate-fric-zones)=
# Zonal Friction Mesh (BlueKenue)

This section walks through the interpolation of friction values on an existing selafin (`.slf`) geometry file. The showcase builds on the `.slf` file created in the {ref}`Telemac pre-processing tutorial <slf-prepro-tm>` ([download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf)). Start with **opening BlueKenue** and open the selafin `.slf` file: click on **File** > **Open...** > navigate to the directory where the `.slf` is stored, make sure to select **Telemac Selafin File (\*.slf)**, highlight `qgismesh.slf`, and press **Open**. Pull the `BOTTOM (BOTTOM)` layer from the workspace data items to **Views** > **2D View (1)** to verify and visualize the correct import of the mesh ({numref}`Fig. %s <fric-bk-slf>`).


```{figure} ../../img/telemac/bk-slf.png
:alt: BlueKenue 2dmesh interpolated elevation
:name: fric-bk-slf

The showcase qgismesh.slf selafin file opened in BlueKenue.
```

(bk-import-friction)=
## Import Friction Zones

As an alternative to the creation of zonal friction values stored in a `.xyz` file generated with QGIS, zones can also be directly drawn in BlueKenue through a series of *Closed lines*. However, because of BlueKenue's very limited capacities to deal with geospatial references and coordinate systems (CRSs), **the preferable option** for creating friction zone input **is** the above-featured application of **QGIS**. 

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

Verify the correct representation of the friction values by pulling the `friction-pts (Z)` layer from the workspace data items to **Views** > **2D View (1)** ({numref}`Fig. %s <bk-fric-pts>`).


```{figure} ../../img/telemac/bk-fric-pts.png
:alt: friction roughness coefficients bluekenue 
:name: bk-fric-pts


The imported friction-pts.xyz file (created with QGIS) visualized in BlueKenue.
```
````

````{tab-item} Closed lines from BlueKenue
If not yet done, import the *Closed lines* delineating roughness zones in the form of `.i2s` / `.i3s` files.
````
`````

## Interpolate Friction on the Mesh

In BlueKenue, go to **File** > **New** > **2D Interpolator**, which will occur in the **Work Space** > **Data Items**. **Drag & drop** either the **friction-pts** `.xyz` points or the *Closed line* objects delineating roughness zones **on the new 2D Interpolator** (see {numref}`Fig. %s <bk-fric-2d-interpolator>`).

```{figure} ../../img/telemac/bk-fric-2d-interpolator.png
:alt: bluekenue 2d interpolator roughness friction
:name: bk-fric-2d-interpolator
:scale: 100%


Drag & drop the friction-pts (or closed lines) on a new 2D Interpolator in BlueKenue.
```



Next, add a new variable to the `qgismesh.slf` mesh by highlighting the **Selafin `qgismesh`** object (in **Work Space** > **Data Items**), and **right-clicking** on it.  Click on **Add Variable...** and enter the following in the popup window ({numref}`Fig. %s <bk-new-slf-variable-fric>` or {numref}`Fig. %s <bk-new-slf-variable-fricID>`), depending on if you are working with friction values (as showcased here with Strickler roughness), or {ref}`friction IDs (see below) <tm-fricID>`:

`````{tab-set}
````{tab-item} BOTTOM FRICTION (Strickler) value
```{figure} ../../img/telemac/bk-new-slf-variable-fric.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fric
:scale: 100%
:align: right


Add a new Variable to the Selafin object for direct friction values.
```
* **Mesh**: `BOTTOM`
* **Name**: `BOTTOM FRICTION` (this example)
* **Units**: keep clear (irrelevant field)
* **Default Node Value**: `30` (in this example) for a default (Strickler) value to use when no xyz friction points can be found in the vicinity of a mesh node

````

````{tab-item} FRICTION ID
```{figure} ../../img/telemac/bk-new-slf-variable-fricID.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fricID
:scale: 100%
:align: right


Add a new Variable to the Selafin object for friction IDs.
```

* **Mesh**: `BOTTOM`
* **Name**: `FRIC_ID` (must be entered, cannot be selected from list)
* **Units**: keep clear (irrelevant field)
* **Default Node Value**: `0` (ID to use when no xyz points can be found in the vicinity of a mesh node)

````
`````

To interpolate the friction values on the mesh, highlight the new variable variable `BOTTOM FRICTION` (or `FRIC_ID`) of the `qgismesh` object in **Work Space** > **Data Items**. The *Anonymous Attribute* of the new variable can be ignored. To map the new variable onto the mesh:

* Highlight the new `BOTTOM FRICTION` (or `FRIC_ID`) mesh variable (in **Data Items**)
* Go to **Tools** > **Map Object...** (top menu in {numref}`Fig. %s <bk-map-2d-interpolator>`)
* Select the **new 2D Interpolator**, and click **OK**, which opens the **Processing...** popup window
* After the processing is completed, click **OK**.

```{figure} ../../img/telemac/bk-map-2d-interpolator.png
:alt: map object  2dinterpolator roughness friction bluekenue
:name: bk-map-2d-interpolator
:scale: 100%

Map the friction value on the new 2D Interpolator in BlueKenue.
```

```{figure} ../../img/telemac/bk-fric-colourscale.png
:alt: bottom friction colourscale selafin bluekenue
:name: bk-fric-colourscale
:scale: 100%
:align: right

Adjust the color scale for BOTTOM FRICTION.
```

Verify the correct interpolation:

* Define a relevant color scale:
  * In **Work Space** > **Data Items** > **qgismesh**, **right-click** on the new **BOTTOM FRICTION** variable > **Properties**.
  * In the properties, go to the **ColourScale** tab, and use, for example, a *Linear* scale with `10` *Levels*, a *Min* of `22`, and an *Interval* of `1.8`. The exemplary minima and interval are good choices for the showcase, but other settings might be preferable for other applications (e.g., prefer *Min* of `0` when using Manning's $n_m$).
  * Press **Apply** > **OK**.
* **Drag & drop** the **BOTTOM FRICTION** variable into **Views** > **2D View (1)** to verify the correct interpolation of friction values (e.g., see {numref}`Fig. %s <bk-fric-on-mesh>` for the showcase).

```{figure} ../../img/telemac/bk-fric-on-mesh.png
:alt: selfin slf mesh bottom friction bluekenue
:name: bk-fric-on-mesh

The correctly interpolated new BOTTOM FRICTION variable of the qgismesh.slf mesh.
```

To **save** the selafin **mesh** with interpolated the interpolated friction values, **right-click** on the **qgismesh selafin object** > **Properties** > go to the **Meta Data** tab, and enter a new **Name**, for example, `qgismesh-friction`. Next, **highlight the selafin object** (e.g., `qgismesh-friction`) and **click on the disk <img src="../../img/telemac/bk-sym-save.png"> symbol**. If renaming did no take effect on the file name, confirm replacing the existing file.


```{admonition} Download qgismesh-friction.slf (with BOTTOM FRICTION)
:class: tip
Download the updated [qgismesh-friction.slf with BOTTOM FRICTION](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf).
```


# Telemac Bindings

(zonal-fric-cas)=
## Implementation in the CAS File

### Friction Keywords

The updated `qgismesh-friction.slf` mesh can be used just like in the {ref}`steady 2d tutorial <telemac2d-steady>`, but some keywords need to be modified, even though the `BOTTOM FRICTION` values assigned in the `.slf` mesh automatically overwrite the global **FRICTION COEFFICIENT** keyword in the `.cas` steering file. However, we need to make Telemac recognize the newly defined `BOTTOM FRICTION` zones as **Strickler** roughness type. To this end, change the **LAW OF BOTTOM FRICTION** to `3` (instead of `4` pointing to Manning's $n_m$), and set the default **FRICTION COEFFICIENT** to `33` (inverse of $n_m$ = 0.03). The definition of the **FRICTION COEFFICIENT** is for coherence and is not strictly needed as it will be overwritten by the `BOTTOM FRICTION` from the `.slf` mesh.

`````{tab-set}
````{tab-item} New (Strickler)
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ Friction at the bed
LAW OF BOTTOM FRICTION : 3 / 3-Strickler
FRICTION COEFFICIENT : 33  / will be overwritten by zonal friction values
```
````

````{tab-item} Old (Manning from steady 2d)
```fortran
/ steady2d.cas steering file
/ ...
/ Friction at the bed
LAW OF BOTTOM FRICTION : 4  / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
```
````
`````

Add the letter `W` to the graphic printouts for writing the friction coefficient to the results file:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : 'U,V,H,S,Q,W' / add W for friction coefficient
```


````{admonition} Do you have more than 10 different friction zones?
:class: tip, dropdown

To increase the number of friction zones recognized by Telemac, set the **MAXIMUM NUMBER OF FRICTION DOMAINS** keyword, for example, to `20`:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
MAXIMUM NUMBER OF FRICTION DOMAINS : 20 / default is 10
```
````


### Initial Hotstart Conditions (optional)

**The following descriptions refer to section 4.1.3 in the {{ tm2d }}.**

To speed up the simulation, this tutorial re-uses the output of the {ref}`steady 2d simulation <telemac2d-steady>` (though, re-created with a printout period of `2500` steps). This type of model initialization is also called *hotstart*, here, based on the steady results file [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf), which needs to be defined as **PREVIOUS COMPUTATION FILE**:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady-t15k.slf / results of 35 CMS steady simulation after 15000 timesteps
```

With the hotstart conditions, the boundaries can be eased to:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.; 0.
PRESCRIBED ELEVATIONS : 0.; 371.33
```

For these boundary conditions to take effect, the liquid boundaries file from the steady 2d simulation must be modified:

* open *boundaries.cli* in a {ref}`text editor <npp>`
* find the `5 5 5` (prescribed Q and H) upstream boundary and replace it with `4 5 5` (prescribed Q only)
* save and close *boundaries.cli*
* for more information, have a look at the spotlight chapter on {ref}`boundary conditions <tm-foc-bc>`
* alternatively, [download the adapted boundaries.cli here](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli).

Finally, comment out any initial conditions keywords in the `.cas` steering file, for instance:


```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ INITIAL CONDITIONS : 'ZERO DEPTH'
/ INITIAL DEPTH : 0.005
```

## Run Friction Zone Simulation

Make sure all required files are placed in a simulation folder (e.g., `/HOME/modeling/friction-tutorial/`), notably:

* the [qgismesh-friction.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf) mesh with `BOTTOM` and `BOTTOM FRICTION` information
* the corrected [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli)
* the [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf) results file to enable the hotstart 
* the [steady2d-zonal-ks.cas](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas) steering file with updated keywords.

Navigate (`cd`) to the Telemac installation directory (`HOEMTEL`) to activate (`source`) the Telemac environment in Terminal (use the same environment as for {ref}`compiling Telemac <tm-compile>`):

```
cd ~/telemac/v8p4/configs
source pysource.gfortranHPC.sh
```

Next, `cd` into the simulation folder and run the simulation, potentially with the `-s` flag, to trace back {ref}`flux convergence <tm-convergence>`:

```
cd ~/modeling/friction-tutorial/
telemac2d.py steady2d-zonal-ks.cas -s
```

The successful simulation run will have finished with something like this:

````{admonition} Unfold to see the correct Terminal output
:class: note, dropdown

```
================================================================================
 ITERATION    10000    TIME:  6 H 56 MIN  40.0000 S   (    25000.0000 S)
--------------------------------------------------------------------------------

[...]

--------------------------------------------------------------------------------
                       BALANCE OF WATER VOLUME
     VOLUME IN THE DOMAIN :    268926.5     M3
     FLUX BOUNDARY    1:     35.00000     M3/S  ( >0 : ENTERING  <0 : EXITING )
     FLUX BOUNDARY    2:    -34.99963     M3/S  ( >0 : ENTERING  <0 : EXITING )
     RELATIVE ERROR IN VOLUME AT T =       0.2500E+05 S :    0.2327571E-14
--------------------------------------------------------------------------------
                   FINAL BALANCE OF WATER VOLUME

     RELATIVE ERROR CUMULATED ON VOLUME:    0.4112446E-14

     INITIAL VOLUME              :     268899.0     M3
     FINAL VOLUME                :     268926.5     M3
     VOLUME THAT ENTERED THE DOMAIN:     27.48362     M3  ( IF <0 EXIT )
     TOTAL VOLUME LOST             :    0.1105946E-08 M3

 END OF TIME LOOP

 EXITING MPI

                     *************************************
                     *    END OF MEMORY ORGANIZATION:    *
                     *************************************

 CORRECT END OF RUN

 ELAPSE TIME :
                              3  MINUTES
                              3  SECONDS
Note: The following floating-point exceptions are signalling: IEEE_UNDERFLOW_FLAG IEEE_DENORMAL
STOP 0

... merging separated result files

... handling result files

        moving: r2dsteady-ks-zonal.slf
      copying: steady2d-zonal-ks.cas_2030-07-28-14h55min04s.sortie
... deleting working dir



My work is done

```
````

The resulting {ref}`flux convergence <tm-flux-convergence>` and {ref}`convergence rates <tm-calculate-convergence>` should look similar to this:

`````{tab-set}
````{tab-item} Flux convergence
```{figure} ../../img/telemac/flux-convergence-zonal-fric.png
:alt: zonal friction telemac flux convergence pythomac
:name: tm-friction-flux-convergence

Flux convergence plot across the two boundaries of the hotstarted steady Telemac2d simulation, starting at a simulation time of 15000 timesteps.
```
````

````{tab-item} Convergence rate
```{figure} ../../img/telemac/convergence-rate-zonal-fric.png
:alt: zonal friction convergence rate fluxes telemac boundaries
:name: tm-friction-convergence-rate

The convergence rate $\iota$ as a function 15000 simulation timesteps of the hotstarted steady 2d simulation with friction zones.
```
````
`````

The required [steady2d-zonal-ks.cas_2023-07-28-14h55min04s is available here](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas_2023-07-28-14h55min04s) for use with instructions from the spotlight chapter on {ref}`convergence <tm-convergence>`.

```{admonition} Look at the results in QGIS

Load the simulation results file (`r2dsteady-ks-zonal.slf`) in QGIS to verify the correctness of the used bottom friction and look at the slight changes in flow velocity and water depth resulting from the now different roughness (friction) values.
```

(tm-fricID)=
# Working with Friction IDs

The friction zones can also be assigned through friction IDs, which then require setting up a zones file and friction data file, for example, as showcased in the Donau example (`HOMETEL/examples/telemac2d/donau/`). 

```{admonition} The Donau zonal friction ID example
:class: tip

The BAW's Donau case study lives in `HOMETEL/examples/telemac2d/donau/` and it was presented at the XXth Telemac-Mascaret user conference. The conference proceedings are available at the BAW's [HENRY portal](https://hdl.handle.net/20.500.11970/100418) (look for the contribution *Reverse engineering of initial & boundary conditions with Telemac and algorithmic differentiation*). However, this case uses an unnecessary complication in the form of a `.bfr` zone file.
```

In the showcase of this tutorial, working with friction tables required assigning the friction IDs defined in {numref}`Tab. %s <tab-tm-fricID-zones>` to the `BOTTOM FRICTION` variable of the `.slf` mesh. The according files can be downloaded from our repositories:

* [get friction-with-IDs.xyz](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction-with-IDs.xyz) for interpolation in BlueKenue ({ref}`see above <bk-interpolate-fric-zones>`, or directly
* [get qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) with `BOTTOM` and `FRIC_ID` instead of `BOTTOM FRICTION` Strickler roughness coefficients (uses default friction ID `0`).

## friction.tbl & CAS

### Create friction.tbl

Create a friction table file called `friction.tbl` (consider this [friction.tbl template](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl)) with the following content, where the `no` entries (here starting in line 36) must correspond to the `FRIC_ID` assigned to the mesh (recall {numref}`Fig. %s <bk-new-slf-variable-fricID>`):

```{margin} More information

Appendix E of the {{ tm2d }} provides more explanations on the tabular parameters (e.g., `typeB`, `rB`, or `nDefB`), and the friction laws (e.g., STRI, NIKU) are explained in more detail in this eBook in the steady-2d {ref}`section on friction <tm2d-friction>`. 
```

```{code-block} fortran
---
name: friction_tbl
linenos: True
caption: |
    Example for a friction(.tbl) ID table.
---
* ----------------------------------------------------------------------------- 
*  EXAMPLE ADAPTED FROM HOMETEL/examples/telemac2d/donau/
*
*  Implemented roughness laws: 
*    NOFR : no friction         (number of values) 
*    HAAL : Haaland   law       (1 value  : rB) 
*    CHEZ : Chezy     law       (1 value  : rB) 
*    STRI : Strickler law       (1 value  : rB) 
*    MANN : Manning   law       (1 value  : rB) 
*    NIKU : Nikuradse law       (1 value  : rB) 
*    LOGW : Log Wall  law       (1 value  : rB) 
*    COWH : Colebrook-White law (2 values : rB, nDef) 
* 
*  no             : FRIC_ID assigned to the SLF mesh
* 
*  Riverbed
*  ------------- 
*  typeB          : roughness law for riverbed
*  rB             : friction value for riverbed
*  nDefB          : Mannings n for shallow flow zones
* 
*  Later walls (only with k-epsilon model) 
*  ----------------------------------------- 
*  typeS          : roughness law for walls          (option) 
*  rS             : friction value for walls         (option) 
*  nDefS          : Mannings n for shallow waters    (option) 
* 
*  Non-submerged Vegetation (if needed) 
*  ------------------------ 
*  dp             : mean diameter                                (option) 
*  sp             : averaged distance between roughness elements (option) 
* 
* ----------------------------------------------------------------------------- 
* no        typeB  rB    NDefB  typeS  rS  NDefS   dp     sp 
* 
  0  STRI   33.0  NULL
  1  STRI   34.6  NULL
  2  STRI   27.7  NULL
  3  STRI   40.3  NULL
  4  STRI   22.7  NULL
END 
```

### Link friction.tbl in CAS file

To activate the friction data, add the following keywords to the `.cas` steering file, and deactivate any not-wall related FRICTION keywords:


`````{tab-set}
````{tab-item} Activation keywords
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ ACTIVATE these keywords
FRICTION DATA : YES / default is NO
FRICTION DATA FILE : 'friction.tbl'
MAXIMUM NUMBER OF FRICTION DOMAINS : 20 / consider to increase (default is 10)
```
````
````{tab-item} Deactivation keywords
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ DEACTIVATE these keywords
/ LAW OF BOTTOM FRICTION : 3 / 3-Strickler
/ FRICTION COEFFICIENT : 80 / not use with zonal friction
```
````
`````

Save the `.cas` steering file.

## Run Telemac with Friction IDs

To run Telemac with friction IDs, make sure the above-indicated keywords are activated in the `.cas` steering file. The required files now embrace:

* [qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) (mesh with `FRIC_ID`)
* [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/boundaries.cli) or hotstart conditions
* [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/r2dsteady-t15k.slf) results file to enable the hotstart 
* [steady2d-zonal-ID.cas](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/steady2d-zonal-ID.cas) steering file updated keywords
* [friction.tbl](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl) with friction IDs

With these files, activate and run Telemac as usual:

```
cd ~/telemac/v8p4/configs
source pysource.gfortranHPC.sh
cd ~/modeling/frictionID-tutorial/
telemac2d.py steady2d-zonal-ID.cas
```


# Advanced Friction Routines

Modifying the **FRICTION_USER** Fortran subroutines is not mandatory for working with friction zones but can be useful for implementing or adapting the behavior of roughness laws. To activate a FRICTION_USER subroutine, for example, to implement the variable power equation from {cite:t}`ferguson_flow_2007`:

* Copy the FICTION_USER subroutine template from  `HOMETEL/sources/telemac2d/friction_user.f` into a new folder of your simulation directory, for example:
```
/HOME/modeling/frictionID-tutorial/user_fortran/friction_user.f
```
* Modify and save edits of `friction_user.f`.
* Tell the steering (`.cas`) file to use the modified FRICTION_USER Fortran file by adding the keyword `FORTRAN FILE : 'user_fortran'`, which makes Telemac2d look up Fortran files in the `/user_fortran/` subfolder.






