
(gaia-run)=
# Run and Analyze

## Run Gaia

Make sure that the simulation folder (e.g., `/gaia2d-tutorial/`) contains at least the following files (or similar, depending on the simulation case):

* A computational mesh, for example, in the form of [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* A hydrodynamic boundary definitions, for example, in the form of [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* A Gaia boundary definitions, for example, in the form of [boundaries-gaia.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries-gaia.cli).
* A results file of a Telemac2d/3d simulation for a hotstart initialization, for example, for 35 m$^3$/s in the form of [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) (result of the {ref}`dry-initialized steady run <tm2d-dry>` ending at `T=15000`).
* A Telemac2d steering file, such as [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* A Gaia steering file, such as [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).

With these files available, open *Terminal*, go to the TELEMAC configuration folder (e.g., `~/telemac/v8p2/configs/`), and launch the environment (e.g., `pysource.openmpi.sh` - use the same as for compiling TELEMAC).

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

With the TELEMAC environment loaded, change to the directory where the TELEMAC Gaia simulation lives (e.g., `/home/telemac/v8p2/mysimulations/gaia2d-tutorial/`) and run the `*.cas` file by calling the **telemac2d.py** script (it will automatically know that it needs to use Gaia when it reads the line containing `COUPLING WITH : 'GAIA'`).

```
cd ~/telemac/v8p2/mysimulations/gaia2d-tutorial/
telemac2d.py steady2d-gaia.cas
```

````{admonition} Speed up
With {ref}`parallelism <mpi>` enabled (e.g., in the {ref}`Mint Hyfo Virtual Machine <hyfo-vm>`), speed up the calculation by using multiple CPUs through the `--ncsize=N` flag. For instance, the following line runs the unsteady simulation on `N=4` CPUs:

```
telemac2d.py steady2d-gaia.cas --ncsize=4
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
                             1  HOURS
                             4  MINUTES
                            34  SECONDS
... merging separated result files

... handling result files
       moving: r2dsteady-gaia.slf
       moving: rGaia-steady2d.slf
       moving: r-control-sections.txt
... deleting working dir

My work is done
```

TELEMAC will write the files *r2dsteady-gaia.slf*, *rGaia-steady2d.slf*, and *r-control-sections.txt*. The result files are also available in this eBook's modeling repository for accomplishing the post-processing tutorial:

* [Download r2dunsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady-gaia.slf),
* [Download rGaia-steady2d.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/rGaia-steady2d.slf), and
* [Download r-control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/rGaia-steady2d.txt).

## Post-processing in QGIS

### Control Section Fluxes

The {ref}`control sections <tm-control-sections>` enable insights into the correct adaptation of the flow at the upstream and downstream boundaries (prescribed Q only). {numref}`Figure %s <gaia-hydrograph>` shows the modeled flow rates where the *Inflow_boundary* and *Outflow_boundary* curves converge after. Note that the graph shows absolute numbers (inflow is negative according to the flow direction definition in *control-sections.txt*). The {ref}`hotstart  <gaia-hotstart>` initialization makes that the fluxes correspond to the prescribed 35 m$^{3}$/s, but some variations are visible at the beginning and toward the end of the simulation. The slight increase toward the end of the simulation might be attributed to sediment transport and the free flux downstream boundary type (`544-4`).

```{figure} ../img/telemac/gaia-hydrograph.png
:alt: result flow discharge telemac2d morphodynamic gaia inflow outflow control sections
:name: gaia-hydrograph

The simulated flows over the upstream *Inflow_boundary* and the downstream *Outflow_boundary* control sections.
```

```{admonition} How to ensure that water volume fluxes are the same at the inflow and outflow control sections?
With the two {ref}`boundary files for Telemac2d and Gaia <gaia-bc>`, it is possible to use different boundary types for hydrodynamics and morphodynamics. Thus, to ensure that water volume fluxes are the same at the inflow and the outflow boundaries, prescribe `455` types (prescribed Q only) also at the outflow boundary in the hydrodynamics boundary file (*boundaries.cli*). Adapt the **PRESCRIBED FLOWRATES** keyword accordingly to `35.;35` in the hydrodynamics steering file (*steady2d-gaia.cas*). However, do not change the morphodynamics boundaries and steering files.
```

### Visualization with QGIS

The results of the Gaia simulation can be visualized and time snapshots exported to raster (e.g., {term}`GeoTIFF`) or shapefile formats in QGIS with the PostTelemac plugin the same way as explained in the {ref}`steady2d tutorial <tm2d-post-export>`. The latest QGIS releases additionally enable to load the Selafin results mesh file (here: *r2dsteady-gaia.slf*) as a QGIS mesh layer, which can then be exported to a video with the Crayfish plugin. To this end, **launch QGIS**, set the {ref}`project CRS <qgis-project>` to **EPSG:25833** (ETRS89 / UTM zone 33N), and save the new project in the `gaia2d-tutorial/` folder (or where ever the Gaia simulation files live). In QGIS' **Browser** panel, fine the **Project Home** folder, expand it and drag-and-drop the two simulation results meshes (*r2dsteady-gaia.slf* and *rGaia-steady2d.slf*) to the **Layers** panel.

Double click on either *r2dsteady-gaia.slf* or *rGaia-steady2d.slf* to open their **Mesh Layer Properties**, then go to the **Source** tab to toggle hydrodynamic (e.g., *water depth* or *scalar flowrate m2s*) or morphodynamic Gaia (e.g., *qs bedload kg(ms)*) simulation parameters at different timesteps. {numref}`Figure %s <qgis-gaia-mesh-properties>` shows the QGIS mesh Layer Properties window of the *rGaia-steady2d.slf* simulation results geometry where red boxes highlight steps for toggling output variables and visualization timesteps. In addition, the **Symbology** tab provides options for value color scales or vector representations (e.g., useful for velocity).

```{figure} ../img/telemac/qgis-gaia-mesh-properties.png
:alt: qgis telemac2d gaia morphodynamics solid discharge bedload results slf
:name: qgis-gaia-mesh-properties

The mesh Layer Properties window with the Source tab for selecting Gaia output variables. The plot color ranges can be adapted in the Symbology tab.
```

Note that only parameters set with the **VARIABLES FOR GRAPHIC PRINTOUTS** keywords in the hydrodynamic ({ref}`steady2d-gaia.cas <tm2d-gen>`) and morphodynamic ({ref}`gaia-morphodynamics.cas <gaia-gen>`) steering files can be plotted in QGIS.

To export a video of the simulation results, use the *Crayfish* plugin:

* In QGIS, make sure the Crayfish plugin is installed (recall the {ref}`QGIS instructions <qgis-tbx-install>`).
* In the **Layer** panel, select **rGaia-steady2d** (or *r2dsteady-gaia*).
* With *rGaia-steady2d* (or *r2dsteady-gaia*) selected, go to **Mesh** (top dropdown menu) > **Crayfish** > **Export Animation ...** (if the layer is not highlighted, an error message pops up: *Please select a Mesh Layer for export*).
* In the **Export Animation** window, go to the **General** tab and define an output file name by clicking on the **...** button (e.g., `velocity-video.avi`).
* Optionally adapt the *Layout* and *Video* format.
* Click **OK** to start the video export.

The first time that a video is exported, Crayfish will require the definition of an **FFmpeg video encoder** and guide through the installation (if required). Follow the instructions and re-start exporting the video. The following video was exported with Crayfish and show velocity vectors:

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/jFgwiAsElH0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Note how the velocity vectors evolve over time and that the highest velocities occur at the bottom ramps (e.g., the two transversal maxima close to the upstream boundary or the transversal maximum close to the downstream boundary). Accordingly, the bedload transport at the bottom ramps should also be pronounced. The following video shows whether the model got the connection between flow velocity and bedload in the steady simulation right.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/BUaqvWZ_AVk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

After watching the video, it can be concluded that the relationship between flow velocities and bedload is approximately correct, but also that the model still requires some corrections. While the wagging sediment tail near the upstream boundary area maybe well represented, the short-term and sudden sediment transport peaks, especially in curves, may require adaptions of {ref}`magnitude and direction parameters <gaia-dir>`.


(bl-plausability)=
## Plausibility

The above-presented results feature steady-state bedload and suspended load transport in an armored riverbed at a low baseflow discharge of 35 m$^{3}$/s. The comparison of the flow velocity and the bedload transport videos has already given an insight into the plausibility, or the physical meaningfulness of the model. Considering additionally that no change of the riverbed elevation is modeled despite the local bedload transport peaks, the model created can be assumed to be basically physically reasonable. Why is that in particular?

The three sediment size classes were defined in the {ref}`Basic Setup of Gaia <gaia-sed>` with average grain diameters of 0.0005 m, 0.02 m, and 0.1 m. The simulation predicts that only the finest grain size class will move at baseflow. The fine sediment class of 0.5-mm diameters (sand) is transported in the form of bedload and in suspension with no measurable effect on bed elevation. Yet, the little export of fine sediment reflects in the above-shown flux comparison graph across the control sections ({numref}`Fig. %s <gaia-hydrograph>`). Still, to verify the physical plausibility of a morphodynamic model, higher (flood) discharges should be test-simulated. Then the coarser grain sizes of 0.02 m (gravel) and 0.1 m (cobble) should also move.

```{admonition} A physical plausibility check is not a model validation
The physical plausibility check serves for verification if the simulation results are physically sound. Physically non-meaningful results would be, for instance, when the water depth permanently increases in a steady simulation, when water flows over floodplains at baseflow or leaves the model at undefined boundary nodes, or when no sediment moves at a (100-years flood) high discharge over an alluvial riverbed. The model validation comes after the calibration (see next section).
```

Since Gaia modifies riverbed elevations, water depth, flow velocity (vectors), and {term}`Topographic change` should also be analyzed (in QGIS or BlueKenue). For instance, if the model predicts {term}`Topographic change` in the form of 10-m deep erosion (scour) at baseflow, the keyword definitions for the {ref}`riverbed <gaia-active-lyr>` should be revised. Likewise, hydro-morphodynamically relevant parameters should all be checked considering the significance of the simulated discharge and, if necessary, TELEMAC keywords should be adjusted. Beyond keyword adaptions in the steering file(s), adjustments may also be necessary in the boundary condition (`*.cli`) files regarding the {ref}`boundary type <gaia-bc>`.

Once the model is approximately physically meaningful, the model can be {ref}`calibrated <bl-calibration>` with observation data. The next section provides a list of keywords that may be used for calibrating {term}`Bedload` and/or {term}`Suspended load` simulations with Gaia.


(bl-calibration)=
## Calibration

```{dropdown} Recall: How to calibrate?
Calibration involves the step-wise adaptation of model input parameters to yield a possibly best stochastic fit of modeled and measured data. In the process of model calibration, only one parameter should be modified at a time by 10 to 20-% deviations from its default value. For instance, if the default is `BETA : 1.3`, the calibration may test for `BETA : 1.2`, then `BETA : 1.1` and so on, ultimately to find out which value for **BETA** brings the model results closest to observations.

Moreover, a sensitivity analysis compares step-wise modifications of multiple parameters (still: one at a time) and theirs effect on model results. For instance, if a 10-% variation of **BETA** yields a 5-% change in global water depth while a 10-% variation of a friction coefficient yields a 20-% change in global water depth, it may be concluded that the model sensitivity with respect to the friction coefficient is higher than with respect to **BETA**. However, such conclusions require careful considerations in multi-parametric, complex models of river ecosystems.
```

This section assumes that the model is already hydrodynamically calibrated (e.g., regarding friction), for instance, as described in the {ref}`steady modeling section <tm2d-calibration>`. Gaia can then be used to model a flood hydrograph with an {ref}`unsteady (quasi-steady) simulation <chpt-unsteady>`. The calibration requires that riverbed elevation measurements from before and after the flood are available (i.e., an event-specific {term}`Topographic change` map).

### Bedload Calibration Parameters
The following list of parameters can be considered for calibrating bedload in Gaia:

* Representative roughness length $k'_{s}$ (cf. Equation {eq}`eq-cf-skin`) with the keyword **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER** $f_{k'_{s}}$ (default: $f_{k'_{s}}$=`3.`). Note that this keyword is a multiplier of the characteristic grain size $D_{50}$; thus: $k'_{s}= f_{k'_{s}} \cdot D_{50}$ (goes into Equation {eq}`eq-cf-skin`)
  * To use this calibration parameter, make sure that `SKIN FRICTION CORRECTION : 1`.
  * On dune-form sand riverbeds, start with $f_{k'_{s}}$=`37.` {cite:p}`mendoza2017`.
  * In alternating bar riverbeds, start with $f_{k'_{s}}$=`3.6` {cite:p}`mendoza2017`.
* For models based on the {ref}`Meyer-Peter and Müller <gaia-mpm>` formula (i.e., using a {term}`Shields parameter` for incipient sediment motion), the **SHIELDS PARAMETERS** keyword may be modified:
  * If erosion is overpredicted, increase **SHIELDS PARAMETERS**.
  * If erosion is underestimated, reduce **SHIELDS PARAMETERS**.
* With slope correction enabled and using the {cite:t}`koch1980` correction formulae, adapt the **BETA** keyword from Equation {eq}`eq-qb-corr` (default is `BETA :  1.3`).
  * If erosion in curved channel sections is overpredicted, decrease **BETA**.
  * If erosion in curved channel sections is underpredicted, increase **BETA**.
* To adjust deposition and erosion pattern in curves (riverbends), enable the **SECONDARY CURRENTS** keyword and modify the **SECONDARY CURRENTS ALPHA COEFFICIENT** value (cf. {ref}`Secondary Currents <gaia-secondary>`).

### Suspended Load Calibration Parameters

The following list of parameters can be considered for calibrating suspended load transport and deposition-erosion pattern in Gaia:

* {ref}`**CLASSES SETTLING VELOCITIES** <gaia-sl-sed>`:
  - Reduce to enhance transport length and reduce deposition rates
  - Increase to shorten transport trajectories and enhance deposition
* {ref}`**CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION** <gaia-sl-sed>`: Reduce to keep sediment in suspension (or vice versa).

**What next?**
: The calibrated model will also require validation. The validation requires another set of riverbed elevation measurements from before and after another flood (i.e., an additional event-specific {term}`Topographic change` map). Alas, {term}`Topographic change` maps are expensive and  it is rare to have at least three {term}`DEM`s from different points in time for a river section, which would enable the creation of two {term}`Topographic change` maps. For this reason, the calibration dataset is often split in practice. For instance, 2/3 of a {term}`Topographic change` map may be used for model calibration and 1/3 for model validation. However, such splitting makes that the two datasets are not statistically independent and the validation quality figures will be biased.
