(basement2d)=
# Run and Check a Steady 2d Simulation

In addition to the {term}`SMS 2dm` file from the {ref}`qgis-prepro-bm` tutorial, the numerical engine of BASEMENT needs a model setup file (**model.json**) and a simulation file (**simulation.json**), which both are created automatically by BASEMENT.

The following sections describe how to make BASEMENT creating the required {ref}`json` files in a project directory such as `C:\Basement\steady2d-tutorial\` (*Windows*) or `~/Basement/steady2d-tutorial/` (*Linux*). Therefore, the **first step is to create a project directory (folder)**.

```{admonition} Special characters in directory/folder names
:class: attention
The defined project folder directory must **not contain** any **dots**, nor **special characters**, nor **spaces**. Only use letters, numbers, *_* (underscore), or *-* (minus) in folder names.
```

**Place** the following **input files in the project folder**:

* The {term}`SMS 2dm` file with interpolated bottom elevations from the {ref}`qgis-prepro-bm` tutorial (**prepro-tutorial_quality-mesh-interp.2dm**).
* A steady discharge inflow file (flat hydrograph) for the upstream boundary condition can be downloaded [here](https://github.com/hydro-informatics/materials-bm/raw/main/flows/steady-inflow.txt) (if necessary copy the file contents locally into a text editor and save the file as **steady-inflow.txt** in the project directory).

## Initiate the Model
This section guides through the model setup, which is saved in a file called `/steady2d-tutorial/`**model.json**. **Start BASEMENT** and **select the folder created above** as the **Scenario Directory**. {numref}`Fig. %s <bm-setup-start>` indicates the position of the directory selection button in addition to the **Save Project** button to regularly save the setup.

```{figure} ../img/basement/setup-start.png
:alt: basement new project setup launch start
:name: bm-setup-start

BASEMENT's welcome screen after selecting a *Scenario Directory* and with the *Save Project* button highlighted. The directory references may look different on other platforms (e.g., start with **"C:/...**).
```

Next, **left-click** on **SETUP**, then **right-click** and select **Add item DOMAIN**. A new tab called **Define Scenario Parameters** opens. For the moment ignore the warning and error messages (red tags) and define a **simulation_name**:

* **Right-click** on **SETUP** and select **Add item 'simulation_name'**. A new entry called *simulation_name* will appear in the *Define Scenario Parameters* tab.
* **Double-click** on **"RUNFILE"** (default value behind **simulation_name**) and **replace** `RUNFILE` with `steady2d`.

Save the project and proceed with the next sections.

(bm-geometry)=
## Geometry and Regions

The **GEOMETRY** group in the **Define Scenario Parameters** tab tells the model, which {term}`SMS 2dm` mesh file to use and enables the definition of region and liquid boundary properties. To this end, make the following settings:

* **Double-click** on the **mesh_file** entry and click on the folder symbol <br> <img src="../img/basement/select-meshfile.png">
* In the popup window select the {ref}`previously created prepro-tutorial_quality-mesh-interp.2dm <qgis-prepro-bm>` and hit **Enter**.


The mesh contains regions, which need to be defined in the model setup:

* **Right-click** on **GEOMETRY** > **Add item REGIONDEF**
* **Add 5 region items** by **right-clicking** on the new **REGIONDEF** entry > **Add item**. The number of regions should correspond to the regions defined in the {ref}`pre-processing tutorial <region-defs>` (see also {numref}`Tab. %s <region-defs-bm>`).
* Define the five regions by a **right-click** on **index** > **Add item**.
  * Every **index** item gets an integer number assigned corresponding to the **MATID** field in the region points shapefile (see the {ref}`regions` section in the {ref}`qgis-prepro-bm` tutorial).
  * The **name** of every region item corresponds to the **type** field of the MATID.

{numref}`Table %s <region-defs-bm>` summarizes the required region definitions. With the regions and the mesh file defined, the GEOMETRY group should resemble {numref}`Fig. %s <bm-regions>`.

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


```{figure} ../img/basement/setup-geometry.png
:alt: region mesh file definitions basement
:name: bm-regions

