---
description: Step-by-step OpenFOAM installation guide for Ubuntu, Debian, and other Linux platforms, enabling CFD and flow-structure interaction simulations without Docker overhead.
---

(openfoam-install)=
# OpenFOAM (Installation)

This tutorial guides through the installation of [OpenFOAM](https://openfoam.org/) on [Ubuntu Linux](https://ubuntu.com/) and {ref}`openfoam-debian`. For installing OpenFOAM on many other platforms (even *Windows*) visit the [developer's website](https://openfoam.org).

```{admonition} Learn OpenFOAM
OpenFOAM represents a powerful modeling tool, which is recommended here for modeling flow-structure interaction. OpenFOAM developers provide detailed documentation with high-quality tutorials on their website. Especially, their 3-week tutorial is a very good start into OpenFOAM modeling for PhD students or engineers.
```

```{admonition} Max out computation power
On Debian Linux / Ubuntu / Mint, preferably install OpenFOAM from the Ubuntu repository rather than installing OpenFOAM in a *Docker* container. The reason for this is that a Docker container is a virtual environment, which does not enable OpenFOAM to directly access the full physical capacity of your computer.
```

## Ubuntu (incl. Mint and Lubuntu)

The installation on *Ubuntu Linux* or one of its derivatives is probably one of the easiest and most sustainable ways for working with OpenFOAM.

### Install OpenFOAM

The installation on any *Ubuntu Linux* platform is straight-forward and can be carried out as described on the [developer's website](https://openfoam.org/download/13-ubuntu/). In detail, these steps include:

1. Download and add the *gpg key* <br> `sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"`
1. Add the repository to *sources.list* <br> `sudo add-apt-repository http://dl.openfoam.org/ubuntu`
1. Update the `apt` package list <br> `sudo apt update`
1. Install OpenFOAM along with a tailored version of ParaView: <br> `sudo apt -y install openfoam13`

Optionally, install *gedit*, which is often used in the documentation and for instructions for setting environment variables:

```
sudo apt install gedit
```

```{tip}
Even though the developer's installation instructions suggest using `apt-get update` / `install`, preferably use `apt update` / `install`.
```

### Update OpenFOAM

The OpenFOAM developers periodically update (recompile) new versions of `openfoam13`. To get these latest versions run:

```
sudo apt update
sudo apt install --only-upgrade openfoam13
```

### Setup User Configuration

OpenFOAM uses a set of environment variables that aid calling the program and its helpers. To define environment variables, every OpenFOAM - *Ubuntu* user needs to modify the *.bashrc* file, which lives in the */home/USER/* directory:

* Open the user *.bashrc* file: <br> `gedit ~/.bashrc`
* On the bottom of the *.bashrc* file add: <br> `source /opt/openfoam13/etc/bashrc`
* Save and close the user *.bashrc* file.

Open a new *Terminal* (or, to be sure, re-login on *Ubuntu*) and test if the system recognizes the OpenFOAM environment variables:

```
simpleFoam -help
```

    Usage simpleFoam [Options]
    ...


If correctly set up, *Terminal* returns a set of options for running OpenFOAM.

### Test-run

With the environment variables defined, create a new directory for OpenFOAM projects:

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
```

Copy the *pitzDaily* OpenFOAM tutorial by using the `$FOAM_[...]` environment variables ([full list](https://openfoamwiki.net/index.php/Environment_variables)):

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Run the *blockMesh* (pre), the *simpleFoam* (main), and the *paraFoam* (post) processors:

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

To get started with OpenFOAM, refer to the *User Guide* provided by [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).

(openfoam-debian)=
## Debian (via Docker)

### Prerequisites

Debian users will need to install *curl* and *docker* for being able to install OpenFOAM. First, make sure to get rid of any outdated version of *docker* (if this returns an error, that is not a problem):

```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

Install *docker* dependencies:

```
sudo apt install apt-transport-https ca-certificates curl gnupg
```

Add *docker*'s *GPG* keys:

```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Add the stable *docker* repository:

```
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update *apt* and install *docker*:

```
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

Verify the successful installation of *docker*:

```
sudo docker run hello-world
```

Until here, *docker* is installed for sudoers only. To enable running *docker* and OpenFOAM for any user, the user's *USERNAME* must be added to the system's `docker` group. Therefore, **add every *docker* and OpenFOAM user to the `docker` group** (required for every **USERNAME**):

```
sudo usermod -aG docker USERNAME
```

With *docker* being installed, the system is ready for the installation of OpenFOAM on *Debian*.

On a remote desktop computer or a virtual machine, make sure to also install *X11* and *Xrdp*, for example for an *Xfce* desktop:

```
sudo apt install xorg dbus-x11 x11-xserver-utils
sudo apt install xfce4 xfce4-goodies xrdp
```

### Install OpenFOAM (v13)

Download the latest OpenFOAM package for *docker*:

```
sudo sh -c "wget http://dl.openfoam.org/docker/openfoam13-linux -O /usr/bin/openfoam13-linux"
```

Make the downloaded `openfoam13-linux` script executable:

```
sudo chmod 755 /usr/bin/openfoam13-linux
```

### Get Started (First-time Launch)

Create a new directory (e.g., */home/OpenFoam13/*) and launch the `openfoam13-linux` environment:

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
openfoam13-linux
```

The *docker* environment should now be launched in *Terminal*. To test OpenFOAM, copy the *pitzDaily* OpenFOAM tutorial by using the [**FOAM** environment variables](https://openfoamwiki.net/index.php/Environment_variables):

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Run the *blockMesh* (pre), the *simpleFoam* (main), and the *paraFoam* (post) processors:

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

To quit *docker*, tap `exit`. The installation procedure is described in detail on the [developer's website](https://openfoam.org/download/13-linux/).

### Usual Launch Procedure

With *docker* and OpenFOAM being installed, every user of the `docker` group (see above instructions for adding users to the docker `group`) can launch OpenFOAM through *Terminal* by entering:

```
openfoam13-linux
```

To quit the program tap (in *Terminal*/*docker*):

```
exit
```

To get started with OpenFOAM, refer to the *User Guide* provided by [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).


## Utilities (Pre- & Post Processors)


### SALOME

To install SALOME, please refer to the TELEMAC installation instruction {ref}`here <salome-install>`.

(freecad-install)=
### FreeCAD

*FreeCAD* is available for most common platforms (operating systems) including *Windows*, *Linux*, and *macOS*. Find the most recent version and installation instructions on the [developer's website](https://www.freecad.org/).
