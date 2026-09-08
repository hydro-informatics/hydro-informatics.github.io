---
description: Guide d'installation d'OpenFOAM étape par étape pour les plateformes Ubuntu, Debian et autres Linux, permettant des simulations d'interaction CFD et flow-structure sans frais généraux Docker.
---

(openfoam-install)=
# OpenFOAM (Installation)

Ce tutoriel guide l'installation de [OpenFOAM](https://openfoam.org/) sur [Ubuntu Linux](https://ubuntu.com/) et {ref}`openfoam-debian`. Pour installer OpenFOAM sur de nombreuses autres plateformes (même *Windows*), visitez le [site Web du développeur](https://openfoam.org).

```{admonition} Learn OpenFOAM
OpenFOAM représente un outil de modélisation puissant, qui est recommandé ici pour la modélisation de l'interaction écoulement-structure. Les développeurs OpenFOAM fournissent une documentation détaillée avec des tutoriels de haute qualité sur leur site Web. En particulier, leur tutoriel de 3 semaines est un très bon début dans la modélisation OpenFOAM pour les doctorants ou les ingénieurs.
```

```{admonition} Max out computation power
Sur Debian Linux / Ubuntu / Mint, de préférence installer OpenFOAM à partir du dépôt Ubuntu plutôt que d'installer OpenFOAM dans un conteneur *Docker*. La raison en est qu'un conteneur Docker est un environnement virtuel, qui ne permet pas à OpenFOAM d'accéder directement à la pleine capacité physique de votre ordinateur.
```

## Ubuntu (y compris la menthe et le lubuntu)

L'installation sur *Ubuntu Linux* ou l'un de ses dérivés est probablement l'un des moyens les plus faciles et les plus durables de travailler avec OpenFOAM.

### Installer OpenFOAM

