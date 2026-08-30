---
description: Dépannage d'erreurs communes TELEMAC, y compris la récupération de simulation parallèle écrasée, les outils de fusion GRETEL et PARTEL et la reconstruction de fichiers de résultats SELAFIN.
---

# Débogage du TELEMAC

Depuis sa création, TELEMAC est devenu un outil robuste et fiable pour la modélisation numérique des flux de surface. Pourtant, il y a quelques petits défis et cette page toujours croissante fournit quelques réponses.

```{admonition} Keyword-research the TELEMAC docs
:class: tip
Pour consulter la référence, l'implémentation et/ou la signification d'une variable, d'une classe, d'un script, d'un fichier ou d'un module, visitez le [TELEMAC doxydocs (stale - voir opentelemac.org)](https://www.opentelemac.org/index.php/modules/18-news-general/85-doxygen-documentation).
```

## Récupérer les fichiers de simulation écrasés

Lorsqu'un Telemac fonctionne en parallèle (en utilisant plusieurs cœurs) s'écrase, ou si vous avez besoin de recombiner des fichiers de sortie partielle de chaque sous-domaine dans un seul fichier, les outils de post-traitement Telemacs offrent des options pour fusionner (ou « pointer ») les résultats de submesh. Deux outils principaux sont disponibles :

