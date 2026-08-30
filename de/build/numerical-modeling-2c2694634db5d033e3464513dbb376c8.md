---
description: Prinzipien der numerischen Modellierung in der Wasserressourcentechnik, die Navier-Stokes-Gleichungen, 1D/2D/3D-Modellauswahl, Mesh-Setup, Kalibrierung und allgemeine Modellierungsfallen abdecken.
---

# Grundsätze

```{admonition} Theory chapter under development
:class: tip

We are working on a more exhaustive theory section on numerical modeling of rivers and reservoirs. Until then, please use our {ref}`glossary` for detailed explanations of technical terms that might be unclear.
```

Numerical models in water resources engineering approximate the motion of fluids through iterative solutions of the {term}`Navier-Stokes equations` and their statistical approximation with the {term}`Reynolds-averaged Navier-Stokes <RANS>` equations. The role of numerical models is becoming more and more important where models can be distinguished regarding their simplification hypotheses (e.g., for dimensions or fluid characteristics). Purely hydrodynamic models simulate the motion of water and have high accuracy for simulating flow phenomena, but major challenges remain for morphodynamic modeling. While one-dimensional (**1d** cross-section-averaged) modeling is slowly abandoned for its incapacity to account for complex flow phenomena in natural rivers, two-dimensional (**2d**) and three-dimensional (**3d**) models are becoming more and more popular. Still, there are challenges in model choices and understanding numerical models. In this context, {cite:t}`mosselman_five_2016` highlight five widespread and common problems in the creation and interpretation of numerical models. These five mistakes are:

1. Vorbereitung: Eindimensionale (1d), zweidimensionale (2d) und dreidimensionale (3d) Modelle erfordern ähnliche Eingangsdaten (Fließreihen, Stufen-Entladungs-Beziehung, Rauheit, digitales Höhenmodell, Korngrößen). Was variiert, sind die Berechnung (3d > 2d > 1d) und die Kalibrierung (1d > 2d > 3d).
2. Netzaufbau: Die Modellgrenzen müssen in einem ausreichenden Abstand zum interessierenden Bereich liegen. Eine Zuflussgrenze sollte nur entlang des permanent benetzten Flussbettes liegen und die stromaufwärts gelegenen 1-2% des modellierten Kanalbettes sollten eine nicht-erosive Einschränkung haben, die den Zellen zugewiesen ist. Andernfalls kann das Modell wegen lokal sehr hoher Geschwindigkeit und Erosionsraten nahe der Einströmgrenze instabil sein.
3. Modellaufbau: Lesen und verstehen Sie, wie Turbulenzverschlüsse im Modell implementiert werden, um die für den Turbulenzverschluss verwendeten Modellparameter realistisch einzustellen und ein stabiles Modell zu erhalten.
4. Modellvalidierung/Nachbearbeitung: Falsches Vertrauen in schlecht validierte numerische Modelle: Jedes Modell benötigt Validierungsdaten, was anstrengende und arbeitsintensive Feldarbeit erfordert.
5. Modellinterpretation: Die Richtung des Sedimenttransports und der Wasserflussvektoren unterscheiden sich meist.

Dieses Kapitel führt Open-Access- und Open-Source-Software mit umfangreichen Tutorials zur Vorverarbeitung (geo) räumlich expliziter Daten, zum Einrichten von Modellsteuerdateien, zum Ausführen von Modellen und zur Nachverarbeitung ein. Tutorials sind in diesem eBook für die folgende Software verfügbar:

* **BASEMENT (Open-Access)**<br> Das Tutorial {ref}`chpt-basement` führt die 2D-Hydrodynamik-Modellierung mit dem numerischen Modell *BASEMENT* 3.x der ETH Zürich (Schweiz) ein, das hauptsächlich mit Benchmark-Tests an **Bergflüssen/Bächen** entwickelt wurde.
* **TELEMAC (Open Source)**<br>Open TELEMAC-MASCARET ist eine leistungsstarke Software-Suite für eine Vielzahl von **Flüssen, Seen und sogar Ozeandeltas**.
  * Get an overview of files and model options in the {ref}`TELEMAC introduction <chpt-telemac>` section.
  * The {ref}`chpt-telemac2d` tutorial introduces 2d hydrodynamic modeling with standard *SLF* (selafin) geometry files.
  * The {ref}`chpt-telemac3d` tutorial introduces 3d hydrodynamic modeling (explorative tutorial).
* **OpenFOAM** represents another powerful modeling tool, which **is recommended for modeling flow-structure interactions**, and this eBook provides a basic introduction by [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/) in the {ref}`OpenFOAM section <chpt-openfoam>`. In addition, the OpenFOAM developer's [3-week tutorial](https://wiki.openfoam.com/index.php?title=%223_weeks%22_series) is a good start into OpenFOAM modeling for PhD students or engineers. On {ref}`Debian Linux / Ubuntu / Mint <linux-install>`, preferably install OpenFOAM from the [Ubuntu repository](https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian#ubuntu).

(calibration)=
## Kalibrierung und Validierung

Ein numerisches Modell kann gute Daten liefern, die nicht aussagekräftig sind, es sei denn, ein Modell wird kalibriert und validiert. Dafür gibt es drei Möglichkeiten.

1. Numerical calibration assesses the stability of the simulation itself. The parameters affected are for example the {term}`CFL` (Courant-Friedrichs-Lewy) condition or other hydraulic parameters. A numerical calibration can be time-consuming and requires expert knowledge to judge the validity of parameters.
1. Hydraulische Kalibrierung (und Validierung), die modellierte Wasserspiegel, Strömungsgeschwindigkeiten oder Bettscherspannung mit Beobachtungsdaten vergleicht.
1. Morphologische Kalibrierung und Validierung simuliert mit beobachteten Geländeänderungsraten (hier nicht anwendbar, da sie im Modell nicht angewendet wurde).

```{admonition} The Difference between Calibration and Validation
**Kalibrierung** ist die iterative Anpassung einer Simulation an die Realität unter Verwendung von Mess- (Beobachtungs-)Daten mit dem Ziel, den Fehler zwischen modellierten und beobachteten Ergebnissen zu minimieren. **Validierung** bewertet nur die Güte (oder den Fehler) des Modells, ohne das Modell selbst anzupassen.
```

This eBook provides hints for model calibration (parameters) in the TELEMAC sections on {ref}`hydrodynamics <tm2d-calibration>` and {ref}`morphodynamics <gaia-calibration>`.

## Was tun mit numerischen Modellergebnissen?

Sobald das Modell kalibriert ist, kann es verwendet werden, um Hochwasserhydrographien zu simulieren, um die Stabilität der Flusstechnik und der Flusslandschaft oder des Überschwemmungsgebiets zu beurteilen. Darüber hinaus kann die [Lebensraumqualität von Flüssen für Zielfischarten](https://pubs.er.usgs.gov/publication/70121265) zum Beispiel in Abhängigkeit von Wassertiefe, Strömungsgeschwindigkeit und Korngröße (und anderen Parametern) bewertet werden.] Es gibt sogar spezielle Software, um diese Aufgaben auszuführen, wie [CASiMiR](http://www.casimir-software.de/ENG/index_eng.html) (kommerziell) oder [River Architect](https://riverarchitect.github.io)].
