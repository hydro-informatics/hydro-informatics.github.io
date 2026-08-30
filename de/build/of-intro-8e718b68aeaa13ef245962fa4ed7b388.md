---
description: Einführung in OpenFOAM Open-Source-CFD-Software zur Simulation von turbulenten Strömungen, Wärmeübertragung und komplexen Geometrien mit der Finite-Volume-Methode auf parallelen Computersystemen.
---

(chpt-openfoam)=
# OpenFOAM

<img src="https://www.openfoam.com/themes/bs4esi/img/openfoam-logo.png" width="91" height="16"> ([Open Field Operation and Manipulation](https://www.openfoam.com)) is a free, open source CFD software developed primarily by OpenCFD Ltd since 2004. OpenFOAM is a C++ toolbox that can be used to deploy Finite Volume Method (FVM)-based solvers for general continuum mechanics problems, mostly for fluid flow and heat transfer.

OpenFOAM hat eine breite Palette von Funktionen, wie zum Beispiel:

* Die Fähigkeit, alles zu simulieren, was mit CFD zu tun hat, wie z. B. turbulente Strömungen in der Automobilaerodynamik, Brände und Brandunterdrückung in Gebäuden, Verbrennung, chemische Reaktionen, Wärmeübertragung, Flüssigkeitssprenkler oder Filme.
* Es umfasst Werkzeuge für den Umgang mit komplexen Geometrien (z.B. einen Fischpass) sowie für die Datenverarbeitung und Visualisierung.
* Es führt parallele Berechnungen durch, die es ermöglichen, die Vorteile moderner Multicore-Prozessoren und Multiprozessor-Computer über den [Message Passing Interface (MPI)-Standard)](https://www.mpi-forum.org/) voll auszuschöpfen.


```{admonition} Requirements for this tutorial
:class: attention

To accomplish this tutorial, make sure that OpenFOAM is installed on you computer (see the {ref}`OpenFOAM installation section <openfoam-install>`). Technically, a basic understanding of the {term}`Navier-Stokes equations`, specifically {term}`RANS` and related turbulence closures, facilitates understanding the descriptions and assumptions made in this tutorial. And you are good to go.
```

## Verzeichnisse (OpenFOAM-Ordnerstruktur)
  
### Grundverzeichnis

Die grundlegende Verzeichnisstruktur für einen OpenFOAM-Fall, der den Mindestsatz an Dateien enthält, die zum Ausführen einer Anwendung erforderlich sind, wird in {numref}`Fig. %s <of-case-structure>` angezeigt:
 
```{figure} ../../img/openfoam/case-structure.png
:alt: case structure openfoam folder directories
:name: of-case-structure

OpenFOAM-Fallverzeichnisstruktur.
```
 

### Konstantes Verzeichnis

Das konstante Verzeichnis enthält alle Werte, die während der Berechnung konstant bleiben. Dies sind Dateien, die die physikalischen Eigenschaften (z. B. Transporteigenschaften und Turbulenzmodelle) angeben. Das Unterverzeichnis *polyMesh* enthält alle Informationen über das Mesh.

```{figure} ../../img/openfoam/constant.png
:alt: case structure openfoam files constant
:name: of-constant-dir

Beispiel für den konstanten Verzeichnisinhalt.
```


### Systemverzeichnis

In diesem Verzeichnis ist es möglich, die mit der Lösungsprozedur verbundenen Parameter zu ändern. Es enthält mindestens folgende Dateien:

* *controlDict* mit Parametern wie Start-/Endzeit, Zeitschritt und Datenausgabe werden eingestellt;
* *fvSchemes*, wobei die Diskretisierungsschemata ausgewählt werden können;
* *fvSolution*, in dem die Parameter und die Lösungsauswahl für den Lauf festgelegt sind.

```{figure} ../../img/openfoam/system.png
:alt: case structure openfoam files parameters
:name: of-system-dir

Beispiel für den Systemverzeichnisinhalt.
```


### Zeitverzeichnisse

Diese Verzeichnisse enthalten die Datendateien für jedes Feld der Simulation.

```{figure} ../../img/openfoam/time-dir.png
:alt: case structure openfoam files parameters time
:name: of-time-dir

Beispiel für den Nullzeitschritt Verzeichnisinhalt.
```


### Dokumentation & Weiterlesen

Die folgende Liste enthält weitere Quellen mit weiteren Informationen zu OpenFOAM
kann gefunden werden, einschließlich Tutorials und Vorlesungsnotizen.

* Allgemeine Informationen zum Ausführen von OpenFOAM, Compilation, Solvers, Modellen, Mesh-Generierung und Nachbearbeitung im [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/) und [OpenFOAM Programmer's Guide](https://doc.cfd.direct/openfoam/dev/)]
* [OpenFOAM Wiki](https://openfoamwiki.net/)]
* The CFD Online OpenFOAM Forum at: [https://www.cfd-online.com/Forums/openfoam/](https://www.cfd-online.com/Forums/openfoam/)
* More tutorials, videos and the book "Mathematics, Numerics, Derivations and OpenFOAM" can be found at: [https://holzmann-cfd.com/](https://holzmann-cfd.com/)  
* Video-Tutorials mit detaillierten Schritt-für-Schritt-Anleitungen finden Sie unter: [youtube.com/OpenFOAMJozsefnagy](https://www.youtube.com/@OpenFOAMJozsefNagy/)]
* Vortragsnotizen eines PhD-Kurses CFD mit OpenSource Software, verfügbar unter: [tfd.chalmers.se](http://www.tfd.chalmers.se/~hani/kurser/OS_CFD/#YEAR_2022)]
  
