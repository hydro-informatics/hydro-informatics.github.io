---
description: Einführung zur Kopplung von TELEMAC Hydrodynamik mit GAIA Morphodynamik zur Simulation von Bettlast und hängenden Sedimenttransport in Flüssen, Seen und Mündungen.
---

# Einführung und Kupplung

```{admonition} Requirements
Dieses Tutorial ist für ** Fortgeschrittene Modeler** konzipiert und vor dem Tauchen in dieses Tutorial sorgen Sie dafür, dass ** die {ref}`TELEMAC pre-processing <slf-prepro-tm>` und {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials** fertig gestellt werden.

Der in diesem Tutorial vorgestellte Fall wurde mit folgender Software erstellt:
* {ref}`Notepad++ <npp>` Texteditor (jeder andere Texteditor wird auch tun.)
* TELEMAC v9.0.0 ({ref}`stand-alone installation <modular-install>`) - frühere Versionen können einige der in diesem eBook verwendeten Keywords nicht erkennen.
*{ref}`QGIS <qgis-install>`.
* Debian Linux / Ubuntu 24.04 (weiterlesen unter {ref}`software chapter <chpt-vm-linux>`).
```

## Terminologie
Eine hydromorphodynamische Simulation impliziert die Modellierung von abgefahrenen **{term}`Sediment transport`*-Prozessen. Die bisherigen Abschnitte in diesem eBook konzentrieren sich auf die Hydrodynamik, die als * die Untersuchung von Flüssigkeiten in Bewegung* definiert ist, und dieser Abschnitt konzentriert sich auf **morphodynamik* definiert als ** die Untersuchung von zeitabhängigen Veränderungen der Formen von Alluvialbetten und deren zugrunde liegenden Vorgänge*.

(gaia-seditrans)=
## Sediment Transport Moden

TELEMAC verfügt über ein dediziertes Modul namens Gaia zur Modellierung von Morphodynamik. Gaia ermöglicht die Modellierung des Sedimenttransports und der morphologischen Evolution (d.h. {term}`Topographic change`) in Flüssen, Seen und Mündungen. Es kommt mit besonderen Routinen, um eine spatio-temporale Variation der Korngrößen, Grading-Kurven und Flussbettschichtung zur Simulation des Sedimenttransports in Form von **{term}`Bedload` (Koarse-Sediment)* und/oder **{term}`Suspended load` (Endsediment)* zu betrachten. {term}`Bedload` wird durch Lösen von semi-empirischen Gleichungen, wie die Formel{cite:t}`meyer-peter_formulas_1948` berechnet. {term}`Suspended load` ist modelliert durch die Lösung der {term}`Advection`-{term}`Diffusion`-Gleichungen (typischerweise die {term}`RANS`-Form), die Verschlüsse für Sedimenterosion und Depositionsflüsse erfordern. {numref}`Figure %s <bl-vs-sl>` illustriert qualitativ die beiden Grundmodi des Sedimenttransports in Form von Hängelast und Bettlast. Ob ein Partikel in Suspension oder als Beladung transportiert wird, kann auch durch Berechnung der {term}`Rouse number` bestimmt werden.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-transport.png
:alt: sediment transport bedload suspended load
:name: bl-vs-sl

