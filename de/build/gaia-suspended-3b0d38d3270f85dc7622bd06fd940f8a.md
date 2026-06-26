---
description: Konfigurieren Sie den hängenden Sedimenttransport in TELEMAC-GAIA unter Verwendung von Advektions-Diffusionsgleichungen, Tracerkonzentrationen und Erosions-Depositionsflussverschlüssen für die Feinpartikelmodellierung.
---

(gaia-sl)=
# Aufgehängte Last

{term}`Suspended load` bezieht sich auf Feinkorn ($\lesssim$ 1-2 mm) Verschiebung in der Wassersäule, wobei Partikel in temporärer Suspension durch die Wirkung von nach oben bewegten Wirbelkörpern gehalten werden. Die TELEMAC Software-Suite nutzt die hydrodynamischen Telemac2d/3d-Modelle, um {term}`Suspended load` zu simulieren, indem die {term}`Advection`-{term}`Diffusion`-Gleichungen mit Tracer-Konzentrationen gelöst werden. Aus diesem Grund erfordert die suspendierte Lastmodellierung eine offene Grenze `LICBOR` für Tracer (z.B. `4` oder `5`) wie in der Datei {ref}`setup of the boundaries-gaia.cli <gaia-bc>` beschrieben.

Um die Simulation der hängenden Last zu aktivieren, fügen Sie die Gaia-Lenkungsdatei Folgendes hinzu:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ SUSPENDED LOAD
SUSPENSION FOR ALL SANDS : YES
```

(gaia-sl-theory)=
## Theoretische Hintergrund

Die Regelgleichung für den suspendierten Sedimenttransport ist die Advektionsdiffusionsgleichung (ADE), die Massenkonservierung von suspendiertem Sediment in der Wassersäule beschreibt:

$$
\frac{\partial (hC)}{\partial t} + \frac{\partial (hUC)}{\partial x} + \frac{\partial (hVC)}{\partial y} = \frac{\partial}{\partial x}\left(\varepsilon_s h \frac{\partial C}{\partial x}\right) + \frac{\partial}{\partial y}\left(\varepsilon_s h \frac{\partial C}{\partial y}\right) + E - D
$$ (eq-ade-2d)

where $C$ is the depth-averaged suspended sediment concentration (Gaia expresses it in g/l, numerically equal to kg m$^{-3}$), $h$ is water depth (m), $U$ and $V$ are depth-averaged velocity components (m s$^{-1}$), $\varepsilon_s$ is the sediment diffusivity coefficient (m$^2$ s$^{-1}$), $E$ is the erosion flux from the bed (kg m$^{-2}$ s$^{-1}$), and $D$ is the deposition flux to the bed (kg m$^{-2}$ s$^{-1}$).

```{admonition} 2D vs. 3D suspended load modeling
:class: note
In 2d (Telemac2d-Gaia-Kupplung) ist die Advektions-Diffusionsgleichung tief integriert und für tiefgemittelte Konzentrationen gelöst. Nahbettkonzentrationen werden aus Gleichgewichtsformeln abgeleitet. In 3d (Telemac3d-Gaia Kopplung) wird die volle 3d Advektion-Diffusionsgleichung gelöst, die vertikale Konzentrationsprofile ermöglicht (z.B. das {cite:t}`rouse_analysis_1939`-Profil). Der 3d-Ansatz wird empfohlen, wenn eine vertikale Sedimentschicht wichtig ist, wie z.B. in tiefen Mündungen oder Reservoiren. Lesen Sie mehr über 3d Hängelast in Abschnitt 2.2 der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

Die Sedimentdiffusivität $\varepsilon_s$ steht in Verbindung mit der turbulenten Wirbelviskosität $\nu_t$:

$$
\varepsilon_s = \frac{\nu_t}{\sigma_s}
$$ (eq-diff-sed)

where $\sigma_s$ is the Schmidt number, which Gaia fixes to $\sigma_s = 1.0$ (i.e., the sediment diffusivity equals the turbulent eddy viscosity). An additional constant diffusivity can be set with the **COEFFICIENT FOR DIFFUSION OF SUSPENDED SEDIMENTS** keyword (real, default `1.E-6` m$^2$ s$^{-1}$).

(gaia-sl-sed)=
## Zusätzliche Sedimentparameter

