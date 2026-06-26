---
description: Konfigurieren Sie den Sedimenttransport in TELEMAC-GAIA unter Verwendung von Meyer-Peter und Müller-Formel, Shields-Parameter und dimensionslose Bettscherspannung für die 2D morphodynamische Flussmodellierung.
---

(gaia-bl)=
# Belastbarkeit


```{admonition} Bedload basics
:class: important

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/e6lk2pk72Gc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Bedload traveling in a lab flume by jumping, rolling, and sliding (under water footage). Source: Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


For a better learning experience, the {ref}`glossary` helps with explanations of the terms {term}`Sediment transport`, (dimensionless) {term}`bedload <Bedload>` transport $\Phi_b$, {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` $\tau_{x}$, and the {term}`Shields parameter` $\tau_{x,cr}$ (in this order).
```

```{admonition} Sediment replenishment, gravel augmentation, bedload addition (etc.)
:class: tip

Die Platzierung von gröberem Sediment für die Restaurierung des Bettlasttransports kann viele verschiedene Formen annehmen und wird durch eine breite Palette von Begriffen beschrieben. In TELEMAC ist die beste Option zur Simulation solcher Geschiebetransport-Restaurierungsbemühungen das Modul [**Nestor**](http://www.opentelemac.org/index.php/modules-list/163-dredgesim-modeling-dredging-operations-in-the-river-bed), das Gaia (oder SISYPHE) benötigt. Lesen Sie mehr in den letzten [Nestor manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/nestor/user/nestor_user_9.0.pdf).
```

(bl-principles)=
## Grundsätze

Die Berechnung des {term}`bedload <Bedload>`-Transports erfordert Expertenwissen über das modellierte Ökosystem, um zu beurteilen, ob das System Sedimentversorgungs-begrenzt oder Transportkapazität-begrenzt {cite:p}`church_morphodynamics_2015` ist.

Sediment-Zubehör Flüsse
: Ein absatzbegrenzter Fluss zeichnet sich durch deutlich sichtbare Inzisionstrends aus, die darauf hindeuten, dass der Fluss möglicherweise mehr Sediment transportieren könnte als im Fluss vorhanden ist. Sediment-supply begrenzte Flussabschnitte treten typischerweise stromabwärts von Staudämmen auf, die eine unüberwindbare Barriere für Sediment darstellen. So ist in einem versorgungsbegrenzten Fluss die **-Flow-Kompetenz** (hydrodynamische Kraft oder ** Transportkapazität**) nicht ausreichend, um ein typischerweise grobes Flussbett zu mobilisieren, sondern ausreichend für den Transport von externer Sedimentversorgung.

Transportkapazitätsbegrenzte (alluviale) Flüsse
: Ein verkehrskapazitätsbegrenzter Fluss zeichnet sich durch Sedimentreichtum aus, wo der Fluss zu klein ist, um alle verfügbaren Sedimente während einer Flut zu transportieren. Sedimentakkumulationen (d.h. das Alluvium) sind vorhanden und der Kanal neigt dazu, in {term}`anabranches <Anabranch>` zu fliehen (oder in feinen/sand dominierten Umgebungen anastomose). Die **Flow-Kompetenz* (bzw. ** Transportkapazität**) reicht also nicht aus, um die gesamte Menge an verfügbarem Sediment (externe Versorgung und Flussbett) zu transportieren.

```{admonition} Limitation types vary in space and in time
:class: important
Die Kanaltypen können im Raum zwischen Flussabschnitten oder Segmenten und in der Zeit stark variieren. So kann beispielsweise derselbe Flussabschnitt, der aufgrund unzureichender Fließfähigkeit zu versorgen scheint, während einer Überschwemmung zu einem Transportkapazitätsbegrenzten Abschnitt werden, wenn hohe Entladungen hohe Schubspannungen auf dem Flussbett ausüben. Die spatio-temporale Variation der Transportbegrenzungstypen ist besonders ausgeprägt in Nah-Census, gesunden Flussökosystemen, die sich ständig an ein morphodynamisches Gleichgewicht anpassen.
```

Die folgenden Zahlen illustrieren die Sedimentversorgung begrenzten Fluss erreicht und eine Transportkapazität begrenzten Fluss erreichen.

`````{tab-set}
````{tab-item} Artificially sediment supply-limited
```{figure} ../../img/nature/doubs-capacity-2015.JPG
:height: 350px
:alt: channel doubs france sediment supply transport limited
:name: doubs-2015

Die Doubs in der Franche-Comté (Frankreich) während einer kleinen Flut. Die Sedimentzufuhr wird durch eine Staudämmkaskade vorgeschaltet mit der Folge eines geraden monotonen Kanals mit erheblichem Pflanzenwachstum entlang der Banken unterbrochen. Das Flussbett besteht in erster Linie aus Bouldern, die die meiste Zeit immobil sind. So kann der Flussabschnitt als künstlich sedimentation limitiert charakterisiert werden (Bild: Sebastian Schwindt 2015).
```
````

````{tab-item} Naturally sediment supply-limited
```{figure} ../../img/nature/krimmler-ache-2010.jpg
:height: 350px
:alt: naturally channel krimmler ache austria sediment supply transport limited
:name: krimml-2010
:class: with-shadow

Die Krimmler Ache in Österreich während einer kleinen Flutveranstaltung. Auch wenn das Wasserbad eine hohe {term}`Sediment yield` hat, ist die Transportkapazität des Wassers in diesem Flussabschnitt so hoch, dass das Flussbett überwiegend aus großen Bouldern besteht. So kann der Flussabschnitt als natürlicher Sedimentversorgungsbegrenzt charakterisiert werden (Bild: Sebastian Schwindt 2010).
```
````

````{tab-item} Capacity-limited
```{figure} ../../img/nature/jenbach-alluvial-2020.jpg
:height: 350px
:alt: alluvial channel jenbach sediment supply transport limited
:name: jenbach-2020

Der Jenbach in den Bayerischen Alpen (Deutschland) nach einer intensiven natürlichen Sedimentversorgung in stromaufwärts gelegener Reichweite in Form eines Erdrutsches. Der Flussabschnitt kann als Transportkapazität begrenzt gekennzeichnet werden (Bild: Sebastian Schwindt 2020).
```
````
`````

**Warum ist die Differenzierung zwischen Sedimentversorgung und Transportkapazität begrenzten Flüssen wichtig für die numerische Modellierung?*

Gaia bietet verschiedene Formeln für die Berechnung des Bettlasttransports, die teilweise entweder aus Laborexperimenten mit unendlicher Sedimentversorgung abgeleitet werden (z.B. die {cite:t}`meyer-peter_formulas_1948`-Formel und deren Derivate, siehe {ref}`below <gaia-mpm>`) oder aus Feldmessungen in teilbelasteten Flüssen (z.B. {cite:t}`wilcock_critical_1993`). Die Formel, die für eine begrenzte Sedimentversorgung verantwortlich ist, beinhaltet oft einen Korrekturfaktor für die {term}`Shields parameter`.

## Formeln und Parameter

{term}`Bedload` is typically designated with $q_b$ (in kg$\cdot$s$^{-1}\cdot$m$^{-1}$ i.e. weight per unit time and width) and accounts for particulate transport in the form of the displacement of rolling, sliding, and/or jumping coarse particles. In river hydraulics, the so-called {term}`Dimensionless bed shear stress`, also referred to as {term}`Shields parameter` {cite:p}`shields_anwendung_1936`, is often used as a threshold value for the mobilization of sediment from the riverbed. TELEMAC and Gaia build on a dimensionless expression of bedload transport intensity according to {cite:t}`einstein_bed-load_1950`:

$$
\Phi_b = \frac{q_b}{\rho_{s} \sqrt{(s - 1) g D^{3}_{pq}}}
$$ (eq-phi-gaia)

wobei $\rho_{s}$ die Dichte der Sedimentkörner ist; $s$ ist das Verhältnis von Sedimentkorn und Wasserdichte (typischerweise 2.68) {cite:p}`schwindt_hydro-morphological_2017`; $g$ ist Schwerkraftbeschleunigung; und $D_{pq}$ ist der charakteristische Korndurchmesser der Sedimentklasse (vgl. {ref}`gaia-sed`). Beachten Sie, dass der dimensionslose Ausdruck $\Phi$ und der dimensionale Ausdruck $q_{b}$ die Einzelbettlast darstellen (d.h. die durch eine Breiteneinheit normalisierte Bettlast). **Gaia-Ausgänge sind dimensional und entsprechen $q_{b}$** (Recall the **VARIABLES FOR GRAPHIC PRINTOUTS* Definitionen in der {ref}`General Parameters section <gaia-gen>`), wobei die Breiteneinheit der Kantenlänge einer numerischen Maschenzelle entspricht, über die die Massenflüsse berechnet werden.

```{admonition} Gaia computes bedload in mass transport rate
:class: note
Im Gegensatz zu SISYPHE berechnet Gaia Bettlastflüsse in Bezug auf (trockene) Massentransportrate pro Stückbreite ohne Poren. Die numerische Berechnung von Sedimentflüssen hinsichtlich Trockenmasse minimiert den Abrundungsfehler, insbesondere für die für das Bettschichtmodell verwendeten Massentransferalgorithmen.
```

```{admonition} Comment on the Original Einstein (1950) Expression
:class: dropdown
Die ursprüngliche Gleichung für $\Phi_b$ finden Sie auf Seite 34 (Equation 42) in {cite:t}`einstein_bed-load_1950`. Diese Formel beinhaltet eine zusätzliche Division durch die Gravitationsbeschleunigung $g$, die nicht in späteren Verweisen auf den Einstein-Ausdruck von $\Phi_b$ erscheint und auch nicht zu einem dimensionslosen Begriff führen würde. Aus diesem Grund wird hier Equation {eq}`eq-phi-gaia` adaptiert.
```

Equation {eq}`eq-phi-gaia` drückt nur die Maßumwandlung für den Bettlasttransport aus (d.h. die Art, wie die Abmessungen entfernt oder dem Sedimenttransport hinzugefügt werden). Tatsächlich ist dies nur der erste Schritt, um die andere Seite einer Bettlastgleichung mit einer (semi-) empirischen Formel zu lösen. Um $\Phi_{b}$ zu berechnen, bietet Gaia eine Reihe von (semi-) empirischen Formeln, die mit Benutzer Fortran-Dateien modifiziert werden können und in der Gaia-Lenkungsdatei mit dem **BED-LOAD TRANSPORT FORMULA FÜR ALL SANDS* `integer`keyword definiert werden können. {numref}`Table %s <tab-gaia-bl-formulae>` listet mögliche ganze Zahlen für das Keyword auf, um eine Bettlast-Transport-Formel zu definieren, einschließlich Referenzen auf Original-Publikationen, Formel-Anwendungsbereiche und die Namen der Fortran-Quellen-Dateien für Modifikationen.

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

**Anmerkung**, dass die Engelund-Hansen-Formel (Optionen `3` und `30`) den gesamten Sedimenttransport*, d.h. die Summe der Beladung und der Schwebelastung berechnen. Aktivieren Sie also bei der Verwendung dieser Formeln nicht zusätzlich suspendierte Lastmodellierung, um Doppelzählungen zu vermeiden.

Um in diesem Tutorial die {cite:t}`meyer-peter_formulas_1948` Formel (`1` laut {numref}`Tab. %s <tab-gaia-bl-formulae>`) zu verwenden, ** die folgende Zeile an die gaia-morphdynamics.cas-Lenkdatei*:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
/
BED LOAD FOR ALL SANDS : YES / deactivate with NO
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1
```

Die folgenden Abschnitte geben nähere Angaben darüber, wie $\Phi_{b}$ mit den in {numref}`Tab. %s <tab-gaia-bl-formulae>` genannten vordefinierten Formeln berechnet wird.

```{admonition} User-defined Bedload transport formulae in a specific Fortran file
:class: tip
Benutzer können mehr Bettladung Transport Formeln hinzufügen, indem eine geänderte Kopie einer FORTRAN-Dateivorlage hinzugefügt wird. Die [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)] erläutert das Verfahren zum Hinzufügen einer neuen benutzerdefinierten Beladungsformel im Detail in Abschnitt 6.3.
```

```{admonition} User Fortran Files
:class: note, dropdown
Um eine Benutzer-Fortran-Datei zu implementieren, kopieren Sie die ursprüngliche TELEMAC Fortran-Datei aus dem `/telemac/sources/`-Verzeichnis (z.B. `/telemac/sources/gaia/bedload_einst.f`) in das Projektverzeichnis (z.B. `/telemac/simulations/gaia-tutorial/user_fortran/bedload_einst.f`). Sagen Sie TELEMAC, wo Sie nach Benutzer-Fortran-Dateien suchen, indem Sie das folgende Schlüsselwort in einer Lenkdatei definieren (z.B. in `gaia-morphodynamics.cas`):

`FORTRAN FILE : 'user_fortran'`
```

(gaia-mpm)=
### Meyer-Peter und Müller (1948)

```{admonition} Recall the validity range for the MPM formula (1)
:class: warning
Übersetzen Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass die Anwendung in dem anwendbaren Parameterbereich liegt, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde.
```

Die {cite:t}`meyer-peter_formulas_1948` Formel wurde 1948 von Schweizer Forschern Eugen Meyer-Peter, Professor an [ETH Zurich](https://ethz.ch/en.html) und Gründer des Hydrauliklabors der Schule (Zurichs berühmtes [VAW](https://vaw.ethz.ch/)] und Robert Müller, veröffentlicht. Ihre empirische Formel ist das Ergebnis von mehr als einem Jahrzehnt der Zusammenarbeit und die Ausarbeitung begann ein Jahr nach der Gründung des VAW 1931, als Robert Müller zum Assistenten von Eugen Meyer-Peter ernannt wurde. Die beiden Wissenschaftler arbeiteten auch mit Henry Favre und Hans-Albert Einstein zusammen, die mit einem anderen Ansatz zur Berechnung der Bettlast auftraten. Eine frühe Version der {cite:t}`meyer-peter_formulas_1948` Formel wurde 1934 veröffentlicht und ist die Grundlage für viele andere Formeln, die sich auf eine kritische {term}`Dimensionless bed shear stress` (d.h. {term}`Shields parameter`) beziehen. Es ist wichtig zu beachten, dass die Formel auf Daten von Labor-Flume-Experimenten mit hoher Sedimentversorgung basiert. Aus diesem Grund entspricht der mit der Formel {cite:t}`meyer-peter_formulas_1948` berechnete Ladungstransport dem {ref}`hydraulic transport capacity <bl-principles>` eines Alluvialkanals. **Die {cite:t}`meyer-peter_formulas_1948`-Formel neigt dazu, den Beladungstransport** zu überschätzen und ist inhärent für die Schätzung der Beladung ** auf Basis vereinfachter 1d-querschnittsgemittelter Hydraulik** (siehe auch die {ref}`Python sediment transport exercise <ex-py-sediment>`). Gute Ergebnisse können erwartet werden, wenn Flutflüsse in einem alluvialen Flussabschnitt simuliert werden.

Letztlich kann die linke Seite von Equation {eq}`eq-phi-gaia` ($\Phi_b$) mit der Formel {cite:t}`meyer-peter_formulas_1948` wie folgt berechnet werden:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x,cr} > \tau_{x} \\ f_{mpm} \cdot (\tau_{x} - \tau_{x,cr})^{3/2} & \mbox{ if } \tau_{x,cr} \leq \tau_{x}\end{cases}
$$ (eq-mpm)

wobei $f_{mpm}$ der MPM-Koeffizient ist (Standard 8), $\tau_{x,cr}$ die {term}`Shields parameter` ($\approx$ 0,047 und bis zu 0,07 in Bergflüssen) und $\tau_{x}$ die {term}`Dimensionless bed shear stress` ist. Bei der Verwendung der Formel {cite:t}`meyer-peter_formulas_1948` mit Gaia ist die Konsistenz mit Originalveröffentlichungen ** versichert durch die Definition von $\tau_{x,cr}$ und $f_{mpm}$ in der Steuerdatei*:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1 / see above
CLASSES SHIELDS PARAMETERS : 0.047;0.047;0.047
MPM COEFFICIENT : 8
```

````{admonition} Wong-Parker correction of the MPM formula
Die Wong-Parker {cite:p}`wong_reanalysis_2006`-Korrektur für die {cite:t}`meyer-peter_formulas_1948`-Formel bezieht sich auf eine statistische Neuanalyse der ursprünglichen Versuchsdatensätze und gilt für {term}`Plane bed`-Flussabschnitte. Zu diesem Zweck liefert die Wong-Parker-Korrektur niedrigere Bettlasttransportwerte und schließt die Form Drag-Korrektur der ursprünglichen Formel mit folgendem Ausdruck aus: $\Phi_{b} \approx 3.97 \cdot (\tau_{x} - 0.0495)^{3/2}$. So verwenden Sie die Wong-Parker-Korrektur in Gaia:

```fortran
CLASSES SHIELDS PARAMETERS : 0.0495;0.0495;0.0495
MPM COEFFICIENT : 3.97
```
````

**Um das Tutorial direkt mit der {cite:t}`meyer-peter_formulas_1948`-Formel fortzusetzen, springen Sie auf den {ref}`correction factors <c-factors>`-Bereich.**

(gaia-einstein)=
### Einstein-Brown (1942/49)

```{admonition} Recall the validity range for the Einstein-Brown formula (2)
:class: warning
Übersetzen Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass die Anwendung in dem anwendbaren Parameterbereich liegt, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde.
```

Hans Albert Einstein, Sohn des berühmten Albert Einstein, war Pionier der Wahrscheinlichkeitsanalyse des Sedimenttransports. Insbesondere er unterschätzt, dass der Beginn und das Ende der Sedimentbewegung in Bezug auf Wahrscheinlichkeiten ausgedrückt werden können. Ferner sei Einstein davon ausgegangen, dass die Sedimentbewegung eine Reihe von stufenweisen Verschiebungen mit anschließenden Ruhezeiten ist und dass der mittlere Abstand einer Partikelverlagerung etwa das hundertfache des Partikel- (Granin)-Durchmessers beträgt. Um den Beobachtungen Rechnung zu tragen, die er in Labor-Folge-Experimenten gemacht hat, führte Einstein Versteck- und Hebekorrekturkoeffizienten {cite:p}`einstein1942` ein.

Die Einstein-Formel unterscheidet sich von jeder {cite:t}`meyer-peter_formulas_1948`-basierten Formel, indem sie keine Schwelle für die beginnende Bewegung von Sediment bedeutet. Trotz oder weil Einsteins Sedimenttransport-Theorie komplexer ist als viele andere Bettlast-Transport-Formeln, wurde es in Engineering-Anwendungen nicht sehr beliebt. Heute ermöglicht Gaia die benutzerfreundliche Anwendung von Einsteins Formel, die ebenfalls 1949 von {cite:t}`brown1949` an einer technischen hydraulischen Konferenz präsentiert wurde. Laut {cite:t}`einstein1942`-{cite:t}`brown1949` wird die linke Seite von Equation{eq}`eq-phi-gaia` ($\Phi_b$) wie folgt berechnet:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x} < 0.0025 \\ F_{eb}\cdot 2.15 \cdot \exp{(-0.391/\tau_{x})} & \mbox{ if } 0.0025 \leq \tau_{x} \leq 0.2\\ F_{eb} \cdot  40 \cdot \tau_{x}^{3} & \mbox{ if } \tau_{x} > 0.2\end{cases}
$$ (eq-einstein-brown)

wenn

$$
F_{eb} = \left(\frac{2}{3} + \frac{36}{D_x}\right)^{0.5} - \left(\frac{36}{D_x}\right)^{0.5}
$$ (eq-f-eb)

$D_x$ ist der dimensionslose Teilchendurchmesser, berechnet als:

$$
D_x = \left[\frac{(s-1)\cdot g}{\nu^2}\right]^{1/3}\cdot D_{pq}
$$ (eq-d-dimless)

where $s$ is the ratio of sediment grain and water density (typically 2.68); $g$ is gravitational acceleration; and $\nu$ is the kinematic viscosity of water ($\approx$10$^{-6}$m$^{2}$ s$^{-1}$) {cite:p}`schwindt_hydro-morphological_2017`.

Um die {cite:t}`einstein1942`-{cite:t}`brown1949`-Formel in Gaia zu verwenden:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 2
```

```{admonition} Consider adapting bedload_einst.f
Die Bewerbungsschwellen in Abhängigkeit von $\tau_{x}$ stammen aus der Gaia Fortran-Datei `bedload_einst.f` in `/telemac/sources/gaia/`. Die ursprÃ1⁄4nglichen {cite:t}`einstein1942`-{cite:t}`brown1949`publikationen schlagen jedoch eine Schwelle von $\tau_{x}$=0.182 (anstatt 0,2) fÃ1⁄4r die Umschaltung der Formelfälle vor.
```


(gaia-engelund)=
### Engelund-Hansen (1967)

```{admonition} Recall the validity range for the Engelund-Hansen formulae (3 and 30)
:class: warning
Übersetzen Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass die Anwendung in dem anwendbaren Parameterbereich liegt, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde. Beachten Sie, dass diese Formeln den gesamten Sedimenttransport** (Bettlast + Schwebelastung) berechnen.
```

Die {cite:t}`engelund_monograph_1967`-Formel entspricht dem gesamten Sedimenttransport einschließlich {term}`Bedload` und {term}`Suspended load`. Ausgehend vom Bagnold Power-Aproach {cite:p}`bagnold_approach_1966,bagnold_empirical_1980` wurde die {cite:t}`engelund_monograph_1967` Formel für Sedimenttransportberechnungen über Dünenkanalbetten entwickelt. Der Ansatz führt zu Energieverlusten, die erforderlich sind, um Partikel auf Dünen des Flussbettes bergauf zu fahren. Die {cite:t}`bagnold_approach_1966` Theorie betrachtet die Gesamtschere als die Summe der zwischen den Körnern und der Flüssigkeit übertragenen Schere und die durch Impulsänderungen durch intergranuläre Kollisionen verursachte Scherung. So erfolgt die Erosion, solange die {term}`Dimensionless bed shear stress` ihren kritischen Wert (d.h. die {term}`Shields parameter`) größer oder gleich ist. Gaia implementiert die {cite:t}`engelund_monograph_1967` durch Berechnung der linken Seite von Equation{eq}`eq-phi-gaia` ($\Phi_b$) wie folgt:

$$
\Phi_b = 0.1\cdot \frac{\tau_{x}^{2.5}}{c_f}
$$ (eq-engelund)

wobei $c_f$ ein adimensionaler Reibungskoeffizient ist und $\tau_x$ die Schildnummer ohne den Hautreibungskorrekturfaktor ist. Lesen Sie mehr über Hautreibung im Abschnitt {ref}`correction factors <c-friction>`. Um die ursprüngliche {cite:t}`engelund_monograph_1967` Formel in Gaia verwenden:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 30
```

Darüber hinaus hat {cite:t}`chollet1979` für die Berechnung eines modifizierten Shields-Parameters $\tau^*_x$ eine schrittweise Funktion eingeführt, die für verschiedene Transportregime gilt:

$$
\tau^*_x = \begin{cases} 0 & \mbox{ if } \tau_{x} \leq 0.06 & \mbox{ (no transport)}\\ [2.5 (\tau_{x} - 0.06)]^{0.5} & \mbox{ if } 0.06 < \tau_{x} < 0.384  & \mbox{ (dune regime)} \\ 1.066\cdot \tau_{x}^{0.176} & \mbox{ if } 0.384 < \tau_{x} < 1.08  & \mbox{ (transition regime)} \\ \tau_{x} & \mbox{ if } 1.08 \leq \tau_{x}  & \mbox{ (sheet flow)} \end{cases}
$$ (eq-f-eh)

Für die Anwendung der {cite:t}`chollet1979`-Änderung der {cite:t}`engelund_monograph_1967`Formel:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 3
```

(gaia-rijn)=
### (1984)

```{admonition} Recall the validity range for the van-Rijn formula (7)
:class: warning
Übersetzen Sie {numref}`Tab. %s <tab-gaia-bl-formulae>`, um sicherzustellen, dass die Anwendung in dem anwendbaren Parameterbereich liegt, der den Bedingungen entspricht, unter denen die Formel entwickelt wurde.
```

Die Sedimenttransportformel von Leo van Rijn {cite:p}`van_rijn_sediment_1984` ist inspiriert von den Theorien von {cite:t}`bagnold_empirical_1980`, {cite:t}`einstein1942` und {cite:t}`ackers_sediment_1973`. Die {cite:t}`van_rijn_sediment_1984` Formeln gehen davon aus, dass die Bettlast von der Schwerkraft dominiert wird, während der hängende Lasttransport durch Turbulenz nach {cite:t}`bagnold_empirical_1980` gesteuert wird. Zu diesem Zweck berechnen die {cite:t}`van_rijn_sediment_1984` Formeln Bettlasttransport ähnlich {cite:t}`ackers_sediment_1973`, wo die Transportraten von Reibungsgeschwindigkeiten abhängen. Um sein Nahbett (Bettlast)-Festtransportmodell zu kalibrieren, nutzte {cite:t}`van_rijn_sediment_1984` Daten aus Experimenten auf Flachbett (Null-Slope) Kanälen mit einem durchschnittlichen Sedimentkorndurchmesser von 1,8 mm. {cite:t}`van_rijn_sediment_1984` hat weitere Experimente durchgeführt, um die Ergebnisse seines Modells gegen unterschiedliche Korndurchmesser zwischen 0,2 und 2 mm zu verwerten. Darüber hinaus wurden {cite:t}`van_rijn_sediment_1984` Kriterien für die Sedimentsuspension anhand von Laborexperimenten mit Korndurchmessern von weniger als 0,5 mm festgelegt und die Kalibrierparameter empirisch vereinfacht. Während die ursprüngliche Formel {cite:t}`van_rijn_sediment_1984` für den gesamten Sedimenttransport (d.h. {term}`Bedload` und {term}`Suspended load`) gilt, sind die folgenden Erläuterungen zur Umsetzung in Gaia nur auf{term}`Bedload` beschränkt.

Nach {cite:t}`van_rijn_sediment_1984` wird die linke Seite der Gleichung {eq}`eq-phi-gaia` ($\Phi_b$) wie folgt berechnet:

$$
\Phi_b = \frac{0.053}{D_{x}^{0.3}} \cdot \left(\frac{\tau_{x} - \tau_{x,cr}}{\tau_{x,cr}}\right)^{2.1}
$$ (eq-rijn)

Explanations of the {term}`Dimensionless bed shear stress` $\tau_{x}$, its critical value $\tau_{x,cr}$ (i.e., the {term}`Shields parameter`), and the dimensionless grain diameter $D_{x}$ are provided in the above sections on the {ref}`Meyer-Peter and Müller <gaia-mpm>` and the {ref}`Einstein-Brown <gaia-einstein>` formulae.

Um die {cite:t}`van_rijn_sediment_1984` Formel in Gaia verwenden:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 7
```

(gaia-wilcock)=
### Wilcock-Crowe (2003)

```{admonition} Applicability of the Wilcock-Crowe formula (10)
:class: warning
Die multifraktionierte Bettlast-Transportformel von {cite:t}`wilcock2003` gibt keine besonderen Gültigkeitsbereiche an, aber die Autoren schränken ihren Ansatz auf Sand-Griff-Kiesel-Sedimente mit einem minimalen Korndurchmesser von 0,063 mm ein. Die Erläuterungen in diesem Abschnitt beschränken sich auf den Anwendungshintergrund des {cite:t}`wilcock2003`-Ansatzes. Der komplexe Satz von Gleichungen wird im Detail in der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) (Abschnitt 3.1.2) und {cite:t}`cordier2019,cordier2020` erläutert.
```

Der {cite:t}`wilcock2003`-Ansatz ist ein multifraktioniertes Sedimenttransportmodell, das vor allem in gepanzerten Flussabschnitten zur Modellierung von Bettabbau oder Abbau eingesetzt wird. Das Modell basiert auf Oberflächenuntersuchungen und ist besonders für die Vorhersage von transienten Bedingungen der Bettpanzerung angepasst. Es betrachtet die gesamte Größenverteilung der Bettoberfläche (von feinsten Sanden bis zu grobsten Kies) und wurde mit insgesamt 49 Flumexperimenten mit kleinen bis hohen Wasserableitungen und fünf verschiedenen Sedimentmischungen kalibriert.

The approach takes up the idea of {cite:t}`parker1990` on applying a reference shear stress at which little but constant solid transport rate can be observed. The reference shear stress is close to, but a little bit larger than the {term}`Shields parameter` $\tau_{x,cr}$. To this end, {cite:t}`wilcock2003` implement a reference transport rate of 0.002 as proposed by {cite:t}`parker1990`.

Darüber hinaus verwendet das Multifraktionsmodell {cite:t}`wilcock2003` die komplette Sedimentkorngrößenverteilung der Flussbettoberfläche und berechnet den Bettlasttransport für jede der angegebenen Korngrößenklassen. Das Sedimenttransportmodell baut auf Flume-Experimenten von {cite:t}`proffitt1983` und {cite:t}`parker1990` auf, die in Abhängigkeit von der Sandfraktion im Flussbett versteckt/exponiert werden. Die Versteck-Exposure-Funktion wurde entwickelt, um Diskrepanzen, die vor früheren Experimenten beobachtet wurden, zu lösen, einschließlich der Versteck-Exposure-Effekt von Sandgehalt auf Kiestransport für schwache bis hohe Sandgehalte in der Schüttung.

Das {cite:t}`wilcock2003`-Modell stellt eine Weiterentwicklung der {cite:t}`meyer-peter_formulas_1948`-Formel dar, übernimmt die Implementierung einer Referenz-Transportrate {cite:p}`parker1990` und es ist kalibriert, um Effekte in Abhängigkeit von der Sandfraktion zu verbergen/exponieren.

Um die {cite:t}`wilcock2003` Formel in Gaia zu verwenden, definieren Sie mehrere {ref}`sediment classes <gaia-sed>` und verwenden Sie:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 10
```

