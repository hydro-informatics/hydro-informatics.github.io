---
description: Configurer le transport des sédiments en suspension dans TELEMAC-GAIA à l'aide d'équations advection-diffusion, de concentrations de traceurs et de fermetures de flux d'érosion-déposition pour la modélisation des particules fines.
---

(gaia-sl)=
# Charge suspendue

{term}`Suspended load` refers to fine particle ($\lesssim$ 1-2 mm) displacement in the water column, where particles are maintained in temporary suspension by the action of upward-moving turbulent eddies. The TELEMAC software suite uses the hydrodynamic Telemac2d/3d models to simulate {term}`Suspended load` by solving the {term}`Advection`-{term}`Diffusion` equations with tracer concentrations. This is why suspended load modeling requires an open boundary `LICBOR` type for tracers (e.g., `4` or `5`) as described in the {ref}`setup of the boundaries-gaia.cli <gaia-bc>` file.

Pour activer la simulation de la charge suspendue, ajouter ce qui suit au fichier de direction de Gaia :

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ SUSPENDED LOAD
SUSPENSION FOR ALL SANDS : YES
```

(gaia-sl-theory)=
## Contexte théorique

L'équation qui régit le transport des sédiments en suspension est l'équation advection-diffusion (ADE), qui décrit la conservation en masse des sédiments en suspension dans la colonne d'eau :

$$
\frac{\partial (hC)}{\partial t} + \frac{\partial (hUC)}{\partial x} + \frac{\partial (hVC)}{\partial y} = \frac{\partial}{\partial x}\left(\varepsilon_s h \frac{\partial C}{\partial x}\right) + \frac{\partial}{\partial y}\left(\varepsilon_s h \frac{\partial C}{\partial y}\right) + E - D
$$ (eq-ade-2d)

where $C$ is the depth-averaged suspended sediment concentration (Gaia expresses it in g/l, numerically equal to kg m$^{-3}$), $h$ is water depth (m), $U$ and $V$ are depth-averaged velocity components (m s$^{-1}$), $\varepsilon_s$ is the sediment diffusivity coefficient (m$^2$ s$^{-1}$), $E$ is the erosion flux from the bed (kg m$^{-2}$ s$^{-1}$), and $D$ is the deposition flux to the bed (kg m$^{-2}$ s$^{-1}$).

```{admonition} 2D vs. 3D suspended load modeling
:class: note
In 2d (Telemac2d-Gaia coupling), the advection-diffusion equation is depth-integrated and solved for depth-averaged concentrations. Near-bed concentrations are derived from equilibrium formulae. In 3d (Telemac3d-Gaia coupling), the full 3d advection-diffusion equation is solved, allowing for vertical concentration profiles (e.g., the {cite:t}`rouse_analysis_1939` profile). The 3d approach is recommended when vertical stratification of sediment is important, such as in deep estuaries or reservoirs. Read more about 3d suspended load in section 2.2 of the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

The sediment diffusivity $\varepsilon_s$ is related to the turbulent eddy viscosity $\nu_t$ by:

$$
\varepsilon s = \frac{\nu t}{\sigma s}
$$ (eq-diff-sed)

where $\sigma_s$ is the Schmidt number, which Gaia fixes to $\sigma_s = 1.0$ (i.e., the sediment diffusivity equals the turbulent eddy viscosity). An additional constant diffusivity can be set with the **COEFFICIENT FOR DIFFUSION OF SUSPENDED SEDIMENTS** keyword (real, default `1.E-6` m$^2$ s$^{-1}$).

(gaia-sl-sed)=
## Additional Sediment Parameters

Fine sediment mixtures involving very fine cohesive particles (less than 0.06-0.1 mm) are referred to as **mud** in Gaia and so do the keywords in the following paragraphs. The distinction between non-cohesive sand and cohesive mud is important because their erosion and deposition behaviors differ fundamentally. More information about mud-related keywords can be found in section 4.2 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

### Deposition Parameters

For suspended load, the definition of additional sediment properties for every sediment class is required (or enabled).

Particle settling velocities $w_{s}$ can be defined with the **CLASSES SETTLING VELOCITIES** keyword to calculate the deposition flux $D$. The classical {cite:t}`krone1962` deposition formula is:

$$
D = w {s} \cdot C \cdot \left(1 - \frac{\tau}{\tau {cd}} \right) \quad \text{if} \tau < \tau {cd}
$$ (eq-gaia-dep)

where $C$ is the suspended sediment concentration (g/l), $\tau$ is the bed shear stress (N m$^{-2}$), and $\tau_{cd}$ is the critical shear stress for deposition (N m$^{-2}$). If $\tau \geq \tau_{cd}$, no deposition occurs because turbulence is too strong to allow particles to settle.

```{admonition} Critical shear stress vs. critical shear velocity
:class: note
The keyword **CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION** is supplied as a **shear stress in N m$^{-2}$** (default `1000.`). Internally, Gaia converts it to a **critical shear velocity** $u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$ for the deposition formula. The large default of `1000` N m$^{-2}$ effectively disables the shear-stress limitation (i.e., deposition always occurs if $w_s > 0$), which is appropriate for non-cohesive sediments.
```

If the **CLASSES SETTLING VELOCITIES** keyword is omitted (or set to `-9`), Gaia computes $w_s$ for each sediment class internally, selecting one of three grain-size-dependent formulae:

* For very fine particles ($D_{50} < 10^{-4}$ m), {cite:t}`stokes1850` law applies:

$$
w {s} = \frac{(s-1) \cdot g \cdot D {50}^2} {18 \nu}
$$ (eq-ws-stokes)

* For intermediate sizes ($10^{-4} \leq D_{50} < 10^{-3}$ m), the Rubey--{cite:t}`zanke1977` formula is used:

$$
w {s} = \frac{10\nu}{D {50}}\left(\sqrt{1 + \frac{(s-1) \cdot g \cdot D {50}^3}{100\nu^2}} - 1\right)
$$ (eq-ws-zanke)

* For coarse particles ($D_{50} \geq 10^{-3}$ m), a constant drag-coefficient relation is used:

$$
w {s} = 1.1\sqrt{(s-1) \cdot g \cdot D {50}}
$$ (eq-ws-coarse)

where $s$ is the relative density of sediment (typically 2.65), $g$ is gravitational acceleration, $D_{50}$ is the grain diameter, and $\nu$ is the kinematic viscosity of water ($\approx$10$^{-6}$ m$^{2}$ s$^{-1}$). The three regimes transition from a viscous ($Re_p \ll 1$, Stokes) to a fully turbulent ($Re_p \gg 1$, constant drag) settling behavior {cite:p}`dey_fluvial_2014`.


To take advantage of Gaia's integrated routines for calculating $w_{s}$, either do not use the CLASSES SETTLING VELOCITIES keyword in the Gaia steering file, or set its per-class values to `-9` (which triggers automatic calculation). Detailed information on the calculation of settling velocities for particular cases (e.g., suspended load calculation for other suspended material than mineral sediment) can be found, for example, in {cite:t}`dey_fluvial_2014` (book section 1.7). Gaia's settling velocity algorithm is located in the file `settling_vel.f` in the `/telemac/sources/gaia/` directory.