Feine Sedimentmischungen mit sehr feinen, kohäsiven Partikeln (weniger als 0,06-0.1 mm) werden in Gaia als **mud** bezeichnet und so die Keywords in den folgenden Absätzen. Die Unterscheidung zwischen nicht-kohäsiven Sand und kohäsivem Schlamm ist wichtig, weil ihre Erosions- und Ablagerungsverhalten sich grundsätzlich unterscheiden. Weitere Informationen zu mudbezogenen Keywords finden Sie in Abschnitt 4.2 in der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

### Depositionsparameter

Für suspendierte Last ist die Definition zusätzlicher Sedimenteigenschaften für jede Sedimentklasse erforderlich (oder aktiviert).

Mit dem **CLASSES SETTLING VELOCITIES** Keyword zur Berechnung des Depositionsflusses $D$ können Partikel-Setting-Vocities $w_{s}$ definiert werden. Die klassische {cite:t}`krone1962`-Depositionsformel ist:

$$
D = w_{s} \cdot C \cdot \left(1 - \frac{\tau}{\tau_{cd}} \right) \quad \text{if } \tau < \tau_{cd}
$$ (eq-gaia-dep)

wobei $C$ die suspendierte Sedimentkonzentration (g/l) ist, $\tau$ ist die Bettscherbeanspruchung (N m$^{-2}$) und $\tau_{cd}$ die kritische Scherbeanspruchung für die Abscheidung ist (N m$^{-2}$). Wenn $\tau \geq \tau_{cd}$, es kommt keine Ablagerung vor, weil Turbulenzen zu stark sind, um Partikel absetzen zu können.

```{admonition} Critical shear stress vs. critical shear velocity
:class: note
Das Schlüsselwort **CLASSES CRITICAL SHEAR STRESS FÜR MUD DEPOSITION** wird als **shear stress in N m$^{-2}$** (default `1000.`) geliefert. Im Innern wandelt Gaia sie in eine **kritische Schergeschwindigkeit**$u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$ für die Abscheideformel um. Der große Standard von `1000` N m$^{-2}$ schaltet die Scherbeanspruchung effektiv ab (d.h. die Ablagerung erfolgt immer, wenn $w_s > 0$), was für nichtkohäsive Sedimente geeignet ist.
```

Wenn das **CLASSES SETTLING VELOCITIES** Keyword entfällt (oder auf `-9` gesetzt), berechnet Gaia $w_s$ für jede Sedimentklasse intern, wobei eine von drei körnigen Formeln ausgewählt wird:

* Für sehr feine Partikel ($D_{50} < 10^{-4}$m), {cite:t}`stokes1850`Gesetz gilt:

$$
w_{s} = \frac{(s-1) \cdot g \cdot D_{50}^2}{18 \nu}
$$ (eq-ws-stokes)

* Für Zwischengrößen ($10^{-4} \leq D_{50} < 10^{-3}$m) wird die Rubey--{cite:t}`zanke1977` Formel verwendet:

$$
w_{s} = \frac{10\nu}{D_{50}}\left(\sqrt{1 + \frac{(s-1) \cdot g \cdot D_{50}^3}{100\nu^2}} - 1\right)
$$ (eq-ws-zanke)

* Bei groben Partikeln ($D_{50} \geq 10^{-3}$m) wird eine konstante Drag-Koeffizienten-Beziehung verwendet:

$$
w_{s} = 1.1\sqrt{(s-1) \cdot g \cdot D_{50}}
$$ (eq-ws-coarse)

wobei $s$ die relative Sedimentdichte (typischerweise 2.65) ist, $g$ Gravitationsbeschleunigung ist,$D_{50}$ ist der Korndurchmesser, und $\nu$ ist die kinematische Viskosität von Wasser ($\approx$10$^{-6}$m$^{2}$s@s$^{-1}$). Die drei Regime wechseln von einer viskosen ($Re_p \ll 1$, Stokes) zu einem voll turbulenten ($Re_p \gg 1$, konstanter Drag) Setzverhalten {cite:p}`dey_fluvial_2014`.


Um Gaias integrierte Routinen für die Berechnung $w_{s}$ zu nutzen, verwenden Sie entweder das CLASSES SETTLING VELOCITIES Keyword in der Gaia-Lenkungsdatei nicht oder setzen Sie seine Per-Class-Werte an `-9` (die die automatische Berechnung auslöst). Detaillierte Informationen zur Berechnung von Absetzgeschwindigkeiten für bestimmte Fälle (z.B. Abgehängte Lastberechnung für sonstiges suspendiertes Material als mineralisches Sediment) finden sich beispielsweise in {cite:t}`dey_fluvial_2014` (Buchse 1.7). Gaias Absetzgeschwindigkeitsalgorithmus befindet sich in der Datei `settling_vel.f` im `/telemac/sources/gaia/`-Verzeichnis.

