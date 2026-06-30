---
description: Tutoriel étape par étape pour l'installation automatique de TELEMAC-MASCARET ouvert sur les systèmes Debian Linux et Ubuntu en utilisant des scripts d'installation.
---

(telemac-autoinstall)=
# TELEMAC (Installation automatique)


## Préface

Ce tutoriel vous accompagne dans l'installation [open TELEMAC-MASCARET](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/) and Ubuntu-based systems with **automatic installer** scripts. **Planifier environ 1-2 heures et une connexion Internet stable; les téléchargements dépassent 1,4 Go.** Pour les instructions détaillées d'installation, allez à {ref}`detailed TELEMAC installation page <telemac-install>`.


(telemac-autoinstall-requirements)=
## Exigences

### Paquets système

`````{tab-set}
````{tab-item} Debian 12

Sur Debian 12, demandez à votre administrateur système d'installer les paquets suivants via aptitude:

```bash
sudo apt update

sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmumps-dev libmumps-seq-dev libscalapack-openmpi-dev libmedc-dev libmed-dev libmedimport-dev libmed-tools python3-pytest-cython python3-sphinx python3-alabaster python3-cftime libcminpack1 python3-docutils python3-h5py python3-imagesize clang python3-netcdf4 python3-nlopt python3-nose python3-numpydoc python3-patsy python3-psutil liblzf1 python3-stemmer python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev liblapacke-dev libxml2-dev llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff-dev libgeotiff-dev libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```

````

````{tab-item} Ubuntu 24 / Mint 22
Sur Ubuntu 24 (ou Mint 22), demandez à votre administrateur système d'installer les paquets suivants via aptitude:

```bash
sudo apt update
sudo apt install -y --no-install-recommends  python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1 libegl1 libxrandr2 libxss1 libxcursor1 libxcomposite1 alsa-base libxi6 libxtst6  python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins  libmedc11t64 libmedc-dev libmed-tools libmed11 libmed-dev libmedimport0v5 libmedimport-dev  libopenmpi-dev openmpi-bin libhdf5-dev libhdf5-openmpi-dev hdf5-tools libmetis-dev libmumps-seq-dev libmumps-dev  libscalapack-openmpi-dev python3-pytest-cython python3-sphinx python3-alabaster python3-cftime  libcminpack1 python3-docutils libfreeimage3 python3-h5py python3-imagesize liblapacke  clang python3-netcdf4 libnlopt0 libnlopt-cxx0 python3-nlopt python3-nose python3-numpydoc  python3-patsy python3-psutil libtbb12 libxml++2.6-2v5 liblzf1 python3-stemmer  python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels  python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev  doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev libxml2-dev  llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev  libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev  libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev  libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff5-dev libgeotiff-dev  libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev  libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```
````
`````

Notez que le script d'installation automatique peut détecter d'autres paquets requis.

### Configurer les chemins d'installation

TELEMAC sera téléchargé (cloné-git) de son dépôt GitLab dans un répertoire que vous choisissez, et qui sera appelé répertoire **ROOT** dans ce qui suit. En outre, SALOME sera téléchargé et installé dans ce répertoire ROOT. Sélectionnez l'une des configurations suivantes :

* Un seul utilisateur sans droits d'administration: `ROOT=/home/<USERNAME>/opt` (c'est-à-dire `ROOT=$HOME/opt`) (XDG-conformant alternative: `ROOT=$HOME/.local`)
* Utilisation partagée sans root: seulement si un emplacement groupable existe déjà, par exemple un NFS partage comme `ROOT=/srv/shared/telemac`
* Système à l'échelle du système (admin requis) sur les systèmes basés sur Debian: préféré `ROOT=/usr/local` (binaires à `/usr/local/bin`, bibliothèques à `/usr/local/lib`); `ROOT=/opt` est également acceptable pour un arbre autonome


### SALOME

Choisir la bonne version de SALOME ne peut pas être raisonnablement automatisé, alors trouvez et téléchargez la dernière version de SALOME, et enregistrez-la dans le répertoire ROOT où vous voulez installer Telemac.