Qualitative Darstellung von zwei Arten des Sedimenttransports. Links: Schwebelastung in Form von feinen Partikeln, die sich mit der Schüttung bewegen; rechts: Bettlast in Form von Partikeln, die auf dem Flussbett rollen, springen oder gleiten.
```

Sediment is further distinguished between very fine, **cohesive** sediment and coarser, **non-cohesive** sediment. In addition, Gaia accounts for bed evolution through an iterative solution of the {term}`Exner equation` {cite:p}`exner_uber_1925` for mass conservation.

Die Rekrutierung von Sedimenten für Schwebelast- und Beladungstransporte erfordert einen detaillierten Blick auf das Flussbett, das später im Abschnitt über die Definition von {ref}`the riverbed composition and the active layer <gaia-active-lyr>` vorgelegt wird.


(tm-coupling)=
## Kupplung TELEMAC und Gaia

Das Morphodynamikmodul Gaia kann intern **gekoppelt* mit den hydrodynamischen Modellen Telemac2d (Auflösung der {term}`Shallow water equations`) oder Telemac3d (Auflösung der Reynolds-gemittelten {term}`Navier-Stokes (RANS) equations <Navier-Stokes equations>`) sein. Dieser Abschnitt erklärt die Arten der Kupplung Telemac2d/Telemac3d (Hydrodynamik) mit Gaia (morphodynamik).

### Von Sisyphe nach Gaia

Sisyphe ist das traditionelle Sedimenttransportmodul in TELEMAC, das weitgehend durch das einheitlichere Gaia-Modul ersetzt wurde. Gaia basiert auf dem historischen Modul SISYPHE, mit einer Vielzahl von Verbesserungen, Korrekturen und Optimierungen implementiert. Gaias einheitlicher Rahmen verwaltet effizient verschiedene Sedimentklassen, Sand-Mud-Gemische und sowohl 2D- als auch 3D-Raumdimensionen. Um Spezifikationen über die hier vorgestellten Features in der TELEMAC-Dokumentation und dem TELEMAC-Forum zu erhalten, ist es nützlich, das SISYPHE-Erbe zu kennen. SISYPHE-Routinen sind noch in den letzten TELEMAC-Versionen über Gaia verfügbar, obwohl einige Keywords Anpassungen erfordern. Lesen Sie mehr in der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) in Anlage 8.1 und in der gaia.dico (`telemac/v9.0.0/sources/gaia/gaia.dico`)

### Kupplung Hydrodynamik (Telemac2d/3d) und Morphodynamik (Gaia)

Ein hydromorphodynamisches Zahlenmodell kann entweder **voll gekoppelt* oder ** entkoppelt** sein.

Vollgekoppeltes Modell
: Ein vollgekoppeltes Modell löst die hydrodynamische {term}`Navier-Stokes equations` gleichzeitig mit Sedimenttransportgleichungen (d.h. Erosion und Abscheidungsfluss von und zum Flussbett über die {term}`Exner equation`). Bed Elevation (d.h. {term}`Topographic change`) wird für jeden Zeitschritt berechnet, was zu **long Berechnung** Zeiten führt. Neben der Kopplung der Schwerkraft-getriebenen Hydrodynamik (d.h. der Schüttung entlang Talhängen), {term}`Sediment transport` und {term}`Topographic change` kann ein Modell auch mit (Oberflächen-)Wellenhydrodynamik gekoppelt werden.

*Anwendungsbereich:* Schnelle morphodynamische Prozesse, wie hyperkonzentrierte sedimentbeladene Strömungen oder Trümmerfluss.



Entkoppeltes Modell
: Ein entkoppeltes Modell wechselt zwischen der Lösung von Hydrodynamik und Morphodynamik (d.h. der {term}`Exner equation`). Das Flussbett wird bei der Berechnung hydrodynamischer Größen als fest angesehen, und dann werden Betthöhenänderungen getrennt nach dem berechneten Strömungsfeld berechnet. Dieser *asynchrone* Ansatz ist rechnerisch effizienter als die volle Kupplung.

*Anwendungsbereich:* Die meisten Flussmodelle, insbesondere See- oder Ozeanmodelle, bei denen morphodynamische Zeitskala viel länger sind als hydrodynamische Zeitskala.

Gaia folgt dem ** entkoppelten* Ansatz. Der für die morphodynamische Berechnung verwendete Zeitschritt ist der gleiche wie für Hydrodynamik (in der Telemac2d- oder Telemac3d-Lenkdatei angegeben). Zu jedem Zeitpunkt werden Hydrodynamik zunächst mit dem eingefrorenen Bett gelöst, dann werden die Sedimenttransportgleichungen und die Bettentwicklung (Exnergleichung) basierend auf dem berechneten Strömungsfeld gelöst.

```{admonition} Coupling period for wave-current-sediment interactions
:class: note
Bei der Kopplung von Gaia mit dem Wellenmodul TOMAWAC kann eine ** Kopplungsdauer** angegeben werden, um zu kontrollieren, wie häufig Wellenfelder aktualisiert werden. Dies ist deshalb relevant, weil Wellenberechnungen teuer sein können und Wellenverhältnisse sich nicht so schnell wie Ströme ändern können. Für die grundsätzliche Telemac2d/3d-Gaia-Kopplung ohne Wellen werden die Morphodynamik bei jedem hydrodynamischen Zeitschritt berechnet. Lesen Sie mehr über die Wellenkupplung in Abschnitt 5.1 der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