(c-factors)=
## Korrekturfaktoren

Korrekturfaktoren für den Sedimenttransport sind erforderlich, um die transversale Kanalneigung, Sekundärströme oder die Hautreibungskorrektur zu berücksichtigen.

(c-friction)=
### Friction Correctors

Friktion wird oft mit vereinfachten Ansätzen betrachtet, die die Hautreibung und den Formwiderstand zusammenklumpen, aber in einem zweidimensionalen Modell wirkt nur die Hautreibung auf die Bettlast. {cite:t}`einstein_bed-load_1950` Konten für Hautreibung mit einem Korrekturfaktor $\mu$ für (dimensionale) Bettscherspannung $\tau$:

$$
\tau' = \mu \cdot \tau
$$ (eq-tau-fr)

```{admonition} How Telemac2d calculates $\tau$
Telemac2d uses the length of the $x$-$y$ velocity vectors to calculate $\tau$ with the user-defined `FRICTION COEFFICIENT` $c_{f}$: $\tau = 0.5\cdot \rho_{w}\cdot c_{f}\cdot (U^2 + V^2)$.
```

Der Korrekturfaktor $\mu$ ist definiert als das Verhältnis des Hautreibungskoeffizienten $c'_{f}$ und des globalen Reibungskoeffizienten $c_{f}$ (d.h. klumpige Hautreibung und Formwiderstand):