```{admonition} How TELEMAC binds to MED files and SALOME
:class: important

TELEMAC lit et écrit `.med` meshs à travers sa couche HERMES, qui est compilée à partir des bibliothèques MED ** (les paquets `libmedc-dev` / `libmed-dev` / `libmedimport-dev`) - **not** à partir des bibliothèques MED groupées à l'intérieur de SALOME. SALOME expédie son propre MED construit avec un ABI différent (64-bit `med_int` et une construction HDF5) et le relie ou le charge avec les déclencheurs de TELEMAC `size of symbol 'med_' changed` liens et l'erreur d'exécution `HERMES_WRONG_MED_FORMAT_ERR`.

SALOME est donc utilisé uniquement pour les outils GUI et mesh. La seule pièce que l'installateur emprunte à SALOME est l'en-tête de Fortran `med_parameter.hf`, que Debian/Ubuntu omit de `libmed-dev` (un trou d'emballage); il ne contient que des constantes et est neutre en ABI. Pour cette raison, **installer SALOME (c.-à-d. fournir `--salome-tar`) avant de lancer l'installateur si vous voulez le support MED** - sinon l'installateur ne peut pas trouver `med_parameter.hf` et MED I/O est désactivé dans la configuration générée. Le fichier généré `pysource.*.sh` supprime en outre tous les répertoires SALOME MED/HDF5 de `LD_LIBRARY_PATH` à l'exécution, de sorte que le système MED est toujours celui qui est chargé.
```

1. Confirmez votre version Linux :
  * Debian: cat /etc/os-release
  * Monnaie : `lsb_release -a`
  * Ubuntu: `inxi -Sx` (travaille également sur la Monnaie)

