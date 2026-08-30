---
description: Konfigurieren Sie den Sedimenttransport in TELEMAC-GAIA mit der Meyer-Peter- und Müller-Formel, dem Shields-Parameter und der dimensionslosen Bettscherspannung für die 2D-morphodynamische Flussmodellierung.
---

(gaia-bl)=
# Bettlast


```{admonition} Bedload basics
:class: important

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/e6lk2pk72Gc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Bedload traveling in a lab flume by jumping, rolling, and sliding (under water footage). Source: Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


For a better learning experience, the {ref}`glossary` helps with explanations of the terms {term}`Sediment transport`, (dimensionless) {term}`bedload <Bedload>` transport $\Phi_b$, {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` $\tau_{x}$, and the {term}`Shields parameter` $\tau_{x,cr}$ (in this order).
```

```{admonition} Sediment replenishment, gravel augmentation, bedload addition (etc.)
:class: tip

Die Platzierung von gröberem Sediment für die Wiederherstellung des Bettentransports kann viele verschiedene Formen annehmen und wird durch eine breite Palette von Begriffen beschrieben. In TELEMAC ist die beste Option für die Simulation solcher Bettlastwiederherstellungsbemühungen das [**Nestor**](http://www.opentelemac.org/index.php/modules-list/163-dredgesim-modeling-dredging-operations-in-the-river-bed)Modul, das Gaia (oder SISYPHE) benötigt. Lesen Sie mehr in der neuesten [Nestor Handbuch](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/nestor/user/nestor_user_9.0.pdf)].
```

(bl-principles)=
## Grundsätze

The calculation of {term}`bedload <Bedload>` transport requires expert knowledge about the modeled ecosystem for judging whether the system is sediment supply-limited or transport capacity-limited {cite:p}`church_morphodynamics_2015`.

Sedimentversorgung begrenzte Flüsse
Ein sedimentversorgungsbegrenzter Fluss zeichnet sich durch deutlich sichtbare Schnitttrends aus, die darauf hindeuten, dass der Fluss möglicherweise mehr Sediment transportieren könnte, als im Fluss verfügbar ist. Sedimentversorgung begrenzte Flussabschnitte treten typischerweise stromabwärts von Dämmen auf, die eine unüberwindbare Barriere für Sedimente darstellen. In einem angebotsbegrenzten Fluss ist somit die **Flow-Kompetenz** (hydrodynamische Kraft oder **Transportkapazität**) nicht ausreichend, um ein typischerweise grobes Flussbett zu mobilisieren, reicht aber für den Transport externer Sedimentversorgung aus.

Transport capacity-limited (alluvial) rivers
: A transport capacity-limited river is characterized by sediment abundance where the flow is too small to transport all available sediment during a flood. Sediment accumulations (i.e., the alluvium) are present and the channel tends to braid into {term}`anabranches <Anabranch>` (or to anastomose in fine/sand-dominated environments). Thus, the **flow competence** (or **transport capacity**) is insufficient to transport the entire amount of available sediment (external supply and riverbed).

```{admonition} Limitation types vary in space and in time
:class: important
Die Kanaltypen können im Raum zwischen Flussabschnitten oder -segmenten und in der Zeit stark variieren. Zum Beispiel kann derselbe Flussabschnitt, der aufgrund unzureichender Strömungskompetenz angebotsbegrenzt zu sein scheint, während eines Hochwassers zu einem transportkapazitätsbegrenzten Abschnitt werden, wenn hohe Ableitungen hohe Scherbelastungen auf das Flussbett ausüben. Die räumlich-zeitliche Variation der Arten von Transportbeschränkungen ist besonders ausgeprägt in gesunden Flussökosystemen, die sich ständig an ein morphodynamisches Gleichgewicht anpassen.
```

Die folgenden Abbildungen zeigen sedimentangebotsbegrenzte Flussreichweiten und eine transportkapazitätsbegrenzte Flussreichweite.

`````{tab-set}
````{tab-item} Artificially sediment supply-limited
```{figure} ../../img/nature/doubs-capacity-2015.JPG
:height: 350px
:alt: channel doubs france sediment supply transport limited
:name: doubs-2015

Die Doubs in der Franche-Comté (Frankreich) während einer kleinen Flut. Die Sedimentversorgung wird durch eine Dämmkaskade stromaufwärts unterbrochen mit der Folge eines geraden monotonen Kanals mit signifikantem Pflanzenwachstum entlang der Ufer. Das Flussbett besteht hauptsächlich aus Felsbrocken, die die meiste Zeit unbeweglich sind. Somit kann der Flussabschnitt als künstlich sedimentangebotsbegrenzt charakterisiert werden (Bild: Sebastian Schwindt 2015).
```
````

````{tab-item} Naturally sediment supply-limited
```{figure} ../../img/nature/krimmler-ache-2010.jpg
:height: 350px
:alt: naturally channel krimmler ache austria sediment supply transport limited
:name: krimml-2010
:class: with-shadow

The Krimmler Ache in Austria during a small flood event. Even though the watershed has a high {term}`Sediment yield`, the transport capacity of the water in this river section is so high that the riverbed predominantly consists of large boulders. Thus, the river section can be characterized as naturally sediment supply-limited (picture: Sebastian Schwindt 2010).
```
````

````{tab-item} Capacity-limited
```{figure} ../../img/nature/jenbach-alluvial-2020.jpg
:height: 350px
:alt: alluvial channel jenbach sediment supply transport limited
:name: jenbach-2020

Der Jenbach in den Bayerischen Alpen (Deutschland) nach einer intensiven natürlichen Sedimentversorgung in stromaufwärts gelegener Reichweite in Form eines Erdrutsches. Der Flussabschnitt kann als transportkapazitätsbegrenzt charakterisiert werden (Bild: Sebastian Schwindt 2020).
```
````
`````

**Warum ist die Unterscheidung zwischen Sedimentversorgung und transportkapazitätsbegrenzten Flüssen für die numerische Modellierung wichtig?**

Gaia provides different formulae for calculating bedload transport, which are partially either derived from lab experiments with infinite sediment supply (e.g., the {cite:t}`meyer-peter_formulas_1948` formula and its derivates, see {ref}`below <gaia-mpm>`) or from field measurements in partially transport capacity-limited rivers (e.g., {cite:t}`wilcock_critical_1993`). Formulae that account for limited sediment supply often involve a correction factor for the {term}`Shields parameter`.

## Formeln und Parameter

{term}`Bedload` is typically designated with $q_b$ (in kg$\cdot$s$^{-1}\cdot$m$^{-1}$ i.e. weight per unit time and width) and accounts for particulate transport in the form of the displacement of rolling, sliding, and/or jumping coarse particles. In river hydraulics, the so-called {term}`Dimensionless bed shear stress`, also referred to as {term}`Shields parameter` {cite:p}`shields_anwendung_1936`, is often used as a threshold value for the mobilization of sediment from the riverbed. TELEMAC and Gaia build on a dimensionless expression of bedload transport intensity according to {cite:t}`einstein_bed-load_1950`:

$$
\Phi_b = \frac{q_b}{\rho_{s} \sqrt{(s - 1) g D^{3}_{pq}}}
$$ (eq-phi-gaia)

where $\rho_{s}$ is the density of sediment grains; $s$ is the ratio of sediment grain and water density (typically 2.68) {cite:p}`schwindt_hydro-morphological_2017`; $g$ is gravitational acceleration; and $D_{pq}$ is the characteristic grain diameter of the sediment class (cf. {ref}`gaia-sed`). Note that the dimensionless expression $\Phi$ and the dimensional expression $q_{b}$ represent unit bedload (i.e., bedload normalized by a unit of width). **Gaia outputs are dimensional and correspond to $q_{b}$** (recall the **VARIABLES FOR GRAPHIC PRINTOUTS** definitions in the {ref}`General Parameters section <gaia-gen>`) where the unit of width corresponds to the edge length of a numerical mesh cell over which the mass fluxes are calculated.

```{admonition} Gaia computes bedload in mass transport rate
:class: note
Im Gegensatz zu SISYPHE berechnet Gaia Bettlastflüsse als (trockene) Massentransportrate pro Breiteneinheit ohne Poren. Die numerische Berechnung von Sedimentflüssen in Bezug auf die Trockenmasse minimiert den Rundungsfehler, insbesondere für die für das Bettschichtmodell verwendeten Stoffaustauschalgorithmen.
```

```{admonition} Comment on the Original Einstein (1950) Expression
:class: dropdown
The original equation for $\Phi_b$ can be found on page 34 (Equation 42) in {cite:t}`einstein_bed-load_1950`. This formula involves an additional division by the gravitational acceleration $g$, which does not appear in later references to the Einstein expression of $\Phi_b$ and would also not result in a dimensionless term. For this reason, Equation {eq}`eq-phi-gaia` is adapted here.
```

Equation {eq}`eq-phi-gaia` expresses only the dimensional conversion for bedload transport (i.e., the way how dimensions are removed or added to sediment transport). In fact, this is only the first step to solve the other side of a bedload equation using a (semi-) empirical formula. To calculate $\Phi_{b}$, Gaia provides a set of (semi-) empirical formulae, which can be modified with user Fortran files and defined in the Gaia steering file with the **BED-LOAD TRANSPORT FORMULA FOR ALL SANDS** `integer` keyword. {numref}`Table %s <tab-gaia-bl-formulae>` lists possible integers for the keyword to define a bedload transport formulae, including references to original publications, formula application ranges, and the names of the Fortran source files for modifications.

```{csv-table} *Bedload transport formulae implemented in Gaia with application limits regarding the grain diameter $D$, **cross section-averaged** Froude number $Fr$, slope $S$, water depth $h$, and flow velocity $u$. The Fortran files live in the /telemac/sources/gaia/ directory.*
:header: Gaia, Author(s), $D$, "*{term}`Fr <Froude number>`*; $S$; $h$; and $u$", User Fortran
:header-rows: 1
:name: tab-gaia-bl-formulae
 "(no.)", "(ref.)", "(10$^{-3}$m)", "(-); (-); (m); (m/s)", "(file name)"
 `1`, "{cite:t}`meyer-peter_formulas_1948`", 0.4 $<D_{50}<$28.6, "10$^{-4}<Fr<$639<br> 0.0004$<S<$0.02<br>0.01$<h<$1.2<br>0.2$<u$", bedload_meyer.f
 `2`, "{cite:t}`einstein_bed-load_1950`-{cite:t}`brown1949`", 0.25$<D_{35}<$32, "", bedload_einst.f
 `3`, "{cite:t}`engelund_monograph_1967` + {cite:t}`chollet1979`", 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", bedload_engel_cc.f
 `7`, {cite:t}`van_rijn_sediment_1984`, 0.6$<D_{50}<$2.0, "0.5$<h$<br>0.2$<u$", bedload_vanrijn.f
 `10`, {cite:t}`wilcock2003`,"0.063 $\lesssim D_{pq}$", "", bedload_wilcock_crowe.f
 `30`, "{cite:t}`engelund_monograph_1967`", 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", bedload_engel.f
```

**Beachten Sie, dass die Engelund-Hansen-Formeln (Optionen `3` und `30`) den gesamten Sedimenttransport** berechnen, dh die Summe aus Bettlast und suspendierter Last. Wenn Sie also diese Formeln verwenden, aktivieren Sie nicht zusätzlich die Modellierung der suspendierten Last, um Doppelzählungen zu vermeiden.

Um die Formel {cite:t}`meyer-peter_formulas_1948` (`1` gemäß {numref}`Tab. %s <tab-gaia-bl-formulae>`) in diesem Tutorial zu verwenden, **fügen Sie die folgende Zeile zur Steuerungsdatei gaia-morphdynamics.cas hinzu**:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
/
BED LOAD FOR ALL SANDS : YES / deactivate with NO
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1
```

The following sections provide more details on how $\Phi_{b}$ is calculated with the pre-defined formulae listed in {numref}`Tab. %s <tab-gaia-bl-formulae>`.

```{admonition} User-defined Bedload transport formulae in a specific Fortran file
:class: tip
Benutzer können weitere Bettlasttransportformeln hinzufügen, indem sie eine modifizierte Kopie einer FORTRAN-Dateivorlage hinzufügen. Das [Gaia-Handbuch](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) erklärt das Verfahren zum Hinzufügen einer neuen benutzerdefinierten Bettlastformel im Detail in Abschnitt 6.3.
```

```{admonition} User Fortran Files
:class: note, dropdown
To implement a user Fortran file, copy the original TELEMAC Fortran file from the `/telemac/sources/` directory (e.g., `/telemac/sources/gaia/bedload_einst.f`) to the project directory (e.g., `/telemac/simulations/gaia-tutorial/user_fortran/bedload_einst.f`). Finally, tell TELEMAC where to look for user fortran files by defining the following keyword in a steering file (e.g., in `gaia-morphodynamics.cas`):

`FORTRAN FILE : 'user_fortran'`
```

(gaia-mpm)=
### Meyer-Peter und Müller (1948)

```{admonition} Recall the validity range for the MPM formula (1)
:class: warning
Überarbeiten Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass sich die Anwendung im geltenden Parameterbereich befindet, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde.
```

The {cite:t}`meyer-peter_formulas_1948` formula was published in 1948 by Swiss researchers Eugen Meyer-Peter, professor at [ETH Zurich](https://ethz.ch/en.html) and founder of the school's hydraulics laboratory (Zurich's famous [VAW](https://vaw.ethz.ch/)), and Robert Müller. Their empirical formula is the result of more than a decade of collaboration and the elaboration began one year after the VAW was founded in 1931 when Robert Müller was appointed assistant to Eugen Meyer-Peter. The two scientists also worked with Henry Favre and Hans-Albert Einstein who came up with another approach for calculating bedload. An early version of the {cite:t}`meyer-peter_formulas_1948` formula was published in 1934 and it is the basis for many other formulas that refer to a critical {term}`Dimensionless bed shear stress` (i.e., {term}`Shields parameter`). It is important to remember that the formula is based on data from lab flume experiments with high sediment supply. This is why bedload transport calculated with the {cite:t}`meyer-peter_formulas_1948` formula corresponds to the {ref}`hydraulic transport capacity <bl-principles>` of an alluvial channel. Thus, **the {cite:t}`meyer-peter_formulas_1948` formula tends to overestimate bedload transport** and it is inherently designed for estimating bedload **based on simplified 1d cross section-averaged hydraulics** (see also the {ref}`Python sediment transport exercise <ex-py-sediment>`). Good results can be expected when flood flows are simulated in an alluvial river section.

Letztendlich kann die linke Seite von Gleichung {eq}`eq-phi-gaia` ($\Phi_b$) mit der {cite:t}`meyer-peter_formulas_1948`-Formel wie folgt berechnet werden:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x,cr} > \tau_{x} \\ f_{mpm} \cdot (\tau_{x} - \tau_{x,cr})^{3/2} & \mbox{ if } \tau_{x,cr} \leq \tau_{x}\end{cases}
$$ (eq-mpm)

Wobei $f_{mpm}$ der MPM-Koeffizient ist (Standard ist 8), $\tau_{x,cr}$ bezeichnet den {term}`Shields parameter` ($\approx$ 0.047 und bis zu 0.07 in Bergflüssen), und $\tau_{x}$ ist der {term}`Dimensionless bed shear stress`. Bei Verwendung der {cite:t}`meyer-peter_formulas_1948`-Formel mit Gaia wird die Konsistenz mit den Originalpublikationen sichergestellt, indem $\tau_{x,cr}$ und $f_{mpm}$ in der Steuerungsdatei** definiert werden:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1 / see above
CLASSES SHIELDS PARAMETERS : 0.047;0.047;0.047
MPM COEFFICIENT : 8
```

````{admonition} Wong-Parker correction of the MPM formula
Die Wong-Parker {cite:p}`wong_reanalysis_2006` Korrektur für die Formel {cite:t}`meyer-peter_formulas_1948` bezieht sich auf eine statistische Neuanalyse der ursprünglichen experimentellen Datensätze und gilt für {term}`Plane bed` Flussabschnitte. Zu diesem Zweck liefert die Wong-Parker-Korrektur niedrigere Transportwerte und schließt die Form-Drag-Korrektur der ursprünglichen Formel mit dem folgenden Ausdruck aus: $\Phi_{b} \approx 3.97 \cdot (\tau_{x} - 0.0495)^{3/2}$. Um die Wong-Parker-Korrektur in Gaia zu implementieren, verwenden Sie:

```fortran
CLASSES SHIELDS PARAMETERS : 0.0495;0.0495;0.0495
MPM COEFFICIENT : 3.97
```
````

**To directly continue with the tutorial using the {cite:t}`meyer-peter_formulas_1948` formula, jump to the {ref}`correction factors <c-factors>` section.**

(gaia-einstein)=
### Einstein-Brown (1942/49)

```{admonition} Recall the validity range for the Einstein-Brown formula (2)
:class: warning
Überarbeiten Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass sich die Anwendung im geltenden Parameterbereich befindet, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde.
```

Hans Albert Einstein, Sohn des berühmten Albert Einstein, war ein Pionier der Wahrscheinlichkeitsanalysen des Sedimenttransports. Insbesondere stellte er die Hypothese auf, dass der Beginn und das Ende der Sedimentbewegung in Bezug auf Wahrscheinlichkeiten ausgedrückt werden können. Darüber hinaus nahm Einstein an, dass die Sedimentbewegung eine Reihe von schrittweisen Verschiebungen ist, gefolgt von Ruheperioden, und dass der durchschnittliche Abstand einer Partikelverschiebung etwa das Hundertfache des Teilchendurchmessers beträgt. Um die Beobachtungen zu berücksichtigen, die er in Laborflimmerexperimenten gemacht hat, führte Einstein außerdem das Verstecken und Heben von Korrekturkoeffizienten ein {cite:p}`einstein1942`.

Die Einstein-Formel unterscheidet sich von jeder {cite:t}`meyer-peter_formulas_1948`-basierten Formel dadurch, dass sie keine Schwelle für die beginnende Bewegung von Sedimenten impliziert. Trotz oder weil Einsteins Sedimenttransporttheorie komplexer ist als viele andere Bettlasttransportformeln, wurde sie in technischen Anwendungen nicht sehr populär. Heute ermöglicht Gaia die benutzerfreundliche Anwendung von Einsteins Formel, die 1949 von {cite:t}`brown1949` auf einer hydraulischen Konferenz vorgestellt wurde. Laut {cite:t}`einstein1942`-{cite:t}`brown1949` wird die linke Seite von Gleichung {eq}`eq-phi-gaia` ($\Phi_b$) wie folgt berechnet:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x} < 0.0025 \\ F_{eb}\cdot 2.15 \cdot \exp{(-0.391/\tau_{x})} & \mbox{ if } 0.0025 \leq \tau_{x} \leq 0.2\\ F_{eb} \cdot  40 \cdot \tau_{x}^{3} & \mbox{ if } \tau_{x} > 0.2\end{cases}
$$ (eq-einstein-brown)

wo

$$
F_{eb} = \left(\frac{2}{3} + \frac{36}{D_x}\right)^{0.5} - \left(\frac{36}{D_x}\right)^{0.5}
$$ (eq-f-eb)

$D_x$ ist der dimensionslose Teilchendurchmesser berechnet als:

$$
D_x = \left[\frac{(s-1)\cdot g}{\nu^2}\right]^{1/3}\cdot D_{pq}
$$ (eq-d-dimless)

Dabei ist $s$ das Verhältnis von Sedimentkorn und Wasserdichte (normalerweise 2,68); $g$ ist die Gravitationsbeschleunigung; und $\nu$ ist die kinematische Viskosität von Wasser ($\approx$10$^{-6}$m$^{2}$s@s$^{-1}$) {cite:p}`schwindt_hydro-morphological_2017`.

Um die {cite:t}`einstein1942`-@-{cite:t}`brown1949` Formeln in Gaia zu verwenden, verwenden Sie:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 2
```

```{admonition} Consider adapting bedload_einst.f
Die Anwendungsschwellenwerte als Funktion von $\tau_{x}$ stammen aus der Gaia Fortran-Datei `bedload_einst.f` in `/telemac/sources/gaia/`. Die ursprünglichen Veröffentlichungen von {cite:t}`einstein1942`-@-{cite:t}`brown1949` deuten jedoch einen Schwellenwert von $\tau_{x}$=0.182 (anstatt 0,2) für den Wechsel der Formelfälle an.
```


(gaia-engelund)=
### Engelund-Hansen (1967) / Chollet-Cunge

```{admonition} Recall the validity range for the Engelund-Hansen formulae (3 and 30)
:class: warning
Überarbeiten Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass sich die Anwendung im geltenden Parameterbereich befindet, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde. Beachten Sie, dass diese Formeln den gesamten Sedimenttransport** (Bettlast + Schwebelast) berechnen.
```

The {cite:t}`engelund_monograph_1967` formula accounts for total sediment transport including {term}`Bedload` and {term}`Suspended load`. Starting from the Bagnold power-approach {cite:p}`bagnold_approach_1966,bagnold_empirical_1980`, the {cite:t}`engelund_monograph_1967` formula was developed for sediment transport calculations over dune channel beds. The approach accounts for energy losses required to drive particles uphill on dunes of the riverbed. The {cite:t}`bagnold_approach_1966` theory considers the total shear as the sum of the shear transmitted between grains and the fluid, and the shear transmitted by momentum changes caused by intergranular collisions. Thus, erosion takes place as long as the {term}`Dimensionless bed shear stress` is greater or equal to its critical value (i.e., the {term}`Shields parameter`). Gaia implements the {cite:t}`engelund_monograph_1967` by calculating the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) as follows:

