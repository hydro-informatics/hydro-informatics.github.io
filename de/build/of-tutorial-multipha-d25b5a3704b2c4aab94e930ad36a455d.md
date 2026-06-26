---
description: Tutorial für die Durchführung von OpenFOAM Mehrphasen-Flow-Simulationen, die Feld- Initialisierung, Solvenz-Ausführung und Überwachung für hydraulische Engineering-Anwendungen.
---

# OpenFOAM

Nachdem er in allen notwendigen Wörterbüchern erstellt und gefüllt ist, kann der Fall schließlich laufen.

* Der erste Schritt besteht darin, eine Region mit Wasser wie in der *setFieldsDict*-Datei definiert zu initialisieren.

```
user@user123:~/OpenFOAM-9/channel/Simulation$ setFields
```

* Für Parallelläufe verwenden Sie den `decomposePar`-Befehl, wie er während des Meshing-Prozesses ausgeführt wird, um die Geometrie in einzelne Geometrien für jeden [MPI (Message Passing Interface, Standard für Parallel Computing)](https://www.mpi-forum.org/)-Prozess zu zerlegen.

```
user@user123:~/OpenFOAM-9/channel/Simulation$ decomposePar

```

* Starten Sie die Simulation, indem Sie im Terminalfenster Folgendes eingeben:

    * Bei Parallelläufen (Substitute "x" mit der Anzahl der Kerne):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ mpirun -np x interFoam -parallel
```

    * Alternativ:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ interFoam
```

Im Folgenden wird ein Beispiel des Ausgabebildschirms der *interFoam*-Löser dargestellt. Die wichtigsten Aspekte sind:

* Die erste Zeile zeigt den mittleren und maximalen Fluss {term}`CFL`Zustand.
* Zeile 2 zeigt stattdessen die Schnittstelle {term}`CFL`Zustand, die restriktiver als die vorherige ist und bei der Lösung von Mehrphasenflüssen streng unter 1 sein sollte.
* "MULES: Correcting alpha.water" hängt von dem Wert ab, der in der *fvSolution*-Datei auf *nAlphaCorr* gesetzt wird.
* Die Zeilen 7 und 9 beziehen sich auf die *nAlphaSubCycles*, die auf 1 gesetzt wurde, was nur eine Schleife bedeutet.
* Die Leitungen 11, 13 und 15 beziehen sich auf die drei Druckkorrektoren und es liegen keine nicht-orthogonalen Korrekturen vor.
* Wie in Zeile 16 gezeigt, wird nur auf diese Iteration (p-rghFinal) eine engere Toleranz angewendet.
  
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

