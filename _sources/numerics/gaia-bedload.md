(gaia-bl)=
# Bedload

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/e6lk2pk72Gc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Bedload traveling in a lab flume by jumping, rolling, and sliding (under water footage). Source: Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

```{admonition} Bedload basics
:class: important

For a better learning experience, the {ref}`glossary` helps with explanations of the terms {term}`Sediment transport`, (dimensionless) {term}`bedload <Bedload>` transport $\Phi_b$, {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` $\tau_{x}$, and the {term}`Shields parameter` $\tau_{x,cr}$ (in this order).
```

```{admonition} Sediment replenishment, gravel augmentation, bedload addition (etc.)
:class: tip

The placement of coarser sediment for the restoration of bedload transport can take many different forms and it is described by a broad range of terms. In TELEMAC, the best option for simulating such bedload restoration efforts is the [**Nestor**](http://www.opentelemac.org/index.php/modules-list/163-dredgesim-modeling-dredging-operations-in-the-river-bed) module that requires Gaia (or SISYPHE). Read more in the most recent {{ nestor }}.
```

(bl-principles)=
## Principles

The calculation of {term}`bedload <Bedload>` transport requires expert knowledge about the modeled ecosystem for judging whether the system is sediment supply-limited or transport capacity-limited {cite:p}`church_morphodynamics_2015`.

Sediment supply-limited rivers
: A sediment supply-limited river is characterized by clearly visible incision trends indicating that the river's runoff could potentially transport more sediment than is available in the river. Sediment-supply limited river sections typically occur downstream of dams, which represent an insurmountable barrier for sediment. Thus, in a supply-limited river, the **flow competence** (hydrodynamic force or **transport capacity**) is insufficient to mobilize a typically coarse riverbed, but it is sufficient for transporting external sediment supply.

Transport capacity-limited (alluvial) rivers
: A transport capacity-limited river is characterized by sediment abundance where the river's runoff is too small to transport all available sediment during a flood. Sediment accumulations (i.e., the alluvium) are present and the channel tends to braid into {term}`anabranches <Anabranch>`. Thus, the **flow competence** (or **transport capacity**) is insufficient to transport the entire amount of available sediment (external supply and riverbed).

```{admonition} Limitation types vary in space and in time
:class: important
The channel types may strongly vary in space between river sections or segments and in time. For instance, the same river section that appears to be supply-limited because of insufficient flow competence may turn into a transport capacity-limited section during a flood when high discharges exert high shear stresses on the riverbed. The spatio-temporal variation of transport limitation types is particularly pronounced in near-census, healthy river ecosystems that are perpetually adjusting to a morphodynamic equilibrium.
```

The following figures feature sediment supply-limited river sections and a transport capacity-limited river section.

`````{tab-set}
````{tab-item} Artificially sediment supply-limited
```{figure} ../img/nature/doubs-capacity-2015.JPG
:height: 350px
:alt: channel doubs france sediment supply transport limited
:name: doubs-2015

The Doubs in the Franche-Comté (France) during a small flood. The sediment supply is interrupted by a cascade of dams upstream with the consequence of a straight monotonous channel with significant plant growth along the banks. The riverbed primarily consists of boulders that are immobile most of the time. Thus, the river section can be characterized as artificially sediment supply-limited (picture: Sebastian Schwindt 2015).
```
````

````{tab-item} Naturally sediment supply-limited
```{figure} ../img/nature/krimmler-ache-2010.jpg
:height: 350px
:alt: naturally channel krimmler ache austria sediment supply transport limited
:name: krimml-2010
:class: with-shadow

The Krimmler Ache in Austria during a small flood event. Even though the watershed has a high {term}`Sediment yield`, the transport capacity of the water in this river section is so high that the riverbed predominantly consists of large boulders. Thus, the river section can be characterized as naturally sediment supply-limited (picture: Sebastian Schwindt 2010).
```
````

````{tab-item} Capacity-limited
```{figure} ../img/nature/jenbach-alluvial-2020.jpg
:height: 350px
:alt: alluvial channel jenbach sediment supply transport limited
:name: jenbach-2020

The Jenbach in the Bavarian Alps (Germany) after an intense natural sediment supply in an upstream reach in the form of a landslide. The river section can be characterized as transport capacity-limited (picture: Sebastian Schwindt 2020).
```
````
`````

**Why is the differentiation between sediment supply and transport capacity-limited rivers important for numerical modeling?**

Gaia provides different formulae for calculating bedload transport, which are partially either derived from lab experiments with infinite sediment supply (e.g., the {cite:t}`meyer-peter_formulas_1948` formula and its derivates, see {ref}`below <gaia-mpm>`) or from field measurements in partially transport capacity-limited rivers (e.g., {cite:t}`wilcock_critical_1993`). Formulae that account for limited sediment supply often involve a correction factor for the {term}`Shields parameter`.

## Formulae and Parameters

{term}`Bedload` is typically designated with $q_b$ (in kg$\cdot$s$^{-1}\cdot$m$^{-1}$ i.e. weight per unit time and width) and accounts for particulate transport in the form of the displacement of rolling, sliding, and/or jumping coarse particles. In river hydraulics, the so-called {term}`Dimensionless bed shear stress`, also referred to as {term}`Shields parameter` {cite:p}`shields_anwendung_1936`, is often used as a threshold value for the mobilization of sediment from the riverbed. TELEMAC and Gaia build on a dimensionless expression of bedload transport intensity according to {cite:t}`einstein_bed-load_1950`:

$$
\Phi_b = \frac{q_b}{\rho_{s} \sqrt{(s - 1) g D^{3}_{pq}}}
$$ (eq-phi-gaia)

where $\rho_{s}$ is the density of sediment grains; $s$ is the ratio of sediment grain and water density (typically 2.68) {cite:p}`schwindt_hydro-morphological_2017`; $g$ is gravitational acceleration; and $D_{pq}$ is the characteristic grain diameter of the sediment class (cf. {ref}`gaia-sed`). Note that the dimensionless expression $\Phi$ and the dimensional expression $q_{b}$ represent unit bedload (i.e., bedload normalized by a unit of width). **Gaia outputs are dimensional and correspond to $q_{b}$** (recall the **VARIABLES FOR GRAPHIC PRINTOUTS** definitions in the {ref}`General Parameters section <gaia-gen>`) where the unit of width corresponds to the edge length of a numerical mesh cell over which the mass fluxes are calculated.

```{admonition} Comment on the Original Einstein (1950) Expression
:class: dropdown
The original equation for $\Phi_b$ can be found on page 34 (Equation 42) in {cite:t}`einstein_bed-load_1950`. This formula involves an additional division by the gravitational acceleration $g$, which does not appear in later references to the Einstein expression of $\Phi_b$ and would also not result in a dimensionless term. For this reason, Equation {eq}`eq-phi-gaia` is adapted here.
```

Equation {eq}`eq-phi-gaia` expresses only the dimensional conversion for bedload transport (i.e., the way how dimensions are removed or added to sediment transport). In fact, this is only the first step to solve the other side of a bedload equation using a (semi-) empirical formula. To calculate $\Phi_{b}$, Gaia provides a set of (semi-) empirical formulae, which can be modified with user Fortran files and defined in the Gaia steering file with the **BED-LOAD TRANSPORT FORMULA FOR ALL SANDS** `integer` keyword. {numref}`Table %s <tab-gaia-bl-formulae>` lists possible integers for the keyword to define a bedload transport formulae, including references to original publications, formula application ranges, and the names of the Fortran source files for modifications.

```{csv-table} *Bedload transport formulae implemented in Gaia with application limits regarding the grain diameter $D$, **cross section-averaged** Froude number $Fr$, slope $S$, water depth $h$, and flow velocity $u$. The Fortran files live in the TELEMAC source/gaia directory.*
:header: Gaia, Author(s), $D$, "*{term}`Fr <Froude number>`*; $S$; $h$; and $u$", User Fortran
:header-rows: 1
:widths: 10, 50, 30, 35, 15
:name: tab-gaia-bl-formulae
"(no.)", "(ref.)", "(10$^{-3}$m)", "(-); (-); (m); (m/s)", "(file name)"
`1`, "{cite:t}`meyer-peter_formulas_1948`", 0.4 $<D_{50}<$28.6, "10$^{-4}<Fr<$639<br> 0.0004$<S<$0.02<br>0.01$<h<$1.2<br>0.2$<u$", [bedload_meyer_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__meyer__gaia_8f.html)
`2`, "{cite:t}`einstein_bed-load_1950`-{cite:t}`brown1949`", 0.25$<D_{35}<$32, "", [bedload_einst.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__einst__gaia_8f.html)
 `3`, {cite:t}`engelund_monograph_1967`, 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", [bedload_engel_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__engel__gaia_8f.html)
 `30`, "{cite:t}`engelund_monograph_1967,chollet1979`", 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", [bedload_engel_cc_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__engel__cc__gaia_8f.html)
 `7`, {cite:t}`van_rijn_sediment_1984`, 0.6$<D_{50}<$2.0, "0.5$<h$<br>0.2$<u$", [bedload_vanrijn_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__vanrijn__gaia_8f.html)
 `10`, {cite:t}`wilcock2003`,"0.063 $\lesssim D_{pq}$", "", [bedload_wilcock_crowe_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__wilcock__crowe__gaia_8f.html)
```

To use the {cite:t}`meyer-peter_formulas_1948` formula (`1` according to  {numref}`Tab. %s <tab-gaia-bl-formulae>`) in this tutorial, **add the following line to the gaia-morphdynamics.cas steering file**:

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
Users can add more bedload transport formulae by adding a modified copy of a FORTRAN file template. The {{ gaia }} explains the procedure for adding a new user-defined bedload formula in detail in section 6.3.
```

```{admonition} User Fortran Files
:class: note, dropdown
To implement a user Fortran file, copy the original TELEMAC Fortran file from the `/telemac/v8p2/sources/` directory (e.g., `/telemac/v8p2/sources/gaia/bedload_einst_gaia.f`) to the project directory (e.g., `/telemac/v8p2/simulations/gaia-tutorial/user_fortran/bedload_einst_gaia.f`). Finally, tell TELEMAC where to look for user fortran files by defining the following keyword in a steering file (e.g., in `gaia-morphodynamics.cas`):

`FORTRAN FILE : 'user_fortran'`
```

(gaia-mpm)=
### Meyer-Peter and Müller (1948)

```{admonition} Recall the validity range for the MPM formula (1)
:class: warning
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

The {cite:t}`meyer-peter_formulas_1948` formula was published in 1948 by Swiss researchers Eugen Meyer-Peter, professor at [ETH Zurich](https://ethz.ch/en.html) and founder of the school's hydraulics laboratory (Zurich's famous [VAW](https://vaw.ethz.ch/)), and Robert Müller. Their empirical formula is the result of more than a decade of collaboration and the elaboration began one year after the VAW was founded in 1931 when Robert Müller was appointed assistant to Eugen Meyer-Peter. The two scientists also worked with Henry Favre and Hans-Albert Einstein who came up with another approach for calculating bedload. An early version of the {cite:t}`meyer-peter_formulas_1948` formula was published in 1934 and it is the basis for many other formulas that refer to a critical {term}`Dimensionless bed shear stress` (i.e., {term}`Shields parameter`). It is important to remember that the formula is based on data from lab flume experiments with high sediment supply. This is why bedload transport calculated with the {cite:t}`meyer-peter_formulas_1948` formula corresponds to the {ref}`hydraulic transport capacity <bl-principles>` of an alluvial channel. Thus, **the {cite:t}`meyer-peter_formulas_1948` formula tends to overestimate bedload transport** and it is inherently designed for estimating bedload **based on simplified 1d cross section-averaged hydraulics** (see also the {ref}`Python sediment transport exercise <ex-py-sediment>`). Good results can be expected when flood flows are simulated in an alluvial river section.

Ultimately, the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) can be calculated with the {cite:t}`meyer-peter_formulas_1948` formula as follows:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x,cr} > \tau_{x} \\ f_{mpm} \cdot (\tau_{x} - \tau_{x,cr})^{3/2} & \mbox{ if } \tau_{x,cr} \leq \tau_{x}\end{cases}
$$ (eq-mpm)

where $f_{mpm}$ is the MPM coefficient (default is 8), $\tau_{x,cr}$ denotes the {term}`Shields parameter` ($\approx$ 0.047 and up to 0.07 in mountain rivers), and $\tau_{x}$ is the {term}`Dimensionless bed shear stress`. When using the {cite:t}`meyer-peter_formulas_1948` formula with Gaia, consistency with original publications is **ensured by defining $\tau_{x,cr}$ and $f_{mpm}$ in the steering file**:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1 / see above
CLASSES SHIELDS PARAMETERS : 0.047;0.047;0.047
MPM COEFFICIENT : 8
```

````{admonition} Wong-Parker correction of the MPM formula
The Wong-Parker {cite:p}`wong_reanalysis_2006` correction for the {cite:t}`meyer-peter_formulas_1948` formula refers to a statistical re-analysis of the original experimental datasets and applies to {term}`Plane bed` river sections. To this end, the Wong-Parker correction yields lower bedload transport values and it excludes the form drag correction of the original formula with the following expression: $\Phi_{b} \approx 3.97 \cdot (\tau_{x} - 0.0495)^{3/2}$. Thus, to implement the Wong-Parker correction in Gaia use:

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
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

Hans Albert Einstein, son of the famous Albert Einstein, was a pioneer of probability-based analyses of sediment transport. In particular, he hypothesized that the beginning and the end of sediment motion can be expressed in terms of probabilities. Furthermore, Einstein assumed that sediment motion is a series of step-wise displacements followed by rest periods and that the average distance of a particle displacement is approximately a hundred times the particle (grain) diameter. Moreover, to account for observations he made in lab flume experiments, Einstein introduced hiding and lifting correction coefficients {cite:p}`einstein1942`.

The Einstein formula differs from any {cite:t}`meyer-peter_formulas_1948`-based formula in that it does not imply a threshold for incipient motion of sediment. However, despite or because Einstein's sediment transport theory is significantly more complex than many other bedload transport formulae, it did not become very popular in engineering applications. Today, Gaia enables the user-friendly application of Einstein's formula, which was similarly presented by {cite:t}`brown1949` at an engineering hydraulic conference in 1949. According to {cite:t}`einstein1942`-{cite:t}`brown1949`, the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) is calculated as follows:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x} < 0.0025 \\ F_{eb}\cdot 2.15 \cdot \exp{(-0.391/\tau_{x})} & \mbox{ if } 0.0025 \leq \tau_{x} \leq 0.2\\ F_{eb} \cdot  40 \cdot \tau_{x}^{3} & \mbox{ if } \tau_{x} > 0.2  \tau_{x}\end{cases}
$$ (eq-einstein-brown)