The GEOMETRY group with REGIONDEFs and the reference to the height-interpolated mesh file (prepro-tutorial_quality-mesh-interp.2dm).
```

```{admonition} Save the project...
Regularly save the model setup by clicking on the disk button (top-right corner, see {numref}`Fig. %s <bm-setup-start>`).
```

The {ref}`liquid-boundary` from the pre-processing tutorial geographically define **inflow and outflow** lines with **stringdef** attributes that are incorporated in the height-interpolated mesh file (*prepro-tutorial_quality-mesh-interp.2dm*). To inform BASEMENT about the types and the properties of the liquid boundaries, complete the GEOMETRY section:

* **Right-click** on **GEOMETRY** > **Add item STRINGDEF**.
* **Right-click** on the new **STRINGDEF** item and select **Add item** two times. Thus, two items should be available to define the upstream and downstream liquid boundaries.
* Define STRINGDEF item **[0]** with:
  * **name** = `Inflow`
  * **upstream_direction** = `right`
* Define STRINGDEF item **[1]** with:
  * **name** = `Outflow`
  * **upstream_direction** = `right`

If you used the provided [liquid boundaries shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/liquid-boundaries.zip) to create the mesh file, the **upstream_direction** must be `right`. {numref}`Figure %s <bm-geo-fin>` shows the definition of the STRINGDEF items using the provided liquid boundaries shapefile.

```{figure} ../img/basement/setup-geometry-final.png
:alt: region mesh file definitions basement
:name: bm-geo-fin

The GEOMETRY group with STRINGDEFs using the provided liquid boundaries shapefile in the computational mesh.
```

(bm-hydraulics)=
## Hydraulics

Hydraulic model characteristics that apply to the above-defined geometry setup are defined in the **HYDRAULICS** group of BASEMENT's model setup. This tutorial uses the **default** for **INITIAL** conditions, which is **"dry"**. Also **keep the default PARAMETERS** for **{term}`CFL`** = `0.9`, **fluid_density** = `1000.0`, **max_time_step** = `100.0`, and **minimum_water_depth** =` 0.01`.

Hydraulic values such as discharge or water depth must be assigned to the liquid boundaries defined above so that the numerical model knows how much water it must make running through the model. Therefore, **add** the following **boundary** definitions in the HYDRAULICS group:

* **Right-click** on **HYDRAULICS** and select **Add item BOUNDARY**.
* **Right-click** on the new **BOUNDARY** item and select **Add item STANDARD**.
* **Right-click two times** on the new **STANDARD** item and select **Add item**. Thus, there should be two items **[0]** and **[1]** to define the inflow and outflow conditions, respectively.
* **Define item [0]** with the following **inflow** conditions:
  * **Right-click** on **[0]** and select **Add item 'discharge_file'**.
  * Click on the folder symbol to select the above-downloaded [steady-inflow.txt](https://github.com/hydro-informatics/materials-bm/raw/main/flows/steady-inflow.txt) file.
  * For **name** tap `Inflow`.
  * **Right-click** on **[0]** and select **Add item 'slope'**.
  * For the new **slope** item, define a value of `0.0044`.
  * For **string_def** select the above-defined `inflow` STRINGDEF.
  * For **type** select `uniform_in`
* **Define item [1]** with the following **outflow** conditions:
  * For **name** tap `Outflow`.
  * **Right-click** on **[1]** and select **Add item 'slope'**.
  * For the new **slope** item, define a value of `0.0044`.
  * For **string_def** select the above-defined `outflow` STRINGDEF.
  * For **type** select `uniform_out`

```{admonition} Liquid boundaries in practice
:class: note
In practice, better use a {term}`Stage-discharge relation` for the downstream boundary condition, which in BASEMENT corresponds to **type** = `hqrelation_out`. The upstream inflow condition, however, is also often specified in practice only by discharge as a function of time, as shown in this tutorial. A critical factor of the discharge-only function of time is the **slope** field value, which corresponds to the energy slope and is often assumed to be equivalent to the channel slope. However, this assumption is **only valid for steady flows**, which almost never occur in reality. This is why, in practice, quasi-unsteady flow conditions are often used in the form of a time-dependent sequence of steady discharges, for example, to model a flood hydrograph.
```

{numref}`Figure %s <bm-hy-standard>` shows the definitions of STANDARD BOUNDARY items in BASEMENT's HYDRAULIC model setup group.

```{figure} ../img/basement/setup-hydraulics-standard.png
:alt: basement standard hydraulic boundary conditions
:name: bm-hy-standard

