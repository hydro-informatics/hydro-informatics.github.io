---
description: Einführung in die geospatiale Python-Programmierung für die Hydrologie, die Open-Source- und kommerzielle Bibliotheken, die Manipulation von Raster- und Vektordaten und die Konvertierung von Geodaten umfasst.
---

(sec-geo-python)=
# Geospatial Python

Python is connected with several libraries providing many open-source and commercial (proprietary) functions for the analyses of geospatial data. This section introduces both, open-source and (briefly) the commercial `arcpy` library. The goal of this section is to provide an understanding of how geospatial data can be used and manipulated with Python code. The file manipulation involves logical and algebraic operations, and conversion from and to other geospatial file formats.

```{admonition} Requirements
:class: important

Stellen Sie sicher, dass Sie die Grundlagen von Python verstehen, insbesondere {ref}`var`, {ref}`sec-pyerror`, {ref}`chpt-functions` und arbeiten Sie mit externen {ref}`sec-pypckg`.
```

```{admonition} Maximize learning success
:class: tip

* Verwenden Sie das Paket [flusstools](https://flusstools.readthedocs.io)], um die Arbeit mit den mit diesem eBook bereitgestellten Tutorials zu erleichtern.
* Understand {ref}`geospatial-data`, which are the underpinnings of any geospatial analysis.
* Verwenden Sie {ref}`qgis-install`, um Geodaten anzuzeigen und Karten in *PDF* oder Bildformaten zu erstellen (z. B. *tif*, *png*, *jpg*).
```

Die Beschreibungen von Open-Source-Paketen für die Verarbeitung von Geodaten basieren auf Erklärungen von [Michael Dieners Python Geospatial Analysis Cookbook](https://github.com/mdiener21/python-geospatial-analysis-cookbook) (Open Access unter MIT-Lizenz). Wenn Sie daher weitere Details zu den hier bereitgestellten Informationen erfahren möchten, werfen Sie einen Blick auf dieses umfassende E-Book.

Eine weitere ausgezeichnete Inspirationsquelle mit vielen Open-Source-Beispielen ist [*pcjericks*] GitHub Repository *py-gdalogr-cookbook*](https://pcjericks.github.io/py-gdalogr-cookbook/).

```{admonition} How to use PyQGIS (QGIS Python environment)
:class: tip, dropdown

To enable working with QGIS commands in standalone Python scripts through `from qgis.core import *`, have a look at the {ref}`PyQGIS section <pygis>` at the bottom of the QGIS tutorial in this eBook.
```