where

$$
F_{eb} = \left(\frac{2}{3} + \frac{36}{D_x}\right)^{0.5} - \left(\frac{36}{D_x}\right)^{0.5}
$$ (eq-f-eb)

$D_x$ is the dimensionless particle diameter calculated as:

$$
D_x = \left[\frac{(s-1)\cdot g}{\nu^2}\right]^{1/3}\cdot D_{pq}
$$ (eq-d-dimless)

where $s$ is the ratio of sediment grain and water density (typically 2.68); $g$ is gravitational acceleration; and $\nu$ is the kinematic viscosity of water ($\approx$10$^{-6}$m$^{2}$ s$^{-1}$) {cite:p}`schwindt_hydro-morphological_2017`.

To use the {cite:t}`einstein1942`-{cite:t}`brown1949` formulae in Gaia use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 2
```

```{admonition} Consider adapting bedload_einst.f
The application thresholds as a function of $\tau_{x}$ stem from the Gaia Fortran file [bedload_einst.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__einst__gaia_8f.html). However, the original {cite:t}`einstein1942`-{cite:t}`brown1949` publications suggest a threshold of $\tau_{x}$=0.182 (rather than 0.2) for switching the formula cases.
```


(gaia-engelund)=
### Engelund-Hansen (1967) / Chollet-Cunge

```{admonition} Recall the validity range for the Engelund-Hansen formulae (3 and 30)
:class: warning
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

