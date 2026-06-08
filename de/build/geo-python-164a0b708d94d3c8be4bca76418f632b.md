---
description: Einführung in die geospatiale Python-Programmierung für die Hydralogie, Abdeckung von Open-Source- und kommerziellen Bibliotheken, Raster- und Vektordatenmanipulation und geospatiale Dateiformatkonvertierung.
---

(sec-geo-python)=
# Geodäsie Python

Python ist mit mehreren Bibliotheken verbunden, die viele Open-Source- und kommerzielle (proprietäre) Funktionen für die Analyse von Geodaten bereitstellen. Dieser Abschnitt führt sowohl Open-Source als auch (kurz) die kommerzielle `arcpy` Bibliothek ein. Ziel dieses Abschnitts ist es, ein Verständnis dafür zu bieten, wie geospatiale Daten verwendet und mit Python-Code manipuliert werden können. Die Dateimanipulation beinhaltet logische und algebraische Operationen und Konvertierung von und in andere geospatiale Dateiformate.

```{admonition} Requirements
:class: important

Stellen Sie sicher, dass Sie die Grundlagen von Python verstehen, insbesondere {ref}`var`, {ref}`sec-pyerror`, {ref}`chpt-functions` und arbeiten mit externen{ref}`sec-pypckg`.
```

```{admonition} Maximize learning success
:class: tip

* Verwenden Sie das [flusstools](https://flusstools.readthedocs.io)Paket, um die Zusammenarbeit mit den Tutorials, die mit diesem eBook bereitgestellt werden, zu erleichtern.
* Verstehen Sie {ref}`geospatial-data`, die die Grundlagen jeder geospatialen Analyse sind.
* Verwenden Sie {ref}`qgis-install`, um geospatiale Daten anzuzeigen und Karten in *PDF* oder Bildformaten zu erstellen (z.B. *tif*, *png*, *jpg*).
```

Die Beschreibungen von Open-Source-Paketen für die Geospatial-Datenverarbeitung basieren auf Erklärungen von [Michael Dieners Python Geospatial Analysis Cookbook](https://github.com/mdiener21/python-geospatial-analysis-cookbook) (offener Zugriff unter MIT-Lizenz). Wenn Sie daher mehr Informationen über alle hier bereitgestellten Informationen erfahren möchten, werfen Sie einen Blick auf dieses umfassende E-Book.

Eine weitere hervorragende Inspirationsquelle mit vielen offenen Beispielen ist [*pcjericks* GitHub Repository *py-gdalogr-cookbook*](https://pcjericks.github.io/py-gdalogr-cookbook/).

```{admonition} How to use PyQGIS (QGIS Python environment)
:class: tip, dropdown

Um die Zusammenarbeit mit QGIS-Befehlen in eigenständigen Python-Skripten über `from qgis.core import *` zu ermöglichen, werfen Sie einen Blick auf die {ref}`PyQGIS section <pygis>` an der Unterseite des QGIS-Tutorials in diesem eBook.
```
