---
description: Einführung in das offene TELEMAC-MASCARET für die 2D- und 3D-Hydromorphodynamik-Flusssimulation mit einem Leitfaden für alle Tutorials zur Vorverarbeitung, zum Steady-Flow, zum instationären Fluss und zum GAIA-Sedimenttransport.
---

(chpt-telemac)=
# TELEMAC

Die auf diesen Seiten beschriebenen numerischen Simulationsmethoden verwenden die frei verfügbare Software *open TELEMAC-MASCARET* (im Folgenden TELEMAC genannt), die als Handelscode von der F&E-Gruppe der Électricité de France (EDF) gestartet wurde. Seit 2010 hat das TELEMAC-MASCARET Konsortium die Entwicklung übernommen (EDF R&D ist immer noch stark involviert) und stellt die Software und ihren Quellcode unter einer [GPLv3 license](http://www.gnu.org/licenses/gpl-3.0.html)] frei zur Verfügung. Besuchen Sie ihre [Website](http://www.opentelemac.org/)], um mehr über TELEMAC zu erfahren.

Working on [Debian Linux](https://www.debian.org/) or one of its derivatives (see the chapter on {ref}`Virtual Machines (VMs) and Linux <chpt-vm-linux>`) facilitates handling TELEMAC, because most of its core algorithms were originally developed on Linux platforms. Using Linux follow the {ref}`TELEMAC installation <telemac-install>` chapter (account for approximately 2 hours for the installation).

(tm-tutorial-guide)=
## Allgemeine Einführung und Tutorial Guide

Die Analyse von Hydroumgebungen mit TELEMAC beinhaltet die Vorverarbeitung zur Abstraktion der Flusslandschaft, das Einrichten von Kontrolldateien, das Ausführen eines TELEMAC-Solvers und die Nachbearbeitung. Der erstmalige Benutzer steht vor einer überwältigenden Anzahl von Softwareoptionen für die Vor- und Nachbearbeitung. Darüber hinaus verfügt TELEMAC über eine breite Palette von Modulen zur zweidimensionalen (2d) und dreidimensionalen (3d) Modellierung hydromorphodynamischer Prozesse verschiedener Gewässer, von Bergflüssen bis zu Küstendeltas unter dem Einfluss von Gezeiten. Außerdem können mehrere Sedimenttransportphänomene modelliert und mit stetigen oder instationären Strömungsbedingungen gekoppelt werden. Folglich ist das Anwendungsspektrum von TELEMAC sehr breit und dieses eBook bietet Tutorials für ein fundiertes Verständnis der grundlegenden Elemente der Flussökosystemmodellierung. Zu diesem Zweck enthält dieses eBook die folgenden Tutorials:

* Generate a Selafin `*.slf*` geometry mesh along with boundary conditions with QGIS, the BASEmesh plugin, and BlueKenue in the {ref}`pre-processing tutorial <slf-prepro-tm>`. **Recommended as first introductory tutorial for beginners.**
* Richten Sie eine rein hydrodynamische, stetige Telemac2d-Simulation in der {ref}`steady 2d tutorial <telemac2d-steady>` (Selafin `*.slf*` Geometrie) ein. ** Empfohlen als zweites Tutorial für Anfänger.**
* Apply quasi-steady (near-census unsteady) flow conditions (e.g., important for modeling a flood hydrograph) in the {ref}`unsteady Telemac2d tutorial <chpt-unsteady>`. This tutorial builds on top of the steady Telemac2d tutorial.
* Setup a purely hydrodynamic 3d model in the {ref}`Telemac3d tutorial <chpt-telemac3d-slf>`.
* Couple hydrodynamics (i.e., Telemac2d or Telemac3d) with morphodynamics (i.e., {term}`Sediment transport`) in the {ref}`Gaia tutorial <tm-gaia>`.


The tutorials build on the user manuals provided by the TELEMAC developers at [http://wiki.opentelemac.org](http://wiki.opentelemac.org/doku.php).


### Vorverarbeitung

Bei der Vorverarbeitung wird die Flusslandschaft in ein Rechennetz (Grid) mit Randbedingungen abstrahiert. Viele Software-Tools können für diesen Zweck verwendet werden, wie zum Beispiel:

* {ref}`qgis-install` und das BASEmesh-Plugin, die im {ref}`QGIS pre-processing tutorial <slf-prepro-tm>` (**die bevorzugte Wahl des Autors**) dargestellt sind.
* The National Research Council Canada's {ref}`Blue Kenue <bluekenue>` GUI software (primarily for *Windows*).
* {ref}`SALOME <salome-install>` zum Erzeugen von Rechenmaschen im MED-Dateiformat.

### Model Setup und Run

The centerpiece of any TELEMAC model is the control (steering or CAS) file, which can be set up with {ref}`Fudaa PrePro <fudaa>`. The model setup is explained in the above {ref}`tutorial guide <tm-tutorial-guide>` for TELEMAC.

### Nachbearbeitung

*Artelia Eau et Environnement* created the [PostTelemac](https://plugins.qgis.org/plugins/PostTelemac/) plugin for {ref}`qgis-install`, which is a powerful and convenient tool for visualizing and post-processing TELEMAC simulation results. The {ref}`Telemac2d (steady) Post-processing <tm-steady2d-postpro>` illustrates the usage of the PostTelemac QGIS plugin (read more in the {ref}`TELEMAC pre-processing tutorial <tm-qgis-plugins>`) to create {ref}`raster <raster>` maps and other useful data derivatives from TELEMAC output. 


(tm-files)=
## Die TELEMAC File Structure

Für jede TELEMAC-Simulation sind die folgenden Eingabedateien **obligatorisch **:

* Lenkungsdatei
  + Dateiformat: `*.cas`
  + Prepare either with {ref}`Fudaa PrePro <fudaa>` or use a text editor (e.g., {ref}`npp`).
* Geometrie-Datei
  + Dateiformate: `*.slf` ([selafin](https://gdal.org/drivers/vector/selafin.html) oder `*.med`) (MED-Dateibibliothek von der [salome-platform](https://www.salome-platform.org)])
  + Prepare `*.slf` geometries with {ref}`QGIS <qgis-tutorial>`or {ref}`Blue Kenue <bluekenue>` (read more in the {ref}`TELEMAC pre-processing tutorial <bk-create-slf>`).
  + Bereiten Sie `*.med` Geometrien mit {ref}`SALOME <salome-install>` vor.
* Grenzbedingungen
  + Dateiformat: `*.cli` (mit `*.slf`) oder `*.bnd`/`*.bcd` (mit `*.med`)
  + Prepare `*.cli` files with {ref}`Fudaa PrePro <fudaa>` or {ref}`Blue Kenue <bluekenue>` (read more in the {ref}`TELEMAC pre-processing tutorial <bk-bc>`).
  + Prepare `*.bnd`/`*.bcd` files either with {ref}`SALOME <salome-install>` or with a text editor.

Es gibt viele weitere Dateien, die nicht für jede TELEMAC-Simulation rechnerisch vorgeschrieben sind, aber für bestimmte Szenarien (z. B. instationäre Flüsse) und Module (z. B. Sedimenttransport mit Gaia) unerlässlich sind. Solche **optionalen** Dateien umfassen:

* Instationäre Flussdatei (z. B. für Wasseroberflächenhöhen oder Durchflussraten)
  + Erfordert eine Stage-Discharge-Beziehungsdatei
  + Dateiformat: `*.qsl`
* Friktionsdatendatei
  + Dateiformat: `*.tbl` oder `*.txt` (`ASCII`)
* Datei Restart / Referenz (für Modellvalidierung)
  + Dateiformat: `.slf` oder `.med`
  + Weitere Informationen finden Sie unter [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (Abschnitt 4.1.3) (siehe auch {cite:t}`hervouet_user_2014`).
* Abschnittsdatei, um Kontrollabschnitte festzulegen (z. B. Durchflussraten, Geschwindigkeit oder Wasseroberflächenhöhe überprüfen)
* Datei mit Quellen (z. B. Wasser oder Sediment)
* Datei der Phasenentladungs-Beziehung
  + Dateiformat: `*.tbl` oder `*.txt` (`ASCII`)
* Zonendateien zur Beschreibung der reginalen Reibung oder anderer zonaler Eigenschaften

Wenn hydraulische Strukturen in ein Modell integriert werden, sind einige der folgenden Dateien erforderlich (abhängig vom Strukturtyp):

* Culverts-Datendatei
* Datei Weirs

Darüber hinaus kann eine *FORTRAN*-Datei (`.f`) erstellt werden, um spezielle Randbedingungen, benutzerdefinierte Algorithmen oder die Verwendung von Einfach- oder Doppelpräzision anzugeben.

```{admonition} Single and double precision
Bei der hydromorphodynamischen Modellierung ist eine einfache Präzision (d.h. 32-Bit *floats*) anstelle einer doppelten Präzision (d.h. unter Verwendung von 64-Bit *floats*) ausreichend und viel schneller.
```

Weitere Eingabedateien können definiert werden, um Ölverschmutzungen, Schadstofftransport, Wind- und Gezeiteneffekte zu simulieren.


## Detaillierte Dateibeschreibungen

### Die Lenkungsdatei (CAS)

Die Steuerungsdatei ist die Hauptsimulationsdatei mit Informationen über obligatorische Dateien (z. B. die [*selafin*](https://gdal.org/drivers/vector/selafin.html) Geometrie oder die Grenze), optionale Dateien und Simulationsparameter. Die Steuerungsdatei kann mit einem einfachen Texteditor oder einer fortschrittlichen Software wie {ref}`Fudaa PrePro <fudaa>` oder {ref}`Blue Kenue <bluekenue>` erstellt oder bearbeitet werden.


### Geometriedateien (SLF oder MED)

Die Geometriedatei im Format [`*.slf` (*selafin* oder *SERAFIN*)](https://gdal.org/drivers/vector/selafin.html) enthält binäre Daten über das Mesh mit seinen Knoten. Das Namensformat der Geometriedatei kann in der Steuerungsdatei geändert werden mit:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF / or MED with SALOME preferably for 3D
```

*MED* files are typically processed with either {ref}`SALOME <salome-install>`.


### Grenzbedingungen (CLI oder BND/BCD) und Liquid Boundary (QSL) Dateien

The boundary file in `*.cli` format contains information about inflow and outflow nodes (coordinates and IDs). The `*.cli` file can be opened and modified with any text editor, which is not recommended to avoid inconsistencies. Preferably use {ref}`Fudaa PrePro <fudaa>` or {ref}`Blue Kenue <bluekenue>` for generating and/or modifying `*.cli` files (read more in the {ref}`TELEMAC pre-processing tutorial <bk-bc>`). Here is an example (header only) for a `*.cli` boundary conditions file:

```
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    101     1
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    102     2
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    103     3
  ...
```


`*.bnd`/`*.bcd` files can be created and edited either with {ref}`SALOME <salome-install>` or a text editor. The following block box shows how a `*.bnd` boundary file for a simple block geometry may look like.

```
4
5 4 4 4 downstream
4 5 5 4 upstream
2 0 0 2 leftwall
2 0 0 2 rightwall

```

Benutzer können eine Datei mit flüssigen Randbedingungen (`*.qsl`) definieren, um zeitabhängige (unruhige) Randbedingungen (z. B. Entladung, Wassertiefe, Strömungsgeschwindigkeit oder Tracer) zu definieren. Der folgende Block zeigt ein Beispiel für eine Datei mit flüssigen Randbedingungen (`*.qsl`):
```
# bc_unsteady.qsl
# Time-dependent inflow (discharge Q(2) and outflow (depth SL(1)
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

Die Randbedingungen und flüssigen Randdateien können in die Steuerungsdatei eingefügt werden mit:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
```

### Stage-Discharge (oder WSE-Q) Datei (txt - ASCII)

Definieren Sie eine Bühnenentladungsdatei, um eine Bühne zu verwenden (Wasseroberflächenhöhe * WSE*) - Entladungsbeziehung für Randbedingungen. Solche Dateien gelten typischerweise für die stromabwärtige Grenze eines Modells an Kontrollabschnitten (z. B. ein freies Überlaufwehr). Der folgende Block zeigt ein Beispiel für eine Stage-Discharge-Datei (`*.txt`):

```
# wse_Q.txt
#
Q(1)     Z(1)
m3/s     m
 50.     0.0
 60.     0.9
100.     1.5
```

Um eine Stage-Discharge-Datei zu verwenden, definieren Sie das folgende Schlüsselwort in der Steuerungsdatei:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```

### Friktionsdatendatei (tbl/txt - ASCII)

Diese optionale Datei ermöglicht die Definition der Bodenreibung bezüglich des Rauheitsgesetzes und der zugehörigen Funktionskoeffizienten.

Um Reibungsdaten zu aktivieren und zu verwenden, definieren Sie die folgenden Schlüsselwörter in der Lenkungsdatei:

```
/steering.cas
FRICTION DATA            : YES
FRICTION DATA FILE       : 'friction.tbl'
```

### Die Results/Restart-Datei (SLF oder MED)


A restart file stems from a previous TELEMAC simulation and does not need to exist at the beginning. A good option for visualizing the results file is the {ref}`PostTelemac plugin <tm-qgis-plugins>` in QGIS. Restart files in MED format are typically processed with the ParaVis module in {ref}`SALOME <salome-install>`.

Die Ergebnis-/Neustart-Datei kann in der Lenkungsdatei wie folgt definiert werden:
```
/steering.cas
RESULTS FILE             : 't2d_channel_output.slf'
```

Das [Telemac2d-Handbuch](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (Abschnitt 4.1.3) bietet weitere Erklärungen zur Verwendung von Ergebnis-/Neustartdateien (z. B. zur Beschleunigung von Simulationen).
