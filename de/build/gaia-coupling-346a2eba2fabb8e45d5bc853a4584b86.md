---
description: Einführung in die Kopplung der TELEMAC-Hydrodynamik mit der GAIA-Morphodynamik zur Simulation des Transports von Betten und suspendierten Sedimenten in Flüssen, Seen und Mündungen.
---

# Einführung und Kopplung

```{admonition} Requirements
Dieses Tutorial wurde für fortgeschrittene Modellierer entwickelt und bevor Sie in dieses Tutorial eintauchen, stellen Sie sicher, dass Sie die Tutorials {ref}`TELEMAC pre-processing <slf-prepro-tm>` und {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>`** vervollständigen.

Der Fall in diesem Tutorial wurde mit der folgenden Software erstellt:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v9.0.0 ({ref}`stand-alone installation <modular-install>`) - frühere Versionen erkennen möglicherweise einige der in diesem eBook verwendeten Schlüsselwörter nicht.
* {ref}`QGIS <qgis-install>`.
* Debian Linux / Ubuntu 24.04 (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

## Terminologie
Eine hydromorphodynamische Simulation impliziert die Modellierung von ablaufenden **{term}`Sediment transport`** Prozessen. Die vorherigen Abschnitte in diesem eBook konzentrieren sich auf Hydrodynamik definiert als *die Untersuchung von Flüssigkeiten in Bewegung * und dieser Abschnitt konzentriert sich auf ** Morphodynamik * definiert als **die Untersuchung von zeitabhängigen Veränderungen in den Formen von Schwemmbetten und ihren zugrunde liegenden Prozessen *.

(gaia-seditrans)=
## Sedimenttransportarten

TELEMAC has a dedicated module called Gaia for modeling morphodynamics. Gaia enables modeling sediment transport and morphological evolution (i.e., {term}`Topographic change`) in rivers, lakes, and estuaries. It comes with particular routines to consider a spatio-temporal variation of grain sizes, grading curves, and riverbed layering for simulating sediment transport in the form of **{term}`Bedload` (coarse sediment)** and/or **{term}`Suspended load` (fine sediment)**. {term}`Bedload` is calculated by solving semi-empiric equations, such as the {cite:t}`meyer-peter_formulas_1948` formula (read more later in this tutorial). {term}`Suspended load` is modeled by solving the {term}`Advection`-{term}`Diffusion` equations (typically, the {term}`RANS` form), which require closures for sediment erosion and deposition fluxes. {numref}`Figure %s <bl-vs-sl>` qualitatively illustrates the two basic modes of sediment transport in the form of suspended load and bedload. Whether a particle is transported in suspension or as bedload can also be determined by calculating of the {term}`Rouse number`.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-transport.png
:alt: sediment transport bedload suspended load
:name: bl-vs-sl

Qualitative Darstellung von zwei Arten des Sedimenttransports. Links: Schwebelast in Form von feinen Partikeln, die sich mit dem Massenstrom bewegen; rechts: Bettlast in Form von Partikeln, die auf dem Flussbett rollen, springen oder gleiten.
```

Sediment is further distinguished between very fine, **cohesive** sediment and coarser, **non-cohesive** sediment. In addition, Gaia accounts for bed evolution through an iterative solution of the {term}`Exner equation` {cite:p}`exner_uber_1925` for mass conservation.

Die Rekrutierung von Sedimenten sowohl für die Schwebelast als auch für den Bettentransport erfordert einen detaillierten Blick auf das Flussbett, der später im Abschnitt über die Definition von {ref}`the riverbed composition and the active layer <gaia-active-lyr>` bereitgestellt wird.


(tm-coupling)=
## Kopplung von TELEMAC und Gaia

Das Morphodynamikmodul Gaia kann intern mit den hydrodynamischen Modellen Telemac2d (auflösen des {term}`Shallow water equations`) oder Telemac3d (auflösen des Reynolds-gemittelten {term}`Navier-Stokes (RANS) equations <Navier-Stokes equations>`) gekoppelt werden. In diesem Abschnitt werden Arten der Kopplung von Telemac2d/Telemac3d (Hydrodynamik) mit Gaia (Morphodynamik) erläutert.

### Von Sisyphe zu Gaia

Sisyphe ist das traditionelle Sedimenttransportmodul in TELEMAC, das weitgehend durch das einheitlichere Gaia-Modul ersetzt wurde. Gaia basiert auf dem historischen Modul SISYPHE, mit einer Vielzahl von Verbesserungen, Korrekturen und Optimierungen. Gaias einheitliches Framework verwaltet effizient verschiedene Sedimentklassen, Sand-Schlamm-Mischungen und sowohl 2D- als auch 3D-Raumdimensionen. Um Spezifikationen zu erhalten, die über die hier in der TELEMAC-Dokumentation und im TELEMAC-Forum vorgestellten Funktionen hinausgehen, ist es nützlich, das SISYPHE-Erbe zu kennen. SISYPHE-Routinen sind immer noch in den letzten TELEMAC-Versionen über Gaia verfügbar, obwohl einige Keywords Anpassungen erfordern. Lesen Sie mehr im [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) in Anhang 8.1 und im gaia.dico (`telemac/v9.0.0/sources/gaia/gaia.dico`).

### Kopplung von Hydrodynamik (Telemac2d/3d) und Morphodynamik (Gaia)

Ein hydromorphodynamisches numerisches Modell kann entweder **voll gekoppelt ** oder **entkoppelt ** werden.

Fully coupled model
: A fully coupled model solves the hydrodynamic {term}`Navier-Stokes equations` simultaneously with sediment transport equations (i.e., erosion and deposition fluxes from and to the riverbed through the {term}`Exner equation`). Bed elevation (i.e., {term}`Topographic change`) is calculated for every timestep, which leads to **long computation** times. In addition to the coupling of gravity-driven hydrodynamics (i.e., bulk flow along valley slopes), {term}`Sediment transport`, and {term}`Topographic change`, a model can also be coupled with (surface) wave hydrodynamics.

*Anwendungsbereich:* Schnelle morphodynamische Prozesse wie hyperkonzentrierte sedimentbeladene Strömungen oder Trümmerströme.



Decoupled model
: A decoupled model alternates between solving hydrodynamics and morphodynamics (i.e., the {term}`Exner equation`). The riverbed is considered fixed when hydrodynamic variables are computed, and then bed elevation changes are calculated separately based on the computed flow field. This *asynchronous* approach is computationally more efficient than full coupling.

*Anwendungsbereich:* Die meisten Flussmodelle und insbesondere See- oder Ozeanmodelle, bei denen morphodynamische Zeitskalen viel länger sind als hydrodynamische Zeitskalen.

Gaia folgt dem **entkoppelten ** Ansatz. Der für die morphodynamische Berechnung verwendete Zeitschritt ist der gleiche wie für die Hydrodynamik (angegeben in der Telemac2d- oder Telemac3d-Lenkdatei). In jedem Zeitschritt wird die Hydrodynamik zuerst mit dem eingefrorenen Bett gelöst, dann werden die Sedimenttransportgleichungen und die Bettentwicklung (Exner-Gleichung) basierend auf dem berechneten Strömungsfeld gelöst.

```{admonition} Coupling period for wave-current-sediment interactions
:class: note
Wenn Gaia mit dem Wellenmodul TOMAWAC gekoppelt wird, kann eine **Kopplungsperiode** angegeben werden, um zu steuern, wie häufig Wellenfelder aktualisiert werden. Dies ist relevant, da Wellenberechnungen teuer sein können und sich die Wellenbedingungen möglicherweise nicht so schnell ändern wie Ströme. Für die grundlegende Telemac2d/3d-Gaia-Kopplung ohne Wellen werden die Morphodynamiken in jedem hydrodynamischen Zeitschritt berechnet. Lesen Sie mehr über Wellenkopplung in Abschnitt 5.1 des [Gaia Manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)].
```

### Dateianforderungen für die Kopplung von Gaia

In addition to the standard Telemac2d steering, boundaries, and geometry mesh files, coupling hydrodynamics with Gaia requires a new steering (`*.cas`) file that needs to be referenced in the main steering file of the simulation. To this end, **create a new folder for the Gaia tutorial** (e.g., called `/gaia2d-tutorial/`), copy the {ref}`dry-initialized steady2d simulation and results files <tm2d-init-dry>` (or clone the [gaia2d-tutorial repository](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/)), and **create a new Gaia steering file** (e.g., called `gaia-morphodynamics.cas`). Thus, the following files should live in the modeling folder for this tutorial:

* Das Rechennetz in Form von [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf)].
* Die Randdefinitionen in Form von [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli)].
* Die Ergebnisse des trocken-initialisierten stationären 2D-Modells laufen für 35 m$^3$/s in Form von [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) ({ref}`dry steady run <tm2d-init-dry>`end bei `T=15000`).
* Eine Telemac2d-Steuerungsdatei für dieses Tutorial, die auf der trocken initialisierten steady2d-Steuerungsdatei aufbaut und [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas)] aufgerufen wird.
* Die neue [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas) Steering-Datei].

```{admonition} Gaia simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/).
```

### Paar Gaia in der hydrodynamischen Steuerungsdatei

Um die Kopplung von Gaia mit einer Telemac2d/Telemac3d-Simulation programmatisch zu implementieren, müssen zusätzlich zu den im {ref}`steady2d chapter <telemac2d-steady>` erläuterten Keywords einige neue Keywords definiert werden. Das erste zusätzliche Schlüsselwort ist die Baseline für jede Kopplung mit Telemac2d oder Telemac3d Steuerungsdatei:

```fortran
/ steady2d-gaia.cas
COUPLING WITH : 'GAIA'
```

```{admonition} steady2d-gaia.cas is the hydrodynamics (Telemac2d or Telemac3d) steering file
:class: note
In diesem Tutorial wird die Steuerungsdatei für Hydrodynamik (Telemac2d oder Telemac3d) als [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas)] und die Steuerungsdatei für Morphodynamik (Gaia) als [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas)] bezeichnet.
```

Darüber hinaus verknüpft das Schlüsselwort **GAIA STEERING FILE** das oben erstellte `gaia-morphodynamics.cas` in der Steuerungsdatei für die Hydrodynamik von Telemac2d (oder Telemac3d):

```fortran
/ steady2d-gaia.cas
/ ...
GAIA STEERING FILE : gaia-morphodynamics.cas
```


(gaia-hotstart)=
### Heißstart

This tutorial builds on the results of the {ref}`dry-initialized steady2d model <tm2d-init-dry>` because Gaia simulations typically require a well-developed flow field as initial condition (see the {ref}`above definitions <tm-coupling>`). Using a former simulation result for model initialization is called **hotstart**, which requires a results file from a previous simulation. For this purpose, make sure that the dry-initialized steady2d results file is in the simulation folder ([download r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf)). Then **define the hotstart in the Telemac2d steering file** with the following keywords:


```fortran
/ steady2d-gaia.cas
/ ...
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
```

```{admonition} COMPUTATION CONTINUED is obsolete in TELEMAC v9.0
:class: warning
Seit TELEMAC v9.0 wurde das Keyword `COMPUTATION CONTINUED`** gelöscht. Der Fortsetzungsschritt wird nun **automatisch aktiviert**, wenn `PREVIOUS COMPUTATION FILE` in der Steuerungsdatei angegeben ist. Die einfache Bereitstellung der vorherigen Berechnungsdatei löst das Hotstart-Verhalten aus.
```

Mit dem Schlüsselwort **INIAL TIME SET TO NULL** wird die Simulationszeit auf `0` zurückgesetzt. Stellen Sie als nächstes sicher, dass alle **INITIAL BEDINGUNGEN**-Keywords mit **/** kommentiert werden (alternativ löschen Sie diese Zeilen von steady2d-gaia.cas):

```fortran
/ steady2d-gaia.cas
/ ...
/ INITIAL CONDITIONS - not required (hotstart)
/ ------------------------------------------------------------------
/ INITIAL CONDITIONS : 'ZERO DEPTH' / use ZERO DEPTH to start with dry model conditions
/ INITIAL DEPTH : 0.005 / use INTEGER for speeding up calculations
```

```{admonition} Bottom elevation must be available in the hotstart geometry (SLF)
:class: warning
Die untere Höhe muss in der Ergebnisdatei der für den Heißstart verwendeten Simulation ausgedruckt werden. Stellen Sie zu diesem Zweck sicher, dass die Liste der Werte für das Schlüsselwort **VARIABLES FOR GRAPHIC PRINTOUTS** `B` enthält, wie im {ref}`explanations for the setup of the dry-initialized model <tm2d-init-dry>` angegeben.
```

```{admonition} Continuing a Gaia computation (sedimentological hotstart)
:class: tip
Um eine Gaia-Simulation aus einer früheren sedimentologischen Berechnung fortzusetzen (d.h. um mit vorhandenen Bettzusammensetzungs- und Schichtdaten neu zu starten), verwenden Sie das Schlüsselwort **PREVIOUS SEDIMENTOLOGICAL COMPUTATION FILE** in der Gaia-Steuerungsdatei. Seit v9.0 aktiviert die Angabe dieser Datei automatisch die Fortsetzung, ohne dass ein zusätzliches Keyword erforderlich ist. Die vorherige Datei sollte die unterste Erhebung (`B`), Schichtdicken (`*ES`) und idealerweise die Sedimentmassen (`*S*` oder `*M*`) oder Verhältnisse (`*A*`, `*R*`) für die richtige Fortsetzung enthalten.
```

The dry-initialized steering file prescribes flowrates and elevations, which requires **modifications in steady2d-gaia.cas** to **prescribed Q only**. The reason for the Q-only prescription is that with Gaia, we want to model-predict changes in water depths and riverbed elevation, which means that the water surface elevation must not be constrained (i.e., not prescribed) as a boundary condition. Thus, the setup of boundary conditions for Gaia also requires slight modifications of the boundary (`*.cli`) file(s), which will be explained in the next section on the {ref}`Basic Setup of Gaia <gaia-bc>`. To this end, make sure that in the hydrodynamics steering file **only the flowrate prescription keyword is activated** and the elevation prescription is deactivated (comment out with `/`):

```fortran
/ steady2d-gaia.cas
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 374.805626;371.33
```

### Kontrollabschnitte

Control sections are sequences of node numbers (or node coordinates) at which TELEMAC sums up fluxes, for instance, to verify inflow and outflow mass balances. The unsteady simulation section provides detailed instructions for {ref}`defining control sections <tm-control-sections>` and this tutorial re-uses the control sections file from the unsteady simulation (**[download control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/control-sections.txt)**).

````{dropdown} Expand to view the file *control-sections.txt*
```
# control sections steady2d
2 -1
Inflow_boundary
144 32
Outflow_boundary
34 5
```
````

Um die Kontrollabschnitte für die Gaia-Simulation zu verwenden, fügen Sie der **Hydrodynamik**-Lenkdatei Folgendes hinzu:

```
/ steady2d-gaia.cas
/ ...
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
```

Beim erneuten Ausführen der Simulation werden die Flüsse über die beiden definierten Kontrollabschnitte in eine Datei namens *r-control-flows.txt* geschrieben.

### Hydrodynamische Lenkung Zusammenfassung

With the above adaptions and using a simulation length of `30000` timesteps (to observe morphodynamic evolution) with a graphical printout period of every `5000` timesteps (to reduce the output file size), the final hydrodynamic steering file should look like this:

```fortran
/ steady2d-gaia.cas
/
TITLE : 'gaia2d steady'
/
/ HOTSTART - continuation is automatic when PREVIOUS COMPUTATION FILE is specified (v9.0+)
PREVIOUS COMPUTATION FILE : r2dsteady.slf / here - 35 CMS initialization after t 15000
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
/
COUPLING WITH : 'GAIA'
GAIA STEERING FILE : gaia-morphodynamics.cas
/
/ DEFAULTS FROM STEADY2D
/
/------------------------------------------------------------------/
/     COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
RESULTS FILE           : r2dsteady-gaia.slf
/
MASS-BALANCE : YES / activates mass balance printouts - does not enforce mass balance
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
/
/ CONTROL SECTIONS
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
/
/------------------------------------------------------------------/
/     GENERAL PARAMETERS
/------------------------------------------------------------------/
TIME STEP : 1.
NUMBER OF TIME STEPS : 30000
GRAPHIC PRINTOUT PERIOD : 5000
LISTING PRINTOUT PERIOD : 5000
/
/------------------------------------------------------------------/
/     NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/ General solver parameters from section 7.1
DISCRETIZATIONS IN SPACE : 11;11
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
ADVECTION : YES
/
/ FINITE ELEMENT SCHEME PARAMETERS - section 7.2.1 in the manual
/------------------------------------------------------------------
TREATMENT OF THE LINEAR SYSTEM : 2 / default is 2 - use 1 to avoid smoothened results
SCHEME FOR ADVECTION OF VELOCITIES : 14 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 14
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITY : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION OF VELOCITY : 1. / v9p0 default
IMPLICITATION COEFFICIENT OF TRACERS : 0.6 / v9p0 default
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VELOCITY : 1.
MASS-LUMPING ON TRACERS : 1.
/ MASS-LUMPING FOR WEAK CHARACTERISTICS : 1. / enabling leads to weak characteristics
SUPG OPTION : 0;0;2;2  / classic supg for U and V
/
/ SOLVER
/------------------------------------------------------------------
INFORMATION ABOUT SOLVER : YES
SOLVER : 1
/
/ TIDAL FLATS  - see section 7.5
TIDAL FLATS : YES
CONTINUITY CORRECTION : YES / default is NO
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2 / value 2 or 3 is required with tidal flats - default is 1
/
/ MATRIX HANDLING - see section 7.6
MATRIX STORAGE : 3 / default is 3
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
/
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 374.805626;0.
/
/ Type of velocity profile can be 1-constant normal profile (default) and (cli) 4-vector is proportional to root (water depth, only for Q)
VELOCITY PROFILES : 4;1
/
/ INITIAL CONDITIONS - not required (hotstart)
/ ------------------------------------------------------------------
/ INITIAL CONDITIONS : 'ZERO DEPTH' / use ZERO DEPTH to start with dry model conditions
/ INITIAL DEPTH : 0.005 / use INTEGER for speeding up calculations
/
/ STABILITY CONTROLS
/ ------------------------------------------------------------------
PRINTING CUMULATED FLOWRATES : YES
/
/------------------------------------------------------------------/
/     TURBULENCE
/------------------------------------------------------------------/
/
DIFFUSION OF VELOCITY : YES / default is YES
TURBULENCE MODEL : 3
/
&ETA
```