$$
\mu = \frac{c'_{f}}{c_{f}}
$$ (eq-f-fr)

Der Hautreibungskoeffizient wird berechnet als:

$$
c'_{f} = 2\cdot \left(\frac{\kappa}{\log(12 h/ k'_{s})}\right)^{2}
$$ (eq-cf-skin)

wobei $\kappa$ die {cite:t}`von_karman_mechanische_1930` Konstante (0.4), $h$ Wassertiefe ist und $k'_{s}$ die repräsentative Rauheitslänge berechnet als $k'_s = \alpha_{ks} \cdot D_{50}$ ist, wobei $\alpha_{ks}$ ein Kalibrierparameter ist (weitere Informationen finden Sie unter {ref}`bedload calibration <bl-calibration>`).

`````{tab-set}
````{tab-item} Skin Friction
Gaia verwendet standardmäßig den Hautreibungskorrekturkoeffizienten, den er vom hydrodynamischen Solvens (d.h. Telemac2d/3d) ableitet. In sehr flachen Gewässern könnte dieses Verhalten Instabilitäten verursachen. Daher kann das **SKIN FRICTION CORRECTION** Keyword in Gaia zur Steuerung der Korrekturfaktorberechnung eingestellt werden:

* `0`: Deaktiviert Korrektur, Einstellung $\mu = 1$ (Gesamtbettscherbeanspruchung der Hydrodynamik wird direkt verwendet)
* `1`: ermöglicht die Korrektur der Hautreibung (**default**), Computing $\mu$ nach Equations{eq}`eq-f-fr` und {eq}`eq-cf-skin`
* `2`: ermöglicht ein Bettform-Vorhersage, das bei der Berechnung $\mu$

Um die Reibungskorrektur der Haut zu deaktivieren (d.h. $\mu$ zu 1), fügen Sie folgendes zur Gaia-Lenkungsdatei hinzu (nicht in diesem Tutorial verwendet):

```fortran
SKIN FRICTION CORRECTION : 0 / default is 1 to enable skin friction correction
```

Der Koeffizient $\alpha_{ks}$ (Verhältnis zwischen Hautreibungsrauhigkeit und mittlerem Durchmesser) kann mit dem **RATIO BETWEEN SKIN FRICTION UND MEAN DIAMETER** Schlüsselwort (Standard: 3.0) geändert werden. Lesen Sie mehr in Abschnitt 3.1.8 der [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
````

````{tab-item} Bedform Roughness
Je feiner das Sediment des Flussbettes ist, desto wichtiger wird die durch die Bettform geschaffene Turbulenz. So ist beispielsweise die auf einem Vielfachen des Durchmessers eines Sandkorns berechnete Hautreibung $k'_{s}$ sehr klein. Sand neigt jedoch dazu, das Flussbett in rissige oder düne Formen zu formen, die zusätzliche *bedform Turbulenz* verursachen, wie im Video unten gezeigt.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/q4eRwyeLKfA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>by Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Gaia berücksichtigt standardmäßig keine Turbulenz (d.h. Rauheitseffekte) von Bettformen, kann aber durch die Einstellung des **COMPUTE BED ROUGHNESS AT SEDIMENT SCALE** Keywords an `YES` (Standard ist `NO`) aktiviert werden. Dann kann eine der folgenden Optionen für das **BED ROUGHNESS PREDICTOR OPTION** Schlüsselwort definiert werden:

* `1` für eine flache Bettannahme mit dem Standardansatz von $k_s = \alpha_{ks} \cdot D_{50}$ (modifiziert mit **RATIO BETWEEN SKIN FRICTION UND MEAN DIAMETER**).
* `2` für wellige Bettformen. Nur für Ströme ist die Welligkeit eine Funktion der Mobilitätsnummer. Für Wellen und kombinierte Wellenströme werden die Bettformmaße in Abhängigkeit von Wellenparametern nach {cite:t}`wiberg1994` berechnet.
* `3` für {cite:t}`rijn2007` Gesamtbettrauhigkeitsvorhersage (nur aktuell). Die Gesamtrauhigkeit wird in Kornrauhigkeit, kleine Rippelrauhigkeit, Mega-Reifen-Komponente und Dunrauhigkeit zersetzt.

Die [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) (Abschnitt 3.1.9) fasst den Satz von Gleichungen zusammen, die in die Berechnung des **BED ROUGHNESS PREDICTOR OPTION* gehen.

````
`````

