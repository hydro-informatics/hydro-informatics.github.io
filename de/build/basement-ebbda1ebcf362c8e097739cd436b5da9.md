---
description: Komplettes Tutorial zum Einrichten und Ausführen von 2D hydrodynamischen numerischen Simulationen mit BASEMENT (ETH Zürich), das BASEHPC-Modellaufbau, Steady-State-Modellierung und Ergebnisvisualisierung abdeckt.
---

(chpt-basement)=
# GRUNDLAGE

```{admonition} Old BASEMENT versions, BASEMD, and BASEHPC
:class: important

BASEMENT Version 2 (v2) wurde mit komplexen Strukturen und einer breiten Palette von Kapazitäten entwickelt, wobei der Schwerpunkt jedoch wenig auf der Rechenzeit lag. BASEMENT Version 3 (v3) vereinfachte den Modellierungsprozess für die Benutzer erheblich und bot hocheffiziente Rechenoptionen, einschließlich einer massiven Parallelisierung von GPUs. Dem vereinfachten v3 fehlen jedoch viele relevante Module, wie z. B. mehrschichtige Flussbetten zur Berechnung der topografischen Veränderung in Abhängigkeit von mehrkörnigen Transportformeln. Jetzt bietet BASEMENT Version 4 (v4) sowohl die vielfältigen Kapazitäten von v2 in Form von BASEMD-Setups als auch die Recheneffizienz von v3 in Form von BASEHPC-Setups. Dieses Tutorial erklärt die Einrichtung eines BASEHPC-Modells.

```

Dieses Kapitel führt durch den Aufbau einer zweidimensionalen (2d) numerischen Simulation mit der an der ETH Zürich (Schweiz) entwickelten frei verfügbaren Software BASEMENT. Besuchen Sie ihre [Website](https://basement.ethz.ch/)], um das Programm herunterzuladen und die detaillierte Dokumentation zu lesen. Dieses Tutorial enthält:

* Aufbau eines 2D-hydrodynamischen, stetigen Modells
* Laufen einer stetigen hydrodynamischen 2D numerischen Simulation
* Nachbearbeitung von Simulationsergebnissen: Visualisieren, Verstehen und Analysieren von Modellausgaben.

```{admonition} Requirements
:class: attention
Das Ausfüllen dieses Tutorials erfordert:

* Die Installation von {ref}`qgis-install`.
* Die Installation von [BASEMENT v4.0.1](https://basement.ethz.ch/) oder neuer].
* Optional: [ParaView](https://www.paraview.org/)].
```

```{admonition} Platform compatibility
:class: tip
Alle in diesem Tutorial enthaltenen Softwareanwendungen sind **kompatibel mit Linux- und Windows**-Plattformen. Beachten Sie, dass BASEMENT **nicht ** für macOS ** verfügbar ist.
```
