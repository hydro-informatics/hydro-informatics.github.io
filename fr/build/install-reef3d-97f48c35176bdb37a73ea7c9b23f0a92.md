---
description: Guide d'installation pour les logiciels CFD open-source REEF3D et DIVEMesh sur Debian, Ubuntu, Linux Mint et les systèmes Linux associés basés sur Debian.
---

# REEF3D (Installation)

Le REEF3D est un cadre hydrodynamique à source ouverte pour les applications CFD à surface libre, la modélisation des vagues, le débit non hydrostatique et les applications à flux peu profond. Il est pertinent pour les cas d'ingénierie hydraulique et côtière où le débit 3D local, les structures hydrauliques, la bathymétrie complexe ou le transport des sédiments sont importants.

Cette page décrit un flux de travail pratique pour les systèmes Linux basés sur Debian, y compris Debian, Ubuntu, Linux Mint, LMDE, Lubuntu et des distributions similaires. Le flux de travail ci-dessous a été vérifié par rapport à la mise en page en amont de GitHub et a publié des informations sur **2026-06-26**. Les modifications en amont sont fréquentes, donc traitez les numéros de version codés dur comme des exemples plutôt que des instructions d'installation permanentes.

```{note}
Pour Linux Mint 22.x, suivez le workflow du paquet Ubuntu 24.04. Pour LMDE, suivez le workflow Debian. Dans les deux cas, le vrai problème n'est généralement pas le système d'exploitation mais les hypothèses de Makefile de REEF3D sur le chemin d'installation d'HYPRE.
```

## Éléments d'installation

Une configuration locale typique nécessite deux exécutables:

- `REEF3D`, le principal résolveur hydrodynamique.
- `DiveMESH`, l'outil mesh et géométrie-préparation utilisé avec REEF3D.

REEF3D est parallèle à MPI et construit actuellement avec `mpicxx`. DIVEMesh est un dépôt séparé et construit avec `g++`.


## Installation automatique avec script helper

Pour la plupart des installations de bureau ou de poste de travail basées sur Debian, la route la plus facile est d'utiliser le script d'aide REEF3D au lieu d'exécuter les commandes manuelles ci-dessous. Le script détecte la distribution Linux, installe les paquets système requis, télécharge les dernières versions de DIVEMesh et REEF3D de GitHub, corrige les problèmes connus du chemin Debian/Ubuntu/Mint Makefile, compile les deux programmes et crée en option un lanceur de bureau.

### La version courte

[Download the installer script `install_reef3d.sh`](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/reef3d-installer/install_reef3d.sh), then run:

```bash
chmod +x install_reef3d.sh
./install_reef3d.sh
```

À la fin d'une installation interactive, le script demande s'il faut créer un lanceur de bureau/menu. Répondre à `Y` pour la créer. Sur les systèmes non interactifs, ou si la réponse doit être fixée à l'avance, utiliser:

```bash
REEF3D_CREATE_DESKTOP=1 ./install_reef3d.sh
```

Par défaut, le script installe REEF3D et DIVEMesh sous :

```bash
~/opt/reef3d
```

Il crée également des liens symboliques dans:

```bash
~/.local/bin
```

Après l'installation, vérifiez que les exécutables sont visibles:

```bash
which REEF3D
which DiveMESH
REEF3D || true
DiveMESH || true
```

Si `which REEF3D` ou `which DiveMESH` ne retourne rien, ouvrez un nouveau terminal ou ajoutez `~/.local/bin` au shell `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Personnalisation

Un répertoire d'installation personnalisé peut être sélectionné avec `--prefix`:

```bash
./install_reef3d.sh --prefix "$HOME/software/reef3d"
```

Pour contrôler le nombre d'emplois de compilateur parallèle, utilisez `-j` ou `--jobs`:

```bash
./install_reef3d.sh -j 8
```

Pour forcer une reconstruction propre, utilisez :

```bash
./install_reef3d.sh --force
```

Pour sauter explicitement le lanceur de bureau, utilisez :

```bash
REEF3D_CREATE_DESKTOP=0 ./install_reef3d.sh
```

```{note}
L'autoinstallateur cible intentionnellement uniquement les systèmes Debian basés sur apt, y compris Debian, Ubuntu, Linux Mint, LMDE et les dérivés proches. D'autres distributions Linux peuvent encore exécuter REEF3D, mais la partie paquet-installation du script doit être adaptée.
```

```{warning}
Le script télécharge les dernières versions en amont de GitHub. C'est pratique pour une première installation, mais pas idéal pour des applications reproductibles. Ainsi, pour les études de cas, enregistrez les étiquettes de sortie REEF3D et DIVEMesh installées, les versions compilatrices, la version OpenMPI et la version système d'exploitation dans la documentation du projet.
```

Les sections suivantes décrivent ce que le script fait en interne et sont utiles pour le dépannage des constructions échouées.



## Installation étape par étape

### Installer les paquets système

Mettre à jour l'index des paquets et installer la chaîne d'outils, MPI, HYPRE et Eigen:

```bash
sudo apt update
sudo apt install \
  build-essential gfortran git wget ca-certificates pkg-config dpkg-dev \
  libopenmpi-dev openmpi-bin \
  libhypre-dev libeigen3-dev