(gaia-dir)=
### Richtung und Magnitude (Intensität)

Natural rivers are characterized by non-straight lines of the {term}`Thalweg`, which involves that water and sediment are subjected to curve effects. However, water and sediment behave differently in a curve because sediment has greater inertia than water {cite:p}`mosselman_five_2016`. Gaia accounts for the inertia of sediment transport as a function of water depth, curve radius, a spiral flow coefficient (`A`), and the depth-averaged, 2d velocities *U* and *V*. In addition, sediment transport reacts more inert to horizontal (transversal) channel slope and can be considered in $x$ and $y$ directions (see also the explanation of the {term}`Exner equation`). To this end, Gaia calculates the slope-corrected unit bedload transport $q_{b,sc}$ as follows:

$$
q_{b,sc} = q_{b} \left[1 + \beta \left(\cos \alpha  \frac{\partial z_{b}}{\partial x} + \sin \alpha \frac{\partial z_{b}}{\partial y} \right)\right]
$$ (eq-qb-corr)

wobei $\alpha$ der Winkel zwischen der Längsachse des Längskanals ($x$) und dem Beladungstransportvektor (siehe auch die {term}`Exner equation`) ist, $\beta$ ist ein empirischer Beladungsintensitätskorrekturfaktor von {cite:t}`koch1980` und $z_{b}$ die Höhe des Flussbetts.

