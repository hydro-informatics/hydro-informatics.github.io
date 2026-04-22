---
description: Configure suspended sediment transport in TELEMAC-GAIA using advection-diffusion equations, tracer concentrations, and erosion-deposition flux closures for fine particle modeling.
---

(gaia-sl)=
# Suspended Load

{term}`Suspended load` refers to fine particle ($\lesssim$ 1-2 mm) displacement in the water column, where particles are maintained in temporary suspension by the action of upward-moving turbulent eddies. The TELEMAC software suite uses the hydrodynamic Telemac2d/3d models to simulate {term}`Suspended load` by solving the {term}`Advection`-{term}`Diffusion` equations with tracer concentrations. This is why suspended load modeling requires an open boundary `LICBOR` type for tracers (e.g., `4` or `5`) as described in the {ref}`setup of the boundaries-gaia.cli <gaia-bc>` file.

To activate the simulation of suspended load, add the following to the Gaia steering file:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ SUSPENDED LOAD
SUSPENSION FOR ALL SANDS : YES
```

(gaia-sl-theory)=
## Theoretical Background

The governing equation for suspended sediment transport is the advection-diffusion equation (ADE), which describes mass conservation of suspended sediment in the water column:

$$
\frac{\partial (hC)}{\partial t} + \frac{\partial (hUC)}{\partial x} + \frac{\partial (hVC)}{\partial y} = \frac{\partial}{\partial x}\left(\varepsilon_s h \frac{\partial C}{\partial x}\right) + \frac{\partial}{\partial y}\left(\varepsilon_s h \frac{\partial C}{\partial y}\right) + E - D
$$ (eq-ade-2d)

where $C$ is the depth-averaged suspended sediment concentration (kg m$^{-3}$ or g/l), $h$ is water depth (m), $U$ and $V$ are depth-averaged velocity components (m s$^{-1}$), $\varepsilon_s$ is the sediment diffusivity coefficient (m$^2$ s$^{-1}$), $E$ is the erosion flux from the bed (kg m$^{-2}$ s$^{-1}$), and $D$ is the deposition flux to the bed (kg m$^{-2}$ s$^{-1}$).

```{admonition} 2D vs. 3D suspended load modeling
:class: note
In 2d (Telemac2d-Gaia coupling), the advection-diffusion equation is depth-integrated and solved for depth-averaged concentrations. Near-bed concentrations are derived from equilibrium formulae. In 3d (Telemac3d-Gaia coupling), the full 3d advection-diffusion equation is solved, allowing for vertical concentration profiles (e.g., the {cite:t}`rouse_analysis_1939` profile). The 3d approach is recommended when vertical stratification of sediment is important, such as in deep estuaries or reservoirs. Read more about 3d suspended load in section 2.2 of the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

The sediment diffusivity $\varepsilon_s$ is related to the turbulent eddy viscosity $\nu_t$ by:

$$
\varepsilon_s = \frac{\nu_t}{\sigma_s}
$$ (eq-diff-sed)

where $\sigma_s$ is the Schmidt number (typically 0.5-1.0 for fine sediments). The **DIFFUSION COEFFICIENT** can be set in the Gaia steering file (default depends on the hydrodynamic turbulence model settings).

(gaia-sl-sed)=
## Additional Sediment Parameters

Fine sediment mixtures involving very fine cohesive particles (less than 0.06-0.1 mm) are referred to as **mud** in Gaia and so do the keywords in the following paragraphs. The distinction between non-cohesive sand and cohesive mud is important because their erosion and deposition behaviors differ fundamentally. More information about mud-related keywords can be found in section 4.2 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

### Deposition Parameters

For suspended load, the definition of additional sediment properties for every sediment class is required (or enabled).

Particle settling velocities $w_{s}$ can be defined with the **CLASSES SETTLING VELOCITIES** keyword to calculate the deposition flux $D$. The classical {cite:t}`krone1962` deposition formula is:

$$
D = w_{s} \cdot C \cdot \left(1 - \frac{\tau}{\tau_{cd}} \right) \quad \text{if } \tau < \tau_{cd}
$$ (eq-gaia-dep)

where $C$ is the suspended sediment concentration (kg m$^{-3}$), $\tau$ is the bed shear stress (N m$^{-2}$), and $\tau_{cd}$ is the critical shear stress for deposition (N m$^{-2}$). If $\tau \geq \tau_{cd}$, no deposition occurs because turbulence is too strong to allow particles to settle.

