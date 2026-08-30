---
description: Konfigurieren Sie den Transport suspendierter Sedimente in TELEMAC-GAIA unter Verwendung von Advektions-Diffusionsgleichungen, Tracerkonzentrationen und Erosions-Ablagerungs-Flussschlüssen für die Feinpartikelmodellierung.
---

(gaia-sl)=
# Schwebstofffracht

{term}`Schwebstoff <Suspended load>` refers to fine particle ($\lesssim$ 1-2 mm) displacement in the water column, where particles are maintained in temporary suspension by the action of upward-moving turbulent eddies. The TELEMAC software suite uses the hydrodynamic Telemac2d/3d models to simulate {term}`Schwebstoff <Suspended load>` by solving the {term}`Advektion <Advection>`-{term}`Diffusion` equations with tracer concentrations. This is why suspended load modeling requires an open boundary `LICBOR` type for tracers (e.g., `4` or `5`) as described in the {ref}`setup of the boundaries-gaia.cli <gaia-bc>` file.

Um die Simulation der Schwebstofffracht zu aktivieren, fügen Sie der Gaia-Lenkdatei Folgendes hinzu:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ SUSPENDED LOAD
SUSPENSION FOR ALL SANDS : YES
```

(gaia-sl-theory)=
## Theoretische Hintergründe

Die herrschende Gleichung für den Transport suspendierter Sedimente ist die Advektions-Diffusions-Gleichung (ADE), die die Massenkonservierung suspendierter Sedimente in der Wassersäule beschreibt:

$$
\frac{\partial (hC)}{\partial t} + \frac{\partial (hUC)}{\partial x} + \frac{\partial (hVC)}{\partial y} = \frac{\partial}{\partial x}\left(\varepsilon_s h \frac{\partial C}{\partial x}\right) + \frac{\partial}{\partial y}\left(\varepsilon_s h \frac{\partial C}{\partial y}\right) + E - D
$$ (eq-ade-2d)

Dabei ist $C$ die tiefgemittelte suspendierte Sedimentkonzentration (Gaia drückt sie in g/l aus, numerisch gleich kg m$^{-3}$), $h$ ist Wassertiefe (m), $U$ und $V$ sind tiefgemittelte Geschwindigkeitskomponenten (m s$^{-1}$), $\varepsilon_s$ ist der Sedimentdiffusionskoeffizient (m$^2$s$^{-1}$), $E$ ist der Erosionsfluss aus dem Bett (kg m$^{-2}$s$^{-1}$) und $D$ ist der Ablagerungsfluss zum Bett (kg m$^{-2}$s$^{-1}$).

```{admonition} 2D vs. 3D suspended load modeling
:class: note
In 2d (Telemac2d-Gaia coupling), the advection-diffusion equation is depth-integrated and solved for depth-averaged concentrations. Near-bed concentrations are derived from equilibrium formulae. In 3d (Telemac3d-Gaia coupling), the full 3d advection-diffusion equation is solved, allowing for vertical concentration profiles (e.g., the {cite:t}`rouse_analysis_1939` profile). The 3d approach is recommended when vertical stratification of sediment is important, such as in deep estuaries or reservoirs. Read more about 3d suspended load in section 2.2 of the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

The sediment diffusivity $\varepsilon_s$ is related to the turbulent eddy viscosity $\nu_t$ by:

$$
\varepsilon_s = \frac{\nu_t}{\sigma_s}
$$ (eq-diff-sed)

wobei $\sigma_s$ die Schmidt-Zahl ist, die Gaia an $\sigma_s = 1.0$ fixiert (d.h. die Sedimentdiffusivität entspricht der turbulenten Wirbelviskosität). Eine zusätzliche konstante Diffusivität kann mit dem Schlüsselwort **COEFFICIENT FOR DIFFUSION OF SUSPENDED SEDIMENTS** eingestellt werden (real, standardmäßig `1.E-6` m$^2$s$^{-1}$).

(gaia-sl-sed)=
## Zusätzliche Sedimentparameter