Die kritische Schubspannung $\tau_{cd}$ für Schlammabscheidung kann mit dem **CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION* Schlüsselwort definiert werden (Standard ist `1000.` N m$^{-2}$, das die Abscheidungsschwelle effektiv deaktiviert; Gaia wandelt sie intern an die kritische Schergeschwindigkeit $u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$ um.

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
CLASSES SETTLING VELOCITIES : -9;-9;-9
CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION : 1000;1000;1000 / N per m2
```

```{admonition} Hindered settling for high concentrations
:class: tip
Bei hohen suspendierten Sedimentkonzentrationen (typischerweise > 10 g/l) reduzieren Partikelpartikel-Interaktionen die effektive Absetzgeschwindigkeit. Dieses Phänomen, das als *hindered settling* bekannt ist, kann in Gaia mit dem **HINDERED SETTLING** Schlüsselwort an `YES` (Standard ist `NO`) aktiviert werden. Die gehinderte Setzformulierung folgt {cite:t}`richardson1954sedimentation`:

$$
w_{s,h} = w_s \cdot (1 - \phi)^n
$$

wobei $\phi$ die volumetrische Sedimentkonzentration ist und $n$ ein empirischer Exponent ist (typischerweise 4.65 für feine Sedimente). Dies ist besonders wichtig für die Simulation hyperkonzentrierter Ströme oder Reservoirsedimentation.
```

### Erosion Parameter

For **cohesive (mud)** sediments, Gaia calculates erosion fluxes $E$ using the {cite:t}`partheniades1965` formula, which is the classical approach for cohesive sediments:

$$
E = \begin{cases} M\cdot \left(\frac{\tau}{\tau_{ce}} - 1\right) & \mbox{ if } \tau > \tau_{ce} \\ 0 & \mbox{ if } \tau \leq \tau_{ce}\end{cases}
$$ (eq-gaia-erosion)

wobei $M$ die Erosionskonstante {cite:t}`krone1962`-{cite:t}`partheniades1965` (in kg m$^{-2}$s$^{-1}$) bezeichnet wird, die in Gaia mit dem Stichwort **LAYERS PARTHENIADES CONSTANT**** definiert werden kann (Standardwert: `1.E-03`). Darüber hinaus kann $\tau_{ce}$ (kritische Scherbelastung für Erosion) mit dem **LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD* Keyword (Standard ist `0.01;0.02;0.03;...` für aufeinanderfolgende Schichten) in N m$^{-2}$ definiert werden.

```{admonition} Non-cohesive sand uses an equilibrium-concentration closure
:class: note
Die obige Partheniades-Formel gilt für **kohäsiver Schlamm**. Für **nicht-kohäsiver Sand** (der in diesem Tutorial verwendete Fall) verwendet Gaia nicht die Partheniades Konstante. Stattdessen wird der Netto-Bett-Wechselfluss aus dem Gleichgewicht der Nah-Bett-Konzentration berechnet $C_{eq}$, das aus der gewählten {ref}`suspension formula <gaia-sl-formulae>` nach dem {cite:t}`celik1988`-Ansatz gewonnen wird: $E - D = w_s \, (C_{eq} - C_{z_{ref}})$, wobei $C_{z_{ref}}$ die tatsächliche Nah-Bett-Konzentration aus der Tiefen-Mittelwert-Konzentration unter Annahme eines {cite:t}`rouse_analysis_1939`-Profils ist. Erosion ($E = w_s C_{eq}$) dominiert, wenn das Bett untersättigt ist, und die Abscheidung ($D = w_s C_{z_{ref}}$) dominiert, wenn es übersättigt ist.
```

```{admonition} Erosion vs. deposition thresholds
:class: note
Die Anstoßenergie für Erosion ist höher als für die Abscheidung, weil Teilchen interteilchenförmige Kräfte überwinden und vom Bett abgehoben werden müssen. Daher ist die kritische Scherbelastung für die Erosion ($\tau_{ce}$) typischerweise größer als die kritische Scherbelastung für die Abscheidung ($\tau_{cd}$). Bei nicht-kohäsiven Sedimenten wird die Erosionsschwelle oft in Bezug auf die {term}`Shields parameter` anstelle der Partheniades-Formulierung ausgedrückt.
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

* **Mud-Gehalt < 30%**: Nicht-kohäsives Verhalten dominiert; Erosion folgt dem Gleichgewicht Konzentrationsansatz für Sande.
* **Mud-Gehalt 30-50%**: Übergangsregelung; lineare Interpolation zwischen nicht-kohäsiven und kohäsiven Formulierungen.
* **Mud Inhalt > 50%**: Kohäsives Verhalten dominiert; Erosion folgt der {cite:t}`partheniades1965` Formulierung.

Dieses Verhalten ist in Gaia automatisch, wenn mehrere Sedimentklassen mit unterschiedlichen Korngrößen definiert sind. Lesen Sie mehr über Sand-Mud-Gemische in Abschnitt 4 der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

(gaia-sl-formulae)=
## Ausgewählte Lastformel

Die Sedimenttransportformeln für die Schwebelastungsmodellierung können mit dem Stichwort **SUSPENSION TRANSPORT FORMULA FOR ALL SANDS** definiert werden, das eine ganzzahlige Zahl akzeptiert, die eine Formel zur Berechnung des Gleichgewichts bei der Nahbettkonzentration $C_{eq}$ in **g/l* (die Einheit Gaia verwendet intern für alle suspendierten Sedimentkonzentrationen). Die Gleichgewichtskonzentration stellt die Sedimentkonzentration in einem Bezugsniveau nahe dem Bett unter Gleichgewichtsbedingungen dar (d.h. wenn Erosion gleich Ablagerung ist). Die berechneten $C_{eq}$-Werte richten sich an die spätere {ref}`definition of initial and boundary conditions <gaia-ic-sl>` für suspendierte Last.

Für die Berechnung von $C_{eq}$ mit dem SUSPENSION TRANSPORT FORMULA FOR ALL SANDS Keyword können folgende Zahlen verwendet werden:

* `1` for the {cite:t}`zyserman1994` formula (**default** and **used in this tutorial**):
  - Empirische Formel basierend auf experimentellen Daten von {cite:t}`guy1966summary`
  - Verwendet eine Hautreibungskorrektur (vgl. {ref}`bedload corrections <c-friction>`) für die {term}`Shields parameter`
  - geeignet für nichtkohäsive Sedimente in fluvialen Umgebungen
  - Referenz (near-bed) Erhebung $z_{ref} = \alpha_{k_s} \cdot D_{50}$ (Standard$3.0 \cdot D_{50}$, änderbar mit **RATIO BETWEEN SKIN FRICTION UND MEAN DIAMETER*)
  - Definiert unter `/telemac/sources/gaia/suspension_fredsoe.f`
  - Formel: $C_{eq} = \frac{0.331 \cdot (\theta' - \theta_{cr})^{1.75}}{1 + 0.72 \cdot (\theta' - \theta_{cr})^{1.75}}$ wobei $\theta' = \mu\theta$ der Parameter Skin-Friction Shields ist und $\theta_{cr}$ der kritische Parameter Shields ist

* `2` für die Formel {cite:t}`bijker1992`
  - Berechnet die suspendierte Lastkonzentration in Abhängigkeit von der Beladung und einer Referenzhautreibungserhöhung
  - Erfordert die Aktivierung von {ref}`bedload calculation <gaia-bl>` (`BED LOAD FOR ALL SANDS : YES`)
  - Geeignet für kombinierte Last-suspendierte Lastberechnungen
  - Referenzhöhe $z_{ref} = k_{sr}$ (die raue Bettrauhigkeit)
  - Definiert unter `/telemac/sources/gaia/suspension_bijker.f`

* `3` für die Formel {cite:t}`van_rijn_suspension_1984`
  - Counterpart des {ref}`van Rijn bedload formula <gaia-rijn>`
  - Verwendet eine Hautreibungskorrektur (vgl. {ref}`bedload corrections <c-friction>`) für die {term}`Shields parameter`
  - Referenzhöhe $z_{ref} = 0.5 \cdot k_s$, wobei $k_s$ die Gesamtrauhigkeit ist (aus der hydrodynamischen Lenkdatei)
  - Ursprünglich für den Sandtransport in Flüssen und Mündungen entwickelt
  - Definiert unter `/telemac/sources/gaia/suspension_vanrijn.f`

* `4` für die Formel {cite:t}`soulsby1997`-{cite:t}`rijn2007`
  - Verwendet die Umlaufgeschwindigkeit von Wellen (d.h. vorgeschlagene Anwendung: Küsten/Marine-Regionen)
  - Kombiniert Strom- und Welleneffekte auf Sedimentsuspension
  - Lesen Sie mehr über Schwebelastung und Wellen in Abschnitt 5.1 der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)
  - Definiert unter `/telemac/sources/gaia/suspension_sandflow.f`

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SUSPENSION TRANSPORT FORMULA FOR ALL SANDS : 1
```

```{admonition} User-defined suspension formulae
:class: tip
Benutzer können benutzerdefinierte Suspension Transport Formeln implementieren, indem die Fortran Quelldateien ändern. Das Verfahren folgt dem gleichen Ansatz wie bei {ref}`user-defined bedload formulae <gaia-bl>`: Kopieren Sie die entsprechende Quelldatei in ein `user_fortran/`-Verzeichnis und verweisen Sie sie in der Lenkdatei mit `FORTRAN FILE : 'user_fortran'`. Die [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) bietet detaillierte Anleitungen in Abschnitt 6.3.
```

(gaia-ic-sl)=
## Ursprüngliche und verbindliche Bedingungen

Gaia ermöglicht eine klassenweise Definition von Anfangskonzentrationen für suspendierte Last nach der Bestellung von {ref}`sediment class definitions <gaia-sed>`. Die folgende Listendefinition legt die Anfangskonzentration für die Sedimentklasse 0,5 mm ({ref}`recall its definition <gaia-sed>`) auf 0,6 **g/l* und 0,0 g/l für die Sedimentgrößenklassen 0,02-m und 0,1 m fest. Die Definition der anfänglich suspendierten Sedimentkonzentrationen kann in 2d an Grenzknoten übergeordnet werden, indem das **EQUILIBRIUM INFLOW CONCENTRATION** Keyword an `YES` gesetzt wird (erfordert, dass die {ref}`tracer boundary <gaia-bc>` auf `5` gesetzt wird).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0.
```

