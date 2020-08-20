---
title: Debugging numerical models
tags: [basement, troubleshooting, numerical, modelling, hydraulics, morphodynamics]
keywords: basement, numerical modelling
sidebar: mydoc_sidebar
permalink: dbg_nm.html
folder: troubleshooting
---

Setting up a numerical model implemented in commercial or non-commercial codes may cause a lot of headache. This page features some basic principles to avoid problems with numerical models.


## Five widespead problems

Erik Mosselmann and Thai Binh Le highlight five widespread and common problems in the creation and interpretation of numerical models ([Mosselmann and Le 2016](https://doi.org/10.1016/j.advwatres.2015.07.025)). These five mistakes are:

1. Preparation: One-dimensional (1D), two-dimensional (2D), and three-dimensional (3D) models require similar input data (flow series, stage-discharge relation, roughness, digital elevation model, grain sizes). What varies are the computation (3D > 2D > 1D) and the calibration (1D > 2D > 3D) efforts.
1. Grid setup: The model boundaries need to be in adequate distance to the area of interest. An inflow boundary should only be along the permanently wetted riverbed and the most upstream 1-2% of the modelled channel bed should have a non-erosive constraint assigned to the cells. Otherwise, the model may be unstable because of locally very high velocity and erosion rates close to the inflow boundary.
1. Model setup: Read and understand how turbulence closures are implemented in the model to set the model parameters used for the turbulence closure realistically and yield a stable model.
1. Model validation / post-processing: Wrong confidence in poorly validated numerical models: Every model requires validation data, which involve exhausting and labor-intensive fieldwork.
1. Model interpretation: The direction of sediment transport and water flow vectors mostly differ.