Feine Sedimentmischungen mit sehr feinen zusammenhängenden Partikeln (weniger als 0,06-0,1 mm) werden in Gaia als **mud** bezeichnet, ebenso wie die Schlüsselwörter in den folgenden Absätzen. Die Unterscheidung zwischen nicht zusammenhängendem Sand und zusammenhängendem Schlamm ist wichtig, da sich ihr Erosions- und Ablagerungsverhalten grundlegend unterscheidet. Weitere Informationen zu schlammbezogenen Keywords finden Sie in Abschnitt 4.2 im [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)].

### Ablagerungsparameter

Für Schwebstofffracht ist die Definition zusätzlicher Sedimenteigenschaften für jede Sedimentklasse erforderlich (oder aktiviert).

Particle settling velocities $w_{s}$ can be defined with the **CLASSES SETTLING VELOCITIES** keyword to calculate the deposition flux $D$. The classical {cite:t}`krone1962` deposition formula is:

$$
D = w_{s} \cdot C \cdot \left(1 - \frac{\tau}{\tau_{cd}} \right) \quad \text{if } \tau < \tau_{cd}
$$ (eq-gaia-dep)

where $C$ is the suspended sediment concentration (g/l), $\tau$ is the bed shear stress (N m$^{-2}$), and $\tau_{cd}$ is the critical shear stress for deposition (N m$^{-2}$). If $\tau \geq \tau_{cd}$, no deposition occurs because turbulence is too strong to allow particles to settle.

```{admonition} Critical shear stress vs. critical shear velocity
:class: note
The keyword **CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION** is supplied as a **shear stress in N m$^{-2}$** (default `1000.`). Internally, Gaia converts it to a **critical shear velocity** $u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$ for the deposition formula. The large default of `1000` N m$^{-2}$ effectively disables the shear-stress limitation (i.e., deposition always occurs if $w_s > 0$), which is appropriate for non-cohesive sediments.
```

Wenn das Schlüsselwort **CLASSES SETTLING VELOCITIES** weggelassen wird (oder auf `-9` gesetzt wird), berechnet Gaia intern $w_s$ für jede Sedimentklasse und wählt eine von drei korngrößenabhängigen Formeln aus:

* Für sehr feine Partikel ($D_{50} < 10^{-4}$m) gilt {cite:t}`stokes1850` Gesetz:

$$
w_{s} = \frac{(s-1) \cdot g \cdot D_{50}^2}{18 \nu}
$$ (eq-ws-stokes)

* Für Zwischengrößen ($10^{-4} \leq D_{50} < 10^{-3}$m) wird die Rubey--{cite:t}`zanke1977`-Formel verwendet:

$$
w_{s} = \frac{10\nu}{D_{50}}\left(\sqrt{1 + \frac{(s-1) \cdot g \cdot D_{50}^3}{100\nu^2}} - 1\right)
$$ (eq-ws-zanke)

* Für grobe Partikel ($D_{50} \geq 10^{-3}$m) wird eine konstante Luftwiderstandskoeffizientenbeziehung verwendet:

$$
w_{s} = 1.1\sqrt{(s-1) \cdot g \cdot D_{50}}
$$ (eq-ws-coarse)

Dabei ist $s$ die relative Dichte des Sediments (normalerweise 2,65), $g$ ist die Gravitationsbeschleunigung, $D_{50}$ ist der Korndurchmesser und $\nu$ ist die kinematische Viskosität von Wasser ($\approx$10$^{-6}$m$^{2}$s$^{-1}$). Die drei Regime wechseln von einem viskosen ($Re_p \ll 1$, Stokes) zu einem völlig turbulenten ($Re_p \gg 1$, konstanter Widerstand) Absetzverhalten {cite:p}`dey_fluvial_2014`.


Um die integrierten Routinen von Gaia für die Berechnung von $w_{s}$ zu nutzen, verwenden Sie entweder nicht das Schlüsselwort CLASSES SETTLING VELOCITIES in der Gaia-Lenkdatei oder setzen Sie die Werte pro Klasse auf `-9` (was eine automatische Berechnung auslöst). Detaillierte Informationen zur Berechnung der Absetzgeschwindigkeiten für Einzelfälle (z. B. Berechnung der Schwebstofffracht für anderes Schwebstoffe als Mineralsediment) finden Sie beispielsweise unter {cite:t}`dey_fluvial_2014` (Buchabschnitt 1.7). Gaias Absetzgeschwindigkeitsalgorithmus befindet sich in der Datei `settling_vel.f` im `/telemac/sources/gaia/`-Verzeichnis.

