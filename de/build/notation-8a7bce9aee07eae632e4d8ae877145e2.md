---
description: Referenztabelle der mathematischen Notation, Symbole, lateinische und griechische Buchstaben verwendet in dieser hydro-informatik eBook für hydraulische und Wasserressourcen-Engineering.
---

# Notierung

Die konsequente Verwendung von Parametern und Symbolen für Parameter ist in einer Notationstabelle mit Symbolen, zugehörigen Parameterdefinitionen und Parametereinheiten zusammengefasst. {numref}`Table %s <tab-notation-latin>` und {numref}`Table %s <tab-notation-greek>` Liste lateinische und griechische Buchstaben (Symbole) in diesem eBook verwendet.


```{list-table} Latin letters (symbols) and parameters used in this eBook (in alphabetical order).
:header-rows: 1
:name: tab-notation-latin

* - Brief
- Einheit
- Beschreibung

* - $A$
  - m$^2$
  - flow cross section

* - $B$
  - m
  - channel width at the water surface

* - $b$
  - m
  - channel bottom width

* - $b_m$
  - m
  - mean flow width

* - $c_{cfl}$
  - $-$
  - Courant-Friedrichs-Lewy ({term}`CFL`) condition

* - $C$
  - g l$^{-1}$
  - depth-averaged suspended sediment concentration (cf. Equation {eq}`eq-ade-2d`)

* - $C_{eq}$
  - g l$^{-1}$
  - equilibrium near-bed (reference-level) suspended sediment concentration (cf. {ref}`gaia-sl-formulae`)

* - $C_{z_{ref}}$
  - g l$^{-1}$
  - near-bed suspended sediment concentration at the reference elevation $z_{ref}$

* - $C_{D}$
  - $-$
  - drag coefficient (cf. {term}`Settling velocity`)

* - $C_{w1}$
  - $-$
  - Spalart-Allmaras closure constant in the destruction term ($\approx 0.3$)

* - $c_{f}$
  - $-$
  - {ref}`combined form drag and skin friction coefficient <c-friction>`

* - $c'_{f}$
  - $-$
  - {ref}`skin friction coefficient <c-friction>` (Equation {eq}`eq-cf-skin`)

* - $c_{mud}$
  - g l$^{-1}$
  - fine material (mud) concentration (cf. Equation {eq}`eq-gaia-dep`)

* - $c_{\varepsilon}$
  - $-$
  - convergence constant (cf. Equation {eq}`error_lim`)

* - $cHSI$
  - index
  - combined habitat suitability index

* - $D$
  - m$^2$/s
  - diffusion coefficient (or diffusivity)

* - $D_{m}$
  - m
  - mean grain diameter of a sediment mixture

* - $D_{pq}$
  - m
  - grain diameter of which $pq$~$\%$ of the mixture are finer

* - $D_{x}$
  - m
  - dimensionless grain diameter (cf. Equation {eq}`eq-d-dimless` and {term}`Shields parameter`)

* - $Fr$
  - $-$
  - {term}`Froude number`

* - $f_D$
  - $-$
  - Darcy-Weisbach friction factor

* - $F_{eb}$
  - $-$
  - Einstein-Brown (EB) factor (Equation {eq}`eq-f-eb`)

* - $f_{eh}$
  - $-$
  - factor in the Engelund and Hansen bedload equation {eq}`eq-f-eh`

* - $f_{fr}$
  - $-$
  - friction correction factor for bed shear stress (Equation {eq}`eq-f-fr`)

* - $f_{k'_{s}}$
  - $-$
  - {ref}`ratio between skin friction and mean diameter <bl-calibration>`

* - $f_{mpm}$
  - $-$
  - Meyer-Peter and Müller (MPM) factor (Equation {eq}`eq-mpm`)

* - $f_w$
  - $-$
  - Spalart-Allmaras near-wall correction function in the destruction term

* - $g$
  - m s$^{-2}$
  - gravitational acceleration

* - $HSI$
  - index
  - habitat suitability index

* - $h$
  - m
  - water depth

* $i$ oder `i`
- $-$
- Ebene ein Skalar Iterator (1d Raum)

* $j$ oder `j`
- $-$
- Ebene zwei Skalar Iterator (2d Raum)

* - `k`
  - $-$
  - level three scalar iterator (3d space)

* - $k$
  - m$^2$ s$^{-2}$ or J kg$^{-1}$
  - {term}`turbulent kinetic energy <Turbulent kinetic energy>`

* - $k_s$
  - m
  - total bed roughness length (height)

* - $k'_{s}$
  - m
  - skin friction roughness length (cf. Equation {eq}`eq-cf-skin`)

* - $k_{sr}$
  - m
  - rippled-bed roughness length (cf. {ref}`gaia-sl-formulae`)

* - $k_{st}$
  - m$^{1/3}$ s$^{-1}$
  - Strickler roughness coefficient (fictive units)

* - $l_w$
  - m
  - shortest distance from a mesh node to the nearest solid lateral boundary (wall distance); used in the Spalart-Allmaras destruction term

* - $M$
  - kg m$^{-2}$ s$^{-1}$
  - {cite:t}`partheniades1965` erosion constant (cf. Equation {eq}`eq-gaia-erosion`)

* - $m$
  - $-$
  - channel bank slope

* - $N$
  - $-$
  - target value of a matrix iterator

* - $n$
  - $-$
  - target value of a scalar iterator

* - $n_m$
  - m$^{-1/3}$ s
  - Manning's roughness coefficient (fictive units)

* - $P$
  - m
  - wetted perimeter

* - $Pr$
  - $-$
  - probability

* - $Q$ (auch $Q_i$ oder $Q_j$)
- m$^3$ s$^{-1}$
- Ableitung (Wasser), Flussmittel oder Volumenstrom

* - $q$
  - m$^2$ s$^{-1}$
  - unit discharge

* - $Q_{b}$
  - kg s$^{-1}$
  - bed load transport (capacity)

* - $Q_{b * cr}$
  - kg s$^{-1}$
  - dimensionless bed load transport (capacity)

* - $q_{b}$
  - kg s$^{-1}$ m$^{-1}$
  - unit bedload transport (capacity)

* - $q_{b,sc}$
  - kg s$^{-1}$ m$^{-1}$
  - {ref}`slope-corrected <gaia-dir>` unit bedload transport (capacity)

* - $Q_{bf}$
  - m$^3$ s$^{-1}$
  - bank-full discharge

* - $q_{s}$
  - kg s$^{-1}$ m$^{-1}$
  - unit sediment transport capacity

* - $q_{s,dep}$
  - kg s$^{-1}$ m$^{-1}$
  - unit suspended deposition flux (Equation {eq}`eq-gaia-dep`)

* - $q_{s,dep}$
  - kg s$^{-1}$ m$^{-1}$
  - unit suspended erosion flux (Equation {eq}`eq-gaia-erosion`)

* - $Re$
  - $-$
  - Reynolds number

* - $Re_p$
  - $-$
  - particle Reynolds number ($Re_p = w_s D / \nu$, cf. {ref}`gaia-sl-sed`)

* - $R_h$
  - m
  - hydraulic radius

* - $S$
  - $-$
  - slope

* - $S_0$
  - $-$
  - channel slope

* - $S_{e}$
  - $-$
  - energy slope

* - $s$
  - $-$
  - ratio of sediment grain and water density

* - $T$
  - years
  - recurrence interval

* - $t$
  - s
  - time, duration

* - $u$ oder $u_j$ oder $u_k$
- m s$^{-1}$
- Strömungsgeschwindigkeit in $x$, $j$ und $k$

* - $\mathbf{u}$ (bold)
- m s$^{-1}$
- Strömungsgeschwindigkeitsvektor (multidimensional)

* - $u_{*}$
  - m s$^{-1}$
  - shear velocity

* - $u_{cr}$
  - m s$^{-1}$
  - critical shear velocity for mud deposition (cf. Equation {eq}`eq-gaia-dep`)

* - $w_{s}$
  - m s$^{-1}$
  - settling velocity (cf. Equation {eq}`eq-ws-stokes` and {term}`Settling velocity`)

* - $w_{s,h}$
  - m s$^{-1}$
  - hindered settling velocity at high concentrations (cf. {ref}`gaia-sl-sed`)

* - $wse$
  - m a.s.l.
  - water surface elevation (absolute)

* - $x$
  - m
  - streamwise coordinate pointing in the upstream direction, or Easting of geodata

* - $y$
  - m
  - spanwise coordinate pointing toward the right bank, or Northing of geodata

* - $z$
  - m
  - vertical coordinate pointing against the gravity acceleration vector

* - $z_{b}$
  - m or m a.s.l.
  - riverbed elevation pointing against the gravity acceleration vector

* - $z_{ref}$
  - m
  - reference (near-bed) elevation for suspended sediment exchange (cf. {ref}`gaia-sl-formulae`)
```


