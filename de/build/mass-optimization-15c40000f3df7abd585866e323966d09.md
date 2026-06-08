---
description: Workflow und Best Practices für die Massenerhaltung in TELEMAC Flussmodellen, die Begrenzungskonditionsaufbau, Trockener Initialisierung und Phasen-Entladungs-Beziehungskalibrierung abdecken.
---

(tm-foc-mass)=
# Massenkonservierung

```{admonition} Tips for modeling rivers
:class: important

Die in diesem Kapitel dargestellten Workflows und Tipps beziehen sich in erster Linie auf die numerische Modellierung von Flüssen mit Telemac. Ähnliche Bedingungen könnten für Seeschwemmungen gelten, aber andere Umgebungen, wie Küstenregionen, erfordern unterschiedliche Überlegungen zum Massenschutz.
```

Dieses Tutorial erfordert keinen laufenden Code, aber wir empfehlen zumindest die Einrichtung eines Telemac-Modells, wie es in der {ref}`steady 2d tutorial <telemac2d-steady>` beschrieben ist, was das Verständnis von Konzepten und Begriffen erleichtert.

(tm-foc-mass-workflow)=
## Workflow für Massenkonservierung

Mit dem Verständnis von Randbedingungen kann ein Telemac-Modell nach folgendem Workflow robust gebaut werden:

1. Make sure to {ref}`draw liquid boundaries according to the recommendations in the section on boundaries <tm-foc-draw-bc>`.
1. For a **dry-initialized model** (e.g., in the {ref}`steady 2d tutorial <telemac2d-steady>`), use `5 5 5` upstream (prescribed Q and H) and a `5 4 4` downstream (prescribed H) boundaries in the `.cli` file to prescribe **steady** discharges through the `PRESCRIBED FLOWRATES` and `PRESCRIBED ELEVATIONS` keywords, respectively in the steering (`.cas`) file.
   * A `4 5 5` upstream (prescribed Q) boundary can cause simulation crashes because of supercritical flow conditions resulting from zero water depth and non-zero flow velocity (recall the {term}`definition of the Froude number <Froude number>`) at the concerned boundary.
   * The `5 5 5` boundary of the dry-initialized model requires a well defined {term}`stage-discharge relation <Stage-discharge relation>` that can be established according to the {ref}`1d hydraulics Python exercise <ex-1d-hydraulics>` and the resulting optimum value for the **ROUGHNESS COEFFICIENT OF BOUNDARIES** keyword in the steering file (see below).
   * For a **wet-initialized** (i.e., {ref}`hotstarted <tm2d-hotstart>`) model, as described in the {ref}`unsteady 2d simulation tutorial <tm2d-hotstart>`, **use a `4 5 5` upstream (prescribed Q)** along with a `5 4 4` downstream (prescribed H) boundary to avoid overdetermined conditions. However, once robustly determined, never modify the **ROUGHNESS COEFFICIENT OF BOUNDARIES** keyword in the steering file (see below).
   * If necessary, modify boundaries in the `.cli` file along with the correct keywords in the steering (`.cas`) file. For more details refer to {ref}`our tutorial on editing boundaries <tm-edit-bc>`.
1. Use the following keywords to prescribe roughness coefficients at the boundaries that correspond to **measured {term}`stage-discharge relation <Stage-discharge relation>`** and back-calculated cross-section averaged hydraulics:
   * **LAW OF FRICTION ON LATERAL BOUNDARIES (integer)**
   * **ROUGHNESS COEFFICIENT OF BOUNDARIES (float)**
   * To back-calculate a roughness (friction) coefficient corresponding to a measured pair of water depth and discharge, take a look at the {ref}`Python exercise on 1-d hydraulics for solving the Manning-Strickler <ex-1d-hydraulics>` formula.
   * *<span style="color: #41C639 ">Note that **not using these keywords** will make that any roughness calibration **affects the mass balance**.</span>*