Der Grad der Bettlastabweichung (durch $\alpha$) und der $\beta$Faktor können in Gaia mit den **FORMULA FOR DEVIATION* und **FORMULA FOR SLOPE EFFECT** (horizontale) Keywords definiert werden. Um ein oder beide Schlüsselwörter zu verwenden, muss das **SLOPE EFFECT* Schlüsselwort auf `YES` gesetzt werden (Standard ist `YES`).

Das **FORMULA FOR DEVIATION** Keyword kann folgende ganze Werte annehmen, um eine bestimmte Formel für die Sedimentformfunktion zu definieren (vgl. Abschnitt 3.1.4 in [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)):

* `1` für die Berechnung der Betthöhe nach {cite:t}`koch1980` (**default**).
* `2` for the {cite:t}`talmon1995` approach based on laboratory experiments, which should be used with the **PARAMETER FOR DEVIATION** keyword for setting the `BETA2` parameter (its default is `PARAMETER FOR DEVIATION : 0.85`, but an optimum was found with `1.6` {cite:p}`mendoza2017`).
* `3` für den {cite:t}`apsley2008bedload`-Ansatz basierend auf dem kritischen Shields-Parameter und dem Reibwinkel des Sediments, der mit dem **FRICTION ANGLE DES SEDIMENT**-Keyword (Standard ist `40.`) verwendet werden sollte.

