---
description: Tutoriel pour l'exécution de la configuration du boîtier de flux multiphase OpenFOAM.
---

# Mise en place du dossier

Lors de la configuration du dossier de cas, les modifications doivent être faites aux fichiers suivants:

* Dans le dossier *Constant* : les différents fichiers de propriétés et le fichier limite dans le dossier *polyMesh*.
* Dans le dossier *System* : les fichiers setFieldsDict, fvSchemes, fvSolution et controlDict.
* Dans le dossier *0* : tous les fichiers qui contiennent.

# Le sous-répertoire *Constant*

Après avoir copié le dossier *polyMesh* à partir des résultats *snappyHexMesh*, il est nécessaire de définir correctement le type des différents éléments composant dans le fichier **boundary**. Par exemple, dans l'exemple ci-dessous, l'élément *Gravel-bottom* était défini comme *wall* alors que l'élément *Inlet* était défini comme *patch*.

```
FoamFile
{
    format      ascii;
    class       polyBoundaryMesh;
    location    "constant/polyMesh";
    object      boundary;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

...
 
    Gravel-bottom
    {
        type            wall;
        inGroups        List<word> 1(wall);
        nFaces          132062;
        startFace       5105689;
    }
    Inlet
    {
        type            patch;
        inGroups        List<word> 1(wall);
        nFaces          288;
        startFace       5237751;
    }
    
 ...
```

Différents types de patch sont disponibles dans OpenFOAM. Pour une explication détaillée, veuillez consulter la section [boundaries](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.2-boundaries) du [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/).

* * patch*: patch générique
* *symétriePlane*: plan de symétrie
* *vide*: des plans arrière d'une géométrie 2D
* * bord* : coin avant et arrière pour une géométrie axisymétrique
* *cyclique*: plan cyclique
* *wall*: utilisé pour définir les fonctions de paroi dans le flux turbulent
* *processeur* : limite interprocesseur

Les fichiers suivants doivent être ajoutés pour définir les propriétés du cas ainsi qu'une liste de fichiers de propriétés pour le cas présent.

```{figure} ../../img/openfoam/interFoam/cases/constant-folder.png
:alt: openfoam 
:name: if-constant-folder

Contenu du dossier constant.
```

Dans les fichiers *turbulenceProperties*, le modèle de turbulence est défini. OpenFOAM comprend le support pour les types de modélisation de turbulence suivants:

* {term}`Reynolds Averaged (Navier-Stokes) <RANS>` Simulation (Moyenne de Reynolds, appelé RAS dans OpenFOAM),
* Simulation Eddy détachée (DES), et
* Simulation de grande taille (LES)

```
simulationType  RAS;

RAS
{
    RASModel        kEpsilon;

    turbulence      on;

    printCoeffs     on;
}
```

Le fichier *transportProperties* définit les propriétés des deux phases considérées en l'espèce (air et eau) et la tension de surface entre les deux phases.

```
phases (water air);

water
{
    transportModel  Newtonian;
    nu              [0 2 -1 0 0 0 0] 1e-06;
    rho             [1 -3 0 0 0 0 0] 1000;
    CrossPowerLawCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 1e-06;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        m               m [ 0 0 1 0 0 0 0 ] 1;
        n               n [ 0 0 0 0 0 0 0 ] 0;
    }

    BirdCarreauCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 0.0142515;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        k               k [ 0 0 1 0 0 0 0 ] 99.6;
        n               n [ 0 0 0 0 0 0 0 ] 0.1003;
    }
}

air
{
    transportModel  Newtonian;
    nu              [0 2 -1 0 0 0 0] 1.48e-05;
    rho             [1 -3 0 0 0 0 0] 1;
    CrossPowerLawCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 1e-06;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        m               m [ 0 0 1 0 0 0 0 ] 1;
        n               n [ 0 0 0 0 0 0 0 ] 0;
    }

    BirdCarreauCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 0.0142515;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        k               k [ 0 0 1 0 0 0 0 ] 99.6;
        n               n [ 0 0 0 0 0 0 0 ] 0.1003;
    }
}

sigma           [1 0 -2 0 0 0 0] 0.072;
```

