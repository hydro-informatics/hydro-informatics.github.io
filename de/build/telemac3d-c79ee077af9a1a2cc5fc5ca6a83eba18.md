---
description: Tutorial zur Einrichtung und Durchführung von 3D hydrodynamischen Simulationen mit Telemac3d nicht-hydrostatischen Gleichungen.
---

(chpt-telemac3d)=
# Über Telemac3d

*Telemac3d* löst die Navier-Stokes-Gleichungen entlang eines dreidimensionalen (3d) Rechengitters mit einem endlichen Elementschema. *Telemac3d* trägt das tetraedrische 3d-Netz aus einem dreieckigen 2d-Netz in einer benutzerdefinierten Anzahl von vertikalen Schichten. Die Anzahl der vertikalen Schichten wird in der TELEMAC-Lenkung (CAS)-Datei definiert.

(chpt-telemac3d-slf)=
# Steady 3d Simulationen mit Telemac

```{admonition} Tutorial under construction
:class: warning
Dieses Tutorial wächst noch und liefert derzeit nur grobe Anleitungen, um ein 3d-Selbstmodell mit TELEMAC zu konstruieren.
```

```{admonition} Requirements
Dieses Tutorial ist für **fortgeschrittene Anfänger* konzipiert und vor dem Tauchen in dieses Tutorial sorgen Sie dafür, dass die {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>`.

