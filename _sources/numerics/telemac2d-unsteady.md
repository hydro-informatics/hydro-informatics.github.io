(chpt-unsteady)=
# Unsteady 2d

```{admonition} Requirements
This tutorial is designed for **advanced modelers** and before diving into this tutorial make sure to complete the {ref}`TELEMAC pre-processing <slf-prepro-tm>` and {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials.

The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

## Get Started

The {ref}`steady 2d tutorial <telemac2d-steady>` hypothesizes that the discharge of a river is constant over time. However, the discharge of a river is never truly steady and varies slightly from second to second, even in flow-controlled rivers. Alas, the inherently unsteady flow regime of rivers cannot realistically be modeled in any numerical software. As a result, we must discretize time-dependent discharge (e.g., a flood hydrograph) in a numerical model as a series of steady discharges. {numref}`Figure %s <unsteady-hydrograph>` illustrates the discretization of a natural flood hydrograph into steps of steady flows, which will be used in this tutorial. Note that the hydrograph **starts at Time = 15000**, which is the result of using the steady2d simulation end state for model initialization. Note that the end time of T=15000 represents the end of the dry steady model initialization, as described in the {ref}`tm2d-dry` section (results can be downloaded, see below).

```{figure} ../img/telemac/unsteady-hydrograph.png
:alt: unsteady flow discharge quasi steady telemac telemac2d hydrodynamic
:name: unsteady-hydrograph

The discretization of a natural hydrograph into steps of steady flows (qualitative hydrograph for this tutorial).
```

This tutorial shows how such a quasi-steady discharge hydrograph can be created through the definition of an inflow sequence (red circles in {numref}`Fig. %s <unsteady-hydrograph>`) and implemented in a Telemac2d simulation. The tutorial builds on the steady simulation of a discharge of 35 m$^3$/s and requires the following data from the {ref}`pre-processing <slf-prepro-tm>` and {ref}`steady2d <telemac2d-steady>` tutorials, which can be downloaded by clicking on the filenames:

* The computational mesh in [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf).
* The boundary definitions in [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli).
* The results of the steady 2d model run for 35 m$^3$/s in [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) (result of the {ref}`dry bonus run <tm2d-dry>` ending at `T=15000`).

Consider saving the files in a new folder, such as `/unsteady2d-tutorial/`.

```{admonition} Unsteady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/).
```

(prepro-unsteady)=
## Model Adaptations

The integration of unsteady flows requires the adaptation of keywords and additional keywords (e.g., for linking liquid boundary files) in the steering (`*.cas`) file from the steady2d tutorial ([download steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

```{admonition} View the unsteady steering file
To view the integration of the unsteady simulation keywords in the steering file, the `unsteady2d.cas` file can be [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/unsteady2d.cas)
```

### Initial Conditions

**The following descriptions refer to section 4.1.3 in the {{ tm2d }}.**

To speed up the calculations and provide a well-converging baseline for the quasi-steady calculations, this tutorial re-uses the output of the steady 2d simulation with dry initial conditions (see the {ref}`tm2d-dry` section). To this end, the steady results file [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) needs to be defined as `PREVIOUS COMPUTATION FILE`:

```fortran
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
/ INITIAL TIME SET TO ZERO : 0 / avoid restarting at 15000
```

In addition, a `INITIAL TIME SET TO ZERO` keyword may be defined with its default of `0` to reset the time from the previous computation file from `15000` to `0`. However, this tutorial does not use this option and continues at timestep 15000.
To avoid ambiguous definitions of the initial conditions, **deactivate** (i.e., delete or comment out lines with a `/`) a little further down in the steering file the **`INITIAL ...` keywords**:

```fortran
/ INITIAL CONDITIONS : 'CONSTANT DEPTH'
/ INITIAL DEPTH : 1
```


### General Parameters

To simulate the hydrograph shown in {numref}`Fig. %s <unsteady-hydrograph>`, the simulation must run for at least 15000 time steps (i.e., from `T=15000` to `T=30000`). Since printing out (intermediate) results has a significant effect on computational speed, we reduce graphic print-out time steps to every `500` time steps (in lieu of `200` used for the steady simulation):

```fortran
TIME STEP : 1.
NUMBER OF TIME STEPS : 15000
GRAPHIC PRINTOUT PERIOD : 500
LISTING PRINTOUT PERIOD : 500
```

(tm2d-liq-file)=
### Open Boundaries

This section features the implementation of quasi-steady (unsteady) flow conditions at the open liquid with a time-dependent inflow hydrograph and a downstream {term}`Stage-discharge relation`  (recall the rationales behind the choice of boundary types from the {ref}`pre-processing tutorial <bk-liquid-bc>`).

---

**Define a Quasi-steady Hydrograph**

With the dry-initialized model ending at T=15000, the hydrograph needs to start at `15000`, even though the model start will represent time *zero* of the unsteady simulation. To implement the triangular-shaped hydrograph shown in {numref}`Fig. %s <unsteady-hydrograph>`, **create a new file called `inflows.liq`** in the simulation folder. Open the new `inflows.liq` file in a text editor and add the red-circled points in {numref}`Fig. %s <unsteady-hydrograph>` as time-dependent flow information at the **upstream (1)** and **downstream (2)** open (liquid) boundaries. In this file:

* Add a file header starting with `#` signs (out-commented lines ignored by TELEMAC).
* Implement 1 columns (for time **T** and upstream inflow rate **Q(1)**).
* Separate the columns either with *spaces*.
* The first column must be time `T` with strictly monotonously increasing values and the last time value must be greater than or equal to the last simulation timestep.