```{list-table} Greek letters (symbols) and parameters used in this eBook (in alphabetical order).
:header-rows: 1
:name: tab-notation-greek

* - Brief
- Einheit
- Beschreibung

* - $\alpha$
  - *rad* or *deg*
  - angle between the longitudinal channel ($x$) axis and a mass transport vector

* - $\alpha_{k_s}$
  - $-$
  - ratio between skin friction roughness and mean grain diameter ({ref}`RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER <bl-calibration>` keyword; same quantity as $f_{k'_{s}}$)

* - $\beta$
  - $-$
  - empiric bedload intensity correction factor (e.g., in {ref}`Gaia <gaia-dir>`)

* - $\Delta {t}$
  - s or years
  - time period (duration) or timestep length

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
  - porosity

* - $\varepsilon$
  - var.
  - absolute error between two quantities (see Equation {eq}`error_rate`)

* - $\varepsilon_s$
  - m$^{2}$ s$^{-1}$
  - sediment turbulent diffusivity (cf. Equation {eq}`eq-diff-sed`)

* - $\eta$
  - m
  - active layer thickness

* - $\eta_L$
  - $-$
  - Kolmogorov length scale

* - $\eta_T$
  - $-$
  - Kolmogorov time scale

* - $\eta_U$
  - $-$
  - Kolmogorov velocity scale

* - $\theta'$
  - $-$
  - skin-friction–corrected {term}`Dimensionless bed shear stress` ($\theta' = \mu\theta$), i.e., the {term}`Shields parameter`-scale shear used in the suspension formulae; equivalent to $\tau_{x}$ with skin friction correction (cf. {ref}`gaia-sl-formulae`)

* - $\theta_{cr}$
  - $-$
  - critical {term}`Shields parameter` (equivalent to $\tau_{x,cr}$)

* - $\nabla$
  - $-$
  - operator vector (*nabla*) of partial differentials $\frac{\partial}{\partial x_i}$ where $x_i$ refers to the dimensions of the flow field {cite:p}`kundu_fluid_2008`

* - $\mu$ = $\nu \cdot \rho_w$
  - kg m$^{-1}$ s$^{-1}$
  - dynamic viscosity

* - $\nu$ = $\mu \cdot \rho_w^{-1}$
  - m$^{2}$ s$^{-1}$
  - kinematic viscosity

* - $\nu_t$
  - m$^{2}$ s$^{-1}$
  - eddy (turbulent) viscosity

* - $\tilde{\nu}$
  - m$^{2}$ s$^{-1}$
  - modified turbulent kinematic viscosity; transport variable in the Spalart-Allmaras turbulence model

* - $\Phi$
  - $-$
  - dimensionless {term}`Sediment transport`

* - $\Phi_b$
  - $-$
  - dimensionless {term}`Bedload` transport

* - $\phi$
  - $-$
  - volumetric sediment concentration (cf. hindered settling, {ref}`gaia-sl-sed`)

* - $\psi$
  - variable
  - constant of a transported particle (substance)

* - $\rho_s$
  - kg m$^{-3}$
  - sediment grain density

* - $\rho_w$
  - kg m$^{-3}$
  - density of water

* - $\sigma_s$
  - $-$
  - Schmidt number relating sediment diffusivity to eddy viscosity (cf. Equation {eq}`eq-diff-sed`; Gaia fixes $\sigma_s = 1.0$)

* - $\tau$
  - N m$^{-2}$
  - bed shear stress

* - $\tau_{cr}$
  - N m$^{-2}$
  - Critical dimensional bed shear stress (cf. Equation {eq}`eq-gaia-erosion`)

* - $\tau_x$
  - $-$
  - {term}`Dimensionless bed shear stress`

* - $\tau_{x,cr}$
  - $-$
  - Critical {term}`Dimensionless bed shear stress` or {term}`Shields parameter`

```
