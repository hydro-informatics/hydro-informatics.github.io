---
description: Guide d'installation étape par étape pour TELEMAC-MASCARET ouvert sur Debian Linux et Ubuntu, couvrant toutes les dépendances, compilation et configuration d'environnement pour les simulations hydro-morphodynamiques.
---

(telemac-install)=
# TELEMAC (Installation)


## Préface


Ce tutoriel vous accompagne dans l'installation [open TELEMAC-MASCARET](http://www.opentelemac.org/) sur [Debian Linux](https://www.debian.org/)-based systems (y compris Ubuntu et dérivés comme Linux Mint). **Planifier environ 1-2 heures et une connexion Internet stable; les téléchargements dépassent 1,4 Go.**

```{admonition} Developer instructions
:class: note

Les développeurs de TELEMAC fournissent des conseils à jour sur la construction à [https://gitlab.pam-retd.fr/otm/telemac-mascaret/ > BUILDING.md](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/main/BUILDING.md), bien que la documentation pour les composants optionnels reste limitée.
```

****


Cette section ne couvre que l'installation ** de TELEMAC. Pour les didacticiels sur les modèles dynamiques hydro(-morpho) avec TELEMAC, voir {ref}`TELEMAC tutorials section <chpt-telemac>`.

Quelques options d'installation sont disponibles :


`````{tab-set}
````{tab-item} Custom Installation (Recommended)
Continuez à lire et à parcourir les sections suivantes.
````

````{tab-item} Mint Hyfo VM

Si vous utilisez le {ref}`Mint Hyfo Virtual Machine <hyfo-vm>`, vous pouvez sauter les tutoriels de configuration ici. TELEMAC v8p3 est déjà installé et configuré, vous pouvez donc passer directement à {ref}`TELEMAC tutorials <chpt-telemac>`. Traitez cette VM comme un environnement de formation : elle est idéale pour l'apprentissage et l'exécution de cas d'échantillons, mais elle n'est pas destinée à la modélisation à l'échelle de la performance et de l'application.

Chargez l'environnement TELEMAC et vérifiez si cela fonctionne avec :

```
cd ~/telemac/v8p3/configs
source pysource.hyfo.sh
config.py
```
````
````{tab-item} SALOME-HYDRO
TELEMAC est également disponible dans la suite logicielle SALOME-HYDRO, qui est une spinoff de SALOME. Cependant, les principales fonctionnalités de SALOME-HYDRO peuvent migrer vers un nouveau plugin QGIS. Par conséquent, ce livre électronique recommande d'installer TELEMAC indépendamment de tout logiciel de pré- ou post-traitement.
````

````{tab-item} Docker Image

Le bureau d'ingénierie autrichien *Flussplan* fournit un conteneur Docker de TELEMAC v8 sur leur [docker-telemac GitHub depositor](https://github.com/flussplan/docker-telemac). Notez qu'un conteneur Docker représente un environnement virtuel facile à installer qui tire parti de la compatibilité multiplateforme, mais affecte les performances de calcul. Si vous avez installé le logiciel propriétaire Docker et que les performances de calcul ne sont pas la principale préoccupation de vos modèles, le conteneur Docker de Flussplan pourrait être un bon choix. Par exemple, des modèles purement hydrodynamiques avec un petit nombre de nœuds de grille et sans implications supplémentaires du module TELEMAC fonctionneront efficacement dans le conteneur Docker.

````
`````

(modular-install)=
## Exigences de base

```{admonition} Good to know
:class: tip

* L'installation de TELEMAC sur un {ref}`Virtual Machine (VM) <chpt-vm-linux>` est un moyen pratique de commencer et d'exécuter des cas d'échantillons, mais il n'est pas recommandé pour les modèles à l'échelle de l'application en raison de la performance des VM.
* Soyez à l'aise avec le {ref}`Linux Terminal <linux-terminal>`; vous en aurez besoin pour compiler et éventuellement dépanner le workflow de construction de TELEMAC.
* Tout au long de ce tutoriel, nous nous référons au paquet *open TELEMAC-MASCARET* comme TELEMAC. *MASCARET* est un module unidimensionnel (1D), tandis que les méthodes mises en évidence ici se concentrent sur la modélisation bidimensionnelle (2d) et tridimensionnelle (3d).
```

```{admonition} Admin (sudo) rights required for installing basic and optional requirements
:class: attention, dropdown

Les privilèges Superuser (`sudo` pour **su**per **do**ers list) sont requis pour de nombreuses étapes de ce workflow, comme l'installation de paquets, la configuration du système d'édition et l'écriture dans les répertoires système. Sur Debian, l'accès au sudo est généralement accordé en installant `sudo`, en ajoutant votre compte au groupe `sudo` et en gérant les autorisations en toute sécurité avec `visudo` (qui modifie `/etc/sudoers`). Pour des instructions de configuration détaillées, consultez le tutoriel {ref}`Debian Linux <user-rights>` et parlez à votre administrateur système.
```