```{admonition} How does TELEMAC count open (liquid) boundaries?
Recall the information provided in the comment box in the {ref}`steady2d tutorial <tm2d-bounds>`.
```

Thus, the [`inflows.liq`](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/inflows.liq) file should look similar to this:

```python
# Inflow hydrograph
#
T	Q(1)
s	m3/s
15000	35
16000	35
17000	50
19000	1130
22000	101
25000	35
99000	35
```

The original `boundaries.cli` file describes the downstream boundary with `prescribed Q and H` (type `5 5 5`). However, in the unsteady calculation, `Q` needs to be free (otherwise, Q(2) needed to be defined in `inflows.liq` with an additional column) and for this reason, the `boundaries.cli` file requires some adaptions:

* **Open** the provided [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli) file with a text editor (e.g., {ref}`npp` on Windows or {ref}`Atom <install-atom>`).
* Use find-and-replace (e.g., `CTRL` + `H` keys in {ref}`npp`, or `CTRL` + `F` keys in {ref}`install-atom`):
  * **Find** `5 5 5`
  * **Replace** with `5 4 4`
  * Click on **Replace ALL**.
* **Save** the file as **boundaries-544.cli** and close it.

Verify the correct settings by downloading [boundaries-544.cli](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/boundaries-544.cli) for the unsteady simulation.

In the **steering file**, adapt the **file name for the boundary conditions** and add the link to **inflows.liq**:

```
BOUNDARY CONDITIONS FILE : boundaries-544.cli
/ ...
LIQUID BOUNDARIES FILE : inflows.liq
```

---

**Rating Curve (Stage-Discharge Relation)**
To activate the use of a {term}`Stage-discharge relation` for an open (liquid) boundary with the `STAGE-DISCHARGE CURVES` keyword needs to be added to the steering file. This keyword accepts the following integers:

* `0` is the **default** that deactivates the usage of a stage-discharge curve.
* `1` applies prescribed elevations as a function of calculated flow rate (discharge).
* `2` applies prescribed flow rates (discharge) as a function of calculated elevation.

The `STAGE-DISCHARGE CURVES` keyword is a list that assigns one of the three integers (i.e., either `0`, `1`, or `2`) to the open (liquid) boundaries. In this tutorial `STAGE-DISCHARGE CURVES : 0;1` actives the use of a {term}`Stage-discharge relation` for the downstream boundary only where the **upstream open boundary number 1** is set to `0` and the **downstream open boundary number 1** is set to `0`.

The form (curve) of the {term}`Stage-discharge relation` needs to be defined in a stage-discharge file ({term}`ASCII` text format). Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). This tutorial uses the following relation that is stored in a file called `ratingcurve.txt` ([download](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/ratingcurve.txt)):

