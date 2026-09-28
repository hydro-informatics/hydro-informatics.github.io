---
description: Leitfaden für Geospatial-Software für die Wasserressourcentechnik einschließlich QGIS-Installation und -Nutzung unter Windows, Linux und macOS für die GIS-Datenvisualisierung und -analyse.
---

(chpt-geo-software)=
# Geodatensoftware

Geospatial-Analysen (oder Analysen) verwenden, manipulieren und veranschaulichen Daten aus geografischen Informationssystemen (GIS). GIS-Daten enthalten geografisch referenzierte und räumlich explizite Informationen von beispielsweise Messstationen, Geländehöhe oder Landnutzung. Die effiziente Verarbeitung von Geodaten beinhaltet Programmiermethoden, wobei *Python* ein effizientes Werkzeug ist. Diese Seite präsentiert Desktop-Software für manuelle Geodatenanalysen und die Darstellung von Geodaten. Für die geospatiale Programmierung lesen Sie bitte das {ref}`sec-geo-python` Kapitel.

(qgis-install)=
## QGIS
For the visualization of geodata (`.shp` and `.tif` files), GIS software is required and the analyses described on these pages refer to the usage of [QGIS](https://www.qgis.org). This eBook uses QGIS within the sections on {ref}`geospatial programming with Python <sec-geo-python>` and numerical modelling with the ETH Zurich's [BASEMENT](../numerics/basement/basement) software.

### QGIS unter Windows installieren
Laden Sie die neueste Version von [QGIS](https://qgis.org/download/) für Windows] herunter und installieren. Obwohl die Entwickler die Installation von QGIS über *OSGeo4W* empfehlen, wird dieser Installationspfad für die Arbeit mit dem * Hydroinformatik* eBook (viele Plugin-Fehler und veraltete Bibliotheksabhängigkeiten) nicht empfohlen. Daher **laden und verwenden Sie vorzugsweise den neuesten QGIS Standalone Installer**.

### QGIS unter Linux installieren (via Flatpak)

Die QGIS-Entwickler bieten detaillierte Installationsanweisungen für mehrere *Linux*-Distributionen an, aber die Anweisungen erfüllen nicht alle in diesem eBook beschriebenen Anforderungen für die Verwendung von QGIS. Eine der funktionalsten Möglichkeiten, QGIS auf *Linux* zu installieren, ist die Verwendung von [Flatpak](https://flathub.org/apps/details/org.qgis.qgis), was eine gewisse Systemvorbereitung erfordert]. Auf *Debian*-basierten *Linux*-Plattformen (z. B. alle Arten von *Ubuntu* wie *Lubuntu* oder *Mint*) öffnen *Terminal* und tippen (die zweite Zeile wird nur benötigt, wenn Sie *GNOME* verwenden):

```
sudo apt install flatpak
sudo apt install gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

Starten Sie das System neu und öffnen Sie die *Software Manager * App. Es wird das Flathub-Repo aktualisieren und hinzufügen. Sobald das Update erfolgreich war, suchen Sie nach QGIS und klicken Sie auf *Installieren * (Geduld - die Installation kann eine Weile dauern).

The *QGIS Flatpak* installation will most likely not include the important *scipy* module. To fix this issue, open  *Terminal* (standard Linux application) and type:
<br>`flatpak run --command=pip3 org.qgis.qgis install scipy --user`

Diese Lösung wurde unter * Linux Ubuntu * und * Linux Mint * getestet. Es funktioniert möglicherweise auch mit *Red Hat*, *openSUSE*, *macOS*, *Arch*, *Fedora*, *Android*, *Debian*, *Kubuntu* und vielen anderen (lesen Sie die Installationsanleitungen auf der [Website des Maintainers](https://flatpak.org/setup/)]. Lesen Sie mehr über die *QGIS Flatpak* Installation auf der [QGIS Webseite](https://qgis.org/download/)].

### QGIS auf macOS installieren

```{admonition} macOS and BASEMENT
:class: attention
Wenn Sie BASEMENT für die numerische Modellierung verwenden möchten: BASEMENT läuft nicht auf macOS.
```

Downloaden und installieren Sie die neueste Version von [QGIS](https://qgis.org/download/) für macOS]. Die Integrität der Verwendung von macOS für die Anwendungen in diesem E-Book wurde noch nicht getestet. Eine mögliche Fehlerbehebung mit * Python * wird beispielsweise von [kyngchaos.com](https://www.kyngchaos.com/software/qgis/)] bereitgestellt.

### Lernen Sie QGIS
Working with geospatial data editors involves complex tasks that require background knowledge before intuitive comprehension is possible. The QGIS developers provide compound [tutorials on their website](https://docs.qgis.org/latest/en/docs/training_manual/index.html) ([also available in other languages including French, German, and Portuguese](https://docs.qgis.org/latest/)).
This eBook occasionally uses QGIS for plotting and creating georeferenced data (e.g., the chapters on {ref}`sec-geo-python` and {ref}`numerical modeling <qgis-prepro-bm>`). To this end, this eBook comes along with a tutorial on geospatial analyses with QGIS (read and do the {ref}`qgis-tutorial`).

(qgis-conda-install)=
### QGIS Conda Environment installieren

In {ref}`Anaconda Prompt <anaconda>`, you can create a new environment to specifically use QGIS features (i.e., tools and scripts) including its raster calculator. The environment is featured by *Open Data Cube* ([read more](https://datacube-qgis.readthedocs.io/en/latest/installation.html)) and can be installed as follows:

```
conda create  -c conda-forge -n qgiscube python=3.11 qgis datacube
conda activate qgiscube
```

(agis)=
## ArcGIS

```{admonition} Windows only
:class: attention
ArcGIS wurde für Windows entwickelt und läuft nicht unter macOS oder Linux. Außerdem muss eine Lizenz erworben werden.
```

Die proprietäre Software *ArcGIS Pro* stellt ein leistungsstarkes Werkzeug für jede Art von Geodatenanalyse dar, einschließlich Webanwendungen. *ArcGIS Pro* wird von [esri](https://www.esri.com/) gepflegt und kommt mit einem eigenen {ref}`conda-env`. Da sich dieses eBook auf frei verfügbare Software konzentriert, wird die Nutzung von *ArcGIS Pro* und seiner *Python*-Umgebung einschließlich des `arcpy`-Pakets auf dieser Website erwähnt.

(others)=
## Andere
Es gibt viele andere Werkzeuge für Geospatialanalysen, die alle viel mehr verdienen, als nur hier erwähnt zu werden. Leider konzentriert sich diese Website aus praktischen Gründen auf die Verwendung von QGIS. Aus diesem Grund gibt es hier nur eine absolut nicht vollständige Liste anderer GIS-Tools:

* [SAGA (System für automatisierte geowissenschaftliche Analysen)](http://www.saga-gis.org/en/index.html)
* [Mapline](https://mapline.com/)]
* [Mapbox](https://www.mapbox.com/)]
* [uDig](http://udig.refractions.net/)]

## Geospatialanalysen

Geospatial-Analysen beinhalten effiziente Code-Praktiken (z.B. mit *Python*) und deshalb sind detaillierte Beschreibungen des Umgangs mit Geodaten in das {ref}`sec-geo-python` Kapitel dieses eBooks eingebettet.