```{admonition} Critical shear stress vs. critical shear velocity
:class: note
The [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) uses **critical shear velocity** $u_{*,cd}$ (m s$^{-1}$) for mud deposition, which relates to critical shear stress by $\tau_{cd} = \rho_w \cdot u_{*,cd}^2$. The default value of `1000` m s$^{-1}$ effectively disables the shear stress limitation (i.e., deposition always occurs if $w_s > 0$), which is appropriate for non-cohesive sediments.
```

The settling velocity is computed internally by Gaia as a function of grain size based on {cite:t}`stokes1850` for fine particles and modifications for larger particles and higher Reynolds numbers {cite:p}`dey_fluvial_2014`:

$$
w_{s} = \frac{(s-1) \cdot g \cdot D^2}{18 \nu} \quad \text{(Stokes regime, } Re_p < 1\text{)}
$$ (eq-ws)

where $s$ is the relative density of sediment (typically 2.65), $g$ is gravitational acceleration, $D$ is the grain diameter, and $\nu$ is the kinematic viscosity of water ($\approx$10$^{-6}$ m$^{2}$ s$^{-1}$). For larger particles where the particle Reynolds number $Re_p = w_s D / \nu > 1$, Gaia applies corrections to the drag coefficient $C_D$ following established empirical relationships.


```{admonition} Placeholder
:class: warning
The drag coefficient $C_D$ formula for the Stokes correction still needs to be added here.
```


To take advantage of Gaia's integrated routines for calculating $w_{s}$, either do not use the CLASSES SETTLING VELOCITIES keyword in the Gaia steering file, or set its per-class values to `-9` (which triggers automatic calculation). Detailed information on the calculation of settling velocities for particular cases (e.g., suspended load calculation for other suspended material than mineral sediment) can be found, for example, in {cite:t}`dey_fluvial_2014` (book section 1.7). Gaia's settling velocity algorithm is located in the file `settling_vel.f` in the `/telemac/sources/gaia/` directory.

The critical shear velocity $u_{*,cd}$ for mud deposition can be defined with the **CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION** keyword (default is `1000.` N m$^{-2}$, which effectively disables the deposition threshold).

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
w_{s,h} = w_s \cdot (1 - \phi)^n
$$

where $\phi$ is the volumetric sediment concentration and $n$ is an empirical exponent (typically 4.65 for fine sediments). This is particularly important for simulating hyperconcentrated flows or reservoir sedimentation.
```

### Erosion Parameters

Gaia calculates erosion fluxes $E$ using the {cite:t}`partheniades1965` formula, which is the classical approach for cohesive sediments:

$$
E = \begin{cases} M\cdot \left(\frac{\tau}{\tau_{ce}} - 1\right) & \mbox{ if } \tau > \tau_{ce} \\ 0 & \mbox{ if } \tau \leq \tau_{ce}\end{cases}
$$ (eq-gaia-erosion)

where $M$ denotes the {cite:t}`krone1962`--{cite:t}`partheniades1965` erosion constant (in kg m$^{-2}$ s$^{-1}$), which can be defined in Gaia with the **LAYERS PARTHENIADES CONSTANT** keyword (default value: `1.E-03`). Moreover, $\tau_{ce}$ (critical shear stress for erosion) can be defined with the **LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD** keyword (default is `0.01;0.02;0.03;...` for successive layers) in N m$^{-2}$.

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

The sediment transport formulae for suspended load modeling can be defined with the **SUSPENSION TRANSPORT FORMULA FOR ALL SANDS** keyword, which accepts an integer number defining a formula for calculating the equilibrium near-bed concentration $C_{eq}$ in **kg/m³** (or equivalently, g/l). The equilibrium concentration represents the sediment concentration at a reference level near the bed under equilibrium conditions (i.e., when erosion equals deposition). The calculated $C_{eq}$ values align with the later {ref}`definition of initial and boundary conditions <gaia-ic-sl>` for suspended load.

The following integer numbers can be used for calculating $C_{eq}$ with the SUSPENSION TRANSPORT FORMULA FOR ALL SANDS keyword:

* `1` for the {cite:t}`zyserman1994` formula (**default** and **used in this tutorial**):
  - Empirical formula based on experimental data from {cite:t}`guy1966summary`
  - Uses a skin friction correction (cf. {ref}`bedload corrections <c-friction>`) for the {term}`Shields parameter`
  - Applicable for non-cohesive sediments in fluvial environments
  - Reference level: 2 grain diameters above the bed
  - Defined in `/telemac/sources/gaia/suspension_fredsoe_gaia.f`
  - Formula: $C_{eq} = \frac{0.331 \cdot (\tau_{*}' - \tau_{*,cr})^{1.75}}{1 + 0.331/0.46 \cdot (\tau_{*}' - \tau_{*,cr})^{1.75}}$ where $\tau_{*}'$ is the skin-friction Shields parameter and $\tau_{*,cr}$ is the critical Shields parameter

* `2` for the {cite:t}`bijker1992` formula:
  - Calculates suspended load concentration as a function of bedload and a reference skin-friction elevation
  - Requires that {ref}`bedload calculation <gaia-bl>` is activated
  - Suitable for combined bedload-suspended load calculations
  - Defined in `/telemac/sources/gaia/suspension_bijker_gaia.f`

* `3` for the {cite:t}`van_rijn_suspension_1984` formula:
  - Counterpart of the {ref}`van Rijn bedload formula <gaia-rijn>`
  - Uses a skin friction correction (cf. {ref}`bedload corrections <c-friction>`) for the {term}`Shields parameter`
  - Calculates reference elevation as $z_{ref} = \max(0.5 k_s, 0.01 \text{ m})$ where $k_s$ is the roughness length
  - Originally developed for sand transport in rivers and estuaries
  - Defined in `/telemac/sources/gaia/suspension_vanrijn_gaia.f`

* `4` for the {cite:t}`soulsby1997`-{cite:t}`rijn2007` formula:
  - Uses orbital velocity of waves (i.e., suggested application: coastal/marine regions)
  - Combines current and wave effects on sediment suspension
  - Read more about suspended load and waves in section 5.1 of the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)
  - Defined in `/telemac/sources/gaia/suspension_sandflow_gaia.f`

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

Gaia enables a class-wise definition of initial concentrations for suspended load following the order of {ref}`sediment class definitions <gaia-sed>`. The following list definition sets the initial concentration for the 0.5-mm sediment class ({ref}`recall its definition <gaia-sed>`) to 0.6 **g/l** (i.e., 0.0006 kg/m$^3$) and 0.0 g/l for the 0.02-m and 0.1-m sediment size classes. The definition of initial suspended sediment concentrations can be overridden in 2d at boundary nodes by setting the **EQUILIBRIUM INFLOW CONCENTRATION** keyword to `YES` (requires that the {ref}`tracer boundary <gaia-bc>` is set to `5`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES : 6.E-04;0.;0.
```

