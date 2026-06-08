---
description: Vollständiges Tutorial zum Aufbau und Betrieb von 2D hydrodynamischen numerischen Simulationen mit BASEMENT (ETH Zürich), zum BASEHPC Modellaufbau, stationäre Modellierung und Ergebnisvisualisierung.
---

(chpt-basement)=
# ABSCHNITT

```{admonition} Old BASEMENT versions, BASEMD, and BASEHPC
:class: important

Die BASEMENT-Version 2 (v2) wurde mit komplexen Strukturen und einer breiten Palette von Kapazitäten entwickelt, jedoch wurde wenig Fokus auf die Rechenzeit gezogen. BASEMENT Version 3 (v3) vereinfachte den Modellierungsprozess für Anwender erheblich und verfügte über hocheffiziente Rechenoptionen, einschließlich massiver Parallelisierung auf GPUs. Der vereinfachte v3 fehlt jedoch an vielen relevanten Modulen, wie z.B. Mehrschicht-Flussbetten zur Berechnung des topographischen Wandels in Abhängigkeit von Mehrkorngrößen-Bettladungstransportformeln. Die BASEMENT Version 4 (v4) bietet nun sowohl die vielfältigen Kapazitäten von v2 in Form von BASEMD-Setups als auch die Recheneffizienz von v3 in Form von BASEHPC-Setups. Dieses Tutorial erklärt die Einrichtung eines BASEHPC-Modells.

```

Dieses Kapitel führt durch die Einrichtung einer zweidimensionalen (2d) numerischen Simulation mit der frei verfügbaren Software BASEMENT an der ETH Zürich (Schweiz). Besuchen Sie ihre [website](https://basement.ethz.ch/), um das Programm herunterzuladen und die ausführliche Dokumentation zu lesen. Diese Lernfunktionen:

* Aufbau eines 2d hydrodynamischen, stationären Modells
* Laufen einer stetigen hydrodynamischen 2d numerischen Simulation
* Nachbearbeitung von Simulationsergebnissen: Modellausgänge visualisieren, verstehen und analysieren.

```{admonition} Requirements
:class: attention
Die Fertigstellung dieses Tutorials erfordert:

* Die Installation von {ref}`qgis-install`.
* Die Installation von [BASEMENT v4.0.1](https://basement.ethz.ch/) oder neuer.
* Optional: [ParaView](https://www.paraview.org/).
```

```{admonition} Platform compatibility
:class: tip
Alle in diesem Tutorial enthaltenen Software-Anwendungen sind **kompatibel mit Linux und Windows*-Plattformen. Beachten Sie, dass BASEMENT **not** verfügbar ** für macOS** ist.
```