```
# Downstream ratingcurve.txt
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
```

To define {term}`Stage-discharge relation`s for multiple open boundaries (e.g., at river diversions or tributaries), add the curves to the same file. TELEMAC automatically recognizes where the curves apply by the number given in parentheses after the parameter name in the column header. For instance, in the above example for this tutorial, the column headers `Z(2)` and `Q(2)` tell TELEMAC to use these values for the second (i.e., downstream) open boundary. The column order is not important because TELEMAC reads the curve type (i.e., either $Q(Z)$ or $Z(Q)$) from the `STAGE-DISCHARGE CURVES` keyword.

````{dropdown} Expand to view an example for multiple stage-discharge curve definitions
The following file block would prescribe {term}`Stage-discharge relation`s to the upstream and downstream boundary conditions in this tutorial. However, the file cannot be used here unless the upstream boundary type is changed to `5 5 5` (`prescribed H and Q`) in the `boundaries.cli` file (read more in the {ref}`pre-processing tutorial <bk-liquid-bc>`).
```
#
# Downstream Rating Curve
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
#
# Upstream Rating Curve
#
Q(1)  Z(1)
m3/s  m
35    371.33
50    371.45
101   371.86
1130  375.73
2560  379.08
```
````

To use the stage-discharge file, **define the `STAGE-DISCHARGE ...` keywords in the steering file**:

```
/ steering.cas
STAGE-DISCHARGE CURVES : 0;1
STAGE-DISCHARGE CURVES FILE : ratingcurve.txt
```

---

**Remove Ambiguous Open Boundary Definition Keywords**

To avoid ambiguous definitions of the open boundaries conditions, **deactivate** (i.e., delete or comment out lines with a `/`) in the steering file the **`PRESCRIBED ...` keywords**:

```fortran
/ PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 0.;371.33
```


### Numerical Parameters

The predictor-corrector schemes (`SCHEME FOR ...` keywords defined with `3`, `4`, `5`, or `15` as explained in the {ref}`steady2d tutorial <tm2d-numerical>`) rely on a parameter defining the number of iterations at every timestep for convergence. For quasi-steady simulations, the developers recommend setting this parameter to `2` or slightly larger (section 7.2.1 in the {{ tm2d }}). Therefore, **add the following line to the steering file**:

```fortran
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2
```

(tm-control-sections)=
### Control Sections

A consistent way to verify fluxes at open boundaries or other particular lines (e.g., tributary inflows or diversions) is to use the `CONTROL SECTIONS` keyword. A control section is defined by a sequence of neighboring node numbers. For instance, to verify the fluxes over the open boundaries in this tutorial, check out the node numbers in the `boundaries.cli` file (e.g., 144 to 32 for the upstream and 34 to 5 for the downstream boundary). Then, **create a new text file** (e.g., **control-sections.txt**) and:

* **Add one comment line** with some short information (e.g., `# control sections input file`). Note that this line is **mandatory**.
* In the **second line** add a **space-separated list of 2 integers** where
  * the first integer defines the number of cross-sections, and
  * the second integer defines if node numbers (i.e. IDs from `boundaries.cli`) or coordinates will be defined. A negative number sets node IDs and a positive number coordinates.
* **Define as many cross sections as defined with the first integer.** Every cross-section definition consists of two lines:
  * The first line is a *string* (text) without spaces that is naming the cross-section (e.g., `inflow_cs`).
  * The second line consists of two numbers defining the start and end points of the cross-sections. If the second integer in the file line is negative, provide two space-separated integers. If the second integer is positive, provide two space-separated pairs of coordinates (put a space between coordinates).

For example, the following *control-sections.txt* file can be used with the steady simulation in this tutorial ([download control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/control-sections.txt)).

```
# control sections steady2d
2 -1
Inflow_boundary
144 32
Outflow_boundary
34 5
```

