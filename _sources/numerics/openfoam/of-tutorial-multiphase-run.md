```{admonition} Contributor
:class: tip
This chapter was written and developed by {{ scolari }} <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="50" height="50">
```

# Run OpenFOAM

After having created and filled in all necessary dictionaries, the case can finally be run. 

* The first step consists in initializing a region containing water as defined in the *setFieldsDict* file.

```
user@user123:~/OpenFOAM-9/channel/Simulation$ setFields
```

* For parallel runs, use the `decomposePar` command, as done during the meshing process, to decompose the geometry into individual geometries for each MPI process.

```
user@user123:~/OpenFOAM-9/channel/Simulation$ decomposePar

```

* Start running the simulation by typing the following in the terminal window:

    * In the case of parallel runs (substitute "x" with the number of cores):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ mpirun -np x interFoam -parallel
```

    * Alternatively:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ interFoam
```

Below, an example of the output screen of the *interFoam* solvers is shown. The main aspects are the following:

* The first line shows the mean and maximum flow {term}`CFL` condition.
* Line 2 shows instead the interface {term}`CFL` condition, which is more restrictive than the previous and should be strictly below 1 when solving multiphase flows.
* "MULES: Correcting alpha.water" depends on the value set to *nAlphaCorr* set in the *fvSolution* file.
* Lines 7 and 9 refer to the *nAlphaSubCycles*, which was set to 1, meaning only one loop.
* Lines 11, 13, and 15 refer to the three pressure correctors and no non-orthogonal corrections are present.
* As shown in line 16, a tighter tolerance is applied only to this iteration (p-rghFinal).
  
```
1    Courant Number mean: 0.00233217 max: 0.961058
2    Interface Courant Number mean: 0.000313967 max: 0.234243
3    deltaT = 0.000461857
4    Time = 148.004
5 
6    smoothSolver:  Solving for alpha.water, Initial residual = 2.35103e-05, Final residual = 1.00306e-08, No Iterations 1
7    Phase-1 volume fraction = 0.144966  Min(alpha.water) = -1.2641e-05  Max(alpha.water) = 1
8    MULES: Correcting alpha.water
9    MULES: Correcting alpha.water
10   Phase-1 volume fraction = 0.144966  Min(alpha.water) = -2.71177e-05  Max(alpha.water) = 1
11   DICPCG:  Solving for p-rgh, Initial residual = 0.000249542, Final residual = 1.17508e-05, No Iterations 6
12   time step continuity errors : sum local = 8.05179e-08, global = 6.39537e-10, cumulative = -2.18471e-08
13   DICPCG:  Solving for p-rgh, Initial residual = 2.05956e-05, Final residual = 1.01515e-06, No Iterations 58
14   time step continuity errors : sum local = 6.95406e-09, global = -1.17766e-09, cumulative = -2.30247e-08
15   DICPCG:  Solving for p-rgh, Initial residual = 2.95498e-06, Final residual = 9.64318e-08, No Iterations 75
16   time step continuity errors : sum local = 6.60043e-10, global = 5.94012e-11, cumulative = -2.29653e-08
17   smoothSolver:  Solving for epsilon, Initial residual = 0.0002476, Final residual = 5.94123e-06, No Iterations 1
18   bounding epsilon, min: -3.63319e-06 max: 21370 average: 8.9958
19   smoothSolver:  Solving for k, Initial residual = 0.000103198, Final residual = 1.17097e-06, No Iterations 1
20   ExecutionTime = 63.45 s  ClockTime = 64 s
```

