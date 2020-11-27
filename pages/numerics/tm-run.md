---
title: Run open TELEMAC
tags: [telemac, numerical, modelling, hydraulics, morphodynamics]
keywords: numerics
summary: "Start a TELEMAC simulation."
sidebar: mydoc_sidebar
permalink: tm-run.html
folder: numerics
---

## Under construction. Expected release of this tutorial: Spring 2021.

Thank you for your patience.

{% include requirements.html content="Make sure that TELEMAC is correctly installed and that simulation files are prepared in line with the [pre-processing instructions](tm2d-pre.html)." %}

## Load environment and files

Load the TELEMAC *Python* variables: 

```
cd ~/telemac/v8p1/configs
source pysource.openmpi.sh
config.py
```


***

## Start a 2D hydrodynamic simulation

To start a simulation, `cd` to the directory where the simulation files live (see previous page) and launch the steering file (*cas*) with *telemac2d.py*: 

```
cd /go/to/dir
telemac2d.py run_2dhydrodynamic.cas
```

Next:
* [> Post-processing of results (2D) >](tm2d-post.html)
* [> Post-processing of results (3D) >](tm3d-post.html)
