---
title: "Compilation Native de Delft3D-FLOW sur Ubuntu et Linux Mint"
subtitle: "Une note d'utilisation du livre Jupyter pour `install-delft3d-flow-native.sh`"
author: "Prepared for hydraulic-engineering computational workflows"
date: "2026-07-02"
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: "0.13"
    jupytext_version: "1.16"
kernelspec:
  display_name: Bash
  language: bash
  name: bash
---

# Delft3D-FLOW

Cette section décrit une procédure d'installation native pour la compilation du noyau hydrodynamique Delft3D 4 sur les systèmes basés sur Ubuntu et Linux Mint sans utiliser Docker. La procédure est implémentée dans le script shell `install-delft3d-flow-native.sh`. Le script clone le dépôt source Deltares Delft3D, installe un environnement de construction Python/Conan local, installe et configure des compilateurs Intel oneAPI, initialise le workflow de dépendance Conan open-source, construit la suite Delft3D 4 ou la cible `flow2d3d`, copie l'arborescence d'installation résultante à un préfixe défini par l'utilisateur, et exécute un test de fumée avec l'exemple standard Delft3D 4. La procédure doit être considérée comme une construction expérimentale d'hôte parce que la procédure documentée de construction Linux pour Delft3D est basée sur un conteneur. L'utilisation prévue est l'expérimentation locale reproductible, l'inspection de code, et l'exécution en ligne de commande de cas d'essai Delft3D-FLOW sur des postes de travail d'ingénierie non conteneurisés.

```{warning}
Ce document décrit une tentative de construction native. Il ne remplace pas le guide officiel de construction Linux de Deltares. Deltares documente la compilation Linux principalement à travers des environnements conteneurisés, alors que ce script tente de reproduire la chaîne d'outils requise directement sur un hôte basé sur Ubuntu ou Linux Mint. Examinez le script avant de l'exécuter : il ajoute le dépôt APT Intel oneAPI, installe les paquets système avec `sudo`, télécharge et compile le code source tiers, et écrit les fichiers ci-dessous `$HOME`. Utilisez-le à vos risques et périls et ne l'utilisez pas sur des systèmes de production, partagés ou institutionnels sans autorisation et sauvegardes.
```

## Se préparer

Le dépôt Delft3D contient du code source pour Delft3D 4 et Delft3D FM. Delft3D-FLOW fait partie de la suite Delft3D 4 dont la configuration de construction est `d3d4-suite`. Dans cette suite, les principaux binaires Delft3D-FLOW sont `d_hydro` et `flow2d3d`. Le système de construction expose également `flow2d3d` comme configuration individuelle; cependant, la configuration de niveau suite est la cible plus conservatrice pour une première installation car il préserve le contexte d'exécution Delft3D 4.

Le script est destiné aux conditions de fonctionnement suivantes:

- l'utilisateur doit exécuter Delft3D-FLOW en ligne de commande sur Linux;
- Docker ou un autre conteneur est indésirable;
- le temps de compilation local (environ une à plusieurs heures) et l'utilisation du disque (environ 25 Go pour un API, sources et arbres de construction) sont acceptables;
- l'hôte est un système dérivé Ubuntu ou Linux Mint avec `apt`;
- Les compilateurs Intel oneAPI peuvent être installés sous `/opt/intel/oneapi`;
- l'utilisateur accepte que la procédure est en dehors de la principale voie Linux testée décrite par Deltares.

La procédure n'est pas destinée à installer ou exécuter l'interface utilisateur graphique de Windows Delft3D. Il installe les noyaux en ligne de commande et les fichiers d'exécution seulement.

To continue, [download the installer script `install-delft3d-flow-native.sh`](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/delft3d-installer/install-delft3d-flow-native.sh).

## Provenance de la procédure

Le script suit la séquence de construction au niveau du dépôt utilisée par les outils d'aide de Deltares. Les dépendances de tiers sont gérées avec Conan 2, tandis que `run_conan.py` effectue une configuration unique de Conan et `build.py` drives installation de dépendance, CMake configuration, compilation et installation. Pour les utilisateurs externes sans accès au serveur de paquets Deltares Nexus, le mode d'initialisation pertinent est :