The {cite:t}`engelund_monograph_1967` formula accounts for total sediment transport including {term}`Bedload` and {term}`Suspended load`. Starting from the Bagnold power-approach {cite:p}`bagnold_approach_1966,bagnold_empirical_1980`, the {cite:t}`engelund_monograph_1967` formula was developed for sediment transport calculations over dune channel beds. The approach accounts for energy losses required to drive particles uphill on dunes of the riverbed. The {cite:t}`bagnold_approach_1966` theory considers the total shear as the sum of the shear transmitted between grains and the fluid, and the shear transmitted by momentum changes caused by intergranular collisions. Thus, erosion takes place as long as the {term}`Dimensionless bed shear stress` is greater or equal to its critical value (i.e., the {term}`Shields parameter`). Gaia implements the {cite:t}`engelund_monograph_1967` by calculating the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) as follows:

$$
\Phi_b = 0.05\cdot \frac{f^{2.5}_{eh}}{c_f}
$$ (eq-engelund)

where $c_f$ is a friction coefficient that accounts for form drag and skin friction (calculated with the hydrodynamics in Telemac2d/3d). Read more about skin friction in the {ref}`correction factors <c-friction>` section. The $f_{eh}$ factor is a function of the {term}`Dimensionless bed shear stress` $\tau_{x}$. To use the {cite:t}`engelund_monograph_1967` formula in Gaia use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 30
```

In addition, {cite:t}`chollet1979` introduced a step-wise function for the calculation of $f_{eh}$:

$$
f_{eh} = \begin{cases} 0 & \mbox{ if } \tau_{x} \leq 0.06 & \mbox{ (no transport)}\\ [2.5 (\tau_{x} - 0.06)]^{0.5} & \mbox{ if } 0.06 < \tau_{x} < 0.384  & \mbox{ (dunes)} \\ 1.066\cdot \tau_{x}^{0.176} & \mbox{ if } 0.384 < \tau_{x} < 1.08  & \mbox{ (transitional)} \\ \tau_{x} & \mbox{ if } 1.08 \leq \tau_{x}  & \mbox{ (sheet flow)} \end{cases}
$$ (eq-f-eh)

To apply the correction {cite:t}`chollet1979` adaption of the {cite:t}`engelund_monograph_1967` formula use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 3
```