### Anforderungen an die Coupling Gaia

Neben den standardmäßigen Telemac2d-Lenkungs-, Begrenzungs- und Geometrie-Mesh-Dateien erfordert die Kopplung der Hydrodynamik mit Gaia eine neue Steuerungsdatei (`*.cas`) die in der Hauptlenkungsdatei der Simulation referiert werden muss. Zu diesem Zweck erstellen Sie ** einen neuen Ordner für das Gaia Tutorial** (z.B. `/gaia2d-tutorial/`), kopieren Sie die {ref}`dry-initialized steady2d simulation and results files <tm2d-init-dry>` (oder klonen Sie das [gaia2d-tutorial repository](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/)) und ** erstellen Sie eine neue Gaia-Lenkdatei** (z.B. `gaia-morphodynamics.cas`). So sollten die folgenden Dateien im Modellierungsordner für dieses Tutorial leben:

* Das Rechennetz in Form von [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* Die Randdefinitionen in Form von [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* Die Ergebnisse des trocken-initialisierten stationären 2d-Modells laufen für 35 m$^3$/s in Form von [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) ({ref}`dry steady run <tm2d-init-dry>` ending at`T=15000`).
* Eine Telemac2d-Lenkungsdatei für dieses Tutorial, die auf der trocken-initialisierten stationären 2d-Lenkdatei aufgebaut und [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* Die neue [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas)lenkdatei.

```{admonition} Gaia simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/).
```

### Paar Gaia in der Hydrodynamik Lenkungsdatei

Um die Kopplung von Gaia mit einer Telemac2d/Telemac3d-Simulation programmatisch umzusetzen, müssen zusätzlich zu den in der {ref}`steady2d chapter <telemac2d-steady>` erläuterten Keywords ein paar neue Keywords definiert werden. Das erste zusätzliche Keyword ist die Basis für jede Kopplung mit Telemac2d oder Telemac3d Lenkdatei:

```fortran
/ steady2d-gaia.cas
COUPLING WITH : 'GAIA'
```

```{admonition} steady2d-gaia.cas is the hydrodynamics (Telemac2d or Telemac3d) steering file
:class: note
In diesem Tutorial wird die Hydrodynamik (Telemac2d oder Telemac3d) Lenkdatei als [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas) und die Morphodynamik (Gaia) Lenkdatei bezeichnet als [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).
```

Darüber hinaus verlinkt das **GAIA STEERING FILE** Keyword die oben erstellte `gaia-morphodynamics.cas` in der hydrodynamischen Steuerungsdatei Telemac2d (oder Telemac3d):

```fortran
/ steady2d-gaia.cas
/ ...
GAIA STEERING FILE : gaia-morphodynamics.cas
```


(gaia-hotstart)=
### Hotstart

Dieses Tutorial baut auf den Ergebnissen der {ref}`dry-initialized steady2d model <tm2d-init-dry>`, da Gaia-Simulationen typischerweise ein gut entwickeltes Flussfeld als Anfangsbedingung benötigen (siehe {ref}`above definitions <tm-coupling>`). Die Verwendung eines früheren Simulationsergebnisses zur Modell initialisation wird **hotstart** genannt, was eine Ergebnisdatei aus einer vorherigen Simulation erfordert. Zu diesem Zweck stellen Sie sicher, dass die trocken-initialisierte stetig2d-Ergebnisse-Datei im Simulationsordner ist ([download r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf)). Dann **definieren Sie den Hotstart in der Telemac2d-Lenkdatei** mit den folgenden Keywords:


```fortran
/ steady2d-gaia.cas
/ ...
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
```

```{admonition} COMPUTATION CONTINUED is obsolete in TELEMAC v9.0
:class: warning
Seit TELEMAC v9.0 ist das Stichwort `COMPUTATION CONTINUED` **deleted**. Der Fortsetzungsschritt wird nun ** automatisch aktiviert**, wenn `PREVIOUS COMPUTATION FILE` in der Lenkdatei angegeben ist. Einfach die vorherige Rechendatei bereitstellen löst das Hotstart-Verhalten aus.
```

Das **INITIAL TIME SET TO ZERO** Keyword setzt die Simulationszeit auf `0`. Als nächstes stellen Sie sicher, dass alle **INITIAL CONDITIONS** Keywords mit einem **/** kommentiert werden (alternativ löschen Sie diese Zeilen von stationären2d-gaia.cas):

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
Die untere Höhe muss in der Ergebnisdatei der für den Hotstart verwendeten Simulation ausgedruckt werden. Zu diesem Zweck stellen Sie sicher, dass die Liste der Werte für das **VARIABLES FOR GRAPHIC PRINTOUTS* Schlüsselwort `B` enthält, wie in der {ref}`explanations for the setup of the dry-initialized model <tm2d-init-dry>` angegeben.
```

```{admonition} Continuing a Gaia computation (sedimentological hotstart)
:class: tip
Um eine Gaia-Simulation aus einer früheren sedimentologischen Berechnung fortzusetzen (d.h. um mit vorhandenen Bettzusammensetzung und Schichtdaten neu zu starten), verwenden Sie das **PREVIOUS SEDIMENTOLOGICAL COMPUTATION FILE** Keyword in der Gaia-Lenkungsdatei. Seit v9.0 aktiviert die Angabe dieser Datei automatisch die Fortsetzung ohne weiteres Keyword. Die frühere Datei sollte die untere Höhe (`B`), die Schichtdicken (`*ES`) und idealerweise die Sedimentmassen (`*S*` oder `*M*`) oder die Verhältnisse (`*A*`, `*R*`) zur ordnungsgemäßen Weiterführung enthalten.
```

Die trocken-initialisierte Lenkdatei verschreibt Fliessraten und Erhebungen, die **Modifikationen in stationär2d-gaia.cas***** nur auf ** verschreibt. Der Grund für die Q-only-Verschreibung ist, dass wir mit Gaia modellbedingte Veränderungen in Wassertiefen und Flussbett-Höhe wollen, was bedeutet, dass die Wasseroberflächen-Höhe nicht als Randbedingung eingeschränkt werden darf (d.h. nicht vorgeschrieben). So erfordert die Einrichtung von Randbedingungen für Gaia auch leichte Änderungen der (`*.cli`) Datei(en), die im nächsten Abschnitt auf der {ref}`Basic Setup of Gaia <gaia-bc>` erläutert werden. Zu diesem Zweck stellen Sie sicher, dass in der Hydrodynamik-Lenkdatei ** nur das fließfähige verschreibungspflichtige Keyword aktiviert* und die Höhenverschreibung deaktiviert wird (mit `/`):

```fortran
/ steady2d-gaia.cas
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 374.805626;371.33
```

### Kontrollabschnitte

Steuerungsabschnitte sind Sequenzen von Knotennummern (oder Knotenkoordinaten), an denen TELEMAC Flußmittel z.B. zur Überprüfung von Zu- und Abflussmassenbilanzen zusammensetzt. Der unruhige Simulationsabschnitt enthält detaillierte Anweisungen für {ref}`defining control sections <tm-control-sections>` und dieses Tutorial verwendet die Datei Control-Abschnitte aus der unruhigen Simulation (**[download control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/control-sections.txt)**).

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

Um die Steuerabschnitte für die Gaia-Simulation zu verwenden, fügen Sie folgendes zur **Hydrodynamik**-Lenkdatei hinzu:

```
/ steady2d-gaia.cas
/ ...
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
```

So wird das Nachlaufen der Simulation die Flussmittel über die beiden definierten Steuerabschnitte in eine Datei namens *r-control-flows.txt* schreiben.

### Hydrodynamische Lenkung Zusammenfassung

Mit den obigen Anpassungen und mit einer Simulationslänge von `30000`Zeitschritten (um die morphodynamische Evolution zu beobachten) mit einer grafischen Ausdruckzeit jeder `5000`Zeitschritte (um die Ausgabedateigröße zu reduzieren) sollte die endgültige hydrodynamische Lenkdatei so aussehen:

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