```bash
python run_conan.py initialize external
```

La première compilation correspondante compile localement toutes les dépendances de tiers :

```bash
python build.py --config d3d4-suite --build --build-type Release --build-dependencies
```

Le script natif automatise ces opérations et ajoute les étapes de préparation au niveau de l'hôte qui seraient normalement fournies par le conteneur de construction Deltares:

- Il installe la chaîne d'outils Intel oneAPI épinglée aux versions utilisées par le conteneur Deltares et le profil Conan : compilateurs C/C++ et Fortran 2024.2, Intel MPI 2021.13 et MKL 2024.2. Si ces paquets épinglés disparaissent du dépôt Intel, le script revient aux dernières versions et corrige la configuration de Conan pour accepter la version du compilateur détecté.
- Il crée un environnement virtuel Python à l'intérieur de l'arborescence source avec `conan ~= 2.29` et un CMake courant, parce que la construction Delft3D nécessite CMake 3.30 ou plus récent, que Ubuntu 24.04 et Linux Mint 22 ne expédient pas.
- Il exporte l'environnement compilateur utilisé à l'intérieur du conteneur Deltares (`CC=mpiicx`, `CXX=mpicxx`, `FC=mpiifx`) afin que CMake configure Delft3D elle-même avec la même chaîne d'outils que les dépendances Conan.

```{important}
Le script maintient délibérément le profil de Deltares Conan proche de sa forme amont et corrige uniquement les chemins de compilateur Intel locaux et, si nécessaire, la version compilateur. Le profil Linux en amont est nommé pour un environnement AlmaLinux 8 et Intel oneAPI 2024. Changer l'identité de distribution dans le profil peut modifier l'identité du paquet Conan et réduire la reproductibilité.
```

## Installation

### Placement du fichier

Placez le script dans un répertoire de travail où l'exécution du shell est autorisée. La disposition suivante est recommandée:

```bash
mkdir -p "$HOME/src/delft3d-native-installer"
cd "$HOME/src/delft3d-native-installer"

# copy or move the script here
ls -l install-delft3d-flow-native.sh
```

Rendre l'exécutable du script :

```bash
chmod +x install-delft3d-flow-native.sh
```

### Installation par défaut

L'invocation par défaut construit la suite Delft3D 4 en mode de sortie, copie l'arborescence d'installation résultante à `$HOME/opt/delft3d-flow`, et exécute l'exemple standard comme un test de fumée:

```bash
./install-delft3d-flow-native.sh
```

Le script demande le mot de passe `sudo` lorsqu'il installe les paquets système. Les valeurs par défaut sont résumées dans {numref}`default-options`.

```{list-table} Default script options
:name: default-options
:header-rows: 1

* - Option
  - Par défaut
  - Fonction
* - `--src-dir`
  - `$HOME/src/delft3d`
  - Emplacement du dépôt source Delft3D cloné.
* - `--prefix`
  - `$HOME/opt/delft3d-flow`
  - Destination finale d'installation/de copie.
* - `--config`
  - `d3d4-suite`
  - Delft3D 4 suites, y compris Delft3D-FLOW.
* - `--build-type`
  - `Release`
  - Type de construction de CMake optimisé.
* - `--jobs`
  - `nproc`
  - Niveau de construction parallèle (`CMAKE_BUILD_PARALLEL_LEVEL` et `MAKEFLAGS`).
* - `--tag`
  - non défini
  - Utilise la branche par défaut à moins qu'une branche, une balise ou un commit ne soit spécifié.
* - `--no-test`
  - non défini
  - Passez le test de fumée avec l'exemple standard.
```

### Installation reproductible

Pour les études d'ingénierie hydraulique, la révision de la source doit être fixée. Une pointe de branche n'est pas une dépendance reproductible du modèle. Utilisez une balise de libération ou commit hash si possible.

```bash
./install-delft3d-flow-native.sh \
  --tag <Delft3D-tag-or-commit> \
  --config d3d4-suite \
  --build-type Release \
  --prefix "$HOME/opt/delft3d-flow"
```