Das **FORMULA FOR SLOPE EFFECT** Schlüsselwort betrifft nicht nur die Richtung des Sedimenttransports, sondern auch die Größe der Bettlast (oder Intensität) und kann folgende Werte annehmen:

* `1` für die Bettstandsrechnung gemäß {cite:t}`koch1980` (**default** und ähnlich FORMULA FOR DEVIATION). Das `1`-Setting ermöglicht die Definition des empirischen Neigungskorrekturfaktors $\beta$ in Equation{eq}`eq-qb-corr` durch das **BETA**-Keyword (Standard ist `BETA : 1.3`).
  - Um die Höhenlage zu erhöhen, erhöhen Sie **BETA***.
  - Um die Höhenlage zu verringern, verringern Sie **BETA***.
* `2` für die Neigungskorrektur in Sandbettflüssen auf Basis eines Ansatzes von {cite:t}`soulsby1997`, der eine Korrektur der {term}`Shields parameter` in Abhängigkeit vom Reibungswinkel des Sediments und der Flussbettneigung anwendet. Der Reibwinkel kann mit dem zusätzlichen **FRICTION ANGLE DES SEDIMENT** Schlüsselwort definiert werden (Standard ist `40.`).
* `3` für den {cite:t}`apsley2008bedload`-Ansatz, der sowohl den kritischen Shields-Parameter als auch den effektiven dimensionslosen Scherdruck modifiziert. Verwenden Sie das **FRICTION ANGLE DES SEDIMENT** Schlüsselwort.

