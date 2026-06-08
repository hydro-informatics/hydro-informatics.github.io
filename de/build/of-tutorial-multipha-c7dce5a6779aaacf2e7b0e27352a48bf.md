---
description: Tutorial zur Nachbearbeitung von OpenFOAM-Simulationen mit ParaView.
---

# Nachbearbeitung

Die Nachbearbeitung ist ein entscheidender Schritt zum Verständnis und zur Analyse der Ergebnisse von {term}`CFD`Simulationen, insbesondere für Mehrphasen-Szenarien. Dieses Tutorial ist konzipiert, um Sie durch die wesentlichen Schritte zu führen, um aussagekräftige Einblicke aus den OpenFOAM-Simulationen zu gewinnen und die Visualisierung und Analyse mit ParaView (ParaFoam) zu betonen. Auf dieser Seite erfahren Sie, wie Sie Tools wie ParaView effizient nutzen können, um Simulationsergebnisse zu interpretieren, OpenFOAM-Ausgänge zu manipulieren und zu verarbeiten.

`````{admonition} Visualization software: ParaView and alternatives
:class: tip

OpenFOAM Nachbearbeitung kann mit paraFoam, einem Software-Modul, das mit OpenFOAM verschifft, durchgeführt werden. ParaFOAM ist eine spezialisierte Version von ParaView, die konfiguriert ist, OpenFOAM-Datendateien ohne zusätzliche Plugins direkt zu verarbeiten. ParaView ist ein universelles Open-Source-Visualisierungstool zur Analyse und Visualisierung großer Datensätze. ParaFOAM ist auf OpenFOAM-Nutzer mit integrierter Kompatibilität zugeschnitten, während ParaView zusätzliche Schritte benötigt, um OpenFOAM-Formate zu lesen, unterstützt aber ein breiteres Spektrum an Datentypen und Analysepipelines.

Um direkt mit ParaView anstelle von paraFOAM zu arbeiten, führen Sie entweder das von OpenFOAM bereitgestellte `foamToVTK`-Dienstprogramm aus, um die Simulationsergebnisse in VTK-kompatible Dateien umzuwandeln, die ParaView natives lesen oder ParaView-Plugins verwenden kann. So kann das **OpenFOAM Reader** Plugin eine `.foam`-Datei laden (typischerweise erstellt im Simulationsfallverzeichnis durch Hinzufügen einer leeren Datei namens `<case>.foam`) und ParaView wird den Fall mit dem Plugin parse.

Alternative Software umfasst Tools wie [VisIt](https://visit-dav.github.io/visit-website/index.html), die ParaView ähnliche Visualisierungsfunktionen bietet. VisIt ist auch Open-Source-Visualisierungssoftware und verfügt über eine intuitive Schnittstelle.

````{admonition} Enable VisIt for OpenFOAM
:class: note, dropdown

Um VisIt für die Analyse der OpenFOAM-Simulationsausgabe zu verwenden, folgen Sie diesen Schritten:

1. Laden Sie VisIt von https://visit-dav.github.io/visit-website/index.html herunter und installieren Sie die erforderlichen Systemabhängigkeiten.

2. Da VisIt nicht native OpenFOAM-Dateien liest, konvertieren Sie die Simulationsdaten in ein mit VisIt kompatibles Format, wie VTK. Nutzen Sie dazu das `foamToVTK` Dienstprogramm von OpenFOAM:

   ```bash
   foamToVTK
   ```

Dies generiert VTK-Dateien in einem `VTK`-Verzeichnis in Ihrem Simulationsfallordner.

3. Um Daten in VisIt zu laden, (open VisIt) navigieren Sie auf das `VTK`-Verzeichnis, das von `foamToVTK` erstellt wurde, und laden Sie die Ziel-VTK-Dateien. Wählen Sie relevante Felder wie Geschwindigkeit, Druck oder andere Größen zur Visualisierung aus.

4. Um Daten zu erforschen, verwenden Sie VisIts Visualisierungstools, wie Slicing, Konturing, Vektorfeldplotierung und zeitliche Evolutionsvisualisierung für dynamische Simulationen.

Individuelle Analyse kann durch die Nutzung der Scripting-Funktionen von VisIt oder mittels fortschrittlicher Filter durchgeführt werden, um spezifische Analysen durchzuführen, wie die Integration von Durchflussmengen, Exportdaten oder die Visualisierung komplexer Interaktionen in Ihren Ergebnissen.

````

`````

## Simulationsdaten abrufen

Für den Fall, dass die Simulationen parallel ausgeführt wurden, besteht der erste Schritt vor der Nachbearbeitung der Daten darin, alle Lösungsschritte des analysierten Falles zu rekonstruieren (d.h. wieder zusammenzubauen). Dies kann entweder für alle Zeitschritte oder nur für einen bestimmten erfolgen. Die Befehle, die im Terminalfenster eingegeben werden müssen, sind unten dargestellt:

* Um alle Lösungsschritte zu rekonstruieren:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar
```
  
* Um einen bestimmten Zeitschritt zu rekonstruieren (ersetzt "x" mit dem Zeitschritt):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar -time x
```

## Visualisierung mit ParaView (paraFoam)