Die kritische Scherspannung $\tau_{cd}$ für die Schlammablagerung kann mit dem Schlüsselwort **CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION** definiert werden (Standard ist `1000.`N m$^{-2}$, was die Ablagerungsschwelle effektiv deaktiviert; Gaia konvertiert sie intern in die kritische Schergeschwindigkeit $u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
CLASSES SETTLING VELOCITIES : -9;-9;-9
CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION : 1000;1000;1000 / N per m2
```

```{admonition} Hindered settling for high concentrations
:class: tip
Bei hohen Konzentrationen suspendierter Sedimente (normalerweise > 10 g/l) verringern die Partikel-Partikel-Wechselwirkungen die effektive Absetzgeschwindigkeit. Dieses Phänomen, bekannt als *hindered settlement*, kann in Gaia mit dem Schlüsselwort **HINDERED SETTLING** auf `YES` (Standard ist `NO`) aktiviert werden. Die Formulierung der behinderten Siedlung folgt {cite:t}`richardson1954sedimentation`:

$$
w_{s,h} = w_s \cdot (1 - \phi)^n
$$

where $\phi$ is the volumetric sediment concentration and $n$ is an empirical exponent (typically 4.65 for fine sediments). This is particularly important for simulating hyperconcentrated flows or reservoir sedimentation.
```

### Erosionsparameter

For **cohesive (mud)** sediments, Gaia calculates erosion fluxes $E$ using the {cite:t}`partheniades1965` formula, which is the classical approach for cohesive sediments:

$$
E = \begin{cases} M\cdot \left(\frac{\tau}{\tau_{ce}} - 1\right) & \mbox{ if } \tau > \tau_{ce} \\ 0 & \mbox{ if } \tau \leq \tau_{ce}\end{cases}
$$ (eq-gaia-erosion)

Dabei bezeichnet $M$ die Erosionskonstante {cite:t}`krone1962`--{cite:t}`partheniades1965` (in kg m$^{-2}$s@s$^{-1}$), die in Gaia mit dem Schlüsselwort **LAYERS PARTHENIADES CONSTANT** definiert werden kann (Standardwert: `1.E-03`). Darüber hinaus kann $\tau_{ce}$ (kritische Scherspannung für Erosion) mit dem Schlüsselwort **LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD** (Standard ist `0.01;0.02;0.03;...` für aufeinanderfolgende Schichten) in N m$^{-2}$ definiert werden.

```{admonition} Non-cohesive sand uses an equilibrium-concentration closure
:class: note
The Partheniades formula above applies to **cohesive mud**. For **non-cohesive sand** (the case used in this tutorial), Gaia does not use the Partheniades constant. Instead, the net bed exchange flux is computed from the equilibrium near-bed concentration $C_{eq}$ obtained from the chosen {ref}`suspension formula <gaia-sl-formulae>` following the {cite:t}`celik1988` approach: $E - D = w_s \, (C_{eq} - C_{z_{ref}})$, where $C_{z_{ref}}$ is the actual near-bed concentration derived from the depth-averaged concentration assuming a {cite:t}`rouse_analysis_1939` profile. Erosion ($E = w_s C_{eq}$) dominates when the bed is under-saturated, and deposition ($D = w_s C_{z_{ref}}$) dominates when it is over-saturated.
```

```{admonition} Erosion vs. deposition thresholds
:class: note
The onset (initialization) energy for erosion is higher than for deposition because particles must overcome inter-particle forces and be lifted from the bed. Consequently, the critical shear stress for erosion ($\tau_{ce}$) is typically larger than the critical shear stress for deposition ($\tau_{cd}$). For non-cohesive sediments, the erosion threshold is often expressed in terms of the {term}`Shields parameter` rather than the Partheniades formulation.
```

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
LAYERS PARTHENIADES CONSTANT : 1.E-03 / in kg per m2 per s
/ LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD : 0.01;0.1;0.1 / in N per m2
```

```{admonition} Sand-mud mixtures
:class: tip
Für gemischte Sedimente, die sowohl Sand- als auch Schlammfraktionen enthalten, wendet Gaia je nach Schlammgehalt in der aktiven Schicht unterschiedliche Erosionsformulierungen an:

* ** Schlammgehalt < 30 %**: Nicht-kohäsives Verhalten dominiert; Erosion folgt dem Gleichgewichtskonzentrationsansatz für Sande.
* **Schlammgehalt 30-50%**: Übergangsregime; lineare Interpolation zwischen nicht-kohäsiven und kohäsiven Formulierungen.
* **Mud content > 50%**: Cohesive behavior dominates; erosion follows the {cite:t}`partheniades1965` formulation.

Dieses Verhalten ist in Gaia automatisch, wenn mehrere Sedimentklassen mit unterschiedlichen Korngrößen definiert werden. Lesen Sie mehr über Sand-Schlamm-Mischungen in Abschnitt 4 des [Gaia Manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)].
```

(gaia-sl-formulae)=
## Schwebstoff Formeln

The sediment transport formulae for suspended load modeling can be defined with the **SUSPENSION TRANSPORT FORMULA FOR ALL SANDS** keyword, which accepts an integer number defining a formula for calculating the equilibrium near-bed concentration $C_{eq}$ in **g/l** (the unit Gaia uses internally for all suspended sediment concentrations). The equilibrium concentration represents the sediment concentration at a reference level near the bed under equilibrium conditions (i.e., when erosion equals deposition). The calculated $C_{eq}$ values align with the later {ref}`definition of initial and boundary conditions <gaia-ic-sl>` for suspended load.

The following integer numbers can be used for calculating $C_{eq}$ with the SUSPENSION TRANSPORT FORMULA FOR ALL SANDS keyword:

* `1` für die {cite:t}`zyserman1994` Formel (**standardmäßig** und **in diesem Tutorial** verwendet):
  - Empirische Formel basierend auf experimentellen Daten von {cite:t}`guy1966summary`
  - Verwendet eine Hautreibungskorrektur (vgl. {ref}`bedload corrections <c-friction>`) für die {term}`Shields parameter`
  - Gilt für nicht kohäsive Sedimente in fluvialen Umgebungen
  - Referenz (in der Nähe des Bettes) Höhe $z_{ref} = \alpha_{k_s} \cdot D_{50}$ (Standard $3.0 \cdot D_{50}$, modifizierbar mit **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER **)
  - Definiert in `/telemac/sources/gaia/suspension_fredsoe.f`
  - Formel: $C_{eq} = \frac{0.331 \cdot (\theta' - \theta_{cr})^{1.75}}{1 + 0.72 \cdot (\theta' - \theta_{cr})^{1.75}}$, wobei $\theta' = \mu\theta$ der Parameter Hautreibung Shields und $\theta_{cr}$ der kritische Parameter Shields ist

* `2` für die {cite:t}`bijker1992` Formel:
  - Berechnet die Schwebstoffkonzentration als Funktion der Geschiebefracht und einer Bezugshöhe der Hautreibung
  - Erfordert, dass {ref}`bedload calculation <gaia-bl>` aktiviert ist (`BED LOAD FOR ALL SANDS : YES`)
  - Geeignet für kombinierte Geschiebe-Schwebstoff Berechnungen
  - Referenzhöhe $z_{ref} = k_{sr}$ (die Rauheit der gewellten Betten)
  - Definiert in `/telemac/sources/gaia/suspension_bijker.f`

* `3` für die {cite:t}`van_rijn_suspension_1984` Formel:
  - Gegenstück von {ref}`van Rijn bedload formula <gaia-rijn>`
  - Verwendet eine Hautreibungskorrektur (vgl. {ref}`bedload corrections <c-friction>`) für die {term}`Shields parameter`
  - Referenzhöhe $z_{ref} = 0.5 \cdot k_s$, wobei $k_s$ die Gesamtrauigkeit ist (aus der hydrodynamischen Lenkungsdatei)
  - Ursprünglich für den Sandtransport in Flüssen und Mündungen entwickelt
  - Definiert in `/telemac/sources/gaia/suspension_vanrijn.f`

* `4` für die Formel {cite:t}`soulsby1997`-@-{cite:t}`rijn2007`:
  - Verwendet Orbitalgeschwindigkeit von Wellen (dh vorgeschlagene Anwendung: Küsten- / Meeresregionen)
  - Kombiniert Strom- und Welleneffekte auf Sedimentsuspension
  - Lesen Sie mehr über Schwebstofffracht und Wellen in Abschnitt 5.1 des [Gaia Manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)]
  - Definiert in `/telemac/sources/gaia/suspension_sandflow.f`

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SUSPENSION TRANSPORT FORMULA FOR ALL SANDS : 1
```

```{admonition} User-defined suspension formulae
:class: tip
Benutzer können benutzerdefinierte Suspensionstransportformeln implementieren, indem sie die Fortran-Quelldateien ändern. Die Prozedur folgt dem gleichen Ansatz wie bei {ref}`user-defined bedload formulae <gaia-bl>`: Kopieren Sie die entsprechende Quelldatei in ein `user_fortran/`-Verzeichnis und verweisen Sie sie in der Steuerungsdatei mit `FORTRAN FILE : 'user_fortran'`. Das [Gaia Manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)] bietet detaillierte Anleitungen in Abschnitt 6.3.
```

(gaia-ic-sl)=
## Anfangs- und Grenzbedingungen

Gaia enables a class-wise definition of initial concentrations for suspended load following the order of {ref}`sediment class definitions <gaia-sed>`. The following list definition sets the initial concentration for the 0.5-mm sediment class ({ref}`recall its definition <gaia-sed>`) to 0.6 **g/l** and 0.0 g/l for the 0.02-m and 0.1-m sediment size classes. The definition of initial suspended sediment concentrations can be overridden in 2d at boundary nodes by setting the **EQUILIBRIUM INFLOW CONCENTRATION** keyword to `YES` (requires that the {ref}`tracer boundary <gaia-bc>` is set to `5`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0.
```

