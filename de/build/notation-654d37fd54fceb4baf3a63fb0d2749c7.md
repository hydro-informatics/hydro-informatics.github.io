---
description: Referenztabelle mit mathematischen Notationen, Symbolen, lateinischen und griechischen Buchstaben, die in diesem Hydroinformatik-E-Book für Hydraulik und Wasserressourcentechnik verwendet werden.
---

# Notation

Die konsistente Verwendung von Parametern und Symbolen für Parameter wird in einer Notationstabelle mit Symbolen, zugehörigen Parameterdefinitionen und Parametereinheiten zusammengefasst. {numref}`Table %s <tab-notation-latin>` und {numref}`Table %s <tab-notation-greek>` listet lateinische und griechische Buchstaben (Symbole) auf, die in diesem eBook verwendet werden.


```{list-table} Latin letters (symbols) and parameters used in this eBook (in alphabetical order).
:header-rows: 1
:name: tab-notation-latin

* - Schreiben
  - Einheit
  - Beschreibung

* - $A$
  - m$^2$
  - Strömungsquerschnitt

* - $B$
  - m
  - Kanalbreite an der Wasseroberfläche

* - $b$
  - m
  - Kanalbodenbreite

* - $b_m$
  - m
  - mittlere Strömungsbreite

* - $c_{cfl}$
  - $-$
  - Courant-Friedrichs-Lewy ({term}`CFL`) Bedingung

* - $C$
  - g l$^{-1}$
  - Tiefengemittelte suspendierte Sedimentkonzentration (vgl. Gleichung {eq}`eq-ade-2d`)

* - $C_{eq}$
  - g l$^{-1}$
  - Gleichgewicht nahe dem Bett (Referenzebene) suspendierte Sedimentkonzentration (vgl. {ref}`gaia-sl-formulae`)

* - $C_{z_{ref}}$
  - g l$^{-1}$
  - In der Nähe von Bett suspendierte Sedimentkonzentration an der Referenzhöhe $z_{ref}$

* - $C_{D}$
  - $-$
  - Luftwiderstandskoeffizient (vgl. {term}`Settling velocity`)

* - $C_{w1}$
  - $-$
  - Spalart-Allmaras Verschlusskonstante im Zerstörungsterm ($\approx 0.3$)

* - $c_{f}$
  - $-$
  - {ref}`combined form drag and skin friction coefficient <c-friction>`

* - $c'_{f}$
  - $-$
  - {ref}`skin friction coefficient <c-friction>` (Gleichung {eq}`eq-cf-skin`)

* - $c_{mud}$
  - g l$^{-1}$
  - fine material (mud) concentration (cf. Equation {eq}`eq-gaia-dep`)

* - $c_{\varepsilon}$
  - $-$
  - Konvergenzkonstante (vgl. Gleichung {eq}`error_lim`)

* - $cHSI$
  - Index
  - Kombinierter Lebensraumeignungsindex

* - $D$
  - m$^2$s/s
  - Diffusionskoeffizient (oder Diffusivität)

* - $D_{m}$
  - m
  - mittlerer Korndurchmesser einer Sedimentmischung

* - $D_{pq}$
  - m
  - grain diameter of which $pq$~$\%$ of the mixture are finer

* - $D_{x}$
  - m
  - dimensionsloser Korndurchmesser (vgl. Gleichung {eq}`eq-d-dimless` und {term}`Shields parameter`)

* - $Fr$
  - $-$
  - {term}`Froude number`

* - $f_D$
  - $-$
  - Reibungsfaktor Darcy-Weisbach

* - $F_{eb}$
  - $-$
  - Einstein-Brown (EB) Faktor (Gleichung {eq}`eq-f-eb`)

* - $f_{eh}$
  - $-$
  - Faktor in der Engelund und Hansen Bettlast Gleichung {eq}`eq-f-eh`

* - $f_{fr}$
  - $-$
  - Reibungskorrekturfaktor für Bettscherbeanspruchung (Gleichung {eq}`eq-f-fr`)

* - $f_{k'_{s}}$
  - $-$
  - {ref}`ratio between skin friction and mean diameter <bl-calibration>`

* - $f_{mpm}$
  - $-$
  - Meyer-Peter und Müller (MPM) Faktor (Gleichung {eq}`eq-mpm`)

* - $f_w$
  - $-$
  - Spalart-Allmaras wandnahe Korrekturfunktion im Zerstörungsterm

* - $g$
  - m s$^{-2}$
  - Gravitationsbeschleunigung

* - $HSI$
  - Index
  - Lebensraumeignungsindex

* - $h$
  - m
  - Wassertiefe

* - $i$ oder `i`
  - $-$
  - Level 1 skalarer Iterator (1d-Raum)

* - $j$ oder `j`
  - $-$
  - Ebene zwei skalarer Iterator (2d-Raum)

* - `k`
  - $-$
  - Level 3 skalarer Iterator (3D-Raum)

* - $k$
  - m$^2$s@s$^{-2}$ oder J kg$^{-1}$
  - {term}`turbulent kinetic energy <Turbulent kinetic energy>`

* - $k_s$
  - m
  - Gesamtrauhigkeitslänge (Höhe)

* - $k'_{s}$
  - m
  - Rauheitslänge der Hautreibung (vgl. Gleichung {eq}`eq-cf-skin`)

* - $k_{sr}$
  - m
  - Rauheitslänge der Rillen (vgl. {ref}`gaia-sl-formulae`)

* - $k_{st}$
  - m$^{1/3}$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - Rauheitskoeffizient des Streichers (fiktive Einheiten)

* - $l_w$
  - m
  - kürzester Abstand von einem Maschenknoten zur nächstgelegenen festen lateralen Grenze (Wandabstand), verwendet im Begriff Spalart-Allmaras-Vernichtung

* - $M$
  - kg m$^{-2}$ s$^{-1}$
  - {cite:t}`partheniades1965` Erosionskonstante (vgl. Gleichung {eq}`eq-gaia-erosion`)

* - $m$
  - $-$
  - Kanalbankhang

* - $N$
  - $-$
  - Sollwert eines Matrix-Iterators

* - $n$
  - $-$
  - Zielwert eines skalaren Iterators

* - $n_m$
  - m$^{-1/3}$s
  - Manning-Rauheitskoeffizient (fiktive Einheiten)

* - $P$
  - m
  - benetzter Umfang

* - $Pr$
  - $-$
  - Wahrscheinlichkeit

* - $Q$ (auch $Q_i$ oder $Q_j$)
  - m$^3$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - Abfluss (Wasser), Flüsse oder Volumenstrom

* - $q$
  - m$^2$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - Einheitsentladung

* - $Q_{b}$
  - kg s$^{-1}$
  - Bettlasttransport (Kapazität)

* - $Q_{b * cr}$
  - kg s$^{-1}$
  - dimensionsloser Bettlasttransport (Kapazität)

* - $q_{b}$
  - kg s$^{-1}$m$^{-1}$
  - Bettlasttransport (Kapazität)

* - $q_{b,sc}$
  - kg s$^{-1}$m$^{-1}$
  - {ref}`slope-corrected <gaia-dir>` Bettlasttransport (Kapazität)

* - $Q_{bf}$
  - m$^3$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - Bankvollständige Entladung

* - $q_{s}$
  - kg s$^{-1}$m$^{-1}$
  - Transportkapazität von Sedimenteinheiten

* - $q_{s,dep}$
  - kg s$^{-1}$m$^{-1}$
  - Unit Suspended Deposition Flux (Gleichung {eq}`eq-gaia-dep`)

* - $q_{s,dep}$
  - kg s$^{-1}$m$^{-1}$
  - Unit Suspended Erosion Flux (Gleichung {eq}`eq-gaia-erosion`)

* - $Re$
  - $-$
  - Reynolds-Nummer

* - $Re_p$
  - $-$
  - Partikel Reynolds-Nummer ($Re_p = w_s D / \nu$, cf. {ref}`gaia-sl-sed`)

* - $R_h$
  - m
  - Hydraulikradius

* - $S$
  - $-$
  - Steigung

* - $S_0$
  - $-$
  - Kanalsteigung

* - $S_{e}$
  - $-$
  - Energiehang

* - $s$
  - $-$
  - Verhältnis von Sedimentkorn und Wasserdichte

* - $T$
  - Jahre
  - Wiederholungsintervall

* - $t$
  - s
  - Zeit, Dauer

* - $u$ oder $u_j$ oder $u_k$
  - m s$^{-1}$
  - flow velocity in $x$, $j$, and $k$ directions, respectively

* - $\mathbf{u}$ (fett)
  - m s$^{-1}$
  - Strömungsgeschwindigkeitsvektor (mehrdimensional)

* - $u_{*}$
  - m s$^{-1}$
  - Schergeschwindigkeit

* - $u_{cr}$
  - m s$^{-1}$
  - kritische Schergeschwindigkeit für die Schlammablagerung (vgl. Gleichung {eq}`eq-gaia-dep`)

* - $w_{s}$
  - m s$^{-1}$
  - Einschwinggeschwindigkeit (vgl. Gleichung {eq}`eq-ws-stokes` und {term}`Settling velocity`)

* - $w_{s,h}$
  - m s$^{-1}$
  - Verhinderte Absetzgeschwindigkeit bei hohen Konzentrationen (vgl. {ref}`gaia-sl-sed`)

* - $wse$
  - m a.s.l.
  - Wasseroberflächenhöhe (absolut)

* - $x$
  - m
  - stromweise Koordinaten, die in stromaufwärts gerichtet sind, oder Ostung von Geodaten

* - $y$
  - m
  - spanweise Koordinaten, die zum rechten Ufer zeigen, oder Nordung von Geodaten

* - $z$
  - m
  - vertikale Koordinate, die gegen den Gravitationsbeschleunigungsvektor zeigt

* - $z_{b}$
  - m oder m a.s.l.
  - Höhe des Flussbettes, die gegen den Gravitationsbeschleunigungsvektor zeigt

* - $z_{ref}$
  - m
  - Referenzhöhe (Nahbett) für den Austausch suspendierter Sedimente (vgl. {ref}`gaia-sl-formulae`)
```


