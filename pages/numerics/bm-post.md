---
title: Post-Processing
keywords: numerics
summary: "Use ParaView and QGIS to visualize and analyze results."
sidebar: mydoc_sidebar
permalink: bm-post.html
folder: numerics
---

# Visualize results with ParaView
##	Get ready with ParaView
*ParaView* is a freely available visualization software, which enables plotting *BASEMENT* v.3.x results in the shape of `xdmf` (*eXtensible Data Model and Format*) files. Download and install the latest version of *ParaView* from their [website](https://www.paraview.org/download/), if no yet done. 

## Load BASEMENT results
Open *ParaView* and click on the folder icon (top left of the window) to open the simulation results file (`results.xdmf`). *ParaView* might ask to choose an appropriate XMDF read plugin. Select `XDMF Reader` here and click `OK`:
 
To explore the model results:
- Select variables (e.g., `flow_velocity`, `water_depth`, or `water_surface`) in *ParaView*'s `Cell Arrays` canvas (green-highlighted circle in the below [figure](#pv-vis)). 
- Click the `Apply` button (red-highlighted circle in the Properties tab in the below [figure](#pv-vis)). All variables are now loaded and can be plotted.
- To plot a variable, select one (e.g., `flow_velocity`) in the toolbar (light-blue-highlighted circle in the upper part of the below [figure](#pv-vis)). Then click the play button in the toolbar (dark-blue-highlighted circle around the green arrow in the upper part of the below [figure](#pv-vis)) to cycle through the time steps.
 
<a name="pv-vis"></a>
{% include image.html file="bm-sim-end.png" alt="bm-x3" caption="*ParaView* after successful import of the model results (`results.xdmf`) - see above descriptions." %} 

All available time steps are listed in the Blocks tab (bottom-left in Figure 1). Anything should be visible at the beginning, because the initial conditions were defined as `dry` (see the [*BASEMENT* modelling exercise part](bm-main.html#init) ). The above [figure](#pv-vis) shows the last time step (`Timestep[25]`), with water flowing at a peak velocity of 3.7 m/s. The 25 available time steps result from the definition made in *BASEMENT*'s `SIMULATION` tab with a total duration of 5000.0 and an output step of 200.0. Note that the time units have no dimension here because they correspond to computational time steps.

## Result interpretation
Look at all variables (`flow_velocity`, `water_depth`, and `water_surface`), explore their evolution over time, different coloring and answer the following questions:

- Are the results are in a physically reasonable and meaningful range?
- When did the simulation become stable?
→ To save time, the simulation duration can be shortened (*BASEMENT*'s `SIMULATION` tab), down to the time step when stability was reached.
- Are there particularities such as rapids that correspond (qualitatively) to field observations (are rapids on confinements and/or terrain drops)?


##	Export visualizations
The animations can be saved as movie (e.g., `avi`) or image (e.g., `jpg`, `png`, `tiff`) files via `File` > `Save Animation...`.
The current state (variable, `Timestep[i])` can be saved as `pvsm` file via `File` > `Save State File`. The state file can also be saved as Python script for external execution and implementation in [Python programs](hy-install.html).

# QGIS
in progress...