```{admonition} Concentration units in Gaia
:class: warning
Gaia erwartet **all ** suspendierte Sedimentkonzentrationen in **g/l ** (Gramm Trockensediment pro Liter), einschließlich der **INIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES **, **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES ** und der `CBOR` Spalte der Grenzdatei. Die Massenkonzentration in g/l ist numerisch identisch mit kg/m3:
* 1 g/l = 1 kg/m3
* 1 mg/l = 0,001 g/l = 0,001 kg/m3

So the example above sets `0.6` g/l = 0.6 kg/m³ = 600 mg/l for the first sediment class. If you need volume concentration $C_v$ instead, convert in post-processing with $C_v = C_m / \rho_s$, where $C_m$ is the mass concentration (g/l) and $\rho_s$ is the sediment density (kg/m³).
```

Lesen Sie mehr über die Definition der Anfangsbedingungen in Abschnitt 2.1.1 im [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)].

(gaia-bc-sl)=
## Grenzverschreibungen

The per-sediment class suspended load concentrations can be prescribed similar to the initial concentrations with the **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES** keyword. Alternatively, the **EQUILIBRIUM INFLOW CONCENTRATION** keyword may be used to automatically compute the inflow concentration based on the equilibrium formula (option `1`-`4` defined above). **None of these keywords is used in this tutorial** because the model starts with a defined initial concentration and allows the system to evolve.

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0. / g/l
/ EQUILIBRIUM INFLOW CONCENTRATION : YES / not used in this tutorial
```

```{admonition} Treatment of boundary fluxes
:class: tip
Das Schlüsselwort **BEHANDLUNG DER FLUXE AN DEN BOUNDARIES** steuert, wie vorgeschriebene Konzentrationen an offenen Grenzen gehandhabt werden:

* `1` (**default**): Vorrang vor vorgegebenem Wert im Diffusionsschritt. Dies kann künstliche Flüsse an Grenzen erzeugen.
* `2`: Priorität beim vorgeschriebenen Flux. Der tatsächliche Sedimentfluss entspricht dem Wasseraustrag multipliziert mit der vorgeschriebenen Konzentration. Diese Option wird für massenkonservative Simulationen mit distributiven Advektionsschemata empfohlen (`3`, `4`, `5`, `13`, `14`).

Verwenden Sie für kritische Massenbilanzanwendungen die Option `2` zusammen mit dem Werbeschema `14` oder `15`.
```

Gaia can be run with liquid boundary files for assigning time-dependent suspended load fluxes (the outflow should be kept in equilibrium). Solid flux time series can be implemented using the already applied `455`-`5` upstream boundary type, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. More information about suspended load boundary conditions can be found in section 2.1.2 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).


## Numerische Parameter

Die meisten numerischen Parameter für die Modellierung der Schwebstofffracht hängen von den hydrodynamischen Telemac2d/3d-Lenkdateidefinitionen ab. Zusätzliche Schlüsselwörter, die sich direkt auf die Simulation der Schwebstofffracht auswirken, sollten in der Gaia-Lenkdatei deklariert werden.

For instance, the **SCHEME FOR ADVECTION ...** keywords for velocities, tracers, and turbulence modeling are defined with the hydrodynamics (Telemac2d/3d) steering file's {ref}`general numerical parameters for finite elements <tm2d-fe>`. In addition, the advection scheme for suspended load can be defined in the Gaia steering file with the **SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS** keyword that accepts one of the following integer keywords (for 2d only):

* `1` für das bedingungslos stabile, nicht-konservative, aber diffusive (für kleine Zeitschritte) *Method of Characteristics * Schema.
* `2` für das nicht-konservative *Streamline Upwind Petrov Galerkin* (SUPG) Schema, das die {term}`CFL-Zahl <CFL>` Bedingung verwendet und weniger diffusiv ist als das *Characteristics* (`1`) Schema.
* `3` or `4` for the conservative *N-scheme* (distributive) with timestep reduction based on the {term}`CFL-Zahl <CFL>` condition. Option `4` includes mass-lumping for improved stability. These options should **not** be used in the presence of tidal flats (use `13` or `14` instead).
* `5` für das massenkonservative *PSI-Verteilungsschema* (**Standard**), das Flüsse nach Tracer-Konzentrationen korrigiert und weniger diffusiv ist als `4` oder `14`. Die Rechenzeit mit `5` ist länger als mit `4` oder `14`. Diese Option sollte **nicht** in Anwesenheit von Gezeitenwohnungen verwendet werden.
* `13` und `14` für das *Edge-basierte N-Schema* (NERD), das `3` und `4` ähnelt, aber an Gezeitenwohnungen angepasst ist. **Option `14` wird in diesem Tutorial** gemäß der Empfehlung im [Gaia-Handbuch](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)] verwendet.
* `15` für das massenkonservative *ERIA-Schema*, das mit Gezeitenflächen funktioniert.

The options `4` and `14` can be defined along with the keyword definition `CORRECTION ON CONVECTION VELOCITY : YES` (logical, default `NO`) that modifies the depth-averaged convection velocity to account for the vertical gradients of velocity and concentration. This setting avoids overestimating suspended load, especially in deep waters, but it is not used in this tutorial.

The **SCHEME OPTION FOR ADVECTION OF SUSPENDED SEDIMENTS** can be additionally defined to either use a **strong (default of `1`)** or a **weak (`2`)** form for advection. A weak form decreases numerical {term}`Diffusion`, is more conservative, and increases computation time (read more in the {ref}`Telemac2d steady section <tm2d-fe>`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14
/ CORRECTION ON CONVECTION VELOCITY : YES / use when SCHEME is 4 or 14 for deep water
```