L'installation sur n'importe quelle plate-forme *Ubuntu Linux* est directe et peut être effectuée comme décrit sur le [site Web du développeur](https://openfoam.org/download/13-ubuntu/). En détail, ces étapes comprennent :

1. Téléchargez et ajoutez la touche *gpg* <br> `sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"`
1. Add the repository to *sources.list* <br> `sudo add-apt-repository http://dl.openfoam.org/ubuntu`
1. Update the `apt` package list <br> `sudo apt update`
1. Installez OpenFOAM avec une version personnalisée de ParaView : <br> `sudo apt -y install openfoam13`

En option, installez *gedit*, qui est souvent utilisé dans la documentation et pour les instructions de réglage des variables d'environnement:

```
sudo apt install gedit
```

```{tip}
Même si les instructions d'installation du développeur suggèrent d'utiliser `apt-get update` / `install`, de préférence utiliser `apt update` / `install`.
```

### Mettre à jour OpenFOAM

Les développeurs OpenFOAM mettent périodiquement à jour (recompiler) les nouvelles versions de `openfoam13`. Pour faire fonctionner ces dernières versions :

```
sudo apt update
sudo apt install --only-upgrade openfoam13
```

### Configuration utilisateur

OpenFOAM utilise un ensemble de variables d'environnement qui aident à appeler le programme et ses helpers. Pour définir les variables d'environnement, chaque utilisateur OpenFOAM - *Ubuntu* doit modifier le fichier *.bashrc* qui vit dans le répertoire */home/USER/* :

* Ouvrir le fichier utilisateur *.bashrc* : <br> `gedit ~/.bashrc`
* Au bas du fichier *.bashrc* ajouter : <br> `source /opt/openfoam13/etc/bashrc`
* Enregistrer et fermer le fichier utilisateur *.bashrc*.

Ouvrir un nouveau *Terminal* (ou, pour être sûr, re-connecter sur *Ubuntu*) et tester si le système reconnaît les variables d'environnement OpenFOAM :

```
simpleFoam -help
```

Utilisation simpleFoam [Options]
...


Si la configuration est correcte, *Terminal* renvoie un ensemble d'options pour exécuter OpenFOAM.

### Essai

Avec les variables d'environnement définies, créez un nouveau répertoire pour les projets OpenFOAM :

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
```

Copier le tutoriel *pitzDaily* OpenFOAM en utilisant les variables d'environnement `$FOAM_[...]` ([liste complète](https://openfoamwiki.net/index.php/Environment_variables)):

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Exécutez les processeurs *blockMesh* (pre), *simpleFoam* (main) et *paraFoam* (post) :

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

Pour commencer avec OpenFOAM, consultez le *Guide de l'utilisateur* fourni par [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).

(openfoam-debian)=
## Debian (via Docker)

### Préalables

Les utilisateurs Debian devront installer *curl* et *docker* pour pouvoir installer OpenFOAM. Tout d'abord, assurez-vous de se débarrasser de toute version obsolète de *docker* (si cela retourne une erreur, ce n'est pas un problème):

```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

Installer les dépendances *docker* :

```
sudo apt install apt-transport-https ca-certificates curl gnupg
```

Ajouter les touches *GPG* de *docker* :

```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Ajouter le dépôt stable *docker* :

```
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Mettre à jour *apt* et installer *docker*:

```
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

Vérifier l'installation réussie de *docker*:

```
sudo docker run hello-world
```

Jusqu'ici, *docker* est installé uniquement pour les sudoers. Pour activer l'exécution de *docker* et OpenFOAM pour tout utilisateur, le *USERNAME* de l'utilisateur doit être ajouté au groupe `docker` du système. Par conséquent, ** ajoutez chaque utilisateur *docker* et OpenFOAM au groupe `docker`** (obligatoire pour chaque **USERNAME**):

```
sudo usermod -aG docker USERNAME
```

Avec *docker* installé, le système est prêt pour l'installation d'OpenFOAM sur *Debian*.

Sur un ordinateur de bureau distant ou une machine virtuelle, assurez-vous d'installer également *X11* et *Xrdp*, par exemple pour un bureau *Xfce* :

```
sudo apt install xorg dbus-x11 x11-xserver-utils
sudo apt install xfce4 xfce4-goodies xrdp
```

### Installer OpenFOAM (v13)

Téléchargez le dernier package OpenFOAM pour *docker*:

```
sudo sh -c "wget http://dl.openfoam.org/docker/openfoam13-linux -O /usr/bin/openfoam13-linux"
```

Rendre l'exécutable de script `openfoam13-linux` téléchargé :

```
sudo chmod 755 /usr/bin/openfoam13-linux
```

### Démarrer (premier lancement)

Créer un nouveau répertoire (par exemple, */home/OpenFoam13/*) et lancer l'environnement `openfoam13-linux`:

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
openfoam13-linux
```

L'environnement *docker* devrait maintenant être lancé dans *Terminal*. Pour tester OpenFOAM, copiez le *pitzDaily* Didacticiel OpenFOAM en utilisant les variables d'environnement [**FOAM**](https://openfoamwiki.net/index.php/Environment_variables):

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Exécutez les processeurs *blockMesh* (pre), *simpleFoam* (main) et *paraFoam* (post) :

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

Pour quitter *docker*, appuyez sur `exit`. La procédure d'installation est décrite en détail sur le [site Web du développeur](https://openfoam.org/download/13-linux/).

### Procédure de lancement habituelle

Avec l'installation de *docker* et OpenFOAM, chaque utilisateur du groupe `docker` (voir les instructions ci-dessus pour ajouter des utilisateurs au docker `group`) peut lancer OpenFOAM via *Terminal* en entrant :

```
openfoam13-linux
```

Pour quitter le programme tapez (dans *Terminal*/*docker*):

```
exit
```

Pour commencer avec OpenFOAM, consultez le *Guide de l'utilisateur* fourni par [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).


## Services publics (pré- et post-processeurs)


### SALOME

Pour installer SALOME, veuillez consulter l'instruction d'installation de TELEMAC {ref}`here <salome-install>`.

(freecad-install)=
### FreeCAD

*FreeCAD* est disponible pour la plupart des plateformes courantes (systèmes d'exploitation) dont *Windows*, *Linux* et *macOS*. Trouvez la version la plus récente et les instructions d'installation sur le [site Web du développeur](https://www.freecad.org/).