$$
\Phi_b = 0.1\cdot \frac{\tau_{x}^{2.5}}{c_f}
$$ (eq-engelund)

where $c_f$ is an adimensional friction coefficient and $\tau_x$ is the Shields number without the skin friction correction factor. Read more about skin friction in the {ref}`correction factors <c-friction>` section. To use the original {cite:t}`engelund_monograph_1967` formula in Gaia use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 30
```

Darüber hinaus hat {cite:t}`chollet1979` eine schrittweise Funktion zur Berechnung eines modifizierten Shields-Parameters $\tau^*_x$ eingeführt, der verschiedene Transportregime berücksichtigt:

$$
\tau^*_x = \begin{cases} 0 & \mbox{ if } \tau_{x} \leq 0.06 & \mbox{ (no transport)}\\ [2.5 (\tau_{x} - 0.06)]^{0.5} & \mbox{ if } 0.06 < \tau_{x} < 0.384  & \mbox{ (dune regime)} \\ 1.066\cdot \tau_{x}^{0.176} & \mbox{ if } 0.384 < \tau_{x} < 1.08  & \mbox{ (transition regime)} \\ \tau_{x} & \mbox{ if } 1.08 \leq \tau_{x}  & \mbox{ (sheet flow)} \end{cases}
$$ (eq-f-eh)

To apply the {cite:t}`chollet1979` modification of the {cite:t}`engelund_monograph_1967` formula use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 3
```

