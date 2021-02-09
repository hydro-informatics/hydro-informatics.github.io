---
title: Post-Processing
tags: [basement, hydraulics, raster, shapefile, qgis, morphodynamics, ecohydraulics]
keywords: numerics
summary: "Use ParaView and QGIS to visualize and analyze results."
sidebar: mydoc_sidebar
permalink: bm-post.html
folder: numerics
---

## Visualize results with ParaView
###	Get ready with ParaView
*ParaView* is a freely available visualization software, which enables plotting *BASEMENT* v.3.x results in the shape of `xdmf` (*eXtensible Data Model and Format*) files. Download and install the latest version of *ParaView* from their [website](https://www.paraview.org/download/), if not yet done. 

### Load BASEMENT results
Open *ParaView* and click on the folder icon (top left of the window) to open the simulation results file (`results.xdmf`). *ParaView* might ask to choose an appropriate XMDF read plugin. Select `XDMF Reader` here and click `OK`:
 
To explore the model results:
- Select variables (e.g., `flow_velocity`, `water_depth`, or `water_surface`) in *ParaView*'s `Cell Arrays` canvas (green-highlighted circle in the below [figure](#pv-vis)). 
- Click the `Apply` button (red-highlighted circle in the Properties tab in the below [figure](#pv-vis)). All variables are now loaded and can be plotted.
- To plot a variable, select one (e.g., `flow_velocity`) in the toolbar (light-blue-highlighted circle in the upper part of the below [figure](#pv-vis)). Then click the play button in the toolbar (dark-blue-highlighted circle around the green arrow in the upper part of the below [figure](#pv-vis)) to cycle through the time steps.
 
<a name="pv-vis"></a>
{% include image.html file="pv-vis.png" alt="bm-x3" caption="ParaView after successful import of the model results (results.xdmf) - see above descriptions." %} 

All available time steps are listed in the Blocks tab (bottom-left in Figure 1). Anything should be visible at the beginning because the initial conditions were defined as `dry` (see the [*BASEMENT* modeling exercise part](bm-main.html#init) ). The above [figure](#pv-vis) shows the last time step (`Timestep[25]`), with water flowing at a peak velocity of 3.7 m/s. The 25 available time steps result from the definition made in *BASEMENT*'s `SIMULATION` tab with a total duration of 5000.0 and an output step of 200.0. Note that the time units have no dimension here because they correspond to computational time steps.

###	Export visualizations<a name="exp-vis"></a>
The animations can be saved as movie (e.g., `avi`) or image (e.g., `jpg`, `png`, `tiff`) files via `File` > `Save Animation...`.
The current state (variable, `Timestep[i])` can be saved as `pvsm` file via `File` > `Save State File`. The state file can also be saved as Python script for external execution and implementation in [Python programs](hy-install.html).

### Export data<a name="exp-data"></a>
For geospatial calculations (e.g., calculate [habitat suitability indices for target fish species](https://riverarchitect.github.io/RA_wiki/SHArC) based on flow velocity and water depth), the simulation results must be converted to geospatial data formats. The first conversion step is to extract relevant point data in *ParaView*:

1. With the `results.xdmf` file opened in *ParaView*, right-click on `results.xdmf` in the `Pipeline Browser`, then `Add Filter` > `Alphabetical` > `Cell Centers`
1. With the `CellCenters1` filter enabled in the `Pipeline Browser` (blue-highlighted circle in the [figure below](#pv-exp-steps)), set the `Time` in the menu bar to the end time step (here: `5000`, i.e., step no. `25`, see the red-highlighted circle in the [figure below](#pv-exp-steps)))
1. In the `Properties` tab (green-highlighted circle in the [figure below](#pv-exp-steps)), check the `Vertex Cells` box, and click the `Apply` button.
1. Press  `CTRL` + `S` on the keyboard > a `Save File` dialogue window opens:
    * Navigate to the folder where you want to save the data
    * Enter a `File name` (e.g., *bm-steady-vanilla*)
    * In the `Files of type` drop-down field, select `Comma or Tab Delimited Files(*.csv *.tsv *.txt)`
    * Click `OK`
1. The `Configure Writer (CSVWriter)` window opens. Make sure that `Point Data` is selected as `Field Association`. Optionally, check the `Choose Arrays To Write` box and select relevant fields only. Press the `OK` button.

The point data export is now complete. The next step is to import the data (here: *bm-steady-vanilla.csv*) in *QGIS* ([next section](#qgis-import)).

<a name="pv-exp-steps"></a>
{% include image.html file="pv-exp-steps.png" alt="bm-x3" caption="The CellCenters (dark-blue circle) filter in ParaView, with the maximum Time step setting (red circle) and the Properties definitions (green circle)" %} 

## QGIS
### Add the Crayfish Plugin<a name="add-crayfish"></a>
For best visualization in *QGIS*, follow the developer's recommendation and install the *Crayfish* Plugin (*QGIS*' `Plugins`menu > `Manage and Install Plugins...` > `All` tab > enter *Crayfish* in the `Search...` field and install the Plugin).
After successful installation, the *Crayfish* tools are available in *QGIS* toolbox, which can be activated as follows:
<a name="qgis-tbx"></a>
{% include image.html file="qgis-tbx.png" alt="bm-5" caption="Open QGIS' Toolbox window from the main menu." %}
The *Crayfish* tools are listed at the bottom of the `Toolbox` window.

### Import results<a name="imp-steps"></a>
There are two (to three) options to import the results in *QGIS*:

1. [Use *ParaView* Outputs](#pv-exp-steps)
1. [Modify `results.xdmf` and directly import results in *QGIS*](#qigs-imp-steps)
1. [Use an import tool (currently only available on demand)](#schmalzl)

#### Use *ParaView* export (here: *bm-steady-vanilla.csv*)

After data export from *ParaView*:<a name="pv-exp-steps"></a>
- In *QGIS*, click on the `Layer` menu > `Add Layer` > `Add Delimited Text Layer...`.
<a name="qgis-add-lyr"></a>
{% include image.html file="qgis-add-lyr.png" alt="bmx" caption="Open the Add Delimited Text Layer import wizard." %} 

- The `Data Source Manager | Delimited Text` window opens ([see figure below](#qgis-import-csv))
- In the `File name` field select *bm-steady-vanilla.csv*
- Enter a `Layer name` (e.g., *bm-steady-vanilla-csv*)
- In the `File Format` canvas, check the `CSV (comma separated values)` box
- In the `Record and Field Options` canvas, activate the `First record has field names` checkbox
- In the `Geometry Definition` canvas, define the `Point Coordinates` as `X field` = `Points:0`, `Y field` = `Points:1` and `Z field` = `Points:2` (verify the correctness: `X`-data should be in the order of 4.2 to 4.4·10<sup>6</sup>, `Y`-data should be in the order of 5.5·10<sup>6</sup>, and `Z`-data should be in the order of 100.0 to 200.0)
- Set the `Geometry CRS` to the `Project CRS` (`ESRI:31493 - Germany_Zone_3`).
- Click the `Add` and the `Close` buttons on the bottom of the window. The points should now be plotted in the main *QGIS* window.
<a name="qgis-import-csv"></a>
{% include image.html file="qgis-import-csv.png" alt="bmy" caption="The Data Source Manager | Delimited Text window with required settings highlighted with the green marker." %} 

#### Use the `results.xdmf` file directly(***recommended for geospatial data conversion***)<a name="qgis-imp-steps"></a>
Modify `results.xdmf` and directly import model result in *QGIS*:
- Open `results.xdmf` in a text editor (e.g., [*Notepad++*](https://notepad-plus-plus.org/downloads/))
- Use the find-and-replace tool (`CTRL` + `H` keys in *Notpad++*) to remove file paths before `results_aux.h5` in the document (otherwise *QGIS* will crash later on - [read more in *BASEMENT*'s User Forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?id=5261)).
- For example: `Find what` = `C:/temp/results_aux.h5` (pay attention to use `/` rather than `\`) and `Replace with` = `results_aux.h5` (see [below figure](#npp-xdmf-replace)). After having removed all path occurrences in the document, save and close `results.xdmf`. 
    <a name="npp-xdmf-replace"></a>
    {% include image.html file="npp-xdmf-replace.png" alt="bmy" caption="Find the string results_aux.h5 in results.xdmf and remove the file directories." %} 
- If not yet done, load the mesh file (here: [`finalmesh.2dm`](bm-pre.html#2dm)) by clicking on *QGIS*' `Layer` menu > `Data Source Manager` > `Mesh` tab and select `finalmesh.2dm`.
- In *QGIS*' `Layers` window, double-click on the `finalmesh` layer to open the `Layer Properties` window.
- In the `Layer Properties` window, go to `Source` > click on `Assign Extra Data Set to Mesh` and choose  `results.xdmf` 
    <a name="qgis-assign-meshdata"></a>
    {% include image.html file="qgis-assign-meshdata.png" alt="bmy" caption="Assign mesh data to the computational mesh." %}     
- After import, double-click on the new `results` layer to open the `Symbology` (`Layer Properties`) and select a variable to represent from the `Groups` canvas. Make sure to enable the contour plot (right side in the [below figure](#qgis-meshdata-u)) symbol, select the timestep to plot (for steady-state simulation, select the last timestep), optionally go to the `Contours` ribbon to change the color pattern (upper-most green circle in the [below figure](#qgis-meshdata-u)), and click `Apply`.
    <a name="qgis-meshdata-u"></a>
    {% include image.html file="qgis-meshdata-u.png" alt="bmy" caption="Illustrate the flow velocity with QGIS' Layer Properties > Symbology controls. The green circles highlight settings for the last timestep of a steady-state simulation." %}    
    {% include image.html file="qgis-meshdata-u-plotted.png" alt="bmy" caption="After application of the above Symbology settings: The flow velocity is illustrated in red-shades." %}
    
Thanks to Matthias Bürgler who helped with instructions in the [*BASEMENT* user forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?pid=6095#p6095).
 
#### Klaus Schmalzl's `Basement_post_W.exe` <a name="schmalzl"></a>
Another option in the future will be [Klaus Schmalzl's `Basement_post_W.exe`](http://people.ee.ethz.ch/~basement/baseweb/users-meetings/30-01-2020/6_Schmalzl.pdf), which is currently only available on demand.


### Convert results to geospatial formats (SHP and TIF)<a name="qgis-exp-steps"></a>
To analyze the imported results, they need to be converted to geo-spatial data format such as [ESRI Shapefiles](https://en.wikipedia.org/wiki/Shapefile) or [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF) rasters. There are two options available depending on how data were imported:

1. Conversion with the [Crayfish plugin](#crayfish-exp) after [direct import of `results.xdmf`](#qgis-imp-steps) (recommended)
1. Conversion of [*ParaView* exports](#pv-conv) (not recommended)

#### Conversion with the Crayfish plugin (recommended)<a name="crayfish-conv"></a>
{% include tip.html content="Ensure that the [*Crayfish* plugin is correctly installed](#add-crayfish) an open *Crayfish*'s `Rasterize` tool from *QGIS*' `Processing` menu > `Toolbox` > `Crayfish` > `Rasterize` (see figure below)" %}
<a name="qgis-crayfish-installed"></a>
{% include image.html file="qgis-crayfish-installed.png" alt="bmy" caption="Open the Rasterize tool of the Crayfish plugin." %}

- In the `Rasterize` window make the following settings (see also [figure below](#qgis-crayfish-exp)):
    * `Input mesh layer` =  `finalmesh`
    * `Minimum extent to render (xmin, xmax, ymin, ymax)` =  click on the `...` button and select the `Layer` option (choose `finalmesh`)
    * `Map units` = `0.1` (can also be larger - the larger this number, the coarser the output *tif*)
    * `Dataset group` =  `flow_velocity` (or whatever variable should be in the final *tif*  - note that rasters can/should have only one value per pixel)
    * `Timestep` = `208 days, 8:00:00` (last timestep in the case of steady-state simulations)
    * `Output layer` = `C:\ ... \u.tif` (or whatever variable / raster specifier applies)
- Click `Run`

<a name="qgis-crayfish-exp"></a>
{% include image.html file="qgis-crayfish-exp.png" alt="bm-qce" caption="Settings to be made in Caryfish's Rasterize tool." %} 

With a `Singleband pseudocolor` > `Spectral` `Symbology`-selection in the `Layer Properties`, the *QGIS* window should now look like this:

<a name="qgis-crayfish-final"></a>
{% include image.html file="qgis-crayfish-final.png" alt="bm-qce" caption="A Singleband pseudocolor (Layer Properties > Symbology) selection will represent the velocity distribution in the final velocity GeoTIFF." %}


#### Conversion of ParaView exports (not recommended)<a name="pv-conv"></a>

- In *QGIS*, right-click the above imported csv-points layer (here: `bm-steaedy-vanilla-csv`) > `Export` > `Save Features As...`
- The `Save Vector Layer as...` window opens ([see figure below](#qgis-exp-sim-pts)), where the following settings need to be defined:
    * `Format` =  `ESRI Shapefile`
    * `File name` =  for example `C:\...\bm-vanilla-pts.shp`
    * `CRS` = `ESRI:31493 - Germany_Zone_3`
    * In the `Encoding`canvas, deactivate the `ns_hyd_discharge`, `Points:0`, `Points:1`, and `Points:2` fields
    * In the `Geometry` canvas, set the `Geometry type` to `Point` and active `Include z-dimension`
    * Check the `Extent (current: layer)` box
- Click `OK`

<a name="qgis-exp-sim-pts"></a>
{% include image.html file="qgis-exp-sim-pts.png" alt="bm-3" caption="The Save Vector Layer As... window with required settings highlighted (green marker)." %} 

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
   
<a name="qgis-make-tiff"></a>
{% include image.html file="qgis-make-tiff.png" alt="bmx3" caption="The Rasterize (Vector to Raster) window with required settings highlighted (green marker)." %}  
 
## Result interpretation
In *ParaView* (renders faster) or *QGIS*, look at all variables (`flow_velocity`, `water_depth`, and `water_surface`), explore their evolution over time, different coloring and answer the following questions:

- Are the results are in a physically reasonable and meaningful range?
- When did the simulation become stable?<br>*To save time, the simulation duration can be shortened (*BASEMENT*'s `SIMULATION` tab), down to the time step when stability was reached.*
- Are there particularities such as rapids that correspond (qualitatively) to field observations (are rapids on confinements and/or terrain drops)?
- Zoom into the [final *tif* raster](#qgis-crayfish-final) and have a look at the triangulation artifacts. The artifacts are not realistic. How can the problem be addressed?

## Other applications
After post-processing, the model still needs to be calibrated and validated ([see next part](bm-calibration.html)). Once the model is calibrated, it can be used to simulate flood hydrographs to assess the stability of river engineering features and the river landscape or inundation area. Moreover, the [habitat quality of rivers for target fish species](https://pubs.er.usgs.gov/publication/70121265) can be assessed as a function of water depth, flow velocity, and grain size (and other parameters). There is even special software to perform these tasks, such as [CASiMiR](http://www.casimir-software.de/ENG/index_eng.html) (commercial) or [River Architect](https://riverarchitect.github.io).