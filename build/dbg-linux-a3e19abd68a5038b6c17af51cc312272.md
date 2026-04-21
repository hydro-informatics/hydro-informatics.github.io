# Debug & Improve Experience

Debian Linux is documented in a comprehensive [wiki](https://wiki.debian.org/) with descriptions for setting up the system, installing software (packages), and tutorials for trouble shooting. This page provides guidance for problems that may occur in particular when Debian Linux is installed on a Virtual Machine (VM).

## Power management (battery life)

Working with Linux on a laptop often drains the battery quickly, especially when working with pure Debian. To increase power efficiency, consider installing lightweight Ubuntu (derivatives), that is **Mate** editions. Also, the following tool can help improve battery life on Ubuntu (derivatives):

```
sudo add-apt-repository ppa:linrunner/tlp 
sudo apt update 
sudo apt install tlp tlp-rdw 
```

Alternatively, [Fedora](https://fedoraproject.org/) or [Arch](https://archlinux.org/) are said to be power efficient. However, Arch can be difficult for Linux novices.


## Particular Problems

### Root Drive Is Running Out of Disk Space

```{tip}
Read this entire section before taking action. Otherwise, you risk to unnecessarily allocate disk space.
```

In general, keep the system clean after updating it through typing in *Terminal*:

```
sudo apt clean
sudo apt autoclean
sudo apt autoremove
sudo apt autoremove --purge
sudo apt autoremove
```

Subversion (SVN) repositories may also contain old and unnecessary chunks, which can be removed (e.g., from a local TELEMAC-MASCARET repository) with (the second argument is the SVN directory):

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
To revert undesired changes in the re-partitioning plan (before clicking on the apply-check mark), click on the yellow return arrow next to the green apply-check mark.
```


### Keep System and Software up to Date

Read more on the [developer's website](https://www.debian.org/doc/manuals/debian-faq/uptodate.en.html).


(dbg-permissions)=
### Permission Denied Messages

**Permission denied** messages may occur because of the fail-safe design of Debian, but denied read and write rights may quickly become annoying, in particular if you need to switch between normal and superuser accounts for installing software packages.

```{admonition} Potentially harmful operation
:class: warning
Never modify the access rights for folders in the `ROOT/` directory. Modifying permissions for folders such as `ROOT/etc/` or `ROOT/root/` may cause unrepairable system damage.
```

This is how to unlock all read and write rights for a directory:

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

Or for all sub-directories and files in these directories:

```
sudo chmod a+rwx /directory/*/*.*
```

This lifts all restrictions from a directory for all users, all its sub-folders and files contained (and sub-sub-folders and sub-sub-files contained, and so on) -- **this can be a very harmful irreversible operation when applied to system directories!**:

```
sudo chmod -R 777 /directory/
```

## Python

### tkinter Imports Fail (No Module Named Tkinter)

`tkinter` is sometimes still only installed for *Python2* on *Linux*, while we want to use it with *Python3*. To ensure that `tkinter` for *Python3* is installed, install via *Terminal*:

 * `sudo apt install python3-tk`  or
 * `sudo apt install python3.X-tk` (replace `X` with your *Python* version) or
 * `sudo apt install tk8.6-dev` to install the library only (this should be sufficient).

 If the above comments do not work, make sure that the `tkinter` repository is available to your system: `sudo add-apt-repository ppa:deadsnakes/ppa` (the repository address may change and depends on your *Linux* and *Python* versions).

## Wine (Windows Apps)

### General wine issues (reinstall)

If *wine* does not work as desired, remove the current installation via *Terminal*:

```bash
sudo apt remove wine wine32 wine64 libwine libwine:i386 fonts-wine
sudo apt remove --purge wine* 
sudo apt autoremove
```

Next, remove the wine prefix and any residual configuration files:

```bash
rm -rf ~/.wine
rm -rf ~/.local/share/applications/wine
``` 

Now, prepare the system for a clean wine installation. Specifically, Wine often needs 32-bit libraries even when creating a 64-bit prefix:

```bash
sudo dpkg --add-architecture i386
sudo apt update
```

If not yet done, add the latest stable Wine version to use the WineHQ repository. First, download and add the repository key:

```bash
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
```


Then, add the repository. For example, if your Linux Mint version is based on Ubuntu 20.04 (Focal):
```bash
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main'
sudo apt update
```

If your Linux Mint is based on a different Ubuntu release, adjust the repository accordingly.

````{admonition} Fix Key Storage DEPRECATION Warning

The warning message `https://dl.winehq.org/wine-builds/ubuntu/dists/focal/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.` can be fixed with the following workflow:

1. Download and save the WineHQ Key in a new location: Run the following command to download the key, dearmor it, and save it into the recommended location (e.g., `/usr/share/keyrings/winehq-archive.key`):

```bash
wget -qO- https://dl.winehq.org/wine-builds/winehq.key | gpg --dearmor | sudo tee /usr/share/keyrings/winehq-archive.key
```

This command fetches the key and converts it into a format apt can use directly.

2. Update the repository configuration

Modify the WineHQ repository entry to reference the new key file. This is typically found in a file like `/etc/apt/sources.list.d/winehq.list` (sometimes also in `/etc/apt/sources.list.d/additional-repositories.list` or `/etc/apt/sources.list` if added manually). Open the file to edit it with your preferred text editor. First, locate the line that looks similar to:

```bash
deb https://dl.winehq.org/wine-builds/ubuntu/ focal main
```

Second, modify it by adding the `signed-by` option so it reads:
```bash
deb [signed-by=/usr/share/keyrings/winehq-archive.key] https://dl.winehq.org/wine-builds/ubuntu/ focal main
```

Save the file and exit the editor.

3. Refresh the package lists: 

```bash
sudo apt update
```

If everything is configured correctly, the warning regarding the legacy trusted.gpg keyring should no longer appear.

````

Now install the stable Wine release:

```bash
sudo apt install --install-recommends winehq-stable
```

Also, consider to install Winetricks, which simplifies installing many runtime libraries and frameworks:
```bash
sudo apt install winetricks
```

### 64-bit Application Not Working

If a 64-bit *msi* or other installer / application is not working as desired, try to adapt the `WINEPREFIX`. First, remove any old prefix if necessary:

```bash
rm -rf ~/.wine
```
Then force Wine to create a 64‑bit prefix:
```bash
WINEARCH=win64 winecfg
```
The wine configuration window will appear. In the "Applications" tab, set the Windows version to **Windows 10**. Click **Apply** and **OK**.


### Installing the .NET Framework

Wine can use Winetricks to install various versions of the .NET Framework. Depending on the requirements of a Windows application, you might need a specific version. For example, to install .NET Framework 4.8, use Winetricks (see above) to create a new prefix:

```bash
WINEPREFIX=~/.wine winetricks dotnet48
```

The installation process can take a while and may require several restarts of Wine. Follow the on-screen instructions carefully.

Some users find that certain .NET versions install more reliably in a 32‑bit prefix—even when targeting Windows 10 apps. If you encounter issues, you may try creating a 32‑bit prefix by omitting the `WINEARCH=win64` environment variable (or explicitly using `WINEARCH=win32`). However, note that truly 64‑bit Windows applications require a 64‑bit environment.


## QGIS 

### GPG error - public key not available (APT UPDATE)

Occasionally (literally...), the GPG key of the QGIS repositories become invalid, which results in an error when using:

```
sudo apt update

[...]

W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: https://ubuntugis.qgis.org/ubuntugis focal InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY D155B8E6A419C5BE

W: Failed to fetch https://qgis.org/ubuntugis/dists/focal/InRelease  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY D155B8E6A419C5BE

[...]
```

To troubleshoot this error, note the unavailable key (i.e., `D155B8E6A419C5BE` in the above example) and then update the unavailable key:


```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D155B8E6A419C5BE
```

To test if the key update worked, tap `sudo apt update`

### No module named OpenGL 

If QGIS throws the error message `ModuleNotFoundError: No module named 'OpenGL'`, install *Mesa* as follows on Ubuntu (i.e., Debian Linux) based operating systems (including Mint and Lubuntu).

Bring `apt` and `pip` to up-to-date:

```
sudo apt update
python -m install --upgrade pip
```

Install the following system packages (if not yet done):

```
sudo apt install build-essential freeglut3 freeglut3-dev mesa-common-dev binutils-gold libglew-dev libglm-dev python-pyqt5
```

Install the following Python pip packages:

```
python -m pip install pyOpenGL
python -m pip install pyOpenGL_accelerate
python -m pip install PyQt5
python -m pip install PyQt5-sip
python -m pip install PyQtWebEngine
```

A system restart (or just reload the user environment with `source ~/.bashsrc`) may be necessary for QGIS to work now without the OpenGL error.


### LAStools

To get LAStools working in QGIS on Ubuntu (make sure to have {ref}`wine` installed):

* Download the LAStools (ZIP) from http://rapidlasso.com/LAStools and extract the ZIP file
* In QGIS, edit the processing options (Providers > Tools for LiDAR data):
  * LasTools folder: enter here the path to the folder that where the extracted ZIP files live (`/dir/to/LAStools/`)
  * Wine folder: enter the path to the {ref}`wine` binary (typically `/usr/bin/`). Alternatively, find where Wine lives with the `whereis wine` command
* If required: edit `LidarToolsAlgorithmProvider.py` (two files may exist):
    line 145:         if (True):
    line 168:         if (True):
    line 188:         if (True):

To troubleshoot a LAStools installation in QGIS read [this proposition on rapidlasso.com](https://rapidlasso.com/2013/09/29/how-to-install-lastools-toolbox-in-qgis/).

Read more about running [LAStools on Ubuntu](https://gis.stackexchange.com/questions/138149/wine-lastools-in-qgis-2-8-1-ubuntu-14-04).

## 3d Graphics Drivers

GPU intense software requiring strong graphics performance, such as the Unreal Engine, will require newest graphics cards and drivers. The default graphics drivers may not be able to satisfy the needs for such appliances. Latest releases of graphics drivers can be installed through proprietary drivers (e.g., nVidia's proprietary drivers to replace nouveau drivers).

Here is one option to update nVidia graphic drivers, though be aware that this action can substantially harm your system (it may not reboot) if you are not running an Ubuntu Linux (derivative) with an appropriate nVidia graphics card. So if you are OK with this warning:

* Open Terminal
* Find the appropriate driver for your system with `sudo apt search nvidia-driver`  (OR search for a driver package: `apt-cache search nvidia-driver`)
* Check latest driver releases
  * in nvidia drivers:

```
sudo apt-cache search 'nvidia-driver-' | grep '^nvidia-driver-[[:digit:]]*'
```

  * in dkms: 

```
sudo apt-cache search 'nvidia-dkms-' | grep '^nvidia-dkms-[[:digit:]]*'
```

```
[...]
nvidia-dkms-470 - NVIDIA DKMS package
nvidia-dkms-470-server - NVIDIA DKMS package
nvidia-dkms-495 - Transitional package for nvidia-dkms-510
nvidia-dkms-510 - NVIDIA DKMS package
nvidia-dkms-510-server - NVIDIA DKMS package
nvidia-dkms-515 - NVIDIA DKMS package
nvidia-dkms-515-server - NVIDIA DKMS package
```

  * in this example, the newest driver is `nvidia-driver-515` (with `nvidia-dkms-515`), which we note down to install them two steps later

* Update package information and your system:

```
sudo apt update
sudo apt full-upgrade
```

* Install the latest driver with: 
```
sudo apt install nvidia-driver-515 nvidia-dkms-515
```
* Reboot your system: 
```
sudo shutdown -r now
```
* Verify the installation in Terminal:
```
nvidia-smi
```

## Mac OS Apps (DMG file handling)

MacOS applications are often distributed as DMG files. Although Linux does not support DMG files natively, they can be converted to a mountable IMG file to then create an ISO image, which is easier to mount and work with on Linux.

### Convert the DMG to an IMG

First, install the `dmg2img` tool:

```bash
sudo apt install dmg2img
```

Convert the DMG file by running:

```bash
dmg2img /path/to/file.dmg
```

This command creates an IMG file with the same basename as the DMG, formatted with Apple's HFS+ filesystem.

### Mount the IMG file

Since the IMG file uses the HFS+ filesystem, load the following kernel module:

```bash
sudo modprobe hfsplus
```

Create a mount point (tpyically, in `/media`):

```bash
sudo mkdir -p /media/user/appname
```

Mount the IMG file using a loop device:

```bash
sudo mount -t hfsplus -o loop /path/to/file.img /media/user/appname
```

### Create an ISO from the mounted IMG

While it is possible to directly work with the mounted IMG, converting it to an ISO improves Linux compatibility. One way to do this is with Brasero, a graphical disc-burning tool for creating ISO images. Thus, first, install Brasero:

```bash
sudo apt install brasero
```

Then follow these steps:

1. **Launch Brasero** by opening it from the system menu (typically under **Sound & Video**) or search for it.
2. Start a new poject with a click on **Data project**.
3. **Add files** with a click on the plus icon (typically at the top left) and select the folder where the IMG file is mounted (`/media/user/appname`).
4. Click **Burn**, choose an output directory, and optionally change the output image name.
5. Click **Create Image** to generate the ISO file.

### Mount the ISO image

ISO images are natively supported by Ubuntu. To mount the new ISO:

1. **(Optional) load the HFS+ module:**  
   If the ISO still uses HFS+ (this is uncommon for standard ISO images), run:
   
   ```bash
   sudo modprobe hfsplus
   ```

2. **Create a mount point for the ISO:**

   ```bash
   sudo mkdir -p /media/user/appnameISO
   ```

3. **Mount the ISO:**  
   If the ISO uses HFS+, mount it with:

   ```bash
   sudo mount -t hfsplus -o loop /path/to/file.iso /media/user/appnameISO
   ```

   Otherwise, for a standard ISO 9660 filesystem, simply use:

   ```bash
   sudo mount -o loop /path/to/file.iso /media/user/appnameISO
   ```

Now, all the contents of the ISO (originally from the DMG/IMG) are accessible in the `/media/user/appnameISO` directory.


```{admonition} Uncertain filesystem and other ISO creation tools
:class: note

If you encounter issues or if the filesystem type is uncertain, you may want to try mounting without specifying a type to let Ubuntu auto-detect it.

There are also command-line tools (like `mkisofs` or `genisoimage`) available for ISO creation if you prefer a non-GUI approach.
```


### Launching the application from the mounted ISO

The contents of the mounted ISO can be explored to locate the application and launching it. Keep in mind that macOS applications are still not natively executable on Linux. A compatibility layer, such as [Darling](https://www.darlinghq.org/) may be needed.

####  Locate the application bundle

MacOS apps are typically packaged as `.app` bundles. Here is how to find them:

- **Browse the mounted directory:**  
  Open the file manager or use the terminal to navigate to the mount point (e.g., `/media/user/appnameISO`).

- **Identify the `.app` bundle:**  
  Look for directories ending with `.app` (for example, `MyApp.app`).

#### Find the executable inside the bundle

- **Open the app bundle:**  
  Inside the `.app` directory, navigate to the `Contents` folder.
  
- **Locate the Binary:**  
  Within `Contents`, the `MacOS` subdirectory typically stores the executable file. For isntance, the full path might be:
  ```
  /media/user/appnameISO/MyApp.app/Contents/MacOS/MyApp
  ```

#### Launch the Application

`````{tab-set}
````{tab-item} Use Darling (macOS Compatibility Layer)

Since macOS binaries do not run natively on Linux, one option is to use [Darling](https://www.darlinghq.org/), which provides a translation layer for macOS apps.

1. **Install Darling:**  
   Follow the instructions on the [Darling website](https://www.darlinghq.org/) to install it on the system.

2. **Launch a Darling shell and run the app:**

   ```bash
   darling shell
   cd /media/user/appnameISO/MyApp.app/Contents/MacOS
   ./MyApp
   ```

   Note that Darling still is experimental, so not all apps run flawlessly.
````

````{tab-item} Run a Cross-Platform App

If the app is written in a cross-platform language (like Java) or includes a launch script:

1. **Check for launch scripts or documentation:**  
   Sometimes the ISO will contain a README or a script (e.g., `launch.sh`) that explains how to run the app on Linux.

2. **Execute the script or command:**  
   Follow the provided instructions to launch the application.

````
`````

#### Verify and troubleshoot


If the app starts, its GUI should open up or there should be a confirmation message in Terminal.

f the application fails to launch, ensure that:
* the necessary compatibility layers (e.g., Darling) are installed.
* all required dependencies are available.
* you have permission to execute the file (you might need to run `chmod +x /path/to/executable`).


```{admonition} Read the docs!
:class: tip

Always consult any provided documentation in the ISO for application-specific instructions or additional dependencies. This can provide insight into whether the app is designed to run on macOS only or if a workaround exists for Linux.

```

