---
title: Post-Processing of TELEMAC output
tags: [telemac, numerical, modelling, hydraulics, morphodynamics, raster, shapefile, qgis, morphodynamics, ecohydraulics]
keywords: numerics
summary: "Use ParaView and QGIS to visualize and analyze results."
sidebar: mydoc_sidebar
permalink: tm3d-post.html
folder: numerics
---

## Under construction. Expected release of this tutorial: Fall 2021.

Thank you for your patience.

{% include requirements.html content="Make sure that *ParaView* is installed ([read instructions](install-telemac.html#paraview)." %}

## Post-processing

### Launch *ParaView*

Start *ParaView* through *SALOME-HYDRO*, in *Terminal*:

* `cd` to the directory where *SALOME-HYDRO* is installed,
* launch the environment, and
* launch *ParaView*.

For example:

```
cd /home/slome-hydro/appli_V1_1_univ/
. env.d/envProducts.sh
./runRemote.sh paraview
``` 

{% include note.html content="Alternatively, launch an independent installation of *ParaView* on *Windows* or *Linux*, and make sure that *MED* coupling is enabled [read more on the installation page](install-telemac.html#paraview))." %}
 