(gaia-rijn)=
### van Rijn (1984)

```{admonition} Recall the validity range for the van-Rijn formula (7)
:class: warning
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

The sediment transport formula from Leo van Rijn {cite:p}`van_rijn_sediment_1984` is inspired by the theories from {cite:t}`bagnold_empirical_1980`, {cite:t}`einstein1942`, and {cite:t}`ackers_sediment_1973`. The {cite:t}`van_rijn_sediment_1984` formulae assume that bedload is dominated by gravity while suspended load transport is controlled by turbulence according to {cite:t}`bagnold_empirical_1980`. To this end, the {cite:t}`van_rijn_sediment_1984` formulae calculate bedload transport similar to {cite:t}`ackers_sediment_1973` where transport rates depend on friction velocities. To calibrate his near-bed (bedload) solid transport model, {cite:t}`van_rijn_sediment_1984` used data from experiments on flat-bed (zero-slope) channels with an average sediment grain diameter of 1.8 mm. {cite:t}`van_rijn_sediment_1984` conducted additional experiments to vet the results of his model against varying grain diameters between 0.2 and 2 mm. In addition, {cite:t}`van_rijn_sediment_1984` established criteria for sediment suspension based on laboratory experiments with grain diameters of less than 0.5 mm and by simplifying calibration parameters empirically. While the original {cite:t}`van_rijn_sediment_1984` formula accounts for total sediment transport (i.e., {term}`Bedload` and {term}`Suspended load`), the following explanations for the implementation in Gaia are limited to {term}`Bedload` only.

According to {cite:t}`van_rijn_sediment_1984`, the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) is calculated as follows:

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

```{admonition} Applicability of the Wilcock-Crow formula (10)
:class: warning
The multi-fraction bedload transport formula from {cite:t}`wilcock2003` does not state particular validity ranges, but the authors restrict their approach to sand-gravel-cobble sediments with a minimum grain diameter of 0.063 mm. The explanations in this section limit to the application background of the {cite:t}`wilcock2003` approach. The complex set of equations is explained in detail in the {{ gaia }} (section 3.1.2) and by {cite:t}`cordier2019,cordier2020`.
```

The {cite:t}`wilcock2003` approach is a multi-fraction sediment transport model that is primarily applicable in armored river sections for modeling bed aggradation or degradation. The approach takes up the idea of {cite:t}`parker1990` on applying a reference shear stress at which little but constant solid transport rate can be observed. The reference shear stress is close to, but a little bit larger than the {term}`Shields parameter` $\tau_{x,cr}$. To this end, {cite:t}`wilcock2003` implement a reference transport rate of 0.002 as proposed by {cite:t}`parker1990`.

Moreover, the multi-fraction {cite:t}`wilcock2003` model uses the complete sediment grain size distribution of the riverbed surface and calculates bedload transport for each of the specified grain size classes (starting with the smallest grain size). The sediment transport model builds on flume experiments from {cite:t}`proffitt1983` and {cite:t}`parker1990`, and it accounts for hiding/exposure effects on gravel transport as a function of the sand fraction in the riverbed.

In a nutshell, the {cite:t}`wilcock2003` model represents a further development of the {cite:t}`meyer-peter_formulas_1948` formula, takes up the implementation of a reference transport rate {cite:p}`parker1990`, and it is calibrated to hiding/exposure effects as a function of the sand fraction.

The calculation of {term}`Bedload` transport according to {cite:t}`wilcock2003` starts with a definition of a dimensionless transport capacity $\Phi_i$ per sediment fraction that removes dimensions from the bedload transport rate computed with a third-party formula for that fraction only (e.g., the {cite:t}`meyer-peter_formulas_1948` formula).

To use the {cite:t}`wilcock2003` formula in Gaia, define multiple {ref}`sediment classes <gaia-sed>` and use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 10
```

