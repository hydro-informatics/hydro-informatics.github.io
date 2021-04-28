# Install OpenFOAM

This tutorial guides through the installation of [*OpenFOAM*](http://www.openfoam.org/) on [Ubuntu Linux](https://www.ubuntu.org/) and [*Debian Linux*](#debian). For installing *OpenFOAM* on many other platforms (even *Windows*) visit the [developer's website](https://openfoam.org).

## Ubuntu (incl. Mint and Lubuntu)

The installation on *Ubuntu Linux* or one of its derivatives is probably one of the easiest and most sustainable ways for working with *OpenFOAM*.

### Install *OpenFOAM*

The installation on any *Ubuntu Linux* platform is straight-forward and can be carried out as described on the [developer's website](https://openfoam.org/download/8-ubuntu/). In detail, these steps include:

1. Download and add the *gpg key* <br> `sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"`
1. Add the repository to *sources.list* <br> `sudo add-apt-repository http://dl.openfoam.org/ubuntu`
1. Update the `apt` package list <br> `sudo apt update`
1. Install *OpenFOAM* along with a tailored version of *ParaView*: <br> `sudo apt-get -y install openfoam8`

Optionally, install *gedit*, which is often used in the documentation and for instructions for setting environment variables:

```
sudo apt install gedit
```

```{tip}
Even though the developer's installation instructions suggest using `apt-get update` / `install`, preferably use `apt update` / `install`.
```

### Update *OpenFOAM*

The *OpenFOAM* developers periodically update (recompile) new versions of `openfoam8`. To get these latest versions run:

```
sudo apt update
sudo apt install --only-upgrade openfoam8
```

### Setup User Configuration

*OpenFOAM* uses a set of environment variables that aid calling the program and its helpers. To define environment variables, every *OpenFOAM* *Ubuntu* user needs to modify the *.bashrc* file, which lives in the */home/USER/* directory:

* Open the user *.bashrc* file: <br> `gedit ~/.bashrc`
* On the bottom of the *.bashrc* file add: <br> `source /opt/openfoam8/etc/bashrc`
* Save and close the user *.bashrc* file.

Open a new *Terminal* (or, to be sure, re-login on *Ubuntu*) and test if the system recognizes the *OpenFOAM* environment variables:

```
simpleFoam -help
```

    Usage simpleFoam [Options]
    ...


If correctly setup, *Terminal* returns a set of options for running *OpenFOAM*.

### Test-run

With the environment variables defined, create a new directory for *OpenFOAM* projects:

```
cd ~
mkdir OpenFoam8
cd OpenFoam8
```

Copy the *pitzDaily* *OpenFOAM* tutorial by using the `$FOAM_[...]` environment variables ([full list](https://openfoamwiki.net/index.php/Environment_variables):

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

To get started with *OpenFoam*, refer to the *User Guide* provided by [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).

## Debian 10 {#debian}

### Prerequisites

Debian users will need to install *curl* and *docker* for being able to install *OpenFOAM*. First, make sure to get rid of any out-dated version of *docker* (if this returns an error, that is not a problem):

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

Until here, *docker* is installed for sudoers only. To enable running *docker* and *OpenFOAM* for any user, the user's *USERNAME* must be added to the system's `docker` group. Therefore, **add every *docker* and *OpenFOAM* user to the `docker` group** (required for every **USERNAME**):

```
sudo usermod -aG docker USERNAME
```

With *docker* being installed, the system is ready for the installation of *OpenFOAM* on *Debian*.

On a remote desktop computer or a virtual machine, make sure to also install *X11* and *Xrdp*, for example for an *Xfce* desktop:

```
sudo apt install xorg dbus-x11 x11-xserver-utils
sudo apt install xfce4 xfce4-goodies xrdp
```

### Install *OpenFOAM* (v8)

Download the latest *OpenFOAM* package for *docker*:

```
sudo sh -c "wget http://dl.openfoam.org/docker/openfoam8-linux -O /usr/bin/openfoam8-linux"
```

Make the downloaded `openfoam8-linux` script executable:

```
sudo chmod 755 /usr/bin/openfoam8-linux
```

### Get Started (First-time Launch)

Create a new directory (e.g., */home/OpenFoam8/*) and launch the `openfoam8-linux` environment:

```
cd ~
mkdir OpenFoam8
cd OpenFoam8
openfoam8-linux
```

The *docker* environment should now be launched in *Terminal*. To test *OpenFOAM*, copy the *pitzDaily* *OpenFOAM* tutorial by using the [**FOAM** environment variables](https://openfoamwiki.net/index.php/Environment_variables):

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

To quit *docker*, tap `exit`. The installation procedure is described in detail on the [developer's website](https://openfoam.org/download/8-linux/).

### Usual Launch Procedure

With *docker* and *OpenFOAM* being installed, every user of the `docker` group (see above instructions for adding users to the docker `group`) can launch *OpenFOAM* through *Terminal* by entering:

```
openfoam8-linux
```

To quit the program tap (in *Terminal*/*docker*):

```
exit
```

To get started with *OpenFoam*, refer to the *User Guide* provided by [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).


## External Utilities (Pre- & Post Processors)

### SALOME <a name="salome"></a>

Similar as for *TELEMAC*, the *SALOME* platform represents a powerful toolkit for generating computational meshes for *OpenFOPAM*. Download *SALOME* from [salome-platform.org](https://www.salome-platform.org/downloads/current-version) for your distribution (here: *Linux Ubuntu*).

Unpack the *SALOME* package in a convenient folder (replace the `.tar.gz` file name with the one you downloaded):

```
tar xfz SALOME-9.6.0-UB20.04-SRC.tar.gz
```

Install dependencies:
```
sudo apt install net-tools libopengl0 libtbb-dev
```

To run *SALOME*, `cd` to the directory where the unpacked package is located and typ `salome`:

```
cd SALOME-9.6.0-UB20.04-SRC.tar.gz
source env_launch.sh
./salome
```

If `./salome` does not work (in particular on a *Virtual Machine*), try to run `./mesa_salome` (prevents problems with *openGL* in the *Mesh* module), or re-compile *SALOME*:

```
./sat prepare SALOME-9.6.0
./sat -t compile SALOME-9.6.0
./sat environ SALOME-9.6.0
./sat launcher SALOME-9.6.0
./salome
```

If there is any error such as:

```
HyMo@HydroDebian:~/Downloads/SALOME-9.6.0-UB20.04-SRC$ ./salome
runSalome running on HydroDebian
Searching for a free port for naming service: 2811 - OK
Searching Naming Service  +omniNames: (0) 20XX-XX-XX 12:34:13.123745: -ORBendPoint option overriding default endpoint.
 found in 0.1 seconds
Searching /Kernel/Session in Naming Service  +SALOME_Session_Server: error while loading shared libraries: libtbb.so.2: cannot open shared object file: No such file or directory
Warning, no type found for resource "localhost", using default value "single_machine"
Traceback (most recent call last):
  File "/home/HyMo/Downloads/SALOME-9.6.0-UB20.04-SRC/BINARIES-UB20.04/KERNEL/bin/salome/orbmodule.py", line 181, in waitNSPID
    os.kill(thePID,0)
ProcessLookupError: [Errno 3] No such process

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/HyMo/Downloads/SALOME-9.6.0-UB20.04-SRC/BINARIES-DEB10/KERNEL/bin/salome/runSalome.py", line 679, in useSalome
    clt = [...]
  File "/home/HyMo/Downloads/SALOME-9.6.0-UB20.04-SRC/BINARIES-DEB10/KERNEL/bin/salome/orbmodule.py", line 183, in waitNSPID
    raise RuntimeError("Process %d for %s not found" % (thePID,theName)
RuntimeError: Process 29241 for /Kernel/Session not found
--- Error during Salome launch ---
```

Then look for the missing libraries indicated in the above block with `error while loading shared libraries: libtbb.so.2: cannot open shared object file`. In this case `libtbb` is missing, which can be installed with `sudo apt install libtbb-dev`.