The HYDRAULIC entry with BOUNDARY > STANDARD definitions for the upstream (inflow) and downstream (outflow) liquid model boundaries.
```

Every surface has imperfections that cause turbulence when fluids such as water flow over it. The turbulences caused by surface imperfections result in decelerated flows near the surface. Since the water in rivers is almost always very close to the Earth's surface in the form of the riverbed relative to the imperfections of a riverbed, the influence of friction-induced turbulence is considerable. In hydrodynamic models, the friction-induced turbulence of the rough surface of riverbeds is accounted for by a **friction coefficient**, such as the **Strickler $k_{st}$** coefficient **or** its **inverse** value called **Manning's $n$**. The exercise on {ref}`ex-1d-hydraulics` in the *Python* chapter explains both roughness coefficients in more detail. This tutorial uses a global Strickler coefficient of $k_{st}$=30 (fictive units of m$^{1/3}$/s), which accounts for the characteristics of a meandering gravel-cobble riverbed {cite:p}`strickler_beitrage_1923`. To this end, **right-click** on the **HYDRAULICS** group and select **Add item FRICTION**. Define the new  **FRICTION** item with:

* **default_friction** = 30.0
* **type** = `strickler`

Next, assign region-specific Strickler values for the five regions defined in {numref}`Tab. %s <region-defs-bm>`:

* **Right-click** on **FRICTION** > **Add item regions**.
* **Right-click** on the new **regions** item and select **Add item** (**five times** for the five regions).
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


{numref}`Figure %s <bm-hy-friction>` shows the definition of the hydraulic FRICTION items in BASEMENT's model setup.

```{figure} ../img/basement/setup-hydraulics-friction.png
:alt: basement friction hydraulic boundary conditions strickler
:name: bm-hy-friction

The HYDRAULICS group with FRICTION definitions for the model and its regions.
```

(bm-physical-props)=
## Physical Properties

The definition of the **PHYSICAL_PROPERTIES** group is mandatory for BASEPLANE_2D. This tutorial uses the **default** physical properties (i.e., *gravity* is `9.81`).

(bm-export-setup)=
## Write Setup File

Make sure that all error messages are resolved and that the model setup resembles {numref}`Fig. %s <ready2export-setup>`. Before exporting the project, save the simulation setup (click on the disk symbol in the top-right corner in {numref}`Fig. %s <ready2export-setup>`). Double-check that BASEMENT correctly wrote the files **model.json**, **simulation.json**, and **results.json** in the project directory (e.g., `/Basement/steady2d-tutorial/`). Export the model setup by clicking on the **Write** button (bottom-right corner in {numref}`Fig. %s <ready2export-setup>`).

```{figure} ../img/basement/setup-ready2export.png
:alt: basement export model setup h5
:name: ready2export-setup

The final model setup to export (write) to a setup (`*.h5` {term}`HDF`) file.
```

The **Console** tab automatically activates and informs about the export progress. If the **Error Output** canvas is not empty, check the error messages and troubleshoot the causes.

(bm-sim-file)=
## Setup Simulation File

After the successful export of the model setup, the **Simulation** ribbon (on the left in {numref}`Fig. %s <ready2export-setup>`) becomes available for setting up the **simulation.json** file in the project folder. Click on the **Simulation** ribbon to setup the *simulation.json* file:

* **Right-click** on the **SIMULATION** group in the **Define Simulation Run** tab and select **Add item 'OUTPUT'**.
* **Right-click** on the new **OUTPUT** item to define four output types:
    * **[0]** = `water_depth`
    * **[1]** = `water_surface`
    * **[2]** = `bottom_elevation`
    * **[3]** = `flow_velocity`
    * **[4]** = `ns_hyd_discharge`
* **Right-click** on the **SIMULATION** group and select **Add item 'TIME'**.
* **Define** the **TIME** item with:
    * **end** = `15000.0`
    * **out** = `1000.0`
    * **start** = `0.0`

```{admonition} Discharge controls
The output parameter `ns_hyd_discharge` (*ns* denotes *nodestring*) enables the verification of discharges at inflow and outflow boundaries (STRINGDEFs), which is a **necessary requirement in practice**. Learn more about mass balance verification in the {ref}`bm-python` section.
```

The values defined in the TIME section refer to the same time units as defined in the above-downloaded and linked *steady-inflow.txt* file. {numref}`Figure %s <bm-sim-setup>` shows BASEMENT with the definitions in the Simulation ribbon.

```{figure} ../img/basement/setup-simulation.png
:alt: basement simulation setup
:name: bm-sim-setup

