---
description: Referenztabelle der mathematischen Notation, Symbole, lateinische und griechische Buchstaben verwendet in dieser hydro-informatik eBook für hydraulische und Wasserressourcen-Engineering.
---

# Notierung

Die konsequente Verwendung von Parametern und Symbolen für Parameter ist in einer Notationstabelle mit Symbolen, zugehörigen Parameterdefinitionen und Parametereinheiten zusammengefasst. {numref}`Table %s <tab-notation-latin>` und {numref}`Table %s <tab-notation-greek>` Liste lateinische und griechische Buchstaben (Symbole) in diesem eBook verwendet.


```{list-table} Latin letters (symbols) and parameters used in this eBook (in alphabetical order).
:header-rows: 1
:name: tab-notation-latin

* - Schreiben
  - Einheit
  - Warenbezeichnung

* - $A$
  - m$^2$
  - Strömungsquerschnitt

* - $B$
  - m
  - Kanalbreite an der Wasseroberfläche

* - $b$
  - m
  - Kanal Bodenbreite

* - $b_m$
  - m
  - mittlere Strömungsbreite

* - $c_{cfl}$
  - $-$
  - Courant-Friedrichs-Lewy ({term}`CFL`)

* - $C$
  - G l$^{-1}$
  - Tiefengemittelte suspendierte Sedimentkonzentration (vgl. Gleichung {eq}`eq-ade-2d`)

* - $C_{eq}$
  - G l$^{-1}$
  - Gleichgewicht bei Bett (Referenzniveau) suspendierte Sedimentkonzentration (vgl. {ref}`gaia-sl-formulae`)

* - $C_{z_{ref}}$
  - G l$^{-1}$
  - Nahbett suspendierte Sedimentkonzentration an der Referenzhöhe $z_{ref}$

* - $C_{D}$
  - $-$
  - Drag Koeffizient (vgl. {term}`Settling velocity`)

* - $C_{w1}$
  - $-$
  - Spalart-Allmaras Schließkonstante im Vernichtungsterm ($\approx 0.3$)

* - $c_{f}$
  - $-$
  - {ref}`combined form drag and skin friction coefficient <c-friction>`

* - $c'_{f}$
  - $-$
  - {ref}`skin friction coefficient <c-friction>` (Equity {eq}`eq-cf-skin`)

* - $c_{mud}$
  - G l$^{-1}$
  - Feinstoffkonzentration (mud) (vgl. Gleichung {eq}`eq-gaia-dep`)

* - $c_{\varepsilon}$
  - $-$
  - Konvergenzkonstante (vgl. Gleichung {eq}`error_lim`)

* - $cHSI$
  - Index
  - kombinierter Lebensraumtauglichkeitsindex

* - $D$
  - m$^2$
  - Diffusionskoeffizient (oder Diffusivität)

* - $D_{m}$
  - m
  - mittlerer Korndurchmesser eines Sedimentgemisches

* - $D_{pq}$
  - m
  - Korndurchmesser, davon $pq$~$\%$ der Mischung feiner

* - $D_{x}$
  - m
  - dimensionsloser Korndurchmesser (vgl. Gleichung {eq}`eq-d-dimless` und {term}`Shields parameter`)

* - $Fr$
  - $-$
  - {term}`Froude number`

* - $f_D$
  - $-$
  - Darcy-Weisbach Reibfaktor

* - $F_{eb}$
  - $-$
  - Einstein-Brown (EB) Faktor (Equation {eq}`eq-f-eb`

* - $f_{eh}$
  - $-$
  - Faktor in der Bettlastgleichung Engelund und Hansen {eq}`eq-f-eh`

* - $f_{fr}$
  - $-$
  - Reibungskorrekturfaktor für Bettscherbeanspruchung (Equation {eq}`eq-f-fr`)

* - $f_{k'_{s}}$
  - $-$
  - {ref}`ratio between skin friction and mean diameter <bl-calibration>`

* - $f_{mpm}$
  - $-$
  - Meyer-Peter und Müller (MPM) Faktor (Equation {eq}`eq-mpm`)

* - $f_w$
  - $-$
  - Spalart-Allmaras Nahwandkorrekturfunktion im Vernichtungsterm

* - $g$
  - m s$^{-2}$
  - Schwerkraftbeschleunigung

* - $HSI$
  - Index
  - Lebensfähigkeitsindex

* - $h$
  - m
  - Wassertiefe

* - $i$ oder `i`
  - $-$
  - ebene ein skalar iterator (1d space)

* - $j$ oder `j`
  - $-$
  - Ebene zwei Skalar Iterator (2d Raum)

* - `k`
  - $-$
  - Ebene drei Skalar Iterator (3d Raum)

* - $k$
  - m$^2$s@s$^{-2}$ oder J kg$^{-1}$
  - {term}`turbulent kinetic energy <Turbulent kinetic energy>`

* - $k_s$
  - m
  - Gesamtbett Rauhigkeitslänge (Höhe)

* - $k'_{s}$
  - m
  - Hautreibungsrauhlänge (vgl. Gleichung {eq}`eq-cf-skin`)

* - $k_{sr}$
  - m
  - Ripled-Bett Rauheitslänge (vgl. {ref}`gaia-sl-formulae`)

* - $k_{st}$
  - m$^{1/3}$ s$^{-1}$
  - Strickler Rauheitskoeffizient (fictive Einheiten)

* - $l_w$
  - m
  - kürzester Abstand von einem Mesh-Knoten zur nächstgelegenen festen seitlichen Begrenzung (Wandabstand); verwendet im Spalart-Allmaras-Vernichtungsterm

* - $M$
  - kg m$^{-2}$ s$^{-1}$
  - {cite:t}`partheniades1965` Erosionskonstante (vgl. Gleichung {eq}`eq-gaia-erosion`)

* - $m$
  - $-$
  - Kanal Bank Hang

* - $N$
  - $-$
  - Zielwert eines Matrix-Iterators

* - $n$
  - $-$
  - Zielwert eines Skalar iterators

* - $n_m$
  - m$^{-1/3}$
  - Rauhigkeitskoeffizient von Manning (Fictive Units)

* - $P$
  - m
  - benetzter Umfang

* - $Pr$
  - $-$
  - Wahrscheinlichkeit

* - $Q$ (auch $Q_i$ oder $Q_j$)
  - m$^3$ s$^{-1}$
  - Entladung (Wasser), Flussmittel oder Volumenstrom

* - $q$
  - m$^2$ s$^{-1}$
  - Einheitsentladung

* - $Q_{b}$
  - S$^{-1}$
  - Bettlasttransport (Kapazität)

* - $Q_{b * cr}$
  - S$^{-1}$
  - dimensionslose Bettlasttransport (Kapazität)

* - $q_{b}$
  - kg s$^{-1}$ m$^{-1}$
  - Einheit Bettlasttransport (Kapazität)

* - $q_{b,sc}$
  - kg s$^{-1}$ m$^{-1}$
  - {ref}`slope-corrected <gaia-dir>` Einheit Bettlasttransport (Kapazität)

* - $Q_{bf}$
  - m$^3$ s$^{-1}$
  - Bankvollentladung

* - $q_{s}$
  - kg s$^{-1}$ m$^{-1}$
  - Einheit Sedimenttransportkapazität

* - $q_{s,dep}$
  - kg s$^{-1}$ m$^{-1}$
  - Einheit suspendierter Abscheidungsfluss (Equenz {eq}`eq-gaia-dep`)

* - $q_{s,dep}$
  - kg s$^{-1}$ m$^{-1}$
  - Einheit ausgesetzter Erosionsfluss (Equation {eq}`eq-gaia-erosion`)

* - $Re$
  - $-$
  - Reynolds-Nummer

* - $Re_p$
  - $-$
  - Partikel-Reynolds-Nummer ($Re_p = w_s D / \nu$, cf. {ref}`gaia-sl-sed`)

* - $R_h$
  - m
  - Hydraulikradius

* - $S$
  - $-$
  - Pisten

* - $S_0$
  - $-$
  - Kanalschräge

* - $S_{e}$
  - $-$
  - Energiesteig

* - $s$
  - $-$
  - Verhältnis von Sedimentkorn und Wasserdichte

* - $T$
  - Jahre
  - Wiederholungsintervall

* - $t$
  - S
  - Zeit, Dauer

* - $u$ oder $u_j$ oder $u_k$
  - m s$^{-1}$
  - Strömungsgeschwindigkeit in $x$, $j$ und $k$-Richtung

* - $\mathbf{u}$ (bold)
  - m s$^{-1}$
  - Strömungsgeschwindigkeitsvektor (multidimensional)

* - $u_{*}$
  - m s$^{-1}$
  - Schergeschwindigkeit

* - $u_{cr}$
  - m s$^{-1}$
  - kritische Schergeschwindigkeit bei Schlammabscheidung (vgl. Gleichung {eq}`eq-gaia-dep`)

* - $w_{s}$
  - m s$^{-1}$
  - Einstellgeschwindigkeit (vgl. Gleichung {eq}`eq-ws-stokes` und {term}`Settling velocity`)

* - $w_{s,h}$
  - m s$^{-1}$
  - gehinderte Absetzgeschwindigkeit bei hohen Konzentrationen (vgl. {ref}`gaia-sl-sed`)

* - $wse$
  - m a.s.l.
  - Wasseroberflächenhöhe (absolut)

* - $x$
  - m
  - strömungsmäßige Koordinaten, die in die stromaufwärts gerichtete Richtung weisen, oder die Ostung von Geodaten

* - $y$
  - m
  - spanweise Koordinaten, die auf die rechte Bank oder die Nordierung von Geodaten zeigen

* - $z$
  - m
  - vertikale Koordinaten, die auf den Gravitationsbeschleunigungsvektor zeigen

* - $z_{b}$
  - m oder m
  - Flussbetthöhe zeigt gegen den Schwerkraftbeschleunigungsvektor

* - $z_{ref}$
  - m
  - Bezugshöhe (Near-Bett) für suspendierten Sedimentaustausch (vgl. {ref}`gaia-sl-formulae`)
```