(c-factors)=
## Correction Factors

Correction factors for sediment transport may be needed to account for transversal channel slope, secondary currents, or skin friction correction.

(c-friction)=
### Friction Correctors

Friction is often considered with simplified approaches lumping together skin friction and form drag, but in a two-dimensional model, only skin friction affects bedload. {cite:t}`einstein_bed-load_1950` accounts for skin friction with a correction factor $f_{fr}$ for (dimensional) bed shear stress $\tau$:

$$
\tau' = f_{fr} \cdot \tau
$$ (eq-tau-fr)

```{admonition} How Telemac2d calculates $\tau$
Telemac2d uses the length of the $x$-$y$ velocity vectors to calculate $\tau$ with the user-defined `FRICTION COEFFICIENT` $c_{f}$: $\tau = 0.5\cdot \rho_{w}\cdot c_{f}\cdot (U^2 + V^2)$.
```

The correction factor $f_{fr}$ is defined as the ratio of the global friction coefficient $c_{f}$ (i.e., lumped skin friction and form drag) and the skin friction-only coefficient $c'_{f}$:

$$
f_{fr} = \frac{c'_{f}}{c_{f}}
$$ (eq-f-fr)

The skin friction-only coefficient is calculated as:

$$
c'_{f} = 2\cdot \left(\frac{\kappa}{log(12 h/ k'_{s})}\right)^{2}
$$ (eq-cf-skin)