The setup of the Simulation ribbon with the definition of five output parameters and the simulation time.
```

(bm-run)=
## Run Simulation (Steady 2d)

The simulation can be run with different options that mainly affect the computation speed (bottom of {numref}`Fig. %s <bm-sim-setup>`).

* The **Standard Hardware** frame enables to switch between single and multi-threaded CPU usage. The default option is multi-threaded, which is strongly recommended with contemporary computers.
* The **High-performance Hardware** frame enables to use a graphical processing unit (GPU), which can be significantly faster than CPU, but only when a powerful graphics processor is available. A standard-slow GPU will not have an advantage and may even slow down the computation. If you are not sure about the GPU of your computer, keep the default options (all void).
* The **Options** frame enables to choose:
  * The **Number of CPU cores**, which enables to use multiple CPUs of a computer. Contemporary computers mostly have at least 8 cores that can all be used when you are working on a server or computer that has no other purpose than running numerical models. Otherwise, keep the system functional while the simulation is running by using half the number of available cores.
  * Numeric precision; for faster simulations, select **Single precision**. For this tutorial, *Double* precision will work sufficiently fast as well, but in practice and for larger models use *Single* precision.

```{admonition} How many CPUs does my computer have?
**Windows** users can fire up **Task Manager** (*Start* > tap `task manager`) and look up the number of available cores in the Task Manager's **Performance** tab.

**Linux** users get an overview of system resources by installing and using {ref}`htop <install-htop>`.
```

To start the simulation click on the **Run** button on the bottom-right of the BASEMENT window. Depending on the hardware and performance settings (e.g., number of CPUs), the simulation of the tutorial model takes approximately 2-10 minutes. BASEMENT informs about the simulation progress in the **Console Output** frame, where the **Error Output** frame should remain empty (see {numref}`Fig. %s <bm-sim-end>`). If any error occurs, go back to the above sections (or even to the {ref}`mesh generation tutorial <qgis-tutorial>`) and fix errors.

```{figure} ../img/basement/simulation-end.png
:alt: basement simulation end
:name: bm-sim-end

BASEMENT after successful simulation.
```

### Export Simulation Results

Once the simulation successfully finished, go to BASEMENT's **Results** ribbon. Find the **RESULTS** group in the **Export Simulation Results** tab and:

* **Right-click** on the **RESULTS** group and select **Add item 'EXPORT'**.
* **Right-click** on the new **EXPORT** item and select **Add item**.
* Select {term}`xdmf` in the **format** field of the new item **[0]**.

**Save the project** (disk symbol in the top-right corner) and find the **Export** indicated in {numref}`Fig. %s <bm-res-exp>`). The export of the simulation outputs to **results.{term}`xdmf`** will be confirmed in the **Console Output** frame.

```{figure} ../img/basement/setup-results-export.png
:alt: basement results export
:name: bm-res-exp

Setup of the Results ribbon after a successful simulation.
```


# Post-processing with QGIS

Start QGIS and create a new project or re-use the project from the {ref}`qgis-prepro-bm` tutorial. Save the new project with (a different) meaningful filename in the BASEMENT modeling folder (e.g., `/Basement/steady2d/`**postpro-tutorial.qgz**). Setup the project similarly as in the pre-processing:

* Use the coordinate reference system **Germany_Zone_4**  ({ref}`start-qgis` section).
* Add a {ref}`satellite imagery basemap <basemap>` (XYZ tile) to facilitate the interpretation of the simulation results.
* Import the height-interpolated quality mesh {ref}`prepro-tutorial_quality-mesh-interp.2dm <qualm-interp>` (**Layer** > **Add Layer** > **Add Mesh Layer...**).


(qgis-imp-steps)=
## Import results.xdmf

The simulation results file **results.{term}`xdmf`** can be loaded in QGIS as an additional data source of the height-interpolated quality mesh ({ref}`prepro-tutorial_quality-mesh-interp.2dm <qualm-interp>`) from the pre-processing tutorial:

* In the **Layers** panel, **double-click** on **prepro-tutorial_quality-mesh-interp.2dm** to open the **Layer Properties** window.
* In the **Layer Properties**  window, go to the **Source** ribbon.
* In the **Available Datasets** frame (see {numref}`Fig. %s <qgis-assign-meshdata>`) click on the **Assign Extra Data Set to Mesh** button <img src="../img/qgis/sym-add-meshdata.png"> and choose `results.xdmf`.
* In the **Static Dataset** frame, select a **Scalar Dataset Group** and use the maximum timestep (i.e., `625 d 00:00:00` in the case of simulation time $t$=15000 with an output interval of 1000).
* Click on **Apply** and **OK**.

{numref}`Figure %s <qgis-assign-meshdata>` shows an exemplary setup of the output data interpolation on the computational mesh. To visualize other output parameters and/or other simulation timesteps, vary the definitions in the **Static Dataset** frame.

```{figure} ../img/qgis/bm-load-results.png
:alt: basement assign qgis metadata mesh
:name: qgis-assign-meshdata

