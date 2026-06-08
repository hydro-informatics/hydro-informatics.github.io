---
description: Hydroinformatics Glossar mit Begriffen und Definitionen
---

(glossary)=
# Glossar

Dieser Abschnitt bietet einen Glossar mit technischen Bedingungen, die in diesem eBook wiederkehren. Obwohl es so erschöpfend wie möglich sein soll, könnten einige Begriffe noch nicht definiert werden.

````{glossary}
  
Advection
: Advection is the motion of particles along with the bulk flow. The properties (e.g., heat) of an advected particle or substance are conserved. Mathematically, advection of incompressible fluids (e.g., water) is described by the {term}`Continuity equation` {cite:p}`kundu_fluid_2008`.

*Französisch: Advektion<br>German: Advektion*

Anabranc
: Ein anaverzweigter Fluss (Abschnitt) zeichnet sich durch einen oder mehrere seitliche Kanäle aus, die vom Hauptflussstamm abweichen. Anabranching (oder auch anastomosing) Kanäle treten vor allem in alluvialen Kanalbetten auf, in denen mehr Sediment zur Verfügung steht als der Wasserabfluss transportieren kann (Transportkapazität begrenzte Flüsse). So hat ein anabranchinger Fluss hohe Sedimentbelastungen und die Kanalanvulsion wird wahrscheinlich bei Überschwemmungen auftreten {cite:p}`nanson_anabranching_1996,riquier_are_2017,huang_why_2007`. Dieses eBook zeigt ein Beispiel für einen anabranching Flussabschnitt im morphdynamischen Modellierungs-Tutorial in {numref}`Fig. %s <jenbach-2020>`.

*Französisch: Anabranche<br>German: Flussarm*

Anastomosing Flüsse
: Siehe {term}`Anabranch`.

ASCII
: Der American Standard Code for Information Interchange (ASCII) ist ein Kodierungsstandard für Text auf Computern. Die Entwicklung von ASCII geht zurück in die Telegrafie und wurde erstmals 1961 für das lateinische Alphabet veröffentlicht. Es wurde später durch andere Alphabete und Sonderzeichen {cite:p}`ascii1980` erweitert. ASCII-Code repräsentiert Zeichen in Form von Zahlen. Der ASCII-Code `65` steht zum Beispiel für Großbuchstaben `A` (utf-8 encoding). In Python-Anwendungen können ASCII-Codenummern durch das Alphabet (z.B. alphabetische Spaltennamen) iterieren, wobei `chr(ASCII)` in Abhängigkeit von der Systemcodierung einen Brief zurückgibt. In Python gibt z.B. `print(chr(78))` für **utf-8* encoding (Standard auf vielen Linux-Systemen) Großbuchstaben`N` zurück. Um den Kodierungstyp Ihrer Python-Installation herauszufinden, öffnen Sie ein Python-Terminal, tippen Sie auf `import sys` und `sys.getdefaultencoding()`.