ParaFoam ist eine kundenspezifische Version der ParaView-Visualisierungssoftware, die vorkonfiguriert wird, um OpenFOAM-Simulationsdaten direkt zu lesen und zu verarbeiten. Es vereinfacht die Nachbearbeitung durch die Integration von OpenFOAM-spezifischen Dateiformaten und Funktionalitäten, so dass Benutzer Felder visualisieren, Einblicke entnehmen und Ergebnisse ohne zusätzliche Einrichtung analysieren können.

Die Arbeit mit paraFoam erfordert, dass der Simulationsfall aufgebaut wurde (siehe oben Abschnitt). Ein Simulationsfall bezieht sich auf den kompletten Satz von Dateien und Konfigurationen, die erforderlich sind, um ein bestimmtes Simulationssszenario zu definieren, auszuführen und zu analysieren. Es umfasst die Geometrie und das Netz der Rechendomäne, Anfangs- und Randbedingungen, Lösungseinstellungen, physikalische Modelle und alle zusätzlichen Parameter, die für die Simulation notwendig sind. Der Fall wird in Verzeichnisse wie `constant` (Materialeigenschaften und Mesh), `system` (solver controls) und `0` (Initial-Bedingungen) organisiert und bildet einen strukturierten Rahmen für numerische Experimente.

### Einführung paraFoam

Sobald der Fall rekonstruiert wurde, wie für den Meshing-Prozess, kann der folgende Befehl verwendet werden, um den Fall in der Software ParaView zu visualisieren:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ paraFoam
```

### Visualisierungspipelines

Der *Kanal. OpenFOAM* sollte nun im Pipeline-Browser vorhanden sein und diese im Layout visualisieren, die *Apply*-Taste drücken. Zusätzlich werden im *Fields*-Bereich die verschiedenen, visualisierbaren Felder angezeigt und können entsprechend dem Fokus der Analyse ausgewählt/ausgewählt werden.

```{figure} ../../img/openfoam/interFoam/Paraview/channelOpenFOAM.png
:alt: openfoam 
:name: of-channelOpenFOAM

Visualisierung der Fallergebnisse in ParaView.
```

Um die Luft- und Wasserphasen zu visualisieren, sollte *alpha.water* im Dropdown-Menü ausgewählt werden, wie im Bild unten gezeigt.

```{figure} ../../img/openfoam/interFoam/Paraview/view-alpha-water.png
:alt: openfoam 
:name: of-view-alphawater

Aktivieren Sie die Einstellung zum Betrachten der Luft- und Wasserphasen in ParaView.
```

Um den gezeigten Zeitschritt zu ändern, können die Pfeile verwendet werden, die in dem rot markierten Bereich zu sehen sind.


```{figure} ../../img/openfoam/interFoam/Paraview/final-time-step.png
:alt: openfoam timestep time step
:name: of-final-time-step

Optionen zur Änderung des zu visualisierenden Zeitschritts.
```

Als nächstes wird zur Visualisierung nur die Wasserphase der Filter *Clip* verwendet. Dies kann entweder im Abschnitt *Filter* im Menü gefunden werden, oder alternativ kann die Verknüpfung verwendet werden. Der *Clip Type* sollte auf *Scalar* eingestellt werden, wobei *alpha.water* als Skalar gewählt wird und der Wert auf 0,5 eingestellt wird, was die Schnittstelle zwischen Luft und Wasser darstellt. Um die Luftphase anzuzeigen, sollte die *Invert*-Option gewählt werden, während für die Wasserphase sie entsorgt werden sollte.

```{figure} ../../img/openfoam/interFoam/Paraview/clip-water.png
:alt: openfoam clip water interFoam
:name: of-clip-water


Clip-Filter zum Betrachten der Wasserphase in ParaView.
```

Um schließlich auch die Wände und Patches zur Ansicht hinzuzufügen, kann der *Extract Block* Filter implementiert werden (klicken Sie auf den *-Kanal. OpenFOAM* Datei vor der Applikation).

```{figure} ../../img/openfoam/interFoam/Paraview/extract-block.png
:alt: openfoam 
:name: of-extract-block

Liste der Filter in ParaView, Highlighting ExtractBlock.
```

Die interessierenden Patches können dann entweder ausgewählt oder ausgewählt werden, und das *Coloring* kann auf Solid Color eingestellt werden.

```{figure} ../../img/openfoam/interFoam/Paraview/choose-patches.png
:alt: openfoam 
:name: of-choose-patches

Verfügbare Optionen zur Auswahl der Patches und zur Änderung der Farbe.
```

Die sich daraus ergebende Sicht auf die Wasserphase und die Blockextraktion ist nachstehend dargestellt:

```{figure} ../../img/openfoam/interFoam/Paraview/alpha-water.png
:alt: openfoam 
:name: of-alpha-water

Simulationsergebnisse zur Wasserphase.
```

Verschiedene Parameter können auch betrachtet werden, wie die Strömungsgeschwindigkeit, und dies kann im *Coloring*-Bereich durch Auswahl *U* erfolgen. Der *preset* kann geändert werden, um die Ergebnisse durch die Auswahl des entsprechenden Icons besser anzuzeigen (grün hoch beleuchtet).

```{figure} ../../img/openfoam/interFoam/Paraview/flow-velocity.png
:alt: openfoam 
:name: of-flow-velocity

Simulationsergebnisse zeigen die Strömungsgeschwindigkeit.
```