Lors de la sélection du modèle de turbulence RAS, il faut ajouter le sous-dictionnaire *RASproperties*. Ce fichier contient les mots-clés définissant le nom du modèle de turbulence RAS, l'option d'activer ou de désactiver la modélisation de turbulence, et un interrupteur pour imprimer les coefficients du modèle au terminal au démarrage de la simulation.

```
RASModel        kEpsilon;
turbulence      on;
printCoeffs     on;
```

Le dictionnaire *momentumTransport* est lu par tout solveur qui inclut la modélisation de turbulence. Les mots-clés définis dans cette sous-diction sont les mêmes que ceux décrits ci-dessus.

```
simulationType  RAS;

RAS
{
    model           kEpsilon;
    turbulence      on;
    printCoeffs     on;
}
```

Les modèles de turbulence peuvent être listés en exécutant un solveur avec l'option *-listMomentumTransportModèles*:

```
user@user123:~/OpenFOAM-9/channel/$ interFoam -listMomentumTransportModels
```

Enfin, le sous-dictionnaire *g* définit simplement l'accélération gravitationnelle et les unités utilisées.

```
dimensions      [ 0 1 -2 0 0 0 0 ];
value           ( 0 0 -9.8065 );
```

****

# Le répertoire *Système*

Le dossier *System* contient les paramètres associés à la procédure de solution elle-même. Les fichiers obligatoires pour l'exécution de la simulation sont le *controlDict* dans lequel les paramètres de contrôle d'exécution sont définis et ceux pour la sortie des données; notamment, les *fvSchemes* où les schémas de discrétisation utilisés dans la solution peuvent être sélectionnés et le *fvSolution* dans lequel les résolveurs d'équations, les tolérances et autres contrôles algorithmes sont définis. De plus, le *setFieldsDict* est ajouté, ce qui permet à l'utilisateur de définir des valeurs sur un ensemble sélectionné de cellules/faces-patch.

Dans le fichier *controlDict*, plusieurs paramètres de contrôle peuvent être définis comme, par exemple, les heures de début et de fin et l'étape temporelle dT de la simulation. En particulier, lors de l'exécution d'une simulation de démarrage à froid (c'est-à-dire un cas dans lequel le canal est initialement sec), l'étape de temps doit être réglée à *ajustable* permettant de régler l'étape de temps en fonction de l'état maximal {term}`CFL` dans la simulation transitoire. De plus, la valeur maximale de l'état {term}`CFL` *maxCo* et la valeur maximale à l'interface *maxAlphaCo* doivent être attribuées.

```
application     interFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         3600;
deltaT          0.1;
writeControl    adjustableRunTime;
writeInterval   1;
purgeWrite      0;
writeFormat     binary;
writePrecision  6;
writeCompression uncompressed;
timeFormat      general;
timePrecision   6;

runTimeModifiable yes;
adjustTimeStep  yes;

maxCo           1.0;
maxAlphaCo      1.0;
maxDeltaT       1.0;
```

