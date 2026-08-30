---
description: Workflow und Best Practices zur Massenerhaltung in TELEMAC-Flussmodellen, die die Einstellung von Randbedingungen, die Trockeninitialisierung und die Kalibrierung der Phasenentladungsbeziehung abdecken.
---

(tm-foc-mass)=
# Massenerhaltung

```{admonition} Tips for modeling rivers
:class: important

Die in diesem Kapitel gezeigten Workflows und Tipps beziehen sich in erster Linie auf die numerische Modellierung von Flüssen mit Telemac. Ähnliche Bedingungen könnten für Seemündungen gelten, aber andere Umgebungen wie Küstenregionen erfordern unterschiedliche Überlegungen zur Massenerhaltung.
```

This tutorial does not require running code, but we recommend to at least setting up a Telemac model, such as described in the {ref}`steady 2d tutorial <telemac2d-steady>`, which eases the understanding of concepts and terms.

(tm-foc-mass-workflow)=
## Workflow für Mass Conservation

Mit dem Verständnis der Randbedingungen kann ein Telemac-Modell robust nach folgendem Workflow aufgebaut werden:

1. Make sure to {ref}`draw liquid boundaries according to the recommendations in the section on boundaries <tm-foc-draw-bc>`.
1. For a **dry-initialized model** (e.g., in the {ref}`steady 2d tutorial <telemac2d-steady>`), use `5 5 5` upstream (prescribed Q and H) and a `5 4 4` downstream (prescribed H) boundaries in the `.cli` file to prescribe **steady** discharges through the `PRESCRIBED FLOWRATES` and `PRESCRIBED ELEVATIONS` keywords, respectively in the steering (`.cas`) file.
   * A `4 5 5` upstream (prescribed Q) boundary can cause simulation crashes because of supercritical flow conditions resulting from zero water depth and non-zero flow velocity (recall the {term}`definition of the Froude number <Froude number>`) at the concerned boundary.
   * Die `5 5 5`-Grenze des trocken initialisierten Modells erfordert ein gut definiertes {term}`stage-discharge relation <Stage-discharge relation>`, das gemäß dem {ref}`1d hydraulics Python exercise <ex-1d-hydraulics>` und dem resultierenden optimalen Wert für das Schlüsselwort **ROUGHNESS COEFFICIENT OF BOUNDARIES** in der Steuerungsdatei festgelegt werden kann (siehe unten).
   * For a **wet-initialized** (i.e., {ref}`hotstarted <tm2d-hotstart>`) model, as described in the {ref}`unsteady 2d simulation tutorial <tm2d-hotstart>`, **use a `4 5 5` upstream (prescribed Q)** along with a `5 4 4` downstream (prescribed H) boundary to avoid overdetermined conditions. However, once robustly determined, never modify the **ROUGHNESS COEFFICIENT OF BOUNDARIES** keyword in the steering file (see below).
   * If necessary, modify boundaries in the `.cli` file along with the correct keywords in the steering (`.cas`) file. For more details refer to {ref}`our tutorial on editing boundaries <tm-edit-bc>`.
1. Use the following keywords to prescribe roughness coefficients at the boundaries that correspond to **measured {term}`stage-discharge relation <Stage-discharge relation>`** and back-calculated cross-section averaged hydraulics:
   * ** RECHT DER FRICHTUNG ÜBER LATERAL BOUNDARIES (ganzzahlig) **
   * **ROUGHNESS-KOEFFIZIENTER VON BOUNDARIEN (Float)**
   * To back-calculate a roughness (friction) coefficient corresponding to a measured pair of water depth and discharge, take a look at the {ref}`Python exercise on 1-d hydraulics for solving the Manning-Strickler <ex-1d-hydraulics>` formula.
   * <span style="color: #41C639 "> Beachten Sie, dass **die Verwendung dieser Schlüsselwörter ** dazu führt, dass jede Rauheitskalibrierung ** die Massenbilanz beeinflusst **.</span>*
1. Führen Sie stetige Simulationen mit **PRESCRIBED FLOWRATES ** aus, die Entladungen entsprechen, für die hydraulische (z. B. Wassertiefe und Strömungsgeschwindigkeit) **Messungen ** zur Verfügung stehen, um die Rauheit ** zu kalibrieren (dh **FRICTION **).
   * Jede anfängliche stationäre Zustandssimulation sollte ausreichend lang laufen ($\geq$10$^4$timesteps), um {ref}`mass convergence <tm-convergence>` zu erreichen, dh nahezu gleiche Zu- und Abflüsse, die über das Schlüsselwort **MASSENBALANCE : JA** geschrieben werden.
   * The roughness should be preferably defined specifically for zones with equal terrain attributes (e.g., *cobble*, *sand bar*, or *vegetation*), as described in the spotlight focus on {ref}`defining roughness zones <tm-friction-zones>`. As a result, simulated and measured water depths (or water surface elevations) and flow velocities should be in similar ranges (not more than $\pm$0.10 m difference).
