---
title: Virtual machines
tags: [telemac, numerical, linux, modelling, install, vm]
keywords: Virtual, machine, TELEMAC-MASCARET
summary: "Create a Debian Linux Virtual Machine (VM) with VirtualBox."
sidebar: mydoc_sidebar
permalink: vm.html
folder: get-started
---

Your computer is one of your important educational companions. So you want to protect the health of your computer and avoid problems caused by redundant or even malicious software. For this reason, it is recommended to install all software used on this website on a so-called Virtual Machine (VM). This page explains what VMs are, what advantages they have exactly, and how you can install [Debian Linux](https://www.debian.org/), one of the most stable and secure operating systems. It does not matter if you use Apple's *mac OS* or Microsoft's *Windows*, or if you already use Linux: The VM will look the same at the end.

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

The guest machine will run Debian Linux, which is one of the most stable Linux distributions and it is freely available. Because of its stability, Debian is an ideal baseline for running numerical simulations that may last for days or even weeks. Of course, there are other options and Debian is rather one of the best options than *the best option*.


## Create a Debian Linux VM

### Get prerequisites (required software)

***Estimated duration: 5-10 minutes.***

* Download and install the latest version of [VirtualBox](https://www.virtualbox.org/).
    + *Oracles*'s *VirtualBox* is a free and open-source hosted hypervisor software.
    + The installation of *VirtualBox* requires administrator rights on the host machine. So if you are working in a professional environment talk to your IT administrator.
    + *VirtualBox* installers are available for *Windows*, *mac OS*, and *Solaris*.
* Download the latest Debian Linux net installer:
    + Visit [debian.org](https://www.debian.org/)
    + In the *Getting Debian* section click on *CD/USB ISO images*
    + Click on [Download CD/DVD images using HTTP](https://www.debian.org/CD/http-ftp/)
    + Find the CD-section and click on the [*amd64*](https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/) version
    + Scroll to the bottom of the page and download the latest net installer (*debian-xx.x.x-amd64-netinst.iso*)

Remember where the *.iso* file is stored.
    
### Create a VM with *VirtualBox*

***Estimated duration: 5-8 minutes.***

In *Windows 10*, click on *Start*, type *Oracle VM VirtualBox* and hit enter. In the *VirtualBox* manager window:

* Click on the blue *New* button to open the VM creation wizard and enter:
    + *Name:* Debian Linux <br>*Note: The wizard should automatically recognize the* Type *and*Version *fields.*
    + *Machine Folder:* `C:\Users\USERNAME\VirtualBox VMs`
    + *Type:* Linux
    + *Version:* Debian (64-bit)  <br>> Click on the *Next* button
    + Allocate memory size: the more memory is allocated to the VM, the faster will be the VM (and for example TELEMAC-MASCARET), but the slower will be the host system (*Windows 10*). Rule of thumb: stay in the green range of the bar (e.g. allocate 8192 MB)
    <br>> Click on the *Next* button
    + Select *Create a virtual hard disk now* and click on the *Create* button.
    + Select *VDI* (native to *VirtualBox*) and click on *Next*.
    + Preferably choose *Dynamically allocated* to start with a small virtual disk size, which can take a maximum size to be defined in the next step. Click on the *Next* button.
    + Leave the default disk name as is and allocate a maximum size for the virtual disk (recommended: min. 32 GB). Click on the *Create* button.  
* Great - the basics are all set now and we are back in the *VirtualBox* main window, where a *Debian Linux* VM should be visible now on the left side of the window.
* With the *Debian Linux* VM highlighted (i.e., just click on it), click on the yellow *Settings* wheel-button, which opens the *Settings* window:
    + In the *System/Motherboard* tab, verify the memory allocation and check the *Enable EFI (special OSes only)* box (enable).
    + In the *System/Processor* tab, select the number of processors that the VM uses. For not slowing down the host system (*Windows 10*), stay in the green range of the CPU bar. For parallel processing with TELEMAC-MASCARET, allocate at least 4 CPUs. 
    + In the *Display* tab, check the *Enable 3D Acceleration* box.
    + In the *Storage* tab, find the *Controller: IDE*, where an *Empty* disk symbol should be located below. Click on the *Empty* disk symbol and find the *Attributes* frame on the right side of the window, where a small blue disk symbol should be visible. Click on the small blue disk symbol to *Choose a virtual disk file ...* > select the Debian Linux net installer (*debian-xx.x.x-amd64-netinst.iso*) that we downloaded before.
    + Click *OK*.

### Install Debian Linux

***Estimated duration: 30 minutes.***

To start the installation of Debian Linux, start the before created Debian Linux VM in the *VirtualBox* manager window (click on the *Debian Linux* VM and then on the green *Start* arrow). The *VirtualBox VM* window will ask for the *.iso* file to use (confirm the selected one), and start navigating through the installation:

* Inside the *VirtualBox VM* window select the *Graphical install* option.
* Navigate through the language options (recommended: English - English (United States)).
* Optionally define a hostname (e.g. debian-vm) and a domain name (e.g. debian-net).
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

Once the VM is shut down, re-open the VM *Settings* (from *VirtualBox Manager* window) and go to the *Storage* tab. Verify that there is again an *Empty* disk symbol in the *Controller: IDE* field.

### Setup Debian Linux {#setup-debian}

***Estimated duration: 15 minutes.***

Start the *Debian Linux* VM from the *VirtualBox* manager window. Once Debian Linux has started, log on with your user credentials.

To enable the full functionality of the system, open the Linux Terminal (`CTRL` + `Alt` + `T` or go to *Activities* > *Files* (filing cabinet symbol), right-click in any folder and select *Open in Terminal*). In *Terminal* type:

```
su
```

Enter the above-created password for the root user name (see installation section).

{% include note.html content="Root access (e.g. for installing software) is granted on many Linux distribution using the `sudo` command before the command to execute. In Debian Linux, `sudo` may refer to the wrong account and not work as desired. As a workaround use `su` in the *Terminal*. Alternatively, type `sudo usermod -a -G sudo YOUR-USER-NAME` in *Terminal* (after `su`)." %}

Install all packages required for building kernel modules:

```
apt update
apt install build-essential dkms linux-headers-$(uname -r)
```

Find the *Devices* drop-down menu of the *VirtualBox VM* window (not in Debian Linux itself) and select *Insert Guest Additions CD image...* (depending on the version of *VirtualBox*, this menu can be on the top or on the bottom of the window).

{% include tip.html content="The *VirtualBox VM* window does not show the menu with the *Devices* entry anywhere?
    + This may happen when the *View* was set to *Scaled mode*.
    + To toggle the view mode and make the menu bar visible, press the RIGHT `CTRL` (`Host`) key + the `C` on your keyboard, while being in the host system view." %}

{% include note.html content="If an error occurs ('The guest system has no CR-ROM ...'), shutdown the VM. In the *VirtualBox* manager window, right-click on the *Debian Linux* VM > *Storage* tab > Add new Optical Drive to *Controller: IDE*. Restart the *Debian Linux* VM." %}

Back in the Debian Linux *Terminal*, mount the *Guest Additions* *iso* file by typing (do not forget `su` if you needed to restart *Terminal*):

```
mkdir -p /mnt/cdrom
mount /dev/cdrom /mnt/cdrom
```

Navigate to the mounted directory and execute the *VBoxLinuxAdditions.run* file with the *--nox11* flag to avoid spawning an xterm window.

```
cd /mnt/cdrom
sh ./VBoxLinuxAdditions.run --nox11
```

The kernel modules will be installed now and *Terminal* should produce a message that invites to reboot the system. Do so by typing:

```
sudo shutdown -r now
```

After rebooting, make sure that the installation was successful. In *Terminal* type:

```
lsmod | grep vboxguest
``` 

If the *Terminal*'s answer is something like `vboxguest   358395 2 vboxsf`, the installation was successful. Read more about *Guest Additions* on the [*VirtualBox* developer's website](https://www.virtualbox.org/manual/ch04.html).

To improve the visual experience do the following: In the top-left corner of the Debian Linux Desktop, click on *Activities* and type *display* in the search box. Open the *Displays* settings to select a convenient display resolution. If you choose a too high resolution, the *VirtualBox VM* window will turn black and jump back to the original resolution after 15-30 seconds. Consider also to turn on *Night Light* to preserve your eye vision. *Apply* the changes and close the *Displays* settings.

### Familiarize with Debian Linux and Terminal {#terminal}

***Estimated duration: 60 minutes.***

To get familiar with Debian Linux, go to the *Activities* menu and find the applications *LibreOffice-Writer*, *Firefox*, the *Software* application (shopping bag symbol), and the *File* manager (filing container symbol).
Find more applications by clicking on the four dots on the left of the menu bar - can you find the Text Editor?
To shutdown Debian Linux (i.e., the VM), click on the top-right corner arrow and press the Power symbol.

The GNOME *Terminal* is one of the most important features, event though it optically shows only an empty window with a blinking cursor at the beginning. There a many ways to open *Terminal* and here are two options:

1. Go to *Applications* and type *Terminal* in the search box, or
1. Open the *File* browser (*Applications* > *Files* - the filing container symbol), navigate to the folder where you want to run *Terminal*, right-click in the free space and left-click on *Open in Terminal*.

*Terminal* runs many powerful native Linux (UNIX) commands, which is the most robust way to install and execute features. There are a couple of tutorials for learning to use *Terminal* and one of the most comprehensive is provided on the *Linux Ubuntu* website (Ubuntu is based on Debian Linux). It is highly recommended to go through the [tutorial provided by the Ubuntu community](https://ubuntu.com/tutorials/command-line-for-beginners) (*estimated duration: 51 minutes*), for better understanding some contents presented here on *hydro-informatics.github.io*. In particular, memorize the commands `cd` (change directory), `su`/`sudo` (superuser), `ls` (listen) and `mkdir` (make directory).


### Enable folder sharing

***Estimated duration: 5-10 minutes.***

Sharing data between the host system (e.g. *Windows 10*) and the guest system (Debian Linux VM) will be needed to transfer input and output files to and from the VM to the host system.

* At a place of your convenience, create a new folder on the host system (e.g. *Windows 10*) and call it shared (e.g. `C:\Users\USER\documents\shared\`).
* Start *VirtualBox* and the Debian Linux VM.<br>Make sure that the scaled view mode is off (toggle view modes with RIGHT `CTRL` (`Host`) key + the `C` on the keyboard).
* Go to the VM VirtualBox window's *Devices* menu, click on *Shared Folders* > *Shared Folders Settings...* and click on the little blue *Add new shared folder* symbol on the right side of the window (see figure below). Make the following settings in the pop-up window:
    + *Folder Path:* Select the just created `...\shared` folder
    + Check the *Enable Auto-mount* box
    + Check the *Make Permanent* box
* Click OK on both pop-up windows.

![share-folder](https://github.com/Ecohydraulics/media/raw/master/png/vm-share-folder.png)

The shared folder will then be visible in the *Files* (*Activities* > *Filing cabinet symbol*) on the left (e.g. as *sf_shared*). A reboot may be required.

{% include note.html content="File sharing only works with the *Guest Additions CD image* installed (see above section on setting up and familiarizing with Debian Linux)." %}

When trying to access the shared folder, a *Permission denied* message may appear. To grant access for your own account, add it to the *vboxsf* group. The *vboxsf* is the one automatically assigned for having access to the shared folder. To verify the group name, go to the shared folder, right-click in the free space, and select *Permissions*. A window with group names that have access to the shared folder opens. To add your own username type (in *Terminal*):

```
su
  ...password:

sudo usermod -a -G vboxsf YOUR-USER-NAME
```

Reboot the Debian Linux VM, and afterwards, test if you can access the folder, and create and modify files. 

### Install and Update Software (optional)

To install other software, preferably use the built-in software manager (*Activities* > *Shopping bag* symbol). The *Software* manager uses official releases in the stable Debian repository ([read more about lists of sources](https://wiki.debian.org/SourcesList)).

To update the repositories, open *Terminal* and type:

```
su
  ...password:

apt-get update
```

Instructions for installing particular and Debian-compatible software (e.g. QGIS) can be found directly on the website of software developers. For example, to install *Anaconda* *Python* visit [docs.anaconda.com](https://docs.anaconda.com/anaconda/install/linux/) and follow the instructions for Debian Linux.

{% include important.html content="If the main purpose of the VM is to run resource-intensive simulations (e.g. with TELEMAC-MASCARET), avoid installing any other software than those required for running the model. Also, as a general rule of thumb: Less is better than more." %}