```{list-table} Greek letters (symbols) and parameters used in this eBook (in alphabetical order).
:header-rows: 1
:name: tab-notation-greek

* - Schreiben
  - Einheit
  - Beschreibung

* - $\alpha$
  - *rad* oder *deg*
  - Winkel zwischen der Längsachse ($x$) und einem Massentransportvektor

* - $\alpha_{k_s}$
  - $-$
  - Verhältnis zwischen Rauheit der Hautreibung und mittlerem Korndurchmesser ({ref}`RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER <bl-calibration>` Schlüsselwort; gleiche Menge wie $f_{k'_{s}}$)

* - $\beta$
  - $-$
  - empiric bedload intensity correction factor (e.g., in {ref}`Gaia <gaia-dir>`)

* - $\Delta {t}$
  - s oder Jahre
  - Zeitraum (Dauer) oder Zeitschrittlänge

* - $\Delta {x}$
  - m
  - horizontal distance or cell size in $x$-direction

* - $\Delta {y}$
  - m
  - spanwise distance or cell size in $y$-direction

* - $\Delta {z}$
  - m
  - difference in height or cell size in $z$-direction

* - $\epsilon$
  - $-$
  - Porosität

* - $\varepsilon$
  - var.
  - Absoluter Fehler zwischen zwei Größen (siehe Gleichung {eq}`error_rate`)

* - $\varepsilon_s$
  - m$^{2}$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - Sediment turbulente Diffusivität (vgl. Gleichung {eq}`eq-diff-sed`)

* - $\eta$
  - m
  - Aktivschichtdicke

* - $\eta_L$
  - $-$
  - Kolmogorov Längenskala

* - $\eta_T$
  - $-$
  - Kolmogorov Zeitskala

* - $\eta_U$
  - $-$
  - Kolmogorov Geschwindigkeitsskala

* - $\theta'$
  - $-$
  - Haut-Reibung-korrigiert {term}`Dimensionless bed shear stress` ($\theta' = \mu\theta$), d.h. die {term}`Shields parameter`-Schere, die in den Suspensionsformeln verwendet wird; entspricht $\tau_{x}$ mit Hautreibungskorrektur (vgl. {ref}`gaia-sl-formulae`)

* - $\theta_{cr}$
  - $-$
  - kritisch {term}`Shields parameter` (entspricht $\tau_{x,cr}$)

* - $\nabla$
  - $-$
  - Operatorvektor (*nabla*) von partiellen Differentialen $\frac{\partial}{\partial x_i}$, wobei $x_i$ sich auf die Dimensionen des Flussfeldes bezieht {cite:p}`kundu_fluid_2008`

* - $\mu$= $\nu \cdot \rho_w$
  - kg m$^{-1}$ s$^{-1}$
  - dynamische Viskosität

* - $\nu$= $\mu \cdot \rho_w^{-1}$
  - m$^{2}$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - kinematische Viskosität

* - $\nu_t$
  - m$^{2}$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - Verwirbelungsviskosität

* - $\tilde{\nu}$
  - m$^{2}$s@s@s$^{-1}$s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s@s
  - modifizierte turbulente kinematische Viskosität; Transportvariable im Spalart-Allmaras Turbulenzmodell

* - $\Phi$
  - $-$
  - dimensionslos {term}`Sediment transport`

* - $\Phi_b$
  - $-$
  - dimensionless {term}`Bedload` transport

* - $\phi$
  - $-$
  - volumetrische Sedimentkonzentration (vgl. gehindertes Absetzen, {ref}`gaia-sl-sed`)

* - $\psi$
  - variabel
  - Konstante eines transportierten Teilchens (Substanz)

* - $\rho_s$
  - kg m$^{-3}$
  - Sedimentkorndichte

* - $\rho_w$
  - kg m$^{-3}$
  - Dichte des Wassers

* - $\sigma_s$
  - $-$
  - Schmidt-Zahl in Bezug auf die Sedimentdiffusion zur Wirbelviskosität (vgl. Gleichung {eq}`eq-diff-sed`; Gaia fixiert $\sigma_s = 1.0$)

* - $\tau$
  - N m$^{-2}$
  - Bettscherspannung

* - $\tau_{cr}$
  - N m$^{-2}$
  - Kritische dimensionale Bettscherspannung (vgl. Gleichung {eq}`eq-gaia-erosion`)

* - $\tau_x$
  - $-$
  - {term}`Dimensionless bed shear stress`

* - $\tau_{x,cr}$
  - $-$
  - Kritisch {term}`Dimensionless bed shear stress` oder {term}`Shields parameter`

```