```{note}
Remplacer `<Delft3D-tag-or-commit>` par une balise ou un commit sélectionné à partir du dépôt Deltares. Le script ne prescrit pas de version spécifique car la révision appropriée dépend de l'archive modèle de l'utilisateur, du cas de validation ou des exigences du projet.
```

### Construction minimale orientée FLOW

Si l'objectif est seulement d'évaluer la cible `flow2d3d` build, le script peut être invoqué comme suit:

```bash
./install-delft3d-flow-native.sh --config flow2d3d
```

Pour les premiers utilisateurs, `d3d4-suite` reste l'essai préféré car c'est la cible de niveau suite associée à Delft3D 4. La cible plus petite `flow2d3d` est plus appropriée après que la chaîne d'outils hôte ait déjà été montrée pour fonctionner.

### Installation du paquet de saut

Sur les postes de travail gérés de l'université ou de l'institut, l'utilisateur peut ne pas vouloir que le script modifie les paquets système. Deux modes réduits sont prévus.

Passez seulement à l'étape d'installation Intel oneAPI :

```bash
./install-delft3d-flow-native.sh --skip-oneapi-install
```

Passer tout `apt` activité:

```bash
./install-delft3d-flow-native.sh --no-apt
```

Ces modes supposent que les compilateurs requis et les outils de construction sont déjà installés. En particulier, les commandes suivantes doivent être résolues après une initialisation API :

```bash
source /opt/intel/oneapi/setvars.sh --force
which icx icpx ifx mpiicx mpiifx mpicxx
```

Si la version préinstallée de OneAPI diffère de 2024.2, le script corrige automatiquement le profil de Conan et les versions du compilateur autorisées, mais une telle déviation déplace la construction plus loin de la base de Deltares.

```{warning}
Une invocation réduite n'est pas une solution portable en soi. Il empêche simplement les actions de gestion de paquets. Si `git`, Python, les compilateurs Intel C/C++ et Fortran, ou les enveloppes Intel MPI sont absentes ou non découvrables, la construction échouera à la vérification de diagnostic correspondante.
```

## Lancement et essai Delft3D-FLOW

### Environnement d'exécution

Après une construction réussie, l'arbre d'installation réside dans le préfixe sélectionné (par défaut `$HOME/opt/delft3d-flow`) et contient, entre autres, `bin/run_dflow2d3d.sh`, `bin/d_hydro`, et les bibliothèques partagées `flow2d3d`. Le script écrit un fichier d'environnement au préfixe. Source ce fichier dans chaque nouveau shell avant d'exécuter Delft3D-FLOW:

```bash
source "$HOME/opt/delft3d-flow/env.sh"
```

Cette commande réinitialise l'exécution Intel oneAPI, définit `DELFT3D_HOME`, et met les binaires et bibliothèques Delft3D sur `PATH` et `LD_LIBRARY_PATH`.

### Essai avec l'exemple standard

L'installateur exécute déjà ce test à la fin de la construction, sauf si `--no-test` a été donné. Pour le répéter manuellement, utilisez l'exemple standard Delft3D 4 distribué avec le dépôt (un cas de test de marée sur la grille `f34` curviline):

```bash
source "$HOME/opt/delft3d-flow/env.sh"

cd "$HOME/src/delft3d/examples/delft3d4/01_standard"
run_dflow2d3d.sh
```

`run_dflow2d3d.sh` localise l'installation par rapport à son propre chemin et lit le fichier de configuration du modèle `config_d_hydro.xml` à partir du répertoire de travail actuel. La course prend des secondes. Considérez le test réussi lorsque toutes les cales suivantes :

1. La sortie console se termine sans messages d'erreur et le script retourne le code de sortie 0.
2. Les fichiers de résultats d'historique et de carte `trih-f34.dat`, `trih-f34.def`, `trim-f34.dat` et `trim-f34.def` ont été écrits dans le répertoire exemple.
3. Le fichier de diagnostic `tri-diag.f34` ne contient aucune ligne avec `*** ERROR`.

Une vérification rapide :

```bash
ls -l trih-f34.* trim-f34.*
grep -i error tri-diag.f34 || echo "no errors in tri-diag.f34"
```

