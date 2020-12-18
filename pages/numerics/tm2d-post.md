---
title: Post-Processing of TELEMAC output
tags: [telemac, numerical, modelling, hydraulics, morphodynamics, raster, shapefile, qgis, morphodynamics, ecohydraulics]
keywords: numerics
summary: "Use ParaView and QGIS to visualize and analyze results."
sidebar: mydoc_sidebar
permalink: tm2d-post.html
folder: numerics
---

## Under construction. Expected release of this tutorial: Spring 2021.

Thank you for your patience.

{% include requirements.html content="Make sure that TELEMAC-MASCARET ran successfully as described on the [model setup & run page](tm-main.html) or use one of the example cases to explore results." %}

## Options

## Get ready with QGIS

### Install the PostTelemac plugin

Open QGIS' *Plugin Manager*, go to the *All* tab and type *posttelemac* in the search field. Click on the *Install* button to install the *PostTelemac* plugin.

{% include image.html file="qgis-plugin-manager.png"%}

{% include image.html file="qgis-plugin-install-posttm.png"%}

After the successful installation, click the *Close* button. The *PostTelemac* symbol should now be visible in the QGIS menu bar.

### Open the PostTelemac plugin

Find the *PostTelemac* icon in the menu bar to open the plugin. By default, the plugin window will most likely open up in the bottom-right corner of the QGIS window. For better handling, click the *detach* symbol and enlarge the detached plugin window. 

{% include image.html file="posttm-display.png" caption="The detached window of the PostTelemac plugin with the Display tab opened to render simulation variables such as VELOCITY U/V, VITESSE (principal absolute U-V velocity) or DEPTH." %}

{% include image.html file="posttm-tools.png" caption="The detached window of the PostTelemac plugin with the Tools tab opened (e.g., to create shapefiles or GeoTIFF rasters)." %}
