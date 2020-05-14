---
title: Run BASEMENT
keywords: numerics
summary: "Set up BASEplane for 2D modelling of rivers."
sidebar: mydoc_sidebar
permalink: bm-main.html
folder: numerics
---

This exercise uses *BASEMENT*'s *BASEplane* module (version 3.0.2) to perform a two-dimensional (2D) hydrodynamic numerical simulation. *BASEMENT* is developed and maintained at the [ETH Zurich](https://ethz.ch/en.html) (Switzerland). To download the program, detailed installation instructions and program documentation, visit the  [*BASEMENT* website](https://basement.ethz.ch/).

## Steady State 2D Simulation with BASEMENT {#bm-intro}
With the 2D mesh ([see generation of the `.2dm` file](#bm-pre.html)) this exercise guides through the setup of a steady-flow, hydrodynamic simulation in *BASEMENT* v.3. The numerical engine of *BASEMENT* needs a model setup file (*model.json*) and a simulation file (*simulation.json*), which both are created automatically by *BASEMENT*. The following sections describe how to make *BASEMENT* creating the two *.json* files. Before getting there, create a new project folder of your choice (e.g., `C:/BM/irme-exercise/`). 

{% include tip.html content="The defined project folder directory must not contain any dots nor special characters nor spaces. Only use letters, numbers, *_* (underscore) or *-* (minus) for folder names." %} 

Then, make sure to place the two required input files in the folder: 

- The 2D mesh `.2dm` file (i.e., the *finalmesh.2d* from the [pre-processing](bm-pre.html)).
- The provided discharge inflow file (flat hydrograph) as upstream boundary condition can be downloaded [here](https://github.com/hydro-informatics/materials/blob/master/numerics/SteadyVanillaInflow.txt) (if necessary, copy the file contents locally into a text editor and save the file as `SteadyVanillaInflow.txt` in the local project directory).


##	Setup the model file in *BASEMENT* v.3.x (Define Scenario Parameters)
This section walks you through the model setup of a hydrodynamic 2D *BASEMENT* simulation. The model setup is saved in a file called model.json. 

Regularly save setting by clicking on the `Write` button (bottom-right corner).
- Open *BASEMENT* and select the Scenario Directory. Then click on `SETUP`, right-click and `Add DOMAIN`. 
- Use the average elevation of each mesh triangle: `GEOMETRY` > `Add item` > `Interpolation` > select WEIGHTED (other options: MEDIAN, MAXIMUM, MINIMUM, MEAN).
- `GEOMETRY` > `MESH_FILE` > select `finalmesh.2dm`.
- `GEOMETRY` > right-click > `Add item REGIONDEF` > `Add item` (5 times) and define the items as:

| INDEX | 1        | 2          | 3          | 4          | 5      |
|-------|----------|------------|------------|------------|--------|
| NAME  | riverbed | lower_bank | upper_bank | floodplain | street |

The window should now look like this:
<a name="bm-mod-reg"></a>
{% include image.html file="bm-mod-reg.png" alt="bm-7" caption="Region definitions." %} 
 
- Next, we need to define inflow and outflow boundary condition with `stringdefs`. In the `GEOMETRY` section right-click – `Add item` `STRINGDEF` – `Add item` (2 times) and define item [0] as:
    * `name` = `Inflow`
    * `upstream_direction` = `right`
- Define `STRINGDEF` item [1] as:
    * `name` = `Outflow`
    * `upstream_direction` = `right` 
    {% include note.html content="If you used [BASEmesh’s *Stringdef* tool](bm-pre.html#stringdef), the upstream direction must be defined as `right`." %}
- Add the initial condition in the `HYDRAULICS` section with by right-clicking > `Add item` > `INITIAL` (if not yet present) and set `type`: “DRY” (i.e., the river is dry at the beginning of the simulation).<a name="init"></a>
- Add upstream and downstream boundary conditions with a right-click on the `HYDRAULICS` section > `Add item` > `BOUNDARY` (if not yet present), then right-click on the new `BOUNDARY` section > `Add item STANDARD` > `Add item` (2 times) 
- Define BOUNDARY item [0] as:<a name="bound"></a>
    * `discharge_file` = `C:/.../SteadyVanillaInflow.txt` (select by clicking on the folder symbol that occurs when the field is activated)
    * `name` = `Inflow`
    * `slope` = 0.0056
    * `string_name` = `Inflow`
    * `type` = uniform_n`
- Define BOUNDARY item [1] as:
    * `name` = `Outflow`
    * `type` = `zero_gradient_out` (note: this is not a good choice in practice, where a [stage-discharge relation or rating curve](https://en.wikipedia.org/wiki/Rating_curve) should be used for the downstream boundary condition)
- Define a global [*Strickler*](https://en.wikipedia.org/wiki/Manning_formula)-based friction value of *k<sub>st</sub>*=30m<sup>1/3</sup>/s: In the `HYDRAULICS` section right-click > `Add item FRICTION` and define `FRICTION` with:
    * `default_friction` = 30.0
    * `type` = `strickler`
- Assign particular [*Strickler*](https://en.wikipedia.org/wiki/Manning_formula) values with a right-click on `regions` and `Add item` (5 times). Then define the five regions items ([0] through [4]) as <a name="fric"></a>

| `friction`  | 28       | 15         | 20         | 40         | 85     |
|-------------|----------|------------|------------|------------|--------|
|`region_name`| riverbed | lower_bank | upper_bank | floodplain | street |

<a name="bm-mod-frc"></a>
{% include image.html file="bm-mod-frc.png" alt="bm-x4" caption="Assignment of friction (roughness) values to model regions." %}  

- In the `PARAMETER` section define:
    * `CFL` = `0.95`
    * `fluid_density` = `1000.0`
    * `max_time_step` = `100.0`
    * `minimum_water_depth` =` 0.01`
- Define a `simulation_name` (e.g., `SteadyVanilla`)

Note that the definitions of `PHYSICAL_PROPERTIES` and `BASEPLANE_2D` are mandatory.
Click on the `Write` button (bottom-right corner) to save the model setup (see image below). If everything is correctly set up, the `Console` tab will automatically open and the `Error Output` canvas is empty.
 
<a name="bm-mod-sum"></a>
{% include image.html file="bm-mod-sum.png" alt="bm-x3" caption="Final model setup" %} 

##	Setup the simulation file BASEMENT v.3.x
The simulation file in *BASEMENT* v.3.x is called simulation.json and located in the same folder as model.json (model setup file). To setup the simulation file:
- In *BASEMENT* go to the `SIMULATION` Tab (situated in left window pane) and unfold the `OUTPUT` and `TIME` items. 
- Right-click on the `OUTPUT` item an `Add item` (5 times). Then define exactly in that irder (important for results export later on):
    * [0] = `water_depth`
    * [1] = `water_surface`
    * [2] = `bottom_elevation`
    * [3] = `flow_velocity`
    * [4] = `ns_hyd_discharge`
- Define the TIME item as:
    * `end` = `5000.0`
    * `out` = `200.0`
    * `start` = `0.0`
The *BASEMENT* window should now look like this:
 
<a name="bm-sim-set"></a>
{% include image.html file="bm-sim-set.png" alt="bm-x3" caption="The Simulation tab setup. In order to export results with *BASEMENT*’s Python scripts, the OUTPUT parameters must be defined in exactly that order." %} 

##	Run the simulation
After the successful simulation setup, select an appropriate `Number of CPU cores` (bottom-right in the above figure). If a high-quality graphics card with a powerful GPU is available, the GPU (high-performance hardware) has a much faster performance. Otherwise (no powerful GPU available), do not select GPU because it may significantly slow down the simulation speed.
For faster simulations, select `Single` precision (bottom-right in the above figure), but in this example, `Double` precision will work sufficiently fast as well. Click on the `Run` button to start the simulation and wait for approximately 2-10 minutes. *BASEMENT* will prompt the simulation progress, while the `Error Output` canvas should remain white (see below [figure](#bm-sim-end)). If any error occurs, go back to the above sections (or even to the mesh generation) and fix error message issues.

<a name="bm-sim-end"></a>
{% include image.html file="bm-sim-end.png" alt="bm-x3" caption="*BASEMENT* after successful simulation." %} 

## Export results
Once the simulation successfully finished, go to *BASEMENT*'s `Results` tab and make sure that the `xdmf` output format is defined. Then click on the `Export` button (see also below [figure](#bm-res-exp)). *BASEMENT* will inform about the export success.

<a name="bm-res-exp"></a>
{% include image.html file="bm-res-exp.png" alt="bm-x3" caption="Export results after successful simulation." %} 

To visualize the results, use ParaView (see the [next part of the exercise](bm-post.html)). 

*BASEMENT*’s developers at the ETH Zurich provide a suite of [Python scripts](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/) for post-processing the simulation results. Here, we need the Python script [`BMv3NodestringResults.py`](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/BMv3NodestringResults.py) ([click to download](ttp://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/BMv3NodestringResults.py)).  
 To run the Python script, a Python3 installation with the `numpy` and `h5py` packages is required. To learn more about the installation and usage of Python, have a look at the [instructions on this website to install Python](hy_install.html).
Note that working with the provided Python file requires that the output variables must be exactly defined as shown in the above [figure](#bm-sim-set) of *BASEMENT*’s `SIMULATION` tab.
 