Une exécution réussie indique que les bibliothèques binaires, les bibliothèques d'exécution et le script de lancement en ligne de commande sont mutuellement cohérents sur l'hôte. Il n'établit pas la validité scientifique d'un modèle de projet. La validation du modèle hydrodynamique demeure spécifique au cas par cas et devrait comprendre la grille, la bathymétrie, l'état des limites, la rugosité, le couplage des procédés et les vérifications d'étalonnage.

### Lancez votre propre modèle

Pour exécuter un modèle de projet, placez les fichiers d'entrée Delft3D-FLOW (par exemple `*.mdf`, grille, bathymétrie et fichiers limites) avec un fichier de configuration `config_d_hydro.xml` dans un répertoire de travail, puis lancez :

```bash
source "$HOME/opt/delft3d-flow/env.sh"

cd /path/to/my-model
run_dflow2d3d.sh                 # uses config_d_hydro.xml
run_dflow2d3d.sh my_config.xml   # or an explicit configuration file
```

Le fichier `config_d_hydro.xml` de `examples/delft3d4/01_standard` sert de modèle; adapter l'entrée `<mdfFile>` au nom du projet `.mdf` fichier. Pour les parcours parallèles avec Intel MPI, l'installation fournit également `run_dflow2d3d_parallel.sh`, qui accepte le nombre de processus et autrement suit les mêmes conventions.

## Fichiers journaux

Chaque installateur écrit un fichier journal horodaté sous :

```bash
$HOME/.cache/delft3d-native-build
```

Si la construction échoue, inspecter la dernière partie du journal :

```bash
tail -n 120 "$HOME/.cache/delft3d-native-build"/build-*.log
```

Pour un enregistrement diagnostique déterministe, copiez la connexion dans le dossier de provenance du modèle ou du logiciel :

```bash
mkdir -p provenance/software
cp "$HOME/.cache/delft3d-native-build"/build-*.log provenance/software/
```

## Modes courants de défaillance

```{list-table} Diagnostic interpretation
:name: diagnostics
:header-rows: 1

* - Symptôme
  - Cause probable
  - Mesures correctives
* - `ifx not found` or `mpiifx not found`
  - Les paquets Intel oneAPI compilateur ou MPI sont absents, ou `setvars.sh` n'a pas été fourni.
  - Réinstaller le compilateur OneAPI et `intel-oneapi-mpi-devel` paquets, ou vérifier `/opt/intel/oneapi/setvars.sh`.
* - `CMake 3.30 or higher is required`
  - Le système CMake ombres l'environnement virtuel CMake.
  - Réinitialisez le script ; il installe CMake en `$HOME/src/delft3d/.venv` et active cet environnement lui-même.
* - Conan rapporte `Invalid setting` pour `compiler.version`.
  - La version OneAPI installée n'est pas blanche dans `conan/config/settings_user.yml`.
  - Laissez le script corriger le profil et les paramètres, ou installez les paquets oneAPI 2024.2 épinglés.
* - Paquet tiers manquant pendant l'installation de Conan.
  - Les utilisateurs externes doivent construire des dépendances localement.
  - Assurez-vous que la commande build inclut `--build-dependencies`; c'est le script par défaut.
* - La configuration de CMake échoue après l'installation de la dépendance.
  - Les bibliothèques hôtes ou la configuration du compilateur diffèrent de la référence du conteneur Deltares Linux.
  - Passez en revue la première erreur CMake, pas seulement le résumé final de la construction.
* - `run_dflow2d3d.sh` commence mais ne peut pas charger une bibliothèque partagée.
  - Le chemin de la bibliothèque est incomplet.
  - Source `<prefix>/env.sh` et confirmer `LD_LIBRARY_PATH` contient `<prefix>/lib`.
* - Build réussit, mais les résultats diffèrent d'un autre poste de travail.
  - La révision source, la version compilatrice, la construction de dépendance ou la configuration d'exécution diffèrent.
  - Enregistrez la révision Git, le journal des scripts, la version OneAPI et les fichiers d'entrée du modèle.
```

## Interprétation du succès

L'installation doit être considérée comme réussie lorsque toutes les conditions suivantes sont remplies:

1. `run_conan.py initialize external` complète sans erreurs à distance.
2. `build.py` complète les étapes de construction et d'installation de CMake.
3. Le préfixe sélectionné contient `bin/run_dflow2d3d.sh`.
4. L'exemple standard de Delft3D 4 s'exécute à partir d'un shell propre après `env.sh` est source et écrit les fichiers de résultats `trih-f34.*` et `trim-f34.*` sans erreurs dans `tri-diag.f34`.
5. Les versions build log, Git revision et compilateur sont archivées.

Pour l'hydraulique de calcul, la disponibilité binaire n'est pas équivalente à la validation du modèle. Une étude de Delft3D-FLOW défendable devrait rapporter la révision du logiciel, l'environnement du compilateur, la schématisation de la grille, les commutateurs de processus physiques, le forçage des limites, les données d'étalonnage et les mesures d'acceptation.

## Désinstallation

Le script installe les fichiers dans l'espace utilisateur par défaut. Pour supprimer l'installation résultante et construire le cache :

```bash
rm -rf "$HOME/opt/delft3d-flow"
rm -rf "$HOME/src/delft3d/build_d3d4-suite_release"
rm -rf "$HOME/src/delft3d/.venv"
rm -rf "$HOME/.conan2"
```

Pour supprimer entièrement l'arbre source cloné:

```bash
rm -rf "$HOME/src/delft3d"
```

Les paquets système installés par `apt`, y compris les paquets Intel oneAPI et l'entrée du dépôt Intel APT dans `/etc/apt/sources.list.d/oneAPI.list`, ne sont pas supprimés automatiquement. Ceci est intentionnel parce que les compilateurs, CMake, Python, Git, et unAPI composants peuvent être partagés par d'autres modèles numériques.

## Citation recommandée pour les rapports

Un énoncé concis de reproductibilité peut être inclus dans la documentation du projet :

> Delft3D-FLOW a été compilé nativement sur un hôte de la Monnaie Ubuntu/Linux en utilisant `install-delft3d-flow-native.sh`. Le script initialise le workflow externe de Conan de Delft3D avec les compilateurs Intel oneAPI 2024.2 et Intel MPI 2021.13, construit la configuration `d3d4-suite` en mode `Release`, et installe l'exécution en ligne de commande sous un préfixe espace utilisateur. La révision de Delft3D Git, la version du compilateur Intel oneAPI et le journal de construction ont été archivés avec les fichiers de provenance du modèle.

## Références

Deltares. 2026. "Compiling Delft3D on Linux." Delft3D GitHub repository documentation. https://github.com/Deltares/Delft3D/blob/main/doc/compiling_Linux.md

Deltares. 2026. "Getting started with code compilation and development." Delft3D GitHub repository documentation. https://github.com/Deltares/Delft3D/blob/main/doc/development.md

Deltares. 2026. "`build.py`." Delft3D GitHub repository. https://github.com/Deltares/Delft3D/blob/main/build.py

Deltares. 2026. "`delft3d_alma8_intel_2024` Conan profile." Delft3D GitHub repository. https://github.com/Deltares/Delft3D/blob/main/conan/config/profiles/delft3d_alma8_intel_2024

Deltares. 2026. "`buildtools.Dockerfile`." Delft3D GitHub repository. https://github.com/Deltares/Delft3D/blob/main/ci/dockerfiles/linux/buildtools.Dockerfile

Intel. 2026. "Install with APT." Intel oneAPI Toolkit Installation Guide for Linux. https://www.intel.com/content/www/us/en/docs/oneapi-toolkit/installation-guide-linux/latest/install-oneapi-toolkit-with-apt.html

Intel. 2024. "Use the setvars and oneapi-vars Scripts with Linux." Intel oneAPI Programming Guide. https://www.intel.com/content/www/us/en/docs/oneapi/programming-guide/2024-2/use-the-setvars-and-oneapi-vars-scripts-with-linux.html

MyST Markdown. 2026. "Callouts & Admonitions." https://mystmd.org/guide/admonitions

Jupyter Book. 2026. "MyST Markdown overview." https://jupyterbook.org/v1/content/myst.html
