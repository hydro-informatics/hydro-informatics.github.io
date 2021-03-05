---
title: Debugging TELEMAC/SALOME
tags: [telemac, troubleshooting]
keywords: basement, numerical modelling
sidebar: mydoc_sidebar
permalink: dbg_tm.html
folder: troubleshooting
---

Since its early development, *TELEMAC* has become a robust an reliable tool for the numerically modelling of open surface flows. Yet there are a few little challenges and this page provides some answers (under development).

## Traceback errors

If a simulation crashes and it is not clear why, debugging with [*gdb*](http://www.gdbtutorial.com) is a good option. To do so, first install *gdb*:

```
sudo apt install gdb
```

Then launch the steering file in debugging mode as follows:

```
telemac2d.py -w tmp simulation_file.cas --split
telemac2d.py -w tmp simulation_file.cas -x
cd tmp
gdb ./out_telemac2d
```

In *gdb* tap:

```
(gdb) run
```

To end *gdb* tap:
 
```
(gdb) quit
```

This approach also works with *Telemac3d* (and other modules).
 
## Errors in steering (CAS) files
 
* make sure to use `:` rather than `=`
* place all model files in the same folder and only use file names without the directories of files
 
 
## SALOME-HYDRO 
 
### SALOME-HYDRO not starting  (**Kernel/Session**) {#salome-dbg}

If an error message is raised by `Kernel/Session` in the `Naming Service` (typically ends up in `[Errno 3] No such process` ... `RuntimeError: Process NUMBER for Kernel/Session not found`), there are multiple possible origins that partially root in potentially hard-coded library versions of the installer. To troubleshoot:

* Manually create copies of newer libraries with names of older versions. For instance,
    + In the 4th line after running `./salome`, `Kernel/Session` may prompt `error while loading [...] libSOMETHING.so.20 cannot open [...] No such file or directory` 
    + Identify the version installed with `whereis libSOMETHING.so.20` (replace `libSOMETHING.so.20` with the missing library); for example, this may output `/usr/lib/x86_64-linux-gnu/libSOMETHING.so.40`
    + Create a copy of the newer library and rename the copy as needed by SALOME; for example, tap  `sudo cp /usr/lib/x86_64-linux-gnu/libSOMETHING.so.40 usr/lib/x86_64-linux-gnu/libSOMETHING.so.20`
    + Most likely, the following files need to be copied:
```
sudo cp /usr/lib/x86_64-linux-gnu/libmpi.so.40 /usr/lib/x86_64-linux-gnu/libmpi.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libicui18n.so.63 /usr/lib/x86_64-linux-gnu/libicui18n.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicuuc.so.63 /usr/lib/x86_64-linux-gnu/libicuuc.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicudata.so.63 /usr/lib/x86_64-linux-gnu/libicudata.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libnetcdf.so.13 /usr/lib/x86_64-linux-gnu/libnetcdf.so.11
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_java.so.40 /usr/lib/x86_64-linux-gnu/libmpi_java.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.40 /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.20
```

* Overwrite the SALOME-HYDRO's internal version of *Qt*:
    + Copy `/usr/lib/x86_64-linux-gnu/libQtCore.so.5`
    + Paste in `/Salome-V2_2/prerequisites/Qt-591/lib/` - confirm replacing `libQtCore.so.5`


### GUI/Qt5 support (GTK version compatibility) {#qt-dbg}

With the newer versions of the *Qt platform* any menu entry in *SALOME-HYDRO* will not show up. To fix this issue, install and configure `qt5ct` styles:

* `sudo apt install qt5-style-plugins libnlopt0`
* `sudo apt install qt5ct`
* Configure `qt5ct` (just tap `qt5ct` in *Terminal*)
    + Go to the *Appearance* tab
    + Set *Style* to `gtk2` and *Standard dialogs* to `GTK2`
    + Click on *Apply* and *OK*
* Open the file `~/.profile` (e.g. use the file browser, go to the `Home` folder and pressing `CTRL` + `H` to toggle viewing hidden files) and add at the very bottom of the file: 

```
export QT_STYLE_OVERRIDE=gtk2
export QT_QPA_PLATFORMTHEME=qt5ct
```

* Save and close `.profile` and reboot (or just re-login). 


{% include note.html content="If a file called `~/.bash_profile` (or `~/.bash_login`) exists, the above lines should be written to this `~/.bash_profile`/`~/.bash_login` because in this case, `.profile` will not be read when logging in." %}

Learn about *Qt* more at [archlinux.org](https://bbs.archlinux.org/viewtopic.php?id=214147&p=3) and in the [arch wiki](https://wiki.archlinux.org/index.php/Uniform_look_for_Qt_and_GTK_applications#QGtkStyle).