Travailler avec TELEMAC exige un logiciel pour télécharger les fichiers sources, les compiler et exécuter le programme. Les prérequis logiciels obligatoires pour installer TELEMAC sur [Debian Linux](https://www.debian.org/) sont expliqués dans les sections suivantes.


### Python3

***Durée estimée : 5-8 minutes.***

Python3 a été installé par défaut sur Debian depuis la version 10 (Buster), et il est nécessaire d'exécuter les scripts du compilateur/lanceur de TELEMAC. Pour démarrer Python3, ouvrez un terminal et lancez `python3`; pour quitter, utilisez `exit()` ou appuyez sur `Ctrl+D`.

TELEMAC a besoin de la bibliothèque [NumPy](https://numpy.org/); la plupart des flux de travail s'appuient également sur [SciPy](https://scipy.org/) et [Matplotlib](https://matplotlib.org/). Parce que TELEMAC n'est pas standard, avoir des en-têtes Python et un environnement propre aide.

Pour installer les paquets système commun, exécutez :

```bash
sudo apt update
sudo apt install python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv
```

````{admonition} Got Qt Errors?
:class: warning, dropdown
Si une erreur survient pendant l'installation, installez les dépendances étendues (y compris Qt) avec la commande suivante :

```
sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
```

Ensuite, essayez d'installer les bibliothèques.
````

Si vous êtes sur une ancienne version Debian qui n'inclut pas `distutils` dans le Python par défaut, installez également `python3-distutils`.

Pour tester si l'installation a été réussie, tapez `python3` dans Terminal et importez les trois bibliothèques :

```bash
Python 3.11.1 (default, Jul  25 2030, 13:03:44) [GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> a = numpy.array((1, 1))
>>> print(a)
[1 1]
>>> exit()
```

Aucune des trois bibliothèques importées ne doit retourner un message `ImportError`. Pour en savoir plus sur Python, lisez la section sur {ref}`sec-pypckg`.

(tm-git-requirements)=
### Git

***Durée estimée: <5 minutes.***

L'installation et l'utilisation de Git sont couvertes par le {ref}`git section of this eBook <chpt-git>`. En plus de ce qui y est décrit, vous aurez besoin de Git Large File Storage (Git LFS) pour gérer de grands actifs si un dépôt lié à TELEMAC l'utilise. Sur Debian, vous n'avez généralement besoin que de `git` (pas `git-all`, qui tire beaucoup d'extras), plus `git-lfs`. Installer et initialiser :

```bash
sudo apt update
sudo apt install git git-lfs
git lfs install
```

`git lfs install` configure LFS pour votre compte utilisateur; il est donc inoffensif même si un dépôt donné n'utilise pas LFS.


### GNU Fortran 95 Compilateur (gfortran)

***Durée estimée: 3-10 minutes.***

Le système de construction basé sur Python de TELEMAC nécessite un compilateur Fortran; le choix commun sur Debian est le compilateur GNU Fortran (`gfortran`), qui est rétrocompatible avec GNU Fortran 95 et supporte de nouvelles normes. Debian fournit `gfortran` à partir de ses dépôts standard. Pour l'installer, ouvrez un terminal et lancez :

```bash
sudo apt update
sudo apt install gfortran

```

Après l'installation, vérifiez votre configuration avec `gfortran --version`; le compilateur doit être sur votre `PATH` pour les scripts de TELEMAC pour le trouver.

```{admonition} If the gfortran installation fails...
:class: attention, dropdown


Ensure the standard Debian "main" component is enabled in your APT sources so the `gfortran` package is available. Edit `/etc/apt/sources.list` as root (or add a file in `/etc/apt/sources.list.d/`), then run `sudo apt update`. Verify availability with `apt-cache policy gfortran` or `apt search gfortran`; note that `gfortran` is a metapackage that installs the current default version (for example, `gfortran-12` or `gfortran-13`). Package details are listed here: [https://packages.debian.org/search?keywords=gfortran](https://packages.debian.org/search?keywords=gfortran).
```

### Autres compilateurs et essentiels

***Durée estimée: 2-5 minutes.***

Pour construire TELEMAC et ses dépendances, vous avez besoin de C/C++ et de CMake. Installez les fichiers Debian `build-essential` (qui fournit `gcc`, `g++` et `make`) et `cmake`; ceux-ci sont nécessaires pour compiler les sources, y compris les compilations parallèles (MPI), bien que MPI lui-même soit fourni par des paquets comme OpenMPI que vous installerez plus tard. Le paquet `dialog` est facultatif mais utile car certains scripts d'aide utilisent des interfaces texte simples. Pour modifier les scripts shell, vous pouvez utiliser `gedit` ([lire plus](https://wiki.gnome.org/Apps/Gedit), ou des alternatives telles que Nano ou Vim). Exécuter :

```bash
sudo apt update
sudo apt install -y build-essential cmake dialog gedit gedit-plugins
```


### Configuration du chemin d'installation

Jusqu'ici, le logiciel a été installé via le gestionnaire de paquets de Debian (APTITUDE, `apt`). En revanche, TELEMAC est téléchargé (c'est-à-dire fermé par git) de son dépôt GitLab dans un répertoire que vous choisissez. Son workflow build/install est particulièrement atypique, donc les choix de chemin comptent. Sélectionnez l'une des configurations suivantes :

* Un seul utilisateur sans droits d'administration: `ROOT=/home/<USERNAME>/opt` (c'est-à-dire `ROOT=$HOME/opt`) (XDG-conformant alternative: `ROOT=$HOME/.local`)
* Utilisation partagée sans root: seulement si un emplacement groupable existe déjà, par exemple un NFS partage comme `ROOT=/srv/shared/telemac`
* Système à l'échelle du système (admin requis) sur les systèmes basés sur Debian: préféré `ROOT=/usr/local` (binaires à `/usr/local/bin`, bibliothèques à `/usr/local/lib`); `ROOT=/opt` est également acceptable pour un arbre autonome

Dans les sections qui suivent, nous démontrons une installation mono-utilisateur de TELEMAC (y compris SALOME) avec `ROOT=/home/HyInfo/opt`.


### Obtenez la Repo TELEMAC

***Durée estimée: 25-40 minutes (grands téléchargements).***

Va chercher les sources de TELEMAC avec Git-LFS. Dans le terminal, créez ou choisissez votre répertoire de travail (ici: `/home/HyInfo/opt` - voir ci-dessus), et changez (`cd`) en celui-ci; par exemple:

```bash
cd /home/HyInfo/opt
git clone https://gitlab.pam-retd.fr/otm/telemac-mascaret.git
```

Cela clone le dépôt dans un sous-répertoire nommé `telemac-mascaret`. Pour les téléchargements plus rapides, vous pouvez utiliser un clone peu profond avec `--depth=1`, en comprenant que cela limite l'histoire.

````{admonition} There are many (experimental) branches of TELEMAC available
:class: tip, dropdown

Le dépôt TELEMAC git fournit de nombreuses autres versions TELEMAC sous forme de branches de développement ou de versions anciennes. Par exemple, les clones suivants, la branche `upwind_gaia` à un sous-dossier local appelé `telemac/gaia-upwind`. Après le clonage de cette seule branche, la compilation de TELEMAC peut être faite comme décrit ci-dessous.

```
git clone -b upwind_gaia --single-branch https://gitlab.pam-retd.fr/otm/telemac-mascaret.git telemac/gaia-upwind
```

En savoir plus sur le clonage de branches TELEMAC dans le wiki [TELEMAC](http://wiki.opentelemac.org/doku.php?id=telemac-mascaret_git_repository).
````

Après le clonage du dépôt, identifiez la dernière version étiquetée. Mettez à jour votre liste d'étiquettes et affichez les versions disponibles :

```bash
cd telemac-mascaret
git fetch --tags
git tag -l
```

En novembre 2025, le dernier communiqué officiel publié sur la page "Releases" de GitLab est `v9.0.0`. Vérifiez cette balise exacte (Détachée HEAD), ou créez-en une branche :

```bash
git checkout tags/v9.0.0
```

Si une nouvelle étiquette apparaît plus tard, remplacez son nom en conséquence.


## Exigences facultatives (parallélisme et autres)

This section walks you through installing additional packages required for parallel execution and working with {ref}`SALOME <salome-install>`'s `.med` files. Confirm that the Terminal finds `gcc` (typically installed via `build-essential`) by running `gcc --version`. The packages below enable parallelism and provide substantial speedups for simulations:

* Interface de transmission des messages (MPI)
* Métis

(tm-system-wide-opts)=
### Installation à l ' échelle du système
Installez les conditions préalables pour MPI, Metis, HDF5, MED et MUMPS. Les noms de paquets diffèrent légèrement entre les dérivés Debian et Ubuntu (Mint), donc utilisez le jeu de correspondance ci-dessous.

**Debian (actuellement stable et testé):**
```bash
sudo apt update
sudo apt install -y libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmetis5 libmumps-dev libmumps-seq-dev libscalapack-openmpi-dev libmedc-dev libmed-tools
```

**Ubuntu et ses dérivés (enable Universe d'abord si ce n'est pas encore fait):**
```bash
sudo add-apt-repository -y universe
sudo apt update
sudo apt install -y sudo apt install -y libmedc11t64 libmedc-dev libmed-tools libmed11 libmed-dev libmedimport0v5 libmedimport-dev libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmumps-seq-dev libmumps-dev libscalapack-openmpi-dev
```

Remarques:

* `libopenmpi-dev` et `openmpi-bin` fournir des en-têtes MPI et `mpirun/mpiexec`.
* `libmetis-dev` supplies the partitioner TELEMAC’s `partel` can use.
* `libhdf5-dev` est requis par MED; `libmedc-dev` et `libmed-tools` fournir le support E/S MED utilisé par les maillages générés par SALOME.
* `libmumps-dev` et `libscalapack-openmpi-dev` sont des moteurs de résolution communs pour les grandes séries parallèles.

Si votre version utilise des paquets « t64 » suffixes (par exemple `libmedc11t64`), acceptez ces noms comme offerts par `apt`.

````{admonition} What is behind this (for the blue detail lovers)?
:class: tip, dropdown

***Parallélisme: MPI et Métis***

Pour ne pas se fier aux paquets de distribution, les commandes suivantes récupèrent une fourche de METAS préparée pour les constructions de TELEMAC. Exécuter comme un utilisateur normal:

```bash
cd ~/telemac/optionals
git clone https://github.com/hydro-informatics/metis.git
cd metis
```

Ce dépôt comprend une fourche de Karypis Lab.

```bash
cd GKlib
make config cc=gcc prefix=~/telemac/optionals/metis/GKlib openmp=set
make
make install
cd ..
```

Modifier `~/telemac/optionals/metis/Makefile` et mettre en haut:

```bash
prefix = ~/telemac/optionals/metis/build/
cc = gcc
```

Puis construire et installer Metis:

```bash
make config
make
make install
```

***HDF5 pour les gestionnaires de format MED***

**HDF5** est la bibliothèque d'E/S utilisée par MED. Pour compiler une version HDF5, configurez-la pour l'installer sous un préfixe non système et exportez des chemins dans votre profil shell. Exemple (modifier la version et le préfixe au besoin):

```bash
# build as a normal user
./configure --prefix=$HOME/opt/hdf5
make
make install

# add to your environment
echo 'export PATH=$HOME/opt/hdf5/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$HOME/opt/hdf5/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# verify
h5cc -showconfig
```

*** Bibliothèque de fichiers MED***

La bibliothèque MED (à partir de l'écosystème {ref}`SALOME <salome-install>`) fournit des E/S maillage/résultats utilisés par de nombreux workflows TELEMAC. Pour construire MED vous-même, assurez-vous que sa version HDF5 corresponde à celle utilisée au moment de la compilation et désactivez les liaisons Python à moins que vous ne sachiez également les en-têtes SWIG/Python requis. Alors construisez-le :

```bash
./configure --prefix=$HOME/telemac/optionals/med-4.1.1 --disable-python
make
make install
```

Remarques:
* `--disable-python` évite les conflits de version SWIG; permettre Python nécessite une correspondance `python3-dev` en-têtes et une version SWIG compatible.
* La compatibilité de la version MED avec votre construction HDF5 est critique; le système de mélange HDF5 avec un MED (ou vice versa) construit sur mesure brise fréquemment TELEMAC I/O.

Si vous avez créé des répertoires de construction temporaires, vous pouvez les supprimer :

```bash
cd ~/telemac/optionals
rm -rf temp
```
````

````{admonition} Verify installations
:class: tip

En-têtes d'essai (Ubuntu/Mint):

```bash
test -d /usr/lib/x86_64-linux-gnu/openmpi/include && echo "OK: Open MPI headers"
test -d /usr/include/hdf5/openmpi && echo "OK: HDF5 (OpenMPI) headers"
```

Tester que les bibliothèques résolvent :

```bash
ldconfig -p | grep -E 'libmpi\.so|libmedC\.so|libmed\.so|libmetis\.so|libhdf5_openmpi\.so|libhdf5_serial\.so|libhdf5\.so'
```

Tester les emballages du compilateur MPI:

```bash
mpif90 --help || true
mpifort --showme:compile --showme:link
```

Vous devriez voir les options Fortran rapportées par les enveloppes MPI. Pour un contrôle rapide :

```bash
mpirun -n 2 /bin/true && echo "OK: mpirun executes"
```

D'autres notes d'installation sont disponibles dans le [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_mpi).
````


(salome-install)=
### SALOME

Ce flux de travail explique l'installation de SALOME sur Linux Mint / Ubuntu. Les dépendances minimales en matière de temps d'exécution exigent (au moins) les installations suivantes:

```bash
sudo apt update
sudo apt install python3-pytest-cython python3-sphinx python3-alabaster python3-cftime libcminpack1 python3-docutils libfreeimage3 python3-h5py python3-imagesize liblapacke clang python3-netcdf4 libnlopt0 libnlopt-cxx0 python3-nlopt python3-nose python3-numpydoc python3-patsy python3-psutil libtbb12 libxml++2.6-2v5 liblzf1 python3-stemmer python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels python3-toml python-is-python3

```

Les dépendances minimales de compilation nécessitent les installations suivantes:

```bash
sudo apt update
sudo apt install pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev liblapacke-dev libxml2-dev llvm-dev libnlopt-dev libnlopt-cxx-dev python3-patsy libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff5-dev libgeotiff-dev libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev python3-statsmodels tcl-dev tk-dev 
```

1. Confirmez votre version Linux :
   * Debian: cat /etc/os-release
   * Monnaie : `lsb_release -a`
   * Ubuntu: `inxi -Sx` (travaille également sur la Monnaie)

2. Télécharger la compilation de SALOME
   * Allez au [formulaire officiel de téléchargement de SALOME](https://www.salome-platform.org/?page_id=2430)
   * Choisissez la dernière version avec la construction Ubuntu (qui correspond à la base de la Monnaie); ou choisissez le moins fréquemment mis à jour "Linux Universal"

3. Vérifier le somme de contrôle : à partir de la page md5 de SALOME, récupérer le fichier correspondant `.md5` pour votre archive et vérifier localement
   * Exemple pour la boule de goudron 9.15 : `md5sum SALOME-9.15.0.tar.gz`
   * Comparer avec "SALOME-9.15.0.tar.gz.md5" de la [md5 page](https://www.salome-platform.org/?page_id=2818) - **ne sautez pas cela**

4. Extraire quelque part propre et sain; par exemple comme `sudo` pour l'ensemble du système (justez le nom si vous avez choisi une autre archive), ou suite à ce workflow fow installer TELEMAC à `/home/HyInfo/opt/`:
  
    ```bash
    mkdir -p /home/HyInfo/opt/salome
    tar -xzf ~/Downloads/SALOME-9.15.0.tar.gz -C /opt/salome --strip-components=1
    chown -R "$USER":"$USER" /home/HyInfo/opt/salome
    ```

````{admonition} Troubleshoot "chown: invalid group: ..."
:class: error, dropdown

Si vous recevez un message comme `chown: invalid group: myuser:myuser`, cela signifie `chown` se plaint parce qu'il n'y a aucun groupe nommé `myuser` sur l'ordinateur. Le propriétaire `myuser` existe, mais le groupe myuser ne le fait pas. Pour corriger cela, vérifiez d'abord votre groupe primaire réel:

```bash
id
```

Cela devrait renvoyer quelque chose comme `uid=1234(myuser) gid=100(users) groups=100(users),123(othergroup)`. Maintenant, vous avez deux options pour le dépannage:

Option 1: Remplacer le deuxième `$USER` par votre groupe principal `id`:

```bash
chown -R "$USER":"$(id -gn "$USER")" /home/HyInfo/opt/salome
```

Option 2 (plus robuste): utiliser la détection automatique de votre groupe primaire:

```bash
chown -R "$USER":"$(id -gn "$USER")" /home/HyInfo/opt/salome
```
````


5. Laissez SALOME vérifier votre système et installer ce qu'il demande
   * Dans le répertoire SALOME extrait, identifiez le nom de l'application
   ```bash
   cd /home/HyInfo/opt/salome/sat
   ./sat config --list
   ```
   * Utiliser le nom de la demande; les descriptions suivantes supposent que le nom de la demande est `SALOME-9.15.0-native`
   * Exécutez le checker intégré; il imprime les paquets qui pourraient manquer:
   ```bash
   cd /home/HyInfo/opt/salome/sat
   ./sat config SALOME-9.15.0-native --check_system
   ```
   * Installez les paquets qu'il liste via `apt`, puis reprenez la vérification jusqu'à ce qu'elle soit propre.

6. Assurez-vous que 3D/OpenGL est OK: vérifier la pile de pilote appropriée (surtout pour NVIDIA) avant de lancer; lire plus sur [SALOME PLATFORM FAQ](https://www.salome-platform.org/?page_id=428)

7. Lancez SALOME à partir du dossier SALOME :
  * si dans le sous-dossier `/sat` premier type `cd ..`
  * Run salome: `./salome`

Si vous frappez des erreurs de permission, assurez-vous d'extraire vers un emplacement que vous possédez ou de fixer la propriété. Certains utilisateurs ont rencontré des problèmes en essayant des emplacements étranges ou WSL; s'en tenir à un chemin normal du système de fichiers que vous contrôlez.

Il y a aussi une option conteneur : on peut exécuter SALOME via Docker/Apptainer, mais l'accélération de ParaViS/ParaView à l'intérieur des conteneurs est notoirement buggy et se casse souvent ; le forum SALOME rend les problèmes dans Docker.



(compile-tm)=
## Compiler TELEMAC

### Adapter et vérifier le fichier de configuration (systel.x.cfg)

***Durée estimée: 2-20 minutes.***


Le fichier `systel.x.cfg` indique à TELEMAC comment compiler et lancer ses modules sur votre ordinateur. Plus précisément, c'est la configuration centrale de TELEMAC qui définit les environnements builds et runtime, y compris les compilateurs, les drapeaux compilateurs, les MPI et les options connexes, les bibliothèques externes et les chemins. Dans la pratique, nous utilisons ce fichier pour déclarer les drapeaux et pointer TELEMAC aux dépendances optionnelles. Par défaut, TELEMAC recherche des fichiers de configuration sous `./configs/` (par exemple `configs/systel.cfg`), et on peut passer outre le chemin avec la variable d'environnement `SYSTELCFG` ou l'option `-f` du lanceur Python.

Cette section décrit la configuration de `systel.x.cfg` pour :

* Linux Mint 22 (testé) et Ubuntu 24.04 (attendu être identique, pas encore testé)
* Debian 12 (essai en cours)

Rappelons que nous décrivons l'installation d'un seul utilisateur de TELEMAC dans le répertoire local `/home/HyInfo/opt/telemac-mascaret` et que nous avons installé SALOME à `/home/HyInfo/opt/salome`.

Notez que nous n'avons pas activé l'API, ni les modules [AED2 (waqtel)](http://wiki.opentelemac.org/doku.php?id=installation_linux_aed) et [GOTM (général ocean)](http://wiki.opentelemac.org/doku.php?id=installation_linux_gotm).

Nos fichiers `cfg` et `pysource` définissent une seule construction (par exemple, `hyinfompiubu` sur Mint / Ubuntu) pour [TELEMAC v9.0](https://www.opentelemac.org/), permettant `mpi` et `dyn` options et utilisant des compilateurs GNU (`cc=mpicc`, `fc=mpifort` soutenus par `gfortran`). Les bibliothèques externes sont reliées par l'intermédiaire d'includes et de blocs de bibliothèques pour **OpenMPI, HDF5, MED** (via {ref}`SALOME <salome-install>`), **METIS et MUMPS** avec ScaLAPACK, BLAS et LAPACK. Les entrées RPATH sont ajoutées afin que l'exécution puisse localiser HDF5 et les bibliothèques connexes, en utilisant des chemins qui correspondent aux mises en page typiques de Debian et d'Ubuntu.


`````{tab-set}
````{tab-item} Mint 22 / Ubuntu 24

The following configuration provides a TELEMAC configuration called **hyinfompiubu**. It  enables optimized core flags, position-independent builds, and big-endian unformatted I/O with modified record markers, plus MPI settings on Linux Mint 22 / Ubuntu 24.04. Executables are launched with `mpirun -np <ncsize>`, and meshes are partitioned using `partel`. Build artifacts are placed under `<root>/builds/hyinfompiubu/{bin,lib,obj}`, and the file also defines suffixes, validation paths, and Python F2PY settings (`f2py`, `gnu95`).

Pour l'utiliser pour compiler TELEMAC:

1. Téléchargez [systel.mint22.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/systel.mint22.cfg) de notre dépôt GitHub, ou copiez le contenu du fichier ci-dessous dans le dossier TELEMAC `/configs`, ici: `/home/HyInfo/opt/telemac-mascaret/configs`.
2. Ouvrez `systel.mint22.cfg` dans un éditeur de texte (par exemple, gedit) et remplacez les deux intances `/home/HyInfo/opt/salome` chemin par votre chemin d'installation SALOME.
3. Vérifier les chemins d'installation des options, en particulier HDF5, MED et Oreillons.
4. Enregistrer `systel.mint22.cfg` et fermer l'éditeur de texte.


```bash
# _____                              _______________________________
# ____/ TELEMAC Project Definitions /______________________________/
#
[Configurations]
configs: hyinfompiubu
#
# _____          _________________________________________________
# ____/ General /_________________________________________________/
#
[general]
language: 2
modules:  system
version:  9.0
options:  mpi dyn
hash_char: #
# Suffixes
sfx_zip:  .tar.gz
sfx_lib:  .a
sfx_obj:  .o
sfx_exe:
sfx_mod:  .mod
# Validation paths
val_root:      <root>/examples
val_rank:      all
# Compilers
cc:      mpicc
cflags:  -fPIC -O3
fc:      mpifort
# Core Fortran flags; TELEMAC expects big-endian unformatted files
fflags:  -cpp -O3 -fPIC -fconvert=big-endian -frecord-marker=4 -DHAVE_MPI
# Build commands
cmd_obj_c: [cc] [cflags] -c <srcName> -o <objName>
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# Splitter and MPI run
par_cmdexec:   <config>/partel < <partel.par> >> <partel.log>
mpi_cmdexec:   mpirun -np <ncsize> <exename>
mpi_hosts:
# ----- Optional library blocks merged in libs_all / incs_all -----
# OpenMPI include dir (Ubuntu 24.04)
inc_mpi:       -I /usr/lib/x86_64-linux-gnu/openmpi/include
# HDF5 (Ubuntu serial headers; change to /usr/include/hdf5/openmpi if using libhdf5-openmpi-dev)
inc_hdf5:  -I /usr/include/hdf5/openmpi
libs_hdf5: -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5
ldflags_opt:   -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi
ldflags_debug: -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi

# MED (from SALOME packages)
inc_med:       -I /home/HyInfo/opt/salome/BINARIES-UB24.04/medfile/include
libs_med:      -L /home/HyInfo/opt/salome/BINARIES-UB24.04/medfile/lib -lmedC -lmed -lmedimport
# METIS
inc_metis:     -I /usr/include
libs_metis:    -L /usr/lib/x86_64-linux-gnu -lmetis
# MUMPS + ScaLAPACK (MPI build)
inc_mumps:     -I /usr/include
libs_mumps:    -L /usr/lib/x86_64-linux-gnu -ldmumps -lmumps_common -lpord -lscalapack-openmpi -lblas -llapack
# Aggregate include and library flags
incs_all: [inc_mpi] [inc_hdf5] [inc_med] [inc_metis] [inc_mumps]
libs_all: [libs_hdf5] [libs_med] [libs_metis] [libs_mumps]

# ===== Build section =====
[hyinfompiubu]
brief: Ubuntu 24.04 gfortran + OpenMPI + MED/HDF5 + METIS + MUMPS/ScaLAPACK
system: linux
mpi:   openmpi
compiler: gfortran
pyd_fcompiler: gnu95
f2py_name: f2py
# build tree under <root>=HOMETEL
bin_dir: <root>/builds/hyinfompiubu/bin
lib_dir: <root>/builds/hyinfompiubu/lib
obj_dir: <root>/builds/hyinfompiubu/obj
# override/extend general flags if needed
options: mpi dyn
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# inherit mods_all/incs_all/libs_all from [general]
mods_all:  -I <config>
```
````

````{tab-item} Debian 12

The following configuration provides a TELEMAC configuration called **hyinfompideb12**. It enables optimized core flags, position-independent builds, and big-endian unformatted I/O with modified record markers, plus MPI settings on Debian 12. Executables are launched with `mpirun -np <ncsize>`, and meshes are partitioned using `partel`. Build artifacts are placed under `<root>/builds/hyinfompideb12/{bin,lib,obj}`, and the file also defines suffixes, validation paths, and Python F2PY settings (`f2py`, `gnu95`).

Pour l'utiliser pour compiler TELEMAC:

1. Téléchargez [systel.debian12.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/systel.debian12.cfg) de notre dépôt GitHub, ou copiez le contenu du fichier ci-dessous dans le dossier TELEMAC `/configs`, ici: `/home/HyInfo/opt/telemac-mascaret/configs`.
2. Ouvrez `systel.debian12.cfg` dans un éditeur de texte (par exemple, gedit) et remplacez les deux intances `/home/HyInfo/opt/salome` chemin par votre chemin d'installation SALOME.
3. Vérifier les chemins d'installation des options, en particulier HDF5, MED et Oreillons.
4. Enregistrer `systel.debian12.cfg` et fermer l'éditeur de texte.

Où les paquets vivent habituellement sur Debian 12 :

* Enveloppes et lanceurs OpenMPI : `/usr/bin/mpifort`, `/usr/bin/mpicc`, `/usr/bin/mpirun` ou `/usr/bin/mpiexec`.
* Parallel HDF5: les en-têtes sont en `/usr/include/hdf5/openmpi`, libs en `/usr/lib/x86_64-linux-gnu/hdf5/openmpi` via `libhdf5-openmpi-dev`.
* METIS/ParMETIS: les en-têtes sont à `/usr/include`; libs à `/usr/lib/x86_64-linux-gnu`.

```bash
# _____                              _______________________________
# ____/ TELEMAC Project Definitions /______________________________/
#
[Configurations]
configs: hyinfompideb12
#
# _____          _________________________________________________
# ____/ General /_________________________________________________/
#
[general]
language: 2
modules:  system
version:  9.0
options:  mpi dyn
hash_char: #
# Suffixes
sfx_zip:  .tar.gz
sfx_lib:  .a
sfx_obj:  .o
sfx_exe:
sfx_mod:  .mod
# Validation paths
val_root:      <root>/examples
val_rank:      all
# Compilers (use MPI wrappers on Debian 12/OpenMPI)
cc:      mpicc
cflags:  -fPIC -O3
fc:      mpifort
# Core Fortran flags; TELEMAC expects big-endian unformatted files
fflags:  -cpp -O3 -fPIC -fconvert=big-endian -frecord-marker=4 -DHAVE_MPI
# Build commands
cmd_obj_c: [cc] [cflags] -c <srcName> -o <objName>
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# Splitter and MPI run
par_cmdexec:   <config>/partel < <partel.par> >> <partel.log>
mpi_cmdexec:   mpirun -np <ncsize> <exename>

# ===== Common includes/libs for Debian 12 (OpenMPI / HDF5-openmpi / MED / METIS / MUMPS / ScaLAPACK) =====
# MPI headers (OpenMPI)
inc_mpi:       -I /usr/lib/x86_64-linux-gnu/openmpi/include

# HDF5 parallel (from libhdf5-openmpi-dev)
inc_hdf5:      -I /usr/include/hdf5/openmpi
libs_hdf5:     -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5

# MED-fichier (from SALOME)
inc_med:       -I /home/HyInfo/opt/salome/BINARIES-DB12/medfile/include
libs_med:      -L /home/HyInfo/opt/salome/BINARIES-DB12/medfile/lib -lmedC -lmed -lmedimport

# METIS (from libmetis-dev)
inc_metis:     -I /usr/include
libs_metis:    -L /usr/lib/x86_64-linux-gnu -lmetis

# MUMPS + ScaLAPACK (OpenMPI build)
inc_mumps:     -I /usr/include
libs_mumps:    -L /usr/lib/x86_64-linux-gnu -ldmumps -lmumps_common -lpord -lscalapack-openmpi -lblas -llapack

# Aggregate libraries used by TELEMAC link step
libs_all: [libs_hdf5] [libs_med] [libs_metis] [libs_mumps]

# ===== Build section =====
[hyinfompideb12]
brief: Debian 12 gfortran + OpenMPI + MED/HDF5 + METIS + MUMPS/ScaLAPACK
system: linux
mpi:   openmpi
compiler: gfortran
pyd_fcompiler: gnu95
f2py_name: f2py
# Build tree under <root>=HOMETEL
bin_dir: <root>/builds/hyinfompideb12/bin
lib_dir: <root>/builds/hyinfompideb12/lib
obj_dir: <root>/builds/hyinfompideb12/obj
# Override/extend general flags if needed
options: mpi dyn
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# Inherit mods_all/incs_all/libs_all from [general]
mods_all:  -I <config>
incs_all:  [inc_mpi] [inc_hdf5] [inc_med] [inc_metis] [inc_mumps]
libs_all:  [libs_hdf5] [libs_med] [libs_metis] [libs_mumps]
# rpath for HDF5-openmpi so executables run without extra env
ldflags_opt:   -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi
ldflags_debug: -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi
```
````

````{tab-item} Customization

Les explications suivantes fournissent des conseils sur la personnalisation d'un fichier `cfg` et des modèles de référence disponibles dans le dossier `/configs` de TELEMAC. Ces instructions sont destinées aux utilisateurs qui n'ont pas utilisé d'apt-installation d'OpenMPI, MUMPS, Metis et HDF5 (voir la boîte d'information {ref}`installation instructions for optionals <tm-system-wide-opts>`).

Un fichier typique `systel.*.cfg` a :
1. Une liste optionnelle `[Configurations]` énumérant les sections de construction disponibles.
2. Une section `[general]` avec par défaut.
3. Une ou plusieurs sections de construction comme `[debgfopenmpi]` qui héritent de `[general]` et surpassent les détails. TELEMAC expédie des configs comme `systel.edf.cfg` avec ces modèles.

**Rechercher et sélectionner le bon modèle de configuration :**
* TELEMAC envoie des fichiers de configuration dans `<root>/configs` (par exemple, `systel.edf.cfg`) avec des sections parallèles/debug pour GNU/Intel; copiez et adaptez-en un pour Debian 12.
* Le lanceur Python lit la section active de votre `systel.*.cfg`; assurez-vous `USETELCFG` points à `[debgfopenmpi]` (ou votre section choisie).

Une section brute OpenMPI/gfortran dans le fichier `cfg` pourrait ressembler à ceci pour une configuration nouvellement définie appelée `debgfopenmpi`:

```bash
# _____                          ___________________________________
# ____/ Debian gfortran OpenMPI /__________________________________/
[debgfopenmpi]

par_cmdexec:   <config>/partel < <partel.par> >> <partel.log>
mpi_cmdexec:   /usr/bin/mpirun -wdir <wdir> -np <ncsize> <exename>

cmd_obj:    /usr/bin/mpifort -cpp -c -O3 -DHAVE_MPI -fconvert=big-endian -frecord-marker=4 <mods> <incs> <f95name>
cmd_lib:    ar cru <libname> <objs>
cmd_exe:    /usr/bin/mpifort -fconvert=big-endian -frecord-marker=4 -lpthread -v -lm -o <exename> <objs> <libs>

mods_all:   -I <config>

incs_all:   -I /usr/include/hdf5/openmpi -I /usr/include
libs_all:   -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5 \
            -L /usr/lib/x86_64-linux-gnu -lmetis
```

La section d'OpenMPI + gfortran de Debian 12 utilise toujours les compilateurs d'emballage d'OpenMPI et n'inclut pas de code dur MPI ou les chemins de bibliothèque dans `libs_all` sauf si vous avez une construction locale inhabituelle. Les enveloppes injectent les en-têtes et bibliothèques appropriés.

**Clés importants:**:
 
* `par_cmdexec` indique à TELEMAC quelle commande utiliser pour diviser votre maillage pour une exécution parallèle. `partel` est le séparateur; la redirection `< <partel.par>` lui fournit son fichier de paramètres et le `>> <partel.log>` collecte sa sortie. Vous gardez cette ligne pour activer l'exécution parallèle ; la supprimer rompt le fractionnement et donne "PARTEL.PAR non trouvé" ou erreurs similaires. Les notes d'installation officielles Linux nécessitent un partitionneur pour les constructions parallèles.
* `mpi_cmdexec` est le lanceur d'exécution. Sur Debian 12, `/usr/bin/mpirun` et `/usr/bin/mpiexec` sont fournis par les paquets OpenMPI et sont équivalents à nos fins. `<wdir>` placeholder est le répertoire de travail; `<ncsize>` est le nombre de rangs MPI; `<exename>` est le solveur produit.
* `cmd_obj`, `cmd_lib`, `cmd_exe` définissent les commandes exactes de compilation, d'archive et de lien. On peut appeler `mpifort` plutôt que `gfortran`; l'emballage insère les en-têtes MPI et les libs corrects pour l'OpenMPI que vous avez installé. Cela évite le codage rigide fragile de `-I/usr/lib/.../openmpi/include` ou `-lmpi` avec un SONAME spécifique. Open MPI encourage fortement cette pratique parce que les drapeaux varient par construction et paquet.
* `mods_all` annexes incluent des chemins pour les fichiers de module que TELEMAC génère pendant la compilation; pointer à `<config>` expose les interfaces entre les composants.
* `incs_all` et `libs_all` sont là où vous ajoutez des options non-MPI que vous avez effectivement activés comme AED2, MED, METIS, HDF5. Laissez les MPI purs en dehors de ceux-ci; laissez l'emballage manipuler MPI.

**Drapeaux importants du compilateur:**
* `-cpp` permet le prétraitement des sources de Fortran ainsi `#include`, `#if`, et `#define` travail. Les sources TELEMAC utilisent la compilation conditionnelle; sans prétraitement, ces directives sont ignorées et la compilation peut échouer. Tout compilateur Fortran moderne avec un préprocesseur de type C accepte ce formulaire.
* `-DNAME` macros telles que `-DHAVE_MPI` ou `-DHAVE_AED2` définir les symboles de préprocesseur que la source vérifie dans les blocs `#ifdef` pour compiler les chemins de code corrects. Vous ajoutez seulement `-DHAVE_AED2` si AED2 est présent. Le mécanisme `-D` est standard pour les compilateurs.
* `-fconvert=big-endian` et `-frecord-marker=4` contrôlent l'ordre des octets et des marqueurs d'enregistrement des fichiers non formatés afin que les binaires de différents compilateurs et plateformes restent compatibles avec les attentes des E/S TELEMAC. GNU Fortran documente ces options ; le marqueur d'enregistrement par défaut est 4 octets et le paramètre `-fconvert` affecte la représentation des enregistrements non formatés. Utilisez ces drapeaux systématiquement dans compiler et exécuter pour les E/S reproductibles non formatés.
* `-O3` est une optimisation standard pour les constructions de version. En sécurité avec le gfortran et la base de code de TELEMAC.


**Notes générales**:
* Use `mpifort` (or `mpif90` symlink) and avoid hard-coding `libmpi.so` or MPI include paths. Open MPI's wrapper compilers inject the correct `-I`/`-L`/`-l` automatically; avoid adding MPI headers/libs to `incs_all`/`libs_all`.
* `mpirun` et `mpiexec` sont des lanceurs valides sur Debian 12; utilisez ce que vous préférez.
* METIS/ParMETIS: utilisez des libs partagées (`-lmetis`, `-lparmetis`) au lieu de coder un code statique `.a` dans votre répertoire d'origine, où les en-têtes sont en `/usr/include`; libs en `/usr/lib/x86_64-linux-gnu`.

**Pièges communs:**
* N'enlevez pas `par_cmdexec` dans « corriger » les erreurs de PARTIEL. Vérifiez que `<partel.par>` est produit et que METAS est disponible si vous avez demandé des essais parallèles. Les documents de TELEMAC mettent l'accent sur un cloisonneur nécessaire au parallélisme.
* Ne pas épingler `libs_all` à un `.../openmpi/libmpi.so` littéral ou à un SONAME. Les compilateurs Wrapper existent précisément pour éviter cela ; les SONAMEs et les lignes de liaison diffèrent par OpenMPI build.
* Ajouter des bibliothèques optionnelles seulement lorsque vous avez effectivement activé la fonctionnalité et que vous savez que les en-têtes et les libs existent. Exemple pour AED2 construit sous votre répertoire personnel :
   `incs_all: [..existing..] -I $HOME/telemac/optionals/aed2/include`  
   `libs_all: [..existing..] -L $HOME/telemac/optionals/aed2 -laed2`  
   Leave MPI out of those lists; the wrapper adds MPI. 


If you enable optionals, add only those to `incs_all`/`libs_all` (use specific links for manually installed packages):
* MÉTIS (pour la partition de mailles de PARTEL)
`incs_all: [inc_metis]` avec `inc_metis: -I /usr/include`
`libs_all: [libs_metis]` avec `libs_metis: -L /usr/lib/x86_64-linux-gnu -lmetis`
* AED2 (si vous l'avez construit sous `~/telemac/optionals/aed2/`)
   Add `-DHAVE_AED2` to `cmd_obj` and include/lib paths to your AED2 install, for example:  
   `incs_all: -I <config> -I $HOME/telemac/optionals/aed2/include`  
   `libs_all: -L $HOME/telemac/optionals/aed2 -laed2`  
   Leave MPI out of these lists; the wrapper adds MPI.
* Parallel HDF5 et MED (si vous utilisez Serafin/SELAFIN MED I/O dans votre construction)
   Example flags:  
   `incs_all: [..existing..] -I /usr/include/hdf5/openmpi -I /usr/include`  
   `libs_all: [..existing..] -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5 -L /usr/lib/x86_64-linux-gnu -lmedC -lmed`

**Checklist avant compilation:**
1. `mpifort -show` imprime une ligne de lien `gfortran` qui contient déjà des libs de MPI. Si ce n'est pas le cas, les paquets OpenMPI dev manquent.
2. Si l'utilisation parallèle de HDF5, `h5pfc -show` existe et montre `.../hdf5/openmpi` dans sa sortie; autrement installer `libhdf5-openmpi-dev`.
3. Le nom de la section `.cfg` choisie est celui exporté à `USETELCFG`. Les scripts Python TELEMAC refuseront de construire si cette section est absente.
````
`````


### Configuration du fichier source Python

***Durée estimée: 4-20 minutes.***

Le fichier source Python vit également dans le dossier `/configs` de TELEMAC, où un modèle appelé `pysource.template.sh` est disponible. Plus précisément, le fichier pysource est un script shell "env" que l'on peut `source` dans chaque terminal avant de construire ou d'exécuter TELEMAC. Le lanceur Python utilise quatre ancrages : `HOMETEL`, `SYSTELCFG`, `USETELCFG` et `SOURCEFILE`. Les scripts Python de TELEMAC regardent `SYSTELCFG` et sélectionne la section nommée `USETELCFG`. Cette section guide soit en utilisant notre `pysource.mint22.sh` / `pysource.debian12.sh` (sans AED2), soit en utilisant un fichier source personnalisé.

`````{tab-set}
````{tab-item} Mint 22 / Ubuntu 24

Pour faciliter la configuration du fichier `pysource.mint22.sh` sur Linux Mint 22 / Ubuntu 24, notre modèle est conçu pour être utilisé avec le fichier de configuration `systel.mint22.cfg` décrit ci-dessus, et il est basé sur le fichier par défaut `pysource.template.sh`. Pour l'utiliser pour compiler TELEMAC:

1. Téléchargez [pysource.mint22.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/pysource.mint22.sh) de notre dépôt GitHub, ou copiez le contenu du fichier ci-dessous dans le dossier TELEMAC `/configs`, ici: `/home/HyInfo/opt/telemac-mascaret/configs` et enregistrez `pysource.mint22.sh`.
2. Ouvrez `pysource.mint22.sh` dans un éditeur de texte (par exemple, gedit) et vérifiez les chemins d'installation. Notez que le fichier contient la définition suivante, qui le rend presque indépendant de la définition de votre chemin d'installation, tant que salome vit dans le même répertoire que celui où vous avez téléchargé TELEMAC:
   `_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
3. Vérifier les chemins d'installation des options, en particulier HDF5, MED (en particulier SALOME), et des oreillons.
4. Enregistrer `pysource.mint22.sh` et fermer l'éditeur de texte.

Notre fichier `pysource.mint22.sh` ressemble à ceci :

```bash
#!/usr/bin/env bash
# TELEMAC environment for Linux Mint 22 (Ubuntu 24.04 base) with MPI/HDF5/METIS/MED/MUMPS/ScaLAPACK

# Resolve this script's directory and HOMETEL from it so it works no matter where you cloned TELEMAC
# Expected layout: ~/opt/telemac/{configs, scripts, sources, ...}
_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HOMETEL="$(cd "${_THIS_DIR}/.." && pwd)"
export SOURCEFILE="${_THIS_DIR}"

# Configuration file and config name used by telemac.py
# Adjust USETELCFG to match a section present in your systel.mint22.cfg
export SYSTELCFG="${HOMETEL}/configs/systel.mint22.cfg"
export USETELCFG="hyinfompiubu"

# Make TELEMAC Python utilities available
# (Both python3 helpers and legacy unix scripts are often useful)
if [ -d "${HOMETEL}/scripts/python3" ]; then
  export PATH="${HOMETEL}/scripts/python3:${PATH}"
fi
if [ -d "${HOMETEL}/scripts/unix" ]; then
  export PATH="${HOMETEL}/scripts/unix:${PATH}"
fi

# Compilers and MPI (OpenMPI from APT)
export MPI_ROOT="/usr"
export CC="mpicc"
export FC="mpifort"
export MPIRUN="mpirun"

# Library/include roots from Ubuntu 24.04 packages
# OpenMPI libraries
_OMPI_LIB="/usr/lib/x86_64-linux-gnu/openmpi/lib"
_OMPI_INC="/usr/lib/x86_64-linux-gnu/openmpi/include"

# HDF5 (serial headers via libhdf5-dev; libs in the multiarch lib dir)
# If you later install parallel HDF5 (libhdf5-openmpi-dev), set _HDF5_INC="$_OMPI_INC"
_HDF5_INC="/usr/include/hdf5/openmpi/"
_HDF5_LIB="/usr/lib/x86_64-linux-gnu/hdf5/openmpi"

# MED (optional - not actively used in the corrent setup)
_MED_INC="/usr/include/med"
_MED_LIB="/usr/lib/x86_64-linux-gnu"

# METIS
_METIS_INC="/usr/include"
_METIS_LIB="/usr/lib/x86_64-linux-gnu"

# MUMPS (both seq and mpi dev packages provide headers+libs under multiarch dir)
_MUMPS_INC="/usr/include"
_MUMPS_LIB="/usr/lib/x86_64-linux-gnu"

# ScaLAPACK (OpenMPI build)
_SCALAPACK_LIB="/usr/lib/x86_64-linux-gnu"

# Expose common hints some TELEMAC configs look for (non-fatal if unused)
export MPI_INCLUDE="${_OMPI_INC}"
export MPI_LIBDIR="${_OMPI_LIB}"

export HDF5_ROOT="/usr"
export HDF5_INCLUDE_PATH="${_HDF5_INC}"
export HDF5_LIBDIR="${_HDF5_LIB}"

export MED_ROOT="$HOME/opt/salome/BINARIES-UB24.04/medfile/"
export MED_INCLUDE_PATH="$HOME/opt/salome/BINARIES-UB24.04/medfile/include"
export MED_LIBDIR="$HOME/opt/salome/BINARIES-UB24.04/medfile/lib"

export METIS_ROOT="/usr"
export METIS_INCLUDE_PATH="${_METIS_INC}"
export METIS_LIBDIR="${_METIS_LIB}"

export MUMPS_ROOT="/usr"
export MUMPS_INCLUDE_PATH="${_MUMPS_INC}"
export MUMPS_LIBDIR="${_MUMPS_LIB}"

export SCALAPACK_LIBDIR="${_SCALAPACK_LIB}"

# Build and wrapped API locations (created after you compile)
# Keep these early in the path so Python can import the TELEMAC modules and extensions
if [ -d "${HOMETEL}/builds/${USETELCFG}/wrap_api/lib" ]; then
  export PYTHONPATH="${HOMETEL}/builds/${USETELCFG}/wrap_api/lib:${PYTHONPATH}"
fi

# TELEMAC Python helpers
if [ -d "${HOMETEL}/scripts/python3" ]; then
  export PYTHONPATH="${HOMETEL}/scripts/python3:${PYTHONPATH}"
fi

# Runtime search paths
# Put OpenMPI first to avoid picking up non-MPI BLAS/LAPACK accidentally
# The standard multiarch directory is added as a safety net
for _libdir in \
  "${_OMPI_LIB}" \
  "${_MED_LIB}" \
  "${_METIS_LIB}" \
  "${_MUMPS_LIB}" \
  "${_SCALAPACK_LIB}" \
  "/usr/lib/x86_64-linux-gnu"
do
  case ":${LD_LIBRARY_PATH}:" in
    *:"${_libdir}":*) ;;
    *) export LD_LIBRARY_PATH="${_libdir}:${LD_LIBRARY_PATH}";;
  esac
done

# Add include directories to CPATH so builds find headers without extra flags
for _incdir in \
  "${_OMPI_INC}" \
  "${_HDF5_INC}" \
  "${_MED_INC}" \
  "${_METIS_INC}" \
  "${_MUMPS_INC}"
do
  case ":${CPATH}:" in
    *:"${_incdir}":*) ;;
    *) export CPATH="${_incdir}:${CPATH}";;
  esac
done

# Convenience: print a one-line summary so you know which config is active
echo "TELEMAC set: HOMETEL='${HOMETEL}', SYSTELCFG='${SYSTELCFG}', USETELCFG='${USETELCFG}'"

# Make Python unbuffered for clearer build logs
export PYTHONUNBUFFERED="1"
```
````

````{tab-item} Debian 12

Pour faciliter la configuration du fichier `pysource.debian12.sh` sur Debian 12, notre modèle est conçu pour être utilisé avec le fichier de configuration `systel.debian12.cfg` décrit ci-dessus, et il est basé sur le fichier par défaut `pysource.template.sh`. Pour l'utiliser pour compiler TELEMAC:

1. Téléchargez [pysource.debian12.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/pysource.debian12.sh) de notre dépôt GitHub, ou copiez le contenu du fichier ci-dessous dans le dossier TELEMAC `/configs`, ici: `/home/HyInfo/opt/telemac-mascaret/configs` et enregistrez `pysource.debian12.sh`.
2. Ouvrez `pysource.debian12.sh` dans un éditeur de texte (par exemple, gedit) et vérifiez les chemins d'installation. Notez que le fichier contient la définition suivante, qui le rend presque indépendant de la définition de votre chemin d'installation, tant que salome vit dans le même répertoire que celui où vous avez téléchargé TELEMAC:
   `_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
3. Vérifier les chemins d'installation des options, en particulier HDF5, MED (en particulier SALOME), et des oreillons.
4. Enregistrer `pysource.debian12.sh` et fermer l'éditeur de texte.

Notre fichier `pysource.debian12.sh` ressemble à ceci :

```bash
#!/usr/bin/env bash
# TELEMAC environment for Debian 12 with MPI/HDF5/MED/METIS/MUMPS/ScaLAPACK
# Assumes all optional dependencies are installed from from apt on Debian 12
# Only SALOME is user-installed

# Resolve script directory and HOMETEL from it
_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HOMETEL="$(cd "${_THIS_DIR}/.." && pwd)"
export SOURCEFILE="${_THIS_DIR}"

# Configuration file and config name used by telemac.py
# Adjust USETELCFG to match a section present in configs/systel.debian12.cfg
export SYSTELCFG="${HOMETEL}/configs/systel.debian12.cfg"
export USETELCFG="hyinfompideb12"

# Make TELEMAC Python utilities available
if [ -d "${HOMETEL}/scripts/python3" ]; then
    case ":${PATH}:" in *:"${HOMETEL}/scripts/python3":*) ;; *) export PATH="${HOMETEL}/scripts/python3:${PATH}";; esac
fi
if [ -d "${HOMETEL}/scripts/unix" ]; then
  case ":${PATH}:" in *:"${HOMETEL}/scripts/unix":*) ;; *) export PATH="${HOMETEL}/scripts/unix:${PATH}";; esac
fi

# Detect Debian multiarch lib directory and common include roots
_arch="$(gcc -dumpmachine 2>/dev/null || echo x86_64-linux-gnu)"
_archlib="/usr/lib/${_arch}"

# Helper to pick the first existing directory
_first_dir() {
  for _d in "$@"; do
    [ -d "$_d" ] && { printf '%s' "$_d"; return 0; }
  done
  return 1
}

# MPI. Prefer OpenMPI wrappers if present
_MPI_BIN="$(dirname "$(command -v mpif90 2>/dev/null || command -v mpifort 2>/dev/null || command -v mpicc 2>/dev/null || echo /usr/bin/mpif90)")"
_MPI_INC="$(_first_dir \
  "${_archlib}/openmpi/include" \
  "/usr/include/openmpi" \
  "/usr/include/mpi" \
  "${_archlib}/mpi/include")"
_MPI_LIB="$(_first_dir \
  "${_archlib}/openmpi/lib" \
  "${_archlib}" \
  "/usr/lib")"

# HDF5 parallel. Debian installs OpenMPI-flavored headers in /usr/include/hdf5/openmpi
_HDF5_INC="$(_first_dir \
  "/usr/include/hdf5/openmpi" \
  "/usr/include/hdf5/serial")"
_HDF5_LIB="$(_first_dir \
  "${_archlib}/hdf5/openmpi" \
  "${_archlib}/hdf5/serial" \
  "${_archlib}")"

# MED-fichier
export _MED_ROOT="$HOME/opt/salome/BINARIES-DB12/medfile/"
export _MED_INC="$HOME/opt/salome/BINARIES-DB12/medfile/include"
export _MED_LIB="$HOME/opt/salome/BINARIES-DB12/medfile/lib"

# METIS and ParMETIS
_METIS_INC="$(_first_dir "/usr/include")"
_METIS_LIB="$(_first_dir "${_archlib}")"
_PARMETIS_INC="$(_first_dir "/usr/include")"
_PARMETIS_LIB="$(_first_dir "${_archlib}")"

# MUMPS and ScaLAPACK
_MUMPS_INC="$(_first_dir "/usr/include/mumps" "/usr/include")"
_MUMPS_LIB="$(_first_dir "${_archlib}")"
_SCALAPACK_LIB="$(_first_dir "${_archlib}")"

# Add useful binaries to PATH
for _bindir in \
  "${_MPI_BIN}" \
  "/usr/bin"
do
  case ":${PATH}:" in *:"${_bindir}":*) ;; *) export PATH="${_bindir}:${PATH}";; esac
done

# Library search path
for _libdir in \
  "${_MPI_LIB}" \
  "${_HDF5_LIB}" \
  "${_SCALAPACK_LIB}" \
  "${_MUMPS_LIB}" \
  "${_METIS_LIB}" \
  "${_PARMETIS_LIB}" \
  "${_MED_LIB}"
do
  [ -n "${_libdir}" ] || continue
  case ":${LD_LIBRARY_PATH}:" in *:"${_libdir}":*) ;; *) export LD_LIBRARY_PATH="${_libdir}:${LD_LIBRARY_PATH}";; esac
done

# Include search path for some build helpers that honor CPATH
for _incdir in \
  "${_MPI_INC}" \
  "${_HDF5_INC}" \
  "${_MED_INC}" \
  "${_METIS_INC}" \
  "${_PARMETIS_INC}" \
  "${_MUMPS_INC}"
do
  [ -n "${_incdir}" ] || continue
  case ":${CPATH}:" in *:"${_incdir}":*) ;; *) export CPATH="${_incdir}:${CPATH}";; esac
done

# Convenience: print a one-line summary
echo "TELEMAC set: HOMETEL='${HOMETEL}', SYSTELCFG='${SYSTELCFG}', USETELCFG='${USETELCFG}'"
echo "MPI bin='${_MPI_BIN}', MPI inc='${_MPI_INC}', MPI lib='${_MPI_LIB}'"
echo "HDF5 inc='${_HDF5_INC}', HDF5 lib='${_HDF5_LIB}'"
echo "MED inc='${_MED_INC}', MED lib='${_MED_LIB}'"

# Unbuffered Python for clearer build logs
export PYTHONUNBUFFERED="1"
```

````
````{tab-item} Customization

As a general note, one should expose TELEMAC's Python utilities on `PATH` and `PYTHONPATH` so `telemac2d.py` etc. are found. Prefer OpenMPI wrapper compilers (`mpifort`, `mpicc`) instead of hardcoding MPI headers and libraries. OpenMPI explicitly recommends this; the wrappers inject the right `-I`/`-L`/`-l` for your installation. For optional features like TelApy, TELEMAC builds a small "wrap_api" tree in the build directory; adding that to `PYTHONPATH` and `LD_LIBRARY_PATH` is the correct way to make the Python API importable. Use the following as a starting point; replace `USERNAME` and adjust `SYSTELCFG` and `USETELCFG`:

```bash
#!/usr/bin/env bash
# TELEMAC environment for Debian 12 + OpenMPI

# 1) Core paths
export HOMETEL="/home/USERNAME/telemac-mascaret"
export SYSTELCFG="${HOMETEL}/configs/systel.cis-debian.cfg"
export USETELCFG="debgfopenmpi"
export SOURCEFILE="${HOMETEL}/configs/pysource.gfortranHPC.sh"

# 2) Make TELEMAC tools available
case ":$PATH:" in *:"${HOMETEL}/scripts/python3":*) ;; *) export PATH="${HOMETEL}/scripts/python3:${PATH}";; esac
case ":$PATH:" in *:"${HOMETEL}/scripts/unix":*)   ;; *) export PATH="${HOMETEL}/scripts/unix:${PATH}";; esac
case ":$PYTHONPATH:" in *:"${HOMETEL}/scripts/python3":*) ;; *) export PYTHONPATH="${HOMETEL}/scripts/python3:${PYTHONPATH}";; esac

# 3) Unbuffered Python for clearer build logs
export PYTHONUNBUFFERED="1"

# 4) TelApy (Python API) - populated after a build; harmless if absent
_wrap_api_lib="${HOMETEL}/builds/${USETELCFG}/wrap_api/lib"
[ -d "$_wrap_api_lib" ] && export LD_LIBRARY_PATH="${_wrap_api_lib}:${LD_LIBRARY_PATH}"
[ -d "$_wrap_api_lib" ] && export PYTHONPATH="${_wrap_api_lib}:${PYTHONPATH}"

# 5) MPI - use OpenMPI wrappers; do NOT point to MPICH
# on Debian 12, mpifort/mpirun live in /usr/bin via openmpi-bin/libopenmpi-dev
command -v mpifort >/dev/null 2>&1 || echo "Warning: mpifort not found; install openmpi-bin libopenmpi-dev"
command -v mpirun  >/dev/null 2>&1 || echo "Warning: mpirun not found; install openmpi-bin"

# 6) Optional libs installed from Debian packages need no path tweaks - otherwise,
# if you compiled optionals under $HOMETEL/optionals (e.g., AED2), add them explicitly:
# export LD_LIBRARY_PATH="${HOMETEL}/optionals/aed2:${LD_LIBRARY_PATH}"
# export PYTHONPATH="${HOMETEL}/optionals/aed2:${PYTHONPATH}"

echo "TELEMAC env set: HOMETEL=${HOMETEL}, USETELCFG=${USETELCFG}"
```

**Notes :**
* `SYSTELCFG` points à votre fichier `.cfg`; `USETELCFG` doit correspondre à l'en-tête de section que vous comptez utiliser, par exemple `[debgfopenmpi]`. C'est ainsi que le lanceur Python de TELEMAC découvre la « recette de construction ».
* `PATH` comprend à la fois `scripts/python3` et `scripts/unix` afin que vous puissiez exécuter `telemac.py`, `compile.py`, `runcode.py`, et shell helpers directement.
* `mpifort` et `mpirun` sont les points d'entrée OpenMPI corrects sur Debian 12. `mpif90` existe mais est un alias legs; OpenMPI recommande `mpifort`. `mpirun` et `mpiexec` sont synonymes et expédient à `/usr/bin`.
* Non `MPIHOME` et non `LD_LIBRARY_PATH` hacker pour OpenMPI. Les compilateurs Wrapper suppriment le besoin d'exporter des chemins OpenMPI include/lib; exporter `LD_LIBRARY_PATH` pour pointer les bibliothèques OpenMPI est à la fois inutile et fragile sur Debian
* `wrap_api/lib` sur `PYTHONPATH` et `LD_LIBRARY_PATH` est la bonne façon de rendre TelApy importable après avoir construit. Ceci correspond à l'endroit où TELEMAC émet les artefacts de l'API.
* Ne définissez pas `MPIHOME=/usr/bin/mpifort.mpich` si vous construisez avec OpenMPI. Cette valeur pointe vers un binaire MPICH et provoque des en-têtes et des bibliothèques mal appariés à la compilation ou à l'exécution. Utilisez OpenMPI systématiquement ou changez la pile entière en MPICH. Les propres docs OpenMPI's mettent l'accent sur la consistance de l'emballage.
* Ne pas ajouter `LD_LIBRARY_PATH=$PATH/lib` ou le pointer à `lib/x86_64-linux-gnu/openmpi`. `$PATH` n'est pas un répertoire de bibliothèque, et le codage dur de la bibliothèque dir dans le fichier env est inutile lorsque vous compilez et liez avec `mpifort`.
* N'utilisez pas de code dur `libmpi.so` n'importe où dans `pysource` ou dans votre `.cfg` si vous utilisez déjà des compilateurs d'emballage. Laissez `mpifort` conduire la ligne de lien.

Si vous utilisez des paquets de distribution, vous n'avez généralement pas besoin de définir des chemins dans `pysource`:
* Outils OpenMPI : `/usr/bin/mpifort`, `/usr/bin/mpicc`, `/usr/bin/mpirun` ou `/usr/bin/mpiexec`.
* HDF5 parallèle (si activé dans votre cfg): en-têtes sous `/usr/include/hdf5/openmpi`, libs sous `/usr/lib/x86_64-linux-gnu/hdf5/openmpi` via `libhdf5-openmpi-dev`.
* METIS de Debian: lien `-lmetis` de `libmetis-dev`; en-têtes `/usr/include`, libs `/usr/lib/x86_64-linux-gnu`. Préférez cela sur un `libmetis.a` sous `~/telemac/optionals`.
````
`````

(tm-compile)=
### Compiler

***Durée estimée: 20-30 minutes (le calcul prend du temps).***

Le compilateur est invoqué par les outils Python de TELEMAC en utilisant l'environnement shell défini par votre script `pysource` (`pysource.mint22.sh` ou `pysource.debian12.sh`). Ce script indique à TELEMAC où vivent les programmes d'aide et les bibliothèques et quelle configuration utiliser. Avec elle en place, la compilation devient simple à partir de Terminal. D'abord, source le fichier `pysource` approprié et ensuite vérifier la configuration en exécutant `config.py`:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs    # adjust this path to your install
source pysource.mint22.sh                       # or: source pysource.debian12.sh
config.py
```

Les scripts `pysource.mint22.sh` ou `pysource.debian12.sh` doivent faire écho aux chemins TELEMAC et au nom de configuration. Courir `config.py` devrait afficher la bannière ASCII et terminer par `My work is done`. Sinon, lisez attentivement la sortie de l'erreur; les causes typiques sont les typos dans les chemins ou les noms de fichiers, ou les erreurs à l'intérieur `pysource.x.sh` ou votre `systel.*.cfg`.


```{admonition} Quick health checks after sourcing
:class: tip

* `mpifort -show` devrait imprimer une ligne de commande `gfortran` avec MPI `-I` et `-L` drapeaux injectés. Ceci vérifie que les compilateurs d'emballage sont en place.
* Si vous avez activé le HDF5 parallèle dans votre `.cfg`, `h5pfc -show` devrait réussir et afficher `.../hdf5/openmpi` dans ses drapeaux. Si elle manque, installez `libhdf5-openmpi-dev`.
* Courir `telemac.py` ou `compile.py` sans chemin complet devrait fonctionner parce que `scripts/python3` et `scripts/unix` sont sur `PATH`. Les notes d'installation de TELEMAC Linux suivent cette approche.
```

Après `config.py` complète avec succès, compiler TELEMAC. Utilisez le drapeau `--clean` pour supprimer les artefacts des constructions antérieures et éviter les conflits :

```bash
compile_telemac.py --clean
```

La construction va courir pendant un certain temps et devrait terminer avec le message `My work is done`. Si elle s'arrête avec des erreurs, faites défiler jusqu'à la première erreur et corrigez le problème signalé avant de ré-exécuter la commande.

```{admonition} How to troubleshoot errors in the compiling process
:class: attention

Si la compilation échoue, lisez attentivement la trace et identifiez le composant exact qui s'est rompu. Revoyez les étapes de configuration de ce composant et vérifiez les chemins, les noms de bibliothèque, les variables d'environnement et les modifications de fichiers à partir de ce guide. **Ne pas réinventer la roue :** la plupart des échecs proviennent de petites typos ou de versions incorrectes dans les fichiers que vous avez créés vous-même. Dépannage peut être frustrant, donc défier vos propres hypothèses, corriger la première erreur dans le journal, puis reconstruire à partir d'un état propre.
```

(testrun)=
### TELEMAC d'essai

***Durée estimée: 5-10 minutes.***


Après la fermeture du terminal ou lors d'un nouveau démarrage du système, vous devrez recharger l'environnement TELEMAC avant de l'exécuter:

```bash
cd ~/opt/telemac-mascaret/configs    # adjust if you installed elsewhere
source pysource.mint22.sh            # or: source pysource.debian12.sh
```

Lancez un cas prédéfini à partir du dossier `examples`:

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
```

```{admonition} Examples not working?
:class: error, dropdown

Ne paniquez pas. Si `config.py` a réussi et que la construction s'est terminée avec "Mon travail est fait", votre installation est généralement bonne. La plupart des défaillances d'exemple viennent de problèmes d'environnement ou manquant de grands fichiers. Assurez-vous d'avoir obtenu le bon `pysource.*.sh`, installé toutes les exigences Git **y compris Git LFS, vérifié la bonne version** et tiré le dépôt complet. Si nécessaire, recoller avec Git LFS activé et recompiler TELEMAC, en commençant par {ref}`git section <tm-git-requirements>`.
```

Pour vérifier le parallélisme, installez *htop* pour visualiser l'utilisation du processeur :

```bash
sudo apt update
sudo apt install htop
```

Démarrer le moniteur CPU:

```bash
htop
```

Dans un nouvel onglet terminal, exécutez un exemple TELEMAC avec le drapeau `--ncsize=N`, où `N` est le nombre de processeurs logiques à utiliser (assurer au moins `N` sont disponibles):

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas --ncsize=4
```

Sinon, utilisez `--nctile` et `--ncnode` pour spécifier les noyaux par noeud (NCTILE) et le nombre de nœuds (NCNODE), respectivement, avec `NCSIZE = NCTILE * NCNODE`. Les deux commandes suivantes sont équivalentes (à partir de `~/opt/telemac-mascaret/examples/telemac2d/donau`):

```bash
telemac2d.py t2d_donau.cas --nctile=4 --ncnode=2
telemac2d.py t2d_donau.cas --ncsize=8
```

```{admonition} Cannot find <<PARTEL.PAR>>?
:class: error, dropdown
Si vous voyez `Cannot find << PARTEL.PAR >>` ou `TypeError: can only concatenate str (not ...) to str`, assurez-vous que `par_cmdexec` est retiré de votre fichier de configuration.
```

Pendant que le calcul fonctionne, regardez l'utilisation globale du processeur. Si plusieurs carottes montrent une activité soutenue à des pourcentages variables, l'exécution parallèle fonctionne.

TELEMAC devrait commencer, lancer l'exemple et terminer par `My work is done`. Pour mesurer l'efficacité, varier `--ncsize`. Par exemple, sur un ordinateur portable contemporain, le cas `donau` fonctionne souvent en approx. 1 minute avec `--ncsize=4` et env. 2-3 minutes avec `--ncsize=2`; les timings exacts dépendent du matériel, de la taille du maillage et des I/O. **L'échelle n'est pas linéaire** en raison des frais généraux de répartition, des limites de bande passante de la mémoire et de l'hyperthreading.

````{admonition} Troubleshoot 'No such file or directory'
:class: attention, dropdown
Si vous avez interrompu la session du terminal et que vous voyez `No such file or directory`, rechargez l'environnement TELEMAC avant de rediriger des exemples :

```bash
cd ~/opt/telemac-mascaret/configs
source pysource.mint22.sh      # or: source pysource.debian12.sh
config.py
```

Puis retournez dans le dossier `examples` et lancez le dossier à nouveau.
````

### Générer TELEMAC Documentation

TELEMAC inclut de nombreux exemples d'applications sous `/telemac-mascaret/examples/`, et vous pouvez construire les manuels d'utilisateur et de référence localement. Premièrement, charger l'environnement TELEMAC:

```bash
source ~/opt/telemac-mascaret/configs/pysource.mint22.sh
```

Pour générer le manuel d'utilisation (cela peut prendre un certain temps et nécessite du latex, c'est-à-dire `texlive` sur Debian/Ubuntu):

```bash
doc_telemac.py
```

Pour générer le manuel de référence :

```bash
doc_telemac.py --reference
```

Pour créer des rapports de documentation et de validation pour tous les cas d'exemple :

```bash
validate_telemac.py
```

```{note}
`validate_telemac.py` iterate à travers de nombreux exemples. Certains peuvent échouer si des modules optionnels ne sont pas installés (par exemple HERMES) ou si un exemple est obsolète. La construction de PDF nécessite généralement une chaîne d'outils LaTeX (par exemple `texlive` sur Debian/Ubuntu); installez-la si l'étape de documentation signale des exécutables LaTeX manquants.
```


(install-telemac-utilities)=
## Services publics (pré- et post-traitement)

```{admonition} More Pre- and Post-processing Software
:class: note

D'autres logiciels pour traiter le traitement préalable et post-traitement de TELEMAC sont disponibles sous la forme de {ref}`SALOME <salome-install>` et ParaView.
```

(qgis-telemac)=
### QGIS et le plugin Q4TS (Linux et Windows)

***Durée estimée: 5-10 minutes (selon la vitesse de connexion).***

QGIS est un outil puissant pour la visualisation, la création et l'édition de données géospatiales et est utile pour le pré-traitement et le post-traitement. Les instructions d'installation apparaissent dans les instructions {ref}`qgis-install` et {ref}`QGIS tutorial <qgis-tutorial>` dans ce livre électronique. Le plugin **Q4TS** prend en charge la préparation et la post-traitement des fichiers pour TELEMAC et peut être relié à {ref}`SALOME <salome-install>` pour lancer TELEMAC à partir d'une interface graphique.

To install Q4TS, follow the developers’ instructions at [https://gitlab.pam-retd.fr/otm/q4ts](https://gitlab.pam-retd.fr/otm/q4ts):

* Dans QGIS, ouvrez le **Plugin Manager** (Plugins > Gérer et installer des plugins...).
* Allez à **Paramètres** > **Ajouter...**, définissez l'URL à `https://otm.gitlab-pages.pam-retd.fr/q4ts/plugins.xml`, choisissez un **Nom** (par exemple, `q4ts`), et laissez les autres champs inchangés. Cliquez sur **OK**.
* Cliquez sur **Rechargez tous les dépôts**.
* Dans l'onglet **All**, recherchez `Q4TS` et installez le plugin.

```{admonition} Plugin not found?
:class: warning, dropdown

Q4TS requires QGIS 3.26 or newer. If your QGIS is older, the Plugin Manager will not list it. The reliable fix is to upgrade QGIS. As a temporary workaround, you can download the ZIP from [https://otm.gitlab-pages.pam-retd.fr/q4ts/q4ts.0.7.0.zip](https://otm.gitlab-pages.pam-retd.fr/q4ts/q4ts.0.7.0.zip) and use **Install from ZIP**, but upgrading QGIS is highly recommended.
```

Après l'installation, Q4TS ajoute des outils dans la boîte à outils de traitement QGIS pour la conversion MED -- SLF, le raffinement des mailles, la création de limites, l'édition de tables de friction, etc. L'utilitaire de base pour le post-traitement est décrit dans le `steady-flow simulation tutorial <tm-use-q4ts>` avec Telemac2d.

To get started with the Q4TS plugin, see {numref}`Fig. %s <q4ts-ubuntu>` (Windows: {numref}`Fig. %s <q4ts-windows>`) and consult the developers' user manual on GitLab: [https://gitlab.pam-retd.fr/otm/q4ts/](https://gitlab.pam-retd.fr/otm/q4ts/-/blob/develop/docs/user_manual/user_manual.md).

`````{tab-set}
````{tab-item} Linux (Ubuntu)
```{figure} ../img/telemac/conf-mint22.jpg
:alt: configure Q4TS on Ubuntu Linux
:name: q4ts-ubuntu

La configuration du Q4TS sur Ubuntu Linux. Pour définir ces chemins dans QGIS, allez dans **Paramètres** (menu supérieur) > **Options...** > **Processus** > **Provideurs** > **Q4TS**.
```
````
````{tab-item} Windows
```{figure} https://gitlab.pam-retd.fr/otm/q4ts/-/raw/develop/docs/images/conf_windows.png
:alt: configure Q4TS on Windows
:name: q4ts-windows

La configuration du Q4TS sous Windows (liens à https://gitlab.pam-retd.fr). Pour définir ces chemins dans QGIS, allez dans **Paramètres** (menu supérieur) > **Options...** > **Processus** > **Provideurs** > **Q4TS**.
```
````
`````

```{admonition} Other (stale) plugins
:class: note, dropdown

Les plugins TELEMAC plus anciens et partiellement inactifs pour QGIS comprennent :

* [Telemac Tools](https://plugins.qgis.org/plugins/telemac_tools/), un générateur expérimental de mailles pour les fichiers `*.slf` développés par *Artelia*. Dans QGIS, activez ** plugins expérimentaux** dans le gestionnaire de plugins **Paramètres** avant de rechercher.
* {ref}`BASEmesh <get-basemesh>`, qui peut créer une maille {term}`SMS 2dm` que vous pouvez convertir en géométrie SELAFIN pour TELEMAC (voir {ref}`QGIS pre-processing tutorial for TELEMAC <tm-qgis-prepro>`).
* *PostTelemac*, qui visualise `*.slf` et les formats de résultats connexes (par exemple, `*.res`) au fil du temps.
* *DEMto3D*, qui exporte la géométrie *STL* adaptée pour être utilisée dans *SALOME* et pour créer des maillages 3D.

Notez que *DEMto3D* apparaît dans le menu **Raster** : **DEMto3D** > **Modèle numérique de terrain (MNT) impression 3D**. Ces plugins peuvent être dépassés ou incompatibles avec les versions QGIS actuelles; préférez Q4TS pour les workflows TELEMAC activement maintenus lorsque c'est possible.
```

(artelia-mesh)=
### Outils Artelia Mesh

Artelia provides a Python-based analysis toolkit on GitHub: [https://github.com/Artelia/Mesh_tools](https://github.com/Artelia/Mesh_tools). Hydro-informatics.com has not yet tested Mesh Tools, but it appears promising for inspecting and analyzing existing meshes rather than generating new ones; see the related discussion in the [TELEMAC forum](https://www.opentelemac.org/index.php/kunena/qgis-for-otm/14662-meshtools).

Après avoir installé le plugin via le Gestionnaire de Plugin QGIS, accédez à partir de **Mesh** > **Mesh Tools**.


(bluekenue)=
### BlueKenue (Windows ou Linux+Wine)

***Durée estimée: 10 minutes.***

[BlueKenue](https://nrc.canada.ca/en/research-development/products-services/software-applications/blue-kenuetm-software-tool-hydraulic-modellers)<sup>TM</sup> is a Windows-based pre- and post-processing tool from the [National Research Council Canada](https://nrc.canada.ca/en), which is designed for TELEMAC. It offers functionality similar to [Fudaa](http://www.opentelemac.org/index.php/latest-news-development-and-distribution/240-fudaa-mascaret-3-6) and includes a capable mesh generator, which is the main reason to install BlueKenue<sup>TM</sup>. Download the installer from the developer site: [https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) (credentials are noted in the [Telemac Forum](http://www.opentelemac.org/index.php/assistance/forum5/blue-kenue)). Then choose the install method for your platform:

1. Sous Windows: exécutez l'installateur BlueKenue `.msi` directement.
2. Sur Linux : utilisez [Wine amd64](https://wiki.debian.org/Wine) via {ref}`PlayOnLinux <play-on-linux>` pour installer BlueKenue<sup>TM</sup>. Pour les systèmes Ubuntu/Debian, consultez la section {ref}`PlayOnLinux <play-on-linux>` dans ce livre électronique. L'installation avec le vin uni seulement est découragée en raison de problèmes de compatibilité communs.

Typique BlueKenue<sup>TM</sup> Les emplacements exécutables sont :

* 32 bits: `"C:\\Program Files (x86)\\CHC\\BlueKenue\\BlueKenue.exe"`
* 64 bits: `"C:\\Program Files\\CHC\\BlueKenue\\BlueKenue.exe"`

Pour de plus amples renseignements sur les plates-formes, veuillez consulter le [CHyMS FAQ](https://chyms.nrc.gc.ca/docs/FAQ.html), en particulier la section intitulée Blue Kenue sur [autres systèmes d'exploitation](https://chyms.nrc.gc.ca/docs/FAQ.html#troubleshooting-how-run-on-another-os).


(fudaa)=
### Fudaa-PrePro (Linux et Windows)

***Durée estimée : 5-15 minutes (limite de temps supérieure si java doit être installé).***

Fudaa-PrePro est un avant-plan graphique basé sur Java pour le système TELEMAC qui vous aide à configurer des modèles en définissant les maillages, les conditions limites et initiales, et les fichiers de pilotage (`.cas`), et il peut également lancer des simulations et aider à la post-traitement de base. Il est maintenu par le projet Fudaa et distribué avec documentation et téléchargements sur leur site, et il est référencé par les développeurs TELEMAC comme un pré-processeur convivial pour configurer les calculs. Préparez-vous avec le logiciel pré- et post-traitement Fudaa-PrePro:

* Installer *Java* :
    + Sur Linux: `sudo apt install default-jdk` (le JRE seul fonctionne pour courir; le JDK est sûr pour le fonctionnement et les outils)
    + Sous Windows: obtenir Java de [java.com](https://java.com/)
* Téléchargez la dernière version à partir du dépôt [Fudaa-PrePro](https://fudaa-project.atlassian.net/wiki/spaces/PREPRO/pages/237993985/Fudaa-Prepro+Downloads).
* Décompresser le fichier téléchargé et procéder selon votre plateforme (voir ci-dessous).
* `cd` vers le répertoire où vous avez décroché les fichiers du programme Fudaa-PrePro.
* Démarrer Fudaa-PrePro à partir du terminal ou de l'offre de commande :
    + Sur *Linux*: lancez `sh supervisor.sh`
    + Sur *Windows*: lancez `supervisor.bat`

Si vous voyez une erreur telle que:

```bash
Error: Could not find or load main class org.fudaa.fudaa.tr.TrSupervisor
```
modifier `supervisor.sh` et remplacer `$PWD Fudaa` par `$(pwd)/Fudaa` afin que le classpath résout correctement. Vous pouvez également ajuster le paramètre RAM par défaut à `supervisor.sh` (ou `supervisor.bat`). Fudaa-PrePro expédie souvent avec `-Xmx6144m` (6 GB); augmentez-le pour de très grands maillages (des millions de nœuds) ou réduisez-le sur des systèmes à faible RAM. Définissez `-Xmx` à un multiple raisonnable de 512 Mo. Par exemple, pour utiliser 2 Go et fixer le chemin de classe:

```bash
#!/bin/bash
cd "$(dirname "$0")"
java -Xmx2048m -Xms512m -cp "$(pwd)/Fudaa-Prepro-1.4.2-SNAPSHOT.jar" org.fudaa.fudaa.tr.TrSupervisor "$@"
```
