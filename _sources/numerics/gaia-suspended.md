(gaia-sl)=
# Suspended Load

{term}`Suspended load` refers to fine particles ($\lesssim$ 0.5 mm) that are transported in the water column. The TELEMAC software suite uses the hydrodynamic Telemac2d/3d models to simulate {term}`Suspended load` by solving the {term}`Advection`-{term}`Diffusion` equations for tracers. This is why suspended load modelling requires an open boundary type for tracers (e.g., `4` or `5`) as described with the {ref}`setup of the *boundaries-gaia.cli* <gaia-bc>` file.

To activate the simulation of suspended load, add the following to the Gaia steering file:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ SUSPENDED LOAD
SUSPENSION FOR ALL SANDS : YES
```

(gaia-sl-sed)=
## Additional Sediment Parameters

Fine sediment mixtures involving very fine cohesive particles (less than 0.1 to 0.06 mm) are referred to as **mud** in Gaia and so do the keywords in the following paragraphs. More information about mud-related keywords can be found in section 4.2 in the {{ gaia }}.

### Deposition Parameters

For suspended load, the definition of additional sediment properties for every sediment class is required (or enabled).

Settling velocities $w_{s}$ for the particles can be defined with the **CLASSES SETTLING VELOCITIES** keyword to calculate the deposition flux $q_{s,dep}$:

$$
q_{s,dep} = w_{s} \cdot c_{mud} \cdot \left[1 - \left(\frac{\sqrt{\tau / \rho_{w}}}{u_{cr}}\right)^{2} \right]
$$ (eq-gaia-dep)

where $c_{mud}$ is the concentration of *mud* in g/l (i.e., g m$^{-3}$), $\tau$ is dimensional bed shear stress (N$\cdot$m$^{-2}$), and $u_{cr}$ is the critical shear velocity for mud deposition (m s$^{-1}$).

The settling velocity is computed as {cite:p}`dey_fluvial_2014`:

$$
w_{s} = \sqrt{\frac{4}{3}\cdot \frac{(s-1)\cdot g\cdot h}{C_{D}}}
$$ (eq-ws)

where $C_{D}$ is the dimensionless drag coefficient that is a function of the {term}`Reynolds number` $Re$ and the most fundamental equation for the drag coefficient stems from {cite:t}`stokes1850`:

$$
C_{D} = \frac{24}{Re}
$$ (eq-cd-stokes)

Experimental data have shown that {cite:t}`stokes1850` original equation requires adaptations for higher {term}`Reynolds number`s ($Re >$ 10-100) {cite:p}`rouse_analysis_1939`. Gaia comes with integrated algorithms for calculating the settling velocity $w_{s}$ and the drag coefficient $C_{D}$ as a function of the grain size. To take advantage of Gaia's integrated routines for calculating $w_{s}$, either do not use the CLASSES SETTLING VELOCITIES keyword in the Gaia steering file, or set its values to `-9`. Detailed information on the calculation of settling velocities for particular cases (e.g., suspended load calculation for other suspended material than mineral sediment) can be found, for example, in {cite:t}`dey_fluvial_2014` (book section 1.7). Gaia's settling velocity algorithm is located in the file *[settling_vel.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/settling__vel_8f_source.html)*.

The critical shear velocity $u_{cr}$ for mud deposition can be defined with the **CLASSES CRITICAL SHEAR VELOCITY FOR MUD DEPOSITION** keyword (default is `1000.` m s$^{-1}$). The fundamental definition of shear-related sediment mobility stems from the {term}`Shields parameter`, which refers to sediment *erosion* (i.e., the mobilization of an immobile grain), against the critical shear *velocity* for mud referring to *deposition*. Since a sort of onset (initialization) energy must be overcome in the erosion process, the threshold for erosion is higher than for deposition. Thus, the critical shear stress for deposition is smaller than the shear stress for erosion.

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
CLASSES SETTLING VELOCITIES : -9;-9;-9
CLASSES CRITICAL SHEAR VELOCITY FOR MUD DEPOSITION : 1000;1000;1000 / N per m2
```

### Erosion Parameters

Gaia calculates the erosion flux $q_{s,e}$ as the ratio of bed shear stress $\tau$ and its critical value for mud erosion $\tau_{cr}$:

$$
q_{s,e} = \begin{cases} M\cdot \left(\frac{\tau}{\tau_{cr}} - 1\right) & \mbox{ if } \tau > \tau_{cr} \\ 0 & \mbox{ if } \tau \leq \tau_{cr}\end{cases}
$$ (eq-gaia-erosion)

where $M$ denote the {cite:t}`krone1962`-{cite:t}`partheniades1965` erosion constant (in kg m$^{-2}$ s$^{-1}$), which can be defined in Gaia with the **LAYERS PARTHENIADES CONSTANT** keyword (default value: `1.E-03`). Moreover, $\tau_{cr}$ can be defined with the **LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD** (default is `0.01;0.02;0.03;...`) in N$\cdot$m$^{-2}$ (**dimensional**).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
LAYERS PARTHENIADES CONSTANT : 1.E-03 / in kg per m2 per s
LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD : 0.01;0.1;0.1 / in N per m2
```

(gaia-sl-formulae)=
## Suspended Load Formulae

The sediment transport formulae for suspended load modeling can be defined with the **SUSPENSION TRANSPORT FORMULA FOR ALL SANDS** keyword, which accepts an integer keyword defining a formula for calculating the equilibrium near-bed concentration $c_{eq}$ in **g/l** (i.e., gram per m$^3$). The calculated $c_{eq}$-values align with the later {ref}`definition of initial and boundary conditions <gaia-ic-sl>` for suspended load. The following integers can be used for calculating $c_{eq}$:

* `1` for the {cite:t}`zyserman1994` formula:
  - uses a skin friction correction (cf. {ref}`bedload corrections <c-friction>`) for the {term}`Shields parameter`.
  - is defined in `/telemac/v8pX/sources/gaia/`**[suspension_fredsoe_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/suspension__fredsoe__gaia_8f.html)**
* `2` for the {cite:t}`bijker1992` formula:
  - calculates suspended load concentration as a function of bedload and reference skin-friction elevation.
  - requires that {ref}`bedload calculation <gaia-bl>` is activated.
  - is defined in `/telemac/v8pX/sources/gaia/`**[suspension_bijker_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/suspension__bijker__gaia_8f.html)**
* `3` for the {cite:t}`van_rijn_suspension_1984` formula:
  - counterpart of the {ref}`gaia-rijn` formula for bedload.
  - uses a skin friction correction (cf. {ref}`bedload corrections <c-friction>`) for the {term}`Shields parameter`.
  - calculates reference skin-friction elevation as a function of roughness length (cf. Equation {eq}`eq-cf-skin` in the bedload section).
  - is defined in `/telemac/v8pX/sources/gaia/`**[suspension_vanrijn_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/suspension__vanrijn__gaia_8f.html)**
* `4` for the {cite:t}`soulsby1997`-{cite:t}`rijn2007` formula:
  - uses an orbital velocity of waves (i.e., suggested application: coastal/marine regions).
  - read more about suspended load and waves in section 5.1 of the {{ gaia }}.
  - is defined in `/telemac/v8pX/sources/gaia/`**[suspension_sandflow_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/suspension__sandflow__gaia_8f.html)**


(gaia-ic-sl)=
## Initial Conditions

```{admonition} Requires TELEMAC v8p2 or more recent
:class: warning
The setup of initial and boundary conditions as described in this eBook requires TELEMAC v8p2 or later. Earlier versions, such as v8p1, will not recognize the keywords for initial conditions.
```

Gaia enables a class-wise definition of initial concentrations for suspended load following the order of {ref}`sediment class definitions <gaia-sed>`. The following list definition sets the initial concentration for the 0.5 mm sediment class ({ref}`recall its definition <gaia-sed>`) to 0.6 **g/l** (i.e., 0.0006 gram per m$^3$) and 0.0 g/l for the 0.02-m and 0.1-m sediment size classes. However, the definition of initial suspended sediment concentrations is overridden in 2d at boundary nodes when the **EQUILIBRIUM INFLOW CONCENTRATION** keyword is set to `YES` (requires that the {ref}`tracer boundary <gaia-bc>` is set to `5`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES : 6.E-04;0.;0.
```