(gaia-rijn)=
### van Rijn (1984)

```{admonition} Recall the validity range for the van-Rijn formula (7)
:class: warning
Überarbeiten Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass sich die Anwendung im geltenden Parameterbereich befindet, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde.
```

Die Sedimenttransportformel von Leo van Rijn {cite:p}`van_rijn_sediment_1984` ist inspiriert von den Theorien von {cite:t}`bagnold_empirical_1980`, {cite:t}`einstein1942` und {cite:t}`ackers_sediment_1973`. Die {cite:t}`van_rijn_sediment_1984`-Formeln gehen davon aus, dass die Bettlast von der Schwerkraft dominiert wird, während der Transport der hängenden Ladung gemäß {cite:t}`bagnold_empirical_1980` durch Turbulenzen gesteuert wird. Zu diesem Zweck berechnen die {cite:t}`van_rijn_sediment_1984` Formeln den Bettlasttransport ähnlich wie {cite:t}`ackers_sediment_1973`, wo die Transportraten von Reibungsgeschwindigkeiten abhängen. Um sein bettnahes Feststofftransportmodell zu kalibrieren, verwendete {cite:t}`van_rijn_sediment_1984` Daten aus Experimenten an Flachbettkanälen mit einem durchschnittlichen Sedimentkorndurchmesser von 1,8 mm. {cite:t}`van_rijn_sediment_1984` führte zusätzliche Experimente durch, um die Ergebnisse seines Modells gegen unterschiedliche Korndurchmesser zwischen 0,2 und 2 mm zu überprüfen. Darüber hinaus hat {cite:t}`van_rijn_sediment_1984` Kriterien für Sedimentsuspension basierend auf Laborexperimenten mit Korndurchmessern von weniger als 0,5 mm und durch empirische Vereinfachung der Kalibrierparameter festgelegt. Während die ursprüngliche {cite:t}`van_rijn_sediment_1984`-Formel den gesamten Sedimenttransport berücksichtigt (d.h. {term}`Bedload` und {term}`Suspended load`), sind die folgenden Erklärungen für die Implementierung in Gaia nur auf {term}`Bedload` beschränkt.

