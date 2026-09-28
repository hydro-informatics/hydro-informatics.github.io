---
description: Tutorial zur Nachbearbeitung von OpenFOAM-Simulationen mit ParaView.
---

# Nachbearbeitung

Die Nachbearbeitung ist ein entscheidender Schritt zum Verständnis und zur Analyse der Ergebnisse von {term}`CFD`-Simulationen, insbesondere für Multiphasenflussszenarien. Dieses Tutorial soll Sie durch die wesentlichen Schritte des Extrahierens sinnvoller Erkenntnisse aus OpenFOAM-Simulationen führen und die Visualisierung und Analyse mit ParaView (ParaFoam) betonen. Auf dieser Seite erfahren Sie, wie Sie Tools wie ParaView effizient nutzen, um Simulationsergebnisse zu interpretieren, OpenFOAM-Ausgaben zu manipulieren und zu verarbeiten.

`````{admonition} Visualization software: ParaView and alternatives
:class: tip

Die OpenFOAM-Nachbearbeitung kann mit paraFoam durchgeführt werden, einem Softwaremodul, das mit OpenFOAM ausgeliefert wird. ParaFOAM ist eine spezielle Version von ParaView, die für die direkte Verarbeitung von OpenFOAM-Datendateien ohne zusätzliche Plugins konfiguriert ist. ParaView ist ein universelles Open-Source-Visualisierungstool zur Analyse und Visualisierung großer Datensätze. ParaFOAM ist auf OpenFOAM-Benutzer mit integrierter Kompatibilität zugeschnitten, während ParaView zusätzliche Schritte zum Lesen von OpenFOAM-Formaten erfordert, aber eine breitere Palette von Datentypen und Analysepipelines unterstützt.

To directly work with ParaView in lieu of paraFOAM, either run the `foamToVTK` utility provided by OpenFOAM to convert the simulation results into VTK-compatible files that ParaView can natively read, or use ParaView plugins. For instance, the **OpenFOAM Reader** plugin allows to load a `.foam` file (typically created in the simulation case directory by adding an empty file named `<case>.foam`) and ParaView will parse the case using the plugin.

Alternative Software enthält Tools wie [VisIt](https://visit-dav.github.io/visit-website/index.html), die ähnliche Visualisierungsmöglichkeiten wie ParaView bieten.] VisIt ist auch Open-Source-Visualisierungssoftware und verfügt über eine intuitive Benutzeroberfläche.

````{admonition} Enable VisIt for OpenFOAM
:class: note, dropdown

Um VisIt zur Analyse der OpenFOAM-Simulationsausgabe zu verwenden, führen Sie die folgenden Schritte aus:

1. Download and install VisIt from https://visit-dav.github.io/visit-website/index.html (ensure you have the required system dependencies).

2. Da VisIt keine OpenFOAM-Dateien nativ liest, konvertieren Sie die Simulationsdaten in ein mit VisIt kompatibles Format wie VTK. Verwenden Sie dazu das von OpenFOAM bereitgestellte `foamToVTK`-Dienstprogramm:

   ```bash
   foamToVTK
   ```

Dadurch werden VTK-Dateien in einem `VTK`-Verzeichnis in Ihrem Simulationsordner generiert.

3. Um Daten in VisIt zu laden (Open VisIt), navigieren Sie zum `VTK`-Verzeichnis, das von `foamToVTK` erstellt wurde, und laden Sie die Ziel-VTK-Dateien. Wählen Sie relevante Felder wie Geschwindigkeit, Druck oder andere Größen für die Visualisierung aus.

4. Um Daten zu erforschen, verwenden Sie die Visualisierungstools von VisIt, wie z. B. Schneiden, Konturieren, Vektorfeldgrafik und Visualisierung der zeitlichen Entwicklung für dynamische Simulationen.

Maßgeschneiderte Analysen können durch die Nutzung der Skriptfunktionen von VisIt oder die Verwendung fortschrittlicher Filter zur Durchführung spezifischer Analysen, wie z. B. die Integration von Flussmengen, den Export von Daten oder die Visualisierung komplexer Interaktionen in Ihren Ergebnissen, implementiert werden.

````

`````

## Abrufsimulationsdaten

In dem Fall, in dem die Simulationen parallel durchgeführt wurden, besteht der erste Schritt darin, alle Lösungsschritte des analysierten Falls zu rekonstruieren (d.h. wieder zusammenzusetzen). Dies kann entweder für alle Zeitschritte oder nur für einen bestimmten erfolgen. Die Befehle, die im Terminalfenster eingegeben werden müssen, sind unten dargestellt:

* Zur Rekonstruktion aller Lösungsschritte:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar
```
  
* Um einen bestimmten Zeitschritt zu rekonstruieren (ersetzen Sie "x" mit dem Zeitschritt):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar -time x
```

## Visualisierung mit ParaView (paraFoam)

