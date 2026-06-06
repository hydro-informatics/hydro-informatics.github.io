The `gaia-example.cas` template accounts for two sediment classes (surface d84 = 64 mm and sub-surface d65 = 13.86 mm), four spatial zones, Meyer-Peter & Müller bedload with a critical Shields number = 0.07, and suspended-load according to Van Rijn (Soulsby--Van Rijn implementation).  Comments (`/ ...`) flag the lines that should definitely be adjusted (file names, fractions, timestep, etc.).

---

## Sample TELEMAC-2D / GAIA steering file

```plaintext
/===================================================================
/  gaia-example.cas   --   TELEMAC-2D  +  GAIA
/  Two-class, four-zone graded bed; MPM bedload + Van Rijn suspended
/===================================================================

/---------- GENERAL FILES ---------------------------------
GEOMETRY FILE                     : 'mesh.slf'
BOUNDARY CONDITIONS FILE          : 'boundaries.cli'
INITIAL CONDITIONS FILE           : 'initial-hydro.slf'     / hydraulic restart
RESULTS FILE                      : 'gaia-results.slf'
REFERENCE FILE                    : ''                      

/----------  COUPLING & TIME -------------------------------
COUPLING WITH                     : 'GAIA'
GAIA COUPLING DELAY               : 1
TIME STEP                         : 2.0           / s
GRAPHIC PRINTOUT PERIOD           : 900
LISTING PRINTOUT PERIOD           : 900
DURATION                          : 86400         / 1 day

/=============================================================
/  GAIA -- PHYSICAL SET-UP
/=============================================================

/---------- SEDIMENT CLASSES ------------------------------
NUMBER OF SEDIMENTS               : 2
CLASSES TYPE OF SEDIMENT          : NCO ; NCO                / both non-cohesive
CLASSES SEDIMENT DIAMETERS        : 0.064  ; 0.01386         / m  (64 mm, 13.86 mm)
CLASSES SEDIMENT DENSITY          : 2680   ; 2680            / kg m-3
CLASSES SHIELDS PARAMETERS        : 0.07   ; 0.07            / dimensionless Shields
CLASSES SETTLING VELOCITIES       : -9     ; -9              / let GAIA compute

/ optional -- uniform grading if zones not used
CLASSES INITIAL FRACTION          : 0.5    ; 0.5           

/---------- ZONING (spatially variable mixture) -----------
NUMBER OF ZONES                   : 4
ZONES FILE                        : 'zones.slf'              / ZONE_ID variable 1-4

/ Fractions per zone (must sum to 1.0, one line per zone):
CLASSES INITIAL FRACTION BY ZONES :
  0.80 ; 0.20 ;      / Zone 1 -- surface-coarse dominated
  0.60 ; 0.40 ;      / Zone 2
  0.40 ; 0.60 ;      / Zone 3 -- finer sub-surface
  0.20 ; 0.80 ;      / Zone 4

/---------- BED-LAYERS & STRATIFICATION -------------------
ACTIVE LAYER THICKNESS            : 0.15                    / m  (approx. 2.5 x d50)
NUMBER OF LAYERS FOR INITIAL STRATIFICATION : 1
LAYERS INITIAL THICKNESS          : 0.50                    / m total below AL

/=============================================================
/  GAIA -- TRANSPORT FORMULAE
/=============================================================

/---------- BEDLOAD (Meyer-Peter & Müller) ---------------
bedload TRANSPORT FORMULA FOR ALL SANDS : 4      / MPM48
SLOPE EFFECT                       : 1
FORMULA FOR SLOPE EFFECT           : 1                     / Koch-Flokstra
SKIN FRICTION CORRECTION           : 1
RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER : 3.

/---------- SUSPENDED-LOAD (Van Rijn) ---------------------
SUSPENSION FOR ALL SANDS          : YES
SUSPENSION TRANSPORT FORMULA FOR ALL SANDS : 4    / Soulsby--Van Rijn 1997/2007
SETTLING VELOCITY FORMULA         : 1

/---------- NUMERICS --------------------------------------
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14  / MURD-TVD
MORPHOLOGICAL TIME STEP           : 60.
MORPHOLOGICAL FACTOR              : 1.

END OF FILE
```

---

## Explanation of keywords

| Requirement | GAIA keyword(s) | Notes |
|-------------|-----------------|-------|
| **Two classes/layers** | `NUMBER OF SEDIMENTS`, `CLASSES ...` | GAIA handles layering automatically once classes are defined |
| **Four zones** | `NUMBER OF ZONES`, `ZONES FILE`, `CLASSES INITIAL FRACTION BY ZONES` | A separate `zones.slf` (one integer per mesh node) lets you localise mixtures |
| **Surface d84 = 64 mm, sub-surface d65 = 13.86 mm** | `CLASSES SEDIMENT DIAMETERS` | GAIA expects metres; 64 mm > 0.064 m |
| **MPM bedload** | `BED-LOAD TRANSPORT FORMULA FOR ALL SANDS = 4` | Code 4 corresponds to Meyer-Peter & Müller 1948 |
| **Critical Shields parameter = 0.07** | `CLASSES SHIELDS PARAMETERS` | Overrides GAIA’s default 0.047 |
| **Suspended load: Van Rijn** | `SUSPENSION TRANSPORT FORMULA FOR ALL SANDS = 4` | GAIA’s integer 4 triggers the Soulsby--Van Rijn current-only form |
| **Settling velocity handled internally** | `CLASSES SETTLING VELOCITIES : -9` | `-9` tells GAIA to compute fall velocity from diameter |

---

### Implementation tips

