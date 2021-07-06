# Debugging TELEMAC/SALOME


Since its early development, *TELEMAC* has become a robust an reliable tool for the numerically modelling of open surface flows. Yet there are a few little challenges and this page provides some answers (under development).

## Traceback errors

If a simulation crashes and it is not clear why, debugging with [*gdb*](http://www.gdbtutorial.com) is a good option. To do so, first install *gdb*:

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

## Errors in Steering (CAS) Files

* make sure to use `:` rather than `=`
* place all model files in the same folder and only use file names without the directories of files

## Instable Simulations

### Accuracy

When the accuracy keywords are improperly defined, TELEMAC may not be able to end the simulation. In this case make sure to comment out the accuracy keywords and let TELEMAC use its default values:

```fortran
/ SOLVER ACCURACY : 1.E-4
/ ACCURACY FOR DIFFUSION OF TRACERS : 1.E-4
/ ACCURACY OF K : 1.E-6
/ ACCURACY OF EPSILON : 1.E-6
/ ACCURACY OF SPALART-ALLMARAS : 1.E-6
```

Moreover, variable time-step calculation may cause eternal model runs (i.e., activated with `VARIABLE TIME-STEP : YES`). To deactivate variable time-step calculation use `VARIABLE TIME-STEP : NO` and define a `TIME STEP` (e.g., `1.`)

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

The simulation of dam breaks or flood hydrographs may cause issues leading to model instability. While the {ref}`tm2d-tidal` section in the Telemac2d steady modeling tutorial suggests physically and computationally meaningful keyword option combinations, section 16.5 in the {{ tm2d }} recommends to use the following settings in the steering file as conservative choices from the BAW's Wesel example (similar to `/telemac/v8p2/examples/telemac2d/wesel/`).

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

## Computation Speed

Some of the keywords in TELEMAC's steering (`*.cas`) file affect computation speed.

* Use the {ref}`ACCURACY and MAXIMUM ITERATION <tm2d-accuracy>` keywords to yield faster convergence.
* Deactivate `TIDAL FLATS`, even though deactivating {ref}`tidal flats <tm2d-tidal>` can not be recommended to yield physically meaningful and stable models.
* When using the GMRES solver (`SOLVER : 7`), varying the {ref}`solver options <tm2d-solver-pars>` may aid to reduce the total calculation time.
* Make sure to use the default `MATRIX STORAGE : 3` keyword.
* Use an earlier simulation (e.g., with a coarser mesh) to initiate the model with the `COMPUTATION CONTINUED : YES` and `PREVIOUS COMPUTATION FILE : *.slf` keywords (see section 4.1.3 in the {{ tm2d }}).

## Errors in Mesh Files

```{hint}
A 3d simulation may crash when it is used with the parameter `CHECKING THE MESH : YES`. Thus, **in 3d, favorably use `CHECKING THE MESH : NO`**.
```

To verify if TELEMAC can read the mesh, load the TELEMAC environment, for example:

```
cd ~/telemac/v8p2/configs
source pysource.openmpi.sh
config.py
```

The go to the directory where the mesh to be checked lives and run `mdump`, for example:

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

A standard answer combination of `1` - `1` - `0` will result in a console print of all nodes and connections between the nodes in the mesh, given that *TELEMAC* is able to read the mesh file. Starting with:

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

*What does this mean?* If `mdump` can read the mesh, the mesh file itself is OK and potential calculation errors stem from other files such as the steering file or the boundary conditions. Otherwise, revise the mesh file and resolve any potential issue.

## SALOME-HYDRO

### SALOME-HYDRO not starting  (**Kernel/Session**) {#salome-dbg}

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
* Open the file `~/.profile` (e.g. use the file browser, go to the `Home` folder and pressing `CTRL` + `H` to toggle viewing hidden files) and add at the very bottom of the file:

```
export QT_STYLE_OVERRIDE=gtk2
export QT_QPA_PLATFORMTHEME=qt5ct
```

* Save and close `.profile` and reboot (or just re-login).


```{note}
If a file called `~/.bash_profile` (or `~/.bash_login`) exists, the above lines should be written to this `~/.bash_profile`/`~/.bash_login` because in this case, `.profile` will not be read when logging in.
```

Learn about *Qt* more at [archlinux.org](https://bbs.archlinux.org/viewtopic.php?id=214147&p=3) and in the [arch wiki](https://wiki.archlinux.org/index.php/Uniform_look_for_Qt_and_GTK_applications#QGtkStyle).