ParaFoam ist eine angepasste Version der ParaView-Visualisierungssoftware, die vorkonfiguriert ist, um OpenFOAM-Simulationsdaten direkt zu lesen und zu verarbeiten. Es vereinfacht die Nachbearbeitung durch die Integration von OpenFOAM-spezifischen Dateiformaten und -Funktionalitäten, sodass Benutzer Felder visualisieren, Erkenntnisse extrahieren und Ergebnisse ohne zusätzliche Einrichtung analysieren können.

Working with paraFoam requires that the simulation case has been constructed (see above section). A simulation case refers to the complete set of files and configurations required to define, run, and analyze a specific simulation scenario. It includes the geometry and mesh of the computational domain, initial and boundary conditions, solver settings, physical models, and any additional parameters necessary for the simulation. The case is organized into directories such as `constant` (material properties and mesh), `system` (solver controls), and `0` (initial conditions), forming a structured framework for numerical experiments.

### Start paraFoam

Sobald der Fall wie beim Meshing-Prozess rekonstruiert wurde, kann der folgende Befehl verwendet werden, um den Fall in der Software ParaView zu visualisieren:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ paraFoam
```

### Visualisierungspipelines

Der *Kanal. OpenFOAM* sollte nun im Pipeline-Browser vorhanden sein und um es im Layout zu visualisieren, drücken Sie die Schaltfläche *Apply*. Zusätzlich werden im Abschnitt *Felder* die verschiedenen visualisierbaren Felder dargestellt und können entsprechend dem Fokus der Analyse ausgewählt/ausgewählt werden.

```{figure} ../../img/openfoam/interFoam/Paraview/channelOpenFOAM.png
:alt: openfoam 
:name: of-channelOpenFOAM

Die Visualisierung des Falls führt zu ParaView.
```

Um die Luft- und Wasserphasen zu visualisieren, sollte *alpha.water* dann im Dropdown-Menü ausgewählt werden, wie im Bild unten gezeigt.

```{figure} ../../img/openfoam/interFoam/Paraview/view-alpha-water.png
:alt: openfoam 
:name: of-view-alphawater

Aktivieren der Einstellung zum Anzeigen der Luft- und Wasserphasen in ParaView.
```

Um den gezeigten Zeitschritt zu ändern, können die Pfeile verwendet werden, die in dem rot markierten Bereich zu sehen sind.


```{figure} ../../img/openfoam/interFoam/Paraview/final-time-step.png
:alt: openfoam timestep time step
:name: of-final-time-step

Optionen zum Ändern des zu visualisierenden Zeitschritts.
```

Als nächstes, um nur die Wasserphase zu visualisieren, wird der * Clip * Filter verwendet. Dies kann entweder im Abschnitt *Filter* im Menü gefunden werden, oder alternativ kann die Verknüpfung verwendet werden. Der *Clip-Typ* sollte auf *Scalar* gesetzt werden, wobei *alpha.water* als Skalar ausgewählt wird und der Wert auf 0,5 gesetzt wird, was die Schnittstelle zwischen Luft und Wasser darstellt. Um die Luftphase anzuzeigen, sollte die Option *Invert* ausgewählt werden, während sie für die Wasserphase deaktiviert werden sollte.

```{figure} ../../img/openfoam/interFoam/Paraview/clip-water.png
:alt: openfoam clip water interFoam
:name: of-clip-water


Clipfilter zur Anzeige der Wasserphase in ParaView.
```

Um schließlich auch die Wände und Patches zur Ansicht hinzuzufügen, kann der Filter *Extrahieren Block * implementiert werden (klicken Sie auf den *Kanal). OpenFOAM*-Datei vor dem Anwenden.

```{figure} ../../img/openfoam/interFoam/Paraview/extract-block.png
:alt: openfoam 
:name: of-extract-block

Liste der in ParaView verfügbaren Filter, Hervorhebung ExtractBlock.
```

Die Patches von Interesse können dann entweder ausgewählt oder deaktiviert werden, und die *Farbe * kann auf Solid Color gesetzt werden.

```{figure} ../../img/openfoam/interFoam/Paraview/choose-patches.png
:alt: openfoam 
:name: of-choose-patches

Verfügbare Optionen zum Auswählen der Patches und Ändern der Farbe.
```

Die resultierende Ansicht der Wasserphase und Blockextraktion ist unten dargestellt:

```{figure} ../../img/openfoam/interFoam/Paraview/alpha-water.png
:alt: openfoam 
:name: of-alpha-water

Simulationsergebnisse, die die Wasserphase hervorheben.
```

Es können auch verschiedene Parameter angezeigt werden, wie z.B. die Strömungsgeschwindigkeit, und dies kann im Abschnitt *Coloring* durch Auswahl von *U* erfolgen. Der * preset* kann geändert werden, um die Ergebnisse besser anzuzeigen, indem das entsprechende Symbol ausgewählt wird (grün markiert).

```{figure} ../../img/openfoam/interFoam/Paraview/flow-velocity.png
:alt: openfoam 
:name: of-flow-velocity

Simulationsergebnisse, die die Strömungsgeschwindigkeit hervorheben.
```

