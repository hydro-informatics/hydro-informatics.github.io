---
title: Other open source software resources
keywords: office, octave, matlab, .m file, texteditor
summary: "This page links to free tools and alternatives provided the open source community."
sidebar: mydoc_sidebar
permalink: hy_others.html
folder: get-started
---


## NotepadPlusPlus {#npp}
[*Notepad++*](https://notepad-plus-plus.org/) is an all-round text editor for basic coding (*R*, *Python*, *Java*, *C*, *Perl*, ...), markdown/html editing and many many (not a typo).

## Libre Office (Instead of MS Office) {#lo}
An office software such as [*LibreOffice*][libreoffice] or Microsoft's *Excel* is required for some of the analyses described on these pages.

## GNU Octave (instead of Matlab) {#octave}
*Matlab* is nowadays established as one of the leading tools in science and engineering. However, license fees and its proprietary nature limit the use of *Matlab* to privileged entities and users. Good news, there is a remedy in the shape of [*GNU Octave*](https://www.gnu.org/software/octave/). *GNU Octave* and *Matlab* use a similar syntax and `.m` files can be run with both programs. 
If error messages occur by running a `.m` file with *GNU Octave*, make sure to load relevant packages at the top of the script (this is one of the major differences between *GNU Octave* and *Matlab*). For example:

```
pkg load io
# ... some script with console output
pkg unload io
```

All stable *GNU Octave* packages can be found one their [website](https://octave.sourceforge.io/packages.php). To install one of these packages, open *GNU Octave* and type in the command window (the first line installs the package, the second line loads the package in the active session):

```
pkg install -forge new_package
pkg load new_package
```
 
 Afterwards, the new package can be loaded anytime by just typing in `pkg load new_package`. For example, the following code snippet installs and loads the `video` package:
 
 ```
pkg install -forge video
pkg load video
```



[libreoffice]: https://www.libreoffice.org/