where $\kappa$ is the {cite:t}`von_karman_mechanische_1930` constant (0.4), $h$ is water depth, and $k'_{s}$ is the representative roughness length, which is often assumed as a multiple of the characteristic grain size (read more in the section on {ref}`bedload calibration <bl-calibration>`).

`````{tab-set}
````{tab-item} Skin Friction
Gaia uses by default the skin friction correction coefficient that it derives from the hydrodynamic solver (i.e., Telemac2d/3d). In very shallow waters, this behavior might cause instabilities. Therefore, the **SKIN FRICTION CORRECTION** (integer on-off, default is `1`) keyword can be defined in Gaia to disable the correction factor calculation and setting $f_{fr}$ to 1. To disable skin friction correction (i.e., set $f_{fr}$ to 1), add the following to the Gaia steering file (not used in this tutorial):

```fortran
SKIN FRICTION CORRECTION : 0 / default is 1 to enable skin friction correction
```

On ripple riverbeds (i.e., fine sandy hills as typically observed at ocean beaches during low tides), the skin friction correction should be set to `2` for enabling a bedform predictor. Read more in section 3.1.8 of the {{ gaia }}.
````

````{tab-item} Bedform Roughness
The finer the sediment of the riverbed, the more important turbulence created by the bed shape becomes. For instance, skin friction calculated based on a multiple of the diameter of a sand grain's characteristic roughness length $k'_{s}$ is very small. However, sand tends to shape the riverbed into ripple or dune forms, which cause additional *bedform turbulence*, as featured in the video below.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/q4eRwyeLKfA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>by Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

By default, Gaia does not account for turbulence (i.e., roughness effects) of bedforms, but it can be enabled by setting the **COMPUTE BED ROUGHNESS AT SEDIMENT SCALE** keyword to `YES` (default is `NO`). Then, one of the following options for the **BED ROUGHNESS PREDICTOR OPTION** keyword can be defined:

* `1` for using the default approach of using a multiple of the characteristic grain diameter for calculating $k'_{s}$ in Equation {eq}`eq-cf-skin`.
* `2` for ripple bedforms with waves and currents as a function of flow velocity and the characteristics grain size {cite:p}`rijn2007,wiberg1994`.
* `3` for ripple bedforms with currents only as a function of flow velocity, water depth, the characteristic grain size, and an additional sand grain diameter {cite:p}`rijn2007,huybrechts2010`.

The {{ gaia }} (section 3.1.9) summarizes the set of equations that go into the calculation of the **BED ROUGHNESS PREDICTOR OPTION**.

````
`````