Read more about the definition of initial conditions in section 2.1.1 in the {{ gaia }}.

(gaia-bc-sl)=
## Boundary Conditions

With the {ref}`tracer boundary <gaia-bc>` set to `5`, per-sediment class suspended load concentrations can be prescribed at the open liquid boundaries similar to the initial concentrations. Alternatively, the **EQUILIBRIUM INFLOW CONCENTRATION** keyword may be used:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES : 6.E-04;0.;0.
/ EQUILIBRIUM INFLOW CONCENTRATION : YES / not used in  this tutorial
```

Gaia can be run with liquid boundary files for assigning time-dependent suspended load fluxes (the outflow should be kept in equilibrium). Solid flux time series can be implemented using `455`-`5` boundary definitions, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. More information about suspended load boundary conditions can be found in section 2.1.2 in the {{ gaia }}.



## Numerical Parameters

Most numerical parameters for suspended load modeling depend on the hydrodynamic Telemac2d/3d steering file definitions. In addition, keywords directly affecting the simulation of suspended load should be declared in the Gaia steering file.

The **SCHEME FOR ADVECTION ...** keywords for velocities, tracers, and turbulence modeling are defined with the hydrodynamics (Telemac2d/3d) steering file's {ref}`general numerical parameters for finite elements <tm2d-fe>`. In addition, the advection scheme for suspended load can be defined in the Gaia steering file with the **SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS** keyword that accepts one of the following integer keywords (for 2d only):

* `1` for the unconditionally stable, non-conservative, but diffusive (for small timesteps) *Characteristics* scheme.
* `2` for the non-conservative *Streamline Upwind Petrov Galerkin* (SUPG) scheme that uses to the {term}`CFL` condition and is less diffusive than the *Characteristics* scheme.
* `3` or `4` for the conservative form of the {term}`Continuity equation` (*Conservative N-scheme*) and with timestep reduction based on the {term}`CFL` condition. This option should not be used in the presence of tidal flats (use `13` or `14`).
* `5` for the mass-conservative PSI distributive scheme (**default**), which corrects fluxes according to the tracer and is less diffusive than `4` or `14`; thus, the computation time with `5` is longer than with `4` or `14`. This option should not be used in the presence of tidal flats.
* `13` and `14` for the *Edge-based N-scheme* (NERD), which is similar to `3` and `4`, but better adapted to tidal flats. **Option `14` is used in this tutorial** according to the recommendation in the {{ gaia }}.
* `15` for the mass-conservative *ERIA scheme* that works with tidal flats.

The options `4` and `14` can be defined along with the keyword definition `CONTINUITY CORRECTION : YES`, and enable a correction of vertical convection velocities. To this end, the keyword **CORRECTION ON CONVECTION VELOCITY** can be set to `YES` to avoid an overestimation of suspended load, especially in deep waters.

The **SCHEME OPTION FOR ADVECTION OF SUSPENDED SEDIMENTS** can additionally be defined to either use a  **strong (default of `1`)** or a **weak (`2`)** form for advection. A weak form decreases {term}`Diffusion`, is more conservative, and increases computation time (read more in the {ref}`Telemac2d steady section <tm2d-fe>`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14
CONTINUITY CORRECTION : YES / use when SCHEME is 4 or 14
```


Read more about the definition of initial conditions in section 2.1.5 in the {{ gaia }}.

## Example Applications

Examples for the implementation of suspended load come along with the TELEMAC installation (e.g., in `telemac/v8p2/examples/gaia`). The following examples in the `gaia` folder are feature (pure) suspended load implementations:

* 2d model of combined cohesive and non-cohesive suspended transport: **hippodrome-t2d/**
* 2d model of cohesive mud: **mud_conservation-t2d/**
* 3d model of combined cohesive and non-cohesive suspended transport: **hippodrome-t2d/**
* 3d model of non-cohesive suspended transport with skin friction correction: **lyn-t3d/**
* 3d model of cohesive suspended transport with rouse vertical profile (cf. {{ gaia }}, section 2.1.2): **rouse-t3d/**
* 3d model of a tidal flume with cohesive sediment: **tidal_flats-t3d/**
* Coupling with waves: **sandpit-t2d/**