```{admonition} Concentration units in Gaia
:class: warning
Gaia erwartet ** alle** suspendierten Sedimentkonzentrationen in **g/l** (Grams trockenem Sediment pro Liter), einschließlich der **INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES**, **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES* und der `CBOR` Spalte der Grenzdatei. Die Massenkonzentration in g/l ist mit kg/m3 numerisch identisch:
* 1 g/l = 1 kg/m3
* 1 mg/l = 0,001 g/l = 0,001 kg/m3

So setzt das obige Beispiel für die erste Sedimentklasse `0.6`g/l = 0,6 kg/m3 = 600 mg/l. Wenn Sie stattdessen Volumenkonzentration $C_v$ benötigen, konvertieren Sie die Nachverarbeitung mit $C_v = C_m / \rho_s$, wobei $C_m$ die Massenkonzentration (g/l) und $\rho_s$ die Sedimentdichte (kg/m3) ist.
```

Lesen Sie mehr über die Definition der Ausgangsbedingungen in Abschnitt 2.1.1 in der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

(gaia-bc-sl)=
## Verschreibungen

The per-sediment class suspended load concentrations can be prescribed similar to the initial concentrations with the **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES** keyword. Alternatively, the **EQUILIBRIUM INFLOW CONCENTRATION** keyword may be used to automatically compute the inflow concentration based on the equilibrium formula (option `1`-`4` defined above). **None of these keywords is used in this tutorial** because the model starts with a defined initial concentration and allows the system to evolve.

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0. / g/l
/ EQUILIBRIUM INFLOW CONCENTRATION : YES / not used in this tutorial
```

```{admonition} Treatment of boundary fluxes
:class: tip
Das Schlüsselwort **TREATMENT OF FLUXES AT THE BOUNDARIES** steuert, wie vorgegebene Konzentrationen an offenen Grenzen gehandhabt werden:

* `1` (**default**): Priority to prescribed value in the diffusion step. This may create artificial fluxes at boundaries.
* `2`: Priorität des vorgeschriebenen Flusses. Der tatsächliche Sedimentfluss entspricht der Wasserentladung multipliziert mit der vorgegebenen Konzentration. Diese Option wird für massenkonservative Simulationen mit distributiven Advektionssystemen empfohlen (`3`, `4`,`5`, `13`,`14`).

Für kritische Massenbilanzanwendungen nutzen Sie die Option `2` zusammen mit dem Advektionsprogramm `14` oder `15`.
```

Gaia kann mit flüssigen Randdateien ausgeführt werden, um zeitabhängige suspendierte Lastflüsse zuzuordnen (der Abfluss sollte im Gleichgewicht gehalten werden). Die Solid-Flow-Time-Serie kann mit der bereits angewandten `455`-`5` Upstream-Grenze realisiert werden, analog zu den Beschreibungen der {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. Weitere Informationen zu ausgesetzten Lastbegrenzungsbedingungen finden Sie in Abschnitt 2.1.2 in der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).


## Numerische Parameter

Die meisten numerischen Parameter für die suspendierte Lastmodellierung hängen von der hydrodynamischen Telemac2d/3d-Lenkdateidefinition ab. In der Gaia-Lenkungsdatei sollten zusätzliche Schlüsselwörter angegeben werden, die die Simulation der suspendierten Last direkt beeinflussen.

Zum Beispiel werden die **SCHEME FOR ADVECTION ...** Schlüsselwörter für Geschwindigkeiten, Tracer und Turbulenzmodellierung mit der Hydrodynamik (Telemac2d/3d) Lenkdatei {ref}`general numerical parameters for finite elements <tm2d-fe>` definiert. Zusätzlich kann das Advektionsschema für suspendierte Last in der Gaia-Lenkungsdatei mit dem **SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS* Schlüsselwort definiert werden, das eines der folgenden Ganzzahl-Keywords akzeptiert (nur für 2d):

* `1` für das bedingungslose, nicht konservativ, aber diffusive (für kleine Zeitschritte) *Methode der Eigenschaften* Schema.
* `2` für das nicht konservative *Streamline Upwind Petrov Galerkin* (SUPG)-System, das den {term}`CFL`Zustand verwendet und weniger diffusiv als das *Characteristics* (`1`)-System ist.
* `3` oder `4` für das Konservierungsmittel *N-scheme* (distributiv) mit Zeitschrittreduktion basierend auf der {term}`CFL`-Zustand. Option `4` beinhaltet Massenverklumpung für verbesserte Stabilität. Diese Optionen sollten **not** in Anwesenheit von Gezeitenwohnungen verwendet werden ( stattdessen `13` oder `14`).
* `5` für das massenkonservative *PSI Distributive Schema* (**default**), das die Flußmittel nach Tracerkonzentrationen korrigiert und weniger diffusiv ist als `4` oder `14`. Die Berechnungszeit mit `5` ist länger als mit `4` oder `14`. Diese Option sollte **not** in Anwesenheit von Gezeitenwohnungen verwendet werden.
* `13` und `14` für den *Edge-basierten N-scheme* (NERD), der `3` und `4` ähnelt, aber an Gezeitenwohnungen angepasst ist. **Option `14` wird in diesem Tutorial** gemäß der Empfehlung in der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
* `15` für das massenkonservative *ERIA-System*, das mit Gezeitenwohnungen arbeitet.

Die Optionen `4` und `14` können zusammen mit der Keyword-Definition `CORRECTION ON CONVECTION VELOCITY : YES` (logisch, default `NO`) definiert werden, die die tiefe gemittelte Konvektionsgeschwindigkeit auf die vertikalen Gradienten von Geschwindigkeit und Konzentration umstellt. Diese Einstellung vermeidet eine Überschätzung der Schwebelastung, insbesondere in tiefen Gewässern, wird aber in diesem Tutorial nicht verwendet.

Die **SCHEME OPTION FÜR ADVECTION VON SUSPENDED SEDIMENTS** kann zusätzlich definiert werden, um entweder ein **starkes (Standard von `1`)* oder ein **weak (`2`)* Formular zur Advektion zu verwenden. Eine schwache Form verringert die Zahlen {term}`Diffusion`, ist konservativer und erhöht die Rechenzeit (weiterlesen unter {ref}`Telemac2d steady section <tm2d-fe>`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14
/ CORRECTION ON CONVECTION VELOCITY : YES / use when SCHEME is 4 or 14 for deep water
```

