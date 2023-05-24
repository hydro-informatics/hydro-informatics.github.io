```{admonition} Contributor
:class: tip
This chapter was written and developed by {{ scolari }} <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="50" height="50">
```

# Post-processing

In the case in which the simulations were run in parallel, before post-processing the data, the first step consists in reconstructing (i.e., reassembling) all solution steps of the analyzed case. This can either be done for all time steps or only for a specific one. The commands that need to be typed in the terminal window are shown below:

* To reconstruct all solution steps:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar
```
  
* To reconstruct a specific time step (substitute "x" with the time step):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar -time x
```

Once the case has been reconstructed, as for the meshing process, the following command should be used to visualize the case in the software ParaView:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ paraFoam
```

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