1. **GRETEL (l'outil de fusion dédié)**
   - GRETEL reprend les fichiers de résultats partiels (sous-domaine) de chaque noyau et les fusionne dans un seul fichier SELAFIN/MED pour l'ensemble du domaine.
   - C'est généralement l'approche ** aller-à** si votre simulation s'est écrasée partiellement, mais vous voulez toujours visualiser ou analyser quels résultats partiels ont été enregistrés.

2. **PARTEL (en mode fusion)**
   - PARTEL est généralement utilisé pour la partition des maillages pour les parcours parallèles, mais il a aussi une capacité de fusion. Certaines versions ou workflows utilisent PARTEL pour partitionner et fusionner.
   - Cependant, pour la plupart des configurations Telemac modernes, **GRETEL** tend à être l'outil de fusion plus rationalisé ou par défaut.

### Comment utiliser GRETEL

1. Si vous avez exécuté votre simulation en parallèle et qu'elle s'est écrasée (ou terminée, mais que vous avez juste besoin de combiner des sous-domaines manuellement), localisez les fichiers de résultats partiels appelés quelque chose comme:
   ```
   T3DRES00000-00001.slf
   T3DRES00000-00002.slf
   …
   ```
ou, pour chaque sous-domaine, les fichiers correspondants se terminant généralement par `-0000X.slf`.

2. Vous pouvez les fusionner en exécutant GRETEL depuis la ligne de commande, par exemple :
   ```
   runcode.py gretel -c <your_config> -f <your_config_file> --merge --ncsize <number_of_subdomains>
   ```
   
Réglez les drapeaux et les noms de fichiers au besoin. Si vous utilisez Telemac3d :
   
   ```
   runcode.py telemac3d <steering_file> --merge -w <folder_path>
   ```

Remplacer `<folder_path>` par le répertoire qui contient les parties de sortie.
   

La syntaxe exacte peut varier selon votre version de Telemac. Certaines installations ont un script Python dédié ou un lanceur pour GRETEL.

3. Une fois GRETEL terminé, il produit un fichier ** unique 3D SELAFIN** (ou MED) avec tous les sous-domaines réunis. Vous pouvez alors visualiser ou poursuivre le traitement de ce fichier fusionné dans votre environnement de post-traitement préféré (p. ex. Blue Kenue, Paraview, QGIS).

### Notes et conseils supplémentaires

- **Checkpoint/Hottart**: Si vous avez besoin de redémarrer une course à partir d'une étape de temps donnée, vous pouvez souvent utiliser les fichiers partiels du sous-domaine directement comme un démarrage rapide en définissant les mots-clés appropriés dans le fichier de pilotage (par exemple, `RESTART FILE` / `RESTART = YES`). Dans ce cas, vous n'avez pas nécessairement besoin de fusionner d'abord: Telemac peut lire les fichiers sous-domaines dans un redémarrage parallèle.
- **Écrits partiels**: Si la course s'est écrasée au milieu de l'écriture ou s'il y avait une corruption de fichier, GRETEL (ou PARTEL) pourrait ne pas fusionner. Vous devriez généralement supprimer ou réparer le ou les fichiers corrompus ou redémarrer à partir d'un point de contrôle plus tôt valide.
- **Batch/Automatic Merge**: Dans de nombreux scripts ou workflows de Telemac, la fusion se produit automatiquement à la fin d'une simulation. Si vous avez besoin de la fusion pour se produire même si la simulation s'est écrasée, l'exécution manuelle de GRETEL ou de PARTEL en mode fusion est généralement la meilleure solution.


## Erreurs de traçage

Si une simulation s'écrase et qu'il n'est pas clair pourquoi débogage avec le débogueur *GNU Project* [GDB](http://www.gdbtutorial.com) est une bonne option. Pour ce faire, installez d'abord GDB :

```
sudo apt install gdb
```

Puis lancez le fichier de direction en mode de débogage comme suit:

```
telemac2d.py -w tmp simulation_file.cas --split
telemac2d.py -w tmp simulation_file.cas -x
cd tmp
gdb ./out_telemac2d
```

Dans la touche *gdb* :

```
(gdb) run
```

Pour terminer la touche *gdb* :

```
(gdb) quit
```

Cette approche fonctionne également avec *Telemac3d* (et d'autres modules).

### Corrections rapides du message d'erreur

Cette section énumère les corrections rapides pour certains messages d'erreur fréquents.

CRASH RANDOM
Si TELEMAC s'écrase pour des raisons apparemment aléatoires, assurez-vous que :

  * Aucune ligne du dossier de direction n'a plus de 72 (caractéristiques actives). Par exemple:

  `````{tab-set}
  ````{tab-item} Too long line (bad)
  ```fortran
  CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION = 0.011; 0.011; 0.011; 0.011
  ```
  ````
  ````{tab-item} Correct line break (good)
  ```fortran
  CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION = 0.011; 0.011
  ; 0.011; 0.011
  ```
  ````

## Fichiers de direction (CAS)

* Préférez `:` sur `=`
* Placez tous les fichiers modèles dans le même dossier et ** utilisez uniquement des noms de fichiers** sans les répertoires de fichiers.



## Fichier Mesh

### Meshes à haute résolution
*Cette section est co-écrite par [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*.

Pour créer des maillages très fins avec une taille de grille inférieure à 1,0 m, un fichier de géométrie selafin (`*.slf`) doit être enregistré au format double précision (SERAFIND). Autrement, les bords des limites du modèle peuvent ne pas être bien représentés dans le maillage de calcul. {numref}`Figure %s <mesh-precision>` illustre la perte de précision des limites lorsque l'on utilise une seule précision (a) au lieu de la double précision (b).

```{figure} ../img/telemac/single-double-precision-mesh.png
:alt: telemac slf selafin single double precision serafind
:name: mesh-precision

La précision de la limite de perte dans une maille de sel de précision unique (a) par rapport à une maille de sel de double précision (b).
```


### Contrôle de cohérence du mesh intégré

```{hint}
Une simulation 3d peut s'écraser lorsqu'elle est utilisée avec le paramètre `CHECKING THE MESH : YES`. Ainsi, **in 3d, utiliser favorablement `CHECKING THE MESH : NO`**.
```

Pour vérifier si TELEMAC peut lire le maillage, chargez l'environnement TELEMAC (par exemple, `source pysource.openmpi.sh`) et allez dans le répertoire où le maillage à vérifier vit et lancez `mdump`, par exemple :

```
cd ~/telemac/studies/test-case/
mdump mesh-to-test.med
```

Jusqu'à la rédaction de ce tutoriel, `mdump` demande des variables d'entrée en français*, ce qui signifie :
* *Mode d'affichage de noeuds?* qui signifie <br>English: **Mode d'affichage de node?**
    + Option `1`: Mode entrelacé
    + Option `2`: Mode non entrelacé
* *Connectivité des éléments?* qui signifie <br>English: **Connectabilité d'élément?**
    + Option `1`: Nodal
    + Option `2`: Descending
* *Il y a 1 courrier(s) de type local dans ce fichier. Lequel voulez-vous lire (0 pour tous=1=2=3=3=?* qui signifie <br>English: **Il y a 1 maillage(s) local(s) dans ce fichier. Lequel voulez-vous lire (0 pour tous ou pour tous ?**
    + Option `0`: Tout lire
    + Option `i`: Lisez le numéro de maillage `i`

Une combinaison de réponses standard de `1` - `1` - `0` entraînera une impression de console de tous les nœuds et connexions entre les nœuds dans le maillage, étant donné que TELEMAC peut lire le fichier maillage. En commençant par :

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

**Ce que signifie cette sortie:** Si `mdump` peut lire le maillage, le fichier maillage lui-même est correct et les erreurs de calcul potentielles proviennent d'autres fichiers comme le fichier de direction ou les conditions limites. Sinon, réviser le fichier maillage et résoudre tout problème potentiel.

## Limites

*Cette section est co-écrite par [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*.

### Pas d'eau dans le modèle
Simulations erronées où ** aucune eau n'entre ou ne sort** le domaine a probablement des conditions limites mal définies. Par exemple, considérez les limites ouvertes indiquées à {numref}`Fig. %s <dbg-bc-bk>` avec `prescribed Q (4 5 5)` en amont et `prescribed H (5 4 4)` en aval.

```{figure} ../img/telemac/dbg-bc-bk.png
:alt: debugging boundary conditions cli bluekenue
:name: dbg-bc-bk

Définition des limites ouvertes (liquides) avec `prescribed Q (4 5 5)` en amont et `prescribed H (5 4 4)` en aval.
```

Intuitivement, vous pouvez penser que la limite en amont est le numéro (1) et la limite en aval le numéro (2). Cependant, l'ordre de numérotation des limites dépend de l'ordre de définition lors de la configuration des limites (par exemple, décrit dans le {ref}`BlueKenue pre-processing tutorial <bk-bc>`). Si vous ne vous souvenez pas de l'ordre de définition, il peut être lu dans le fichier limite (`*.cli`) à tout moment. Par exemple, le fichier limite pour le mesh ci-dessus ({numref}`Fig. %s <dbg-bc-bk>`) ressemble à la représentation en {numref}`Fig. %s <dbg-boundaries>` où le **Outlet** est défini **ci-dessus** le **Inlet**. Par conséquent, la limite ouverte ** en aval (sortie) est le numéro (1)** et la limite ouverte ** en amont (entrée) est le numéro (2)** dans cette simulation.

```{figure} ../img/telemac/dbg-boundaries.png
:alt: debugging boundary conditions cli bluekenue
:name: dbg-boundaries

Définition exemplaire d'une limite en aval (Outlet) et d'une limite en amont (Inlet) ouverte dans une limite. cli fichier correspondant à {numref}`Fig. %s <dbg-bc-bk>`.
```

Ainsi, ces deux limites doivent être référencées dans le fichier de direction (`*.cas`) comme suit pour prescrire un débit `Q` (par exemple, 10 m$^3$/s) en amont et une profondeur `H` (par exemple, 0,75 m) en aval :

```fortran
PRESCRIBED FLOWRATES : 0.;10
PRESCRIBED DEPTHS : 0.75;0.
```

### Problème sur le nombre de bornes (Simulation Stop)

Cette section guide les messages d'erreur de débogage tels que:

```fortran
DEBIMP_2D: PROBLEM ON BOUNDARY NUMBER       2
        GIVE A VELOCITY PROFILE
        IN THE BOUNDARY CONDITIONS FILE
        OR CHECK THE WATER DEPTHS
        OTHER POSSIBLE CAUSE:
        SUPERCRITICAL ENTRANCE WITH FREE DEPTH
```

Pour obtenir une meilleure appréciation de la cause de l'erreur (par exemple, pour comprendre si les conditions de flux supercritiques à l'entrée sont la cause), ajouter le {term}`Nombre de Froude <Froude number>` aux variables de sortie dans le fichier de direction (`*.cas`). À cette fin, ajouter `F` au mot clé de la variable de sortie :

```fortran
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F
```

Avec plus de précision de la cause de l'erreur, essayez l'une des options suivantes:

Limites supercritiques à l'entrée
Pour les conditions de débit supercritiques à l'entrée, assurez-vous qu'une limite `prescribed Q and H` obtient également une décharge et une profondeur assignées dans le dossier de direction. Par exemple, si l'inlet dans Figures {numref}`%s <dbg-bc-bk>` et {numref}`%s <dbg-boundaries>` était `5 5 5` (`prescribed Q and H`) au lieu de `4 5 5`, le fichier de pilotage doit prescrire des débits et des profondeurs. Par exemple, ajoutez une profondeur de `0.9` pour l'Inlet comme suit :

  ```fortran
  PRESCRIBED FLOWRATES : 0.;10
  PRESCRIBED DEPTHS : 0.75;0.9
  ```

Modifier le profil de vitesse (vertical)
: La définition d'un mot clé `VELOCITY PROFILE` dans le fichier de pilotage est expliquée dans le {ref}`steady2d tutorial <tm2d-bounds>` dans ce livre électronique. L'ajout `VERTICAL` s'applique uniquement aux modèles 3d (lisez plus dans le {ref}`Telemac 3d (SLF) section <tm3d-slf-boundaries>`).

Modèles 3d avec des limites supercritiques
: Trop de couches verticales peuvent entraîner des éléments de maille 3d très minces qui provoquent localement des flux supercritiques. Ainsi, envisagez de réduire le {ref}`NUMBER OF HORIZONTAL LEVELS <tm3d-slf-vertical>` dans le fichier de direction pour satisfaire l'état {term}`Nombre de Courant <CFL>`.

## Gaia (Morphodynamique)

### CONDITIONS FONDAMENTALES NON RETENUES

TELEMAC-Gaia peut interrompre un message d'erreur comme `KEYWORD:` [...] `UNKNOWN BOUNDARY CONDITIONS FILE ...`. Ce message signifie que le type de condition limite dans le fichier `*.cli` ne correspond pas aux conditions limites définies dans le fichier `*.cas`. Par exemple, si la colonne limite du traceur (charge en suspension) (`9` dans le fichier Gaia `*.cli` pour `CBOR`) est définie à `5`, essayez d'utiliser `EQUILIBRIUM INFLOW CONCENTRATION : YES` ou double-vérifiez les nombres définis pour le mot-clé **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALEURS**.

En savoir plus sur la configuration des fichiers de conditions limites pour Gaia dans le {ref}`Gaia Basics section <gaia-bc>`. La définition des types de limites dans le fichier de direction Gaia est décrite séparément pour {ref}`bedload <gaia-bc-bl>` et {ref}`suspended load <gaia-bc-sl>`.

## BlueKenue

*Cette section est co-écrite par [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*.

BlueKenue peut lancer des erreurs ou ne pas afficher correctement lorsque vous travaillez avec des mailles 3d. Certains des problèmes peuvent être résolus en utilisant la dernière version de BlueKenue (v3.12.2-alpha au moment de la rédaction de cet article).

**OnFileOpendata(): ERROR: sur Activer()**
: ** Causes :** Le message d'erreur se produit généralement avec des modèles parallélisés lorsque Telemac3d / PARTEL n'a pas correctement fusionné le maillage à la fin de la simulation.

**Solution:** Force TELEMAC à ne pas supprimer le dossier de simulation temporaire (un dossier qui est visible dans le répertoire de simulation par défaut seulement pendant qu'une simulation est en cours). Conserver le répertoire de calcul temporaire est réalisé en ajoutant un drapeau `-t` à la fin de la commande de simulation. Par exemple, tapez sur ce qui suit pour conserver le dossier de simulation pour une simulation Telemac3d (lisez davantage à l'annexe A du [Manuel Telemac3d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf)):

  ```
  telemac3d.py steering-file.cas -t
  ```
  
Le dossier temporaire contient des fichiers T3DRES (mesh partition) qui peuvent être fusionnés puis ouverts dans BlueKenue. Pour fusionner les fichiers T3DRES, exécutez la commande suivante (assurez-vous que l'environnement TELEMAC est toujours activé avec `source pysource.YOUR-ENV.sh`):
  
  ```
  runcode.py --merge -w temp_directory/ telemac3d file.cas
  ```
  
Pour obtenir de l'aide pour exécuter cette commande, lisez [cette entrée de forum TELEMAC](http://opentelemac.co.uk/index.php/assistance/forum5/21-telemac-3d/7221-continue-computation-from-temporary-file).
  
Pour **mises à jour sur ce message**, suivez le thread [BlueKenue dans le forum TELEMAC](http://www.openmascaret.org/index.php/assistance/forum5/blue-kenue/13278-issue-with-geometry-file?start=10#38837) pour le dépannage des mises à jour sur cette erreur.

## Plugin PostTelemac

Certaines versions de QGIS peuvent lancer une erreur Python (cadre jaune dans la région supérieure de la vue de carte) et un clic sur **Stack** révèle un message d'erreur. Au bas du message d'erreur, il pourrait être écrit `import error: no module named gdal`. L'erreur provient probablement d'une déclaration d'importation dans l'un des scripts Python du plugin PostTelemac. Pour résoudre l'erreur d'importation de gdal, trouvez le script Python qui soulève le message d'erreur. Par exemple, le script `posttelemac_hdf_parser.py` peut causer l'erreur par son énoncé `import gdal`. Pour dépanner, ouvrir et sous Windows, vous pouvez le trouver dans le répertoire suivant:

```
C:\Users\USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\PostTelemac\meshlayerparsers\posttelemac_hdf_parser.py
```

Dans le fichier ouvert :

* Ouvrir le fichier concerné, qui est ici : **`posttelemac_hdf_parser.py`**
* Find the `import gdal` statement and **replace it with `from osgeo import gdal` (i.e.,  <s>`import gdal`</s> and write `from osgeo import gdal`)
* Enregistrer et fermer le fichier Python.

Essayez de démarrer le plugin PostTelemac. Il devrait fonctionner sans problèmes maintenant.


## SALOME-HYDRO

(salome-dbg)=
### SALOME-HYDRO ne commence pas (**Kernel/Session**)

Si un message d'erreur est soulevé par `Kernel/Session` dans le `Naming Service`, il finit généralement par
```
$ [Errno 3] No such process ... 
   RuntimeError: Process NUMBER for Kernel/Session not found
```

Il y a plusieurs origines possibles de telles erreurs qui s'enracinent partiellement dans les versions de bibliothèque potentiellement codées en dur de l'installateur. Les options de dépannage suivantes existent, mais celles-ci nécessitent un examen attentif car elles pourraient nuire au système d'exploitation:

* Créez manuellement des copies de bibliothèques plus récentes avec les noms des anciennes versions. Par exemple,
  + Dans la 4ème ligne après avoir lancé `./salome`, `Kernel/Session` peut inviter

```
$ error while loading [...] libSOMETHING.so.20 cannot open [...] No such file or directory
```

  + Identifiez la version installée avec `whereis libSOMETHING.so.20` (remplacez `libSOMETHING.so.20` avec la bibliothèque manquante); par exemple, cette commande peut sortir

```
$ /usr/lib/x86_64-linux-gnu/libSOMETHING.so.40
```

  + Créez une copie de la bibliothèque plus récente et renommez la copie selon les besoins de SALOME; par exemple, appuyez sur

```
sudo cp /usr/lib/x86_64-linux-gnu/libSOMETHING.so.40 usr/lib/x86_64-linux-gnu/libSOMETHING.so.20
```

  + Très probablement, les fichiers suivants doivent être copiés:

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

* Remplacer la version interne de *Qt* de SALOME-HYDRO :
  + Copier

```
/usr/lib/x86_64-linux-gnu/libQtCore.so.5
```
  + Coller (confirmer en remplaçant `libQtCore.so.5`)

```
/Salome-V2_2/prerequisites/Qt-591/lib/
``` 


(qt-dbg)=
### Support GUI/Qt5 (compatibilité avec la version GTK)

Avec les versions les plus récentes de la plateforme *Qt*, toute entrée de menu dans *SALOME-HYDRO* ne s'affichera pas. Pour résoudre ce problème, installez et configurez `qt5ct` styles:


```
sudo apt install qt5-style-plugins libnlopt0 qt5ct
```

Puis :

* Configurez `qt5ct` (appuyez sur `qt5ct` dans *Terminal*)
  + Aller à l'onglet *Apparence*
  + Définir *Style* à `gtk2` et * boîte de dialogue standard* à `GTK2`
  + Cliquez sur *Appliquer* et *OK*
* Ouvrez le fichier `~/.profile` (par exemple, utilisez le navigateur du fichier, allez dans le dossier `Home` et appuyez sur `CTRL` + `H` pour basculer en regardant les fichiers cachés) et ajoutez au bas du fichier :

```
export QT_STYLE_OVERRIDE=gtk2
export QT_QPA_PLATFORMTHEME=qt5ct
```

* Enregistrer et fermer `.profile` et redémarrer (ou simplement re-login).

```{note}
If a file called `~/.bash_profile` (or `~/.bash_login`) exists, the above lines should be written to this `~/.bash_profile`/`~/.bash_login` because in this case, `.profile` will not be read when logging in.
```

En savoir plus sur *Qt* à [archlinux.org](https://bbs.archlinux.org/viewtopic.php?id=214147&p=3) et dans [arch wiki](https://wiki.archlinux.org/index.php/Uniform_look_for_Qt_and_GTK_applications#QGtkStyle).