```{admonition} Diffusion of suspended sediment
:class: tip
Der Diffusionsterm der Advektionsdiffusionsgleichung wird von der turbulenten Wirbelviskosität des hydrodynamischen Lösers und einer konstanten Hintergrunddiffusivität bestimmt, die in der Gaia-Lenkdatei eingestellt werden kann:

* **COEFFICIENT FOR DIFFUSION OF SUSPENDED SEDIMENTS** (real, default`1.E-6`m$^2$s$^{-1}$): Konstante Diffusivität in 2d (in 3d Verwendung **COEFFICIENT FOR HORIZONTAL DIFFUSION OF SUSPENDED SEDIMENTS** und **COEFFICIENT FOR VERTICAL DIFFUTER

Für die meisten fluvialen Anwendungen ist der Standardwert ausreichend, da die turbulente Diffusivität über den konstanten Hintergrundterm dominiert.
```

Lesen Sie mehr über die Definition von numerischen Parametern in Abschnitt 2.1.5 in der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

## Morphologische Kupplung

Wenn die Schwebelastung zusammen mit der Bettentwicklung aktiviert wird, tragen die Erosions- und Abscheidungsflüsse zur Massenbilanz des Bettes durch die {term}`Exner equation`. Der Nettofluss (erosion minus Abscheidung) verändert die Betthöhe zu jedem Zeitschritt.