2. Télécharger la compilation de SALOME
  * Allez au [formulaire officiel de téléchargement de SALOME](https://www.salome-platform.org/?page_id=2430)
  * Choisissez la dernière version avec la compilation Debian/Ubuntu (qui correspond à la base Ubuntu/Mint); ou choisissez le moins fréquemment mis à jour "Linux Universal"

3. Vérifier le somme de contrôle : à partir de la page md5 de SALOME, récupérer le fichier correspondant `.md5` pour votre archive et vérifier localement
  * Exemple pour le Tarball 9.15: dans le répertoire de téléchargement du Tarball, lancez `md5sum SALOME-9.15.0.tar.gz` (terminal)
  * Allez à SALOME [md5 page](https://www.salome-platform.org/?page_id=2818), choisissez le fichier md5 correspondant, et vérifiez que son contenu correspond exactement à la réponse du terminal
  * **Ne sautez pas ça!**

### Obtenez les scripts d'installation

* Téléchargement par les utilisateurs de Debian 12 :
  * [telemac debian12 installer.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/telemac_debian12_installer.sh) et l'enregistrer dans le répertoire ROOT.
  * [systel.debian12.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/systel.debian12.cfg) et l'enregistrer dans le répertoire ROOT.
  * [pysource.debian12.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/pysource.debian12.sh) et l'enregistrer dans le répertoire ROOT.
* Mint 22 / Ubuntu 24 utilisateurs télécharger:
  * [telemac ubuntu24 installer.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/telemac_ubuntu24_installer.sh) et l'enregistrer dans le répertoire ROOT.
  * [systel.mint22.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/systel.mint22.cfg) et sauvegardez-le dans le répertoire ROOT.
  * [pysource.mint22.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/pysource.mint22.sh) et l'enregistrer dans le répertoire ROOT.

Assurez-vous que tous les fichiers sont dans le même répertoire (installation ROOT) sur votre ordinateur.

## Lancer les installateurs

### Modèle d'installation
Note that you might need **admin (sudo) rights** for installing additional system packages and that the installation can take a while because the script downloads Telemac. The script installs by default Telemac v9.1.1. To install another version, use the `--tag "TAG"` option when running the scripts; latest tags can be found at [https://gitlab.pam-retd.fr/otm/telemac-mascaret.git](https://gitlab.pam-retd.fr/otm/telemac-mascaret.git). Both installers also install the system MED packages and compile TELEMAC automatically at the end of the run (unless you pass `--skip-compile`).

Pour lancer l'installateur, tapez sur (remplacez `ROOT` avec votre répertoire ROOT et `SALOME-x.xx.xSRC.tar.gz` avec le nom du tarball SALOME que vous avez téléchargé) :

`````{tab-set}
````{tab-item} Debian 12
```bash
cd ROOT
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "ROOT" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
```

L'installateur a déjà compilé TELEMAC à la fin de sa course (sauf si vous avez passé `--skip-compile`). Pour charger l'environnement - et en option reconstruire à partir de zéro - exécuter:
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean   # only needed for a fresh rebuild
```

````

````{tab-item} Ubuntu 24 / Mint 22
```bash
cd ROOT
chmod +x telemac_ubuntu24_installer.sh
./telemac_ubuntu24_installer.sh --root "ROOT" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
```

Après l'installation, l'environnement Telemac peut être chargé comme suit:
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.mint22.sh
```
````
`````

Les scripts d'installation cloneront la repo `telemac-mascaret` GitLab (avec la balise attribuée), et un dossier `salome`, dans lequel il déballe le tarball SALOME. Si vous rencontrez des erreurs avec SALOME, consultez le {ref}`detailed SALOME installation instructions <salome-install>` dans la section sur l'installation « manuelle » de Telemac.

````{admonition} Test SALOME
:class: tip

SALOME est installé dans le `ROOT/salome` maintenant, et vous pouvez exécuter l'interface graphique comme suit:

```bash
cd ROOT/salome
./salome
```
````

Pour tester l'installation, exécutez le script `config.py` (après la source de l'environnement Telemac):

```bash
config.py
```


### Exemple d'installation

Supposons que vous travaillez sur Debian 12, en conséquence vous avez téléchargé `SALOME-9.15.0-native-DB12-SRC.tar.gz`, défini le répertoire ROOT comme `/home/HyInfo/opt/`, et téléchargé `telemac_debian12_installer.sh`. Ainsi, l'installation peut être démarrée avec ces commandes :

```bash
cd /home/HyInfo/opt
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "/home/HyInfo/opt" --salome-tar "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz" --salome-md5 "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz.md5"
```

Maintenant, activez l'environnement Telemac et compilez comme suit:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean
```

### Exemple d'installation avec une autre version

Supposons que vous travaillez sur Debian 12, en conséquence vous avez téléchargé `SALOME-9.15.0-native-DB12-SRC.tar.gz`, défini le répertoire ROOT comme `/home/HyInfo/opt/`, téléchargé `telemac_debian12_installer.sh`, et voulez **installer Telemac v9.5.0** (si cela existait à https://gitlab.pam-retd.fr/otm/telemac-mascaret.git). Cette installation peut être démarrée avec ces commandes :

```bash
cd /home/HyInfo/opt
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "/home/HyInfo/opt" --tag "v9.5.0" --salome-tar "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz" --salome-md5 "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz.md5"
```

Maintenant, activez l'environnement Telemac et compilez Telemac comme suit:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean
```

### Re-Installer

Pour réparer/réinstaller une installation existante:

1. Naviguez dans votre répertoire TELEMAC :

  ```bash
  cd ~/opt/telemac-mascaret
  ```

2. Relancez l'installateur avec `--skip-apt` pour régénérer les fichiers de configuration (vous utilisez une version plus récente du script d'installation)
  
  ```bash
  chmod +x ./telemac_debian12_installer.sh
  ./telemac_debian12_installer.sh --skip-apt --root "/ROOTDIR" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
  ```

3. Régénérer en réexécutant la configuration et compiler :

  ```bash
  source configs/pysource.debian12.sh
  compile_telemac.py --clean
  ```


(testrun-autoinstaller)=
## TELEMAC d'essai

***Durée estimée: 5-10 minutes.***

Charger l'environnement TELEMAC:

`````{tab-set}
````{tab-item} Debian 12
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.debian12.sh
```
````

````{tab-item} Ubuntu 24 / Mint 22
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.mint22.sh
```
````
`````


Lancez un cas prédéfini à partir du dossier `examples`:

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
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

```{admonition} Got errors?
:class: error, dropdown

S'il y a des erreurs graves, l'installateur automatique pourrait ne pas avoir fonctionné pour votre système (ou subversion). Dans ce cas, il est plus sûr, de recommencer et {ref}`install Telemac manually <telemac-install>`.

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



## Services publics (pré- et post-traitement)

Pour installer des utilitaires pré- et post-traitement, reportez-vous aux instructions dans le {ref}`manual installation section <install-telemac-utilities>`, comme BlueKenue ou le plugin Q4TS dans QGIS. Notez que pour le plugin Q4TS, votre chemin exécutable SALOME est `/ROOT/salome/salome`, et votre script Telemac *environnement* est `/ROOT/telemac-mascaret/configs/pysource.debian12.sh` (ou `/ROOT/telemac-mascaret/configs/pysource.mint22.sh` si vous avez installé sur Ubuntu/Mint).