Assign mesh data to the computational mesh.
```

To improve the visualization of the results, re-open the **Layer Properties** of the mesh layer and go to the **Symbology** ribbon. Visualize a simulation output parameter, such as **flow_velocity**, as follows:

* In the **Settings tab** (hammer symbol in the top-left corner highlighted in {numref}`Fig. %s <symbology4u>`) find the **Groups** listbox.
* In the **Groups** listbox, find the parameter to visualize (e.g., **flow_velocity**) and enable the contours symbol.
* Switch to the **Contours tab** next to the Settings tab (highlighted box in the top-left of {numref}`Fig. %s <symbology4u>`) and select a **Color Ramp**.
* After defining a visualization click **Apply** and **OK**.

```{figure} ../img/qgis/vis-flow-vel.png
:alt: basement qgis results velocity meshdata
:name: symbology4u

Visualize the flow_velocity parameter with the Symbology controls. The red boxes highlight relevant tabs and entries.
```

{numref}`Figure %s <qgis-plot-metadata>` illustrates a visualization of the flow velocity at the end of the simulation. The flow velocity results are also available as a video sequence ([download](https://github.com/hydro-informatics/materials-bm/raw/main/exports/velocity-video-crayfish.avi)).

```{figure} ../img/qgis/bm-meshdata-u-plotted.png
:alt: plotted qgis basement results flow velocity
:name: qgis-plot-metadata

After application of the above Symbology settings: The flow velocity is illustrated in red shades.
```

(bm-rasterize-output)=
## Rasterize Outputs

The {ref}`raster` format is useful for many post-processing tasks such as map algebra (e.g., for habitat analysis or the assessment of inundation area and depth). To this end, QGIS provides the **Rasterize mesh dataset** tool for converting mesh data at any simulation timestep to a {ref}`Raster <raster>` (e.g., as {term}`GeoTIFF`). To open the *Rasterize mesh dataset* tool, go to either **Processing** > **Toolbox** or make sure that the **View** > **Panels** > **Processing Toolbox** is checked. In the **Processing Toolbox** click on the **Mesh** group and double click on **Rasterize mesh dataset** (see also {numref}`Fig. %s <qgis-rasterize-mesh-menu>`).

```{figure} ../img/qgis/rasterize-mesh-menu.png
:alt: rasterize basement velocity water depth qgis
:name: qgis-rasterize-mesh-menu

Open the Rasterize mesh tool in QGIS' Processing Toolbox.
```

Make the following settings in the `Rasterize` window  (see also {numref}`Fig. %s <qgis-rasterize-mesh>`):

* Set the **Input Mesh Layer** to  `prepro-tutorial_quality-mesh-interp`.
* In the **Dataset groups** frame, click on the **...** button > **Select in Available Dataset Groups** and select **one parameter** (e.g., **flow_velocity**). Then, clicking on the **Go back** <img src="../img/qgis/sym-go-back.png"> button. Make sure that the **Dataset groups** canvas contains only **1** selected **option**. Otherwise, the tool will create a messy multiband {ref}`Raster <raster>`.
* In the **Dataset time** frame, check the **Dataset group time step** radio button and select the last simulation timestep (i.e., `625 d 00:00:00`).
* In the **Extent [optional]** field, click on the **...** button > **Calculate from Layer** > **prepro-tutorial_quality-mesh-interp**.
* For **Pixel size** tap `2.0` meters (the larger this number, the coarser will be the output raster).
* For **Output coordinate system** select `Project CRS: ESRI:31494 - Germany_Zone_4`.
* Define an **Output raster layer** by clicking on the **...** button > **Save to File**. Go to the target directory (e.g., `C:/Basement/steady2-tutorial/`) and enter a raster name, such as `u-end.tif` (`u` for flow velocity, `end` for last timestep, and `.tif` for {term}`GeoTIFF`).  Click **Save**.
* Click on the **Run** button to start rasterizing the mesh dataset.

After the successful rasterization, close the **Rasterize Mesh Dataset** window with a click on the **Close** button.

```{figure} ../img/qgis/rasterize-mesh.png
:alt: setup rasterize mesh geotiff
:name: qgis-rasterize-mesh