```{admonition} Sediment sliding
:class: tip
Übersteigt die untere Steigung eine kritische Steigung (typischerweise der Ruhewinkel), können durch geomechanische Prozesse Sedimente bewegt werden. Gaia implementiert Sedimentgleiten mit dem **SDIMENT SLIDE** Schlüsselwort:
* `0`: kein Gleiten (**default**)
* `1`: einfache massenkonservative Glättung von unteren Steigungen bis zum Ruhewinkel
* `2`: avalanching formula from {cite:t}`apsley2008bedload`

Verwenden Sie das **FRICTION ANGLE DES SEDIMENT** Schlüsselwort.
```

(gaia-secondary)=
### Sekundäre Ströme

Sekundäre Ströme können in gekrümmten Kanälen (d.h. in den meisten naturnahen Flüssen) auftreten, wo sich Wasser wie ein Gyroskop durch Flussbogen bewegt. Insbesondere sind Sekundärströmungen spiralförmige Bewegungen, bei denen Wasser nahe der Oberfläche in Richtung der äußeren Biegung angetrieben wird, während Wasser nahe dem Flussbett zur inneren Biegung hin angetrieben wird. So sind Sekundärströme ein 3d-Phänomen, das nur mit Hilfsansätzen in 2d-Modellen dargestellt werden kann. Für den {term}`Bedload`-Transport ist der Nahbettstrom zur inneren Biegung besonders wichtig, weil er die Erosion an der äußeren Biegung fördert und zur Abscheidung an der inneren Biegung führen kann.