Laut {cite:t}`van_rijn_sediment_1984` wird die linke Seite von Gleichung {eq}`eq-phi-gaia` ($\Phi_b$) wie folgt berechnet:

$$
\Phi_b = \frac{0.053}{D_{x}^{0.3}} \cdot \left(\frac{\tau_{x} - \tau_{x,cr}}{\tau_{x,cr}}\right)^{2.1}
$$ (eq-rijn)

Explanations of the {term}`Dimensionless bed shear stress` $\tau_{x}$, its critical value $\tau_{x,cr}$ (i.e., the {term}`Shields parameter`), and the dimensionless grain diameter $D_{x}$ are provided in the above sections on the {ref}`Meyer-Peter and Müller <gaia-mpm>` and the {ref}`Einstein-Brown <gaia-einstein>` formulae.

To use the {cite:t}`van_rijn_sediment_1984` formula in Gaia use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 7
```

(gaia-wilcock)=
### Wilcock-Crowe (2003)

```{admonition} Applicability of the Wilcock-Crowe formula (10)
:class: warning
The multi-fraction bedload transport formula from {cite:t}`wilcock2003` does not state particular validity ranges, but the authors restrict their approach to sand-gravel-cobble sediments with a minimum grain diameter of 0.063 mm. The explanations in this section limit to the application background of the {cite:t}`wilcock2003` approach. The complex set of equations is explained in detail in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) (section 3.1.2) and by {cite:t}`cordier2019,cordier2020`.
```

Der {cite:t}`wilcock2003`-Ansatz ist ein Multifraktions-Sedimenttransportmodell, das hauptsächlich in gepanzerten Flussabschnitten zur Modellierung der Aggradation oder Degradation von Betten angewendet wird. Das Modell basiert auf Oberflächenuntersuchungen und ist besonders für die Vorhersage von transienten Bedingungen der Bettpanzerung geeignet. Es berücksichtigt die volle Größenverteilung der Bettoberfläche (vom feinsten Sand bis zum gröbsten Kies) und wurde mit insgesamt 49 Flume-Experimenten mit kleinen bis hohen Wasserableitungen und fünf verschiedenen Sedimentmischungen kalibriert.

The approach takes up the idea of {cite:t}`parker1990` on applying a reference shear stress at which little but constant solid transport rate can be observed. The reference shear stress is close to, but a little bit larger than the {term}`Shields parameter` $\tau_{x,cr}$. To this end, {cite:t}`wilcock2003` implement a reference transport rate of 0.002 as proposed by {cite:t}`parker1990`.

Moreover, the multi-fraction {cite:t}`wilcock2003` model uses the complete sediment grain size distribution of the riverbed surface and calculates bedload transport for each of the specified grain size classes. The sediment transport model builds on flume experiments from {cite:t}`proffitt1983` and {cite:t}`parker1990`, and it accounts for hiding/exposure effects on gravel transport as a function of the sand fraction in the riverbed. The hiding-exposure function is designed to resolve discrepancies observed from previous experiments, including the hiding-exposure effect of sand content on gravel transport for weak to high values of sand content in the bulk.

Kurz gesagt stellt das {cite:t}`wilcock2003`-Modell eine Weiterentwicklung der {cite:t}`meyer-peter_formulas_1948`-Formel dar, greift die Implementierung einer Referenztransportrate {cite:p}`parker1990` auf und ist auf Versteck-/Expositionseffekte als Funktion des Sandanteils kalibriert.

Um die Formel {cite:t}`wilcock2003` in Gaia zu verwenden, definieren Sie mehrere {ref}`sediment classes <gaia-sed>` und verwenden Sie:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 10
```