(gaia-dir)=
### Direction and Magnitude (Intensity)

Natural rivers are characterized by non-straight lines of the {term}`Thalweg`, which involves that water and sediment are subjected to curve effects. However, water and sediment behave differently in a curve because sediment has greater inertia than water {cite:p}`mosselman_five_2016`. Gaia accounts for the inertia of sediment transport as a function of water depth, curve radius, a spiral flow coefficient (`A`), and the depth-averaged, 2d velocities *U* and *V*. In addition, sediment transport reacts more inert to horizontal (transversal) channel slope and can be considered in $x$ and $y$ directions (see also the explanation of the {term}`Exner equation`). To this end, Gaia calculates the slope-corrected unit bedload transport $q_{b,sc}$ as follows:

$$
q_{b,sc} = q_{b} \left[1 + \beta \left(\cos \alpha  \frac{\partial z_{b}}{\partial x} + \sin \alpha \frac{\partial z_{b}}{\partial y} \right)\right]
$$ (eq-qb-corr)

where $\alpha$ is the angle between the longitudinal channel ($x$) axis and the bedload transport vector (see also the {term}`Exner equation`), $\beta$ is an empiric bedload intensity correction factor from {cite:t}`koch1980`, and $z_{b}$ is the riverbed elevation.

The degree of bedload deviation (through $\alpha$) and the $\beta$ factor can be defined in Gaia with the **FORMULA FOR DEVIATION** and **FORMULA FOR SLOPE EFFECT** (horizontal) keywords. To use one or both keywords, the **SLOPE EFFECT** keyword must be set to `YES` (disable by setting it to `NO`).

The **FORMULA FOR DEVIATION** keyword can take the following integer values to define a particular formula for the sediment shape function (cf. section 3.1.4 in {{ gaia }}):

* `1` for bed level computation according to {cite:t}`koch1980` (**default**).
* `2` for the {cite:t}`talmon1995` approach based on laboratory experiments, which should be used with the **PARAMETER FOR DEVIATION** keyword for setting the `BETA2` parameter (its default is `PARAMETER FOR DEVIATION : 0.85`, but an optimum was found with `1.6` {cite:p}`mendoza2017`).

The  **FORMULA FOR SLOPE EFFECT** keyword affects not only the direction of sediment transport but also the bedload magnitude (or intensity) and it can take the following values:

* `1` for bed level computation according to {cite:t}`koch1980` (**default** and similar to FORMULA FOR DEVIATION). The `1`-setting enables the definition of the empiric bed slope correction factor $\beta$ in Equation {eq}`eq-qb-corr` through the **BETA** keyword (default is `BETA : 1.3`).
  - To increase bed elevation change, increase **BETA**.
  - To decrease bed elevation change, decrease **BETA**.
