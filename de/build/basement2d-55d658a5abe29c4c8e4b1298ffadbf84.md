---
description: Tutorial zum Ausführen und Validieren einer stetigen 2D-Hydrodynamiksimulation mit BASEMENT v4, die den Aufbau von model.json und simulation.json, die Randbedingungen und die Überprüfung der Ergebnisse abdeckt.
---

(basement2d)=
# Ausführen und Überprüfen einer stationären 2D-Simulation

```{admonition} Recall BASEMENT versions, BASEMD, and BASEHPC
:class: note

BASEMENT Version 2 (v2) wurde mit komplexen Strukturen und einer breiten Palette von Kapazitäten entwickelt, wobei der Schwerpunkt jedoch wenig auf der Rechenzeit lag. BASEMENT Version 3 (v3) vereinfachte den Modellierungsprozess für die Benutzer erheblich und bot hocheffiziente Rechenoptionen, einschließlich einer massiven Parallelisierung von GPUs. Dem vereinfachten v3 fehlen jedoch viele relevante Module, wie z. B. mehrschichtige Flussbetten zur Berechnung der topografischen Veränderung in Abhängigkeit von mehrkörnigen Transportformeln. Jetzt bietet BASEMENT Version 4 (v4) sowohl die vielfältigen Kapazitäten von v2 in Form von BASEMD-Setups als auch die Recheneffizienz von v3 in Form von BASEHPC-Setups. Dieses Tutorial erklärt die Einrichtung eines BASEHPC-Modells.

```

Zusätzlich zur {term}`SMS 2dm`-Datei aus dem {ref}`qgis-prepro-bm`-Tutorial benötigt die numerische Engine von BASEMENT eine Modell-Setup-Datei (**model.json**) und eine Simulationsdatei (**simulation.json**), die beide automatisch von BASEMENT erstellt werden.

In den folgenden Abschnitten wird beschrieben, wie BASEMENT die erforderlichen {ref}`json`-Dateien in einem Projektverzeichnis wie `C:\Basement\steady2d-tutorial\` (*Windows*) oder `~/Basement/steady2d-tutorial/` (*Linux*) erstellen kann. Daher ist der **erste Schritt das Erstellen eines Projektverzeichnisses (Ordners)**.

```{admonition} Special characters in directory/folder names
:class: attention
Das definierte Projektordnerverzeichnis darf ** keine **Punkte **, noch ** Sonderzeichen **, noch ** Leerzeichen ** enthalten. Verwenden Sie nur Buchstaben, Zahlen, * * (Underscore) oder *-* (minus) in Ordnernamen.
```

** Platzieren Sie die folgenden **Eingabedateien im Projektordner**:

* Die {term}`SMS 2dm` Datei mit interpolierten unteren Erhebungen aus dem {ref}`qgis-prepro-bm` Tutorial (**prepro-tutorial quality-mesh-interp.2dm**).
* Eine stetige Entlade-Inflow-Datei (flacher Hydrograph) für die vorgelagerte Randbedingung kann heruntergeladen werden [hier](https://github.com/hydro-informatics/materials-bm/raw/main/flows/steady-inflow.txt)] (falls erforderlich kopieren Sie den Dateiinhalt lokal in einen Texteditor und speichern Sie die Datei als **steady-inflow.txt** im Projektverzeichnis).

## Initiieren Sie das Modell
Dieser Abschnitt führt durch das Modell-Setup, das in einer Datei namens **model.json** gespeichert ist (hier: im Ordner `/steady2d-tutorial/`). **Starte BASEMENT** und **wähle den oben erstellten Ordner** als **Szenarioverzeichnis** aus (siehe {numref}`Fig. %s <bm-setup-start>`).

```{figure} ../../img/basement/setup-start.png
:alt: basement new project setup launch start
:name: bm-setup-start