(c-factors)=
## Korrekturfaktoren

Korrekturfaktoren für den Sedimenttransport können erforderlich sein, um die transversale Kanalsteigung, Sekundärströme oder die Korrektur der Hautreibung zu berücksichtigen.

(c-friction)=
### Reibungskorrektureinrichtungen

Reibung wird oft mit vereinfachten Ansätzen betrachtet, die Hautreibung und Formwiderstand in einen Topf werfen, aber in einem zweidimensionalen Modell beeinflusst nur die Hautreibung die Bettlast. {cite:t}`einstein_bed-load_1950` berücksichtigt Hautreibung mit einem Korrekturfaktor $\mu$ für (dimensionale) Bettscherbeanspruchung $\tau$:

$$
\tau' = \mu \cdot \tau
$$ (eq-tau-fr)

```{admonition} How Telemac2d calculates $\tau$
Telemac2d uses the length of the $x$-$y$ velocity vectors to calculate $\tau$ with the user-defined `FRICTION COEFFICIENT` $c_{f}$: $\tau = 0.5\cdot \rho_{w}\cdot c_{f}\cdot (U^2 + V^2)$.
```

Der Korrekturfaktor $\mu$ ist definiert als das Verhältnis des reinen Hautreibungskoeffizienten $c'_{f}$ und des globalen Reibungskoeffizienten $c_{f}$ (d.h. stückige Hautreibung und Formwiderstand):