Settings to export simulation results with QGIS's Rasterize tool.
```

To enhance the visualization of the new (flow velocity) raster, double-click on the new raster in the **Layers** panel and switch to the **Symbology** tab. Select **Singleband pseudocolor** for **Render type** (in the top region of the window) and a **Color ramp**. To suppress zero-value pixels, double-click on the **Color** of the **0**-**Value** field, and in the **Select color** window reduce the **Opacity** to **0$%$**. {numref}`Figure %s <bm-exported-u-raster>` shows an example visualization of the exported flow velocity raster.


```{figure} ../img/qgis/bm-exported-u.png
:alt: basement output rasterize mesh geotiff visualization singleband pseudocolor
:name: bm-exported-u-raster

A Singleband pseudocolor (Layer Properties > Symbology) represents the exported GeoTIFF flow velocity raster with a *Reds* color ramp and zero-value pixels set to zero-opacity, superpositioned on google satellite imagery {cite:p}`googlesat`.
```

```{admonition} Analyze geodata results with Python
Facilitate the conversion and analysis of geospatial data with efficient {ref}`sec-geo-python` applications and the {{ ft_url }} package.
```

(bm-crayfish)=
## Mesh Visualization with Crayfish

The open-source [Crayfish](https://www.lutraconsulting.co.uk/projects/crayfish/) plugin enables the visualization of mesh values (e.g., change of node values over time) with many features, such as exporting video animations of model results. To create a video of, for instance, the flow velocity outputs at the 1+15 simulation timesteps, use the Crayfish plugin as follows:

* In QGIS, make sure the Crayfish plugin is installed (recall the {ref}`QGIS instructions <qgis-tbx-install>`).
* In the **Layer** panel, select **prepro-tutorial_quality-mesh-interp**.
* With *prepro-tutorial_quality-mesh-interp* selected, go to **Mesh** (top dropdown menu) > **Crayfish** > **Export Animation ...** (if the layer is not highlighted, an error message pops up: *Please select a Mesh Layer for export*).
* In the **Export Animation** window, go to the **General** tab and define an output file name by clicking on the **...** button (e.g., `velocity-video.avi`).
* Click **OK**.

The first time that a video is exported, Crayfish will require the definition of an **FFmpeg video encoder** and guide through the installation (if required). Follow the instructions and re-start exporting the video.

 ```{admonition} The resulting video export may look like this:

 <iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/AYG0i1becyI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
 ```

```{admonition} Make animations of other parameters
:class: note
To make videos of other simulation parameters, change the currently visualized parameter of the mesh (*prepro-tutorial_quality-mesh-interp*) as {ref}`explained above<qgis-imp-steps>`.
```


(bm-paraview)=
# Post-processing with ParaView

*ParaView* is freely available visualization software, which enables plotting and processing BASEMENT's *results.{term}`xdmf`* file for scientific purposes. Download and install (requires **Admin**/**sudo** rights) the latest version of *ParaView* from their [website](https://www.paraview.org/download/) (if not yet done).

## Import results.xdmf
Open *ParaView* and **click on the folder icon** (top-left of the window indicated in {numref}`Fig. %s <fig-pv-import>`) to load the simulation results file (`results.xdmf`). *ParaView* might ask to choose an appropriate XDMF read plugin: **Select `XDMF Reader`** and click `OK`. Now, the `results.xdmf` should be visible in the **Pipeline Browser** and the **Apply** button has turned green (click on it).

```{figure} ../img/paraview/import-results.png
:alt: basement results paraview
:name: fig-pv-import

ParaView after successful import of the model results (results.xdmf).
```

(pv-vis)=
## Visualize Parameters
ParaView shows by default one of the result parameters at timestep 0 (i.e., bare, dry terrain). To explore other parameters, select them in the dropdown menu of the **Active Variable Controls** menu bar (red highlight box in {numref}`Fig. %s <fig-pv-vis>`). The *Active Variable Controls* menu bar also contains options for manipulating the color range and legend. Toggle through the timesteps by using the video control buttons in the **VCR Controls** toolbar (light blue highlight box in {numref}`Fig. %s <fig-pv-vis>`).


```{figure} ../img/paraview/vis-u.png
:alt: basement results paraview
:name: fig-pv-vis