Standardmäßig betrachten Telemac2d und Gaia keine sekundären Ströme, aber ein Ansatz basierend auf {cite:t}`engelund1974` kann aktiviert werden, indem das **SECONDARY CURRENTS** Keyword auf `YES` gesetzt wird (Standard ist `NO`). In Gaia wird der Spiralflusskoeffizient $A$ auf 7 (Engelund's Wert) gesetzt. Das **SECONDARY CURRENTS ALPHA COEFFICIENT** Keyword kann verwendet werden, um diesen Koeffizienten in Abhängigkeit von Kanalbodenrauhigkeit zu ändern:

* `SECONDARY CURRENTS ALPHA COEFFICIENT : 0.75`
* `SECONDARY CURRENTS ALPHA COEFFICIENT : 1.0` für ein glattes Flussbett (**default**)

Für **dieses Tutorial*:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SECONDARY CURRENTS : YES
SECONDARY CURRENTS ALPHA COEFFICIENT : 0.8
```

(gaia-bc-bl)=
## Rahmenbedingungen

Die {ref}`Gaia Basis section on boundary conditions <gaia-bc>` erklärt die geometrische Definition offener Flüssigkeitsgrenzen in den `*.cli`-Dateien. Um einen Beladungstransport von **10 kg$\cdot$s$^{-1}$** (gesamter Feststoff ohne Poren) über die stromaufwärtige (`LIEBOR=5`) Grenze und den freien Ablauf an der stromabwärtigen (`LIEBOR=4`) Grenze zu verschreiben, **add the PRESCRIBED SOLID DISCHARGES Schlüsselwort an die Gaia Lenkdatei (gaia-morphodynamics.cas)*

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
PRESCRIBED SOLID DISCHARGES : 10.;0.
```

Beachten Sie, dass sich die ersten und zweiten Werte in der Liste der vorgeschriebenen festen Entladungen auf die in der `boundaries-gaia.cli` bzw. (d.h. stromauf und stromabwärts in dieser Reihenfolge) aufgeführte erste und zweite offene Grenze beziehen.

```{admonition} Units for PRESCRIBED SOLID DISCHARGES
:class: important
Das **PRESCRIBED SOLID DISCHARGES** Schlüsselwort gibt die vollständige Feststoffentladung in **kg/s** an (Masse pro Zeit, nicht pro Stückbreite). Dies ist der trockene Massenfluss, ohne Poren zu berücksichtigen. Wenn über dieses Keyword ein Wert angegeben wird, dient die `Q2BOR` Spalte in der Randbedingungen-Datei nur als Profilform (Werte sollten > 0 für ein konstantes Profil sein, typischerweise auf 1,0 gesetzt).
```

```{admonition} Distributing solid discharge among sediment classes
:class: tip
Wenn mehrere Sedimentklassen definiert sind, kann die Feststoffentladung unter ihnen mit dem **CLASSES IMPOSED SOLID DISCHARGES DISTRIBUTION* Keyword (Sequenz von durch Semikolonen getrennten realen Werten, eine pro Klasse, summiert auf 1.0) verteilt werden. Wird dieses Schlüsselwort nicht verwendet, wird die Entladung nach den von Gaia berechneten Sandverhältnissen verteilt.
```

Gaia can be run with liquid boundary files for assigning time-dependent solid discharges (the outflow should be kept in equilibrium). Solid discharge time series can be implemented using `455`-`5` boundary definitions, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. For more guidance, have a look at the *yen-2d* example (`telemac/examples/gaia/yen-2d`) featuring a quasi-steady bedload simulation at the Rhine River. In addition, more background information about the definition of bedload boundary conditions can be found in sections 3.1.10-3.1.12 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

## Anwendungsbeispiele

Beispiele für die Implementierung der Beladung kommen zusammen mit der TELEMAC-Installation (im `/telemac/examples/gaia/`-Verzeichnis). Die folgenden Beispiele in der `gaia/`-Ordner-Feature (pure) Bettlastberechnungen:

* Anwendung der {ref}`Wilcock-Crowe formula <gaia-wilcock>` (mehrfache Sedimentklassen): **wilcock crowet2d/*
* Beladung in einer Biegung des Rheins mit quasi stetigen (unsteady) Strömungsbedingungen: **yen-2d/**
* Beladung gekoppelt mit Telemac3d: **bosse-t3d/**
* Modell eines gepanzerten Flussbettes: **guenter-t2d/**
* Küstensand (Bettlast) Transport mit dem Wellenausbreitungsmodul Tomawac: **littoral-t2d-tom/**
* Kupplung mit dem Baggermodul Nestor: **nestor dig test-t2d/**
* Finite Volumenlöser mit zeitabhängiger Feststoffentladung in einer `*.liq`: **flume bc-t2d/*