* `2` for slope correction in sand-bed rivers based on an approach from {cite:t}`soulsby1997`, which applies a correction of the {term}`Shields parameter` as a function of the friction angle of the sediment and the riverbed slope. The friction angle can be defined with the additional **FRICTION ANGLE OF THE SEDIMENT** keyword (default is `40.`).

(gaia-secondary)=
### Secondary Currents

Secondary currents may occur in curved channels (i.e., in most near-census natural rivers) where water moves like a gyroscope through river bends. More specifically, secondary flows are helical motions in which water near the surface is driven toward the outer bend, while water near the riverbed is driven toward the inner bend. Thus, secondary flows are a 3d phenomenon that can be represented in 2d models only with auxiliary approaches. For {term}`Bedload` transport, the near-bed current toward the inner bend is especially important, because it promotes erosion at the outer bend and may lead to deposition at the inner bend.

By default, Telemac2d and Gaia do not consider secondary currents, but an approach based on {cite:t}`engelund1974` can be enabled by setting the **SECONDARY CURRENTS** keyword to `YES` (default is `NO`). In addition, the **SECONDARY CURRENTS ALPHA COEFFICIENT** keyword can be used to adapt the roughness length as a function of channel bottom roughness (i.e., smooth or rough riverbeds). For instance, use `SECONDARY CURRENTS ALPHA COEFFICIENT : 0.75` for a very rough riverbed, or `SECONDARY CURRENTS ALPHA COEFFICIENT : 1.` (default) for a smooth riverbed. For **this tutorial use**:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SECONDARY CURRENTS : YES
SECONDARY CURRENTS ALPHA COEFFICIENT : 0.8
```

(gaia-bc-bl)=
## Boundary Conditions

The {ref}`Gaia Basis section on boundary conditions <gaia-bc>` explains the geometric definition of open liquid boundaries in the `*.cli` files. To prescribe a bedload transport of **10 kg$^3\cdot$s$^{-1}$** across the upstream (`LIEBOR=5`) boundary and free outflow at the downstream (`LIEBOR=4`) boundary, **add the PRESCRIBED SOLID DISCHARGES keyword to the Gaia steering file (gaia-morphodynamics.cas)**:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
PRESCRIBED SOLID DISCHARGES : 10.;0.
```

Recall that the first and second values in the list of prescribed solid discharges refer to the first and second open boundary listed in the `boundaries-gaia.cli`, respectively (i.e., upstream and downstream in that order).

```{admonition} Porosity and PRESCRIBED SOLID DISCHARGES
:class: important
The **PRESCRIBED SOLID DISCHARGES** keyword makes TELEMAC calculate sediment mass balances accounting for the riverbed porosity $\epsilon$. Thus, the solid mass flux printouts correspond to $q_{b}/(1-\epsilon)$.
```

Gaia can be run with liquid boundary files for assigning time-dependent solid discharges (the outflow should be kept in equilibrium). Solid discharge time series can be implemented using `455`-`5` boundary definitions, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. For more guidance, have a look at the *yen-2d* example (`telemac/v8p2/examples/gaia/yen-2d`) featuring a quasi-steady bedload simulation at the Rhine River. In addition, more background information about the definition of bedload boundary conditions can be found in section 3.1.11 in the {{ gaia }}.

## Example Applications

Examples for the implementation of bedload come along with the TELEMAC installation (in the `/telemac/v8p2/examples/gaia/` directory). The following examples in the `gaia/` folder feature (pure) bedload calculations:

* Application of the {ref}`Wilcock-Crowe formula <gaia-wilcock>` (multiple sediment classes): **wilcock_crowe-t2d/**
* Bedload in a bend of the Rhine River with quasi steady (unsteady) flow conditions: **yen-2d/**
* Bedload coupled with Telemac3d: **bosse-t3d/**
* Model of an armored (stratified) riverbed: **guenter-t2d/**
* Coastal sand (bedload) transport coupled with the wave propagation module Tomawac: **littoral-t2d-tom/**
* Coupling with the dredging module Nestor: **nestor_dig_test-t2d/**
* Finite Volume solver featuring time-dependent solid discharge in a `*.liq`: **flume_bc-t2d/**