Le dictionnaire *fvSchemes* du répertoire système définit les schémas numériques des termes qui apparaissent dans l'application en cours d'exécution. Pour les schémas temporels *ddtSchemes*, à l'exception du schéma d'Euler précis de premier ordre, d'autres options sont disponibles, comme les schémas Cran-Nicholson de deuxième ordre et rétrograde. Les schémas de gradient *gradSchemes* sont ensuite définis. Les régimes disponibles sont le régime de gradient de Gauss et le régime de gradient des moindres carrés. Le schéma d'interpolation peut être linéaire à base cellulaire (linéaire) ou linéaire à base ponctuelle (pointLinear) ou moins de carrés (leastSquares). Le schéma de divergence à utiliser peut être défini avec le mot clé *divSchemes*. Des informations détaillées concernant les options disponibles et la syntaxe correspondante peuvent être trouvées dans la section [diversité schemes](https://www.openfoam.com/documentation/guides/latest/doc/guide-schemes-divergence.html) de la [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/). Pour les *laplacianSchemes*, toutes les options sont basées sur l'application du théorème de Gauss, exigeant ainsi un schéma d'interpolation pour transformer les coefficients des valeurs cellulaires aux faces, et un schéma de gradient surface-normal. Les *schemes d'interpolation* sont nécessaires pour transformer les quantités de centres cellulaires en centres de visage. Plusieurs schémas d'interpolation sont disponibles, de ceux basés uniquement sur la géométrie à, par exemple, {term}`convection <Convection>` schémas qui sont une fonction du flux local.

```
ddtSchemes
{    default         Euler;}

gradSchemes
{    default         Gauss linear;}

divSchemes
{
    div(rhoPhi,U)   Gauss linearUpwind grad(U);
    div(phi,alpha)  Gauss interfaceCompression vanLeer 1;
    div(phi,k)      Gauss upwind;
    div(phi,epsilon) Gauss upwind;
    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
}

laplacianSchemes
{    default         Gauss linear corrected;}

interpolationSchemes
{    default         linear;}

snGradSchemes
{    default         corrected;}

wallDist
{    method meshWave;}
```

Les fichiers *fvSolution* contiennent un ensemble de sous-dictions spécifiques au solveur en cours d'exécution. De plus, il existe un ensemble de sous-dictions standard, y compris les *solvers*, *relaxationFactors*, *PISO* et *SIMPLE*, qui couvrent la plupart de celles utilisées par les solveurs standard. Un exemple de l'ensemble d'entrées requis pour le solveur interFoam peut être trouvé dans le dossier [case folder](https://github.com/hydro-informatics/openfoam.git) (*Simulation*). Vous trouverez un aperçu détaillé de toutes les options disponibles dans le [Guide de l'utilisateur OpenFOAM](https://doc.cfd.direct/openfoam/user-guide/) [Solution et Algorithm Control](https://www.openfoam.com/documentation/user-guide/6-solving/6.3-solution-and-algorithm-control)].

Le *setFieldsDict* permet à l'utilisateur d'attribuer une certaine valeur à un ensemble sélectionné de cellules/faces-patch. Pour le présent tutoriel, ce dictionnaire a été utilisé pour attribuer un niveau d'eau initial à l'entrée du modèle. Plusieurs options sont disponibles pour sélectionner les cellules d'intérêt. Dans l'exemple ci-dessous, l'option *boxToCell* a été sélectionnée, qui sélectionne toutes les cellules dont le centre cellulaire est situé à l'intérieur de la zone de délimitation donnée.

```
defaultFieldValues
(
    volScalarFieldValue alpha.water 0
);

regions    // Select based on surface
(
    boxToCell
    {
        box (-3.6 5.1 -2.5) (0.4 -4.0 1.2);
        fieldValues
        (
            volScalarFieldValue alpha.water 1
        );
    }
);
```

On peut aussi utiliser d'autres sources, comme *fieldToCell*, qui sélectionne toutes les cellules caractérisées par une valeur de champ dans la plage sélectionnée [min; max]. Une option très utile lors du réglage du niveau initial d'eau est aussi la source *surfaceToCell* qui sélectionne les cellules à l'aide d'une surface, basée sur une surface {term}`STL` importée. Dans ce cas, le dictionnaire ressemblerait à:

```
defaultFieldValues
(
    volScalarFieldValue alpha.water 0
);

regions    // Select based on surface
(
  surfaceToCell
      {
          file            "./constant/triSurface/water.stl";
          outsidePoints   ((x y z));
          includeCut      true;
          includeInside   true;
          includeOutside  false;
          nearDistance    -1;
          curvature       -100;
          fieldValues
          (
              volScalarFieldValue alpha.water 1
          );
      }
 );
```

Le mot-clé *outsidePoints* définit l'extérieur de la surface. *InclureCut*, *InclureInside* et *InclureOutside* sont des booléens qui déterminent s'il faut inclure dans la sélection les cellules coupées par la surface, les cellules à l'intérieur de la surface et/ou à l'extérieur de la surface, respectivement. Le mot-clé *nearDistance* est un scalaire qui détermine quelles cellules avec le centre près de la surface à inclure. Enfin, *courbure* comprend les cellules proches d'une forte courbure à la surface.

Une liste complète de toutes les sources disponibles se trouve dans la section [OpenFOAM Wiki](https://openfoamwiki.net/index.php/TopoSet) dans la section *TopoSet*.

# Le répertoire *0*
Le répertoire *0* est le répertoire temporel contenant les fichiers décrivant les conditions initiales de la simulation. Dans ce répertoire, un fichier texte pour chaque champ est requis pour l'exécutable du résolveur interFoam. Dans le cas présent, ces fichiers incluent : $U$ pour la vitesse de débit, *p-rgh* pour la pression dynamique, *nut* pour la viscosité turbulente, $k$ pour le {term}`turbulent kinetic energy <Turbulent kinetic energy>`, $\epsilon$ pour le taux de dissipation de l'énergie cinétique turbulente, et *alpha.water.orig* pour les phases initiales. L'ensemble complet des fichiers utilisés pour ce tutoriel se trouve dans le [case folder](https://github.com/hydro-informatics/openfoam.git).


# Dictionnaires variables

## Champ U Dictionnaire

Ce dictionnaire définit les conditions limites et la configuration initiale du champ vecteur $U$. Pour les conditions initiales uniformes *internalField* avec une valeur de (0 0 0) ont été définies. Pour tous les murs et patchs restants, les éléments suivants ont été assignés:

* **Patch air** : *pressionOutletVelocity* condition, qui attribue une condition de gradient zéro au flux sortant du domaine et une vitesse basée sur le flux dans la direction patch-normale au flux entrant dans le domaine.
* **Surfaces de béton, fond de gravier et zones d'obstacle**: *aucun état de glissement*. La vitesse du patch est réglée à (0 0 0)
* **Patch d'entrée**: une condition *flowRateInletVelocity* a été choisie. Cela permet de définir le débit volumétrique ou massique à l'entrée.
* ** patch de sortie** : une condition limite *zeroGradient* a été définie. Les valeurs internes sont donc extrapolées à la face limite.

```
dimensions      [0 1 -1 0 0 0 0]; //kg m s K mol A cd
internalField   uniform (0 0 0);

boundaryField
{
     Air
        {
        	type            pressureInletOutletVelocity;
         	value           uniform (0 0 0);
        }

     Concrete-sides
        {
        	type            noSlip;
        }

     Gravel-bottom
        {
        	type            noSlip;
        }

     Inlet
        {
        	type            flowRateInletVelocity;
        	volumetricFlowRate constant 0.5;
	}

     Obstacle
        {
        	type            noSlip;
        }

     Outlet
        {
                type            zeroGradient;
        }
}
```

## dictionnaire de champ p-rgh

Ce dictionnaire définit les conditions de limites et la configuration initiale du champ dimensionnel p-rgh, exprimé en Pa. Le *internalField* a été initialisé avec une valeur 0 dans l'ensemble du domaine. Les champs restants étaient les suivants :

* **Patch aérien**: la pression totale* a été attribuée. Cette condition fixe la pression statique sur le dispositif en fonction de la spécification de la pression totale et permet de représenter adéquatement la pression atmosphérique.
* **Tous les autres patchs**: la condition utilisée était une limite *fixedFluxPressure*. Cette condition limite est utilisée comme alternative à *zeroGradient*, dans les cas où la gravité et la tension de surface sont également présentes dans les équations de solution.

```
dimensions      [1 -1 -2 0 0 0 0];//kg m s K mol A cd
internalField   uniform 0;//initially atmospheric pressure in the entire domain

boundaryField
{
     Air
        {
        	type            totalPressure;
        	p0              uniform 0;
        }

     Concrete-sides
        {
        	type            fixedFluxPressure;
        	value           uniform 0; 
        }

     Gravel-bottom
        {
        	type            fixedFluxPressure;
        	value           uniform 0;
        }

     Inlet
        {
        	type            fixedFluxPressure;
        	value           uniform 0;
	}

     Obstacle
        {
        	type            fixedFluxPressure;
        	value           uniform 0;
        }

     Outlet
        {
                type            fixedFluxPressure;
        	value           uniform 0;
        }
}
```

## champ de noix Dictionnaire

Ce dictionnaire définit les conditions limites et la configuration initiale de l'écrou de viscosité turbulente, exprimée en m$^2$/s. Le *internalField* a été initialisé avec une valeur 0 dans tout le domaine. Les champs restants ont été définis comme suit :

* **Air, Inlet et Outlet patch** : la condition a été fixée à *calculée*, ce qui signifie qu'aucune valeur n'est prescrite et qu'elle est calculée à partir du modèle de turbulence {term}`RANS` et des valeurs pour $k$ ({term}`turbulent kinetic energy <Turbulent kinetic energy>`) et $\epsilon$ dans ce cas.
* **Toutes les parois restantes** : l'état de la limite *nuskRoughWallFunction* a été appliqué.

Cette condition limite fournit une contrainte murale sur la viscosité turbulente. Cela permet de tenir compte des effets de la rugosité. La mise en œuvre des différents matériaux présents dans le modèle a été effectuée en définissant les différentes hauteurs de rugosité ks (par exemple, 0,0052 pour les murs en béton).

```
dimensions      [0 2 -1 0 0 0 0];
internalField   uniform 0;

boundaryField
{

    Air
    {
      type            calculated;
      value           uniform 0;
    }

    Concrete-sides
    {
      type            nutkRoughWallFunction;
      Ks              uniform 0.0052;
      Cs              uniform 0.5;
      value           uniform 0;
    }

    Gravel-bottom
    {
      type            nutkRoughWallFunction;
      Ks              uniform 0.15;
      Cs              uniform 0.5;
      value           uniform 0;
    }

    Inlet
    {
      type            calculated;
      value           uniform 0;
    }

    Obstacle
    {
      type            nutkRoughWallFunction;
      Ks              uniform 0.0052;
      Cs              uniform 0.5;
      value           uniform 0;
    }

    Outlet
    {
        type            calculated;
        value           uniform 0;
    }
}
```

## champ k Dictionnaire

Ce dictionnaire définit les conditions limites et la configuration initiale pour le {term}`turbulent kinetic energy <Turbulent kinetic energy>` $k$, exprimée en m$^2$/s. Le *internalField* a été initialisé avec une valeur uniforme dans l'ensemble du domaine. Les champs restants étaient les suivants :

```{aside} Meaning of letters
*q* pour la racine carrée de l'énergie cinétique turbulente et *R* pour le tenseur de stress Reynolds (lisez plus dans le glossaire à {term}`turbulent kinetic energy <Turbulent kinetic energy>`.
```

* **Patch air et sortie**: *inletOutlet*, qui correspond à une condition *zeroGradient*, à l'exception du cas où le vecteur de vitesse à côté de la limite est dirigé à l'intérieur du domaine. Dans ce dernier cas, il passe à un état *fixedValue*.
* **Patch d'entrée**: *fixedValue*. La valeur correspondante était celle attribuée au champ interne*.
* **Tous les murs restants**: *kqRWallFunction*. Cette condition limite fournit un enrouleur simple autour de l'état de gradient zéro.


```
dimensions      [0 2 -2 0 0 0 0];
internalField   uniform 1.22e-03;

boundaryField
{
    Air
  {
      type            inletOutlet;
      inletValue      $internalField;
      value           $internalField;
  }

  Concrete-sides
  {
    type            kqRWallFunction;
    value           $internalField;
  }

  Gravel-bottom
  {
    type            kqRWallFunction;
    value           $internalField;
  }

  Inlet
  {
    type            fixedValue;
    intensity       0.05;
    value           $internalField;
  }

  Obstacle
  {
    type            kqRWallFunction;
    value           $internalField;
  }

  Outlet
  {
      type            inletOutlet;
      inletValue      $internalField;
      value           $internalField;
  }
}
```

## epsilon champ Dictionnaire

Ce dictionnaire définit les conditions limites et les premières dispositions pour le taux de dissipation $\epsilon$ de {term}`turbulent kinetic energy <Turbulent kinetic energy>`, exprimé en m$^2~$s$^{-3}$. Le *internalField* a été initialisé avec une valeur uniforme dans l'ensemble du domaine. Les champs restants ont été définis comme suit :

* **Patch air et sortie**: *inletOutlet*, comme décrit ci-dessus pour $k$.
* **Patch d'entrée**: *fixedValue*, correspondant à la valeur interne Field.
* **Tous les murs restants**: *epsilonWallFunction*. Cette condition limite fournit une contrainte de paroi sur le taux de dissipation d'énergie cinétique turbulente $\epsilon$ et l'énergie cinétique turbulente $k$ contribution de production pour les modèles de turbulences de nombres de Reynolds faibles et élevées.

```
dimensions      [0 2 -3 0 0 0 0];
internalField   uniform 3.20e-05;

boundaryField
{
    Air
    {
        type            inletOutlet;
        inletValue      $internalField;
        value           $internalField;
    }

    Concrete-sides
    {
      type            epsilonWallFunction;
      value           $internalField;
    }

    Gravel-bottom
    {
      type            epsilonWallFunction;
      value           $internalField;
    }

    Inlet
    {
      type            fixedValue;
      value           $internalField;
    }

    Obstacle
    {
      type            epsilonWallFunction;
      value           $internalField;
    }

    Outlet
    {
        type            inletOutlet;
        inletValue      $internalField;
        value           $internalField;
    }
}
```

## alpha.water field Dictionnaire

Ce dictionnaire définit les conditions limites et les conditions initiales du champ non-dimensionnel alpha.water. Le *internalField* a été initialisé avec une valeur uniforme égale à 0 dans tout le domaine, ce qui signifie qu'aucune eau n'est présente dans le domaine au moment 0. L'eau sera ensuite initialisée en exécutant la commande *setFields* avec les paramètres définis dans le dictionnaire correspondant. Les champs restants ont été définis comme suit :

* **Air patch** : *inletOutlet*, ce qui évite la possibilité que l'eau revienne dans le domaine. Dans le cas où le flux sort, une condition *zeroGradient* est appliquée, et de même, si le flux retourne une valeur égale à celle définie comme *inletValue*.
* **Patch d'entrée** : *fixedValue*, correspondant à une valeur uniforme de 1, ce qui signifie que le patch entier n'est composé que d'eau (pas de phase d'air présente).
* **Patch de sortie et tous les murs restants**: *zeroGradient*. Dans ce cas, les valeurs internes sont extrapolées à la face limite.

```
dimensions      [0 0 0 0 0 0 0];

internalField   uniform 0;

boundaryField
{
  Air
  {
    type            inletOutlet;
    inletValue      uniform 0;
    value           uniform 0;
  }

  Concrete-sides
  {
    type            zeroGradient;
  }

  Gravel-bottom
  {
    type            zeroGradient;
  }

  Inlet
    {
        type            fixedValue;
        value           uniform 1;
    }

  Obstacle
  {
    type            zeroGradient;
  }

    Outlet
  {
    type            zeroGradient;
  }
}
```