The Active Variable Controls (red box) and VCR Controls (light blue box) in ParaView to visualize output parameters at different timesteps.
```

```{admonition} Familiarize with the Viewport
The Viewport (default `Layout #1`) provides many tools for zooming into the model and changing perspectives between 2d and 3d. Click in the Viewport and hold the left mouse button to change perspectives. Take a couple of minutes to familiarize with the perspectives.
```

To **export an animation of an output parameter** over time as movie (e.g., `avi`) or image (e.g., `jpg`, `png`, `tiff`) go to **File** > **Save Animation...**.


## Save Project Pipeline
With its approach of sequences of programmable filter application, ParaView saves a *Current State* in the PVSM format rather than a project as in QGIS. The current state of a dataset in ParaView can be saved as `pvsm` file via **File** > **Save State File**. **Save** the current state of the tutorial ParaView project, for instance, in the simulation folder as **pv-project.pvsm**. To load an existing ParaView state (i.e., project), go to **File** > **Load state**.

```{admonition} Automate ParaView Pipelines
The state file can also be saved as a Python script to leverage automated pipelines and exports (read more in the {ref}`Python <standalone>` chapter).
```

(pv-exp-data)=
## Export Data
Similar to QGIS, output parameter datasets can be extracted, manipulated, or transformed in ParaView. For this purpose, programmable filters can be applied to the original dataset in ParaView to calculate (i.e., apply the **Calculator** <img src="../img/paraview/sym-calc.png"> filter), for example, the Froude number from the water depth and flow velocity datasets (read more in the [ParaView Wiki](https://www.paraview.org/Wiki/Python_calculator_and_programmable_filter)). This tutorial only features the export of mesh point data to a {term}`CSV` file with programmable filters:

* Make sure that the **Time** in the **Current Time Controls** toolbar (light blue box in {numref}`Fig. %s <fig-pv-cell-centers>`) is set to 15000 (maximum timestep).
* In the **Pipeline Browser**, **right-click** on `results.xdmf` > **Add Filter** > **Alphabetical** (i.e., a list of all available filters) > **Cell Centers**.
* In the **CellCenters1** **Properties**, check the **Vertex Cells** box and click on the now again green **Apply** button (see {numref}`Fig. %s <fig-pv-cell-centers>`).
* To save the currently active vertex data **press  `CTRL` + `S` on the keyboard**, which opens a *Save File* dialogue window. In the **Save File** window:
  * Navigate to a target folder (e.g., the simulation folder `/Basement/steady2d-tutorial/`)
  * Enter a **File name** (e.g., `flow_velocity.csv`)
  * In the **Files of type** drop-down field, select **Comma or Tab Delimited Files(`*.csv *.tsv *.txt`)**.
  * Click **OK**.
* The **Configure Writer (CSV Writer)** window opens:
  * Check the **Choose Array To Write** box.
  * Select **flow_velocity points** only (or more/other parameters).
  * Keep all other defaults.
  * Click **OK**.

```{figure} ../img/paraview/cell-centers.png
:alt: paraview basement export data
:name: fig-pv-cell-centers

Application of the CellCenters programmable filter in ParaView, with the maximum timestep defined in the Current Time Controls toolbar (light blue box).
```

Now, a *flow_velocity.*{term}`CSV` file has been written that contains point coordinates (x, y, and z coordinates) and flow_velocity in *x* (flow_velocity:0) and *y* (flow_velocity:1) directions. The flow_velocity:2 (*z*-direction) is always zero in this 2d simulation. The *flow_velocity.*{term}`CSV` file can also be used with QGIS (for instance, in QGIS go to **Layer** > **Add Layer** > **Add Delimited Text Layer...** > select *flow_velocity.csv*, assign the correct columns and separators > click **Add**).

```{admonition} Challenge: Calculate the absolute velocity
Import *flow_velocity.csv* in QGIS and calculate the absolute flow velocity $U$ from $u_x$ (flow_velocity:0) and $u_y$ (flow_velocity:1) as $U = \sqrt{u^2_x + u^2_y}$. How do the flow fields comply with the above-created `u-end.tif` (see {ref}`bm-rasterize-output` section) raster?
```

(bm-python)=
# Python Simulation Verification
BASEMENT's developers at the ETH Zurich provide a suite of [Python scripts](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/) for post-processing the simulation results. For the here used BASEMENT v3, download the Python script [BMv3NodestringResults.py](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/BMv3NodestringResults.py), which exports defined output parameters at the user-defined {ref}`STRINGDEFs <bm-geo-fin>`.

To run the Python script, {ref}`install Python <install-python>` for your platform along with the `numpy` and `h5py` packages.

```{admonition} Guidance for installing Python
Consider to install Python in a {ref}`conda-env` (*Windows*) or a {ref}`venv (pip) <pip-env>` (*Linux*) with {{ ft_url }}, which already includes all requirements for running *BMv3NodestringResults.py*.
```

For running the *Python* script on any platform:

* Optionally activate the relevant *Python* (conda or venv) environment.
* `cd` (change directory) into the simulation folder.
* Run `python BMv3NodestringResults.py`.

In detail, this looks as follows:

`````{tab-set}
````{tab-item} Windows / conda
Launch *Windows* or *Anaconda Prompt* and tap (requires that the conda environment {ref}`flussenv <conda-quick>` is installed):
```
conda activate flussenv
cd C:\Basement\steady2d-tutorial\
python BMv3NodestringResults.py
```
````