````{dropdown} Expand to view an example for coordinate-based control sections
The following control section file uses point coordinates rather than node ID numbers to define three sections. Read more in {cite:t}`baxter2013` (i.e., section 4.1.2 in the [Baxter tutorial](http://www.opentelemac.org/index.php/component/jdownloads/summary/4-training-and-tutorials/185-telemac-2d-tutorial?Itemid=55)).
```
# control section file using coordinates
3 0
affluent_creek
19572355.895577 626823.06664 1952347.2733 626923.9554
main_river_upstream
1946449.824 635349.6070 194.919 635209.807
main_river_downstream
1967737.56993 620784.415608 1967998.16429 620638.17849
```
````

The second line in this file tells TELEMAC to use `2` control sections, which are defined by node IDs (`-1`). To use the control sections for the simulation add the following to the steering file:

```
/ steady2d.cas
/ ...
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
```

Thus, re-running the simulation will write the fluxes across the two define control sections to a file called *r-control-flows.txt*. The {{ tm2d }} provides explanations in section 5.2.2.

## Run Telemac2d Unsteady

Go to the configuration folder of the local TELEMAC installation (e.g., `~/telemac/v8p2/configs/`) and launch the environment (e.g., `pysource.openmpi.sh` - use the same as for compiling TELEMAC).

```
cd ~/telemac/v8p2/configs
source pysource.openmpi.sh
```

````{admonition} If you are using the Hydro-Informatics (Hyfo) Mint VM
:class: note, dropdown

If you are working with the {ref}`Mint Hyfo VM <hyfo-vm>`, load the TELEMAC environment as follows:

```
cd ~/telemac/v8p2/configs
source pysource.hyfo-dyn.sh
```
````

With the TELEMAC environment loaded, change to the directory where the above-created 3d-flume simulation lives (e.g., `/home/telemac/v8p2/mysimulations/unsteady2d-tutorial/`) and run the `*.cas` file by calling the **telemac2d.py** script.

```
cd ~/telemac/v8p2/mysimulations/unsteady2d-tutorial/
telemac2d.py unsteady2d.cas
```

````{admonition} Speed up
With {ref}`parallelism <mpi>` enabled (e.g., in the {ref}`Mint Hyfo Virtual Machine <hyfo-vm>`), speed up the calculation by using multiple CPUs through the `--ncsize=N` flag. For instance, the following line runs the unsteady simulation on `N=2` CPUs:

```
telemac2d.py unsteady2d.cas --ncsize=2
```
````
A successful computation should end with the following lines (or similar) in *Terminal*:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                            10  MINUTES
                            32  SECONDS
... merging separated result files

... handling result files
       moving: r2dunsteady.slf
       moving: r-control-sections.txt
... deleting working dir

My work is done
```

Telemac2d will write the files *r2dunsteady.slf* and *r-control-sections.txt*. Both result files are also available in the modelling repository to enable accomplishing the post-processing tutorial:

* [get r2dunsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dunsteady.slf), and
* [get r-control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r-control-sections.txt).


## Post-processing

### Open Boundary Flows

The unsteady simulation intends to model time-variable flows over the open upstream and downstream open boundaries. The above-defined {ref}`control sections <tm-control-sections>` enable insights into the correct adaptation of the flow at the upstream inflow boundary (`prescribed Q` through *inflows.liq*) and the downstream outflow boundary (`prescribed H` through *ratingcurve.txt*). {numref}`Figure %s <res-unsteady-hydrograph>` shows the modeled flow rates where the *Inflow_boundary* shows perfect agreement with *inflows.liq* and the *Outflow_boundary* reflects the flattening of the discharge curve in the modeled meandering gravel-cobble bed river.

```{figure} ../img/telemac/res-unsteady-hydrograph.png
:alt: result unsteady flow discharge telemac2d hydrodynamic inflow outflow control sections
:name: res-unsteady-hydrograph

The simulated flows over the upstream *Inflow_boundary* and the downstream *Outflow_boundary* control sections.
```

The peak inflow corresponds to the specified 1130 m$^3$/s while the outflow peak discharge is only 889 m$^3$/s and the peak takes about 1070 seconds (inflow at $T=19000$ and outflow at $T\approx 20070$) to travel through the section.


````{admonition} Resolve volume balance issues in unsteady simulations
:class: warning, dropdown
The total inflow and outflow volumes in the here featured simulation amount to 3479930.958 m$^3$ and 3430100.437 m$^3$, respectively. Thus, there is a total volume error of 1.4$%$. To overcome such issues, the {{ tm2d }} recommend using a minimum value for water depth to define when a cell is wet or dry. Still, the developers do not recommend using a minimum water depth for most simulations and emphasize using this option only for unsteady (quasi-steady) simulations. Defining a minimum water depth requires setting the `TREATMENT OF THE TIDAL FLATS` keyword to `2` (read more in the {ref}`steady2d tutorial <tm2d-tidal>`), which is not compatible with the parallelization routines, nor with the here used `SCHEME FOR ADVECTION ... : 14` settings. Thus, good results, but long non-parallelized quasi-steady calculations can be yielded with the following keywords in the steering file:

```fortran
OPTION FOR THE TREATMENT OF TIDAL FLATS : 2 / use segment-wise flux control
MINIMUM VALUE OF DEPTH : 0.1 / in meters
```
````


### Visualization with QGIS

The results of the unsteady simulation can be visualized and exported to raster (e.g., {term}`GeoTIFF`) or shapefile formats in QGIS with the PostTelemac plugin the same way as explained in the steady2d tutorial ({ref}`read the steady2d post-processing <tm2d-post-export>`). The latest QGIS releases additionally enable to load the Selafin results mesh file (here: *r2dunsteady.slf*) as a QGIS mesh layer. Therefore, **launch QGIS**, go to the **Layer** menu and click on **Add Layer** > **Add Mesh Layer...**. In the popup window (*Data Source Manager / Mesh*), **select r2dunsteady.slf**, click **Add**, and **Close**. {numref}`Figure %s <qgis-r2dunsteady-imported>` shows the imported r2dunsteady mesh layer in QGIS with a *Softlight* blending (set in the *Symbology*) on google satellite imagery.

```{figure} ../img/telemac/qgis-r2dunsteady-imported.png
:alt: qgis telemac2d unsteady quasi steady simulation results slf
:name: qgis-r2dunsteady-imported

The unsteady (quasi-steady) simulation results file r2dunsteady.slf imported as mesh layer in QGIS and super-positioned on google satellite imagery {cite:p}`googlesat`.
```

The simulation parameter (e.g., `U`, `V`, or `Q`) and the timestep shown can be controlled in the layer properties of the `r2dunsteady` layer (double-click on it in the *Layers* panel).

To **create a video of simulation results**, use the open-source [Crayfish](https://www.lutraconsulting.co.uk/projects/crayfish/) plugin that enables the animated visualization of meshes and their attributes (e.g., change of node values over time). Get the *Crayfish* plugin from QGIS **Plugins** menu > **Manage and Install Plugins...** > tap `crayfish` in the **All** tab and click on **Install Plugin**. The plugin is now ready to create a video by clicking through QGIS **Mesh** menu > **Crayfish** **Export Animation ...**. In the *Crayfish* popup window, toggle through three tabs, and adapt video settings (e.g., define a file name such as `velocity-video.avi` in the **General** tab). Note that *Crayfish* will automatically export the frame and active variable (here, the default is `U`) selected on the mesh (*Layer Properties*). When all settings are made, click on **OK** to start the export.

```{admonition} Crayfish first time use
:class: warning
The first time that a video is exported, *Crayfish* will require the definition of an **FFmpeg video encoder** and guide through the installation (if required). Follow the instructions (preferably use automatic installers). If *Crayfish* did not automatically continue the video export, re-start exporting the video after the FFmpeg installation.
```

The below-shown box features and exemplary video output of flow velocity.

```{dropdown} Expand to view the resulting video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/JKAiZ1ChUEg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>
```

**What next?**
: This tutorial ends with the graphical output of modeled flow parameters, but there are a couple more steps to accomplish in practice. For instance, the time that the flow peak takes to travel through the modeled river section might be too short (i.e., flow is too fast) or too long (i.e., flow is too slow) compared to observation data (e.g., from stream gauges). In these cases, model calibration through variations of the {ref}`FRICTION COEFFICIENT <tm2d-friction>` keyword might be a solution. Read more in the {ref}`calibration` section.
