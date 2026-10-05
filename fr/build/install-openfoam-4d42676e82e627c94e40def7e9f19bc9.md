---
description: Installation d'OpenCFD OpenFOAM v2406, résolveurs de sédiments Olsen, conditions de sortie BAW, ParaView et VisIt sur Debian, Ubuntu et Windows via WSL2.
---

(openfoam-install)=
# OpenFOAM (installation)

Cette section explique l'installation de [OpenCFD OpenFOAM v2406](https://dl.openfoam.com/source/v2406/) avec un script d'installateur automatique multiplateforme qui compile le programme aux côtés des composants de transport des sédiments et de la limite de sortie ainsi que ParaView et VisIt-DAV pour post-traitement.

| Component | Function |
| :--- | :--- |
| `sediDriftFoam` | Olsen et al. (2023) fixed-mesh suspended-sediment solver. |
| `sediDriftFoam2` | Olsen (2025) sediment solver with bed-elevation and free-surface adjustment. |
| `sediDriftFoam2Rating` | New experimental extension of `sediDriftFoam2` for a stage–discharge relation. |
| BAW `HydBCsForOF` | Boundary-condition library, including a stage–discharge outlet for water–air simulations with `interFoam`. |

Les résolveurs originaux sont documentés par [Nils Reidar Olsen](https://www.pvv.ntnu.no/~nilsol/sediDriftFoam2/); la condition limite de sortie native est documentée dans [BAW's depositary](https://github.com/baw-de/HydBCsForOF).

```{admonition} OpenFOAM Distribution
:class: important

Ces instructions ciblent la version d'OpenCFD v2406, et non les versions d'OpenFOAM Foundation (p. ex. v9 ou v13). L'installation par défaut compile la version source de juin 2024 et correspond à des sources tiers dans un répertoire utilisateur séparé. Les installations OpenFOAM existantes et les fichiers de démarrage shell sont conservés. Ne combinez pas les bibliothèques compilées sur différentes distributions ou versions OpenFOAM.
```

## Exigences et fichiers d'installation

L'installateur prend en charge les systèmes x86-64 fonctionnant sous Debian 12, Ubuntu 22.04 ou Ubuntu 24.04. Les dérivés doivent utiliser une distribution de base supportée correspondante. Windows construit fonctionner dans Windows Subsystem pour Linux 2 (WSL2), pas comme des exécutables Windows natifs.

L'installation nécessite une bonne et stable connexion Internet, Python 3.10 ou ultérieure, et un compte utilisateur avec `sudo` accès pour les paquets système. Permettre environ 20 GiB d'espace disque libre et au moins 8 GiB de RAM; la vérification de la construction source nécessite au moins 15 GiB sans. La compilation peut prendre plusieurs heures. Le post-traitement graphique nécessite un bureau Linux ou WSLg.

L'installateur est maintenu dans le [`OpenFOAM-installer` subfolder](https://github.com/Ecohydraulics/numerical-software-installers/tree/main/OpenFOAM-installer) du dépôt `Ecohydraulics/numerical-software-installers`. Avec Git installé, clonez le dépôt et entrez ce sous-dossier:

```bash
git clone --depth 1 https://github.com/Ecohydraulics/numerical-software-installers.git
cd numerical-software-installers/OpenFOAM-installer
```

Ces commandes fonctionnent également dans PowerShell. Pour une commande existante, entrez son répertoire `OpenFOAM-installer` au lieu de clonage à nouveau. Sinon, utilisez **Code → Télécharger ZIP** sur la [page de dépôt](https://github.com/Ecohydraulics/numerical-software-installers), extraire les archives, et entrer `numerical-software-installers-main/OpenFOAM-installer`.

Conserver le sous-dossier d'installation complet; `install.py` seul est insuffisant. Le dépôt contient des fichiers d'installation, et non les distributions logicielles, qui sont téléchargés pendant l'installation. Exécutez les commandes ci-dessous de `OpenFOAM-installer`, qui contient `install.py` et `install.ps1`.

(openfoam-debian)=
## Debian et Ubuntu

### Compiler et installer

Si Python est absent, installez-le d'abord :

```bash
sudo apt update
sudo apt install python3
```

Prévisualiser l'installation, puis compiler et installer:

```bash
python3 install.py --dry-run
python3 install.py --install-system-packages --examples --smoke-test
```

Exécutez l'installateur en tant qu'utilisateur normal, sans le préfixer avec `sudo`. L'option `--install-system-packages` autorise l'installation de dépendances de construction, de dépendances d'exécution graphique et de ParaView par `sudo apt-get`. Visit-DAV 3.5.0 est téléchargé sous la forme d'un binaire vérifié par checksum correspondant au système d'exploitation. ParaView suit la version disponible depuis les dépôts de distribution configurés.

```{admonition} APT Commands
:class: note

L'installateur utilise `apt-get`, l'interface rétrocompatible recommandée pour les scripts. Les commandes `apt` ci-dessus sont destinées à une utilisation interactive. Aucune des deux interfaces n'est obsolète; voir le manuel [Debian APT manual](https://manpages.debian.org/bookworm/apt/apt.8.en.html#SCRIPT_USAGE_AND_DIFFERENCES_FROM_OTHER_APT_TOOLS).
```

L'option `--examples` télécharge le cas grossier A de Nils Reidar Olsen. L'option `--smoke-test` exécute une courte série `interFoam` pour vérifier la bibliothèque BAW. Un essai à sec imprime le plan sans vérifier les prérequis ni compiler le code.

```{admonition} Distribution Derivatives
:class: note

Si un dérivé n'est pas reconnu, vérifiez sa base Debian ou Ubuntu avant de sélectionner `--visit-platform debian12`, `--visit-platform ubuntu22` ou `--visit-platform ubuntu24`. La redéfinition sélectionne le binaire VisIt ; elle n'établit pas de compatibilité avec un système d'exploitation non supporté.
```

### Réutiliser une installation OpenCFD v2406 existante

Au lieu de compiler le noyau OpenFOAM, spécifiez le fichier d'activation v2406 existant. Pour l'installation du paquet Debian à `/usr/lib/openfoam/openfoam2406`, utilisez :

```bash
python3 install.py --install-system-packages \
  --reuse-openfoam /usr/lib/openfoam/openfoam2406/etc/bashrc \
  --examples --smoke-test
```

C'est une alternative à la commande source-build précédente. Les résolveurs de sédiments et la bibliothèque BAW sont encore compilés dans le nouveau répertoire utilisateur. L'installation existante doit inclure des en-têtes de développement, `wmake`, et un compilateur de travail. Son API doit être 2406; son niveau de patch peut différer de la version source par défaut.

## Windows via WSL2

Dans un administrateur PowerShell, installer Ubuntu 24.04 pour WSL:

```powershell
wsl --install -d Ubuntu-24.04
```

Redémarrer Windows si demandé. Lancez Ubuntu une fois et créez un compte utilisateur Linux normal. Confirmer que la distribution utilise WSL2:

```powershell
wsl --list --verbose
```

Si sa version est 1, exécutez `wsl --set-version Ubuntu-24.04 2`. WSLg prend en charge les applications graphiques sur Windows 11 et Windows 10 construire 19044 ou plus tard; voir les [exigences d'installation Microsoft](https://learn.microsoft.com/windows/wsl/tutorials/gui-apps).

À partir du répertoire `OpenFOAM-installer` du dépôt, utilisez un PowerShell ordinaire :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -InstallSystemPackages -Examples -SmokeTest
```

Le lanceur invoque le même installateur Python dans WSL2. Les fichiers d'installation peuvent rester sur le système de fichiers Windows, mais la compilation et les cas doivent résider sur le système de fichiers Linux, pas sous `/mnt/c`. ParaView et VisIt fonctionnent comme des applications Linux affichées par WSLg.

Pour une distribution initiale WSL nommée `Debian` qui fonctionne Debian 12, ajouter `-Distro Debian`. Vérifiez sa version avant l'installation; une distribution Debian nouvellement téléchargée n'a pas besoin d'être Debian 12. Pour réutiliser OpenCFD v2406, ajoutez `-ReuseOpenfoam` suivi de son chemin Linux `etc/bashrc`.

## Répertoire d'installation et vérification

Le répertoire d'installation par défaut est `~/.local/openfoam-sediment-v2406` dans le répertoire d'origine de l'utilisateur Linux. Spécifiez un autre chemin Linux dédié avec `--prefix /home/USER/path` ou Windows `-Prefix /home/USER/path`; le chemin ne doit pas contenir d'espace blanc. Limiter la concordance de compilation avec `--jobs 4` ou `-Jobs 4`, si nécessaire. La valeur par défaut n'est pas plus de huit processus de compilation, réduits selon le système RAM.

Dans un terminal Linux ou WSL, entrez l'environnement installé :

```bash
source ~/.local/openfoam-sediment-v2406/activate.sh
```

Cette commande ouvre un nouveau shell interactif isolé. Il ne modifie pas `.bashrc` ou fusionne un environnement OpenFOAM antérieur. Seules les préférences OpenFOAM au niveau du projet sont chargées; les préférences utilisateur/groupe existantes sont exclues. Saisissez `exit` pour revenir au shell précédent. Pour un répertoire d'installation personnalisé, utilisez plutôt son `activate.sh`.

Vérifiez l'installation dans ce nouveau shell:

```bash
foamEtcFile -show-api
foamEtcFile -show-patch
printf '%s\n' "$WM_PROJECT_DIR" "$WM_OPTIONS"
command -v sediDriftFoam sediDriftFoam2 sediDriftFoam2Rating
sediDriftFoam -help
sediDriftFoam2 -help
sediDriftFoam2Rating -help
```

La sortie API doit être `2406`. L'aide au solvant doit se charger sans erreur de bibliothèque manquante. Le répertoire d'installation contient les registres de compilation et `environment-probe.log` à `logs/`, les détails de construction à `build-environment.txt` et les enregistrements de source et d'installation à `receipt.json`. La sortie BAW runtime-test est stockée à `runs/baw-smoke/`.

```{admonition} Scope of Verification
:class: warning

La compilation réussie et l'essai BAW n'établissent ni la validité d'une simulation de sédiments ni la précision de l'extension expérimentale de la courbe de notation. L'installateur n'exécute pas le Case A d'Olsen. Avant utilisation scientifique, vérifier la qualité du maillage, la conservation, les conditions de limite hydraulique et l'accord avec les résultats de référence appropriés. Conserver les enregistrements de construction avec les entrées de simulation.
```

Si l'installation échoue, inspecter `logs/` avant de recommencer. Les builds interrompus conservent les téléchargements et les journaux. Ne supprimez pas une installation OpenFOAM existante pour résoudre un conflit de version. Lors de la modification des pins sources, du code d'installation ou de l'environnement du compilateur, sélectionnez un nouveau répertoire d'installation plutôt que de mélanger des binaires anciens et nouveaux.

```{admonition} Archive Verification
:class: warning

Une inadéquation de checksum indique que les octets reçus ne correspondent pas à l'archive épinglée; elle n'établit pas en soi que la version a changé. Le téléchargeur rejette les réponses partielles et HTML et signale les valeurs SHA256 attendues et reçues, le nombre d'octets, le type de contenu et le chemin miroir. Conserver la sortie d'erreur complète si la vérification échoue. Ne modifiez pas la somme de contrôle ou ne désactivez pas la vérification. Les téléchargements temporaires rejetés sont supprimés; les archives vérifiées sont conservées.
```

Si le répertoire d'installation ou son journal est inopinément absent, localisez le répertoire avant de le reconstruire. Un arbre trouvé dans la corbeille de bureau doit être restauré sur son chemin original enregistré, sans construction active et sans destination existante écrasée. Trouver l'arbre dans la corbeille n'établit pas quand ni pourquoi il a bougé. Les instructions de récupération fournies décrivent l'inspection et la restauration du journal; ne pas compiler dans la corbeille.

````{admonition} Recovery from a Failed Installation
:class: note

Les installateurs précédents ont rejeté le nom de fichier Linux valide `jouleHeatingSource:V` ou ont échoué pendant le chargement de l'environnement avec `/bin/bash: cannot execute binary file` ou `pop_var_context`. La chargeuse corrigée isole les arguments de commande et suspend les modes shell stricts pendant l'initialisation OpenFOAM, puis vérifie le projet sélectionné, API et ABI avant la compilation. Préserver le répertoire échoué et sélectionner un nouveau préfixe d'installation; ne pas contourner son marqueur de propriété. Réessayer sans avoir besoin d'un cache précédent :

```bash
python3 install.py --install-system-packages \
  --prefix "$HOME/.local/openfoam-sediment-v2406-initfix" \
  --examples --smoke-test
```

L'installateur télécharge et vérifie les archives dans le nouveau préfixe. La réutilisation des caches est facultative : utilisez `--source-cache` uniquement avec un répertoire existant vérifié. Une erreur `Archive cache directory not found` précède les changements au préfixe cible ou aux paquets système; omettez cette option et essayez à nouveau avec le même préfixe. Sur Windows, utilisez `-Prefix` avec un chemin Linux. Après le succès, activez le nouveau préfixe `activate.sh`. Déplacement d'une installation utilisateur n'inverse pas les modifications du paquet APT. Le [recovery instructions](https://github.com/Ecohydraulics/numerical-software-installers/blob/main/OpenFOAM-installer/docs/RECOVERY.md) décrit le retour récupérable et l'examen des transactions-paquets.
````

## Cas de sédiments et sorties étape-décharge

Avec `--examples`, les fichiers d'entrée d'Olsen sont stockés à `cases/olsen-upstream/cylinder9_case_A/` dans le répertoire d'installation. Travaillez sur une copie en écriture. Inspecter le maillage avant d'exécuter le résolveur sélectionné:

```bash
cd /path/to/case-copy
checkMesh -constant -allTopology -allGeometry
```

Résoudre les erreurs de maillage avant la simulation. Pour le cas A fourni, invoquer `sediDriftFoam2` explicitement à partir du répertoire des cas; le nom `controlDict` publié peut toujours être `simpleFoam`. La méthode fixe `sediDriftFoam` nécessite un cas compatible préparé séparément parce que ses entrées sédimentaires sont différentes. Exécutez les résolveurs Olsen en série. Les algorithmes de mailles et de sorties mobiles ne conviennent pas à la décomposition des MPI. `sediDriftFoam2` et `sediDriftFoam2Rating` écraser `scour.txt` lors du lancement; l'archiver avant de redémarrer.

### Sortie BAW pour interFoam

The installer prepares `cases/baw-interFoam/` and compiles the shared library `lib_BAW_public_BCs_v2412_20260813.so` against the selected v2406 installation. The `v2412` text is part of the upstream filename, not the build's OpenFOAM version. This library is loaded by the case through the `libs` entry in `system/controlDict`; it does not require recompiling `interFoam`.

Pour une courbe de notation propre au site, configurer les entrées de sortie appariées `waterLevel_alpha_prgh` `p_rgh` et `alpha.water`, en utilisant le mode `ratingCurveTable` décrit dans la documentation de BAW](https://github.com/baw-de/HydBCsForOF). Utiliser le boîtier préparé comme exemple de configuration, et non comme données hydrauliques étalonnées.

### Sortie expérimentale pour le résolveur à lit mobile d'Olsen

Dans une copie jetable, placer le fichier `examples/ratingCurveProperties` à `constant/ratingCurveProperties`. Remplacer le tableau illustratif par un débit extérieur spécifique au site en m3/s et une élévation de la surface de l'eau en m, exprimée dans le repère vertical du maillage. Les valeurs de décharge doivent augmenter strictement, et les élévations ne doivent pas diminuer. Réglez `outletPatch` à la sortie réelle, vérifiez les limites de profondeur et d'altitude et changez `enabled false` à `enabled true`. Exécutez `sediDriftFoam2Rating` explicitement. Sans cette configuration, l'extension est inactive.

```{admonition} Distinct Boundary-Condition Formulations
:class: warning

L'état natif de BAW utilise les champs eau-air `alpha.water` et la pression hydrostatique réduite `p_rgh` à Pa. Elle ne peut pas être attribuée directement à la pression cinématique monophasée d'Olsen `p` en m2/s2. L'extension d'évaluation distincte ajuste la surface libre géométrique dans un calcul en série quasi stable; il ne s'agit pas d'une formulation Lagrangien-Eulérienne arbitraire validée transitoire ou conservatrice. Il conserve l'hexaédral d'Olsen, c'est-à-dire les restrictions de maillage ordonnées verticalement. Le mesh fixe `sediDriftFoam` n'a pas de surface libre mobile.
```

Complétez les tests dans les instructions de validation de la courbe de notation](https://github.com/Ecohydraulics/numerical-software-installers/blob/main/OpenFOAM-installer/docs/RATING_CURVE.md) avant d'utiliser l'extension pour la recherche ou la conception.

## Services publics (pré- et post-processeurs)

### ParaView

Activez l'environnement installé, puis ouvrez le boîtier de simulation avec le lecteur OpenFOAM intégré de ParaView :

```bash
cd /path/to/case-copy
touch case.foam
paraview case.foam
```

Sélectionnez `internalMesh` et les correctifs de limites pertinents, y compris `bedWall` et `freeSurface` où présents. Activer `Conc`, `U` et `p`, puis sélectionner **Appliquer**. Choisissez le champ affiché et utilisez les commandes d'animation pour inspecter les séries chronologiques. Pour les cas d'eau-air BAW, inspecter `alpha.water` et `p_rgh`. Aucun plugin de ParaView lié à OpenFOAM n'est requis; voir la [Documentation du lecteur OpenFOAM](https://www.paraview.org/paraview-docs/v5.12.0/python/paraview.simple.OpenFOAMReader.html).

### Visit-DAV

Exporter le cas vers VTK et générer des manifestes de séries chronologiques dans le shell activé:

```bash
python3 ~/.local/openfoam-sediment-v2406/postprocess.py /path/to/case-copy
visit
```

Pour un répertoire d'installation personnalisé, ajustez le chemin de script. Dans VisIt, ouvrez l'un des fichiers imprimés `.visit`, ajoutez un emplacement **Pseudocolor** de `Conc` ou un autre scalar disponible, sélectionnez **Draw**, et utilisez les contrôles d'animation. Le volume ouvert, le lit et la surface libre se manifestent séparément. L'exportateur conserve les coordonnées de mailles dépendantes du temps et enregistre les valeurs de temps OpenFOAM à partir des métadonnées plutôt que de déduire le temps à partir des noms de fichiers; voir la [VisIt file-series documentation](https://visit-sphinx-github-user-manual.readthedocs.io/en/v3.5.0/using_visit/WorkingWithFiles/Supported_File_Types.html#creating-visit-files).

Conserver tous les fichiers de timestep exportés. Les valeurs de temps OpenFOAM n'ont pas besoin d'égaler le temps morphodynamique accéléré enregistré par le solveur d'Olsen. Reconstruire parallèle `interFoam` champs et mesh avant l'exportation série. Pour régénérer les manifestes après des pas de temps supplémentaires, déplacer plus tôt `.visit` fichiers mis de côté; différents manifestes existants ne sont pas écrasés.

```{admonition} Remote or Headless Computers
:class: note

Sur un serveur sans bureau graphique, transférer le boîtier ou son exportation VTK vers un poste de travail de visualisation. Les options `--skip-visualization` et Windows `-SkipVisualization` omettre les deux téléspectateurs lorsqu'une installation de construction seulement est nécessaire. Utilisez les lanceurs `paraview` et `visit` de l'installateur pour éviter les conflits entre les bibliothèques OpenFOAM et les bibliothèques de visualisation.
```

### SALOME

SALOME n'est pas installé par ce script. Son installation est décrite dans les instructions TELEMAC: {ref}`salome-install`.

(freecad-install)=
### FreeCAD

FreeCAD n'est pas installé par ce script. Les paquets Windows, Linux et macOS et les instructions d'installation sont disponibles dans le [Projet FreeCAD](https://www.freecad.org/).