```{admonition} Diffusion of suspended sediment
:class: tip
Der Diffusionsterm der Advektions-Diffusions-Gleichung wird durch die turbulente Wirbelviskosität des hydrodynamischen Solvers plus eine konstante Hintergrunddiffusivität bestimmt, die in der Gaia-Lenkdatei eingestellt werden kann:

* **COEFFIZIENTER FÜR DIE VERTEILUNG VON ERWEITERTEN SEDIMENTEN** (real, standardmäßig `1.E-6`m$^2$s$^{-1}$): Konstante Diffusivität hinzugefügt in 2d (in 3d-Verwendung **COEFFIZIENTER FÜR DIE HORIZONTALE VERTEILUNG VON ERWEITERTEN SEDIMENTEN** und **COEFFIZIENTER FÜR DIE VERTEILTE VERTEILUNG **).

Für die meisten fluvialen Anwendungen ist der Standardwert ausreichend, da die turbulente Diffusivität über den konstanten Hintergrundterm dominiert.
```

Lesen Sie mehr über die Definition numerischer Parameter in Abschnitt 2.1.5 im [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)].

## Morphologische Kopplung

When suspended load is activated together with bed evolution, the erosion and deposition fluxes contribute to the mass balance of the bed through the {term}`Exner-Gleichung <Exner equation>`. The net flux (erosion minus deposition) modifies the bed elevation at each time step.