$$
\mu = \frac{c'_{f}}{c_{f}}
$$ (eq-f-fr)

Der reine Hautreibungskoeffizient wird wie folgt berechnet:

$$
c'_{f} = 2\cdot \left(\frac{\kappa}{\log(12 h/ k'_{s})}\right)^{2}
$$ (eq-cf-skin)

wobei $\kappa$ die {cite:t}`von_karman_mechanische_1930`-Konstante (0.4) ist, $h$ die Wassertiefe ist und $k'_{s}$ die repräsentative Rauheitslänge ist, die als $k'_s = \alpha_{ks} \cdot D_{50}$ berechnet wird, wobei $\alpha_{ks}$ ein Kalibrierungsparameter ist (lesen Sie mehr im Abschnitt über {ref}`bedload calibration <bl-calibration>`).

`````{tab-set}
````{tab-item} Skin Friction
Gaia verwendet standardmäßig den Korrekturkoeffizienten der Hautreibung, den sie vom hydrodynamischen Solver ableitet (d. H. Telemac2d/3d). In sehr flachen Gewässern kann dieses Verhalten zu Instabilitäten führen. Daher kann das Schlüsselwort **SKIN FRICTION CORRECTION** in Gaia festgelegt werden, um die Korrekturfaktorberechnung zu steuern:

* `0`: Deaktiviert Korrektur, Einstellung $\mu = 1$ (Gesamtbettscherspannung von Hydrodynamik wird direkt verwendet)
* `1`: Ermöglicht die Korrektur der Hautreibung (**Standard**), berechnet $\mu$ gemäß Gleichungen {eq}`eq-f-fr` und {eq}`eq-cf-skin`
* `2`: Ermöglicht einen Bettform-Prädiktor, der Wellen bei der Berechnung berücksichtigt $\mu$

To disable skin friction correction (i.e., set $\mu$ to 1), add the following to the Gaia steering file (not used in this tutorial):

```fortran
SKIN FRICTION CORRECTION : 0 / default is 1 to enable skin friction correction
```

Der Koeffizient $\alpha_{ks}$ (Verhältnis zwischen Hautreibungsrauhigkeit und mittlerem Durchmesser) kann mit dem Schlüsselwort **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER** geändert werden (Standard ist 3.0). Lesen Sie mehr in Abschnitt 3.1.8 des [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)].
````

````{tab-item} Bedform Roughness
The finer the sediment of the riverbed, the more important turbulence created by the bed shape becomes. For instance, skin friction calculated based on a multiple of the diameter of a sand grain's characteristic roughness length $k'_{s}$ is very small. However, sand tends to shape the riverbed into ripple or dune forms, which cause additional *bedform turbulence*, as featured in the video below.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/q4eRwyeLKfA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>by Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Standardmäßig berücksichtigt Gaia keine Turbulenzen (d. H. Rauheitseffekte) von Bettformen, aber es kann aktiviert werden, indem das Schlüsselwort COMPUTE BED ROUGHNESS AT SEDIMENT SCALE** auf `YES` gesetzt wird (Standard ist `NO`). Dann kann eine der folgenden Optionen für das Schlüsselwort **BED ROUGHNESS PREDICTOR OPTION** definiert werden:

* `1` für eine Flachbettannahme mit dem Standardansatz von $k_s = \alpha_{ks} \cdot D_{50}$ (geändert mit **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER**).
* `2` for ripple bedforms. For currents only, the ripple roughness is a function of the mobility number. For waves and combined waves-currents, bedform dimensions are calculated as a function of wave parameters following {cite:t}`wiberg1994`.
* `3` für {cite:t}`rijn2007` Gesamtbettrauheit Prädiktor (nur Ströme). Die Gesamtrauhigkeit wird zerlegt in Kornrauhigkeit, kleinräumige Rillenrauhigkeit, Mega-Ripple-Komponente und Dünenrauhigkeit.

Das [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)] (Abschnitt 3.1.9) fasst den Satz von Gleichungen zusammen, die in die Berechnung der ** BED ROUGHNESS PREDICTOR OPTION** eingehen.

````
`````