1. Verwenden Sie das kalibrierte Modell für Ihre Zwecke mit Hotstart-Bedingungen:
   * Das Schlüsselwort **PRESCRIBED FLOWRATES** in der `.cas`-Datei reicht aus, um physische {ref}`habitat suitability indices <hsi-def-ex>` für bestimmte Entladungen zu berechnen.
   * Define unsteady inflows through a hydrograph file, such as `inflows.liq` used in the {ref}`unsteady 2d <tm2d-liq-file>` tutorial.


````{admonition} Finite volume solver
:class: tip
:name: fv-tip

Werfen Sie einen Blick auf Telemacs endliches Volumenschema, das bei der Erhaltung des Massengleichgewichts besser ist und keinen Umgang mit ** TIDAL FLATS** erfordert. Es kann aktiviert werden, indem die folgenden Schlüsselwörter gesetzt werden:

```fortran
/ steering .cas file
EQUATIONS : 'SAINT-VENANT FV' / the apostrophes are strictly needed here
VARIABLE TIME-STEP : TRUE / use instead of the TIME STEP keyword
DURATION: 1000 / example value
DESIRED COURANT NUMBER : 0.6
/
/ additional FV recommendations
OPTION FOR THE DIFFUSION OF VELOCITIES : 2 / only option to get mass conservation but can cause problems with tidal flats
SCHEME FOR ADVECTION OF VELOCITIES : 3 / use 3, also for FV - MATRIX STORAGE must be 3
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4 / overrides SUPG OPTION and OPTION FOR CHARACTERISTICS
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2 / increase for higher accuracy and longer computing time, requires SCHEME OF ADVECTION 3,4,5, or 15 and OPTION 2,3,4
TYPE OF SOURCES : 2 / 2=Dirac is the only possibility for mass conservation, the default=1 means linear function and is not mass conservative
CONTINUITY CORRECTION : YES / particularly important when not only discharge but also depth is imposed at boundaries
```

Lesen Sie mehr über das endliche Volumenschema in Abschnitt 7.2.2 des [Telemac2d Manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) und das Malpasset-Beispiel (`telemac/v9.0.0/examples/malpasset/`).

````

(tm-foc-mass-keywords)=
## Zusätzliche Steering File Keywords

Während einer Simulation kann die Massenbilanz beobachtet werden, indem das Schlüsselwort **MASSENBALANCE** in der Steuerungsdatei aktiviert wird, was jedoch ** keine Massenbilanz** erzwingt:

```fortran
/ steering .cas file
MASS-BALANCE : YES
```

After the simulation, the conservation of mass can be verified as discussed in the analysis of the {ref}`results in the steady 2d tutorial <verify-steady-tm2d>`.

Die Priorität, die Telemac verwendet, um eine Massenbilanz zu erhalten, kann definiert werden mit:

```fortran
/ steering .cas file
TREATMENT OF FLUXES AT THE BOUNDARIES : 1 / 1-priority of prescribed values, 2-priority of correct fluxes
```

Andere schlüsselwörter können definiert werden, um nicht nur zu beobachten, sondern auch die massenbilanz zu verbessern. Zum Beispiel ist die Standardanzahl von Grenzknoten in einer Lenkdatei 30, was in einem großen Modell schnell überschritten wird. Wenn es also mehr als 30 Randknoten gibt, erhöhen Sie die maximale Anzahl von Randknoten in der Steuerungsdatei (`.cas`), zum Beispiel auf `50`:

```fortran
/ steering .cas file
MAXIMUM NUMBER OF BOUNDARIES : 50
```

Also, too small water depths can cause supercritical flows at liquid boundaries, which should be avoided, either by correctly defining the boundary nodes at the bottom of the riverbed only (recall the {ref}`recommendations to draw liquid boundaries <tm-foc-draw-bc>`) or by increasing the minimum water depth from its default value of 0.1 m to a higher value in the steering file, for example to 0.2 m:

```fortran
/ steering .cas file
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES BOUNDARY CONDITIONS : 0.2
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES INITIAL CONDITIONS : 0.2
```

In addition, the `MINIMUM VALUE OF DEPTH` keyword may be increased from its default value of `0.0`, but such increases might negatively effect on the mass balance.

Um die Rechengeschwindigkeit zu erhöhen, empfehlen einige Tutorials die Verwendung von Massenklumpen, die sich jedoch negativ auf die Massenerhaltung auswirken:

* Vermeiden Sie **MASSING LUMPING ...** Keywords: Sie führen eine falsche Glättung ein.
* Behalten Sie den Standardwert für **H CLIPPING **, da Änderungen die Massenerhaltung beeinträchtigen.