```{admonition} Concentration units in Gaia
:class: warning
Gaia internally works with concentrations in **kg/m³**. When specifying concentrations, ensure consistency:
* 1 g/l = 0.001 kg/m³ = 1 kg/m³ (these are equivalent!)
* 1 mg/l = 0.001 g/l = 0.001 kg/m³

The example above sets `6.E-04` kg/m³ = 0.6 g/l = 600 mg/l for the first sediment class.
```

Read more about the definition of initial conditions in section 2.1.1 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

(gaia-bc-sl)=
## Boundary Prescriptions

The per-sediment class suspended load concentrations can be prescribed similar to the initial concentrations with the **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES** keyword. Alternatively, the **EQUILIBRIUM INFLOW CONCENTRATION** keyword may be used to automatically compute the inflow concentration based on the equilibrium formula (option `1`-`4` defined above). **None of these keywords is used in this tutorial** because the model starts with a defined initial concentration and allows the system to evolve.

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES : 6.E-04;0.;0.
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

The options `4` and `14` can be defined along with the keyword definition `CONTINUITY CORRECTION : YES` that enables a correction of vertical convection velocities. This setting avoids overestimating suspended load, especially in deep waters, but it is not used in this tutorial.

The **SCHEME OPTION FOR ADVECTION OF SUSPENDED SEDIMENTS** can be additionally defined to either use a **strong (default of `1`)** or a **weak (`2`)** form for advection. A weak form decreases numerical {term}`Diffusion`, is more conservative, and increases computation time (read more in the {ref}`Telemac2d steady section <tm2d-fe>`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14
/ CONTINUITY CORRECTION : YES / use when SCHEME is 4 or 14 for deep water
```

```{admonition} Solver settings for suspended sediment diffusion
:class: tip
When using implicit schemes for suspended sediment diffusion, the following keywords can be adjusted in the Gaia steering file:

* **SOLVER FOR DIFFUSION OF SUSPENDED SEDIMENTS**: Choice of solver (default `1` = conjugate gradient)
* **MAXIMUM NUMBER OF ITERATIONS FOR SOLVER FOR DIFFUSION OF SUSPENDED SEDIMENTS**: Maximum iterations (default `60`)
* **ACCURACY FOR DIFFUSION OF SUSPENDED SEDIMENTS**: Convergence criterion (default `1.E-8`)

For most applications, default values are adequate. Increase maximum iterations if solver warnings appear in the listing output.
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