```{admonition} Morphological factor for suspended load
:class: tip
Für Langzeitsimulationen, bei denen morphologische Zeitskala viel länger als hydrodynamische Zeitskala sind, kann ein **MORPHOLOGISCHEr FACTOR* zur Beschleunigung der Bettentwicklung eingesetzt werden. Dieser Faktor multipliziert den Nettoerosion/Depositionsfluss, wodurch mehrjährige morphologische Simulationen mit angemessenen Rechenzeiten ermöglicht werden. Verwendung mit Vorsicht: morphologische Faktoren über 10-20 können unrealistische Ergebnisse einführen. Das Schlüsselwort ist in der Gaia-Lenkungsdatei definiert:

```fortran
MORPHOLOGICAL FACTOR : 10. / accelerate bed evolution 10x
```
```

## Anwendungsbeispiele

Beispiele für die Implementierung der hängenden Last kommen zusammen mit der TELEMAC-Installation (im `/telemac/examples/gaia/`-Verzeichnis). Die folgenden Beispiele in der `gaia/`-Ordner-Funktion (rein) hängen Lastberechnungen:

* 2d Modell des kombinierten zusammenhängenden und nichtkohäsiven Pendelverkehrs: **Hippodrom-t2d/*
* 2d Modell des kohäsiven Schlamm-Massenschutzes: **mud conservation-t2d/*
* 3d Modell des kombinierten zusammenhängenden und nichtkohäsiven Pendelverkehrs: **hippodrom-t3d/*
* 3d Modell des nicht-kohäsiven Hängetransports mit Hautreibungskorrektur: **lyn-t3d/*
* 3d Modell des zusammenhängenden Hängetransports mit vertikalem Rouse-Profil (vgl. [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf), Abschnitt 2.1.2): **rouse-t3d/**
* 3d Modell einer Flut mit kohäsivem Sediment: **tidal flats-t3d/*
* Kupplung mit Wellen: **sandpit-t2d/**

```{admonition} Recommended workflow for suspended load simulations
:class: note
1. **Start mit Hydrodynamik*: Stellen Sie sicher, dass das hydrodynamische Modell (Telemac2d/3d) kalibriert ist und vor der Kopplung mit Gaia sinnvolle Strömungsfelder erzeugt.
2. **Definale Sedimentklassen*: Geben Sie für den Standort geeignete Korngrößen an. Feine Sedimente ($D < 0.063$ mm) sind typischerweise kohäsiv; gröbere Sedimente sind nicht kohäsiv.
3. **Select Suspension Formel*: Wählen Sie auf Basis der Umwelt (Fluss: `1` oder `3`; Küste mit Wellen: `4`).
4. **Erstbedingungen festlegen*: Verwendung gemessener oder geschätzter suspendierter Sedimentkonzentrationen.
5. **Choose Advektion Schema*: Verwenden Sie `14` für Robustheit mit Gezeitenwohnungen oder `5` für eine bessere Genauigkeit in tiefen Kanälen.
6. **Calibraterosion/Deposition*: Passen Sie Partheniades konstant $M$, kritische Scherbeanspruchungen und Absetzgeschwindigkeiten auf die beobachteten Konzentrationen.
7. **Währende Massenbilanz**: Aktivieren Sie `MASS-BALANCE : YES` in der hydrodynamischen Steuerungsdatei, um den Sedimentschutz zu überwachen.
```