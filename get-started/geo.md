(chpt-geo-software)=
# Geospatial Software

Geospatial analyses (or analytics) use, manipulate, and illustrate data from geographic information systems (GIS). GIS data contain geographically referenced and spatially explicit information of for example gauging stations, terrain elevation, or land use. Efficient processing of geospatial data involves programming methods, where *Python* is an efficient tool. This page presents desktop software for manual geospatial analyses and the illustration of geospatial data. For geospatial programming, please refer to the {ref}`sec-geo-python` chapter.

(qgis-install)=
## QGIS
For the visualization of geodata (`.shp` and `.tif` files), GIS software is required and the analyses described on these pages refer to the usage of [QGIS](https://www.qgis.org). This eBook uses QGIS within the sections on {doc}`geospatial programming with *Python* <geo-python>` and numerical modelling with the ETH Zurich's {doc}`BASEMENT <../numerics/basement>` software.

### Install QGIS on Windows
Download and install the latest version of [QGIS](https://www.qgis.org/en/site/forusers/download.html) for Windows.

### Install QGIS on Linux (via Flatpak)

The QGIS developers provide detailed installation instructions for several *Linux* distributions, but the instructions will not satisfy all requirements for the use of QGIS described in this eBook. One of the most functional ways for installing QGIS on *Linux* is to use [*Flatpak*](https://flathub.org/apps/details/org.qgis.qgis), which requires some system preparation. On *Debian*-based *Linux* platforms (e.g., all sorts of *Ubuntu* such as *Lubuntu* or *Mint*) open *Terminal* and tap (the second line is only needed if you use *GNOME*):

```
sudo apt install flatpak
sudo apt install gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

Restart the system and open the *Software Manager* app. It will update and add the flathub repo. Once the update was successful, search for QGIS and click *Install* (patience - the installation may take a while).

The *QGIS Flatpak* installation will most likely not include the important *scipy* module. To fix this issue, open  *Terminal* (standard Linux application) and type:
<br>`flatpak run --command=pip3 org.qgis.qgis install scipy --user`

This solution has been tested on *Linux Ubuntu* and *Linux Mint*. It potentially also works with *Red Hat*, *openSUSE*, *Mac OS*, *Arch*, *Fedora*, *Android*, *Debian*, *Kubuntu* and many more (read installation guides on the [maintainer's website](https://flatpak.org/setup/)). Read more about the *QGIS Flatpak* installation on the [QGIS website](https://qgis.org/en/site/forusers/alldownloads.html#flatpak).


### Install QGIS on macOS

```{admonition} macOS and BASEMENT
:class: attention
If you plan to use BASEMENT for numerical modeling: BASEMENT will not run on macOS.
```

Download and install the latest version of [QGIS](https://www.qgis.org/en/site/forusers/download.html) for macOS. The integrity of using macOS for the applications in this ebook has not yet been tested. Possible troubleshooting with *Python* is provided, for instance, by [kyngchaos.com](https://www.kyngchaos.com/software/qgis/).

### Learn QGIS
Working with geospatial data editors involves complex tasks that require background knowledge before intuitive comprehension is possible. The QGIS developers provide compound [tutorials on their website](https://docs.qgis.org/testing/en/docs/training_manual/index.html) ([also available in other languages including Czech, French, German, and Portuguese](https://www.qgis.org/en/site/forusers/trainingmaterial/index.html)).
This eBook occasionally uses QGIS for plotting and creating georeferenced data (e.g., the chapters on {ref}`sec-geo-python` and {ref}`numerical modeling <qgis-prepro-bm>`). To this end, this eBook comes along with a tutorial on geospatial analyses with QGIS (read and do the {ref}`qgis-tutorial`).

(qgis-conda-install)=
### Install QGIS conda Environment

In [*Anaconda Prompt*](../get-started/ide.html#anaconda), you can create a new environment to specifically use QGIS features (i.e., tools and scripts) including its raster calculator. The environment is featured by *Open Data Cube* ([read more](https://datacube-qgis.readthedocs.io/en/latest/installation.html) and can be installed as follows:

```
conda create  -c conda-forge -n qgiscube python=3.6 qgis=3 datacube
conda activate qgiscube
```

(agis)=
## ArcGIS Pro

```{admonition} Windows only
:class: attention
ArcGIS Pro is designed for Windows and will not run on macOS or Linux. In addition, a license needs to be purchased.
```

The proprietary software *ArcGIS Pro* represents a powerful tool for any kind of geospatial analysis including web applications. *ArcGIS Pro* is maintained by [esri](https://www.esri.com/) and comes with an own {ref}`conda-env`. With this eBook's focus on freely available software, the usage of *ArcGIS Pro* and its *Python* environment including the `arcpy` package is just mentioned on this website.

(others)=
## Others
There are many other tools for geospatial analyses, which all deserve much more than just being mentioned here. Alas, for practical reasons, this website focuses on the usage of QGIS. This is why there is just an absolutely-not-complete list of other GIS tools here:

* [SAGA (System for Automated Geoscientific Analyses)](http://www.saga-gis.org/en/index.html)
* [Mapline](https://mapline.com/)
* [Mapbox](https://www.mapbox.com/)
* [uDig](http://udig.refractions.net/)

## Geospatial Analyses

Geospatial analyses involve efficient code practices (e.g., with *Python*) and this is why detailed descriptions of geospatial data handling are embedded in the {ref}`sec-geo-python` chapter of this eBook.
