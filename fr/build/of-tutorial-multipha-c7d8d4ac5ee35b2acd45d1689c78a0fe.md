---
description: Tutoriel pour l'exécution de simulations de flux multiphases OpenFOAM, couvrant l'initialisation sur le terrain, l'exécution du solveur et la surveillance pour les applications d'ingénierie hydraulique.
---

# Exécuter OpenFOAM

Après avoir créé et rempli tous les dictionnaires nécessaires, le cas peut enfin être exécuté.

* La première étape consiste à initialiser une région contenant de l'eau telle que définie dans le fichier *setFieldsDict*.

```
user@user123:~/OpenFOAM-9/channel/Simulation$ setFields
```

* Pour les parcours parallèles, utilisez la commande `decomposePar`, comme cela a été fait pendant le processus de maillage, pour décomposer la géométrie en géométries individuelles pour chaque [MPI (Message Passing Interface, une norme pour le calcul parallèle)](https://www.mpi-forum.org/) process.

```
user@user123:~/OpenFOAM-9/channel/Simulation$ decomposePar

```

* Commencez à exécuter la simulation en tapant ce qui suit dans la fenêtre du terminal :

    * Dans le cas de parcours parallèles (suppléter "x" avec le nombre de carottes):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ mpirun -np x interFoam -parallel
```

    * Sinon:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ interFoam
```

Ci-dessous, un exemple de l'écran de sortie des solveurs *interFoam* est affiché. Les principaux aspects sont les suivants:

* La première ligne indique le débit moyen et maximal {term}`Nombre de Courant <CFL>` condition.
* La ligne 2 montre plutôt l'interface {term}`Nombre de Courant <CFL>` condition, qui est plus restrictive que la précédente et devrait être strictement inférieure à 1 lors de la résolution des flux multiphasés.
* "MULES: Correction alpha.water" dépend de la valeur définie à *nAlphaCorr* définie dans le fichier *fvSolution*.
* Les lignes 7 et 9 renvoient aux *nAlphaSubCycles*, qui ont été fixés à 1, ce qui signifie qu'il n'y a qu'une seule boucle.
* Les lignes 11, 13 et 15 renvoient aux trois correcteurs de pression et il n'y a aucune correction non orthogonale.
* Comme le montre la ligne 16, une tolérance plus stricte n'est appliquée qu'à cette itération (p-rghFinal).
  
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

