---
description: Einführung in die offene TELEMAC-MASCARET für die hydromorphodynamische Flusssimulation 2D und 3D, mit einem Leitfaden für alle Tutorials, die Vorverarbeitung, stetige Strömung, unruhige Strömung und GAIA Sedimenttransport.
---

(chpt-telemac)=
# TELEMAC

Die auf diesen Seiten beschriebenen numerischen Simulationsmethoden verwenden die frei verfügbare Software *open TELEMAC-MASCARET* (im Folgenden TELEMAC genannt), die als Handelscode von der F&D-Gruppe der Électricité de France (EDF) gestartet wurde. Seit 2010 übernimmt das TELEMAC-MASCARET Consortium die Entwicklung (EDF R&D ist noch zutiefst beteiligt) und stellt die Software und ihren Quellcode unter einer [GPLv3 License](http://www.gnu.org/licenses/gpl-3.0.html). Besuchen Sie ihre [website](http://www.opentelemac.org/), um mehr über TELEMAC zu erfahren.

Die Zusammenarbeit mit [Debian Linux](https://www.debian.org/) oder einem seiner Derivate (siehe Kapitel {ref}`Virtual Machines (VMs) and Linux <chpt-vm-linux>`) erleichtert die Handhabung von TELEMAC, da die meisten seiner Kernalgorithmen ursprünglich auf Linux-Plattformen entwickelt wurden. Mit Linux folgen Sie dem {ref}`TELEMAC installation <telemac-install>`Kapitel (Berechnung für ca. 2 Stunden für die Installation).

(tm-tutorial-guide)=
## Allgemeine Einführung und Anleitung

Die Analyse von Hydro-Umgebungen mit TELEMAC beinhaltet die Vorverarbeitung zur Abstraktion der fluvialen Landschaft, die Einrichtung von Kontrolldateien, den Betrieb eines TELEMAC-Lösers und die Nachbearbeitung. Der erste Benutzer sieht eine überwältigende Anzahl von Softwareoptionen für die Vor- und Nachbearbeitung vor. Darüber hinaus verfügt TELEMAC über eine breite Palette von Modulen für zweidimensionale (2d) und dreidimensionale (3d) Modellierung von hydromorphodynamischen Prozessen verschiedener Wasserkörper, von Bergflüssen bis Küstendeltas unter dem Einfluss von Tides. Auch können mehrere Sedimenttransporterscheinungen modelliert und mit stetigen oder unruhigen Strömungsverhältnissen gekoppelt werden. Folglich ist das Anwendungsspektrum von TELEMAC sehr breit und dieses eBook bietet Tutorials für ein fundiertes Verständnis grundlegender Elemente der Flussökosystemmodellierung. Zu diesem Zweck verfügt dieses eBook über folgende Tutorials:

* Generieren Sie ein Selafin `*.slf*` Geometrie-Netz zusammen mit Randbedingungen mit QGIS, dem BASEmesh-Plugin und BlueKenue in der {ref}`pre-processing tutorial <slf-prepro-tm>`. **Einführendes Tutorial für Anfänger**
* Eine rein hydrodynamische, stetige Telemac2d-Simulation in der {ref}`steady 2d tutorial <telemac2d-steady>` (Selafin`*.slf*` Geometrie) einrichten. **Ein zweites Tutorial für Anfänger**
* Quasi-steady (near-census unsteady) Strömungsbedingungen (z.B. wichtig für die Modellierung eines Flut-Hydrographen) in der {ref}`unsteady Telemac2d tutorial <chpt-unsteady>`. Dieses Tutorial baut auf dem stationären Telemac2d Tutorial.
* Aufbau eines rein hydrodynamischen 3d Modells in der {ref}`Telemac3d tutorial <chpt-telemac3d-slf>`.
* Doppel-Hydrodynamik (d.h. Telemac2d oder Telemac3d) mit Morphodynamik (d.h.{term}`Sediment transport`) in der {ref}`Gaia tutorial <tm-gaia>`.


The tutorials build on the user manuals provided by the TELEMAC developers at [http://wiki.opentelemac.org](http://wiki.opentelemac.org/doku.php).


### Vorverarbeitung

Die Vorverarbeitung beinhaltet die Abstraktion der Flusslandschaft in ein Rechennetz (Grid) mit Randbedingungen. Für diesen Zweck können viele Software-Tools verwendet werden, z.B.:

* {ref}`qgis-install` und das BASEmesh-Plugin, die im {ref}`QGIS pre-processing tutorial <slf-prepro-tm>` dargestellt sind (** die bevorzugte Wahl des Autors*).
* Die Software {ref}`Blue Kenue <bluekenue>` GUI des National Research Council Canada (vor allem für *Windows*).
* {ref}`SALOME <salome-install>` zur Generierung von Rechennetzen im MED-Dateien-Format.

### Modell Setup und Run

Das Herzstück eines TELEMAC Modells ist die Steuerungsdatei (Steering oder CAS), die mit {ref}`Fudaa PrePro <fudaa>` eingerichtet werden kann. Das Modell-Setup wird im obigen {ref}`tutorial guide <tm-tutorial-guide>` für TELEMAC erläutert.

### Nachbearbeitung

*Artelia Eau et Environnement* erstellte das [PostTelemac](https://plugins.qgis.org/plugins/PostTelemac/) Plugin für {ref}`qgis-install`, das ein leistungsstarkes und komfortables Tool zur Visualisierung und Nachbearbeitung von TELEMAC-Simulationsergebnissen ist. Die {ref}`Telemac2d (steady) Post-processing <tm-steady2d-postpro>` illustriert die Nutzung des PostTelemac QGIS Plugins (weiterlesen im {ref}`TELEMAC pre-processing tutorial <tm-qgis-plugins>`) um {ref}`raster <raster>`Karten und andere nützliche Datenderivate vom TELEMAC-Ausgang zu erstellen.


(tm-files)=
## Die TELEMAC Dateistruktur

Für jede TELEMAC-Simulation sind die folgenden Eingabedateien **verpflichtend**:

* Steuerungsdatei
  + Dateiformat: `*.cas`
  + Bereiten Sie sich entweder mit {ref}`Fudaa PrePro <fudaa>` vor oder verwenden Sie einen Texteditor (z.B. {ref}`npp`).
* Geometriedatei
  + Dateiformate: `*.slf` ([selafin](https://gdal.org/drivers/vector/selafin.html) oder `*.med` (MED-Dateibibliothek von der [salome-platform](https://www.salome-platform.org)
  + Bereiten Sie `*.slf` Geometrien mit {ref}`QGIS <qgis-tutorial>`or{ref}`Blue Kenue <bluekenue>` vor (lesen Sie mehr unter {ref}`TELEMAC pre-processing tutorial <bk-create-slf>`).
  + Bereiten Sie `*.med` Geometrien mit {ref}`SALOME <salome-install>`.
* Schwere Bedingungen
  + Dateiformat: `*.cli` (mit `*.slf`) oder `*.bnd`/`*.bcd` (mit `*.med`)
  + Bereiten Sie `*.cli`-Dateien mit {ref}`Fudaa PrePro <fudaa>` oder {ref}`Blue Kenue <bluekenue>` vor (weiterlesen unter {ref}`TELEMAC pre-processing tutorial <bk-bc>`).
  + Prepare `*.bnd`/`*.bcd` files either with {ref}`SALOME <salome-install>` or with a text editor.

Es gibt viele weitere Dateien, die für jede TELEMAC-Simulation nicht rechnerisch vorgeschrieben sind, sondern für bestimmte Szenarien (z.B. unruhige Ströme) und Module (z.B. Sedimenttransport mit Gaia) wesentlich sind. Solche **optional** Dateien umfassen:

* Unsteady flow file (z.B. für Wasseroberflächenerhebung oder Durchflussraten)
  + Erfordert eine Phase-Decharge-Beziehungsdatei
  + Dateiformat: `*.qsl`
* Friktionsdatendatei
  + Format: `*.tbl` oder `*.txt` (`ASCII`)
* Restart / Referenz (für Modellvalidierung) Datei
  + Dateiformat: `.slf` oder `.med`
  + Weitere Informationen in der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (Abschnitt 4.1.3) (siehe auch {cite:t}`hervouet_user_2014`).
* Abschnittsdatei zur Einstellung von Steuerabschnitten (z.B. Überprüfung von Durchflussraten, Geschwindigkeit oder Wasseroberflächenerhebung)
* Quellen (z.B. Wasser oder Sediment) Datendatei
* Datei aufheben
  + Format: `*.tbl` oder `*.txt` (`ASCII`)
* Zonen-Dateien, um Reginalreibung oder andere zonale Eigenschaften zu beschreiben

Wenn hydraulische Strukturen in ein Modell integriert werden, werden einige der folgenden Dateien benötigt (je nach Strukturtyp):

* Datendatei umwandeln
* Weirs Datendatei

Darüber hinaus kann eine *FORTRAN* (`.f`)-Datei erstellt werden, um spezielle Randbedingungen, benutzerdefinierte Algorithmen oder die Verwendung von entweder Einzel- oder Doppelpräzision anzugeben.

```{admonition} Single and double precision
Bei der hydromorphodynamischen Modellierung ist eine Einzelpräzision (d.h. 32-Bit * Floats*) statt Doppelpräzision (d.h. mit 64-Bit *floats*) ausreichend und viel schneller.
```

Mehr Eingabedateien können definiert werden, um Ölverschüttungen, Schadstofftransport, Wind und Tide-Effekte zu simulieren.


## Detaillierte Dateibeschreibungen

### The Steering File (CAS)

Die Lenkdatei ist die Hauptsimulationsdatei mit Informationen über obligatorische Dateien (z.B. die [*selafin*](https://gdal.org/drivers/vector/selafin.html) Geometrie oder die Grenze), optionale Dateien und Simulationsparameter. Die Lenkdatei kann mit einem Texteditor oder einer erweiterten Software wie {ref}`Fudaa PrePro <fudaa>` oder {ref}`Blue Kenue <bluekenue>` erstellt oder bearbeitet werden.


### Geometriedateien (SLF oder MED)

Die Geometriedatei im Format [`*.slf` (*selafin* oder *SERAFIN*)](https://gdal.org/drivers/vector/selafin.html) enthält binäre Daten über das Netz mit seinen Knoten. Das Namensformat der Geometriedatei kann in der Lenkdatei mit:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF / or MED with SALOME preferably for 3D
```

*MED*-Dateien werden typischerweise mit entweder {ref}`SALOME <salome-install>` verarbeitet.


### Boundary Bedingungen (CLI oder BND/BCD) und Liquid Boundary (QSL) Dateien

Die Randdatei im Format `*.cli` enthält Informationen über Zufluss- und Abflussknoten (Koordinaten und IDs). Die `*.cli`-Datei kann mit jedem Texteditor geöffnet und geändert werden, was nicht empfohlen wird, Unstimmigkeiten zu vermeiden. Verwenden Sie vorzugsweise {ref}`Fudaa PrePro <fudaa>` oder {ref}`Blue Kenue <bluekenue>` zur Generierung und/oder Modifizierung von `*.cli`-Dateien (lesen Sie mehr unter {ref}`TELEMAC pre-processing tutorial <bk-bc>`). Hier ist ein Beispiel (nur Header) für eine `*.cli` Randbedingungen Datei:

```
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    101     1
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    102     2
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    103     3
  ...
```


`*.bnd`/`*.bcd` Dateien können entweder mit {ref}`SALOME <salome-install>` oder einem Texteditor erstellt und bearbeitet werden. Die folgende Blockbox zeigt, wie eine `*.bnd` Randdatei für eine einfache Blockgeometrie aussehen kann.

```
4
5 4 4 4 downstream
4 5 5 4 upstream
2 0 0 2 leftwall
2 0 0 2 rightwall

```

Benutzer können eine flüssige Randbedingungen-Datei (`*.qsl`) definieren, um zeitabhängige (unsteady) Randbedingungen (z.B. Entladung, Wassertiefe, Strömungsgeschwindigkeit oder Tracer) zu definieren. Der folgende Block zeigt ein Beispiel für eine flüssige Randbedingungen (`*.qsl`)-Datei:
```
# bc_unsteady.qsl
# Time-dependent inflow (discharge Q(2) and outflow (depth SL(1)
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

Die Randbedingungen und Flüssigkeitsgrenzdateien können in der Lenkdatei hinzugefügt werden mit:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
```

### Stage-Decharge (oder WSE-Q) Datei (txt - ASCII)

Definieren Sie eine Stage-Decharge-Datei, um eine Stufe zu verwenden (Wasser-Oberflächen-Elevation *WSE*) - Entlade-Beziehung für Randbedingungen. Solche Dateien gelten typischerweise für die stromabwärtige Begrenzung eines Modells an Kontrollabschnitten (z.B. einem freien Überlaufwehr). Der folgende Block zeigt ein Beispiel für eine Stage-Decharge (`*.txt`)-Datei:

```
# wse_Q.txt
#
Q(1)     Z(1)
m3/s     m
 50.     0.0
 60.     0.9
100.     1.5
```

Um eine Stage-Decharge-Datei zu verwenden, definieren Sie das folgende Schlüsselwort in der Lenkdatei:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```

### Friction Data File (tbl/txt - ASCII)

Diese optionale Datei ermöglicht die Definition der unteren Reibung in Bezug auf das Rauheitsgesetz zu verwenden und zugehörige Funktionskoeffizienten.

Um Reibungsdaten zu aktivieren und zu verwenden, definieren Sie die folgenden Keywords in der Lenkdatei:

```
/steering.cas
FRICTION DATA            : YES
FRICTION DATA FILE       : 'friction.tbl'
```

### Die Ergebnisse/Restart-Datei (SLF oder MED)


Eine Neustart-Datei stammt aus einer vorherigen TELEMAC-Simulation und muss zu Beginn nicht existieren. Eine gute Möglichkeit zur Visualisierung der Ergebnisse ist die {ref}`PostTelemac plugin <tm-qgis-plugins>` in QGIS. Neue Dateien im MED-Format werden typischerweise mit dem ParaVis-Modul unter {ref}`SALOME <salome-install>` verarbeitet.

Die Ergebnisse/Neustart-Datei kann in der Lenkdatei wie folgt definiert werden:
```
/steering.cas
RESULTS FILE             : 't2d_channel_output.slf'
```

Das [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (Abschnitt 4.1.3) gibt mehr Erläuterungen zur Nutzung von Ergebnissen/Neustart-Dateien (z.B. zur Beschleunigung von Simulationen).