```{admonition} Morphological factor for suspended load
:class: tip
Für Langzeitsimulationen, bei denen morphologische Zeitskalen viel länger sind als hydrodynamische Zeitskalen, kann ein **MORPHOLOGISCHER FAKTOR** angewendet werden, um die Entwicklung von Betten zu beschleunigen. Dieser Faktor multipliziert den Nettoerosions-/Ablagerungsfluss und ermöglicht mehrjährige morphologische Simulationen mit angemessenen Berechnungszeiten. Verwenden Sie jedoch mit Vorsicht: Morphologische Faktoren von mehr als 10-20 können unrealistische Ergebnisse liefern. Das Schlüsselwort ist in der Gaia Steering Datei definiert:

```fortran
MORPHOLOGICAL FACTOR : 10. / accelerate bed evolution 10x
```
```

## Beispielanträge

Examples for the implementation of suspended load come along with the TELEMAC installation (in the `/telemac/examples/gaia/` directory). The following examples in the `gaia/` folder feature (pure) suspended load calculations:

* 2d-Modell des kombinierten zusammenhängenden und nicht zusammenhängenden ausgesetzten Transports: **hippodrome-t2d/**
* 2d-Modell zur Erhaltung der zusammenhängenden Schlammmasse: **mud conservation-t2d/**
* 3D-Modell des kombinierten zusammenhängenden und nicht zusammenhängenden ausgesetzten Transports: **hippodrome-t3d/**
* 3D-Modell des nicht zusammenhängenden suspendierten Transports mit Korrektur der Hautreibung: **lyn-t3d/**
* 3D-Modell des zusammenhängenden Schwebstofftransports mit vertikalem Rouse-Profil (vgl. [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf), Abschnitt 2.1.2): **rouse-t3d/**
* 3D-Modell eines Gezeitenflusses mit zusammenhängendem Sediment: **tidal flats-t3d/**
* Kopplung mit Wellen: **sandpit-t2d/**

```{admonition} Recommended workflow for suspended load simulations
:class: note
1. **Beginn mit Hydrodynamik**: Stellen Sie sicher, dass das hydrodynamische Modell (Telemac2d/3d) kalibriert ist und angemessene Strömungsfelder erzeugt, bevor es mit Gaia gekoppelt wird.
2. **Definieren Sie Sedimentklassen**: Für das betreffende Gebiet geeignete Korngrößen angeben. Feine Sedimente ($D < 0.063$mm) sind typischerweise kohäsiv; gröbere Sedimente sind nicht kohäsiv.
3. **Suspensionsformel auswählen**: Wählen Sie basierend auf der Umgebung (fluvial: `1` oder `3`; Küste mit Wellen: `4`).
4. **Erste Bedingungen festlegen**: Gemessene oder geschätzte Konzentrationen suspendierter Sedimente verwenden.
5. **Choose advection scheme**: Use `14` for robustness with tidal flats, or `5` for better accuracy in deep channels.
6. **Calibrate erosion/deposition**: Adjust Partheniades constant $M$, critical shear stresses, and settling velocities to match observed concentrations.
7. **Validate mass balance**: Enable `MASS-BALANCE : YES` in the hydrodynamics steering file to monitor sediment conservation.
```