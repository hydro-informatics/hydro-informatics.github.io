# Debugging TELEMAC

Since its early development, TELEMAC has become a robust and reliable tool for the numerically modeling of open surface flows. Yet there are a few little challenges and this always growing page provides some answers.

```{admonition} Keyword-research the TELEMAC docs
:class: tip
To look up the reference, implementation, and/or meaning of a variable, class, script, file, or module, visit the {{ tmdoxy }}.
```

## Traceback errors

If a simulation crashes and it is not clear why debugging with [*gdb*](http://www.gdbtutorial.com) is a good option. To do so, first install *gdb*:

```
sudo apt install gdb
```

Then launch the steering file in debugging mode as follows:

```
telemac2d.py -w tmp simulation_file.cas --split
telemac2d.py -w tmp simulation_file.cas -x
cd tmp
gdb ./out_telemac2d
```

In *gdb* tap:

```
(gdb) run
```

To end *gdb* tap:

```
(gdb) quit
```

This approach also works with *Telemac3d* (and other modules).

## Steering (CAS) Files

* Prefer `:` over `=`
* Place all model files in the same folder and **only use file names** without the directories of files.

## Unstable Simulations

### Accuracy

When the accuracy keywords are improperly defined, TELEMAC may not be able to end the simulation. In this case, make sure to comment out the accuracy keywords and let TELEMAC use its default values:

```fortran
/ SOLVER ACCURACY : 1.E-4
/ ACCURACY FOR DIFFUSION OF TRACERS : 1.E-4
/ ACCURACY OF K : 1.E-6
/ ACCURACY OF EPSILON : 1.E-6
/ ACCURACY OF SPALART-ALLMARAS : 1.E-6
```

Moreover, variable timestep calculation may cause eternal model runs (i.e., activated with `VARIABLE TIME-STEP : YES`). To deactivate variable time-step calculation use `VARIABLE TIME-STEP : NO` and define a `TIME STEP` (e.g., `1.`)

### Implicitation
To increase model stability, modify the following variables or make sure that the variables are within reasonable ranges in the *CAS* file:

* `IMPLICITATION FOR DEPTH` should be between `0.5` and `0.6`.
* `IMPLICITATION FOR VELOCITIES` should be between `0.5` and `0.6`.
* `IMPLICITATION FOR DIFFUSION` should be `1.` or smaller.

### Surface Oscillations (Wiggles)
When physically non-meaningful gradients or oscillations occur at the water surface or the bathymetry has steep slopes, the following keyword settings may help:

* `FREE SURFACE GRADIENT` - default is `1.0`, but it can be reduced to `0.1` to achieve stability (nevertheless, start with going incrementally down, such as a value of `0.9`).
* `DISCRETIZATIONS IN SPACE : 12;11` - uses quasi-bubble spatial discretization with 4-node triangles for velocity.

### Residual Mass Errors
To reduce residual mass errors use in the steering file:

```fortran
CONTINUITY CORRECTION : YES
```

### Divergence

To limit divergence issues, use the `CONTROL OF LIMITS` and `LIMIT VALUES` keywords. The `LIMIT VALUES` keyword is a list of 8 integers for minimum and maximum values for H, U, V, and T (tracers). The implementation in the steering file looks like this:

```fortran
CONTROL OF LIMITS : YES / default is NO
LIMIT VALUES : -1000;9000;-1000;1000;-1000;1000;-1000;1000 / default mins and max for H, U, V, tracer
```

### Tidal Flats

The simulation of dam breaks or flood hydrographs may cause issues leading to model instability. While the {ref}`tm2d-tidal` section in the Telemac2d steady modeling tutorial suggests physically and computationally meaningful keyword option combinations, section 16.5 in the {{ tm2d }} recommends using the following settings in the steering file as conservative choices from the BAW's Wesel example (similar to `/telemac/v8p2/examples/telemac2d/wesel/`).

```fortran
VELOCITY PROFILES : 4;0
TURBULENCE MODEL : 1
VELOCITY DIFFUSIVITY : 2.
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2
FREE SURFACE GRADIENT COMPATIBILITY : 0.9
H CLIPPING : NO
TYPE OF ADVECTION : 1;5
SUPG OPTION : 0;0
TREATMENT OF THE LINEAR SYSTEM : 2
SOLVER : 2
PRECONDITIONING : 2
SOLVER ACCURACY : 1.E-5
CONTINUITY CORRECTION : YES
```


### Exceeding Maximum Iterations
*This section is co-authored by {{ scolari }}*.

A simulation may print `EXCEEDING MAXIMUM ITERATIONS` warnings in the *Terminal*:

```fortran
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  0.7234532E-01
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
```

To troubleshoot the `EXCEEDING MAXIMUM ITERATIONS` warnings, try the following options:

*	Decrease the timestep gradually.
*	Decrease the solver accuracy (e.g. from `1.E-8` to `1.E-6`),
*	Increase the `MAXIMUM NUMBER OF ITERATIONS FOR SOLVER` keyword value, but do not exceed `200`.
*	Change the `VELOCITY PROFILE` type (read this eBook's instructions for {ref}`2d <tm2d-bounds>` or {ref}`3d  <tm3d-slf-boundaries>`).
*	Cold starts (i.e., {ref}`defining initial conditions with the INITIAL CONDITIONS keyword in the steering file <tm2d-init>`) may not converge. Therefore, either
  *	increase the `PRESCRIBED FLOWRATES` gradually (or in a {ref}`liquid boundary file <tm2d-liq-file>`), or
  *	{ref}`create an initial conditions Selafin file <bk-create-slf>`, assigning a water depth at the inlet nodes.


## Computation Speed

Some of the keywords in TELEMAC's steering (`*.cas`) file affect computation speed.

* Use the {ref}`ACCURACY and MAXIMUM ITERATION <tm2d-accuracy>` keywords to yield faster convergence.
* Deactivate `TIDAL FLATS`, even though deactivating {ref}`tidal flats <tm2d-tidal>` can not be recommended to yield physically meaningful and stable models.
* When using the GMRES solver (`SOLVER : 7`), varying the {ref}`solver options <tm2d-solver-pars>` may aid to reduce the total calculation time.
* Make sure to use the default `MATRIX STORAGE : 3` keyword.
* Use an earlier simulation (e.g., with a coarser mesh) to initiate the model with the `COMPUTATION CONTINUED : YES` and `PREVIOUS COMPUTATION FILE : *.slf` keywords (see section 4.1.3 in the {{ tm2d }}).

Moreover, Telemac2d provides a way to stop a simulation (step) when fluxes stabilize. To enable this feature, add the following block in the steering (`*.cas`) file:

```
/ steady state stop criteria in steering.cas
STOP IF A STEADY STATE IS REACHED : YES / default is NO
STOP CRITERIA : 1.E-3;1.E-3;1.E-3 / use list of three values - defaults are 1.E-4
```

However, stop criteria are not functional for non-stationary flows (e.g., {cite:t}`von_karman_mechanische_1930` vortex street downstream of bridge piers). Read more about the convergence stop criteria in the {{ tm2d }} (section 5.1).

## Mesh File

### Fine High-resolution Meshes
*This section is co-authored by {{ scolari }}*.

For creating very fine meshes with a grid size smaller than 1.0 m, a selafin (`*.slf`) geometry file should be saved in double precision format (SERAFIND). Otherwise, model boundary edges may not be well represented in the computational mesh. {numref}`Figure %s <mesh-precision>` illustrates the loss in boundary accuracy when single-precision (a) is used instead of double-precision (b).

```{figure} ../img/telemac/single-double-precision-mesh.png
:alt: telemac slf selafin single double precision serafind
:name: mesh-precision

The loss boundary precision in a single-precision selafin mesh (a) compared to a double-precision selafin mesh (b).
```


### Built-in Mesh Consistency Check

```{hint}
A 3d simulation may crash when it is used with the parameter `CHECKING THE MESH : YES`. Thus, **in 3d, favorably use `CHECKING THE MESH : NO`**.
```

To verify if TELEMAC can read the mesh, load the TELEMAC environment (e.g., `source pysource.openmpi.sh`) and go to the directory where the mesh to be checked lives and run `mdump`, for example:

```
cd ~/telemac/studies/test-case/
mdump mesh-to-test.med
```

Until the time of writing this tutorial, `mdump` asks for input variables in *French*, which mean the following:
* *Mode d'affichage de noeuds?* which means in <br>English: **Node display mode?**
    + Option `1`: Interlaced mode
    + Option `2`: Non-interlaced mode
* *Connectivité des éléments?* which means in <br>English: **Element connectivity?**
    + Option `1`: Nodal
    + Option `2`: Descending
* *Il y a 1 maillage(s) de type local dans ce fichier. Lequel voulez-vous lire (0 pour tous|1|2|3|...|n)?* which means in <br>English: **There is 1 local mesh(es) in this file. Which one do you want to read (0 for all or |1|2|3|...|n)?**
    + Option `0`: Read all
    + Option `i`: Read mesh number `i`

A standard answer combination of `1` - `1` - `0` will result in a console print of all nodes and connections between the nodes in the mesh, given that TELEMAC can read the mesh file. Starting with:

```
(**********************************************************)
(* INFORMATIONS GENERALES SUR LE MAILLAGE DE CALCUL N°01: *)
(**********************************************************)

- Nom du maillage : <<Mesh_Hn_1>>
- Dimension du maillage : 2
- Type du maillage : MED_NON_STRUCTURE
- Description associee au maillage :

(**********************************************************************************)
(* MAILLAGE DE CALCUL |Mesh_Hn_1| n°01 A L'ETAPE DE CALCUL (n°dt,n°it)=(-01,-01): *)
(**********************************************************************************)
- Nombre de noeuds : 243
- Nombre de mailles de type MED_SEG2 : 80
- Nombre de mailles de type MED_TRIA3 : 404
- Nombre de familles : 15

[...]
```

**What this output means:** If `mdump` can read the mesh, the mesh file itself is OK and potential calculation errors stem from other files such as the steering file or the boundary conditions. Otherwise, revise the mesh file and resolve any potential issue.

## Boundaries

*This section is co-authored by {{ scolari }}*.

### No Water in the Model
Erroneous simulations where **no water is entering or exiting** the domain have most likely improperly defined boundary conditions. For instance, consider the open  boundaries shown in {numref}`Fig. %s <dbg-bc-bk>` with `prescribed Q (4 5 5)` upstream and `prescribed H (5 4 4)` downstream.

```{figure} ../img/telemac/dbg-bc-bk.png
:alt: debugging boundary conditions cli bluekenue
:name: dbg-bc-bk

The definition of open (liquid) boundaries with `prescribed Q (4 5 5)` upstream and `prescribed H (5 4 4)` downstream.
```

Intuitively, you may think that the upstream boundary is number (1) and the downstream boundary is number (2). However, the order of boundary numbering depends on the definition order during the setup of the boundaries (e.g., described in the {ref}`BlueKenue pre-processing tutorial <bk-bc>`). If you do not remember the definition order, it can be read in the boundary (`*.cli`) file at any time. For instance, the boundary file for the above-shown mesh ({numref}`Fig. %s <dbg-bc-bk>`) looks like the representation in {numref}`Fig. %s <dbg-boundaries>` where the **Outlet** is defined **above** the **Inlet**. Therefore, the **downstream (Outlet) open boundary is number (1)** and the **upstream (Inlet) open boundary is number (2)** in this simulation.

```{figure} ../img/telemac/dbg-boundaries.png
:alt: debugging boundary conditions cli bluekenue
:name: dbg-boundaries

Exemplary definition of a downstream (Outlet) and an upstream (Inlet) open boundary in a boundary.cli file corresponding to {numref}`Fig. %s <dbg-bc-bk>`.
```

Thus, these two boundaries must be referenced in the steering (`*.cas`) file as follows to prescribe a flow rate `Q` (e.g., 10 m$^3$/s) at the upstream and a depth `H` (e.g., 0.75 m) at the downstream boundary:

```fortran
PRESCRIBED FLOWRATES : 0.;10
PRESCRIBED DEPTHS : 0.75;0.
```

### Problem on Boundary Number (Simulation Stop)

This section guides through debugging error messages such as:

```fortran
DEBIMP_2D: PROBLEM ON BOUNDARY NUMBER       2
        GIVE A VELOCITY PROFILE
        IN THE BOUNDARY CONDITIONS FILE
        OR CHECK THE WATER DEPTHS
        OTHER POSSIBLE CAUSE:
        SUPERCRITICAL ENTRANCE WITH FREE DEPTH
```

To get a better appreciation of the cause of the error (e.g., to figure out if supercritical flow conditions at the entrance are the cause), add the {term}`Froude number` to the output variables in the steering (`*.cas`) file. To this end, add `F` to the output variable keyword:

```fortran
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F
```

With a more precise of the cause for the error, try one of the following options:

Supercritical boundaries at the entrance
:	For supercritical flow conditions at the entrance, make sure that a `prescribed Q and H` boundary also gets a discharge and a depth assigned in the steering file. For instance, if the Inlet in Figures {numref}`%s <dbg-bc-bk>` and {numref}`%s <dbg-boundaries>` was `5 5 5` (`prescribed Q and H`) instead of `4 5 5`, the steering file needs to prescribe flowrates and depths. For instance, add a depth of `0.9` for the Inlet as follows:

  `PRESCRIBED FLOWRATES : 0.;10`

  `PRESCRIBED DEPTHS : 0.75;0.9`

Change the (vertical) velocity profile
: The definition of a `VELOCITY PROFILE` keyword in the steering file is explained in the {ref}`steady2d tutorial <tm2d-bounds>` in this eBook. The addition `VERTICAL` applies to 3d models only (read more in the {ref}`Telemac 3d (SLF) section <tm3d-slf-boundaries>`).

3d models with supercritical boundaries
: Too many vertical layers may result in very thin 3d mesh elements that cause supercritical flows locally. Thus, consider reducing the {ref}`NUMBER OF HORIZONTAL LEVELS <tm3d-slf-vertical>` in the steering file to satisfy the {term}`CFL` condition.

## Gaia (Morphodynamics)

### UNKNOWN BOUNDARY CONDITIONS

TELEMAC-Gaia may interrupt with an error message such as `KEYWORD: ... UNKNOWN BOUNDARY CONDITIONS FILE ...`. This message means that the boundary condition type in the `*.cli` file does not match the boundary conditions defined in the `*.cas` file. For instance, if the tracer (suspended load) boundary column (`9` in the Gaia `*.cli` file for `CBOR`) is set to `5`, try using `EQUILIBRIUM INFLOW CONCENTRATION : YES` or double-check the numbers defined for the **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES** keyword.

Read more about setting up boundary condition files for Gaia in the {ref}`Gaia Basics section <gaia-bc>`. The definition of boundary types in the Gaia steering file are described separately for {ref}`bedload <gaia-bc-bl>` and {ref}`suspended load <gaia-bc-sl>`.

## BlueKenue

*This section is co-authored by {{ scolari }}*.

BlueKenue may throw errors or not correctly show when working with 3d meshes. Some of the issues can be resolved by using the latest version of BlueKenue (v3.12.2-alpha at the time of editing this article).

**OnFileOpendata(): ERROR: on Activate()**
: **Causes:** The error message typically occurs with parallelized model runs when Telemac3d / PARTEL did not correctly merge the mesh at the end of the simulation.

  **Solution:** Force TELEMAC to not delete the temporary simulation folder (a folder that is visible in the simulation directory by default only while a simulation is running). Keeping the temporary calculation directory is achieved through adding a `-t` flag at the end of the simulation run command. For instance, tap the following to keep the simulation folder for a Telemac3d simulation (read more in in Annex A of the {{ tm3d }}): `telemac3d.py steering-file.cas -t`<br>The temporary folder contains T3DRES (mesh partition) files that can be merged and then opened in BlueKenue. To merge the T3DRES files run the following command (make sure the TELEMAC environment is still activated with `source pysource.YOUR-ENV.sh`):<br>`runcode.py --merge -w temp_directory/ telemac3d file.cas` <br>To get help with running this command, read [this TELEMAC Forum entry](http://opentelemac.co.uk/index.php/assistance/forum5/21-telemac-3d/7221-continue-computation-from-temporary-file).

  For **updates on this message**, follow the [BlueKenue thread in the TELEMAC Forum](http://www.openmascaret.org/index.php/assistance/forum5/blue-kenue/13278-issue-with-geometry-file?start=10#38837) for troubleshooting updates on this error.

## PostTelemac Plugin

Some versions of QGIS may throw a Python error (yellow frame in the top region of the map viewport) and a click on **Stack** reveals an error message. At the bottom of the error message, it might be written `import error: no module named gdal`. The error probably stems from an import statement in one of the PostTelemac plugin's Python scripts. To troubleshoot the gdal import error, find the Python script that is raising the error message. For instance, `C:\Users\USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\PostTelemac\meshlayerparsers\`**`posttelemac_hdf_parser.py`** may cause the error with its `import gdal` statement. Therefore:

* Open the concerned file, which is here: **`posttelemac_hdf_parser.py`**
* Find the `import gdal` statement and **replace it with `from osgeo import gdal` (i.e.,  <s>`import gdal`</s> and write `from osgeo import gdal`)
* Save and close the Python file.

Retry to start the PostTelemac plugin. It should run without issues now.


## SALOME-HYDRO

(salome-dbg)=
### SALOME-HYDRO not starting  (**Kernel/Session**)

If an error message is raised by `Kernel/Session` in the `Naming Service` (typically ends up in `[Errno 3] No such process` ... `RuntimeError: Process NUMBER for Kernel/Session not found`), there are multiple possible origins that partially root in potentially hard-coded library versions of the installer. To troubleshoot:

* Manually create copies of newer libraries with names of older versions. For instance,
  + In the 4th line after running `./salome`, `Kernel/Session` may prompt `error while loading [...] libSOMETHING.so.20 cannot open [...] No such file or directory`
  + Identify the version installed with `whereis libSOMETHING.so.20` (replace `libSOMETHING.so.20` with the missing library); for example, this may output `/usr/lib/x86_64-linux-gnu/libSOMETHING.so.40`
  + Create a copy of the newer library and rename the copy as needed by SALOME; for example, tap  `sudo cp /usr/lib/x86_64-linux-gnu/libSOMETHING.so.40 usr/lib/x86_64-linux-gnu/libSOMETHING.so.20`
  + Most likely, the following files need to be copied:
```
sudo cp /usr/lib/x86_64-linux-gnu/libmpi.so.40 /usr/lib/x86_64-linux-gnu/libmpi.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libicui18n.so.63 /usr/lib/x86_64-linux-gnu/libicui18n.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicuuc.so.63 /usr/lib/x86_64-linux-gnu/libicuuc.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicudata.so.63 /usr/lib/x86_64-linux-gnu/libicudata.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libnetcdf.so.13 /usr/lib/x86_64-linux-gnu/libnetcdf.so.11
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_java.so.40 /usr/lib/x86_64-linux-gnu/libmpi_java.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.40 /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.20
```

* Overwrite the SALOME-HYDRO's internal version of *Qt*:
  + Copy `/usr/lib/x86_64-linux-gnu/libQtCore.so.5`
  + Paste in `/Salome-V2_2/prerequisites/Qt-591/lib/` - confirm replacing `libQtCore.so.5`


(qt-dbg)=
### GUI/Qt5 support (GTK version compatibility)

With the newer versions of the *Qt platform* any menu entry in *SALOME-HYDRO* will not show up. To fix this issue, install and configure `qt5ct` styles:

* `sudo apt install qt5-style-plugins libnlopt0`
* `sudo apt install qt5ct`
* Configure `qt5ct` (just tap `qt5ct` in *Terminal*)
  + Go to the *Appearance* tab
  + Set *Style* to `gtk2` and *Standard dialogs* to `GTK2`
  + Click on *Apply* and *OK*
* Open the file `~/.profile` (e.g. use the file browser, go to the `Home` folder and press `CTRL` + `H` to toggle viewing hidden files) and add at the very bottom of the file:

```
export QT_STYLE_OVERRIDE=gtk2
export QT_QPA_PLATFORMTHEME=qt5ct
```

* Save and close `.profile` and reboot (or just re-login).

```{note}
If a file called `~/.bash_profile` (or `~/.bash_login`) exists, the above lines should be written to this `~/.bash_profile`/`~/.bash_login` because in this case, `.profile` will not be read when logging in.
```

Learn about *Qt* more at [archlinux.org](https://bbs.archlinux.org/viewtopic.php?id=214147&p=3) and in the [arch wiki](https://wiki.archlinux.org/index.php/Uniform_look_for_Qt_and_GTK_applications#QGtkStyle).