```{list-table} Greek letters (symbols) and parameters used in this eBook (in alphabetical order).
:header-rows: 1
:name: tab-notation-greek

* - Schreiben
  - Einheit
  - Warenbezeichnung

* - $\alpha$
  - *rad* oder *deg*
  - Winkel zwischen Längskanal ($x$) und Massentransportvektor

* - $\alpha_{k_s}$
  - $-$
  - Verhältnis zwischen Hautreibungsrauhigkeit und mittlerem Korndurchmesser ({ref}`RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER <bl-calibration>`Keyword; gleiche Menge wie $f_{k'_{s}}$)

* - $\beta$
  - $-$
  - empirischer Intensitätskorrekturfaktor (z.B. in {ref}`Gaia <gaia-dir>`)

* - $\Delta {t}$
  - oder Jahre
  - Zeitdauer (Dauer) oder Zeitschrittlänge

* - $\Delta {x}$
  - m
  - horizontale Entfernung oder Zellgröße in $x$-Richtung

* - $\Delta {y}$
  - m
  - Abstand oder Zellgröße in $y$-Richtung

* - $\Delta {z}$
  - m
  - Höhenunterschied oder Zellgröße in $z$-Richtung

* - $\epsilon$
  - $-$
  - Porosität

* - $\varepsilon$
  - var.
  - absoluter Fehler zwischen zwei Mengen (siehe Gleichung {eq}`error_rate`)

* - $\varepsilon_s$
  - m$^{2}$ s$^{-1}$
  - Sedimentturbulente Diffusivität (vgl. Gleichung {eq}`eq-diff-sed`)

* - $\eta$
  - m
  - aktive Schichtdicke

* - $\eta_L$
  - $-$
  - Kolmogorov Länge Skala

* - $\eta_T$
  - $-$
  - Kolmogorov Zeitskala

* - $\eta_U$
  - $-$
  - Kolmogorov Geschwindigkeitsskala

* - $\theta'$
  - $-$
  - skin-friction–korrigiert {term}`Dimensionless bed shear stress` ($\theta' = \mu\theta$), d.h. die in den Suspensionsformeln verwendete {term}`Shields parameter`-Skala-Schere; entspricht $\tau_{x}$ mit Hautreibungskorrektur (vgl. {ref}`gaia-sl-formulae`)

* - $\theta_{cr}$
  - $-$
  - kritisch {term}`Shields parameter` (entspricht $\tau_{x,cr}$)

* - $\nabla$
  - $-$
  - Operator-Vektor (*nabla*) von Teildifferenzen $\frac{\partial}{\partial x_i}$, wobei $x_i$ die Abmessungen des Flussfeldes {cite:p}`kundu_fluid_2008`

* - $\mu$ = $\nu \cdot \rho_w$
  - kg m$^{-1}$ s$^{-1}$
  - dynamische Viskosität

* - $\nu$ = $\mu \cdot \rho_w^{-1}$
  - m$^{2}$ s$^{-1}$
  - kinematische Viskosität

* - $\nu_t$
  - m$^{2}$ s$^{-1}$
  - eddy (turbulent) Viskosität

* - $\tilde{\nu}$
  - m$^{2}$ s$^{-1}$
  - modifizierte turbulente kinematische Viskosität; Transportvariable im Spalart-Allmaras Turbulenzmodell

* - $\Phi$
  - $-$
  - besonders{term}`Sediment transport`

* - $\Phi_b$
  - $-$
  - dimensionslos {term}`Bedload`transport

* - $\phi$
  - $-$
  - volumetrische Sedimentkonzentration (vgl. behindertes Absetzen, {ref}`gaia-sl-sed`)

* - $\psi$
  - Variable
  - Konstante eines transportierten Partikels (Substanz)

* - $\rho_s$
  - m$^{-3}$
  - Sedimentkorndichte

* - $\rho_w$
  - m$^{-3}$
  - Wasserdichte

* - $\sigma_s$
  - $-$
  - Schmidt-Nummer, die die Sedimentdiffundivität der Eddy-Viskosität betrifft (vgl. Gleichung {eq}`eq-diff-sed`; Gaia korrigiert $\sigma_s = 1.0$)

* - $\tau$
  - N m$^{-2}$
  - Bettscherbeanspruchung

* - $\tau_{cr}$
  - N m$^{-2}$
  - Critical Maß Bettscherbeanspruchung (vgl. Gleichung {eq}`eq-gaia-erosion`)

* - $\tau_x$
  - $-$
  - {term}`Dimensionless bed shear stress`

* - $\tau_{x,cr}$
  - $-$
  - Critical {term}`Dimensionless bed shear stress` oder {term}`Shields parameter`

```