Bedload
: Bedload (also referred to as *bed load*) $Q_b$ (or $q_b$ for unit bedload) in kg$\cdot$s$^{-1}$ (or kg$\cdot$s$^{-1}\cdot$m$^{-1}$) is a special type of {term}`Sediment transport` describing the displacement of coarse particles by rolling, sliding, and/or jumping on the riverbed. In river hydraulics, the so-called {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` or also referred to as {term}`Shields parameter` {cite:p}`shields_anwendung_1936` is often used as the threshold value for the mobilization of sediment from the riverbed. The dimensionless expression of bedload transport is {cite:p}`einstein_bed-load_1950`:

  $$
  \Phi_b = \frac{q_b}{\rho_{w} \sqrt{(s - 1) g D^{3}_{pq}}} \approx \frac{Q_b}{0.5\cdot(b + B)\rho_{w} \sqrt{(s - 1) g D^{3}_{pq}}}
  $$

wobei $\rho_{w}$ die Dichte des Wassers ist; $s$ ist das Verhältnis von Sedimentkorn und Wasserdichte (typischerweise 2.68) {cite:p}`schwindt_hydro-morphological_2017`; $g$ ist Schwerkraftbeschleunigung; $D_{pq}$ ist der Korndurchmesser, dessen $pq \%$ des Gemisches feiner ist; und $b$ und $B$ die Kanalboden- und Oberflächenbreite sind (oder Zellbreite/Höheight).

Lesen Sie mehr über die Berechnung der Beladung in diesem eBook in der {ref}`Python exercises <mpm>` oder der {ref}`Telemac2d-Gaia tutorial <tm-gaia>`. In numerischen Modellen wird der Beladungstransport häufig mit der {term}`Exner equation` berechnet.

  ```{image} https://github.com/Ecohydraulics/media/raw/main/png/sediment-uptake.png
  ```

Der Begriff *Traveling bedload* bezieht sich außerdem auf einen Transportmodus, der der Waschlast ähnlich ist, jedoch ohne Hängelast {cite:p}`yu_effect_2009,piton_sediment_2016`.

*Französisch: Charriage<br>German: Geschiebtransport*

Benthos
: The betnhos is composed of organisms inhabiting the bottom of aquatic environments, including oceans, lakes, and rivers. Benthic organisms reside in close proximity to the substrate and comprise various species like invertebrates (e.g., worms, mollusks, crustaceans, and insects), certain fish, and amphibians. The benthos plays a crucial role in nutrient cycling, organic matter decomposition, and it serves as a food source for higher trophic levels {cite:p}`flint1975effects, costello2009distinguishing`.

Boussinesq Näherung
: Die Boussinesq Approximation der {term}`continuity equation <Continuity equation>` setzt voraus, dass Dichteschwankungen außer dem Schwerkraftbegriff (d.h. in den vertikalen Impulsgleichungen) vernachlässigt werden können. Darüber hinaus geht die Boussinesq Approximation davon aus, dass ein Fluid nicht inkomprimierbar ist und dass die Wellenbewegung inviscid {cite:p}`boussinesq_essai_1877,spiegel1960` ist. Achtung: nicht zu verwechseln mit der {term}`Boussinesq hypothesis`.

*Französisch: Näherung von Boussinesq<br>German: Boussinesq-Approximation*

Boussinesq Hypothese
: Die Boussinesq-Hypothese besagt, dass die turbulenten Spannungen mit den mittleren Geschwindigkeitsgradienten in ähnlicher Weise zusammenhängen, wie die viskosen Spannungen mit den Gesamtgeschwindigkeitsgradienten {cite:p}`glegg_chapter_2017` zusammenhängen. In der Praxis entspricht die Boussinesq-Hypothese der Annahme, dass der durch turbulente Wirbel verursachte Impulstransfer mit einer Wirbelviskosität modelliert werden kann, was beispielsweise für Turbulenzverschlüsse (z.B. in {term}`RANS`Modellen) {cite:p}`boussinesq_essai_1877,schmitt_boussinesq_2007` wichtig ist. Vorsicht: nicht mit dem {term}`Boussinesq approximation` verwechselt werden.

*Französisch: hypothèse de Boussinesq<br>German: Näherung von Boussinesq*

Geflecht-
: Eine Flechtflussmorphologie bezieht sich auf anaverzweigte Kanalnetze mit hohem {term}`bedload <Bedload>`-Versorgung, meist in mäßig steilem Mittelland zu Bergflüssen {cite:p}`leopold_river_1957, rosgen_classification_1994`.

  ```{figure} ../img/nature/devoll-alluvial-braided-2021.jpg
  :alt: river geomorphology anabranch tresse zopfform
  :name: braided-channel

Ein geflochtener Teil des Devolli (Albanien). Quelle: Sebastian Schwindt (2021)
  ```

*Französisch: en tresse<br>German: Geflecht- bzw. Zopfausbildung (?)*

CF
: **Computational Fluid Dynamics (CFD)** ist ein Zweig der Fluidmechanik, der numerische Methoden und Algorithmen verwendet, um Probleme mit Fluidflüssen zu analysieren und zu lösen.

CFD beinhaltet die Simulation des Fluidverhaltens, wie die Bewegung von Luft, Wasser oder Gasen, indem die regulären mathematischen Gleichungen (typischerweise die {term}`Navier-Stokes equations`) mit iterativen Rechentechniken gelöst werden. Diese Simulationen geben Einblicke in komplexe Phänomene der Fluiddynamik, einschließlich Turbulenz, Wärmeübertragung, chemische Reaktionen und Mehrphasenströmungen.

CFD ist weit verbreitet in einer Vielzahl von Branchen, einschließlich Luft- und Raumfahrt, Automotive, Bauingenieurwesen oder Energieproduktion, um Designs zu optimieren, Leistung vorherzusagen und Effizienz zu verbessern. Allgemeine CFD-Tools sind spezialisierte Software wie {ref}`OpenFOAM <chpt-openfoam>` (offene Quelle), FLOW-3D (proprietär), ANSYS Fluent (proprietary), oder STAR-CCM+ (proprietary). Obwohl {ref}`Telemac <chpt-telemac>` aufgrund seiner Fähigkeit, Fluidflussprobleme mit numerischen Techniken zu lösen, unter die breitere Kategorie der CFD-Software fällt, ist es spezialisierter für den freien Oberflächenfluss und den Sedimenttransport als allgemeine CFD-Software.

CFL-Zahl
: Im Bereich der Hydrodynamik bezieht sich die Abkürzung CFL-Zahl allgemein auf den Zustand **Courant-Friedrichs-Lewy**, der ein Konvergenzkriterium für die numerische Lösung an die {term}`Navier-Stokes equations` (Teildifferenzgleichungen, PDE) darstellt. Die CFL-Zahl gilt für explizite Zeitintegrationsschemata, die in Abhängigkeit von der Größe der Netzzellen für große Zeitschritte instabil werden können. Heute verwendet die meisten numerischen Software einen internen Wert für die CFL-Zahl, um den maximalen Zeitschritt, der für die Stabilität von expliziten Solven erforderlich ist, adaptiv zu berechnen. In der 2d-Modellierung wird der CFL-Zahl-Zustand als $c_{cfl}={u_x \cdot \Delta t}/\Delta x + {u_y \cdot \Delta t}/\Delta y$ definiert, wobei $\Delta t$ der Zeitschritt ist, $\Delta x$ und $\Delta y$ Gitterzellengrößen in $x$ und $y$-Richtung des Koordinatenreferenzsystems sind, und $u_x$ und $u_y$ sind die Strömungsgeschwindigkeiten in den $x$ und $y$-Richtung. Ein expliziter Soldat wird als stabil angenommen, wenn $c_{cfl} \leq c_{cfl, crit}$, wobei der kritische Wert $c_{cfl, crit}$ für den CFL-Zahl-Zustand kleiner als 1,0 sein muss. Dazu verwendet die numerische Modellierungssoftware wie BASEMENT einen Standardwert von $c_{cfl, crit} = 0.9$.

*Französisch: Nombre de Courant<br>German: CFL-Zahl-Zahl*

Protokollierung
: Flussbettverstopfung beschreibt die Sedimentation der porösen groben Sedimentmatrix der hyporheischen Zone unter und entlang von Kies-Kies-Kies-Bett-Flüssen. Wir differenzieren zwischen externer und interner Verstopfung: äußere Verstopfung wirkt sich auf Surfschichten aus und ist eine direkte Folge der Ablagerung feiner, kohäsiver Sedimente; interne Verstopfung erfolgt in tieferen Schichten der Hypothekenzone und ist die Folge einer spontanen Perkolation oder Kornsortierung an der Oberfläche {cite:p}`berkman_effect_1987,schaelchli_clogging_1992`.

  ```{figure} ../img/nature/outer-clogging.jpg
  :alt: riverbed clogging siltation colmation colmatation Kolmation
  :name: outer-clogging

Beispiel für äußere Flussbettverstopfung einer groben Sedimentmatrix mit feinem Schlammsediment. Bild: Sebastian Schwindt (2021).
  ```

*Französisch: Colmation/colmatation<br>German: Kolmation*

Continuity equation
: The differential form of the continuity equation is $\frac{\partial \psi}{\partial t}+\mathbf{u} \cdot \nabla \psi = 0$ where $\psi$ is a constant of the particle/substance in consideration and $\mathbf{u}$ is the fluid velocity vector. The $\nabla$ operator is literally a vector of partial differential operators $\frac{\partial}{\partial x_i}$ where $x_i$ refers to the dimensions of the flow field. In the case of steady flow (no variability in time) the advection equation becomes $\mathbf{u} \cdot \nabla \psi = 0$ {cite:p}`kundu_fluid_2008`.

  The mass continuity equation of an incompressible fluid, such as water, considers the constant $\Psi$ as a mass and has the form $\nabla \cdot \mathbf{u} = 0$ or $\frac{\partial u_i}{\partial x_i} = 0$ {cite:p}`kundu_fluid_2008`.

*Französisch: Équation de continuité<br>German: Kontinuitätsgleichung*

Convection
: Convection encompasses {term}`Advection` and {term}`Diffusion` {cite:p}`kundu_fluid_2008`. Thus, convection is fluid motion because of bulk transport (water flowing in a river with reference to {term}`Advection`) and dispersion of a fluid component from high-density to low-density regions ({term}`Diffusion`) in the flow field (e.g., an ink drop dispersing in a river).

*Französisch: Konvektion<br>German: Konvektion*

Koordinatenreferenzsystem
: Ein Koordinatenreferenzsystem (Koordinatenreferenzsystem), auch Spatial Reference System (**SRS**) genannt, ist ein Orientierungseinheitssystem, um Objekte in einer Karte geographisch zu lokalisieren. Das Koordinatenreferenzsystem beinhaltet einen Ursprung ($x$=0.0 und $y$=0,0) und eine Projektion. Objekte einer Karte können durch die Transformation ihrer Koordinatenreferenzsystem bezüglich der Koordinaten und der Projektion in eine andere Karte gebracht werden. Lesen Sie mehr über Koordinatenreferenzsystem in der Rubrik unter {ref}`Projections and Coordinate Systems <prj>`.

*Französisch: Système de coordonnées <br>German: Koordinatenreferenzsystem / Koordinatenbezugsystem (KBS)*

CSV
: Das Comma-Separated Values (CSV)-Dateiformat beschreibt die Struktur einer Textdatei, die einfach strukturierte Daten speichert. Die Dateinameerweiterung ist `*.csv`, die auch Tab-Separated Values (TSV) enthalten kann. Der Separator (d.h. Komma, Semikolon oder Tab) begrenzt (oder trennt) Kolonwerte in einer Zeile einer `*.csv`Datei. Die Spreadsheet-Software, wie z.B. {ref}`Libre Office Calc <lo>`, ermöglicht es, `*.csv`-Dateien für zellformulabasierte Datenanalysen zu importieren und zu verarbeiten.

Digitales Oberflächenmodell (DOM)
: Ein digitales Aufzugsmodell (Digitales Oberflächenmodell (DOM)) stellt die bloße Erdoberfläche ohne Objekte wie Gebäude oder Bäume dar. Ein Digital Surface Model (Digitales Höhenmodell (DHM)) umfasst dagegen Objekte wie Bäume oder Gebäude. Darüber hinaus stellt ein Digital Terrain Model (Digitales Geländemodell (DGM)) ähnliche Daten zu einem Digitales Oberflächenmodell (DOM) dar und sowohl Digitales Oberflächenmodell (DOM) als auch Digitales Geländemodell (DGM) können in vielen Regionen der Welt synonym verwendet werden. In den USA bezieht sich ein Digitales Geländemodell (DGM) jedoch auf einen {ref}`Vector <vector>` (regelmäßig beabstandete Punkte) Datensatz, während ein Digitales Oberflächenmodell (DOM) ein {ref}`raster`dataset ist. Die Übersetzung in andere Sprachen geht nicht mit der gleichen Definition von Digitales Oberflächenmodell (DOM), Digitales Höhenmodell (DHM) und Digitales Geländemodell (DGM) zusammen, und die folgenden Übersetzungen beziehen sich auf die englischen Definitionen anstatt auf die gleichen (übersetzten) Wörter.

*Französisch für Digitales Höhenmodell (DHM): Modèle numérique d'élévation (MNE) <br>German for Digitales Höhenmodell (DHM): Digitales Höhenmodell (DHM)*

*Französisch für Digitales Oberflächenmodell (DOM): Modèle numérique de Gelände (MNT) <br>Deutsch für Digitales Oberflächenmodell (DOM): Digitales Oberflächenmodell (DOM)*

*Französisch für Digitales Geländemodell (DGM): Modèle numérique d'élévation (MNE) <br>German for Digitales Geländemodell (DGM): Digitales Geländemodell (DGM)*

Letztlich gibt es viele Optionen für *korrekt* Digitales Oberflächenmodell (DOM)-terminologie abhängig von der Region, in der Sie sind. Was ist der richtige Begriff in welcher Sprache? Es gibt keine universelle Antwort auf diese Frage und eine gute Wahl ist, mit dem Kommunikationspartner geduldig zu sein.


Diadrom
: Diadromfisch {term}`guilds <Guild>` migrieren zwischen Meer und Süßwasser in ihrem Lebenszyklus, im Gegensatz zu {term}`potamodromous fish <Potamodromous>`, dass nur in Süßwasserregionen wandert. In diadromen Fischgulden wird zwischen sub-guilds {cite:p}`myers_fish_1949` unterschieden:
  
* * * Anadromous* Fisch leben in den Meeren und wandern zu Süßwasser, hauptsächlich zur Reproduktion. Beispiele für anadromöse Fische sind Meeresforelle (*Salmo trutta trutta*) oder Pazifiklachs (*Oncorhynchus*).
* * *Katadrom* Fisch leben in Süßwasser und wandern zum Meer zur Reproduktion. Ein Beispiel für kakadromen Fisch ist American Eel (*Anguilla rostrata*).
* * * Amphidromous* Fische wandern regelmäßig zwischen Meer und Süßwasser. Ein Beispiel für Amphidromfische ist runder Goby (*Neogobius melanostomus*) {cite:p}`lecaudey_fish_2019`.

Verbreitung
: Diffusion ist das Ergebnis einer zufälligen Bewegung von Partikeln, angetrieben durch Konzentrationsunterschiede (z.B. Dissipation von hochkonzentrierten Partikeln zu Bereichen geringer Konzentration). Mathematisch wird die Diffusion von $\frac{\partial \psi}{\partial t} = \nabla \cdot (D \nabla \psi)$ beschrieben, wobei $\psi$ eine Konstante des betrachteten Partikels/Substanzes ist; $D$ ist ein Diffusionskoeffizient (oder Diffusivität) in m$^2$/s, der eine Proportionalitätskonstante zwischen molekularem Fluss und Gradient einer Substanz (oder Spezies) ist. Der $\nabla$ (*nabla*)-Operator ist ein Vektor von Teildifferenzen $\frac{\partial}{\partial x_i}$, wobei $x_i$ die Abmessungen des Flussfeldes {cite:p}`kundu_fluid_2008` angibt.

*Französisch: Diffusion<br>German: Diffusion*

Dimensionless bed shear stress
: The dimensionless bed shear stress $\tau_x$ (in the literature often called $\theta$) is derived from the shear forces that act on the riverbed as a result of flowing water. $\tau_x$ is a key parameter in the calculation of {term}`bedload <Bedload>` transport where many semi-empiric equations assume that a sediment grain is mobile when a particle size-related, critical value of the dimensionless bed shear stress is exceeded. This critical value of dimensionless bed shear stress is also referred to as {term}`Shields parameter`. To this end, $\tau_x$ is calculated based on hydraulic characteristics and the characteristic grain size $D_{pq}$ {cite:p}`von_karman_mechanische_1930,kramer_modellgeschiebe_1932`:

  $$
  \tau_{x} = \frac{\rho_w \cdot g \cdot R_h \cdot S_e}{\rho_w \cdot g \cdot \left(s-1\right) \cdot D_{pq}}
  $$

  where $R_h$ is the hydraulic radius (cf. calculation in the {ref}`1d hydraulic Python exercise <calc-1d-hyd>`); $S_{e}$ is energy slope; and $s$ is the ratio of sediment grain and water density (typically 2.68) {cite:p}`schwindt_hydro-morphological_2017`. $R_h$ may be substituted by water depth in wide rivers with monotonous cross-sectional shape and for (grid) cells of a 2d numerical model. The terms $\rho_w$ (water density) and $g$ (gravitational acceleration) cancel in the nominator and denominator, and are provided here to make clear that the nominator essentially is (dimensional) bed shear stress.

*Französisch: Cisaillement adimensionel<br>German: Dimensionslose Schubspannung*


Dirichlet Randbedingung
: Eine Dirichlet-Grenzbedingung (nach Johann Peter Gustav Lejeune Dirichlet) gibt Werte für die Lösungen von gewöhnlichen oder partiellen Differentialgleichungen an den Grenzen (d.h. Außenkanten) eines (numerischen) Modells vor. Deshalb werden Dirichlet-Grenzbedingungen auch als Grenzbedingungen erster Ordnung bezeichnet. Im Gegensatz dazu gibt eine zweite Ordnung {term}`Neumann boundary condition` Werte für die Derivate der gewöhnlichen oder partiellen Differentialgleichungen {cite:p}`kundu_fluid_2008` vor.

*Französisch: Zustand aux limits de Dirichlet <br>German: Dirichlet-Randbedingungen*


Echolot
: Ein Echolot emittiert ein akustisches Signal unter Wasser, das von den Objekten der Unterwasserlandschaft reflektiert wird. Echo-Sounding ist eine aktive {term}`Sonar`-Technik und ermöglicht die Schaffung einer Unterwasser-Digitales Oberflächenmodell (DOM), die auch als Badymetrie bezeichnet wird. Um Echogeräusche durchzuführen, muss eine Sonde auf einem Boot installiert werden, das eine minimale navigierbare Wassertiefe benötigt. Darüber hinaus erfordert die Verwendung des Echolots (Sonde) selbst auch eine minimale Wassertiefe, um mit wenig Störgeräuschen zu arbeiten. Daher ist durch Erfahrung eine Mindestwassertiefe von 1-2 m notwendig, um die Badymetrie eines Flusses durch Echoschallen zu untersuchen. Echobeschallung kann mit Einstrahlgeräten (einer Unterwasserstelle) oder Mehrstrahlgeräten (Unterwasseroberfläche) durchgeführt werden.

*Französisch: Échosondeur / Sondeur acoustique <br>German: Echolot / Fächerecholot*

Ethohydraulik
: Ethohydraulik ist die interdisziplinäre Untersuchung des aquatischen Tierverhaltens in Abhängigkeit von hydraulischen Umgebungen, insbesondere im Hinblick auf die Wechselwirkung von Organismen mit Wasserflussmustern in ihren natürlichen Lebensräumen. Der Begriff ist eine Mischung aus "Ethologie" und "Hydraulik", geprägt um eine wissenschaftliche Feldverschmelzung Verhaltensökologie mit Fluidmechanik zu beschreiben. So untersucht ethohydraulics, wie Fischarten ihr Schwimmverhalten an verschiedene Wasserströme in Flüssen und Flüssen anpassen {cite:p}`lehmann2022ethohydraulics`.

*Französisch: ethohydraulique (f) <br>German: Ethohydraulik (w)*

Exner equation
: The {cite:t}`exner_uber_1925` equation yields sediment mass conservation in a hydro-morphodynamic model (see also the {ref}`TELEMAC-Gaia tutorial <tm-gaia>`) and expresses that the time-dependent {term}`Topographic change` rate $\frac{\partial \eta}{\partial t}$ equals the unit sediment ({term}`bedload <Bedload>`) fluxes $q_b$ over the boundaries {cite:p}`hirano1971,blom2003`:

  $$
  \frac{\partial \eta}{\partial t} = -\frac{1}{\epsilon}\frac{\partial q_b}{\partial x}
  $$

wobei $\epsilon$ die Porosität der aktiven Transportschicht (Ribbett) ist und $\eta$ die Dicke der aktiven (Ribbett) Transportschicht ist.

  ```{admonition} TELEMAC-Gaia uses a mass-conservative form of the Exner equation
  :class: note, dropdown

Das Morphodynamik-Modul von TELEMAC {ref}`Gaia <tm-gaia>` verwendet ein vertikales Integral eines Massentransportvektors $\boldsymbol{q_b}$ in der Exner-Gleichung, das die Sedimentkorndichte $\rho_s$:

  $$
  \left(1 - \epsilon\right) \frac{\partial \left(\rho_s \eta\right)}{\partial t} + \nabla \cdot \left(\rho_s \boldsymbol{q_b} \eta \right) = 0
  $$

Der $\nabla$-Operator ist ein Vektor von Teildifferenzen $\frac{\partial}{\partial x_i}$, wobei $x_i$ die Dimensionen des Flussfeldes {cite:p}`kundu_fluid_2008` angibt. Der Unit-Bettload-Transportvektor $\boldsymbol{q_b}$ besteht aus einer $x$ und einer $y$-Komponente:

  $$
  \boldsymbol{q_b} =  \begin{pmatrix}q_{b_x} \\ q_{b_y} \end{pmatrix}  =  \begin{pmatrix}q_{b} \cos \alpha \\ q_{b} \sin \alpha  \end{pmatrix}
  $$

wobei $\alpha$ der Winkel zwischen dem Längskanal ($x$) und dem Bettlasttransportvektor $\boldsymbol{q_b}$ ist.
  ```

*Französisch: Equation de Exner<br>German: Exner-Gleichung*


Froud-Nummer
: Die Froude-Nummer $Fr$ ist das Verhältnis zwischen Trägheit und Schwerkraft, und es ist eine Schlüsselanzahl der Wellenausbreitung. So sagt $Fr$, ob Informationen in Vorwärtsrichtung übermittelt werden können oder nicht {cite:p}`chow59,hager09,hager10`:

  $$
  Fr^2 = \frac{Q^2}{A^3 g} \frac{\partial A}{\partial h}\begin{cases} < 1 \rightarrow \mbox{ subcritical flow (upstream and downstream wave propagation)} \\ = 1 \rightarrow \mbox{critical flow (standing waves in upstream direction)} \\ > 1 \rightarrow \mbox{ supercritical flow (downstream wave propagation only)} \end{cases}
  $$

Der Übergang von überkritischem Fluss zu unterkritischem Fluss wird als *hydraulischer Sprung* bezeichnet. Für einen rechteckigen Querschnitt $A$ wird die Froude-Nummer:

  $$
  Fr = \frac{u}{\sqrt{g \cdot h}}
  $$

Die Froude-Nummer ist auch die Basis für die Skalierung vieler Sedimenttransporterscheinungen im offenen Kanalfluss {cite:p}`yalin71,yalin77`.

*Französisch: Nombre de Froude <br>German: Froude-Zahl*

Geodäsie
: Das Georeferenced Tag Image File Format (GeoTIFF) verlinkt geographische Positionen an {ref}`raster`Bilder. Ein GeoTIFF beinhaltet mehrere Dateien, die das verschlagwortete Bild selbst enthalten (`*.tif`-Datei), eine Weltdatei (`*.tfw`-Datei), die Informationen über das geographische Referenz- und Projektionssystem enthält, und potenziell eine `*.ovr`-Datei, die das GeoTIFF mit anderen Ressourcendaten verknüpft. Lesen Sie mehr über das *Open Geospatial Consortium*'s [Standard für GeoTIFF](https://www.ogc.org/standards/geotiff).

Geomorphe Heterogenität
: Geomorphe Heterogenität beschreibt das räumliche Muster gemorpher Einheiten (z.B. {term}`Riffle pool`) innerhalb der {term}`River corridor`. Es beschreibt die Ungleichförmigkeit eines Flusses im Vergleich zu einem monotonen trapezförmigen oder rechteckigen künstlichen Kanal {cite:p}`wohlegu2022`.

Schuldner
: Eine ökologische Gilde beschreibt eine Gruppe von Arten, die gemeinsame Ökosystemressourcen teilen. Arten in einer Gilde sind nicht notwendigerweise miteinander verbunden, noch verwenden sie unbedingt ähnliche ökologische Nischen. Der Begriff Gilde wurde von {cite:t}`root_niche_1967` eingeführt und wird in Ökohydraulik verwendet, um (physikalische) Lebensraumpräferenzen von Fischarten und deren Lebensstadien zu beschreiben. Zum Beispiel können wir zwischen {term}`reophilic <Reophile>` und {term}`limnophilous <Limnophile>`Fische Gilden unterscheiden. Darüber hinaus können wir zwischen Fisch {term}`spawning guilds <Spawning guild>` und {term}`potamodromous <Potamodromous>`, {term}`oceanmodromous <Oceanodromous>` und {term}`diadromous <Diadromous>`migration guilds unterscheiden.

  *French: Guilde (f) <br>German: Gilde (w)*

HDF
: The [Hierarchical Data Format (HDF)](https://www.hdfgroup.org/) provides the `*.h5` (HDF4) and `*.h5` (HDF5) file formats that store large datasets in an organized manner. HDF is often used with high-performance computing (HPC) applications, such as numerical models, to store large amounts of data output. This eBook impinges on HDF datasets in the {ref}`chpt-basement` tutorial where {term}`xdmf` files represent the model output, and in the {ref}`chpt-telemac` tutorials. In particular, Telemac builds on mesh and boundary files of the EnSim Core that is described in the user manual of the pre- and post-processing software [Blue Kenue](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/2011_UserManual.pdf)<sup>TM</sup> (the newest [Blue Kenue installer](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) contains an updated version of the user manual). Understanding the HDF format significantly facilitates troubleshooting structural errors of computational meshes for numerical models.

Hyporhezone
: Die hyporheische Zone ist der Raum unter und entlang Flüssen, in denen Oberflächenwasser und Grundwasseraustausch stattfinden. Für das Ökosystem sind die Austauschprozesse einer funktionellen, nicht-{term}`clogged <Clogging>` hyporheic-Zone wichtig, insbesondere für die Fischpeichung {cite:p}`boulton_hyporheic_1998`.

Kolmogorov Mikroskalen
: Der russische Mathematiker Andrey Nikolaevich Kolmogorov stellte das Konzept vor, dass die kleinsten Skalen der Turbulenz für jede turbulente Strömung (d.h. universal) {cite:p}`youschkevitch_kolmogorov_1983` ähnlich sind. Nach diesem Konzept, den sogenannten Kolmogorov-Mikroskalen, wird die {term}`turbulent kinetic energy <Turbulent kinetic energy>` Wärme abgeführt, wenn die Viskosität dominiert. Die Kolmogorov Mikroskalen können für Länge, Zeit und Geschwindigkeitseinheiten in Abhängigkeit von der kinematischen Viskosität $\nu$ und der Dissipationsrate $\epsilon$ von {term}`turbulent kinetic energy <Turbulent kinetic energy>` (pro Einheitsmasse) berechnet werden.

  The Kolmogorov length scale $\eta_L$ is calculated as follows, and typically is in the order of 0.1-10 m$^{-3}$ {cite:p}`dey_fluvial_2014`:

  $$
  \eta_L = {\left( \frac{\nu^3 }{\epsilon } \right)} ^{1/4}
  $$

Die Kolmogorov-Zeitskala $\eta_T$ wird als {cite:p}`dey_fluvial_2014` berechnet:

  $$
  \eta_T = {\left( \frac{\nu}{\epsilon } \right)} ^{1/2}
  $$

Die Geschwindigkeitsskala Kolmogorov $\eta_U$ wird als {cite:p}`dey_fluvial_2014` berechnet:

  $$
  \eta_U = ( \nu \cdot \epsilon )^{1/4}
  $$

Krylov Raum
: Krylov (sub) Leerzeichen werden in numerischen Approximationssystemen verwendet, um Lösungen für Sparse zu finden (viele Nulleinträge), hochdimensionale lineare Systeme {cite:p}`bunch1974`. Zu diesem Zweck verwenden Krylov (sub) Raummethoden Gaussian Eliminierung (z.B. {term}`LU decomposition`) zur Beschleunigung der Berechnungen {cite:p}`gutknecht2007`.

*Französisch: Sous-espaces de Krylov / Méthode de la puissance itérée <br>German: Krylowraum*

IAHR
: The International Association for Hydro-Environment Engineering and Research (IAHR) is an independent non-profit organization that unites professionals in the field of water resources. The IAHR has multiple branches and publishes several journals in collaboration with external publishing companies. Read more about the IAHR at [https://www.iahr.org](https://www.iahr.org).

Libyen
: Light Detection and Ranging (*LiDAR* oder *lidar*) verwendet Laserpulse, um Erdoberflächeneigenschaften wie Baldachin oder Geländeerhebung zu messen. Die Laserpulse werden von einer Fernerkundungsplattform (Fixstation oder Airborne) an Oberflächen gesendet, die die Pulse mit unterschiedlicher Geschwindigkeit (Zeit-of-Flight informiert über Geländehöhe) und Energiemuster (Leben verhalten sich anders als Rock) reflektieren. Lidardaten sind in ihrer Rohform eine Punktwolke mit verschiedenen georeferierten Informationen über das reflektierte Signal. Lidar-Punktwolken für Endbenutzer werden typischerweise im *las*-Format oder im *laz*-Format gespeichert. *las*-formatierte Daten sind viel schneller zu verarbeiten, aber auch viel größer als *laz*-formatierte Daten. Aus diesem Grund werden vorzugsweise Deckeldaten im *laz*-Format übertragen, während das *las*-Format vorzugsweise zur Verarbeitung von Deckeldaten verwendet wird.

limnophil
: Der Begriff limnophil wird als Noun in Bezug auf Arten verwendet, die lieber in ruhigen Gewässern leben. So kolonisieren limnophile Arten, wie häufiges Rind (*Scardinius erythrophthalmus*), langsam fließende bis stagnierende Frischwassergebiete. Im Gegensatz zu limnophilen Arten bevorzugen reophile Arten schnell fließende Regionen (siehe auch {term}`Reophile`).

*Französisch:<br>German: limnophil*

LU Zersetzung
: Für die Lösung von linearen Systemen (Matrizen) gilt eine tieferliegende (LU) Zersetzung, indem eine Matrix von Gleichungen in eine obere und eine untere dreieckige Matrix umorganisiert wird. Somit ist die LU-Zersetzung eine Form der Gaussian-Abspaltung, die typischerweise in numerischer Analyse (z.B. {ref}`Telemac2d <tm2d-solver-pars>`) oder maschinelles Lernen angewendet wird.

*Französisch: Décomposition LU<br>German: LR Zerlegung (Gaußsches Eliminationsverfahren)*

MPI
: In Computing steht MPI für *Message Passing Interface*, die ein tragbarer Nachrichtenübermittlungsstandard ist. MPI wird in vielen Open-Source-C, C++ und Fortran-Anwendungen implementiert, um Parallel Computing zu ermöglichen.

Navier-Stokes Gleichungen
: Die allgemeine Form der Navier-Stokes-Gleichungen beschreibt die Bewegung einer Newtonischen Flüssigkeit und drückt die Erhaltung von Masse und Dynamik {cite:p}`batchelor_2000_chpt3`. Die Navier-Stokes-Gleichungen sind eine spezielle Art von {term}`Continuity equation`, die aus Cauchys Gleichung (Konservierung von Impuls) abgeleitet wird. Die Gleichung vereinfacht mit der Annahme von inkompressiblen Fluiden und reduziert sich bei vernachlässigbaren viskosen Effekten auf die *Euler Gleichung*, was in weitem Abstand von den Grenzen {cite:p}`kundu_fluid_2008` der Fall ist.
Eine theoretische, exakte Lösung der Navier-Stokes-Gleichungen würde eine perfekte Beschreibung vieler natürlicher Prozesse ergeben. Die zugrunde liegenden Systemgleichungen beinhalten jedoch unbekanntere Parameter als Gleichungen. Aus diesem Grund sind für die Lösung der Navier-Stokes-Gleichungen strenge Vereinfachungen (z.B. die {term}`Shallow water equations`) und numerische Approximationen mit erheblich größerem Rechenaufwand als für eine analytische Lösung erforderlich. Vereinfachungshypothesen sind beispielsweise eine hydrostatische Druckverteilung (die zu den seichten Wassergleichungen führt) oder die Annahme, dass ein Fluid inkomprimierbar ist.
Moderne Modelle verwenden überwiegend eine bestimmte Form der Navier-Stokes-Gleichungen, insbesondere die {term}`Reynolds-averaged Navier-Stokes (RANS) <RANS>`-Gleichungen.

*Französisch: Equations de Navier-Stokes <br>German: Navier-Stokes-Gleichungen*

Neumann Randbedingung
: Eine Neumann-Grenzbedingung (nach Carl Gottfried Neumann) gibt an den Grenzen (d.h. Außenkanten) eines (numerischen) Modells Werte für die Derivate gewöhnlicher oder partieller Differentialgleichungen vor. Deshalb werden auch Neumann-Grenzbedingungen als Grenzbedingungen zweiter Ordnung bezeichnet. Im Gegensatz dazu gibt ein First-Order {term}`Dirichlet boundary condition` Werte für die Lösungen von gewöhnlichen oder partiellen Differentialgleichungen {cite:p}`kundu_fluid_2008` vor.

*Französisch: Zustand aux limits de Neumann <br>German: Neumann-Rand Bedingungen*

Ozeanodrom
: Oceanodromous {term}`fish guilds <Guild>` leben ausschließlich in Ozeanen. Während ozeanodromhaltige Fische {term}`diadromous fish <Diadromous>` (vom Meer bis zum Süßwasser) begegnen können, werden sie wahrscheinlich nie {term}`potamodromous <Potamodromous>` fish{cite:p}`myers_fish_1949` treffen. Beispiele für ozeanmodromhaltige Fische sind Atlantische Makrelen (*Scomber scombrus*) oder Atlantik Hering (*Clupea harengus*).

Betriebssystem
: Ein Betriebssystem (OS) verwaltet die Hardware eines Computers, einer Software (Ressourcen) und Dienste für jedes Programm, das Sie installieren möchten.

*Französisch: Système d'exploitation <br>German: Betriebssystem*

Pelagische Zone
: Die pelagische Zone umfasst die offene Wassersäule in Ozeanen, Meeren und (großen) Seen, ausgenommen die Boden- und Küstengebiete. Die pelagische Zone ist in Subzonen auf der Basis von Tiefe und Lichtdurchdringung, einschließlich der epipelagischen (Oberflächenschicht), mesopelagischen (Twilight Zone), Bathypelagic (Midnight Zone) und abyssopelagic (Abyssalzone) unterteilt. Diese Zone wird von pelagischen Organismen wie Fisch, Meeressäugern und Plankton bewohnt, die an das Leben in der Wassersäule angepasst sind (aus dem Meeresboden, das heißt {term}`benthos <Benthos>`) {cite:p}`costello2009distinguishing`.

Plane Bett
: Ein Flugzeugbett bezieht sich auf eine Art Flussbett, die durch unregelmäßige Bettformen mit entfernter, unterschiedlicher Eingrenzung gekennzeichnet ist, oft im Übergang zwischen Transportkapazität begrenzt und Sedimentversorgung begrenzte Flussabschnitte {cite:p}`schwindt_hydro-morphological_2017`.

  ```{figure} ../img/nature/plane_bed_Drance.jpg
  :alt: planebed plane bed river stream example geomorphology
  :name: plane-bed

Beispiel eines Planbettflussabschnitts an der Drance (VS, Schweiz). Bild: Sebastian Schwindt (2016).
  ```

Kartoffeln
: Potamodromous {term}`fish guilds <Guild>` live und migrieren in Süßwasserregionen. Ihre Migration ist meist auf Reproduktion zurückzuführen. Der Unterschied mit {term}`diadromous fish <Diadromous>` ist, dass diese vom Meer in Süßwasserregionen wandern. Darüber hinaus werden potamodrome Fische sehr wahrscheinlich nie {term}`oceanmodromous <Oceanodromous>` fish {cite:p}`myers_fish_1949`. Beispiele für potamodromöse Fische sind Eal (*Anguilla anguilla*) und Flussforelle (*Salmo trutta fario*).


(Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen
: Die reynolds-gemittelten Navier-Stokes ((Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen)-Gleichungen sind eine statistische Approximation der {term}`Navier-Stokes equations` zur Modellturbulenz mit einem Zeitmittel und Geschwindigkeits- und Druckvarianz. Speziell machen (Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen-Lösungen in groben Skalen (d.h. gröber als {term}`Kolmogorov microscales`) Turbulenzen durch Austausch von Geschwindigkeit $u_k$ (und Druck)-Komponenten durch einen Mittelwert $\overline{u_k}$ und Fluktuationen $u'_k$ um diesen Mittelwert {cite:p}`nikora_double-averaging_2007`. Die Unterschrift $_k$ gibt Fließrichtungen 1 (streamwise/longitudinal $x$-Richtung), 2 (lateral /$y$-Richtung) und 3 (vertikal /$z$-Richtung) an. Die (Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen-Gleichungen lesen wie folgt {cite:p}`franca_turbulence_2015` für Massenbilanz (Reynolds-gemittelt {term}`continuity equation <Continuity equation>`):

  $$
  \frac{\partial \left(\rho_w\overline{u_k}\right)}{\partial x_k} = 0
  $$

wobei $\rho_w$ Wasserdichte bedeutet und $u$ die Strömungsgeschwindigkeit ist. Die (Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen Impulsbilanz lautet wie folgt: {cite:p}`franca_turbulence_2015`:

  $$
  \overbrace{\frac{\partial \left(\rho_w \overline{u_j}\right)}{\partial t}}^{I} + \textcolor{orange}{\overbrace{\frac{\partial \left(\overline{\rho'_w u'_j}\right)}{\partial t}}^{II}} + \overbrace{\frac{\partial \left(\overline{u_k} \overline{\rho_w} \overline{u_j}\right)}{\partial x_k}}^{III} + \textcolor{orange}{\overbrace{\frac{\partial \left(\overline{u_k} \overline{\rho'_w u_j'}\right)}{\partial x_k}}^{IV}} + \textcolor{orange}{\overbrace{\frac{\partial \left(\overline{u_j} \overline{\rho'_w u_k'}\right)}{\partial x_k}}^{V}} =\\\ \overbrace{-\frac{\partial \overline{p}}{\partial x_j}}^{VI} + \overbrace{\mu \frac{\partial^2 u_j}{\partial x_k \partial x_k}}^{VII}
  -\overbrace{\frac{\partial \overline{\rho_w} \overline{u'_k u'_j}}{\partial x_k}}^{VIII} - \textcolor{orange}{\overbrace{\frac{\partial \overline{\rho'_w u'_k u'_j}}{\partial x_k}}^{IX}} + \overbrace{\overline{\rho_w} g}^{X}
  $$

wobei Subskript $_j$ analog $_k$ ist, $t$ Zeit bedeutet, $p$ Druck ist und $\mu$ die dynamische Viskosität (von Wasser) ist. Die Begriffe I bis X haben folgende Bedeutungen:

* I lokale Ableitung von (Zeit) gemittelte Dynamik
* <font color='orange'>II Lokale Ableitung der durchschnittlichen Dynamik schwanken</font>
* III bedeuten {term}`advection <Advection>`
* <font color='orange'>IV mean{term}`advection <Advection>`tim-fluktuation (in $_k$Richtung)</font>
* <font color='orange'>V meine {term}`advection <Advection>`tim der Momentumfluktuation (in$_j$Richtung)</font>
* VI Durchschnittsdruck
* VII viskose Diffusion
* VIII Reynolds Stress
*<font color='orange'>IX turbulent{term}`diffusion <Diffusion>` (d.h. turbulenter Transport von Momentumfluktuation)</font>
* X mittlere Körperkraft / Schwerkraft

Die <font color='orange'>orange-color</font>begriffe beinhalten <font color='orange'>densityfluktuation</font>, und damit <font color='orange'>cancel out</font> unter Verwendung der {term}`Boussinesq approximation`. Unter dem Begriff VIII bezeichnet $\overline{u'_k u'_j}$ den Reynolds-Stress Tensor, der ein zusätzlicher Stress ist, der aus der Mittelung von Reynolds resultiert und ein Schließproblem darstellt. Zu diesem Zweck wird häufig das (in)famous $k$-$\epsilon$-Modell verwendet, wobei $k$ die {term}`turbulent kinetic energy <Turbulent kinetic energy>` und $\epsilon$ ihre Dissipationsrate angibt.

  ```{aside} Telemac Implementation
Telemac3d-Nutzer können das Spalart-Allamaras-Modell aktivieren, um so genannte *Detached Eddy Simulation* (DES) zu ermöglichen, indem die `HORIZONTAL TURBULENCE MODEL` und `VERTICAL TURBULENCE MODEL` Keywords an `5` gesetzt werden, während LES über das Smagorinsky-Modell (`4`) aktiviert werden kann.
  ```

(Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen-Löser sind rechnerisch hocheffizient, aber physikalisch unpräzis, weil sie nur als statistische Momente Turbulenz darstellen {cite:p}`nikora_double-averaging_2007`. Aus diesem Grund gibt es einen zunehmenden Trend bei der numerischen Modellierung zur Verwendung sogenannter Large Eddy Simulations (LES), die bei hoch {term}`Reynolds numbers <Reynolds number>` verwendet werden können, um große Wirbel genau zu modellieren und kleinere Wirbel mit einem feinen Strukturmodell zu simulieren. Eine genaue Repräsentation von Turbulenzen war mittels der Direct Numerical Simulation (DNS) möglich, die derzeit und für die meisten Freiflächengewässer nicht rechnerisch machbar ist {cite:p}`georgiou_direct_2018`.

*Französisch: Moyenne de Reynolds <br>German: (Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen*


Kennlinie
: Siehe {term}`Stage-discharge relation`.

reophil
: Der Begriff Reophil wird als Noun in Bezug auf Arten verwendet, die lieber in schnell fließendem Wasser leben. Außerdem wird zwischen reophilen A- und B-Arten unterschieden. Reophil Eine Art (z.B. braun/river Forelle *Salmo trutta (fario)* oder minnow *Phoxinus phoxinus*) kolonisiert den Hauptstrom eines Flusses an allen Lebensstadien. reophil B-Arten (z.B. Guadgeon *Gobio gobio*) besetzen ruhigere Flussregionen (z.B. Ochsen) in einigen Lebensstadien. Im Gegensatz zu reophilen Spezies bevorzugen limnophile Arten (z.B. gemeine Rudd *Scardinius erythrophthalmus*) ruhige (stagnierende) Flussregionen (siehe auch {term}`Limnophile`).

*Französisch: <br>German: reophil*

Reynolds-Nummer
: Die Reynolds-Nummer $Re$ bezieht viskose Kräfte auf Trägheit und ist ein Schlüsselparameter für Strömungsturbulenz {cite:p}`chow59`:

  $$
  Re = \frac{u h}{\nu} \begin{cases} < 800 \rightarrow \mbox{ laminar flow} \\ \geq 800 \mbox{ and } \leq 2000 \rightarrow \mbox{ transitional flow} \\ > 10000 \rightarrow \mbox{ turbulent flow} \end{cases}
  $$

Wo $\nu$ die kinematische Viskosität (10$^{-6}$m$^{2}$s$^{-1}$für Wasser unter 20$^{\circ}$C) bezeichnet. Bei Schotterbettflüssen sind Trägheitskräfte typischerweise im Vergleich zu zähen Kräften dominant; daher ist $Re$ im Allgemeinen größer als 2000 und der Fluss ist turbulent{cite:p}`chow59,wohl_mountain_2000`.

*Französisch: Nombre de Reynolds <br>German: Reynolds-Zahl*


Rheotaxis
: Rheotaxis ist ein Verhalten, das von Wasserorganismen in Abhängigkeit von der Strömungsrichtung des Wassers gezeigt wird, und unterstützt Fische bei der Kompensation von Driftverlusten {cite:p}`elder2015influence`. Es zeichnet sich durch zwei Arten aus: positive und negative Rheotaxis. Positive Rheotaxis beinhaltet die Orientierung gegen den Fluss, häufig bei Salmoniden beobachtet. Negative Rheotaxis beinhaltet Bewegung mit der Strömung, typisch für Aale oder bestimmte Arten von Süßwasserkatzen, aber dieses Verhalten ist weniger häufig als positive Rheotaxis.

*Französisch: Rhéotaxie (f) <br>German: Rheotaxis (w)*

Inhaltsverzeichnis
: Das proprietäre Rich Text Format (RTF) wickelt Rohtext in Funktionsblöcke, die grafisch aromatisierte *Word*-ähnliche Prozessoren ermöglichen, Dokumenteigenschaften wie Schriftgröße und -typ zu identifizieren. Gemeinsame RTFs sind beispielsweise *docx* oder *odf* und ermöglichen den Austausch von Textdateien zwischen verschiedenen *Word*-ähnlichen Prozessoren auf verschiedenen Betriebssystemen.

Riffle Pool
: Riffle-Pool (oder Pool-Riffle) Sequenzen sind eine Sequenz von schnell fließenden, flachen Flusseinheiten und tieferen, langsamer fließenden Einheiten eines Flusses, wobei die Abmessungen einer Einheit etwa einer Kanalbreite {cite:p}`lisle1979sorting` entsprechen. Die Wartung von Riffle-Pool-Kanälen erfordert eine ausreichende Sedimentversorgung bei kleineren Überschwemmungen und eine Geschwindigkeitsumkehr, wenn diese Überschwemmungen {cite:p}`caamano_unifying_2009` auftreten.

*Französisch: Rapide (m, Verifkation erforderlich) - Affouillement (m, Verifkation erforderlich) <br>German: Furt (w) - Kolk (m); manchmal auch Rausche (w) - Kolk (m); obwohl "Rausche" eher auf "glide" verweist.*


  ```{figure} ../img/nature/pool-riffle.jpg
  :alt: riffle pool bedform gravel bed
  :name: riffle-pool

Eine Pool-Riffle-Sequenz am American River in der Nähe von Sacramento (CA, USA). Quelle: Sebastian Schwindt (2018)
  ```

Flusskorridor
: Der Flusskorridor umfasst den aktiven Flusskanal(en), die Hochwassergebiete und die Hypothekenzone unter {cite:p}`wohlegu2022`.

Flussbettverstopfung
: Siehe {term}`Clogging`.

Rouse Nummer
: Die Rouse-Nummer $Ro$ bestimmt den Transportmodus (im Wesentlichen {term}`bedload <Bedload>` oder {term}`suspended load <Suspended load>`) eines Sedimentpartikels und dient zur Berechnung des Konzentrationsprofils des suspendierten Sediments. Die Rouse-Nummer wird aufgrund ihrer ursprünglichen Definition eines *Exponents in der suspendierten Lastfunktion* (siehe Seite 13ff in {cite:t}`rouse_analysis_1939`) auch als Kapital $Z$ bezeichnet. Es wird wie folgt berechnet:

  $$
  Ro = \frac{w_s}{\kappa\cdot u_*}
  $$

wobei $w_s$ die {term}`settling velocity <Settling velocity>`, $\kappa$ (=0,41) die van Karmàn Konstante {cite:p}`von_karman_mechanische_1930` ist und $u_*$ die {term}`shear velocity <shear velocity>` ist.

Ein Partikel wird in der Regel in Suspension transportiert, wenn es eine niedrige Rouse-Nummer ($Ro \lessapprox 0.5$) hat, in der Wassersäule, wenn es eine Rouse-Nummer zwischen etwa 0,5 und 2,0 hat, als Bettlast, wenn seine Rouse-Nummer höher ist, und neigt dazu, für sehr hohe Rouse-Nummern ($Ro \gtrapprox 12$) {cite:p}`dubuis_clogging_2023` hinterlegt.


Saint-Venant Gleichungen
: Der französische Mathematiker Adhémar Jean Claude Barré de Saint-Venant führte Maßvereinfachungen der {term}`Navier-Stokes equations` ein. Für einfache Querschnitte können die eindimensionalen (1d), durchschnittenen Saint-Venant-Gleichungen angewendet werden und stellen die Basislinie für die Manning-Strickler-Formel dar (vgl. {ref}`1d Hydraulics Python exercise <ex-1d-hydraulics>`). Die zweidimensionalen (2d), tiefengemittelten Saint-Venant-Gleichungen werden häufiger als die {term}`Shallow water equations` bezeichnet, die eine hydrostatische Druckverteilung {cite:p}`graf_hydraulique_2011` andeuten.

*Französisch: Équations (de Barré) de Saint-Venant <br>German: Saint-Venant-Gleichungen / Flachwassergleichungen (f, pl.)*

Sandbett
: Sandbettflüsse zeichnen sich durch die Fülle von feinem Sediment und Sandstäben aus. Im Vergleich zu einem Kiesbett neigt ein Sandbett zu einer höheren Schwebebelastung. Diese Art von Morphologie wird oft Lowland- und Küstenregionen beobachtet, in denen die hypothetische Energieklasse niedrig ist, ist weniger intensiv als in steileren Regionen {cite:p}`kleinhans2005, zyserman1994`.

  ```{figure} ../img/nature/sand-bed.jpg
  :alt: sandbed dunes anti-dunes
  :name: sand-bed

Dune Bettformen eines Sandbetts in einem Seitenkanal des Inn River in Bayern, Deutschland. Quelle. Sebastian Schwindt (2022)
  ```

Sedimenttransport
: Fluvialer Sedimenttransport umfasst zwei Arten der Partikelverlagerung: (1) Schweblast und (2) Bettlast (siehe Abbildung unten). Finer-Partikel mit einem Gewicht, das von der Flüssigkeit (Wasser) getragen werden kann, werden als {term}`Suspended load` transportiert. Coarser Partikel rollen, gleiten und springen auf dem Kanalbett werden als {term}`bedload <Bedload>` transportiert. Es gibt eine dritte Art Transport, die sogenannte Waschlast, die feiner ist als die grobe Bettlast, aber zu schwer (groß) in Suspension zu transportieren{cite:p}`einstein_bed-load_1950`. Die Einheiten für den Sedimenttransport sind für einen integralen Strömungsquerschnitt kg$^3\cdot$s$^{-1}$ oder pro Stückbreite kg$^3\cdot$s$^{-1}$m$^{-1}$. Darüber hinaus kann die {term}`Rouse number` dazu verwendet werden, ob ein Partikel in Suspension, als Bettlast oder gar nicht transportiert wird.

  ```{image} https://github.com/Ecohydraulics/media/raw/main/png/sediment-transport.png
  ```

*Französisch: Transport solide<br>German: Sedimenttransport*

Sedimentausbeute
: Die Sedimentausbeute ist die pro Flächeneinheit erodierte Sedimentmenge (Tonnen$\cdot$km$^{-2}\cdot$year$^{-1}$) eines Wassershed {cite:p}`griffiths2006a`.

*Französisch: Abbrechen solide<br>German: Feststoffeintrag*


Settling velocity
: The settling velocity $w_s$ is computed as a function of the ratio of sediment grain and water density $s$, gravitational acceleration $g$, grain size $D_x$, and the dimensionless drag coefficient $C_D$ {cite:p}`dey_fluvial_2014`:

  $$
  w_{s} = \sqrt{\frac{4}{3}\cdot \frac{(s-1)\cdot g\cdot D_x}{C_{D}}}
  $$

$C_{D}$ ist wiederum eine Funktion der {term}`Reynolds number` und kann wie folgt angenähert werden (nicht allgemein gültig!) {cite:p}`stokes1850`:

  $$
  C_{D} = \frac{24}{Re}
  $$



Shallow Wassergleichungen
: In seichten (d.h. kleinen Wassertiefen) und weiten Gewässern (viele Flüsse) kann die Annahme der hydrostatischen Druckverteilung zur Vereinfachung der {term}`Navier-Stokes equations` vorgenommen werden. Die entsprechende vereinfachte Form der {term}`Navier-Stokes equations` wird als seichte Wassergleichungen bezeichnet. Die flachen Wassergleichungen bedeuten, dass die vertikale Strömungsgeschwindigkeit gegenüber der horizontalen (und Längs-) Strömungsgeschwindigkeit vernachlässigbar ist. Diese Annahme ist in vielen Flusssystemen gültig, aber es gibt mehrere Fälle, für die die flachen Wassergleichungen nicht geeignet sind {cite:p}`kundu_fluid_2008`.

So sind z.B. die tiefengemittelten flachen Wassergleichungen ** für druckbeaufschlagte Ströme (z.B. bei Weiden oder in Rohren) nicht geeignet**. Dieses eBook empfiehlt, die flachen Wassergleichungen** nur dann zu verwenden, wenn die Wassertiefe kleiner als das 1/20-fache der charakteristischen Wellenlänge ist (z.B. Flutwellen oder in tsunami/oceanischen Modellen) und wenn die Wassertiefe kleiner als 1/10 der benetzten Kanalbreite ist. Die Anwendung der seichten Wassergleichungen wird in diesem eBook mit den Tutorials auf 2d numerische Modellierung (d.h. in den {ref}`BASEMENT <basement2d>` und {ref}`Telemac2d <telemac2d-steady>`Kapiteln) vorgestellt.

*Französisch: Équations (de Barré) de Saint-Venant<br>German: Flachwassergleichungen*

Schergeschwindigkeit
: Schergeschwindigkeit $u_*$ (oder Reibungsgeschwindigkeit) drückt Schubspannung in Geschwindigkeitseinheiten aus. Der Parameter ist z.B. zur Beschreibung der Scherwirkung von tiefgemittelter Strömungsgeschwindigkeit nützlich. Es kann wie folgt berechnet werden {cite:p}`schwindt_hydro-morphological_2017`:

  $$
  u_* \approx \sqrt{\tau_b / \rho_w} = g\cdot R_h \cdot S_e \approx g\cdot h \cdot S_e
  $$

wobei $\tau_b$ die {term}`bed shear stress <Dimensionless bed shear stress>` angibt, $rho_w$ die Dichte des Wassers ist, $R_h$ ist der hydraulische Radius (siehe auch {ref}`1d hydraulic Python exercise <calc-1d-hyd>`), $g$ ist gravitationale Beschleunigung, und $S_{e}$ ist Energieflanke. $R_h$ kann durch Wassertiefe $h$ in breiten Flüssen mit monotoner Querschnittsform und für (grid) Zellen eines 2d numerischen Modells ersetzt werden.

*Französisch: Vitesse de frottement<br>German: Schubspannungsgeschwindigkeit*


Shields parameter
: The {cite:t}`shields_anwendung_1936` parameter $\tau_{x,cr}$ (in the literature also often named $\theta_{cr}$) is a dimensionless value of critical bed shear stress for sediment mobility. For this reason, the Shields parameter is also often referred to as **dimensionless critical bed shear stress**. Flow conditions and grain sizes with a {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` $\tau_x$ smaller than the Shields parameter curve are considered immobile. Vice versa, flow conditions and grains associated with a {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` larger than the Shields parameter are considered mobile. In fully turbulent flow, the Shields parameter can be considered a constant value of approximately 0.047$\pm$0.15 {cite:p}`von_karman_mechanische_1930,kramer_modellgeschiebe_1932,smart_sedimenttransport_1983`. To evaluate if a grain is in motion, its {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` value is plotted against its dimensionless diameter $D_x$ in the so-called Shields diagram (also referred to as the *Hunter-Rouse* {cite:p}`rouse_critical_1965` diagram). $D_x$ is calculated for any grain with a diameter $D_{pq}$ (in m) as {cite:p}`einstein_bed-load_1950`:

  $$
  D_x = \left[\frac{(s-1)\cdot g}{\nu^2}\right]^{1/3}\cdot D_{pq}
  $$

  where $s$ is the ratio of sediment grain and water density (typically 2.68); $g$ is gravitational acceleration; and $\nu$ is the kinematic viscosity of water ($\approx$10$^{-6}$m$^{2}$ s$^{-1}$) {cite:p}`schwindt_hydro-morphological_2017`. Read the definition of {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` for the calculation of $\tau_{x}$. {numref}`Figure %s <shields-diagram>` shows the Shields diagram where the Shields curve is plotted based on descriptions in {cite:t}`guo_logarithmic_2002`.

  ```{figure} ../img/shields-diagram.jpg
  :alt: Shields diagram guo hunter critical bed shear stress
  :name: shields-diagram

Der Shields-Parameter $\tau_{x,cr}$ (kritische dimensionslose Bettscherspannung) für die Kornmobilität in Abhängigkeit vom dimensionslosen Teilchendurchmesser $D_x$, laut {cite:t}`guo_logarithmic_2002` (Bildquelle: {cite:t}`schwindt_hydro-morphological_2017`).
  ```

Über die Korngröße und die lokale Hydrodynamik hinaus ist $\tau_{x,cr}$ auch eine Funktion der globalen Kanalrauhigkeit und Steigung, der relativen Unter- und Bettlasttransportintensität {cite:p}`wilcock_critical_1993,gregoretti_inception_2008,lamb_is_2008,recking_bed-load_2008,ferguson_river_2012`.

Spawning guild
: Verschiedene Gruppen von Fischen (d.h. {term}`fish guilds <Guild>`) haben unterschiedliche Praktiken und Präferenzen für das Laichen ihrer Eier. Bei Ökohydraulischen wird z.B. zwischen {term}`fish guilds <Guild>` unterschieden, die es vorziehen, Nester in der Oberfläche des Flussbettes zu bauen (*lithophilous*) oder ihre Eier zu sedimentieren (*psamnophilous*) oder Pflanzen (*phytophilous*). Auch *pelagophile* Fische geben ihre Eier in das frei fließende Wasser frei.

Aufgehängte Last
: Aufgehängte Last ist eine spezielle Art von {term}`Sediment transport`, die die Verschiebung von feinen Partikeln mit dem Massenstrom beschreibt.

*Französisch: Transport en suspension<br>German: Schwebstofftransport*

SMS 2dm
: SMS (Surface-water Modeling System) ist eine proprietäre Software-Suite von *Aquaveo* für Oberflächenwassermodellierung. `2dm`-Dateiformat wird natives mit SMS produziert und stellt ein Rechennetz mit x, y und z-Koordinaten von Knoten zusammen mit Knoten-IDs dar. Die [developer's wiki](https://www.xmswiki.com/wiki/SMS:2D_Mesh_Files_*.2dm) bietet eine umfassende Beschreibung des Dateiformats.

Sonar
: Schallnavigation und Reichweite (*Sonar*) ist eine Technik zur Ortung von Objekten im Raum und Unterwasser durch Aussendung von Schallimpulsen. Ein aktives *Sonar*-System, wie Funkerkennung und Reichweite (*radar*), sendet und empfängt Schallsignale zur Abbildung von Objekten unter Wasser (Zeit-of-Flight-Messung). Passive *Sonar* erfasst Signale, die von einem Objekt selbst emittiert werden (z.B. Vibrationen von Fischbewegung oder Walfänger), kann aber keine genauen Abbildungen von Unterwasserobjekten vornehmen.

SRS
: Siehe {term}`CRS`.

Phasenauslastung
: Eine Phasen-Entladungs-Beziehung (auch als **Ratingkurve** bezeichnet) zeigt die Entladung (in m$^3$/s oder CFS) in Abhängigkeit von der Wasseroberflächen-Elevationsfunktion (in m über dem Meeresspiegel oder ft) bei einem bestimmten Flussquerschnitt. Die meisten Strommessstationen haben eine regelmäßig kalibrierte Phasenentladungsbeziehung, die oft von einer staatlichen Behörde gehalten wird. Deshalb sind es meistens staatliche Behörden, die online Bühnen-Entladungsfunktionen für ihre Vermessungsstationen bereitstellen, wie zum Beispiel der bayerische Staat an der [Mühldorf am Innlehr](https://www.hnd.bayern.de/pegel/donau_bis_passau/muehldorf-18004506/abflusstafel?).

*Französisch: Courbe d'étalonnage / Courbe hauteur-débit / Courbe de tarage<br>German: Wasserstands-Abfluss Beziehung, bzw. Abflusskurve / Abflussschlüsselkurve / Eichkurve*

Schritt Pool
: Step-Pools sind eine Art von morphologischen Einheiten, die typischerweise in steilen Bergflüssen gefunden. Sie zeichnen sich durch hohe Gradienten (über 2%) und eine raue Oberfläche aus Cobble und bedrock {cite:p}`gonda2008characteristics`.

STL
: Das Standard Tessellation Language (STL)-Dateiformat ist in einem dreidimensionalen (3d)-Druck-CAD-Software-Typ namens [stereolithography](https://en.wikipedia.org/wiki/Stereolithography). Eine STL-Datei beschreibt 3d-Strukturen in Form von unstrukturierten triangulierten Oberflächen mit beliebigen Einheiten.

In den Warenkorb
: Der Begriff Talweg stammt aus der alten deutschen Rechtschreibung für das Tal (heute: *Tal*) und sollte besser als *Talweg* bezeichnet werden. Die buchstäbliche Übersetzung von Talweg ist Talweg und bezieht sich ursprünglich auf eine Linie, die die tiefsten Punkte der Talquerschnittsprofile längs verbindet. Geomorphologen verwenden manchmal leicht verschiedene Definitionen von Talweg. Das internationale Recht ist ausdrücklicher, wenn es sich um den Talweg als primärer navigierbarer Kanal bei Boardern zwischen zwei Ländern handelt.

*Französisch: talweg / thalweg<br>German: Talweg*

Topographic change
: Topographic change is the increase or decrease in elevation of the Earth's surface as a function of time. Conceptually, tracking topographic changes could consist of a simple comparison (i.e., subtraction) of elevation changes at two different moments. However, topographic change detection is not quite that simple, since every measurement technique has spatial inaccuracies with regards to the exact location and elevation of recorded points. For this reason, methods have been developed that, based on a level of detection (LoD), generate topographic change maps conveying and accounting for spatial uncertainty. Depending on the method, either strict global LoD raster {cite:p}`pasternack_flood-driven_2017` or less strict pixel-based LoD values {cite:p}`wheaton_accounting_2010` are used to remove uncertainty from topographic change maps. Topographic change maps also enable the visualization of soil loss (i.e., erosion), which is a growing challenge for agriculture and beyond. To this end, the USGS developed a publicly available website that is dedicated to topographic change (visit [https://usgs.gov](https://www.usgs.gov/core-science-systems/eros/topochange)).

*Französisch: Changement du Gelände (non-technique) <br>German: Topografischer Wandel (kein technischer Begriff)*

Turbulenzen
: Siehe {term}`Reynolds-averaged Navier-Stokes <RANS>`gleichungen.

Turbulent kinetic energy
: Turbulence kinetic energy (TKE, or $k$ in this eBook) is the mean kinetic energy per unit mass associated with turbulent eddies. It is measured as the quadratic velocity fluctuations. In a river or lab flume, TKE can be indirectly measured with an Acoustic Doppler Velocimeter (ADV) that enables to derive the streamwise ($u_x$ or just $u$), later/spanwise ($u_y$ or $v$), and vertical ($u_z$ or $w$) velocity fluctuations (i.e., $u'_x$, $u'_y$, and $u'_z$, respectively) with the following expression {cite:p}`nikora_adv_1998,kundu_fluid_2008`:

  $$
  k = \frac{1}{2} \cdot \left( {\overline{{u'_x}^{2}} + \overline{{u'_y}^{2}} + \overline{{u'_z}^{2}}} \right)
  $$ (eq-tke)

  Thus, $k$ is the half trace of the Reynolds stress tensor (see {term}`RANS`) {cite:p}`franca_turbulence_2015`. For evaluating $k$ in field or lab experiments, have a look at our Python packages [TKE-calculator (standalone scripts)](https://tke-calculator.readthedocs.io) and [TKE-analyst (pip-installer)](https://tkeanalyst.readthedocs.io).

  In numerics, the TKE ($k$) is calculated by turbulence closure methods, such as the $k$-$\epsilon$ closure, which are required for numerically solving the {term}`Reynolds-averaged Navier-Stokes <RANS>` equations.

xdmf
: The [eXtensible Data Model and Format (XDMF)](https://www.xdmf.org/) library provides standard routines for exchanging (scientific) datasets that result from high performance computing (HPC) tasks. XDMF files redundantly store *light* and *heavy* data in XML and HDF5 format and *Python* interfaces exist for both formats. Thus, XDMF or XMF files are often linked to a `*.h4` or `*.h5` ({term}`HDF`) file that contains heavy simulation datasets.
````
