(sec-geo-python)=
# Geospatial Python

Python is connected with several libraries providing many open-source and commercial (proprietary) functions for the analyses of geospatial data. This section introduces both, open-source and (briefly) the commercial `arcpy` library. The goal of this section is to provide an understanding of how geospatial data can be used and manipulated with Python code. The file manipulation involves logical and algebraic operations, and conversion from and to other geospatial file formats.

```{admonition} Requirements
:class: important

Make sure you understand the basics of Python, especially {ref}`var`, {ref}`sec-pyerror`, {ref}`chpt-functions`, and working with external {ref}`sec-pypckg`.
```

```{admonition} Maximize learning success
:class: tip

* Use the {{ ft_url }} package to facilitate working with the tutorials provided with this eBook.
* Understand {ref}`geospatial-data`, which are the underpinnings of any geospatial analysis.
* Use {ref}`qgis-install` to display geospatial data and to create maps in *PDF* or image formats (e.g., *tif*, *png*, *jpg*).
```

The descriptions of open source packages for geospatial data handling build on explanations from [Michael Diener's Python Geospatial Analysis Cookbook](https://github.com/mdiener21/python-geospatial-analysis-cookbook) (open access under MIT license). Therefore, if you want to learn more details about any here information provided, take a look at this comprehensive e-book.

Another excellent source of inspiration with many open-sourced examples is [*pcjericks* GitHub repository *py-gdalogr-cookbook*](https://pcjericks.github.io/py-gdalogr-cookbook/).

```{admonition} How to use PyQGIS (QGIS Python environment)
:class: tip, dropdown

To enable working with QGIS commands in standalone Python scripts through `from qgis.core import *`, have a look at the {ref}`PyQGIS section <pygis>` at the bottom of the QGIS tutorial in this eBook.
```