```

Paquets optionnels mais utiles:

```bash
sudo apt install paraview htop tree
```

Vérifiez que les outils importants sont visibles:

```bash
g++ --version
mpicxx --version
which mpicxx
mpirun --version
```

Vérifiez où Debian/Ubuntu a installé HYPRE et Eigen:

```bash
dpkg -L libhypre-dev | grep -E 'HYPRE\.h|libHYPRE\.so'
dpkg -L libeigen3-dev | grep 'Eigen/Dense' | head
```

Sur les systèmes Debian/Ubuntu/Mint, les en-têtes HYPRE sont généralement sous `/usr/include/hypre`, tandis que la bibliothèque est normalement sous un chemin multi-arch comme `/usr/lib/x86_64-linux-gnu/`. C'est pourquoi le fichier de makefile REEF3D en amont a souvent besoin d'un ajustement local.

### Obtenez le code source

Utilisez Git plutôt qu'une archive source aléatoire lorsque c'est possible. Le REEF3D Makefile actuel insère la branche Git et engage les métadonnées dans la compilation, de sorte qu'une commande Git évite les chaînes de version déroutantes.

```bash
mkdir -p ~/src
cd ~/src

git clone https://github.com/REEF3D/REEF3D.git
git clone https://github.com/REEF3D/DIVEMesh.git
```

Liste des versions REEF3D disponibles:

```bash
cd ~/src/REEF3D
git tag --sort=-v:refname | head
```

Pour une installation reproductible, consultez une étiquette de sortie spécifique au lieu de construire ce qui se passe sur `master`:

```bash
# Example only. Replace with the release tag you want to use.
git checkout 26.05
```

```{warning}
Ne gardez pas les anciennes notes d'installation qui disent, par exemple, `cd REEF3D-25.02` comme si c'était la dernière version. Utilisez la page de sortie de GitHub ou `git tag --sort=-v:refname | head` et épinglez la version explicitement dans vos notes de projet.
```

### Construire DIVEMesh

DIVEMesh est séparé de REEF3D et devrait être construit en premier:

```bash
cd ~/src/DIVEMesh
make clean
make -j"$(nproc)"
```

L'exécutable attendu est:

```bash
ls -lh bin/DiveMESH
```

Si vous voulez l'exécutable disponible à l'échelle du système:

```bash
sudo install -m 755 bin/DiveMESH /usr/local/bin/DiveMESH
```

** Correction de ligne du compilateur DIVEMesh**

Au moment de la vérification, le fichier DIVEMesh en amont contenait:

```make
CXX := -g++
```

Ce n'est pas une commande de compilateur valide sur un shell normal Debian/Ubuntu/Mint. Si votre build échoue avec un message comme `-g++: command not found`, corrigez la ligne:

```bash
cd ~/src/DIVEMesh
sed -i 's/^CXX := -g++/CXX := g++/' Makefile
make clean
make -j"$(nproc)"
```

### Construire REEF3D avec les paquets système Debian/Ubuntu/Mint

En amont du REEF3D Makefile, on suppose que l'HYPRE est installé sous `/usr/local/hypre` et qu'il utilise le groupe Eigen de `ThirdParty/eigen-3.3.8`. Les paquets Debian/Ubuntu/Mint installent HYPRE ailleurs, donc ajustez le Makefile avant de compiler. Ne **not** collez les anciens extraits de Makefile qui fixent `CXXFLAGS` à `-std=c++11`; le Makefile actuel en amont utilise `CXXFLAGS := -std=c++17 ...`.

À partir du répertoire source REEF3D :

```bash
cd ~/src/REEF3D
cp Makefile Makefile.orig
```

Corrigez les chemins HYPRE tout en gardant le réglage C++17 en amont :

```bash
python3 - <<'PY'
from pathlib import Path

p = Path("Makefile")
s = p.read_text()

s = s.replace("HYPRE_DIR := /usr/local/hypre", "HYPRE_DIR := /usr")
s = s.replace(
    "LDFLAGS := -L ${HYPRE_DIR}/lib/ -lHYPRE",
    "LIBDIR := /usr/lib/$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)\nLDFLAGS := -L $(LIBDIR) -lHYPRE",
)
s = s.replace(
    "INCLUDE := -I ${HYPRE_DIR}/include -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY",
    "INCLUDE := -I /usr/include/hypre -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY",
)

p.write_text(s)
PY
```

Puis compilez :

```bash
make clean
make release -j"$(nproc)"
```

L'exécutable attendu est:

```bash
ls -lh bin/REEF3D
```

Pour une installation utilisateur-local, ajoutez les deux répertoires exécutables à votre chemin shell :

```bash
cat >> ~/.bashrc <<'EOF'

# REEF3D local build
export PATH="$HOME/src/REEF3D/bin:$HOME/src/DIVEMesh/bin:$PATH"
EOF