1. Run steady simulations with **PRESCRIBED FLOWRATES** corresponding to discharges for which hydraulic (e.g., water depth and flow velocity) **measurements** are available to **calibrate the roughness** (i.e., **FRICTION**).
   * Any initial steady state simulation should run sufficiently long ($\geq$ 10$^4$ timesteps) to reach {ref}`mass convergence <tm-convergence>`, that is, close-to equal inflows and outflows written through the **MASS-BALANCE : YES** keyword.
   * The roughness should be preferably defined specifically for zones with equal terrain attributes (e.g., *cobble*, *sand bar*, or *vegetation*), as described in the spotlight focus on {ref}`defining roughness zones <tm-friction-zones>`. As a result, simulated and measured water depths (or water surface elevations) and flow velocities should be in similar ranges (not more than $\pm$0.10 m difference).
1. Use the calibrated model for your purposes with hotstart conditions:
   * The **PRESCRIBED FLOWRATES** keyword in the `.cas` file is sufficient to calculate physical {ref}`habitat suitability indices <hsi-def-ex>` for specific discharges.
   * Define unsteady inflows through a hydrograph file, such as `inflows.liq` used in the {ref}`unsteady 2d <tm2d-liq-file>` tutorial.


````{admonition} Finite volume solver
:class: tip
:name: fv-tip

Sehen Sie sich das endliche Volumenschema von Telemac an, das bei der Erhaltung der Massenbilanz besser ist und nicht mit **TIDAL FLATS** zu tun hat. Es kann durch die Einstellung der folgenden Keywords aktiviert werden:

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

Lesen Sie mehr über das endliche Volumenschema in Abschnitt 7.2.2 der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) und das Malpasset-Beispiel (`telemac/v9.0.0/examples/malpasset/`).

````

(tm-foc-mass-keywords)=
## Weitere Steering File Keywords

Während einer Simulation kann die Massenbilanz durch Aktivierung des **MASS BALANCE** Schlüsselworts in der Lenkdatei beobachtet werden, das jedoch ** keine Massenbilanz durchsetzt*:

```fortran
/ steering .cas file
MASS-BALANCE : YES
```

Nach der Simulation kann die Erhaltung der Masse wie in der Analyse der {ref}`results in the steady 2d tutorial <verify-steady-tm2d>` diskutiert werden.

Die Priorität, die Telemac verwendet, um Massenbilanz zu liefern, kann definiert werden mit:

```fortran
/ steering .cas file
TREATMENT OF FLUXES AT THE BOUNDARIES : 1 / 1-priority of prescribed values, 2-priority of correct fluxes
```

Andere Schlüsselwörter können definiert werden, um nicht nur zu beobachten, sondern auch die Massenbilanz zu verbessern. Beispielsweise beträgt die Standardzahl der Grenzknoten in einer Lenkdatei 30, die in einem großen Modell schnell überschritten wird. Wenn es also mehr als 30 Grenzknoten gibt, erhöhen Sie die maximale Anzahl von Grenzknoten in der Lenkungsdatei (`.cas`) z.B. an `50`:

```fortran
/ steering .cas file
MAXIMUM NUMBER OF BOUNDARIES : 50
```

Auch können zu kleine Wassertiefen zu überkritischen Strömungen an Flüssigkeitsgrenzen führen, die vermieden werden sollten, entweder indem die Grenzknoten nur am Boden des Flussbettes korrekt definiert werden (Recall the {ref}`recommendations to draw liquid boundaries <tm-foc-draw-bc>`) oder durch Erhöhung der Mindestwassertiefe von seinem Standardwert von 0,1 m auf einen höheren Wert in der Lenkdatei, beispielsweise auf 0,2 m:

```fortran
/ steering .cas file
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES BOUNDARY CONDITIONS : 0.2
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES INITIAL CONDITIONS : 0.2
```

Darüber hinaus kann das `MINIMUM VALUE OF DEPTH`-Keyword aus seinem Standardwert von `0.0` erhöht werden, aber solche Erhöhungen könnten sich negativ auf die Massenbilanz auswirken.

Um die Rechengeschwindigkeit zu erhöhen, empfehlen einige Tutorials die Verwendung von Massenklumpen, die sich jedoch negativ auf die Massenerhaltung auswirken:

* Vermeiden Sie **MASSING LUMPING ...** Keywords: Sie führen falsche Glättung ein.
* Halten Sie den Standardwert für **H CLIPPING**, da Änderungen die Massenerhaltung beeinträchtigen.