(gaia-dir)=
### Richtung und Größe (Intensität)

Natural rivers are characterized by non-straight lines of the {term}`Thalweg`, which involves that water and sediment are subjected to curve effects. However, water and sediment behave differently in a curve because sediment has greater inertia than water {cite:p}`mosselman_five_2016`. Gaia accounts for the inertia of sediment transport as a function of water depth, curve radius, a spiral flow coefficient (`A`), and the depth-averaged, 2d velocities *U* and *V*. In addition, sediment transport reacts more inert to horizontal (transversal) channel slope and can be considered in $x$ and $y$ directions (see also the explanation of the {term}`Exner equation`). To this end, Gaia calculates the slope-corrected unit bedload transport $q_{b,sc}$ as follows:

$$
q_{b,sc} = q_{b} \left[1 + \beta \left(\cos \alpha  \frac{\partial z_{b}}{\partial x} + \sin \alpha \frac{\partial z_{b}}{\partial y} \right)\right]
$$ (eq-qb-corr)

Hierbei ist $\alpha$ der Winkel zwischen der Längsachse ($x$) und dem Bettlasttransportvektor (siehe auch {term}`Exner equation`), $\beta$ ist ein empirischer Bettlastintensitätskorrekturfaktor von {cite:t}`koch1980` und $z_{b}$ ist die Flussbetthöhe.

Der Grad der Bettlastabweichung (über $\alpha$) und der $\beta$-Faktor können in Gaia mit den Schlüsselwörtern **FORMULA FOR DEVIATION** und **FORMULA FOR SLOPE EFFECT** (horizontal) definiert werden. Um eines oder beide Keywords zu verwenden, muss das Schlüsselwort **SLOPE EFFECT** auf `YES` gesetzt werden (Standard ist `YES`).

Das Schlüsselwort **FORMULA FOR DEVIATION** kann die folgenden ganzzahligen Werte verwenden, um eine bestimmte Formel für die Funktion Sedimentform zu definieren (siehe Abschnitt 3.1.4 in [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)]):

* `1` für Bett-Level-Berechnung gemäß {cite:t}`koch1980` (**Standard**).
* `2` for the {cite:t}`talmon1995` approach based on laboratory experiments, which should be used with the **PARAMETER FOR DEVIATION** keyword for setting the `BETA2` parameter (its default is `PARAMETER FOR DEVIATION : 0.85`, but an optimum was found with `1.6` {cite:p}`mendoza2017`).
* `3` für den {cite:t}`apsley2008bedload`-Ansatz basierend auf dem kritischen Shields-Parameter und dem Reibungswinkel des Sediments, der mit dem Schlüsselwort **FRICTION ANGLE OF THE SEDIMENT** verwendet werden sollte (Standard ist `40.`).

Das Schlüsselwort **FORMULA FOR SLOPE EFFECT** beeinflusst nicht nur die Richtung des Sedimenttransports, sondern auch die Größe (oder Intensität) der Bettbelastung und kann folgende Werte annehmen:

* `1` für Bett-Level-Berechnung gemäß {cite:t}`koch1980` (**Standard** und ähnlich wie FORMULA FOR DEVIATION). Die Einstellung `1` ermöglicht die Definition des empirischen Korrekturfaktors der Bettneigung $\beta$ in Gleichung {eq}`eq-qb-corr` durch das Schlüsselwort **BETA** (Standard ist `BETA : 1.3`).
  - Um die Änderung der Betthöhe zu erhöhen, erhöhen Sie ** BETA **.
  - Um die Änderung der Betthöhe zu verringern, verringern Sie ** BETA **.
* `2` für die Hangkorrektur in Sandbettflüssen basierend auf einem Ansatz von {cite:t}`soulsby1997`, der eine Korrektur des {term}`Shields parameter` als Funktion des Reibungswinkels des Sediments und des Flussbetthangs anwendet. Der Reibungswinkel kann mit dem zusätzlichen Schlüsselwort **FRICTION ANGLE OF THE SEDIMENT** definiert werden (Standard ist `40.`).
* `3` für den {cite:t}`apsley2008bedload`-Ansatz, der sowohl den kritischen Shields-Parameter als auch die effektive dimensionslose Scherspannung modifiziert. Verwenden Sie mit dem Schlüsselwort **FRICTION ANGLE OF THE SEDIMENT**.