Der Willkommensbildschirm von BASEMENT nach dem Auswählen eines *Szenario-Verzeichnisses* mit der Schaltfläche *Projekt speichern* in der oberen rechten Ecke. Die Verzeichnisreferenzen können auf anderen Plattformen unterschiedlich aussehen (z. B. mit **"C:/...** unter Windows beginnen).
```

Als nächstes **links-klicken** auf **SETUP**, dann **rechts-klicken** und wählen **Element BASEHPC** hinzufügen. Ein neuer Tab namens **Define Scenario Parameters** wird geöffnet. Ignorieren Sie im Moment die Warn- und Fehlermeldungen (rote Tags) und definieren Sie einen **simulation name**:

* **Klicken Sie mit der rechten Maustaste auf **SETUP** und wählen Sie **Hinzufügen Element 'simulation name'**. Ein neuer Eintrag namens *simulation name* erscheint unten auf der Registerkarte *Szenarioparameter definieren*.
* **Scrollen Sie nach unten**, **Doppelklicken** auf **"RUNFILE"** (Standardwert hinter **simulation name**) und **ersetzen** `RUNFILE` mit `steady2d`.

**Scrollen Sie zurück** nach oben** und **Speichern Sie das Projekt**, um mit den nächsten Abschnitten fortzufahren.

(bm-geometry)=
## Geometrie und Regionen

The **GEOMETRY** group in the **Define Scenario Parameters** tab tells the model, which {term}`SMS 2dm` mesh file to use and enables the definition of region and liquid boundary properties. To this end, make the following settings:

* **Double-click** on the **Value** field of the **mesh_file** row and click on the folder symbol <br> <img src="../../img/basement/select-meshfile.png">
* In the popup window select the {ref}`previously created prepro-tutorial_quality-mesh-interp.2dm <qgis-prepro-bm>` and hit **Enter**.


Das im letzten Kapitel erstellte Mesh enthält mehrere Regionen, die ebenfalls im Modellaufbau definiert werden müssen:

* **Rechtsklick** auf **GEOMETRY**> **Hinzufügen Element REGIONDEF**
* **Add 5 region items** by **right-clicking** on the new **REGIONDEF** entry > **Add item**. The number of regions should correspond to the regions defined in the {ref}`pre-processing tutorial <region-defs>`, which are also below-listed in {numref}`Tab. %s <region-defs-bm>`.
* Definieren Sie die fünf Regionen mit einem **Rechtsklick** auf **index** > **Item hinzufügen**.
  * Jedes **index [0]** Element erhält eine ganzzahlige Zahl, die dem MATID-Feld in der Regionspunkte-Shapefile zugeordnet ist (siehe {ref}`regions` Abschnitt im {ref}`qgis-prepro-bm` Tutorial).
  * Der **name** jedes Regionselements entspricht dem **type** Feld der MATID.

{numref}`Table %s <region-defs-bm>` fasst die erforderlichen Regionendefinitionen zusammen. Wenn die Regionen und die Mesh-Datei definiert sind, sollte die GEOMETRY-Gruppe {numref}`Fig. %s <bm-regions>` ähneln.

```{list-table} REGIONDEF items and their definitions to be defined in BASEMENT's model setup.
:header-rows: 1
:name: region-defs-bm

* - **REGIONDEF**
  - [0]
  - [1]
  - [2]
  - [3]
  - [4]
* - **index [0]**
  - 1
  - 2
  - 3
  - 4
  - 5
* - **Name **
  - Flussbett
  - block ramp
  - gravel bank
  - Überschwemmungsgebiet
  - Sand Einlage
```


```{figure} ../../img/basement/setup-geometry.png
:alt: region mesh file definitions basement
:name: bm-regions

Die GEOMETRY-Gruppe mit REGIONDEFs und dem Verweis auf die höheninterpolierte Mesh-Datei (prepro-tutorial quality-mesh-interp.2dm).
```

```{admonition} Save the project...
Speichern Sie das Modell-Setup regelmäßig, indem Sie auf die Disk-Taste klicken (oben rechts, siehe {numref}`Fig. %s <bm-setup-start>`).
```

Die {ref}`liquid (hydraulic) boundaries <liquid-boundary>` aus dem Vorverarbeitungs-Tutorial definieren geografisch **Inflow- und Outflow**-Zeilen mit **stringdef**-Attributen, die in die Mesh-Datei (*prepro-tutorial quality-mesh-interp.2dm*) mit Höheninformationen integriert sind. Um die Arten und Eigenschaften der Flüssigkeitsgrenzen mitzuteilen, füllen Sie den Abschnitt GEOMETRIE aus:

* **Rechtsklick** auf **GEOMETRY**> **Hinzufügen Element STRINGDEF**.
* **Klicken Sie mit der rechten Maustaste auf das neue **STRINGDEF**-Element und wählen Sie **Element** zweimal. Daher sollten zwei Elemente verfügbar sein, um die vor- und nachgelagerten Flüssigkeitsgrenzen zu definieren.
* Definieren Sie STRINGDEF Element **[0]** mit:
  * **name** = `inflow`
  * **upstream direction** = `right`
* Definieren Sie STRINGDEF item **[1]** mit:
  * **name** = `outflow`
  * **upstream direction** = `right`

Wenn Sie die bereitgestellte [liquid borders shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/liquid-boundaries.zip)] zum Erstellen der Mesh-Datei verwendet haben, muss die **upstream direction** `right` sein. {numref}`Figure %s <bm-geo-fin>` zeigt die Definition der STRINGDEF-Elemente unter Verwendung der bereitgestellten liquid borders shapefile.

```{figure} ../../img/basement/setup-geometry-final.png
:alt: region mesh file definitions basement
:name: bm-geo-fin

Die GEOMETRY-Gruppe mit STRINGDEFs, die die bereitgestellten flüssigen Grenzen Shapefile im Rechennetz verwenden.
```

(bm-hydraulics)=
## Hydraulik

Hydraulische Modellmerkmale, die für den oben definierten Geometrieaufbau gelten, werden in der Gruppe **HYDRAULICS** des BASEMENT-Modellaufbaus definiert. Dieses Tutorial verwendet den **standard** für **initial** Bedingungen, der **"trocken"** ist. Halten Sie auch ** den Standard PARAMETERS** für **{term}`CFL-Zahl <CFL>`** = `0.9`, **fluid density** = `1000.0`, **max time step** = `100.0` und **minimum Wassertiefe** = ` 0.01`.

Hydraulische Mengen, wie Wassertiefe und Abfluss, müssen den oben definierten Flüssigkeitsgrenzen zugeordnet werden, damit das numerische Modell weiß, wie viel Wasser es durch das Modell laufen muss. Fügen Sie daher die folgenden Randdefinitionen in der HYDRAULICS-Gruppe hinzu:

* **Klicken Sie mit der rechten Maustaste auf **HYDRAULICS** und wählen Sie **Element BOUNDARY**.
* **Klicken Sie mit der rechten Maustaste auf das neue ** BOUNDARY**-Element und wählen Sie **Element STANDARD hinzufügen**.
* **Rechtsklicken Sie zweimal** auf das neue **STANDARD**-Element und wählen Sie jedes Mal **Element** hinzufügen. Daher sollte es zwei Elemente **[0]** und **[1]** geben, um die Zufluss- bzw. Abflussbedingungen zu definieren.
* **Definieren Sie den Artikel [0]** mit den folgenden **Zufluss**-Bedingungen:
  * Für **name** geben Sie `inflow` ein.
  * Für **string name** wählen Sie *inflow* (wie oben definiert).
  * Für **type** wählen Sie `uniform_in`
  * **Klicken Sie mit der rechten Maustaste auf **[0]** und wählen Sie **Element 'Slope'**.
  * Definieren Sie für das neue **slope** Element einen Wert von `0.0044`. Nachdem Sie den Steigungswert eingegeben haben, prüfen Sie, ob BASEMENT den Dezimaltrenner korrekt verstanden hat: Verwenden Sie den Dezimaltrenner Ihres Systemgebietsschemas (z. B. auf einer europäischen Tastatur muss möglicherweise `,` anstelle von `.` verwendet werden).
  * **Rechtsklick** auf **[0]** und **Element 'discharge file'** hinzufügen.
  * Klicken Sie in der neuen Zeile *discharge file* auf das Ordnersymbol, um die oben beschriebene Datei [steady-inflow.txt](https://github.com/hydro-informatics/materials-bm/raw/main/flows/steady-inflow.txt)] auszuwählen.
* **Definieren Sie Item [1]** mit den folgenden **Outflow**-Bedingungen:
  * Für **name** tap `outflow`.
  * For **string_name** select the above-defined `outflow` STRINGDEF.
  * Für **type** wählen Sie `uniform_out`
  * **Klicken Sie mit der rechten Maustaste auf **[1]** und wählen Sie **Element 'Slope'**.
  * Definieren Sie für das neue **slope** Element einen Wert von `0.0044`.

```{admonition} Liquid boundaries in practice
:class: note
In der Praxis könnte ein {term}`Wasserstands-Abfluss Beziehung <Stage-discharge relation>` für die nachgelagerte Randbedingung vorzuziehen sein, die in BASEMENT **type** = `hqrelation_out` entspricht. Der stromaufwärtige Zulaufzustand wird in der Praxis aber auch oft nur durch zeitabhängige Entladung vorgegeben, wie in diesem Tutorial gezeigt. Ein kritischer Faktor der Entladungsfunktion der Zeit ist der **Slope**-Feldwert, der dem Energiehang entspricht und oft als äquivalent zum Kanalhang angenommen wird. Diese Annahme gilt jedoch **nur für stetige Strömungen **, die in der Realität fast nie vorkommen. Deshalb werden in der Praxis oft quasi instationäre Strömungsverhältnisse in Form einer zeitabhängigen Abfolge von stetigen Entladungen verwendet, um beispielsweise einen Fluthydrographen zu modellieren.
```

{numref}`Figure %s <bm-hy-standard>` zeigt die Definitionen von STANDARD BOUNDARY-Elementen in der HYDRAULIC-Modell-Setup-Gruppe von BASEMENT.

```{figure} ../../img/basement/setup-hydraulics-standard.png
:alt: basement standard hydraulic boundary conditions
:name: bm-hy-standard

Der HYDRAULIC-Eintrag mit BOUNDARY > STANDARD-Definitionen für die vorgelagerten (Zufluss) und nachgelagerten (Abfluss) Flüssigkeitsmodellgrenzen.
```

Every surface has imperfections that cause turbulence when fluids such as water flow over it. The turbulences caused by surface imperfections result in decelerated flows near the surface. Since the water in rivers is almost always very close to the Earth's surface in the form of the riverbed relative to the imperfections of a riverbed, the influence of friction-induced turbulence is considerable. In hydrodynamic models, the friction-induced turbulence of the rough surface of riverbeds is accounted for by a **friction coefficient**, such as the **Strickler $k_{st}$** coefficient **or** its **inverse** value called **Manning's $n$**. The exercise on {ref}`ex-1d-hydraulics` in the *Python* chapter explains both roughness coefficients in more detail. This tutorial uses a global Strickler coefficient of $k_{st}$=30 (fictive units of m$^{1/3}$/s), which accounts for the characteristics of a meandering gravel-cobble riverbed {cite:p}`strickler_beitrage_1923`. To this end, **right-click** on the **HYDRAULICS** group and select **Add item FRICTION**. Define the new  **FRICTION** item with:

* **default friction** = 30.0
* **type** = `strickler`

Next, assign region-specific Strickler values for the five regions defined in {numref}`Tab. %s <region-defs-bm>`:

* **Rechtsklick** auf **FRICTION**> **Hinzufügen von Elementregionen**.
* **Klicken Sie mit der rechten Maustaste auf das neue **Regionen**-Element und wählen Sie **Element** hinzufügen (**fünfmal** für die fünf Regionen).
* Weisen Sie die in {numref}`Tab. %s <region-kst>` aufgeführten Werte **friction** und **region name** den **five regions items** zu.

```{list-table} Strickler values for HYDRAULIC FRICTION regions.
:header-rows: 1
:name: region-kst

* - Region
  - Flussbett
  - Blockrampen
  - Grasbanken
  - Überschwemmungsgebiete
  - Sand
* - **Reibung**
  - 34
  - 18
  - 24
  - 14
  - 39
* - **region name**
  - Flussbett
  - block ramp
  - gravel bank
  - Überschwemmungsgebiet
  - Sand Einlage
```


{numref}`Figure %s <bm-hy-friction>` zeigt die Definition der hydraulischen FRICTION-Elemente im BASEMENT-Modellaufbau.

```{figure} ../../img/basement/setup-hydraulics-friction.png
:alt: basement friction hydraulic boundary conditions strickler
:name: bm-hy-friction

Die HYDRAULICS Gruppe mit FRICTION Definitionen für das Modell und seine Regionen.
```

(bm-physical-props)=
## Physikalische Eigenschaften

Die Definition der Gruppe **PHYSICAL PROPERTIES** ist für BASEPLANE 2D obligatorisch. Dieses Tutorial verwendet die **default** physikalischen Eigenschaften (d.h. *gravity* ist `9.81`).

(bm-export-setup)=
## Write Setup File

Make sure that any potential warning or error message is resolved and that the model setup resembles {numref}`Fig. %s <ready2export-setup>`. Before exporting the project, save the simulation setup (click on the disk symbol in the top-right corner in {numref}`Fig. %s <ready2export-setup>`). Double-check that BASEMENT correctly wrote the files **model.json**, **simulation.json**, and **results.json** in the project directory (e.g., `/Basement/steady2d-tutorial/`). Export the model setup by clicking on the **Write** button (bottom-right corner in {numref}`Fig. %s <ready2export-setup>`).

```{figure} ../../img/basement/setup-ready2export.png
:alt: basement export model setup h5
:name: ready2export-setup

The final model setup to export (write) to a setup (`*.h5` {term}`HDF`) file.
```

Die Registerkarte **Konsole** wird automatisch aktiviert und informiert über den Exportfortschritt. Wenn die **Fehlerausgabe** Canvas nicht leer ist, überprüfen Sie die Fehlermeldungen und beheben Sie die Ursachen.

```{admonition} Out of range (NUM >= 110) in file ... Substance.cpp one line 188
:class: error

This error message can be related to an incoherent definition of string names in the .2dm mesh file and the model setup. Even varying capital letters could be the cause. For instance, if the last two lines (bottom of) `prepro-tutorial_quality-mesh-interp.2dm` define the liquid boundaries with all-lower letters `inflow` and `outflow`, but you called them `Inflow` and `Outflow`, correct the error either by renaming the strings at the bottom of the .2dm file, or correcting the `string_name` fields defined in the {ref}`HYDRAULICS section <bm-hydraulics>`.
```

(bm-sim-file)=
## Einrichtungssimulationsdatei

Nach dem erfolgreichen Export des Modell-Setups steht das **Simulation**-Band (links unter {numref}`Fig. %s <ready2export-setup>`) zum Einrichten der **simulation.json**-Datei im Projektordner zur Verfügung. Klicken Sie auf das Menüband **Simulation**, um die Datei *simulation.json* einzurichten:

* **Klicken Sie mit der rechten Maustaste auf die Gruppe **SIMULATION** in der aktivierten Registerkarte **Simulation Run** und wählen Sie **Element 'OUTPUT'**.
* **Klicken Sie mit der rechten Maustaste auf das neue **OUTPUT** Element, um fünf Ausgabetypen zu definieren:
    * **[0]** = `water_depth`
    * **[1]** = `water_surface`
    * **[2]** = `bottom_elevation`
    * **[3]** = `flow_velocity`
    * **[4]** = `ns_hyd_discharge`
* **Klicken Sie mit der rechten Maustaste auf die Gruppe **SIMULATION** und wählen Sie **Hinzufügen des Elements 'ZEIT'**.
* **Definieren Sie das **TIME** Element mit:
    * **end** = `15000.0`
    * **out** = `1000.0`
    * **start** = `0.0`

```{admonition} Discharge controls
The output parameter `ns_hyd_discharge` (*ns* denotes *nodestring*) enables us to verify the discharge mass balance at inflow and outflow boundaries (STRING_NAMEs), which is a **necessary requirement in practice**. Learn more about mass balance controls in the {ref}`simulation verification <bm-python>` section.
```

Die im TIME-Abschnitt definierten Werte beziehen sich auf die gleichen Zeiteinheiten wie in der oben heruntergeladenen und verknüpften Datei *steady-inflow.txt* definiert. {numref}`Figure %s <bm-sim-setup>` zeigt BASEMENT mit den Definitionen im Simulationsband.

```{figure} ../../img/basement/setup-simulation.png
:alt: basement simulation setup
:name: bm-sim-setup

Die Einrichtung des Simulationsbandes mit der Definition von fünf Ausgabeparametern und der Simulationszeit.
```

(bm-run)=
## Laufsimulation (Steady 2d)

The simulation can be run with different options that mainly affect the computing time (bottom of {numref}`Fig. %s <bm-sim-setup>`).

* Der **Standard-Hardware**-Rahmen ermöglicht den Wechsel zwischen Einzel- und Mehrfach-CPU-Auslastung. Die Standardoption ist Multithreaded, was bei modernen Computern dringend empfohlen wird.
* Der **Hochleistungs-Hardware**-Rahmen ermöglicht die Verwendung einer grafischen Verarbeitungseinheit (GPU), die deutlich schneller als die CPU sein kann, jedoch nur, wenn ein leistungsstarker Grafikprozessor verfügbar ist. Eine standardlangsame GPU hat keinen Vorteil und kann sogar die Berechnung verlangsamen. Wenn Sie sich über die GPU Ihres Computers nicht sicher sind, behalten Sie die Standardoptionen (alle ungültig).
* Der **Options**-Rahmen ermöglicht die Auswahl:
  * Die **Anzahl der CPU-Kerne **, die es ermöglicht, mehrere CPUs eines Computers zu verwenden. Moderne Computer haben meist mindestens 8 Kerne, die alle verwendet werden können, wenn Sie auf einem Server oder Computer arbeiten, der keinen anderen Zweck hat, als numerische Modelle auszuführen. Andernfalls halten Sie das System funktionsfähig, während die Simulation läuft, indem Sie die Hälfte der verfügbaren Kerne verwenden.
  * Numerische Präzision; für schnellere Simulationen wählen Sie **Single precision**. Für dieses Tutorial funktioniert * Double * Präzision auch ausreichend schnell, aber in der Praxis ist * Single * Präzision meist ausreichend und deutlich schneller.

```{admonition} How many CPUs does my computer have?
**Windows**-Benutzer können **Task Manager** starten (*Start* > tippen Sie auf `task manager`) und die Anzahl der verfügbaren Kerne im Tab **Performance** des Task Managers nachschlagen.

**Linux**-Benutzer erhalten einen Überblick über die Systemressourcen, indem sie {ref}`htop <install-htop>` installieren und verwenden.
```

To start the simulation click on the **Run** button on the bottom-right of the BASEMENT window. Depending on the hardware and performance settings (e.g., number of CPUs), the simulation of the tutorial model takes approximately 1-10 minutes. BASEMENT informs about the simulation progress in the **Console Output** frame, where the **Error Output** frame should remain empty (see {numref}`Fig. %s <bm-sim-end>`). If any error occurs, go back to the above sections (or even to the {ref}`mesh generation tutorial <qgis-tutorial>`) to fix errors.

```{figure} ../../img/basement/simulation-end.png
:alt: basement simulation end
:name: bm-sim-end

BASEMENT nach erfolgreicher Simulation.
```

### Exportsimulationsergebnisse

Sobald die Simulation erfolgreich abgeschlossen ist, gehen Sie zu BASEMENT's **Results** Band. Finden Sie die Gruppe **Ergebnisse ** in der Registerkarte **Export Simulation Ergebnisse ** und:

* **Klicken Sie mit der rechten Maustaste auf die Gruppe **Ergebnisse ** und wählen Sie **Hinzufügen Element 'EXPORT'**.
* **Klicken Sie mit der rechten Maustaste auf das neue **EXPORT**-Element und wählen Sie **Element hinzufügen**.
* Wählen Sie {term}`xdmf` im Feld **format** des neuen Elements **[0]**.

** Speichern Sie das Projekt** (Disk-Symbol in der oberen rechten Ecke) und finden Sie den **Export**, der unter {numref}`Fig. %s <bm-res-exp>` angegeben ist. Der Export der Simulationsausgaben nach **results.{term}`xdmf`** wird im **Console Output**-Frame bestätigt.

```{figure} ../../img/basement/setup-results-export.png
:alt: basement results export
:name: bm-res-exp

Einrichtung des Ergebnisbandes nach erfolgreicher Simulation.
```


# Nachbearbeitung mit QGIS

Start QGIS and create a new project or re-use the project from the {ref}`qgis-prepro-bm` tutorial. Save the new project with (a different) meaningful filename in the BASEMENT modeling folder (e.g., `/Basement/steady2d/`**postpro-tutorial.qgz**). Setup the project similarly as in the pre-processing:

* Verwenden Sie das Koordinatenreferenzsystem **Germany Zone 4** ({ref}`start-qgis`).
* Add a {ref}`satellite imagery basemap <basemap>` (XYZ tile) to facilitate the interpretation of the simulation results.
* Importieren Sie das höheninterpolierte Qualitätsnetz {ref}`prepro-tutorial_quality-mesh-interp.2dm <qualm-interp>` (**Layer** > **Layer** hinzufügen > ** Mesh Layer...**).


(qgis-imp-steps)=
## Import results.xdmf

Die Simulationsergebnisdatei **results.{term}`xdmf`** kann in QGIS als zusätzliche Datenquelle des höheninterpolierten Qualitätsgitters ({ref}`prepro-tutorial_quality-mesh-interp.2dm <qualm-interp>`) aus dem Vorverarbeitungs-Tutorial geladen werden:

* Im Fenster **Layers** klicken Sie **doppelklicken** auf **prepro-tutorial quality-mesh-interp.2dm**, um das Fenster **Layer Properties** zu öffnen.
* Gehen Sie im Fenster **Layer Properties** zum **Source**-Band.
* Klicken Sie im Rahmen **Verfügbare Datensätze ** (siehe {numref}`Fig. %s <qgis-assign-meshdata>`) auf die Schaltfläche **Zuweisen von zusätzlichem Datensatz zu Mesh ** <img src="../../img/qgis/sym-add-meshdata.png"> und wählen Sie `results.xdmf`.

```{admonition} Could not read mesh dataset.
:class: error

This error can be caused by two known formatting issues in BASEMENT. To troubleshoot it, have a look at our {ref}`chapter on debugging BASEMENT <dbg-bm-xdmf>`.
```

* Wählen Sie im **Static Dataset**-Rahmen eine **Scalar Dataset Group** aus und verwenden Sie den maximalen Zeitschritt (d.h. `625 d 00:00:00` im Falle der Simulationszeit $t$=15000 mit einem Ausgabeintervall von 1000).
* Klicken Sie auf **Apply** und **OK**.

{numref}`Figure %s <qgis-assign-meshdata>` zeigt einen beispielhaften Aufbau der Ausgangsdateninterpolation auf dem Rechennetz. Um andere Ausgabeparameter und/oder andere Simulationszeitschritte zu visualisieren, variieren Sie die Definitionen im **Static Dataset**-Rahmen.

```{figure} ../../img/qgis/bm-load-results.png
:alt: basement assign qgis metadata mesh
:name: qgis-assign-meshdata

Weisen Sie Mesh-Daten dem Computer-Mesh zu.
```

Um die Visualisierung der Ergebnisse zu verbessern, öffnen Sie erneut die **Layer Properties** der Mesh-Schicht und gehen Sie zum **Symbology**-Band. Visualisieren Sie einen Simulationsausgabeparameter wie **Fließgeschwindigkeit** wie folgt:

* In the **Settings tab** (hammer symbol in the top-left corner highlighted in {numref}`Fig. %s <symbology4u>`) find the **Groups** listbox.
* Suchen Sie in der Liste **Gruppen ** den zu visualisierenden Parameter (z. B. **Fließgeschwindigkeit **) und aktivieren Sie das Konturensymbol.
* Switch to the **Contours tab** next to the Settings tab (highlighted box in the top-left of {numref}`Fig. %s <symbology4u>`) and select a **Color Ramp**.
* Nach dem Definieren einer Visualisierung klicken Sie auf **Apply** und **OK**.

```{figure} ../../img/qgis/vis-flow-vel.png
:alt: basement qgis results velocity meshdata
:name: symbology4u

Visualisieren Sie den Parameter Fließgeschwindigkeit mit den Symbology-Steuerelementen. Die roten Kästchen markieren relevante Tabs und Einträge.
```

{numref}`Figure %s <qgis-plot-metadata>` veranschaulicht eine Visualisierung der Strömungsgeschwindigkeit am Ende der Simulation. Die Strömungsgeschwindigkeitsergebnisse sind auch als Videosequenz ([download](https://github.com/hydro-informatics/materials-bm/raw/main/exports/velocity-video-crayfish.avi)]) verfügbar.

```{figure} ../../img/qgis/bm-meshdata-u-plotted.png
:alt: plotted qgis basement results flow velocity
:name: qgis-plot-metadata

Nach Anwendung der oben genannten Symbologie-Einstellungen: Die Strömungsgeschwindigkeit ist in roten Tönen dargestellt.
```

(bm-rasterize-output)=
## Rasterisieren Outputs

The {ref}`raster` format is useful for many post-processing tasks such as map algebra (e.g., for habitat analysis or the assessment of inundation area and depth). To this end, QGIS provides the **Rasterize mesh dataset** tool for converting mesh data at any simulation timestep to a {ref}`Raster <raster>` (e.g., as {term}`GeoTIFF`). To open the *Rasterize mesh dataset* tool, go to either **Processing** > **Toolbox** or make sure that the **View** > **Panels** > **Processing Toolbox** is checked. In the **Processing Toolbox** click on the **Mesh** group and double click on **Rasterize mesh dataset** (see also {numref}`Fig. %s <qgis-rasterize-mesh-menu>`).

```{figure} ../../img/qgis/rasterize-mesh-menu.png
:alt: rasterize basement velocity water depth qgis
:name: qgis-rasterize-mesh-menu

Öffnen Sie das Rasterize Mesh Tool in der QGIS Processing Toolbox.
```

Führen Sie die folgenden Einstellungen im Fenster `Rasterize` aus (siehe auch {numref}`Fig. %s <qgis-rasterize-mesh>`):

* Stellen Sie die **Input Mesh Layer** auf `prepro-tutorial_quality-mesh-interp`.
* In the **Dataset groups** frame, click on the **...** button > **Select in Available Dataset Groups** and select **one parameter** (e.g., **flow_velocity**). Then, clicking on the **Go back** <img src="../../img/qgis/sym-go-back.png"> button. Make sure that the **Dataset groups** canvas contains only **1** selected **option**. Otherwise, the tool will create a messy multiband {ref}`Raster <raster>`.
* Aktivieren Sie im **Dataset time**-Rahmen die **Dataset group time step**-Funktaste und wählen Sie den letzten Simulationszeitschritt aus (z. B. `625 d 00:00:00`).
* Klicken Sie im Feld **Extent [optional]** auf die Schaltfläche **...** > **Berechnen aus Layer** > **prepro-tutorial quality-mesh-interp**.
* For **Pixel size** tap `2.0` meters (the larger this number, the coarser will be the output raster).
* Für **Ausgabe-Koordinatensystem** wählen Sie `Project CRS: ESRI:31494 - Germany_Zone_4`.
* Definieren Sie eine **Output-Rasterschicht**, indem Sie auf die Schaltfläche **...** > **In Datei speichern** klicken. Gehen Sie zum Zielverzeichnis (z. B. `C:/Basement/steady2-tutorial/`) und geben Sie einen Rasternamen ein, z. B. `u-end.tif` (`u` für Flussgeschwindigkeit, `end` für letzten Zeitschritt und `.tif` für {term}`GeoTIFF`). Klicken Sie auf **Save**.
* Klicken Sie auf die Schaltfläche **Run**, um das Rastern des Mesh-Datasets zu starten.

Schließen Sie nach der erfolgreichen Rasterung das Fenster **Rasterize Mesh Dataset** mit einem Klick auf die Schaltfläche **Close**.

```{figure} ../../img/qgis/rasterize-mesh.png
:alt: setup rasterize mesh geotiff
:name: qgis-rasterize-mesh

Einstellungen zum Export von Simulationsergebnissen mit dem Rasterize-Tool von QGIS.
```

Um die Visualisierung des neuen (Fließgeschwindigkeits-)Rasters zu verbessern, doppelklicken Sie auf das neue Raster im **Layers**-Panel und wechseln Sie zur Registerkarte **Symbology**. Wählen Sie **Singleband pseudocolor** für **Rendertyp** (im oberen Bereich des Fensters) und eine **Farbrampe**. Um Nullwertpixel zu unterdrücken, doppelklicken Sie auf die **Farbe ** des Feldes **0**-**Wert ** und reduzieren Sie im ** Farbfenster **Opacity ** auf **0$\%$**. {numref}`Figure %s <bm-exported-u-raster>` zeigt eine Beispielvisualisierung des exportierten Strömungsgeschwindigkeitsrasters.


```{figure} ../../img/qgis/bm-exported-u.png
:alt: basement output rasterize mesh geotiff visualization singleband pseudocolor
:name: bm-exported-u-raster

Eine Singleband-Pseudofarbe (Layer Properties > Symbology) stellt das exportierte GeoTIFF-Flussgeschwindigkeitsraster mit einer *Reds*-Farbrampe und Nullwertpixeln dar, die auf Null-Opazität eingestellt sind und auf Google-Satellitenbildern {cite:p}`googlesat` überlagert werden.
```

```{admonition} Analyze geodata results with Python
Erleichtern Sie die Konvertierung und Analyse von Geodaten mit effizienten {ref}`sec-geo-python`-Anwendungen und dem [flusstools](https://flusstools.readthedocs.io)-Paket].
```

(bm-crayfish)=
## Mesh Visualisierung mit Crayfish

Das Open-Source-Plugin [Crayfish](https://www.lutraconsulting.co.uk/projects/crayfish/)] ermöglicht die Visualisierung von Mesh-Werten (z. B. Änderung von Knotenwerten im Laufe der Zeit) mit vielen Funktionen, z. B. dem Export von Videoanimationen von Modellergebnissen. Um zum Beispiel ein Video der Ausgänge der Strömungsgeschwindigkeit in den 1 + 15 Simulationszeitschritten zu erstellen, verwenden Sie das Crayfish-Plugin wie folgt:

* Stellen Sie in QGIS sicher, dass das Crayfish-Plugin installiert ist (rufen Sie {ref}`QGIS instructions <qgis-tbx-install>` zurück).
* Wählen Sie im Feld **Layer** **prepro-tutorial quality-mesh-interp**.
* Mit *prepro-tutorial quality-mesh-interp* ausgewählt, gehen Sie zu **Mesh** (Top-Dropdown-Menü) > **Crayfish** > **Export-Animation ...** (wenn die Ebene nicht hervorgehoben ist, erscheint eine Fehlermeldung: *Bitte wählen Sie eine Mesh-Ebene für den Export*).
* Gehen Sie im Fenster **Export Animation** zur Registerkarte **Allgemein** und definieren Sie einen Ausgabedateinamen, indem Sie auf die Schaltfläche **...** klicken (z. B. `velocity-video.avi`).
* Klicken Sie auf **OK**.

Beim ersten Export eines Videos benötigt Crayfish die Definition eines **FFmpeg-Video-Encoders** und führt durch die Installation (falls erforderlich). Befolgen Sie die Anweisungen und starten Sie den Export des Videos erneut.

 ```{admonition} The resulting video export may look like this:

 <iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/AYG0i1becyI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
 ```

```{admonition} Make animations of other parameters
:class: note
Um Videos von anderen Simulationsparametern zu erstellen, ändern Sie den aktuell visualisierten Parameter des Meshs (*prepro-tutorial quality-mesh-interp*) als {ref}`explained above<qgis-imp-steps>`.
```


(bm-paraview)=
# Nachbearbeitung mit ParaView

*ParaView* ist eine frei verfügbare Visualisierungssoftware, die es ermöglicht, die Datei *results.{term}`xdmf`* von BASEMENT für wissenschaftliche Zwecke zu zeichnen und zu verarbeiten. Download und Installation (erfordert **Admin**/**sudo** Rechte) der neuesten Version von *ParaView* von deren [Website](https://www.paraview.org/download/) (falls noch nicht fertig).

## Import results.xdmf
Öffnen Sie *ParaView* und **klicken Sie auf das Ordnersymbol** (oben links im Fenster, das unter {numref}`Fig. %s <fig-pv-import>` angezeigt wird), um die Simulationsergebnisse zu laden (`results.xdmf`). *ParaView* kann darum bitten, ein geeignetes XDMF-Lese-Plugin auszuwählen: **Wählen Sie `XDMF Reader`** und klicken Sie auf `OK`. Jetzt sollte der `results.xdmf` im **Pipeline Browser** sichtbar sein und der **Apply** Button ist grün geworden (klicken Sie darauf).

```{figure} ../../img/paraview/import-results.png
:alt: basement results paraview
:name: fig-pv-import

ParaView nach erfolgreichem Import der Modellergebnisse (results.xdmf).
```

(pv-vis)=
## Visualisieren von Parametern
ParaView shows by default one of the result parameters at timestep 0 (i.e., bare, dry terrain). To explore other parameters, select them in the dropdown menu of the **Active Variable Controls** menu bar (red highlight box in {numref}`Fig. %s <fig-pv-vis>`). The *Active Variable Controls* menu bar also contains options for manipulating the color range and legend. Toggle through the timesteps by using the video control buttons in the **VCR Controls** toolbar (light blue highlight box in {numref}`Fig. %s <fig-pv-vis>`).


```{figure} ../../img/paraview/vis-u.png
:alt: basement results paraview
:name: fig-pv-vis

Die Active Variable Controls (rotes Feld) und VCR Controls (hellblaues Feld) in ParaView, um Ausgabeparameter in verschiedenen Zeitschritten zu visualisieren.
```

```{admonition} Familiarize with the Viewport
The Viewport (default `Layout #1`) provides many tools for zooming into the model and changing perspectives between 2d and 3d. Click in the Viewport and hold the left mouse button to change perspectives. Take a couple of minutes to familiarize with the perspectives.
```

Um eine Animation eines Ausgabeparameters** über die Zeit als Film (z.B. `avi`) oder Bild (z.B. `jpg`, `png`, `tiff`) zu exportieren, gehen Sie zu **File** > **Save Animation...**.


## Projektpipeline retten
Mit seinem Ansatz von Sequenzen programmierbarer Filteranwendungen speichert ParaView einen *Current State* im PVSM-Format und nicht ein Projekt wie in QGIS. Der aktuelle Zustand eines Datensatzes in ParaView kann als `pvsm` Datei über **File** > **Save State File** gespeichert werden. **Save** den aktuellen Zustand des Tutorials ParaView Projekt, zum Beispiel im Simulationsordner als **pv-project.pvsm**. Um einen vorhandenen ParaView-Status (d.h. Projekt) zu laden, gehen Sie zu **File** > **Load state**.

```{admonition} Automate ParaView Pipelines
Die Statusdatei kann auch als Python-Skript gespeichert werden, um automatisierte Pipelines und Exporte zu nutzen (mehr dazu im Kapitel {ref}`Python <standalone>`).
```

(pv-exp-data)=
## Ausfuhrdaten
Similar to QGIS, output parameter datasets can be extracted, manipulated, or transformed in ParaView. For this purpose, programmable filters can be applied to the original dataset in ParaView to calculate (i.e., apply the **Calculator** <img src="../../img/paraview/sym-calc.png"> filter), for example, the Froude number from the water depth and flow velocity datasets (read more in the [ParaView Wiki](https://www.paraview.org/Wiki/Python_calculator_and_programmable_filter)). This tutorial only features the export of mesh point data to a {term}`CSV` file with programmable filters:

* Make sure that the **Time** in the **Current Time Controls** toolbar (light blue box in {numref}`Fig. %s <fig-pv-cell-centers>`) is set to 15000 (maximum timestep).
* Im **Pipeline-Browser** **klicken Sie mit der rechten Maustaste** auf `results.xdmf` > ** Filter** hinzufügen > **Alphabetisch** (d.h. eine Liste aller verfügbaren Filter) > **Zellzentren**.
* Aktivieren Sie im **CellCenters1** **Eigenschaften** das Feld **Vertex Cells** und klicken Sie auf den jetzt wieder grünen **Apply** Button (siehe {numref}`Fig. %s <fig-pv-cell-centers>`).
* To save the currently active vertex data **press  `CTRL` + `S` on the keyboard**, which opens a *Save File* dialogue window. In the **Save File** window:
  * Navigate to a target folder (e.g., the simulation folder `/Basement/steady2d-tutorial/`)
  * Geben Sie einen ** Dateinamen** ein (z. B. `flow_velocity.csv`)
  * Wählen Sie im Dropdown-Feld **Files of type** **Comma oder Tab Delimited Files(`*.csv *.tsv *.txt`)** aus.
  * Klicken Sie auf **OK**.
* Das Fenster **Configure Writer (CSV Writer)** wird geöffnet:
  * Aktivieren Sie das Feld **Choose Array To Write**.
  * Wählen Sie nur **Fließgeschwindigkeit points** (oder mehr/andere Parameter).
  * Behalten Sie alle anderen Standardwerte.
  * Klicken Sie auf **OK**.

```{figure} ../../img/paraview/cell-centers.png
:alt: paraview basement export data
:name: fig-pv-cell-centers

Anwendung des programmierbaren CellCenter-Filters in ParaView mit dem maximalen Zeitschritt, der in der Symbolleiste Aktuelle Zeitsteuerungen (hellblaues Feld) definiert ist.
```

Jetzt wurde eine *Fließgeschwindigkeit.*{term}`CSV` Datei geschrieben, die Punktkoordinaten (x, y und z Koordinaten) und Fließgeschwindigkeit in *x* (Fließgeschwindigkeit:0) und *y* (Fließgeschwindigkeit:1) Richtungen enthält. Die Fließgeschwindigkeit:2 (*z*-Richtung) ist in dieser 2d-Simulation immer Null. Die Datei *Fließgeschwindigkeit.*{term}`CSV` kann auch mit QGIS verwendet werden (z. B. in QGIS gehen Sie zu **Layer** >) **Layer hinzufügen**> **Hinzufügen Delimited Text Layer...** > wählen Sie *Fließgeschwindigkeit.csv*, weisen Sie die richtigen Spalten und Trennzeichen zu > klicken Sie auf **Hinzufügen**.

```{admonition} Challenge: Calculate the absolute velocity
Importieren Sie *Fließgeschwindigkeit.csv* in QGIS und berechnen Sie die absolute Strömungsgeschwindigkeit $U$ aus $u_x$ (Fließgeschwindigkeit:0) und $u_y$ (Fließgeschwindigkeit:1) als $U = \sqrt{u^2_x + u^2_y}$. Wie entsprechen die Flussfelder dem oben erstellten `u-end.tif` (siehe {ref}`bm-rasterize-output`) Raster?
```

(bm-python)=
# Python Simulation Verifizierung
Die Entwickler von BASEMENT an der ETH Zürich stellen eine Suite von [Python scripts](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/)] zur Nachbearbeitung der Simulationsergebnisse zur Verfügung. Für das hier verwendete BASEMENT v3 laden Sie das Python-Skript [BMv3NodestringResults.py](http://people.ee.ethz.ch/~basement/baseweb/download/tools/python-scripts/BMv3NodestringResults.py)] herunter, das definierte Ausgabeparameter unter dem benutzerdefinierten {ref}`STRINGDEFs <bm-geo-fin>` exportiert.

Um das Python-Skript auszuführen, {ref}`install Python <install-python>` für Ihre Plattform zusammen mit den Paketen `numpy` und `h5py`.

```{admonition} Guidance for installing Python
Consider to install Python in a {ref}`conda-env` (*Windows*) or a {ref}`venv (pip) <pip-env>` (*Linux*) with [flusstools](https://flusstools.readthedocs.io), which already includes all requirements for running *BMv3NodestringResults.py*.
```

Zum Ausführen des * Python * Skripts auf jeder Plattform:

* Optional aktivieren Sie die entsprechende * Python * (Conda oder venv) Umgebung.
* `cd` (Verzeichnis ändern) in den Simulationsordner.
* Führen Sie `python BMv3NodestringResults.py`.

Im einzelnen sieht dies wie folgt aus:

`````{tab-set}
````{tab-item} Windows / conda
Starten Sie *Windows* oder *Anaconda Prompt* und tippen Sie (erfordert, dass die conda-Umgebung {ref}`flussenv <conda-quick>` installiert ist):
```
conda activate flussenv
cd C:\Basement\steady2d-tutorial\
python BMv3NodestringResults.py
```
````

````{tab-item} Linux / pip
Launch *Linux Terminal* and tap (requires that the pip environment {ref}`vflussenv <pip-quick>` is installed in the HOME directory):
```
cd ~
source vflussenv/bin/activate
cd /Basement/steady2d-tutorial/
python BMv3NodestringResults.py
```

Wenn {ref}`vflussenv <pip-quick>` in einem anderen Verzeichnis als HOME installiert ist, ersetzen Sie `cd ~` in der ersten Zeile des obigen Codeblocks durch das übergeordnete Installationsverzeichnis von {ref}`vflussenv <pip-quick>`.
````
`````

{numref}`Figure %s <export-py>` illustriert das Ausführen von *BMv3NodestringResults.py* auf *Windows* in *Anaconda Prompt*.

```{figure} ../../img/basement/export-ns-py.png
:alt: export nodestring python script basement BMv3NodestringResults
:name: export-py

Ein Python Anaconda Prompt Fenster mit BMv3NodestringResults.py
```

Durch Ausführen des *Python*-Skripts werden drei {term}`CSV`-Dateien generiert, die Werte unter dem benutzerdefinierten {ref}`STRINGDEFs <bm-geo-fin>` enthalten:

* **Discharge.csv** enthält Zu- und Abflüsse.
* **results.csv** enthält jeden OUTPUT-Parameter, der in {ref}`simulation setup file <bm-sim-file>` definiert ist.
* **timestep.csv** listet die Anzahl der OUTPUT-Parameter-Timesteps auf.

The primarily important file is **Discharge.csv**, from which can be read when inflow and outflow converge in a steady-state simulation (i.e., **the simulation stabilizes**). A steady simulation in which the sum of all inflows does not equal all outflows must be considered erroneous. For instance, if the sum of outflows in the last timestep is smaller than the sum of inflows, then the simulation time is too short. The diagram in {numref}`Fig. %s <convergence-diagram-bm>` plots inflow and outflow for the simulation setup of this tutorial. The diagram suggests that the model reaches stability after timestep 11 (simulation time $t \leq 11000$). Thus, the simulation time could be limited to $t = 12000$, but a simulation time of $t = 10000$ would be too short.

```{figure} ../../img/basement/convergence-diagram.png
:alt: basement convergence model simulation discharge verification validation
:name: convergence-diagram-bm

Konvergenz von Zu- und Abfluss an den Modellgrenzen.
```


```{admonition} Checkup: discharge convergence
Note the difference between the convergence duration in this steady simulation with BASEMENT (plot in {numref}`Fig. %s <convergence-diagram-bm>`) that starts with a dry model compared to the steady Telemac2d tutorial (plot in {numref}`Fig. %s <steady-flux-convergence>`).

* **Ständige Erhöhung der Entladung in einer stetigen Simulation**<br> Die Definition von {ref}`upstream_direction <bm-geo-fin>` (z. B. falsch definiert als `"left"` oder `"right"`) kann diesen Fehler verursachen.
* **Abfluss kleiner als Inflow**<br>Erhöhen Sie die Simulationszeit (siehe {ref}`bm-sim-file`).
* **Kein Wasser im Modell**<br> Die in der Datei *steady-inflow.txt* definierte Entladung (siehe Abschnitt {ref}`bm-hydraulics`) muss angemessene Flüsse in der Simulationszeit definieren. Darüber hinaus kann die Definition von {ref}`upstream_direction <bm-geo-fin>` (z. B. falsch definiert als `"left"` oder `"right"`) diesen Fehler verursachen. Abhängig von den Regionseinstellungen Ihres Systems verwenden Sie das englische **`.`** anstelle des europäischen **`,`** Dezimalbegrenzungszeichens, um Entladungen in *steady-inflow.txt* zu definieren.
```

**What next?**
: The verification of the model stability represents only one step on the pathway to a useable model in practice. Before a numerical model can be used for simulating decision-making scenarios, it must be calibrated and validated with measurement data (similar to TELEMAC {ref}`hydrodynamics <tm2d-calibration>`). 