The critical shear stress $\tau_{cd}$ for mud deposition can be defined with the **CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION** keyword (default is `1000.` N m$^{-2}$, which effectively disables the deposition threshold; Gaia converts it internally to the critical shear velocity $u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
CLASSES SETTLING VELOCITIES : -9;-9;-9
CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION : 1000;1000;1000 / N per m2
```

```{admonition} Hindered settling for high concentrations
:class: tip
At high suspended sediment concentrations (typically > 10 g/l), particle-particle interactions reduce the effective settling velocity. This phenomenon, known as *hindered settling*, can be enabled in Gaia with the **HINDERED SETTLING** keyword set to `YES` (default is `NO`). The hindered settling formulation follows {cite:t}`richardson1954sedimentation`:

$$
w {s,h} = w s \cdot (1 - \phi)^n
$$

where $\phi$ is the volumetric sediment concentration and $n$ is an empirical exponent (typically 4.65 for fine sediments). This is particularly important for simulating hyperconcentrated flows or reservoir sedimentation.
```

### Erosion Parameters

For **cohesive (mud)** sediments, Gaia calculates erosion fluxes $E$ using the {cite:t}`partheniades1965` formula, which is the classical approach for cohesive sediments:

$$
E = \begin{cases} M\cdot \left(\frac{\tau}{\tau {ce}} - 1\right) & \mbox{ si } \tau > \tau {ce} \\ 0 & \mbox{ si } \tau \leq \tau {ce}\end{cases}
$$ (eq-gaia-erosion)

where $M$ denotes the {cite:t}`krone1962`--{cite:t}`partheniades1965` erosion constant (in kg m$^{-2}$ s$^{-1}$), which can be defined in Gaia with the **LAYERS PARTHENIADES CONSTANT** keyword (default value: `1.E-03`). Moreover, $\tau_{ce}$ (critical shear stress for erosion) can be defined with the **LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD** keyword (default is `0.01;0.02;0.03;...` for successive layers) in N m$^{-2}$.

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
For mixed sediments containing both sand and mud fractions, Gaia applies different erosion formulations depending on the mud content in the active layer:

* **Mud content < 30%**: Non-cohesive behavior dominates; erosion follows the equilibrium concentration approach for sands.
* **Mud content 30-50%**: Transitional regime; linear interpolation between non-cohesive and cohesive formulations.
* **Mud content > 50%**: Cohesive behavior dominates; erosion follows the {cite:t}`partheniades1965` formulation.

This behavior is automatic in Gaia when multiple sediment classes with different grain sizes are defined. Read more about sand-mud mixtures in section 4 of the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

(gaia-sl-formulae)=
## Suspended Load Formulae

The sediment transport formulae for suspended load modeling can be defined with the **SUSPENSION TRANSPORT FORMULA FOR ALL SANDS** keyword, which accepts an integer number defining a formula for calculating the equilibrium near-bed concentration $C_{eq}$ in **g/l** (the unit Gaia uses internally for all suspended sediment concentrations). The equilibrium concentration represents the sediment concentration at a reference level near the bed under equilibrium conditions (i.e., when erosion equals deposition). The calculated $C_{eq}$ values align with the later {ref}`definition of initial and boundary conditions <gaia-ic-sl>` for suspended load.

The following integer numbers can be used for calculating $C_{eq}$ with the SUSPENSION TRANSPORT FORMULA FOR ALL SANDS keyword:

* `1` for the {cite:t}`zyserman1994` formula (**default** and **used in this tutorial**):
  - Empirical formula based on experimental data from {cite:t}`guy1966summary`
  - Uses a skin friction correction (cf. {ref}`bedload corrections <c-friction>`) for the {term}`Shields parameter`
  - Applicable for non-cohesive sediments in fluvial environments
  - Reference (near-bed) elevation $z_{ref} = \alpha_{k_s} \cdot D_{50}$ (default $3.0 \cdot D_{50}$, modifiable with **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER**)
  - Defined in `/telemac/sources/gaia/suspension_fredsoe.f`
  - Formula: $C_{eq} = \frac{0.331 \cdot (\theta' - \theta_{cr})^{1.75}}{1 + 0.72 \cdot (\theta' - \theta_{cr})^{1.75}}$ where $\theta' = \mu\theta$ is the skin-friction Shields parameter and $\theta_{cr}$ is the critical Shields parameter

* `2` for the {cite:t}`bijker1992` formula:
  - Calculates suspended load concentration as a function of bedload and a reference skin-friction elevation
  - Requires that {ref}`bedload calculation <gaia-bl>` is activated (`BED LOAD FOR ALL SANDS : YES`)
  - Suitable for combined bedload-suspended load calculations
  - Reference elevation $z_{ref} = k_{sr}$ (the rippled bed roughness)
  - Defined in `/telemac/sources/gaia/suspension_bijker.f`

* `3` for the {cite:t}`van_rijn_suspension_1984` formula:
  - Counterpart of the {ref}`van Rijn bedload formula <gaia-rijn>`
  - Uses a skin friction correction (cf. {ref}`bedload corrections <c-friction>`) for the {term}`Shields parameter`
  - Reference elevation $z_{ref} = 0.5 \cdot k_s$ where $k_s$ is the total roughness (from the hydrodynamics steering file)
  - Originally developed for sand transport in rivers and estuaries
  - Defined in `/telemac/sources/gaia/suspension_vanrijn.f`

* `4` for the {cite:t}`soulsby1997`-{cite:t}`rijn2007` formula:
  - Uses orbital velocity of waves (i.e., suggested application: coastal/marine regions)
  - Combines current and wave effects on sediment suspension
  - Read more about suspended load and waves in section 5.1 of the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)
  - Defined in `/telemac/sources/gaia/suspension_sandflow.f`

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SUSPENSION TRANSPORT FORMULA FOR ALL SANDS : 1
```

```{admonition} User-defined suspension formulae
:class: tip
Users can implement custom suspension transport formulae by modifying the Fortran source files. The procedure follows the same approach as for {ref}`user-defined bedload formulae <gaia-bl>`: copy the relevant source file to a `user_fortran/` directory and reference it in the steering file with `FORTRAN FILE : 'user_fortran'`. The [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) provides detailed guidance in section 6.3.
```

(gaia-ic-sl)=
## Initial and Boundary Conditions

Gaia enables a class-wise definition of initial concentrations for suspended load following the order of {ref}`sediment class definitions <gaia-sed>`. The following list definition sets the initial concentration for the 0.5-mm sediment class ({ref}`recall its definition <gaia-sed>`) to 0.6 **g/l** and 0.0 g/l for the 0.02-m and 0.1-m sediment size classes. The definition of initial suspended sediment concentrations can be overridden in 2d at boundary nodes by setting the **EQUILIBRIUM INFLOW CONCENTRATION** keyword to `YES` (requires that the {ref}`tracer boundary <gaia-bc>` is set to `5`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0.
```

```{admonition} Concentration units in Gaia
:class: warning
Gaia expects **all** suspended sediment concentrations in **g/l** (grams of dry sediment per litre), including the **INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES**, **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES**, and the `CBOR` column of the boundary file. Mass concentration in g/l is numerically identical to kg/m³:
* 1 g/l = 1 kg/m³
* 1 mg/l = 0.001 g/l = 0.001 kg/m³

So the example above sets `0.6` g/l = 0.6 kg/m³ = 600 mg/l for the first sediment class. If you need volume concentration $C_v$ instead, convert in post-processing with $C_v = C_m / \rho_s$, where $C_m$ is the mass concentration (g/l) and $\rho_s$ is the sediment density (kg/m³).
```

Read more about the definition of initial conditions in section 2.1.1 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

(gaia-bc-sl)=
## Boundary Prescriptions

The per-sediment class suspended load concentrations can be prescribed similar to the initial concentrations with the **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES** keyword. Alternatively, the **EQUILIBRIUM INFLOW CONCENTRATION** keyword may be used to automatically compute the inflow concentration based on the equilibrium formula (option `1`-`4` defined above). **None of these keywords is used in this tutorial** because the model starts with a defined initial concentration and allows the system to evolve.

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0. / g/l
/ EQUILIBRIUM INFLOW CONCENTRATION : YES / not used in this tutorial
```

```{admonition} Treatment of boundary fluxes
:class: tip
The **TREATMENT OF FLUXES AT THE BOUNDARIES** keyword controls how prescribed concentrations are handled at open boundaries:

* `1` (**default**): Priority to prescribed value in the diffusion step. This may create artificial fluxes at boundaries.
* `2`: Priority to prescribed flux. The actual sediment flux equals the water discharge multiplied by the prescribed concentration. This option is recommended for mass-conservative simulations with distributive advection schemes (`3`, `4`, `5`, `13`, `14`).

For critical mass-balance applications, use option `2` together with advection scheme `14` or `15`.
```

Gaia can be run with liquid boundary files for assigning time-dependent suspended load fluxes (the outflow should be kept in equilibrium). Solid flux time series can be implemented using the already applied `455`-`5` upstream boundary type, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. More information about suspended load boundary conditions can be found in section 2.1.2 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).


## Numerical Parameters

Most numerical parameters for suspended load modeling depend on hydrodynamic Telemac2d/3d steering file definitions. Additional keywords directly affecting the simulation of suspended load should be declared in the Gaia steering file.

For instance, the **SCHEME FOR ADVECTION ...** keywords for velocities, tracers, and turbulence modeling are defined with the hydrodynamics (Telemac2d/3d) steering file's {ref}`general numerical parameters for finite elements <tm2d-fe>`. In addition, the advection scheme for suspended load can be defined in the Gaia steering file with the **SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS** keyword that accepts one of the following integer keywords (for 2d only):

* `1` for the unconditionally stable, non-conservative, but diffusive (for small timesteps) *Method of Characteristics* scheme.
* `2` for the non-conservative *Streamline Upwind Petrov Galerkin* (SUPG) scheme that uses the {term}`CFL` condition and is less diffusive than the *Characteristics* (`1`) scheme.
* `3` or `4` for the conservative *N-scheme* (distributive) with timestep reduction based on the {term}`CFL` condition. Option `4` includes mass-lumping for improved stability. These options should **not** be used in the presence of tidal flats (use `13` or `14` instead).
* `5` for the mass-conservative *PSI distributive scheme* (**default**), which corrects fluxes according to tracer concentrations and is less diffusive than `4` or `14`. Computation time with `5` is longer than with `4` or `14`. This option should **not** be used in the presence of tidal flats.
* `13` and `14` for the *Edge-based N-scheme* (NERD), which is similar to `3` and `4`, but adapted to tidal flats. **Option `14` is used in this tutorial** according to the recommendation in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
* `15` for the mass-conservative *ERIA scheme* that works with tidal flats.

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
The diffusion term of the advection-diffusion equation is governed by the turbulent eddy viscosity from the hydrodynamic solver plus a constant background diffusivity that can be set in the Gaia steering file:

* **COEFFICIENT FOR DIFFUSION OF SUSPENDED SEDIMENTS** (real, default `1.E-6` m$^2$ s$^{-1}$): constant diffusivity added in 2d (in 3d use **COEFFICIENT FOR HORIZONTAL DIFFUSION OF SUSPENDED SEDIMENTS** and **COEFFICIENT FOR VERTICAL DIFFUSION OF SUSPENDED SEDIMENTS**).

For most fluvial applications, the default value is adequate because the turbulent diffusivity dominates over the constant background term.
```

Read more about the definition of numerical parameters in section 2.1.5 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

## Morphological Coupling

When suspended load is activated together with bed evolution, the erosion and deposition fluxes contribute to the mass balance of the bed through the {term}`Exner equation`. The net flux (erosion minus deposition) modifies the bed elevation at each time step.

```{admonition} Morphological factor for suspended load
:class: tip
For long-term simulations where morphological timescales are much longer than hydrodynamic timescales, a **MORPHOLOGICAL FACTOR** can be applied to accelerate bed evolution. This factor multiplies the net erosion/deposition flux, allowing multi-year morphological simulations with reasonable computation times. However, use with caution: morphological factors greater than 10-20 may introduce unrealistic results. The keyword is defined in the Gaia steering file:

```fortran
MORPHOLOGICAL FACTOR : 10. / accelerate bed evolution 10x
```
```

## Example Applications

Examples for the implementation of suspended load come along with the TELEMAC installation (in the `/telemac/examples/gaia/` directory). The following examples in the `gaia/` folder feature (pure) suspended load calculations:

* 2d model of combined cohesive and non-cohesive suspended transport: **hippodrome-t2d/**
* 2d model of cohesive mud mass conservation: **mud_conservation-t2d/**
* 3d model of combined cohesive and non-cohesive suspended transport: **hippodrome-t3d/**
* 3d model of non-cohesive suspended transport with skin friction correction: **lyn-t3d/**
* 3d model of cohesive suspended transport with Rouse vertical profile (cf. [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf), section 2.1.2): **rouse-t3d/**
* 3d model of a tidal flume with cohesive sediment: **tidal_flats-t3d/**
* Coupling with waves: **sandpit-t2d/**

```{admonition} Recommended workflow for suspended load simulations
:class: note
1. **Start with hydrodynamics**: Ensure the hydrodynamic model (Telemac2d/3d) is calibrated and produces reasonable flow fields before coupling with Gaia.
2. **Define sediment classes**: Specify grain sizes appropriate for the site. Fine sediments ($D < 0.063$ mm) are typically cohesive; coarser sediments are non-cohesive.
3. **Select suspension formula**: Choose based on the environment (fluvial: `1` or `3`; coastal with waves: `4`).
4. **Set initial conditions**: Use measured or estimated suspended sediment concentrations.
5. **Choose advection scheme**: Use `14` for robustness with tidal flats, or `5` for better accuracy in deep channels.
6. **Calibrate erosion/deposition**: Adjust Partheniades constant $M$, critical shear stresses, and settling velocities to match observed concentrations.
7. **Validate mass balance**: Enable `MASS-BALANCE : YES` in the hydrodynamics steering file to monitor sediment conservation.
```