* **`zones.slf` creation** -- populate an extra scalar variable `ZONE_ID` (values 1-4) in GIS/Blue-Kenue, then export as Selafin; GAIA reads it automatically when `ZONES FILE` is set.  
* **Hydrodynamic coupling** -- in the main **Telemac-2D** `.cas` add  
  ```
  COUPLING WITH : 'GAIA'
  GAIA STEERING FILE : 'gaia-example.cas'
  ```  
  so GAIA receives depth, velocity, etc. at every coupling step.
* **Calibrating the model** -- if erosion is too strong, raise `SHIELDS PARAMETERS` or the skin-friction multiplier; if depositional lobes are over-predicted, tweak `ACTIVE LAYER THICKNESS` and Van Rijn settling velocity range. 
* **Numerics** -- the TVD MURD scheme (`14`) is robust for high Péclet numbers; keep `MORPHOLOGICAL TIME STEP` ≥ the hydrodynamic step to avoid aliasing.



# Implementation of discharge-dependent bedload and suspended load

*GAIA* can compute an **equilibrium** inflow automatically **only for suspended load** (`EQUILIBRIUM INFLOW CONCENTRATION = YES`).  
For **bedload** you must still tell the code how much solid discharge enters.  The closest practical substitutes are  

1. **Prescribe a capacity-based value yourself** with `PRESCRIBED SOLID DISCHARGES`, or  
2. **Feed a time-series** through a `*.liq` liquid-boundary file (boundary type 5), letting GAIA update the inflow every time-step.  

For suspended load, the very same `*.liq` file can carry time-varying class-by-class concentrations, so you can couple them directly to the discharge hydrograph.

---

## Equilibrium bedload at the upstream boundary

### Why there is no built-in keyword  
`EQUILIBRIUM INFLOW CONCENTRATION` works only on suspended tracers; the developers explicitly note that it "is **not** implemented for bedload". Therefore, GAIA expects you to send a solid flux at the boundary.

### Practical work-arounds  

| Method | Steering-file keywords | Notes |
|-------|-----------------------|-------|
| **A. Constant capacity value** | `PRESCRIBED SOLID DISCHARGES : 10.` (kg/s or m3/s depending on `SOLID DISCHARGE UNIT`) | Quick and robust for steady runs.  Pick  *qb* from your MPM/Van Rijn formula at the design discharge |
| **B. Quasi-equilibrium time series** | keep `PRESCRIBED SOLID DISCHARGES` at 0; add a **liquid BC file** carrying `QSBL(i)` columns (see §2) and set the boundary in the `*.cli` to **`LIEBOR = 5`** (prescribed flux) with **`EBOR = 0`** so the bed elevation is frozen at the first node |
| **C. User FORTRAN** | edit `GAIABC` (or `BORDGAIA`) to compute the bedload capacity on-the-fly from local shear stress and overwrite `QSIL(i)`. | Full equilibrium, but requires recompilation. |

> **Tip:** If you want "zero bed evolution" right at the inlet, combine method B with `NOEROD BOUNDARIES : 1` to make the first mesh row non-erodible.  This is often easier than coding a FORTRAN hook. 

---

## Creating a *discharge-dependent* suspended-load boundary

### The three options GAIA offers

1. **Constant per boundary**  
   `PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.05; 0.03` (g/L)
2. **Automatic capacity**  
   `EQUILIBRIUM INFLOW CONCENTRATION : YES` (needs `LITBOR = 5` in the `*.cli`)
3. **Time series in a `*.liq` file** (recommended for hydrographs).

### Building the `*.liq` file

```text
# bc_sed.qsl   (example with one sediment class)
T     Q(1)  SL(1)  QSBL(1)  CSUSP(1)
s     m3/s   m     kg/s     g/l
0.0     20    1.8    0.30     0.03
3600.   80    1.8    5.20     0.12
7200.  120    1.8    9.75     0.25
```

* **Column order**: after the hydraulic variables GAIA appends **tracers first**, then each suspended-sediment class.  
* Add the file path in the **hydrodynamic** steering file (not GAIA):  
  ```
  LIQUID BOUNDARIES FILE : 'bc_sed.qsl'
  ``` 
* Ensure the matching boundary node in `*.cli` is `5 5 5 ...` so TELEMAC reads every column as "prescribed‐value".

### Multiple classes  
Simply add further `QSBL(j)` and `CSUSP(j)` columns for each class; GAIA allocates them sequentially after any other tracers.

---

## Checklist of steering-file keywords

| Task | Mandatory keyword(s) | Where to put |
|------|----------------------|--------------|
| Constant bedload inflow | `PRESCRIBED SOLID DISCHARGES` | GAIA `.cas` |
| Time-series bedload | `LIQUID BOUNDARIES FILE`, `LIEBOR=5`, `EBOR=0` | Hydro `.cas` + `.cli` |
| Constant suspended load | `PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES` | GAIA `.cas` |
| Capacity suspended load | `EQUILIBRIUM INFLOW CONCENTRATION : YES` | GAIA `.cas` |
| Time-series suspended load | same `*.liq` file as hydraulics | Hydro `.cas` |

*Remember*: GAIA uses **g/L** for concentrations and **kg/s** (or **m3/s**) for solid discharge, depending on `SOLID DISCHARGE UNIT`.

---

### Further reading and examples

* Hydro-Informatics tutorials on **bedload** and **suspended load** boundary conditions
* The GAIA **User Manual**, sec. 2.1 to 2.2 for inflow/outflow theory and syntax 
* Example model `examples/gaia/yen-t2d` shipped with TELEMAC, which couples a `*.qsl` file to a Rhine hydrograph 

With these ingredients you can switch between capacity inflow, constant loads or fully dynamic hydro-sediment time series by editing just a handful of keywords—no extra coding required. 