source ~/.bashrc
```

Ensuite, vérifiez :

```bash
which REEF3D
which DiveMESH
```

### Alternative: construire HYPRE manuellement sous `/usr/local/hypre`

Le Dockerfile en amont construit OpenMPI et HYPRE à partir de la source et installe HYPRE sous `/usr/local/hypre`. Cela correspond plus étroitement au Makefile par défaut de REEF3D, mais il est plus envahissant sur un poste de travail.

N'utilisez le manuel `/usr/local/hypre` route que lorsque vous avez besoin d'une version HYPRE spécifique ou lorsque le paquet de distribution cause des problèmes de solveur/lien. Pour les postes de travail normaux Debian, Ubuntu et Mint, préférez d'abord `libhypre-dev`.

### Essai

Avant de mettre en place un projet, lancez un petit tutoriel en amont ou un exemple à partir du répertoire REEF3D `Tutorials`:

```bash
cd ~/src/REEF3D/Tutorials
find . -maxdepth 2 -type f | head
```

Suivez les instructions envoyées avec le tutoriel sélectionné. Ne commencez pas à déboguer votre propre géométrie STL, bathymétrie, paramètres de turbulence et conditions limites avant de confirmer que le binaire fonctionne sur un petit cas en amont.

### MPI lance des notes

Pour les parcours parallèles, utilisez `mpirun` ou `mpiexec` selon le tutoriel ou la configuration du cas :

```bash
mpirun -np 4 REEF3D
```

Ne pas exécuter les tâches MPI avec `sudo`. OpenMPI bloque l'exécution racine par défaut pour une raison. Le Dockerfile en amont définit les variables `OMPI_ALLOW_RUN_AS_ROOT` parce que les conteneurs fonctionnent souvent en tant que racine; cette solution appartient aux conteneurs, et non aux postes de travail normaux.

## Dépannage

### `mpicxx: command not found`

Installez les paquets de développement OpenMPI :

```bash
sudo apt install libopenmpi-dev openmpi-bin
which mpicxx
```

### `fatal error: HYPRE.h: No such file or directory`

Le chemin HYPRE include est incorrect ou `libhypre-dev` manque.

```bash
sudo apt install libhypre-dev
dpkg -L libhypre-dev | grep HYPRE.h
```

Assurez-vous que le fichier REEF3D Makefile contient:

```make
INCLUDE := -I /usr/include/hypre -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY
```

### `/usr/bin/ld: cannot find -lHYPRE`

Le linker ne recherche pas le répertoire multi-arch de la bibliothèque Debian/Ubuntu.

```bash
dpkg -L libhypre-dev | grep libHYPRE.so
dpkg-architecture -qDEB_HOST_MULTIARCH
```

Assurez-vous que le fichier REEF3D Makefile contient quelque chose d'équivalent à:

```make
LIBDIR := /usr/lib/$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)
LDFLAGS := -L $(LIBDIR) -lHYPRE
```

### `fatal error: Eigen/Dense: No such file or directory`

Le REEF3D pointe normalement vers Eigen groupé:

```make
EIGEN_DIR := ThirdParty/eigen-3.3.8
```

Si ce dossier manque, utilisez plutôt le chemin système Eigen :

```make
EIGEN_DIR := /usr/include/eigen3
```

Reconstruction ensuite :

```bash
make clean
make release -j"$(nproc)"
```

### La construction échoue après avoir changé de branches ou de balises

Nettoyer le répertoire de construction & #160;:

```bash
make clean
make release -j"$(nproc)"
```

Si cela échoue encore, restaurer le Makefile original et réappliquer seulement le patch de chemin HYPRE:

```bash
cp Makefile.orig Makefile
```

### Binary s'écrase sur un autre ordinateur

La cible en amont `release` utilise `-march=native`. Cela peut créer des binaires optimisés pour le processeur sur lequel ils ont été compilés. Si vous compilez sur une machine et exécutez sur une autre, construire avec la cible moins agressive:

```bash
make clean
make all -j"$(nproc)"
```

Alternativement, modifier la cible `release` et supprimer `-march=native` avant de compiler pour un cluster avec des générations de CPU mixtes.

## Vérification / enregistrement de la version

Pour la reproductibilité, enregistrez l'état/la version exact:

```bash
cd ~/src/REEF3D
git rev-parse --short HEAD
git status --short
mpicxx --version
mpirun --version
ldconfig -p | grep HYPRE || true
```

Conservez la balise/commit REEF3D, la version du système d'exploitation, la version du compilateur, la version MPI et le patch Makefile avec la documentation du cas de simulation.

## Sources REEF3D

- REEF3D Dépôt GitHub: <https://github.com/REEF3D/REEF3D>
- REEF3D publie: <https://github.com/REEF3D/REEF3D/releases>
- REEF3D site en amont et tutoriels: <https://reef3d.wordpress.com/>
- DIVEMesh GitHub dépôt: <https://github.com/REEF3D/DIVEMesh>
- Recherche de paquets Debian : <https://packages.debian.org/>
