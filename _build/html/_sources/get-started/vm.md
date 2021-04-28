# Virtual machines and Linux

Your computer is one of your most important educational companions. So you want to protect the health of your computer and avoid problems caused by redundant or even malicious software. For this reason, it is recommended to install all software used on this website on a so-called Virtual Machine (VM). This page explains what VMs are, what advantages they have exactly, and how you can install [Debian Linux](https://www.debian.org/), one of the most stable and secure operating systems. It does not matter if you use Apple's *mac OS* or Microsoft's *Windows*, or if you already use Linux: The VM will look the same at the end.

## About

### What is a Virtual Machine (VM)?

A Virtual Machine (VM) represents a virtual operating system (OS) running on a host system that directly runs on a physical computer. The physical computer (hardware) resources of the host system are allocated via so-called hypervisors. For this reason, the virtual machine is referred to as a *guest machine* and the hypervisor as a *host machine*. Thus, a *guest machine* is an isolated, virtualized environment that runs independently on the host operating system.

### Why use a VM?

Free resources on a computer represent, from an economic point of view, dead storage space that causes costs without generating income. This is why system administrators often create multiple virtual servers to better allocate physical resources and save energy. A VM is also useful for smart end-users such as researchers and engineers. Here are some advantages of a VM:

* Applications and services of multiple VMs do not interfere with each other.
* Independence of the guest system from the operating system of the host system and the physical hardware.
* VMs can be moved or cloned by simply copying them to other systems.
* Hardware resources can be dynamically allocated via the host hypervisor.
* Better and more efficient use of existing hardware resources.
* Short deployment times for systems and applications running on a VM.
* VMs provide high availability and flexibility because of their independence of physical resources.


In the context of hydro-informatics for water resources management, a VM can serve to execute various *Python* scripts with different dependencies or, most importantly, to set up a clean and efficient environment for the execution of numerical models such as [open TELEMAC-MASCARET](http://www.opentelemac.org/).

### Contents and Debian Linux

This page guides through the installation of a [Debian Linux](https://www.debian.org/) virtual machine. The host hypervisor is assumed to be Oracle's [VirtualBox](https://www.virtualbox.org/) on *Windows 10*. If you are not using *Windows 10*, just download the *VirtualBox* installer that suits your system.

The guest machine will run Debian Linux, which is one of the most stable Linux distributions, and it is freely available. Because of its stability, Debian is an ideal baseline for running numerical simulations that may last for days or even weeks. Of course, there are other options, and Debian is rather one of the best options than *the best option*.

There are a couple of Debian Linux spin-offs, such as [*Ubuntu*](https://ubuntu.com) with some other derivatives that are more light-weight (and faster). New Linux users will have an easy start with the *Ubuntu* variants [*Linux Mint* (*Xfce*)](https://www.linuxmint.com) or [*Lubuntu*](https://lubuntu.me/downloads/). Most versions *Ubuntu* can be used instead of the Debian Linux presented here to complete the tutorials on this website.

## Create a Debian Linux VM

### Get prerequisites (required software)

***Estimated duration: 5-30 minutes (depends on connection speed).***

* Download and install the latest version of [VirtualBox](https://www.virtualbox.org/).
    + *Oracles*'s *VirtualBox* is a free and open-source hosted hypervisor software.
    + The installation of *VirtualBox* requires administrator rights on the host machine. So if you are working in a professional environment, talk to your IT administrator.
    + *VirtualBox* installers are available for *Windows*, *mac OS*, and *Solaris*.
* Download the latest Debian Linux (or on of its spin-offs - see next bullet point) net installer (this is the **recommended** solution **for** working with **TELEMAC**):
    + Find the CD-section and click on the [*amd64*](https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/) version
    + Scroll to the bottom of the page and download the latest net installer (*debian-xx.x.x-amd64-netinst.iso*)
    + If the above link is not working, visit [debian.org](https://www.debian.org/), find the *Getting Debian* section (do not click on the one in the top menu), click on *CD/USB ISO images* and click on [Download CD/DVD images using HTTP](https://www.debian.org/CD/http-ftp/).
* *ISO* images for Debian spin-offs can also be used to complete the tutorials on this website (all-round systems):
    + [*Lubuntu*](https://lubuntu.me/downloads/) is a fast and light-weight derivative of *Ubuntu*
    + [*Linux Mint* (*Xfce*)](https://www.linuxmint.com) is another efficient *Ubuntu* spin-off that is always based the penultimate *Ubuntu* version (e.g., if the current *Ubuntu* version is 20.0, then the current *Mint* version is 19.0 and builds on *Ubuntu* 19.0)

Remember where the downloaded Linux *.ISO* file is stored.

### Create a VM with *VirtualBox*

***Estimated duration: 5-8 minutes.***

In your host system (e.g., *Windows 10*), click on *Start*, type *Oracle VM VirtualBox*, and hit enter. In the opened *VirtualBox* manager window:

* Click on the blue *New* button to open the VM creation wizard and enter:
    + *Name:* Debian Linux <br>*Note: The wizard should automatically recognize the* Type *and*Version *fields.*
    + *Machine Folder:* `C:\Users\USERNAME\VirtualBox VMs`
    + *Type:* Linux
    + *Version:* Debian (64-bit)  <br>> Click on the *Next* button
    + Allocate memory size: the more memory is allocated to the VM, the faster will be the VM (and for example TELEMAC-MASCARET), but the slower will be the host system (*Windows 10*). Rule of thumb: stay in the green range of the bar (e.g., allocate 8192 MB)
    <br>> Click on the *Next* button
    + Select *Create a virtual hard disk now* and click on the *Create* button.
    + Select *VDI* (native to *VirtualBox*) and click on *Next*.
    + Preferably choose *Dynamically allocated* to start with a small virtual disk size, which can take a maximum size to be defined in the next step. Click on the *Next* button.
    + Leave the default disk name as is and allocate a maximum size for the virtual disk (recommended: min. 32 GB). Click on the *Create* button.
* Great - the basics are all set now and we are back in the *VirtualBox* main window, where a *Debian Linux* VM should be visible now on the left side of the window.
* With the *Debian Linux* VM highlighted (i.e., just click on it), click on the yellow *Settings* wheel-button, which opens the *Settings* window:
    + In the *System/Motherboard* tab, verify the memory allocation and check the *Enable EFI (special OSes only)* box (enable).
    + In the *System/Processor* tab, select the number of processors that the VM uses. To not slowing down the host system (*Windows 10*), stay in the green range of the CPU bar. For parallel processing with TELEMAC-MASCARET, allocate at least 4 CPUs.
    + In the *Display* tab, check the *Enable 3D Acceleration* box.
    + In the *Storage* tab, find the *Controller: IDE*, where an *Empty* disk symbol should be located below.
        - Click on the *Empty* disk symbol and find the *Attributes* frame on the right side of the window, where a small blue disk symbol should be visible.
        - Click on the small blue disk symbol to *Choose a disk file ...* > select the Debian Linux net installer (*debian-xx.x.x-amd64-netinst.iso*) that you downloaded before.
    + Click *OK*.

### Install Debian Linux

***Estimated duration: 30 minutes.***

To install Debian Linux to the VM, start the before created *Debian Linux VM* in the *VirtualBox* manager window (click on the *Debian Linux* VM and then on the green *Start* arrow). The *VirtualBox VM* window will ask for the *.iso* file to use (confirm the selected one), and start navigating through the installation:

* Inside the *VirtualBox VM* window, select the *Graphical install* option.
* Navigate through the language options (recommended: English - English (United States)).
* Optionally define a hostname (e.g., debian-vm) and a domain name (e.g., debian-net).
* Create a root user name and password (write down the credentials somewhere) as well as a user name (no root rights) and password.
* Set up the clock.
* Disk partitioning: Choose the *Guided - use entire disk* option. Click *Continue* (2 times).
* Select the *All files in one partition (recommended for new users)* option. Click *Continue*.
* Make sure that *Finish partitioning and write changes to disk* is selected and click *Continue*.
* Select *Yes* in the next step (*Write the changes to disks?*). <br>... grab your favorite beverage and wait while the installation progresses ...
* Select *No* to answer the question *Scan another CD or DVD?* and click *Continue*.
* Select the geographically closest mirror to access Debian archives (software repositories and updates) and click *Continue* (2 times).
* Skip the proxy information question (just click *Continue*).
* Optionally, select *No* to answer the question *Participate in the package usage survey?* and click *Continue*.
* Software to install: Select *GNOME* and keep the other defaults (Debian desktop, print server, and standard system utilities).
 <br>... continue enjoying your favorite beverage and wait while the installation progresses ...
* Click *Continue* to finalize the installation and reboot (or shutdown) the VM.

Once the VM is shutdown, re-open the VM *Settings* (from *VirtualBox Manager* window) and go to the *Storage* tab. Verify that there is again an *Empty* disk symbol in the *Controller: IDE* field.

## Get started with (Debian) Linux

## Setup Linux {#setup-debian}

***Estimated duration: 15 minutes.***

Start the *Debian Linux* VM from the *VirtualBox* manager window. Once Debian Linux has started, log on with your user credentials.

To enable the full functionality of the system, open the Linux Terminal (`CTRL` + `Alt` + `T` or go to *Activities* > *Files* (filing cabinet symbol), right-click in any folder and select *Open in Terminal*). In *Terminal* type:

```
su
```

Enter the above-created password for the root user name (see installation section).

```{note}
Root access (e.g., for installing software) is granted on many Linux distribution using the `sudo` command before the command to execute. In Debian Linux, `sudo` may refer to the wrong account and not work as desired. As a workaround type `su` in *Terminal*. More later on this page.
```

Install all packages required for building kernel modules:

```
apt update
apt install build-essential dkms linux-headers-$(uname -r)
```

Find the *Devices* drop-down menu of the *VirtualBox VM* window (not in Debian Linux itself) and select *Insert Guest Additions CD image...* (depending on the version of *VirtualBox*, this menu can be on the top or the bottom of the window).

```{tip}
The *VirtualBox VM* window does not show the menu with the *Devices* entry anywhere?<br><br>
    + This may happen when the *View* was set to *Scaled mode*.<br><br>
    + To toggle the view mode and make the menu bar visible, press the RIGHT `CTRL` (`Host`) key + the `C` on your keyboard, while being in the host system view.
```

```{note}
If the error `The guest system has no CR-ROM ...` occurs, shutdown the VM. In the *VirtualBox* manager window, right-click on the *Debian Linux* VM > *Storage* tab > Add new Optical Drive to *Controller: IDE*. Restart the *Debian Linux* VM.
```

Back in the Debian Linux *Terminal*, mount the *Guest Additions* *iso* file by typing in *Terminal*:

```
sudo mkdir -p /mnt/cdrom
sudo mount /dev/cdrom /mnt/cdrom
```

Navigate to the mounted directory and execute the *VBoxLinuxAdditions.run* file with the *--nox11* flag to avoid spawning an xterm window.

```
cd /mnt/cdrom
sudo sh ./VBoxLinuxAdditions.run --nox11
```

The kernel modules will be installed now and *Terminal* should prompt a message that invites to reboot the system. Do so by typing:

```
shutdown -r now
```

After rebooting, make sure that the installation was successful. In *Terminal* type:

```
lsmod | grep vboxguest
```

If the *Terminal*'s answer is something like `vboxguest   358395 2 vboxsf`, the installation was successful. Read more about *Guest Additions* on the [*VirtualBox* developer's website](https://www.virtualbox.org/manual/ch04.html).

To improve the visual experience do the following:
* In the top-left corner of the Debian Linux Desktop, click on *Activities* and type *displays* in the search box.
* Open the *Displays* settings to select a convenient display resolution.
    + If you choose a too high resolution, the *VirtualBox VM* window will turn black and jump back to the original resolution after 15-30 seconds.
    + Consider also to turn on *Night Light* to preserve your eye vision.
* *Apply* the changes and close the *Displays* settings.

### Familiarize with Debian Linux and Terminal {#terminal}

***Estimated duration: 60 minutes.***

To get familiar with Debian Linux, go to the *Activities* menu and find the applications *LibreOffice-Writer*, *Firefox*, the *Software* application (shopping bag symbol), and the *File* manager (filing container symbol).
Find more applications by clicking on the four dots on the left of the menu bar - can you find the Text Editor?
To shutdown Debian Linux (i.e., the VM), click on the top-right corner arrow and press the Power symbol.

The GNOME *Terminal* is one of the most important features, event though it optically shows only an empty window with a blinking cursor at the beginning. There are many ways to open *Terminal* and here are two options:

1. Go to *Applications* and type *Terminal* in the search box, or
1. Open the *File* browser (*Applications* > *Files* - the filing container symbol), navigate to the folder where you want to run *Terminal*, right-click in the free space, and left-click on *Open in Terminal*.

*Terminal* runs many powerful native Linux (UNIX) commands, which is the most robust way to install and execute features. There are a couple of tutorials for learning to use *Terminal* and one of the most comprehensive is provided on the *Linux Ubuntu* website (Ubuntu is based on Debian Linux). It is highly recommended to go through the [tutorial provided by the Ubuntu community](https://ubuntu.com/tutorials/command-line-for-beginners) (*estimated duration: 51 minutes*), for better understanding some contents presented here on *hydro-informatics.github.io*. In particular, memorize the commands `cd` (change directory), `su`/`sudo` (superuser), `ls` (listen) and `mkdir` (make directory).


### Setup user rights {#users}
When installing software later, it is good practice to install it for your user account and not for `root`. Such system-relevant actions require *superuser* (`su`) rights. However, your default user name is not on the so-called *su-doers* list, which is essentially a file where all user accounts are listed that are authorized to use `sudo` in front of any command. So add your user account to the *su-doers* list by opening *Terminal* and typing:

```
su
    password: ...
sudo usermod -aG sudo YOUR-USER-NAME
```

Open a new *Terminal* tab (`Shift` + `CTRL` + `T`), which should open up in your default user space with default user rights. Check if your account is on the *su-doers* list by typing:

```
sudo -v
```

If visually nothing happens, you are good to go. Otherweise, if you get a message like `Sorry, user [username] may not run sudo on [hostname].`, verify that you correctly typed the above command and *YOUR-USER-NAME* (with correct cases).

### Enable folder sharing {#share}

***Estimated duration: 5-10 minutes.***

```{admonition} Requirements
Make sure to install *Guest Additions* to enable folder sharing (see the above [Setup Linux](#setup-debian) section).
```

Sharing data between the host system (e.g., *Windows 10*) and the guest system (*Debian Linux VM*) enables to transfer files to and from the VM to the host system.

* At a place of your convenience, create a new folder on the host system (e.g., *Windows 10*) and call it shared (e.g., `C:\Users\USER\documents\shared\`).
* Start *VirtualBox* and the Debian Linux VM.<br>*Make sure that the scaled view mode is off (toggle view modes with RIGHT `CTRL` (`Host`) key + the `C` on the keyboard).*
* Go to the VM *VirtualBox* window's *Devices* menu, click on *Shared Folders* > *Shared Folders Settings...* and click on the little blue *Add new shared folder* symbol on the right side of the window (see figure below). Make the following settings in the pop-up window:
    + *Folder Path:* Select the just created `...\shared` folder
    + Check the *Enable Auto-mount* box
    + Check the *Make Permanent* box
* Click OK on both pop-up windows.

![share-folder](https://github.com/Ecohydraulics/media/raw/master/png/vm-share-folder.png)

The shared folder will then be visible in the *Files* (*Activities* > *Filing cabinet symbol*) on the left (e.g., as *sf_shared*).

```{note}
File sharing only works with the *Guest Additions CD image* installed (see above section on setting up and familiarizing with Debian Linux).
```

A ***Permission denied*** message is likely to appear when you click on `sf_shared`. The message may appear because your user name is not assigned to the *vboxsf* group. The *vboxsf* is the one, which is automatically assigned for accessing the shared folder. To verify the group name, go to the shared folder, right-click in the free space, and select *Permissions*. A window with group names that have access to the shared folder opens. To add your username type (in *Terminal*):

```
sudo usermod -aG vboxsf YOUR-USER-NAME
```

Afterwards, **reboot the *Debian Linux VM*** and test if you can access the folder, and create and modify files.

***

### Enable OpenGL {#opengl}

*VirtualBox* experimentally enables [*OpenGL*](https://www.opengl.org), which is used by many graphical user interfaces. To make *OpenGL* work on a virtual machine, the install [*X.Org X Window System*](https://www.x.org/) (xserver):

```
sudo apt install xorg
```

Run *Xorg* as normal user with:

```
startx
```

Or run *Xorg* as root (super user) with:

```
sudo service gdm start
```

To edit the configuration of *Xorg* run:

```
sudo editor /etc/X11/xorg.conf
```

Add *nvidia* repositories and drivers (maybe not necessary on newer versions of *Debian*:

```
sudo apt install software properties-common
sudo add-apt-repository contrib
sudo add-apt-repository non-free
sudo apt update
```

Then install *OpenGL* with:

```
sudo apt install libopengl0-glvnd-nvidia libglx0-glvnd-nvidia
```

### Install and Update Software (optional)

***Estimated duration: Variable.***

To install other software, preferably use the built-in software manager (*Activities* > *Shopping bag* symbol). The *Software* manager uses official releases in the stable Debian repository ([read more about lists of sources](https://wiki.debian.org/SourcesList)).

To update repositories and upgrade installed packages, open *Terminal* and type:

```
sudo apt update
sudo apt full-upgrade
sudo apt autoremove
```

The last command removes files that are not needed any more and reduces  system garbage.

```{note}
Being a new Linux end user, preferably use `apt` rather than `apt-get`. That means:<br>**Do use `sudo apt install PACKAGE`**<br>**Avoid `sudo apt-get install PACKAGE`**<br>Still, you may need to use `apt-get` for some specific cases (e.g., if a package provider instructs you to do so).
```

Instructions for installing particular and Debian-compatible software (e.g., QGIS) can be found directly on the website of software developers. For example, to install *Anaconda* *Python* visit [docs.anaconda.com](https://docs.anaconda.com/anaconda/install/linux/) and follow the installation instructions for Debian Linux.

```{attention}
If the main purpose of the VM is to run resource-intensive simulations (e.g., with TELEMAC-MASCARET), avoid installing any other software than those required for running the model. Also, as a general rule of thumb: Less is better than more.
```

### Add Package Repositories

For adding (trusted) software (package) repositories use *software-properties-common*, which provides the `add-apt-repository` command:

```
sudo apt install software-properties-common
sudo add-apt-repository contrib
sudo add-apt-repository non-free
sudo apt update
```

### Find Packages

Some software will run into errors because of missing library files (e.g., `libGLX.so.0: No such file or directory`). To find out what package needs to be installed for getting the missing library file, install *apt-file*

```
sudo apt install apt-file
sudo apt-file update
```

To find out the package name of a missing library file (e.g., `libGLX.so.0`), tap:

```
apt-file find libGLX.so.0
```

After a couple of seconds of searching, *apt-file* will prompt something like:

```
libglx0-glvnd-nvidia: /usr/lib/x86_64-linux-gnu/libGLX.so.0
```

That means, to get the library file `libGLX.so.0`, the package `libglx0-glvnd-nvidia` must be installed; for instance:

```
sudo apt install libglx0-glvnd-nvidia
```

### Install & Use *Windows* Applications in *Linux* (*Wine*) {#wine}

***Estimated duration: 10-15 minutes.***

If you want to emulate a *Windows* environment on any *Linux* system (for whatever reason), use the [*Wine*](https://wiki.debian.org/Wine) compatibility layer, which enables installing and running *Windows* applications. The above-described installation of Debian Linux creates a 64-bit VM and to enable program compatibility with 32-bit architectures, add 32-bit architectures through *Terminal*:

```
sudo dpkg --add-architecture i386 && sudo apt update
```

Then, install *Wine* with:

```
sudo apt install wine wine32 wine64 libwine libwine:i386 fonts-wine
```

After installing *Wine*, verify or configure folder links and compatibility environments by typing  `wine winecfg`, which opens the *Wine configuration* window, where:

* Folder links are defined in the *Desktop Integration* tab.
* The *Applications* tab enables to define the *Windows* compatibility layer to use (e.g., *Windows 10*) and set applications.

To install a *Windows* application:

1. Download the installer (e.g., an *exe* or *msi* file).
1. Open *Terminal* and type `wine control` > A *Windows*-like window opens ([read more](https://wiki.winehq.org/Control)).
1. In that window, click on the *Add/Remove...* button, which opens up another window (*Add/Remove Programs*).
1. Click on the *Install...* button and select the downloaded *exe* or *msi* installer.
    + Follow the installation instructions (standard *Windows* procedure).
    + Consider to add a *Desktop Icon*, or note the installation directory (e.g., `"C:\\Program Files (x86)\\CHC\\BlueKenue\\"`).
    + In the background. *Terminal* might prompt the message `err:mscoree:LoadLibraryShim error reading registry key for installroot` - you may ignore such messages ([read more](https://forum.winehq.org/viewtopic.php?t=14618)).

```{warning}
NEVER run wine as root (sudo). If you did anyway, do `cd $HOME` and tap `sudo chown -R $USER:$USER .wine`
```

**Launch a *Windows* application** by typing `wine explorer` in *Terminal*.  *Wine*'s *Windows* file system will be displayed in a *Windows*-like window. To start and application:

* If a *Desktop Icon* was created during the installation, go to *Desktop* and double-click on the application (e.g., *BlueKenue*)
* Otherwise, identify the installation path and the executable that launches the application.
    + 32-bit programs are typically installed in `"C:\\Program Files (x86)\\` (e.g., `"C:\\Program Files (x86)\\CHC\\BlueKenue\\BlueKenue.exe"`).
    + 64-bit programs are typically installed in `"C:\\Program Files\\`.
* With the installation path, any *Windows* application can be launched through *Terminal* with:
    + `wine "C:\\path\\to\\the.exe"` (use `\\` to separate sub-directories).
    + For example, `wine "C:\\Program Files (x86)\\CHC\\BlueKenue\\BlueKenue.exe"` typically starts *Blue Kenue<sup>TM</sup>*.

## Re-use (transfer or copy) a VM on another Host

Once you have created a VM on a virtual hard disk (the ***vdi*** file), you can always transfer it to another *host* system. To copy (or transport) a VM:

1. Copy the *vdi* file where your VM is installed (e.g., *Debian Linux.vdi*) to another system (let's call it *Host-2*), for example by using a USB flash drive.
1. Make sure that *VirtualBox* is installed on the *Host-2* system and open *VirtualBox* on  *Host-2*.
1. In *VirtualBox*, create a *New* (the blue rack-wheel) *Virtual Machine*.
1. In the process of creating a *New* VM, the wizard asks if you want to create a new hard disk image or an existing one. Select *Existing hard disk* and choose the copied *vdi* file.
1. Finalize the *New* VM wizard and start the VM as usual.
