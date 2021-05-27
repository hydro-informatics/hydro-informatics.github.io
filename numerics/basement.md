(chpt-basement)=
# BASEMENT

This chapter guides through the setup of a two-dimensional (2d) numerical simulation with the freely available software *BASEMENT* v3.1.1 developed at the ETH Zurich (Switzerland). Visit their [website](https://basement.ethz.ch/) to download the program and documentation. This tutorial features:

* Model setup
* Running a steady hydrodynamic 2d numerical simulation with BASEMENT v.3
* Post-processing of simulation results: Visualize, understand and analyze the model output.

```{admonition} Requirements
:class: attention
Completing this tutorial requires:

* An installation of {ref}`qgis-install`.
* An {term}`SMS 2dm` file resulting from the {ref}`qgis-prepro` tutorial.
* An installation of [BASEMENT v3.1.1](https://basement.ethz.ch/) or newer.
* Optional: an installation of [ParaView](https://www.paraview.org/).
```

```{admonition} Platform compatibility
:class: tip
All software applications featured in this tutorial can be run on *Linux* and *Windows* platforms. Note that *BASEMENT* is not available for *macOS*.
```

(simulate)=
## Steady 2d Simulation Setup

In addition to the {term}`SMS 2dm` file from the {ref}`qgis-prepro` tutorial, the numerical engine of *BASEMENT* needs a model setup file (**model.json**) and a simulation file (**simulation.json**), which both are created automatically by *BASEMENT*. The following sections describe how to make *BASEMENT* creating these two {ref}`json` files in a project directory such as `C:\Basement\steady2d-tutorial\` (*Windows*) or `~/Basement/steady2d-tutorial/` (*Linux*).

```{admonition} Special characters in folder names
:class: attention
The defined project folder directory must **not contain** any **dots** nor **special characters** nor **spaces**. Only use letters, numbers, *_* (underscore), or *-* (minus) in folder names.
```

Place the following two input files in the folder:

* The {term}`SMS 2dm` file with interpolated bottom elevations from the {ref}`qgis-prepro` tutorial (**prepro-tutorial_quality-mesh-interp.2dm**).
* A steady discharge inflow file (flat hydrograph) for the upstream boundary condition can be downloaded [here](https://github.com/hydro-informatics/materials-bm/raw/main/flows/steady-inflow.txt) (if necessary copy the file contents locally into a text editor and save the file as **steady-inflow.txt** in the project directory).

### Initiate the Model
This section guides through the model setup, which is saved in a file called `/steady2d-tutorial/`**model.json**. Begin with launching BASEMENT and selecting the above-created folder as **Scenario Directory**. {numref}`Fig. %s <bm-setup-start>` indicates the position of the directory selection button and the **save project** button to regularly save the setup.

```{figure} ../img/basement/setup-start.png
:alt: basement new project setup launch start
:name: bm-setup-start

BASEMENT's welcome screen after selecting a *Scenario Directory* and with the *Save Project* button highlighted. The directory references may look different on other platforms (e.g., start with **"C:/...**).
```

Next, **left-click** on **SETUP**, then **right-click** and select **Add item DOMAIN**. A new tab called **Define Scenario Parameters** opens, which are explained in the next sections. For the moment ignore the warning and error messages (red tags), but define a **simulation name**:

* **Right-click** on **SETUP** and select **Add item 'simulation_name'**. A new entry called *simulation_name* will appear in the *Define Scenario Parameters* tab.
* **Double-click** on **"RUNFILE"** (default value of behind **simulation_name**) and replace the name `RUNFILE` with `steady2d`.

Save the project and proceed with the next sections.

(bm-geometry)=
### Geometry and Regions

The **GEOMETRY** entry in the **Define Scenario Parameters** tab tells the model, which {term}`SMS 2dm` mesh file to use and enables the definition of region and liquid boundary properties. To this end, make the following settings:

* **Double-click** on the **mesh_file** entry and click on the folder symbol <br> <img src="../img/basement/select-meshfile.png">
* In the popup window select the {ref}`previously created prepro-tutorial_quality-mesh-interp.2dm <qgis-prepro>` and hit the **Enter** key.
* Define model regions:
  * **Right-click** on **GEOMETRY** > **Add item REGIONDEF**
  * Add **5** region items by **right-clicking** on the new **REGIONDEF** entry > **Add item** (repeat five times). The number of regions should correspond to the regions defined in the {ref}`qgis-prepro` tutorial ({numref}`Tab. %s <region-defs>`).
  * Define the five regions by a **right-click** on **index** > **Add item**. Every **index** item gets an integer number assigned corresponding to the **MATID** field in the region points shapefile (see the {ref}`regions` section in the {ref}`qgis-prepro` tutorial). The **name** of every region item corresponds to the **type** field of the MATID. {numref}`Tab. %s <region-defs-bm>` summarizes the required region definitions.

```{list-table} REGIONDEF items and their definitions to be defined in BASEMENT's model setup.
:header-rows: 1
:name: region-defs-bm

* - **REGIONDEF**
  - [0]
  - [1]
  - [2]
  - [3]
  - [4]
* - **index [0]**
  - 1
  - 2
  - 3
  - 4
  - 5
* - **name**
  - riverbed
  - block_ramp
  - gravel_bank
  - floodplain
  - sand_deposit
```

With the regions and the mesh file defined, the GEOMETRY section should resemble {numref}`Fig. %s <bm-regions>`.

```{figure} ../img/basement/setup-geometry.png
:alt: region mesh file definitions basement
:name: bm-regions

The GEOMETRY entry with REGIONDEFs and the reference to the height-interpolated mesh file (prepro-tutorial_quality-mesh-interp.2dm).
```

```{admonition} Save the project...
Regularly save the model setup by clicking on the disk button (top-right corner, see {numref}`Fig. %s <bm-setup-start>`).
```

The {ref}`liquid-boundary` from the pre-processing tutorial geographically define an inflow and an outflow line with **stringdef** attributes that are incorporated in the eight-interpolated mesh file (prepro-tutorial_quality-mesh-interp.2dm). To inform BASEMENT about types and properties of the liquid boundaries complete the GEOMETRY section.

* **Right-click** on **GEOMETRY** > **Add item STRINGDEF**.
* **Right-click** on the new **STRINGDEF** item and select **Add item** two times. Thus, two items should be available to define the upstream and downstream liquid boundaries.
* Define STRINGDEF item **[0]** with:
  * **name** = `Inflow`
  * **upstream_direction** = `right`
* Define STRINGDEF item **[1]** with:
  * **name** = `Outflow`
  * **upstream_direction** = `right`
  * If you used the provided [liquid boundaries shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/liquid-boundaries.zip) to create the mesh file the **upstream_direction** must be `left`.


{numref}`Figure %s <bm-geo-fin>` shows the definition of the STRINGDEF items with the liquid boundaries template shapefile (i.e., *upstream_direction* is `left`).

```{figure} ../img/basement/setup-geometry-final.png
:alt: region mesh file definitions basement
:name: bm-geo-fin

The GEOMETRY entry with STRINGDEFs using the liquid boundaries template shapefile (i.e., *upstream_direction* is `left`).
```

(bm-hydraulics)=
### Hydraulics

Hydraulic model characteristics that apply to the above-defined geometry setup are defined in the **HYDRAULICS** entry of BASEMENT's model setup. This tutorial uses the default type for INITIAL conditions, which is **"dry"**. Keep also the default PARAMETERS, which are **{term}`CFL`** = `0.9`, **fluid_density** = `1000.0`, **max_time_step** = `100.0`, and **minimum_water_depth** =` 0.01`.

Hydraulic values such as discharge or water depth must be assigned to the liquid boundaries defined above so that the numerical model knows how much water it must make running through the model. Therefore, add the following boundary definitions in the HYDRAULICS section.

* **Right-click** on **HYDRAULICS** and select **Add item BOUNDARY**.
* **Right-click** on the new **BOUNDARY** item and select **Add item STANDARD**.
* **Right-click two times** on the new **STANDARD** item and select **Add item**. Thus, there should be two items **[0]** and **[1]** to define the inflow and outflow conditions, respectively.
* Define item [0] with the following inflow conditions:
  * **Right-click** on **[0]** and select **Add item 'discharge_file'**.
  * Click on the folder symbol to select the above-downloaded [steady-inflow.txt](https://github.com/hydro-informatics/materials-bm/raw/main/flows/steady-inflow.txt) file.
  * For **name** tap `Inflow`.
  * **Right-click** on **[0]** and select **Add item 'slope'**.
  * For the new **slope** item define a value of `0.0044`.
  * For **string_def** select the above-defined `inflow` STRINGDEF.
  * For **type** select `uniform_in`
* Define item [1] with the following outflow conditions:
  * For **name** tap `Outflow`.
  * For **string_def** select the above-defined `outflow` STRINGDEF.
  * For **type** select `zero_gradient_out`

```{admonition} Liquid boundaries in practice
:class: note
In practice better use a {term}`Stage-discharge relation` for the downstream boundary condition, which in BASEMENT corresponds to **type** = `hqrelation_out`. The upstream inflow condition, however, is also often specified in practice only by discharge as a function of time, as shown in this tutorial. A critical factor of the discharge-only function of time is the **slope** field value, which corresponds to the energy slope and is often assumed to be equivalent to the channel slope. However, this assumption is only valid for steady discharges such as those in this tutorial, which almost never occur in reality. This is why, in practice, quasi-unsteady flow conditions are often used in the form of a time-dependent sequence of steady discharges, for example for modeling a flood hydrograph.
```

{numref}`Figure %s <bm-hy-standard>` shows the definition of the STANDARD BOUNDARY items for BASEMENT's HYDRAULIC model setup.

```{figure} ../img/basement/setup-hydraulics-standard.png
:alt: basement standard hydraulic boundary conditions
:name: bm-hy-standard

The HYDRAULIC entry with BOUNDARY > STANDARD definitions for the upstream (inflow) and downstream (outflow) liquid model boundaries.
```

Every surface has imperfections that cause turbulence when fluids such as water flow over it. The turbulence caused by surface imperfections results in decelerated flows near the surface. Since the water in rivers is almost always very close to the Earth's surface in the form of the riverbed relative to the imperfections of a riverbed, the influence of such friction-induced turbulence is great. In hydrodynamic models, the friction effect of the rough surface of riverbeds is accounted for by a friction coefficient, such as the Strickler $k_{st}$ coefficient or its inverse value called Manning's $n$. The exercise on {ref}`ex-1d-hydraulics` in the *Python* chapter explains both roughness coefficients in more detail. This tutorial uses only a global roughness coefficient in the form of a Strickler coefficient of $k_{st}$=30 (fictive units of m$^{1/3}$/s), which is accounts for the characteristics of a meandering gravel-cobble riverbed {cite:p}`strickler_beitrage_1923`. To this end, **right-click** on the **HYDRAULICS** entry and select **Add item FRICTION**. Define the new  **FRICTION** item with:

* **default_friction** = 30.0
* **type** = `strickler`

Next, assign specific Strickler values for the five regions defined in {numref}`Tab. %s <region-defs-bm>`:

* **Right-click** on **FRICTION** and **Add item regions**.
* **Right-click** on the new **regions** item and select **Add item** (**five times** for the five regions)
* Assign the **friction** and **region_def** values listed in {numref}`Tab. %s <region-kst>` to the **five regions items**.
* Set the **type** of the five regions to **"strickler"**.

```{list-table} Strickler values for HYDRAULIC FRICTION regions.
:header-rows: 1
:name: region-kst

* - Region
  - Riverbed
  - Block ramps
  - Gravel banks
  - Floodplains
  - Sand
* - **friction**
  - 34
  - 18
  - 24
  - 14
  - 39
* - **region_def**
  - riverbed
  - block_ramp
  - gravel_bank
  - floodplain
  - sand_deposit
```


{numref}`Figure %s <bm-hy-friction>` shows the definition of the HYDRAULIC FRICTION items in BASEMENT's model setup.

```{figure} ../img/basement/setup-hydraulics-friction.png
:alt: basement friction hydraulic boundary conditions strickler
:name: bm-hy-friction

The HYDRAULIC entry with FRICTION definitions for the model and its regions.
```

(bm-physical-props)=
### Physical Properties

The PHYSICAL_PROPERTIES are a mandatory element for BASEPLANE_2D and this tutorial uses the default physical properties (i.e., *gravity* is `9.81`).

(bm-export-setup)=
### Write Setup File

Make sure that all error messages are resolved and that the model setup resembles {numref}`Fig. %s <bm-ready2export-setup>`. Before exporting the project, save the simulation setup (click on the disk symbol in the top-right corner in {numref}`Fig. %s <bm-ready2export-setup>`). Double-check that BASEMENT correctly wrote the model files **model.json**, **simulation.json**, and **results.json** in the project directory (e.g., `/Basement/steady2d-tutorial/`). Export the model setup by clicking on the **Write** button (bottom-right corner in {numref}`Fig. %s <bm-ready2export-setup>`).

```{figure} ../img/basement/setup-ready2export.png
:alt: basement export model setup h5
:name: ready2export-setup

The final model setup to export (write) to a setup (`*.h5`) file.
```

The **Console** tab becomes automatically actives and informs about the export progress. If the **Error Output** canvas is not empty, check the error messages and troubleshoot the causes.


### Setup the Simulation File

After the successful export of the model setup, the **Simulation** ribbon (on the left in {numref}`Fig. %s <bm-ready2export-setup>`) becomes available for setting up the **simulation.json** file in the project folder. Click on the **Simulation** ribbon to setup the *simulation.json* file:

* **Right-click** on the **SIMULATION** entry in the **Define Simulation Run** tab and select **Add item 'OUTPUT'**.
* **Right-click** on the new **OUTPUT** entry to define four output types:
    * **[0]** = `water_depth`
    * **[1]** = `water_surface`
    * **[2]** = `bottom_elevation`
    * **[3]** = `flow_velocity`
    * Do not change the order of the output variables to enable using BASEMENT's *Python* scripts for post-processing.
* **Right-click** on the **SIMULATION** entry and select **Add item 'TIME'**.
* Define the TIME item with:
    * **end** = `5000.0`
    * **out** = `200.0`
    * **start** = `0.0`

The values defined in the TIME section refer to the same time units as defined in the above downloaded and linked *steady-inflow.txt* file. {numref}`Figure %s <bm-sim-setup>` shows BASEMENT with the definitions in the SIMULATION ribbon.


```{figure} ../img/basement/setup-simulation.png
:alt: basement simulation setup
:name: bm-sim-setup

The setup of the Simulation ribbon. To export results with BASEMENT's Python scripts, the OUTPUT parameters must be defined in exactly that order.
```

## Run BASEMENT 2d Simulation

After the successful simulation setup, select an appropriate `Number of CPU cores` (bottom-right in the above figure). If a high-quality graphics card with a powerful GPU is available, the GPU (high-performance hardware) has a much faster performance. Otherwise (no powerful GPU available), do not select GPU because it may significantly slow down the simulation speed.
For faster simulations, select `Single` precision (bottom-right in the above figure), but in this example, `Double` precision will work sufficiently fast as well. Click on the `Run` button to start the simulation and wait for approximately 2-10 minutes. *BASEMENT* will prompt the simulation progress, while the `Error Output` canvas should remain white (see {numref}`Fig. %s <bm-sim-end>`)). If any error occurs, go back to the above sections (or even to the mesh generation) and fix error message issues.


```{figure} ../img/bm-sim-end.png
:alt: basement simulation end
:name: bm-sim-end

*BASEMENT* after successful simulation.
```

### Export results
Once the simulation successfully finished, go to *BASEMENT*'s `Results` tab and make sure that the `xdmf` output format is defined. Then click on the `Export` button (see {numref}`Fig. %s <bm-res-exp>`). *BASEMENT* will inform about the export success.


```{figure} ../img/bm-res-exp.png
:alt: basement results export
:name: bm-res-exp

Export results after successful simulation.
```

*BASEMENT*’s developers at the ETH Zurich provide a suite of [Python scripts](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/) for post-processing the simulation results. Here, we need the Python script [BMv3NodestringResults.py](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/BMv3NodestringResults.py) ([click to download](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/BMv3NodestringResults.py)).

To run the Python script, a Python3 installation with the `numpy` and `h5py` packages is required. To learn more about the installation and usage of Python, have a look at the instructions to [install Python](../python-basics/pyinstall).
Note that working with the provided Python file requires that the output variables must be exactly defined as shown in {numref}`Fig. %s <bm-sim-se>` (**BASEMENT*’s `SIMULATION` tab).


## Post-processing with ParaView

*ParaView* is a freely available visualization software, which enables plotting *BASEMENT* v.3.x results in the shape of `xdmf` (*eXtensible Data Model and Format*) files. Download and install the latest version of *ParaView* from their [website](https://www.paraview.org/download/), if not yet done.

### Load BASEMENT Results
Open *ParaView* and click on the folder icon (top left of the window) to open the simulation results file (`results.xdmf`). *ParaView* might ask to choose an appropriate XMDF read plugin. Select `XDMF Reader` here and click `OK`:

To explore the model results:
- Select variables (e.g., `flow_velocity`, `water_depth`, or `water_surface`) in *ParaView*'s `Cell Arrays` canvas (green-highlighted circle in {numref}`Fig. %s <pv-vis>`).
- Click the `Apply` button (red-highlighted circle in the Properties tab in {numref}`Fig. %s <pv-vis>`). All variables are now loaded and can be plotted.
- To plot a variable, select one (e.g., `flow_velocity`) in the toolbar (light-blue-highlighted circle in the upper part of {numref}`Fig. %s <pv-vis>`). Then click the play button in the toolbar (dark-blue-highlighted circle around the green arrow in the upper part of  {numref}`Fig. %s <pv-vis>` to cycle through the time steps.

```{figure} ../img/pv-vis.png
:alt: basement results paraview
:name: pv-vis

ParaView after successful import of the model results (results.xdmf) - see above descriptions.
```

All available time steps are listed in the Blocks tab (bottom-left in Figure 1). Anything should be visible at the beginning because the initial conditions were defined as `dry` (see the setup of [inital conditions](#init)). The above {numref}`Fig. %s <pv-vis>`) shows the last time step (`Timestep[25]`), with water flowing at a peak velocity of 3.7 m/s. The 25 available time steps result from the definition made in *BASEMENT*'s `SIMULATION` tab with a total duration of 5000.0 and an output step of 200.0. Note that the time units have no dimension here because they correspond to computational time steps.

(exp-vis)=
### Export Visualizations

The animations can be saved as movie (e.g., `avi`) or image (e.g., `jpg`, `png`, `tiff`) files via `File` > `Save Animation...`.
The current state (variable, `Timestep[i])` can be saved as `pvsm` file via `File` > `Save State File`. The state file can also be saved as Python script for external execution and implementation in [Python programs](../python-basics/pypckg.html#stand-alone).

(exp-data)=
### Export Data
For geospatial calculations (e.g., calculate [habitat suitability indices for target fish species](https://riverarchitect.github.io/RA_wiki/SHArC) based on flow velocity and water depth), the simulation results must be converted to geospatial data formats. The first conversion step is to extract relevant point data in *ParaView*:

1. With the `results.xdmf` file opened in *ParaView*, right-click on `results.xdmf` in the `Pipeline Browser`, then `Add Filter` > `Alphabetical` > `Cell Centers`
1. With the `CellCenters1` filter enabled in the `Pipeline Browser` (blue-highlighted circle in the [figure below](#pv-exp-steps), set the `Time` in the menu bar to the end time step (here: `5000`, i.e., step no. `25`, see the red-highlighted circle in the [figure below](#pv-exp-steps))
1. In the `Properties` tab (green-highlighted circle in the [figure below](#pv-exp-steps), check the `Vertex Cells` box, and click the `Apply` button.
1. Press  `CTRL` + `S` on the keyboard > a `Save File` dialogue window opens:
    * Navigate to the folder where you want to save the data
    * Enter a `File name` (e.g., *bm-steady-vanilla*)
    * In the `Files of type` drop-down field, select `Comma or Tab Delimited Files(*.csv *.tsv *.txt)`
    * Click `OK`
1. The `Configure Writer (CSVWriter)` window opens. Make sure that `Point Data` is selected as `Field Association`. Optionally, check the `Choose Arrays To Write` box and select relevant fields only. Press the `OK` button.

The point data export is now complete. The next step is to import the data (here: *bm-steady-vanilla.csv*) in *QGIS* ([next section](#qgis-import)).


```{figure} ../img/pv-exp-steps.png
:alt: paraview basement export data
:name: pv-exp-steps

