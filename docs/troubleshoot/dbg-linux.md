# Debugging Debian Linux

Debian Linux is documented in a comprehensive [Wiki](https://wiki.debian.org/) with descriptions for setting up the system, installing software (packages), and tutorials for trouble shooting. This page provides guidance for problems that may occur in particular when Debian Linux is installed on a Virtual Machine (VM). 

## Particular problems

### Root drive is running out of disk space

```{tip}
Read this entire section before taking action. Otherwise, you risk to unnecessarily allocate disk space.
```

In general, keep the system clean after updating it through typing in *Terminal*:

```
sudo apt-get clean
sudo apt-get autoclean
sudo apt-get autoremove
sudo apt-get autoremove --purge
sudo apt autoremove
```

Subversion (*SVN*) repositories may also contain old and unnecessary chunks, which can be removed (e.g., from a local TELEMAC-MASCARET repository) with (the second argument is the *SVN* directory):

```
svn cleanup ~/telemac/v8p1 --non-interactive
```

If the root partition of the virtual disk is running out of space, Debian prompts a warning message *Root drive is running out of disk space [...]*. There are many ways described for freeing up space through the deletion of obsolete or unnecessary packages, but this problem may occur even though only absolutely necessary packages are installed on a too small virtual disk.

In the case that the disk space limitation problem occurs on a virtual disk created with *VirtualBox*, open *VirtualBox*, highlight the VM subjected to the problem (e.g. *Debian Linux*). Make sure that the VM is off. In *VirtualBox* locate the *File* drop-down menu (top-left), click on it and open the *Virtual Media Manager*. Highlight the virtual disk where Debian Linux is installed and increase the *Size*. Click *Apply* and *Close* the *Virtual Media Manager*.

Increasing the virtual disk space alone is not sufficient, because the free disk space needs to be allocated to the root partition. To do so:
* Start Debian Linux (e.g. in *VirtualBox*, click on *Start*).
*Once Debian Linux started, go to *Activities* and type `gparted` in the search box. Find the *Gparted* software and click on it. If not yet installed, install and open *Gparted*.
* In *Gparted* look for the `ext4` partition (typically `/dev/sda2`) and highlight the partition directly behind that partition (typically `/dev/sda3`).
* Right-click on `/dev/sda3` (the partition behind the root partition) and click on *Swapoff*.
* Right-click again on `/dev/sda3` and click on *Resize/Move*.
    + In the *Free space preceding (MiB):* box, enter a reasonable size to free up disk space for the root partition (e.g., `2000`).
    + Make sure that the *New size* and *Free space following* boxes are coherent with the available disk space, in particular if you just increased the size of the virtual disk.
    + Click on *Resize/Move*.
* Right-click on the root partition (`/dev/sda2`) and click on *Resize/Move*.
    + Increase the partition size by the amount of disk space free-ed up from the following partition (e.g. increase `6667` MiB to `8667` MiB).
    + Make sure that there is no *Free space following* and that the field are coherent with the available space after the root partition.
    + Click on *Resize*.
* Find the green check mark in the top menu of *Gparted* and click on it. This action will apply the changes. Most likely, a warning message informs about possible problems when restarting the system with the new partition configuration (click OK - increasing the root disk is not problematic if it is at the cost of any empty partition).
* After repartitioning successful finished, right-click on the partition after the root partition (`/dev/sda3`) and make sure that it is again in *Swapoff* mode. If this is not the case (i.e., you cannot find *Swapoff* in the context menu and only *Swapon* is visible), click on *Swapon*.  

```{tip}
If you made undesired changes in the re-partitioning plan (before clicking on the apply-check mark), you can revert changes by clicking on the yellow return arrow next to the green apply-check mark.
```


### Keep system and software up to date

Read more on the [developer's website](https://www.debian.org/doc/manuals/debian-faq/uptodate.en.html).

### Permission denied messages

***Permission denied*** messages may occur because of the fail-safe design of Debian, but denied read and write rights may quickly become annoying, in particular if you need to switch between normal and superuser accounts for installing software packages.

This is how you can unlock all read and write rights for a directory:

```
sudo chmod a+rwx /directory
```

Or for all subdirectories:

```
sudo chmod a+rwx /directory/*
```

Or for all files in a directory:

```
sudo chmod a+rwx /directory/*.*
```

Or for all subdirectories and files in these directories:
```
sudo chmod a+rwx /directory/*/*.*
```

This lifts all restrictions from a directory for all users, all its sub-folders and files contained (and sub-sub-folders and sub-sub-files contained, and so on):

```
sudo chmod -R 777 /directory/
```

## Python 

### `tkinter` imports fail (no module named tkinter)

`tkinter` is sometimes still only installed for *Python2* on *Linux*, while we want to use it with *Python3*. To ensure that `tkinter` for *Python3* is installed, install via *Terminal:
 
 * `sudo apt-get install python3-tk`  or 
 * `sudo apt-get install python3.X-tk` (replace `X` with your *Python* version) or
 * `sudo apt install tk8.6-dev` to install the library only (this should be sufficient). 
 
 If the above comments do not work, make sure that the `tkinter` repository is available to your system: `sudo add-apt-repository ppa:deadsnakes/ppa` (the repository address may change and depends on your *Linux* and *Python* versions).
 
## Wine

### General wine issues
If *wine* does not work as desired, remove the current installation via *Terminal*:

```
sudo apt remove wine wine32 wine64 libwine libwine:i386 fonts-wine
```

Then `cd` to your *Downloads* folder, then pull the latest *Wine* packages, and add the repository to your `/etc/apt/sources.list` (the following sequences of commands does all of that - consider to adapt the `cd` to your *Downloads* folder):

```
cd $HOME/Downloads
sudo apt update
sudo apt -y install gnupg2 software-properties-common
wget -qO - https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add -
sudo apt-add-repository https://dl.winehq.org/wine-builds/debian/
```

Install *wine* *stable* and *development* (and staging) on *Debian 10.x*:

```
wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key | sudo apt-key add -    
echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list
sudo apt update
sudo apt install --install-recommends winehq-stable
sudo apt install --install-recommends winehq-devel
sudo apt install winehq-staging
```  

```{tip}
Add the above commands line-by-line (do not copy-paste entire code blocks).
```

### 64-bit application not working

If a 64-bit *msi* or other installer / application is not working as desired, try to adapt the `WINEPREFIX` for your user (note: this is not an elegant solution):

```
WINEARCH=win64 WINEPREFIX=/home/YOUR-USER-NAME/.wine64 wineboot -u
```
