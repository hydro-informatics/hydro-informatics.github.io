```{admonition} Contributor
:class: tip
This chapter was written and developed by [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/) <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="50" height="50">
```

# Post-processing

Post-processing is a crucial step in understanding and analyzing the results of {term}`CFD` simulations, particularly for multiphase flow scenarios. This tutorial is designed to guide you through the essential steps of extracting meaningful insights from OpenFOAM simulations, emphasizing the visualization and analysis with ParaView (ParaFoam). On this page, you will learn how to efficiently use tools like ParaView to interpret simulation outcomes, manipulate and process OpenFOAM outputs.

`````{admonition} Visualization software: ParaView and alternatives
:class: tip

OpenFOAM post-processing can be accomplished with paraFoam, a software module that ships with OpenFOAM. ParaFOAM is a specialized version of ParaView configured to directly process OpenFOAM data files without additional plugins. ParaView is a general-purpose open-source visualization tool for analyzing and visualizing large datasets. ParaFOAM is tailored for OpenFOAM users with built-in compatibility, while ParaView requires additional steps to read OpenFOAM formats, but supports a wider range of data types and analysis pipelines.

To directly work with ParaView in lieu of paraFOAM, either run the `foamToVTK` utility provided by OpenFOAM to convert the simulation results into VTK-compatible files that ParaView can natively read, or use ParaView plugins. For instance, the **OpenFOAM Reader** plugin allows to load a `.foam` file (typically created in the simulation case directory by adding an empty file named `<case>.foam`) and ParaView will parse the case using the plugin.

Alternative software includes tools like [VisIt](https://visit-dav.github.io/visit-website/index.html), which provides similar visualization capabilities to ParaView. VisIt is also open-source visualization software and has an intuitive interface.

````{admonition} Enable VisIt for OpenFOAM
:class: note, dropdown

To use VisIt for analyzing OpenFOAM simulation output, follow these steps:

1. Download and install VisIt from https://visit-dav.github.io/visit-website/index.html (ensure you have the required system dependencies).

2. Since VisIt does not natively read OpenFOAM files, convert the simulation data into a format compatible with VisIt, such as VTK. To this end, use the `foamToVTK` utility provided by OpenFOAM:

   ```bash
   foamToVTK
   ```

   This will generate VTK files in a `VTK` directory within your simulation case folder.

3. To load data in VisIt, (open VisIt,) navigate to the `VTK` directory created by `foamToVTK`, and load the target VTK files. Select relevant fields such as velocity, pressure, or other quantities for visualization.

4. To explore data, use VisIt's visualization tools, such as slicing, contouring, vector field plotting, and temporal evolution visualization for dynamic simulations.

Customized analysis can be implemented by leveraging VisIt's scripting capabilities or using advanced filters to perform specific analyses, such as integrating flow quantities, exporting data, or visualizing complex interactions in your results.

````

`````

## Retrieve simulation data

In the case in which the simulations were run in parallel, before post-processing the data, the first step consists in reconstructing (i.e., reassembling) all solution steps of the analyzed case. This can either be done for all time steps or only for a specific one. The commands that need to be typed in the terminal window are shown below:

* To reconstruct all solution steps:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar
```
  
* To reconstruct a specific time step (substitute "x" with the time step):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar -time x
```

## Visualizatioin with ParaView (paraFoam)

ParaFoam is a customized version of the ParaView visualization software that comes pre-configured to read and process OpenFOAM simulation data directly. It simplifies post-processing by integrating OpenFOAM-specific file formats and functionalities, allowing users to visualize fields, extract insights, and analyze results without additional setup.

Working with paraFoam requires that the simulation case has been constructed (see above section). A simulation case refers to the complete set of files and configurations required to define, run, and analyze a specific simulation scenario. It includes the geometry and mesh of the computational domain, initial and boundary conditions, solver settings, physical models, and any additional parameters necessary for the simulation. The case is organized into directories such as `constant` (material properties and mesh), `system` (solver controls), and `0` (initial conditions), forming a structured framework for numerical experiments.

### Launch paraFoam

Once the case has been reconstructed, as for the meshing process, the following command can be used to visualize the case in the software ParaView:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ paraFoam
```

### Visualization pipelines

The *channel.OpenFOAM* should now be present in the Pipeline Browser and to visualize it in the layout, press the *Apply* button. Additionally, in the *Fields* section, the various fields that can be visualized are shown and can be selected/deselected according to the focus of the analysis.

```{figure} ../../img/openfoam/interFoam/Paraview/channelOpenFOAM.png
:alt: openfoam 
:name: of-channelOpenFOAM

Visualization of the case results in ParaView.
```

In order to visualize the air and water phases, *alpha.water* should then be selected in the drop-down menu as shown in the image below.

```{figure} ../../img/openfoam/interFoam/Paraview/view-alpha-water.png
:alt: openfoam 
:name: of-view-alphawater

Enabling the setting for viewing the air and water phases in ParaView.
```

To change the shown time step, the arrows that can be seen in the area highlighted in red can be used.


```{figure} ../../img/openfoam/interFoam/Paraview/final-time-step.png
:alt: openfoam timestep time step
:name: of-final-time-step

Options for changing the time step to be visualized.
```

Next, to visualize only the water phase, the *Clip* filter is used. This can either be found in the *Filters* section in the menu, or alternatively, the shortcut can be used. The *Clip Type* should be set to *Scalar*, selecting *alpha.water* as scalar and setting the value to 0.5, which represents the interface between air and water. To view the air phase, the *Invert* option should be selected whereas for the water phase it should be deselected.

```{figure} ../../img/openfoam/interFoam/Paraview/clip-water.png
:alt: openfoam clip water interFoam
:name: of-clip-water


Clip filter used for viewing the water phase in ParaView.
```

Finally, to also add the walls and patches to the view, the *Extract Block* filter can be implemented (click on the *channel.OpenFOAM* file before applying it).

```{figure} ../../img/openfoam/interFoam/Paraview/extract-block.png
:alt: openfoam 
:name: of-extract-block

List of filters available in ParaView, highlighting ExtractBlock.
```

The patches of interest can then be either selected or deselected, and the *Coloring* can be set to Solid Color.

```{figure} ../../img/openfoam/interFoam/Paraview/choose-patches.png
:alt: openfoam 
:name: of-choose-patches

Available options for selecting the patches and changing the color.
```

The resulting view of the water phase and block extraction is shown below:

```{figure} ../../img/openfoam/interFoam/Paraview/alpha-water.png
:alt: openfoam 
:name: of-alpha-water

Simulation results highlighting the water phase.
```

Different parameters can also be viewed, such as the flow velocity, and this can be done in the *Coloring* section by selecting *U*. The *preset* can be modified to better view the results by selecting the corresponding icon (highlighted in green).

```{figure} ../../img/openfoam/interFoam/Paraview/flow-velocity.png
:alt: openfoam 
:name: of-flow-velocity

Simulation results highlighting the flow velocity.
```