The CellCenters (dark-blue circle) filter in ParaView, with the maximum Time step setting (red circle) and the Properties definitions (green circle)
```

## Post-processing with QGIS

```{tip}
Ensure that the [*Crayfish* plugin](../get-started/geo#plugins) is correctly installed and available in the *Toolbox*.
```

<a name="imp-steps"></a>
There are two (to three) options to import the results in *QGIS*:

1. [Use *ParaView* Outputs](#pv-exp-steps)
1. [Modify `results.xdmf` and directly import results in *QGIS*](#qigs-imp-steps)
1. [Use an import tool (currently only available on demand)](#schmalzl)

### Use *ParaView* export (here: *bm-steady-vanilla.csv*)

After data export from *ParaView*:<a name="pv-exp-steps"></a>
- In *QGIS*, click on the `Layer` menu > `Add Layer` > `Add Delimited Text Layer...`.

```{figure} ../img/qgis/add-txt-lyr.png
:alt: basement qgis add layer
:name: qgis-add-lyr-bm

Open the Add Delimited Text Layer import wizard.
```

- The `Data Source Manager | Delimited Text` window opens ([see figure below](#qgis-import-csv)
- In the `File name` field select *bm-steady-vanilla.csv*
- Enter a `Layer name` (e.g., *bm-steady-vanilla-csv*)
- In the `File Format` canvas, check the `CSV (comma separated values)` box
- In the `Record and Field Options` canvas, activate the `First record has field names` checkbox
- In the `Geometry Definition` canvas, define the `Point Coordinates` as `X field` = `Points:0`, `Y field` = `Points:1` and `Z field` = `Points:2` (verify the correctness: `X`-data should be in the order of 4.2 to 4.4·10<sup>6</sup>, `Y`-data should be in the order of 5.5·10<sup>6</sup>, and `Z`-data should be in the order of 100.0 to 200.0)
- Set the `Geometry CRS` to the `Project CRS` (`ESRI:31493 - Germany_Zone_3`).
- Click the `Add` and the `Close` buttons on the bottom of the window. The points should now be plotted in the main *QGIS* window.

```{figure} ../img/qgis-import-csv.png
:alt: qgis import basement results 2dm
:name: qgis-import-csv

The Data Source Manager | Delimited Text window with required settings highlighted with the green marker.
```

(qgis-imp-steps)=
### Use the `results.xdmf` file directly (**recommended for geospatial data conversion**)

Modify `results.xdmf` and directly import model result in *QGIS*:
- Open `results.xdmf` in a text editor (e.g., [*Notepad++*](../get-started/others.html#npp)
- Use the find-and-replace tool (`CTRL` + `H` keys in *Notpad++*) to remove file paths before `results_aux.h5` in the document (otherwise *QGIS* will crash later on - [read more in *BASEMENT*'s User Forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?id=5261)).
- For example: `Find what` = `C:/temp/results_aux.h5` (pay attention to use `/` rather than `\`) and `Replace with` = `results_aux.h5` (see [below figure](#npp-xdmf-replace)). After having removed all path occurrences in the document, save and close `results.xdmf`.

```{figure} ../img/npp-xdmf-replace.png
:alt: find replace error import results qgis basement
:name: npp-xdmf-replace

Find the string results_aux.h5 in results.xdmf and remove the file directories.
```
- If not yet done, load the mesh file (here: [`finalmesh.2dm`](../numerics/pre-qgis.html#2dm) by clicking on *QGIS*' `Layer` menu > `Data Source Manager` > `Mesh` tab and select `finalmesh.2dm`.
- In *QGIS*' `Layers` window, double-click on the `finalmesh` layer to open the `Layer Properties` window.
- In the `Layer Properties` window, go to `Source` > click on `Assign Extra Data Set to Mesh` and choose  `results.xdmf`

```{figure} ../img/qgis-assign-meshdata.png
:alt: basement assign qgis metadata
:name: qgis-assign-meshdata

Assign mesh data to the computational mesh.
```

- After import, double-click on the new `results` layer to open the `Symbology` (`Layer Properties`) and select a variable to represent from the `Groups` canvas. Make sure to enable the contour plot (right side in the [below figure](#qgis-meshdata-u) symbol, select the timestep to plot (for steady-state simulation, select the last timestep), optionally go to the `Contours` ribbon to change the color pattern (upper-most green circle in the [below figure](#qgis-meshdata-u), and click `Apply`.

```{figure} ../img/qgis-meshdata-u.png
:alt: basement qgis results velocity meshdata
:name: qgis-meshdata-u

Illustrate the flow velocity with QGIS' Layer Properties > Symbology controls. The green circles highlight settings for the last timestep of a steady-state simulation.
```

```{figure} ../img/qgis-meshdata-u-plotted.png
:alt: plotted qgis basement results
:name: qgis-plot-metadata

After application of the above Symbology settings: The flow velocity is illustrated in red-shades.
```

Thanks to Matthias Bürgler who helped with instructions in the [*BASEMENT* user forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?pid=6095#p6095).

### Klaus Schmalzl's `Basement_post_W.exe` <a name="schmalzl"></a>
Another option in the future will be [Klaus Schmalzl's `Basement_post_W.exe`](http://people.ee.ethz.ch/~basement/baseweb/users-meetings/30-01-2020/6_Schmalzl.pdf), which is currently only available on demand.

### Convert results to geospatial formats (SHP and TIF)<a name="qgis-exp-steps"></a>
To analyze the imported results, they need to be converted to geo-spatial data format such as [ESRI Shapefiles](https://en.wikipedia.org/wiki/Shapefile) or [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF) rasters. There are two options available depending on how data were imported:

1. Conversion with the *Crayfish* plugin after [direct import of `results.xdmf`](#qgis-imp-steps) (recommended)
1. Conversion of [*ParaView* exports](#pv-conv) (not recommended)

#### Conversion with the Crayfish plugin (recommended)<a name="crayfish-conv"></a>

Open the *Crayfish* plugin's `Rasterize` tool from *QGIS*' `Processing` menu > `Toolbox` > `Crayfish` > `Rasterize` (see figure below).


```{figure} ../img/qgis-crayfish-installed.png
:alt: rasterize crayfish qgis
:name: qgis-crayfish-installed

Open the Rasterize tool of the Crayfish plugin.
```

- In the `Rasterize` window make the following settings (see also [figure below](#qgis-crayfish-exp):
    * `Input mesh layer` =  `finalmesh`
    * `Minimum extent to render (xmin, xmax, ymin, ymax)` =  click on the `...` button and select the `Layer` option (choose `finalmesh`)
    * `Map units` = `0.1` (can also be larger - the larger this number, the coarser the output *tif*)
    * `Dataset group` =  `flow_velocity` (or whatever variable should be in the final *tif*  - note that rasters can/should have only one value per pixel)
    * `Timestep` = `208 days, 8:00:00` (last timestep in the case of steady-state simulations)
    * `Output layer` = `C:\ ... \u.tif` (or whatever variable / raster specifier applies)
- Click `Run`

```{figure} ../img/qgis-crayfish-exp.png
:alt: setup rasterize crayfish plugin
:name: qgis-crayfish-exp

Settings to be made in Crayfish's Rasterize tool.
```

With a `Singleband pseudocolor` > `Spectral` `Symbology`-selection in the `Layer Properties`, the *QGIS* window should now look like this:


```{figure} ../img/qgis-crayfish-final.png
:alt: bm-qce
:name: qgis-crayfish-final

A Singleband pseudocolor (Layer Properties > Symbology) selection will represent the velocity distribution in the final velocity GeoTIFF.
```


#### Conversion of ParaView exports (not recommended)<a name="pv-conv"></a>

- In *QGIS*, right-click the above imported csv-points layer (here: `bm-steaedy-vanilla-csv`) > `Export` > `Save Features As...`
- The `Save Vector Layer as...` window opens ([see figure below](#qgis-exp-sim-pts), where the following settings need to be defined:
    * `Format` =  `ESRI Shapefile`
    * `File name` =  for example `C:\...\bm-vanilla-pts.shp`
    * `CRS` = `ESRI:31493 - Germany_Zone_3`
    * In the `Encoding`canvas, deactivate the `ns_hyd_discharge`, `Points:0`, `Points:1`, and `Points:2` fields
    * In the `Geometry` canvas, set the `Geometry type` to `Point` and active `Include z-dimension`
    * Check the `Extent (current: layer)` box
- Click `OK`


```{figure} ../img/qgis-exp-sim-pts.png
:alt: basement qgis export points
:name: qgis-exp-sim-pts

The Save Vector Layer As... window with required settings highlighted (green marker).
```

Next, the point shapefile needs to be converted to a [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF) raster format to enable further data analyses. Therefore:
- In *QGIS* `Raster` menu, click on `Conversion` and select `Rasterize (Vector to Raster)`
- In the `Rasterize (Vector to Raster)` window define:
    * `Input layer` = `bm-vanilla-pts`
    * For `Field to use for a burn-in value`, select one target value, for example: `water_dept` (note: rasters can ave only one value per pixel)
    * Do not assign any value in the `A fixed value to burn` field
    *  `Output raster size units` = `Pixels`
    * `Width/Horizontal resolution` = `5.0`
    * `Height/Vertical resolution` = `5.0`
    * `Output extent (xmin, xmax, ymin, ymax)`: Click on the `...` button and select `Use Layer extent` > `Use extent from` `bm-vanilla-pts`
    * Below the `Advanced parameters` canvas, define a raster output directory and name (e.g., `vanilla-depth.tif`)
- Click `Run`.


```{figure} ../img/qgis-make-tiff.png
:alt: basement qgis export tiff raster
:name: qgis-make-tiff

The Rasterize (Vector to Raster) window with required settings highlighted (green marker).
```

```{tip}
Facilitate the conversion of geospatial data with efficient *Python* algorithms (see the [geospatial *Python*](../geopy/geo-python) chapter). Many *Python* conversion routines are also efficiently accessible and tailored for river analysis in the [*flusstools*](https://flusstools.readthedocs.io/) package.
```

## Result interpretation
In *ParaView* (renders faster) or *QGIS*, look at all variables (`flow_velocity`, `water_depth`, and `water_surface`), explore their evolution over time, different coloring and answer the following questions:

- Are the results are in a physically reasonable and meaningful range?
- When did the simulation become stable?<br>*To save time, the simulation duration can be shortened (*BASEMENT*'s `SIMULATION` tab), down to the time step when stability was reached.*
- Are there particularities such as rapids that correspond (qualitatively) to field observations (are rapids on confinements and/or terrain drops)?
- Zoom into the [final *tif* raster](#qgis-crayfish-final) and have a look at the triangulation artifacts. The artifacts are not realistic. How can the problem be addressed?

After post-processing, the model still needs to be [calibrated and validated](../numerics/calibration) before it can be used for scientific or engineering purposes in river ecosystem analyses.
