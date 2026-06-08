---
description: Prinzipien der numerischen Modellierung in der Wasserressourcen-Engineering, Abdeckung Navier-Stokes Gleichungen, 1D/2D/3D Modellauswahl, Mesh-Setup, Kalibrierung und gemeinsame Modellierungs-Pistenfälle.
---

# Grundsätze

```{admonition} Theory chapter under development
:class: tip

Wir arbeiten an einer umfassenderen Theorie zur numerischen Modellierung von Flüssen und Reservoiren. Bis dahin nutzen Sie unsere {ref}`glossary` für detaillierte Erläuterungen zu technischen Bedingungen, die unklar sein könnten.
```

Zahlreiche Modelle in der Wasserressourcen-Engineering nähern sich der Bewegung von Flüssigkeiten durch iterative Lösungen der {term}`Navier-Stokes equations` und deren statistischer Näherung mit den {term}`Reynolds-averaged Navier-Stokes <RANS>`-Gleichungen. Die Rolle der numerischen Modelle wird immer wichtiger, wenn Modelle hinsichtlich ihrer Vereinfachungshypothesen (z.B. für Dimensionen oder Fluideigenschaften) unterschieden werden können. Rein hydrodynamische Modelle simulieren die Bewegung von Wasser und haben eine hohe Genauigkeit für die Simulation von Strömungserscheinungen, aber große Herausforderungen bleiben für die morphodynamische Modellierung. Während eindimensionale (**1d* querschnittsgemittelte) Modellierungen für ihre Unfähigkeit langsam aufgegeben werden, um komplexe Flussphänomene in natürlichen Flüssen zu berücksichtigen, werden zweidimensionale (*2d**) und dreidimensionale (*3d**) Modelle immer beliebter. Dennoch gibt es Herausforderungen in Modellwahlen und das Verständnis von numerischen Modellen. In diesem Zusammenhang hebt {cite:t}`mosselman_five_2016` fünf weit verbreitete und gemeinsame Probleme bei der Erstellung und Interpretation von numerischen Modellen hervor. Diese fünf Fehler sind:

1. Vorbereitung: Eindimensionale (1d), zweidimensionale (2d) und dreidimensionale (3d) Modelle erfordern ähnliche Eingangsdaten (Flow-Serie, Stage-Decharge-Beziehung, Rauhigkeit, digitale Höhenmodell, Korngrößen). Die Berechnung (3d > 2d > 1d) und die Kalibrierung (1d > 2d > 3d) sind unterschiedlich.
2. Grid-Setup: Die Modellgrenzen müssen in ausreichender Entfernung zum interessierenden Bereich liegen. Eine Zuflussgrenze sollte nur entlang des permanent benetzten Flussbettes liegen und die stromaufwärts gelegenen 1-2% des modellierten Kanalbettes sollten eine den Zellen zugeordnete nicht-erosive Eingrenzung aufweisen. Ansonsten kann das Modell aufgrund von lokal sehr hohen Geschwindigkeiten und Erosionsraten nahe der Zuflussgrenze instabil sein.
3. Modellaufbau: Lesen und verstehen, wie Turbulenzverschlüsse im Modell implementiert werden, um die Modellparameter für den Turbulenzverschluss realistisch einzustellen und ein stabiles Modell zu liefern.
4. Modellvalidierung/Nachbearbeitung: Falsches Vertrauen in schlecht validierte numerische Modelle: Jedes Modell benötigt Validierungsdaten, die erschöpfende und arbeitsintensive Feldarbeit beinhalten.
5. Modellinterpretation: Die Richtung des Sedimenttransports und der Wasserflussvektoren unterscheiden sich meist.

Dieses Kapitel führt Open-Access- und Open-Source-Software mit umfangreichen Tutorials zur Vorverarbeitung (geo) räumlich explizite Daten, zur Erstellung von Modellkontrolldateien, Laufmodelle und Nachbearbeitung ein. Tutorials sind in diesem eBook für folgende Software verfügbar:

* **BASEMENT (open-access)*<br> Das {ref}`chpt-basement` tutorial führt 2d hydrodynamische Modellierung mit dem Zahlenmodell der ETH Zürich (Schweiz) *BASEMENT* 3.x ein, das in erster Linie mit Benchmark-Tests an **Mountain Rivers/streams** entwickelt wurde.
**TELEMAC (offene Quelle)*<br>Open TELEMAC-MASCARET ist eine leistungsstarke Software-Suite für eine Vielzahl von **rivers, Seen und sogar Ocean deltas**.
* Einen Überblick über Dateien und Modelloptionen erhalten Sie im Abschnitt {ref}`TELEMAC introduction <chpt-telemac>`.
* Das {ref}`chpt-telemac2d` tutorial führt 2d hydrodynamische Modellierung mit Standard *SLF* (selafin) Geometriedateien ein.
* Das {ref}`chpt-telemac3d` tutorial führt 3d hydrodynamische Modellierung ein (explorative Tutorial).
* **OpenFOAM** stellt ein weiteres leistungsstarkes Modellierungstool dar, das ** für die Modellierung von Strömungs-Struktur-Interaktionen* empfohlen wird, und dieses eBook bietet eine grundlegende Einführung von [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/) in the {ref}`OpenFOAM section <chpt-openfoam>`. Darüber hinaus ist der OpenFOAM-Entwickler [3-week tutorial](https://wiki.openfoam.com/index.php?title=%223_weeks%22_series)] ein guter Start in die OpenFOAM-Modellierung für Doktoranden oder Ingenieure. Auf {ref}`Debian Linux / Ubuntu / Mint <linux-install>`, installieren Sie vorzugsweise OpenFOAM von der [Ubuntu repository](https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian#ubuntu).

(calibration)=
## Kalibrierung und Validierung

Ein numerisches Modell kann gute Daten liefern, die nicht aussagekräftig sind, es sei denn, ein Modell wird kalibriert und validiert. Es gibt drei Möglichkeiten.

1. Numerische Kalibrierung beurteilt die Stabilität der Simulation selbst. Betroffene Parameter sind beispielsweise der Zustand {term}`CFL` (Courant-Friedrichs-Lewy) oder andere hydraulische Parameter. Eine numerische Kalibrierung kann zeitaufwendig sein und erfordert Expertenwissen, um die Gültigkeit von Parametern zu beurteilen.
1. Hydraulische Kalibrierung (und Validierung), die modellierte Wasseroberflächen Ebenen, Strömungsgeschwindigkeiten oder Bettscherspannung mit Beobachtungsdaten vergleicht.
1. Morphologische Kalibrierung und Validierung vergleichen simuliert mit beobachteten Geländeänderungsraten (hier nicht anwendbar, weil es im Modell nicht angewandt wurde).

```{admonition} The Difference between Calibration and Validation
**Calibration** ist die iterative Anpassung einer Simulation an die Realität unter Verwendung von Messdaten (Beobachtung) mit dem Ziel, den Fehler zwischen modellierten und beobachteten Ergebnissen zu minimieren. **Validation** beurteilt nur die Güte (oder Fehler) des Modells, ohne das Modell selbst anzupassen.
```

Dieses eBook bietet Hinweise zur Modellkalibrierung (Parameter) in den TELEMAC-Abschnitten unter {ref}`hydrodynamics <tm2d-calibration>` und {ref}`morphodynamics <gaia-calibration>`.

## Was mit Numerischen Modellergebnissen zu tun?

Sobald das Modell kalibriert ist, kann es verwendet werden, um Flut-Hydrographen zu simulieren, um die Stabilität der Fluss-Engineering-Funktionen und die Flusslandschaft oder Inundation Bereich zu bewerten. Außerdem kann die [Gewohnheitsqualität der Flüsse für Zielfischarten](https://pubs.er.usgs.gov/publication/70121265) in Abhängigkeit von Wassertiefe, Fließgeschwindigkeit und Korngröße (und anderen Parametern) beurteilt werden. Es gibt sogar spezielle Software, um diese Aufgaben zu erfüllen, wie [CASiMiR](http://www.casimir-software.de/ENG/index_eng.html)(kommerziell) oder [River Architect](https://riverarchitect.github.io).