Der in diesem Tutorial vorgestellte Fall wurde mit folgender Software erstellt:
* ein Texteditor wie {ref}`Notepad++ <npp>` (jeder andere Texteditor wird den Job machen).
* Telemac v8p2r0 oder neuer ({ref}`stand-alone installation <modular-install>`)
*{ref}`QGIS <qgis-install>`.
* Debian Linux 10 (Buster) auf einer virtuellen Maschine installiert (weiterlesen unter {ref}`software chapter <chpt-vm-linux>`).
```

Dieses Tutorial zeigt, wie eine stetige Entladung mit Telemac3d mit dem SLF-Geometrieformat simuliert werden kann. **Das Tutorial baut auf der stetigen2d-Simulation* der 35-m$^3$/s-Entladung auf und benötigt die folgenden Daten aus den {ref}`pre-processing <slf-prepro-tm>` und {ref}`steady2d <telemac2d-steady>` Tutorials, die durch Klicken auf die Dateinamen heruntergeladen werden können:

* Das Rechennetz in [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf).
* Die Grenzdefinitionen in [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/boundaries.cli).
* Die Ergebnisse des {ref}`steady 2d model <tm2d-init-dry>`simulatons von 35 m$^3$/s in [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) (bis`t=15000`)

Betrachten Sie das Speichern der Dateien in einem neuen Ordner, wie `/steady3d-tutorial/`.

```{admonition} 3d-steady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/steady3d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/steady3d-tutorial/).
```

(prepro-3dsteady-slf)=
## Wiederverwendung des 2d Modells

Die Simulation von 3d-Flow-Phänomenen-Flows erfordert die Anpassung von Schlüsselwörtern und zusätzlichen Schlüsselwörtern (z.B. zur Verknüpfung von Flüssigkeitsgrenzdateien) in der Steuerungsdatei (`*.cas`) aus dem stationären 2d-Tutorial ([download stationär2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

```{admonition} View the steady3d steering file
Um die Integration der stationären3d-Simulations-Keywords in der Lenkdatei anzuzeigen, kann die `steady3d.cas`-Datei [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas).
```


## Datei steuern

This tutorial features a steady, hydrodynamic model with an inflow rate of 35 m$^3$/s (prescribed upstream flow rate boundary) and an outflow depth of 2 m (prescribed downstream elevation). The simulation uses 5 vertical layers that constitute a numerical grid of prisms. 3d outputs of *U* (*x*-direction), *V* (*y*-direction), and *W* (*z*-direction) velocities, as well as the elevation *Z*, are written to a file named `r3dsteady.slf`. 2d outputs of depth-averaged *U* velocity (*x*-direction), depth-averaged *V* velocity (*y*-direction), and water depth *h* are written to a file named `r2d3dsteady.slf`.

Der folgende Codeblock zeigt die Lenkdatei `t3d_flume.cas` und Details für jeden Parameter werden nach dem Codeblock bereitgestellt. Der slash `/` charakter kommentiert Zeilen (d.h. TELEMAC ignoriert alles in einer Zeile des `/`-Zeichens). Der `:`-Zeichen trennt `VARIABLE NAME` und `VALUE`s. Alternativ zum `:` kann auch ein `=`-Zeichen verwendet werden. Die `&ETA` am Ende der Datei macht TELEMAC eine Liste der verwendeten Keywords aus (in der *DAMOCLES*-Routine).

```{tip}
Um die Einstellung der Lenkungsdatei (CAS) für dieses Tutorial zu erleichtern, [downloaden Sie das Template](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas) (rechtsklicken Sie auf den Link > *Save Link As...* navigieren Sie in den lokalen Tutorialordner), der weitere Beschreibungen und Optionen für Simulationsparameter enthält.
```

````{admonition} Expand to view the steady3d.cas steering file
:class: note, dropdown
```fortran
/ steady3d.cas
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
/
TITLE : '3d steady'
MASS-BALANCE : YES
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
3D RESULT FILE           : r3dsteady.slf
2D RESULT FILE           : r2d3dsteady.med
/ FILE FOR 2D CONTINUATION : r2dsteady.slf / activates 2d-init automatically since v9.0 (no extra keyword needed)
/
VARIABLES FOR 2D GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
VARIABLES FOR 3D GRAPHIC PRINTOUTS : Z,U,V,W
/
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
/
TIME STEP : 1.
NUMBER OF TIME STEPS : 8000
GRAPHIC PRINTOUT PERIOD : 500
LISTING PRINTOUT PERIOD : 200
/
/------------------------------------------------------------------/
/			VERTICAL
/------------------------------------------------------------------/
/ vertical cell height defined by initial condition x no. of levels
/ will be adapted for every time step
NUMBER OF HORIZONTAL LEVELS : 5 / default and minimum is 2, upward vertical direction
MESH TRANSFORMATION : 1 / 0-CALCOT (user defined) 1-SIGMA (default) 3-user defined
ELEMENT : 'PRISM' / default is 'PRISM' but preferably use 'TETRAHEDRON'
/
/------------------------------------------------------------------/
/			NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/
/ ADVECTION-DIFFUSION
/------------------------------------------------------------------
SCHEME FOR ADVECTION OF VELOCITIES : 5
SCHEME FOR ADVECTION OF K-EPSILON : 5
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4 / use 2 for without tidal flats for speed
SCHEME OPTION FOR ADVECTION OF K-EPSILON : 4
SCHEME OPTION FOR ADVECTION OF TRACERS : 4
/
MATRIX STORAGE : 3 / 1 (element-by-element), 3 (segment-wise faster)
SUPG OPTION : 1  / 0=none 1=classical SUPG (default) 2=Courant-scaled; single integer since v9.0
/
/ PROPAGATION HEIGHT AND STABILITY
/ ------------------------------------------------------------------
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITIES : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION : 1.
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
/
/ MASS LUMPING - enable to fasten calculations (smoothens) - possibly avoid in 3d
/ ------------------------------------------------------------------
/ MASS-LUMPING FOR DIFFUSION : 1 / 1 is ON - 0 is OFF (default)
/ MASS-LUMPING FOR DEPTH : 1.  / VELOCITY has no effect
/ MASS-LUMPING FOR WEAK CHARACTERISTICS : 1
/
/------------------------------------------------------------------/
/			HYDRODYNAMICS
/------------------------------------------------------------------/
/
/ HYDRODYNAMIC SOLVER
/------------------------------------------------------------------
NON-HYDROSTATIC VERSION : YES
/ solver options are
/ 1-conjugate method 2-conjugate residual method 3-conjugate gradient
/ 4-minimum error 5-square conjugate gradient 6-stabilized conjugate gradient CGSTAB
/ 7-Generalised Minimum RESidual GMRES is the favorite for improperly conditioned systems - RECOMMENDED in 3d
/ 8-direct solver YSMP (Yale) is not working with parallel versions
SOLVER FOR DIFFUSION OF VELOCITIES : 1 / 1-default
SOLVER FOR PROPAGATION : 7 / 7-default
SOLVER FOR PPE : 7 / 7-default
/ SOLVER FOR DIFFUSION OF TRACERS : 1 / one value per tracer
SOLVER FOR DIFFUSION OF K-EPSILON : 1 / 1-default
/
/ Set OPTIONS for GMRES
/ Increasing values for precision, but also more memory consumption
OPTION OF SOLVER FOR DIFFUSION OF VELOCITIES : 5 / 5-default since v8
OPTION OF SOLVER FOR PROPAGATION : 5 / 5-default since v8
OPTION OF SOLVER FOR PPE : 5 / 5-default since v8
OPTION OF SOLVER FOR DIFFUSION OF K-EPSILON : 5 / 5-default since v8
/
/ Solver ACCURACY
ACCURACY FOR DIFFUSION OF VELOCITIES : 1.E-8 / default is 1.E-8
ACCURACY FOR PROPAGATION : 1.E-8 / default is 1.E-8
ACCURACY FOR PPE : 1.E-4 / default is 1.E-4
ACCURACY FOR DIFFUSION OF K-EPSILON : 1.E-8 / default is 1.E-8
/
/ Solver MAXIMUM ITERATIONS
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF VELOCITIES : 100 / default is 60
MAXIMUM NUMBER OF ITERATIONS FOR PROPAGATION : 200 / default is 100
MAXIMUM NUMBER OF ITERATIONS FOR PPE : 100 / default is 100
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF K-EPSILON : 200 / default is 200
/
/ PRECONDITIONING - DEFAULT Value is 2 for all
PRECONDITIONING FOR DIFFUSION OF VELOCITIES : 2
PRECONDITIONING FOR PROPAGATION : 2
PRECONDITIONING FOR PPE : 2
PRECONDITIONING FOR DIFFUSION OF TRACERS : 2
PRECONDITIONING FOR DIFFUSION OF K-EPSILON : 2
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/ Use Nikuradse roughness law - all others are not 3D compatible
LAW OF BOTTOM FRICTION : 5
LAW OF FRICTION ON LATERAL BOUNDARIES : 5  / for natural banks - 0 for symmetry
FRICTION COEFFICIENT FOR THE BOTTOM : 0.1 / 3 times d90 according to van Rijn
/
/ Liquid boundaries - avoid Thompson (invalid in 3d)
PRESCRIBED FLOWRATES  : 35.;35.
PRESCRIBED ELEVATIONS : 0.;371.33
/
/ INITIAL CONDITIONS
/ ------------------------------------------------------------------
INITIAL CONDITIONS : 'CONSTANT DEPTH' / or CONSTANT DEPTH see docs sec. 4.2
INITIAL DEPTH : 0.1
INITIAL GUESS FOR DEPTH : 1 / INTEGER for speeding up calculations
/
/ Other
/------------------------------------------------------------------
VELOCITY VERTICAL PROFILES : 2;2 / 0 (user-defined), 1 (Constant), 2 (Log)
VELOCITY PROFILES : 1;1 / horizontal profile
/
/------------------------------------------------------------------/
/			TIDAL FLATS
/------------------------------------------------------------------/
TIDAL FLATS : YES / default is YES - disable for faster model runs
/ TREATMENT OF NEGATIVE DEPTHS : 2 / requires mass lumping for depth set to 1
TREATMENT ON TIDAL FLATS FOR TRACERS : 1 / ensure conservation
/ more in section docs 6.6
/
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/ in 3d use k-epsilon model, alternatively Spalart-Allmaras (5) or
/  Smagorinsky (4) for highly non-linear flow
HORIZONTAL TURBULENCE MODEL : 3
VERTICAL TURBULENCE MODEL : 3
MIXING LENGTH MODEL : 3 / telemac docs sec. 5.2.2
COEFFICIENT FOR HORIZONTAL DIFFUSION OF VELOCITIES : 1.E-6 / is default
COEFFICIENT FOR VERTICAL DIFFUSION OF VELOCITIES   : 1.E-6 / is default
/
/------------------------------------------------------------------/
/			PARALLELISM
/------------------------------------------------------------------/
PARALLEL PROCESSORS : 0 / default is 0 - all others define number of processors
/ PARTIONING TOOL : METIS / default is METIS, others are SCOTCH, PARMETIS, PTSCOTCH
/
/ ENABLE COMMAND PRINTS IN TERMINAL
&ETA
```

````

(tm3d-slf-env)=
### Computing Environment

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 3 in der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).**

Die Berechnungsumgebung definiert eine **Title*** (z.B. `TELEMAC 3D FLUME`). Die wichtigsten Parameter sind die **input** Dateien:

*`GEOMETRY FILE`: `qgismesh.slf` - Alternativ wählen Sie eine *serafin* (SLF) Geometriedatei
*`Boundary conditions file`: `boundaries.cli` - mit einer *SLF*-Datei mit einer *CLI*-Grenzdatei
*`FILE FOR 2D CONTINUATION`: `r2dsteady.slf` — optional; initialisiert das 3D-Modell aus einer 2D-Ergebnisdatei, die eine stetige 3D-Simulation darstellt. Seit v9.0 reicht die Bereitstellung dieses Schlüsselworts aus, um die 2D-Fortsetzung zu aktivieren; das frühere `2D CONTINUATION : YES`word wurde entfernt. Das Dateiformat ist standardmäßig an `'SERAFIN'`; verwenden Sie `FILE FOR 2D CONTINUATION FORMAT : 'MED'` wenn die Quelldatei im MED-Format ist.

Der **output*** kann mit folgenden Keywords definiert werden:

* `3D RESULT FILE`: `r3dsteady.slf` - can be either a *MED* file or a *SLF* file
* `2D RESULT FILE`: `r2d3dsteady.med` - can be either a *MED* file or a *SLF* file
* `VARIABLES FOR 3D GRAPHIC PRINTOUTS`:  `U,V,H,S,Q,F` - many more options can be found in section 3.12 of the [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf)
* `VARIABLES FOR 2D GRAPHIC PRINTOUTS`:  `U,V,H` - many more options can be found in section 3.13 of the [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf)

Darüber hinaus druckt die `MASS-BALANCE : YES`-Einstellung die Massenflüsse und Fehler in der Rechenregion aus, was ein wichtiger Parameter für die Überprüfung der Plausibilität des Modells ist.

### Allgemeine Parameter
**Die folgenden Beschreibungen beziehen sich auf Abschnitt 3.2 in der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).**

Die *Allgemeine Parameter* geben *time* und *location* Einstellungen für die Simulation an:

* **Location** can be used for geo-referencing of outputs (not to set in this tutorial).
* **Time**:
  + `TIME STEP`: `1.0` defines the time step as a multiple of graphic/listing printout periods.<br>*Use small enough and sufficient time steps to achieve/increase computational stability and increase to yield computational efficiency.*
  + `NUMBER OF TIME STEPS`: `8000` defines the overall simulation length. <br>*Limit the number of time steps to a minimum (e.g., until equilibrium conditions are reached in a steady simulation).*
  + `GRAPHIC PRINTOUT PERIOD` : `500` time step at which graphic variables are written,
  + `LISTING PRINTOUT PERIOD`: `200` time step at which listing variables are printed (in this example, listings are printed every `200` · `1.0` = 200 seconds)

Ändern Sie die Zeitparameter, um den Effekt in der Simulation später zu untersuchen.

```{attention}
Grafikausdrucke, wie alle anderen Datenausdrucke, sind zeitaufwendig und verlangsamen die Simulation.
```

### Numerische Parameter

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 6 in der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).**

Dieser Abschnitt definiert interne numerische Parameter für die {term}`Advection` und {term}`Diffusion`.

In Telemac3d wird empfohlen, das sogenannte Distributive Predictor-corrector (PSI)-System ([lesen Sie mehr](https://henry.baw.de/bitstream/handle/20.500.11970/104314/13_Hervouet_2015.pdf?sequence=1&isAllowed=y) at the BAW's Hydraulic Engineering Repository) mit lokaler Implikation für Gezeitenwohnungen (für Geschwindigkeit, Tracer und k-epsilon) zu verwenden:

* Set the PSI scheme:
    + `SCHEME FOR ADVECTION OF VELOCITIES`: `5`
    + `SCHEME FOR ADVECTION OF K-EPSILON`: `5`
    + `SCHEME FOR ADVECTION OF TRACERS`: `5`
* Enable predictor-corrector with local implication:
    + `SCHEME OPTION FOR ADVECTION OF VELOCITIES`: `4`
    + `SCHEME OPTION FOR ADVECTION OF K-EPSILON`: `4`
    + `SCHEME OPTION FOR ADVECTION OF TRACERS`: `4`

Diese Werte (`5` für das System und `4` für die Systemoption) sind Standardwerte seit v8p1, aber es macht immer noch Sinn, diese Parameter für die Rückwärtskompatibilität der Lenkdatei zu definieren. Wenn das Auftreten von Gezeitenwohnungen ausgeschlossen werden kann (Anmerkung, dass bereits ein wenig Rückwasser vor einer Barriere eine Gezeitenwohnung darstellen kann), kann die `SCHEME OPTIONS` zur Beschleunigung der Simulation in der Regel auf `2` gesetzt werden.

Ähnlich wie {term}`Advection` können die obigen Keywords verwendet werden, um {term}`Diffusion`Schritte zu definieren (`ADVECTION` mit `DIFFUSION` in den Keywords zu ersetzen), wobei ein Wert von `0` verwendet werden kann, um den Standardwert von `1` und disable Diffusion zu überschreiben.

Das Schlüsselwort `SUPG OPTION` (Streamline Upwind Petrov Galerkin) steuert, ob Upwinding gilt und welche Art von Upwinding verwendet wird. Seit v9.0 nimmt dieses Keyword eine **single ganze Zahl*** (Earlierversionen akzeptierten eine Vierelementliste; dieses Formular ist nicht mehr gültig):

* `0` disables upwinding,
* `1` ermöglicht Upwinding mit dem klassischen SUPG-System (Standard; empfohlen, wenn die {term}`CFL`bedingung unbekannt ist), und
* `2` ermöglicht den Aufschwung mit einem Courant-scaled SUPG-System, wo die Höhe der Aufwindung der lokalen Courant-Nummer entspricht.

Lesen Sie mehr in Abschnitt 6.2.2 der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).

Eine zusätzliche Möglichkeit zur Beschleunigung besteht darin, eine Massenklumpung für Diffusion, Tiefe und/oder schwache Eigenschaften zu ermöglichen. Massenklumpen führt zu schneller Konvergenz, aber es führt künstliche Dispersion in den Ergebnissen ein, weshalb die Massenklumpung durch die TELEMAC-Entwickler entmutigt wird. Die bereitgestellte [steady3d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas) umfasst die Schlüsselwörter für Massenklumpen, obwohl sie über die `/` zu Beginn der Zeile deaktiviert sind.

** Implizitierungsparameter* (`IMPLICITATION FOR DEPTH` und `IMPLICITATION FOR VELOCITIES`) sollten zwischen 0,55 und 0,60 (Standard 0,55 seit v8p1) eingestellt werden und den Grad der zeitlichen Gewichtung in der Diskretisierung kontrollieren. `IMPLICITATION FOR DIFFUSION` wird standardmäßig auf `1.0` gesetzt. Lesen Sie mehr in Abschnitt 6.4 der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).

Mit dem Parameter `FREE SURFACE GRADIENT COMPATIBILITY` kann die Modellstabilität erhöht werden. Sein Standardwert ist `1.0`, aber es kann auf `0.1` reduziert werden, um störende Schwingungen in Modellen mit steilen Badgradienten zu unterdrücken.

Für Flusshydraulik wird die Aktivierung der nicht-hydrostatischen Druckkorrektur empfohlen: `NON-HYDROSTATIC VERSION : YES`. Dies fügt zu jedem Zeitschritt eine Poisson-Gleichung (PPE) hinzu, deren Soldat von `SOLVER FOR PPE`,`OPTION OF SOLVER FOR PPE`, `ACCURACY FOR PPE`,`MAXIMUM NUMBER OF ITERATIONS FOR PPE` und `PRECONDITIONING FOR PPE` gesteuert wird. Der Standardlöser der CAS-Datei (`7`, GMRES) und das Genauigkeitsziel von `1.E-4` sind für die meisten Flussmodelle geeignet. Lesen Sie mehr über die Solvenzparameter in Abschnitt 6.5 der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).

(tm3d-slf-vertical)=
### Vertikale (3d) Parameter

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 4.1 in der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).**

Telemac3d wird *Horizontal Ebenen* (d.h. Schichten) hinzufügen, die Kopien der 2d-mesh entsprechen, um eine 3d-mesh Prismen (Standard) oder Tetraeder zu bauen. Diese Parameter können definiert werden mit:

* `NUMBER OF HORIZONTAL LEVELS`: `5`, wobei Standard und Minimum `2` und die horizontalen Ebenen in vertikaler Richtung nach oben weisen. Die Dicke der vertikalen Schichten ergibt sich aus der Wassertiefe, die durch den Parameter `INITIAL ELEVATION` (siehe Abschnitt unter {ref}`3d initial conditions <tm3d-slf-init>`) benutzerdefinierte werden kann.
* `MESH TRANSFORMATION`: `1` ist die Art der Verteilung (Standard ist `1`, eine homogene Sigmaverteilung). Für unsteady (quasi-steady) Simulationen, setzen Sie diesen Wert an `2` (oder `0` - calcot) und implementieren Sie ein `ZSTAR`-Array in einer Benutzer-Forran-Datei (`USER_MESH_TRANSFORM` subroutine).
*`ELEMENT`: `'PRISM'` (Standard) und Prismen können optional in Tetraeder aufgeteilt werden, indem dieser Parameter an `'TETRAHEDRON'` (kann die Simulation möglicherweise abstürzen).

```{admonition} Unsteady (quasi-steady) simulations
:class: tip
Für unruhige Simulationen (zeitvariable Zu- und Abflussraten) wird die Dicke vertikaler Schichten mit dem `ZSTAR`-Parameter in einer Benutzer-Forran-Datei (Subroutine) wie in Abschnitt 4.1 des [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf) beschrieben vordefiniert. Lesen Sie mehr über die Einrichtung einer unruhigen Simulation mit TELEMAC in der {ref}`Telemac2d unsteady tutorial <chpt-unsteady>`.
```

Um mit dem Schreiben von Subroutinen zu beginnen (es ist keine Magie), werfen Sie einen Blick auf das **bottom bc* Beispiel (`~/telemac/v9.0.0/examples/telemac3d/bottom_bc/`). Insbesondere prüfen Sie die Benutzer fortran-Datei `/user_fortran-source/user_mesh_transf.f` und deren Ruf in der Lenkdatei `t3d_bottom_source.cas` durch die Definition des `FORTRAN FILE`keyword und der Einstellung von `MESH TRANSFORMATION : 2`.

(tm3d-slf-boundaries)=
### Geöffnet (flüssig)

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 4.2 in der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).**

Parameter für **Boundary Conditions* ermöglichen die Definition von Rauhigkeitsgesetzen und Eigenschaften von Flüssigkeitsgrenzen.

TELEMAC-Entwickler empfehlen die Nutzung des {cite:t}`nikuradse_stromungsgesetze_1933`Rohheitsgesetzes in 3d (Anzahl `5`), da alle anderen nicht sinnvoll oder nicht integral in der 3d-Version implementiert sind. Um das {cite:t}`nikuradse_stromungsgesetze_1933`Rohheitsrecht auf den Grund und die Grenzen anzuwenden, verwenden Sie:

* `LAW OF BOTTOM FRICTION`: `5`
* `LAW OF FRICTION ON LATERAL BOUNDARIES`: `5`, which can well be applied to model natural banks, or set to `0` (no-slip) for symmetry.<br>*Note that the boundary conditions file sets the `LIUBOR` and `LIVBOR` for the `leftwall` and `rightwall` boundary edges to zero, to enable friction.
* `FRICTION COEFFICIENT FOR THE BOTTOM`: `0.1` corresponds to 3 times a hypothetical *d90* (grain diameter of which 90% of the surface grain mixture are finer) according to {cite:p}`vanrijn2019`.
* `FRICTION COEFFICIENT FOR LATERAL SOLID BOUNDARIES`: `0.1` corresponds to 3 times a hypothetical *d90*, similar as for the bottom.

Die Flüssiggrenzwerte für `PRESCRIBED FLOWRATES` und `PRESCRIBED ELEVATIONS` entsprechen den Definitionen der **downstream* Grenzkante in Zeile 2 und der **upstream* Grenzkante in Zeile 3. Aus der Grenzdatei versteht TELEMAC die **downstream*-Grenze als Randnummer **1** (erstes Listenelement) und die **upstream*-Grenze als Randnummer **2** (zweites Listenelement). Daher:

* Der Listenparameter `PRESCRIBED FLOWRATES : 35.;35.` gibt dem **downstream** und den **upstream** Grenzkanten einen Durchsatz von 35 m$^3$/s zu.
* Der Listenparameter `PRESCRIBED ELEVATIONS : 0.;371.33` gibt der **upstream*-Grenze (Anzahl 1) und einer Höhe von 371.3 m a.s.l der **downstream*-Grenze (Anzahl 2) keine Höhe zu. Um zu erinnern, wie TELEMAC offene Grenzen zählt, lesen Sie das Kommentarfeld in der {ref}`steady2d tutorial <tm2d-bounds>`.

The `0.` value for the water does physically not make sense at the upstream boundary, but because they do not make sense, and because the boundary file (`boundaries.cli`) only defines (*prescribes*) a flow rate (by setting `LIUBOR` and `LIVBOR` to `5`), TELEMAC will ignore the zero-water depth at the upstream boundary.

Anstelle einer Liste in der Steuerung `*.cas`-Datei können die flüssigen Randbedingungen auch mit einer flüssigen Randbedingungsdatei im Textformat *ASCII* definiert werden. Zu diesem Zweck kann eine `LIQUID BOUNDARIES FILE` oder eine `STAGE-DISCHARGE CURVES FILE` (§ 4.3.8 und 4.3.10 in der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf)] definiert werden. Die [steady3d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas)-Datei enthält diese Keywords im Abschnitt *COMPUTATION ENVIRONMENT*, obwohl sie am Anfang der Zeile durch das `/`-Zeichen deaktiviert sind. Eine flüssige Begrenzungsdatei (*QSL*) kann so aussehen:

```fortran
# t3d_canal.qsl
# time-dependent inflow upstream-discharge Q(2) and outflow downstream-depth SL(1)
T           Q(2)     SL(1)
s           m3/s     m
0.            0.     374.0
500.        100.     375.0
5000.       150.     575.7
```

```{admonition} ELEVATION versus DEPTH
:class: note
Der `ELEVATION`-Parameter in der `*.cas`-Datei bedeutet Wassertiefe, während das `ELEVATION`-Keyword in einer externen Flüssigkeitsgrenzdatei (z.B. Stage-Decharge-Kurve) auf absolute (geodetische) Erhöhung (`Z` plus `H`) verweist.
```

Bei vorgegebener Strömungsgeschwindigkeit kann für alle Flüssigkeitsgrenzen ein horizontales und ein vertikales Geschwindigkeitsprofil vorgegeben werden. Bei nur einem **downstream** und einer **upstream** Flüssigkeitsgrenze (in dieser Reihenfolge nach der oben definierten Grenzdatei) sind die Geschwindigkeitsprofil-Keywords Listen von je zwei Elementen, wobei der erste Eintrag auf den **downstream*** und das zweite Element auf **upstream** Grenzkanten bezieht:

*`VELOCITY PROFILES`: `1;1` ist die Standardoption für die **horizontal**-Profile. Wenn auf `2;2` gesetzt, werden die Geschwindigkeitsprofile aus der Randbedingungsdatei gelesen.
*`VELOCITY VERTICAL PROFILES`: `2;2` setzt die **vertical** Geschwindigkeitsprofile an logarithmic. Der Standard ist `1;1` (constant). Alternativ kann eine benutzerdefinierte `USER_VEL_PROF_Z` subroutine in einer Fortran-Datei implementiert werden.

Lesen Sie mehr über Optionen zur Definition von Geschwindigkeitsprofilen in Abschnitt 4.3.12 der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).

(tm3d-slf-init)=
### Ursprüngliche Bedingungen
Die **initial-Bedingungen* beschreiben den Zustand zu Beginn der Simulation. Dieses Tutorial verwendet eine konstante Höhe (entsprechend einer konstanten Wassertiefe) von `2.` und ermöglicht die Verwendung einer anfänglichen Vermutung für die Wassertiefe, um die Simulation zu beschleunigen:

*`INITIAL CONDITIONS`: `'CONSTANT ELEVATION'` kann alternativ an `'CONSTANT DEPTH'`
*`INITIAL DEPTH`: `0.1` entspricht der Wassertiefe.
*`INITIAL GUESS FOR DEPTH`: `1` muss ein **integer***-Wert sein und die Berechnung beschleunigt (Konvergenz).


### Turbulenzen

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 5.2 in der [Telemac3d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf).**

Die Grundprinzipien der Turbulenz und deren Anwendung an die {term}`Navier-Stokes equations` werden in der {ref}`steady Telemac2d tutorial <tm2d-turbulence>` erläutert. In 3d empfehlen TELEMAC Entwickler das $k-\epsilon$ Modell (`3`) für die meisten Flussanwendungen. Folgende Modellnummern sind sowohl für `HORIZONTAL TURBULENCE MODEL` als auch für `VERTICAL TURBULENCE MODEL` erhältlich:

* `1` — constant viscosity (controlled by `COEFFICIENT FOR HORIZONTAL/VERTICAL DIFFUSION OF VELOCITIES`),
* `2` — mixing length (meaningful only for `VERTICAL TURBULENCE MODEL`; see below),
* `3` — $k-\epsilon$ model (recommended default),
* `4` — Smagorinski model,
* `5` — {cite:t}`spalart1992` one-equation {term}`RANS` model; **both** `HORIZONTAL TURBULENCE MODEL` **and** `VERTICAL TURBULENCE MODEL` must be set to `5`,
* `7` — $k-\omega$ model (TELEMAC-3D only), and
* `9` — Detached Eddy Simulation (DES; TELEMAC-3D only).

Die Lenkdatei verwendet das Modell $k-\epsilon$ für horizontale und vertikale Richtungen:

* `HORIZONTAL TURBULENCE MODEL`: `3`
* `VERTICAL TURBULENCE MODEL`: `3`

If `VERTICAL TURBULENCE MODEL` is set to `2` (mixing length), a `MIXING LENGTH MODEL` value can be assigned. Since v9.0, the default is `3` ({cite:t}`nezu1993`, recommended for river flow). A value of `1` (Prandtl mixing length) remains available and is preferable for strongly tidal environments.



## Laufen Telemac3d

Gehen Sie in den Konfigurationsordner der lokalen TELEMAC-Installation (z.B. `~/telemac/v9.0.0/configs/`) und starten Sie die Umgebung (z.B. `pysource.openmpi.sh` - verwenden Sie die gleiche wie für die Erstellung von TELEMAC).

```
cd ~/telemac/v9.0.0/configs
source pysource.openmpi.sh
```

````{admonition} If you are using the Hydro-Informatics (Hyfo) Mint VM
:class: note, dropdown

Wenn Sie mit der {ref}`Mint Hyfo VM <hyfo-vm>` zusammenarbeiten, laden Sie die TELEMAC-Umgebung wie folgt ein:

```
cd ~/telemac/v8p2/configs
source pysource.hyfo-dyn.sh
```
````

Mit der geladenen TELEMAC-Umgebung wechseln Sie in das Verzeichnis, in dem die oben erstellten 3d-flume-Simulationszeiten (z.B. `/home/telemac/v9.0.0/mysimulations/steady3d-tutorial/`) gespeichert sind und die `*.cas`-Datei ausführen, indem Sie das Skript **telemac3d.py** anrufen.

```
cd ~/telemac/v9.0.0/mysimulations/steady3d-tutorial/
telemac3d.py steady3d.cas
```


Infolgedessen sollte eine erfolgreiche Berechnung mit folgenden Zeilen (oder ähnlichen) in *Terminal* enden:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                            10  MINUTES
                            17  SECONDS
... merging separated result files

... handling result files
       moving: r3dsteady.slf
... deleting working dir

My work is done
```