````{tab-item} Linux / pip
Launch *Linux Terminal* and tap (requires that the pip environment {ref}`vflussenv <pip-quick>` is installed in the HOME directory):
```
cd ~
source vflussenv/bin/activate
cd /Basement/steady2d-tutorial/
python BMv3NodestringResults.py
```

If {ref}`vflussenv <pip-quick>` is installed in another directory than HOME, replace `cd ~` in the first line of the above code block with the parent installation directory of {ref}`vflussenv <pip-quick>`.
````
`````

{numref}`Figure %s <export-py>` illustrates running *BMv3NodestringResults.py* on *Windows* in *Anaconda Prompt*.

```{figure} ../img/basement/export-ns-py.png
:alt: export nodestring python script basement BMv3NodestringResults
:name: export-py

A Python Anaconda Prompt window running BMv3NodestringResults.py
```

Running the *Python* script generates three {term}`CSV` files that contain values at the user-defined {ref}`STRINGDEFs <bm-geo-fin>`:

* **Discharge.csv** contains inflow and outflow discharges.
* **results.csv** contains any OUTPUT parameter defined in the {ref}`simulation setup file <bm-sim-file>`.
* **timestep.csv** lists the number of OUTPUT parameter timesteps.

The primarily important file is **Discharge.csv**, from which can be read when inflow and outflow converge in a steady-state simulation (i.e., **the simulation stabilizes**). A steady simulation in which the sum of all inflows does not equal all outflows must be considered erroneous. For instance, if the sum of outflows in the last timestep is smaller than the sum of inflows, then the simulation time is too short. The diagram in {numref}`Fig. %s <convergence-diagram-bm>` plots inflow and outflow for the simulation setup of this tutorial. The diagram suggests that the model reaches stability after timestep 11 (simulation time $t \leq 11000$). Thus, the simulation time could be limited to $t = 12000$, but a simulation time of $t = 10000$ would be too short.

```{figure} ../img/basement/convergence-diagram.png
:alt: basement convergence model simulation discharge verification validation
:name: convergence-diagram-bm

Convergence of inflow and outflow at the model boundaries.
```

Note the difference between the convergence duration in this steady simulation with BASEMENT (plot in {numref}`Fig. %s <convergence-diagram-bm>`) that starts with a dry model compared to the shorter convergence duration in the Telemac2d  tutorial that starts with an initial condition of 1.0 m water depth (plot in {numref}`Fig. %s <convergence-diagram-tm2d>`). This difference mainly stems from the type of initial conditions (dry channel versus initial depth) that also reflects in a zero-outflow in the BASEMENT simulation and an outflow surplus that is visible in the Telemac2d simulation at the beginning of the simulations.

```{admonition} Discharge convergence issues
* **Perpetually increasing discharge in a steady simulation**<br>The definition of the  {ref}`upstream_direction <bm-geo-fin>` (e.g., wrongly defined as `"left"` or `"right"`) may cause this error.
* **Outflow smaller than inflow**<br>Increase the simulation time (see the {ref}`bm-sim-file` section).
* **No water in the model**<br>The discharge defined in the *steady-inflow.txt* file (see {ref}`bm-hydraulics` section) must define reasonable flows in the simulation time. In addition, the definition of the  {ref}`upstream_direction <bm-geo-fin>` (e.g., wrongly defined as `"left"` or `"right"`) may cause this error. Depending on your system's region settings, use the English **`.`** in lieu of the European **`,`** decimal delimiter to define discharges in *steady-inflow.txt*.
```

**What next?**
: The verification of the model stability represents only one step on the pathway to a useable model in practice. Before a numerical model can be used for simulating decision-making scenarios, it must be calibrated and validated with measurement data (similar to TELEMAC {ref}`hydrodynamics <tm2d-calibration>`). 