```{admonition} Sediment sliding
:class: tip
Wenn die untere Steigung eine kritische Steigung (typischerweise den Ruhewinkel) übersteigt, können Sedimente aufgrund geomechanischer Prozesse bewegt werden. Gaia implementiert Sedimentgleiten mit dem Schlüsselwort **SEDIMENT SLIDE**:
* `0`: kein Schieben (**Standard**)
* `1`: Einfache massenkonservative Glättung der Bodenhänge bis zum Ruhewinkel
* `2`: Lawinenformel von {cite:t}`apsley2008bedload`

Verwenden Sie mit dem Schlüsselwort **FRICTION ANGLE OF THE SEDIMENT**.
```

(gaia-secondary)=
### Sekundärströme

Secondary currents may occur in curved channels (i.e., in most near-census natural rivers) where water moves like a gyroscope through river bends. More specifically, secondary flows are helical motions in which water near the surface is driven toward the outer bend, while water near the riverbed is driven toward the inner bend. Thus, secondary flows are a 3d phenomenon that can be represented in 2d models only with auxiliary approaches. For {term}`Bedload` transport, the near-bed current toward the inner bend is especially important, because it promotes erosion at the outer bend and may lead to deposition at the inner bend.

By default, Telemac2d and Gaia do not consider secondary currents, but an approach based on {cite:t}`engelund1974` can be enabled by setting the **SECONDARY CURRENTS** keyword to `YES` (default is `NO`). In Gaia, the spiral flow coefficient $A$ is set to 7 (Engelund's value). The **SECONDARY CURRENTS ALPHA COEFFICIENT** keyword can be used to modify this coefficient as a function of channel bottom roughness:

* `SECONDARY CURRENTS ALPHA COEFFICIENT : 0.75` für ein sehr raues Flussbett
* `SECONDARY CURRENTS ALPHA COEFFICIENT : 1.0` für ein glattes Flussbett (**Standard**)

Für **dieses Tutorial verwenden**:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SECONDARY CURRENTS : YES
SECONDARY CURRENTS ALPHA COEFFICIENT : 0.8
```

(gaia-bc-bl)=
## Grenzbedingungen

The {ref}`Gaia Basis section on boundary conditions <gaia-bc>` explains the geometric definition of open liquid boundaries in the `*.cli` files. To prescribe a bedload transport of **10 kg$\cdot$s$^{-1}$** (total solid discharge without pores) across the upstream (`LIEBOR=5`) boundary and free outflow at the downstream (`LIEBOR=4`) boundary, **add the PRESCRIBED SOLID DISCHARGES keyword to the Gaia steering file (gaia-morphodynamics.cas)**:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
PRESCRIBED SOLID DISCHARGES : 10.;0.
```

Recall that the first and second values in the list of prescribed solid discharges refer to the first and second open boundary listed in the `boundaries-gaia.cli`, respectively (i.e., upstream and downstream in that order).

```{admonition} Units for PRESCRIBED SOLID DISCHARGES
:class: important
Das Schlüsselwort **PRESCRIBED SOLID DISCHARGES** gibt den gesamten Feststoffaustrag in **kg/s** (Masse pro Zeit, nicht pro Einheitsbreite) an. Dies ist der Trockenmassenfluss ohne Berücksichtigung der Poren. Wenn ein Wert über dieses Schlüsselwort angegeben wird, dient die Spalte `Q2BOR` in der Randbedingungen-Datei nur als Profilform (Werte sollten für ein konstantes Profil > 0 sein, typischerweise auf 1.0 festgelegt).
```

```{admonition} Distributing solid discharge among sediment classes
:class: tip
Wenn mehrere Sedimentklassen definiert sind, kann der Feststoffaustrag mit dem Schlüsselwort **CLASSES IMPOSED SOLID DISCHARGES DISTRIBUTION** unter ihnen verteilt werden (Sequenz der reellen Werte, getrennt durch Semikolone, einer pro Klasse, summiert sich auf 1,0). Wenn dieses Schlüsselwort nicht verwendet wird, wird die Entladung entsprechend den von Gaia berechneten Sandverhältnissen verteilt.
```

Gaia can be run with liquid boundary files for assigning time-dependent solid discharges (the outflow should be kept in equilibrium). Solid discharge time series can be implemented using `455`-`5` boundary definitions, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. For more guidance, have a look at the *yen-2d* example (`telemac/examples/gaia/yen-2d`) featuring a quasi-steady bedload simulation at the Rhine River. In addition, more background information about the definition of bedload boundary conditions can be found in sections 3.1.10-3.1.12 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

## Beispielanträge

Examples for the implementation of bedload come along with the TELEMAC installation (in the `/telemac/examples/gaia/` directory). The following examples in the `gaia/` folder feature (pure) bedload calculations:

* Anwendung des {ref}`Wilcock-Crowe formula <gaia-wilcock>` (mehrere Sedimentklassen): **wilcock crowe-t2d/**
* Bettlast in einem Bogen des Rheins mit quasi stetigen (unruhigen) Strömungsverhältnissen: **yen-2d/**
* Geschiebetransport gekoppelt mit Telemac3d: **bosse-t3d/**
* Modell eines gepanzerten (schichteten) Flussbettes: **guenter-t2d/**
* Küstensandtransport in Verbindung mit dem Wellenausbreitungsmodul Tomawac: **littoral-t2d-tom/**
* Kupplung mit dem Baggermodul Nestor: **nestor dig test-t2d/**
* Finite Volume Solver mit zeitabhängiger Feststoffentladung in einem `*.liq`: **flume bc-t2d/**