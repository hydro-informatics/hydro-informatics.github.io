# Other Software Resources

(npp)=
## NotepadPlusPlus (Text Editor)
[*Notepad++*](https://notepad-plus-plus.org/) is an all-round text editor for basic coding (*R*, *Python*, *Java*, *C*, *Perl*, ...), markdown/html editing and many many (not a typo) more. Alternatives for *Notepad++* are, for example, {ref}`install-atom` (cross-platform), [Vim](https://www.vim.org/) (Linux) or [GNU Emacs](https://www.gnu.org/software/emacs/) (Linux).

(lo)=
## Office Applications

Office applications greatly simplify everyday office life. However, the most popular application from Microsoft has a high price. Here are some free-to-use alternatives (for non-commercial use). Got no specific idea which software you want to use for non-commercial purposes? **Try Only Office!**

### Only Office

Only Office resembles MS Office a lot, it is very intuitive and enables cloud-based collaboration. It is free to use for non-commercial purposes and comes at an OK price for commercial purposes. On any Ubuntu Linux-based platform (e.g., Ubuntu, Mint, or Lubuntu), it is available through the software manager (or snap, flathub, or whatever you use...). Mint users find more information at [https://community.linuxmint.com](https://community.linuxmint.com/software/view/org.onlyoffice.desktopeditors).

For more installation options (e.g., for other Linux platforms, macOS, or Windows) visit the DesktopEditors section on [https://www.onlyoffice.com](https://www.onlyoffice.com/desktop.aspx).

```{admonition} Look for DesktopEditors to use Only Office for free
:class: tip

Make sure to follow the non-commercial desktop-use installation instructions on [https://www.onlyoffice.com](https://www.onlyoffice.com/desktop.aspx). Other versions are not for free.
```

### Libre Office

[LibreOffice][libreoffice] is completely free to use (see their [license terms](https://www.libreoffice.org/about-us/licenses)) and works on most popular platforms. However, it is less intuitive to use than, for instance, Only Office.

(octave)=
## GNU Octave (Matlab&reg; alternative)
*Matlab*&reg; is nowadays established as one of the leading tools in science and engineering. However, license fees and its proprietary nature limit the use of *Matlab*&reg; to privileged entities and users. The good news is that there is a remedy in the shape of [GNU Octave](https://www.gnu.org/software/octave/). *GNU Octave* and *Matlab*&reg; use very similar syntax and `.m` files can be run with both programs.
If error messages occur by running a `.m` file with *GNU Octave*, make sure to load relevant packages at the top of the script (this is one of the major differences between *GNU Octave* and *Matlab*&reg;). For example:

```
pkg load io
# ... some script with console output
pkg unload io
```

All stable *GNU Octave* packages can be found on their [website](https://octave.sourceforge.io/packages.php). To install one of these packages, open *GNU Octave* and type in the command window:

```
pkg install -forge new_package  # installs the package
pkg load new_package  # loads the package in the active session
```

 Afterward, the new package can be loaded anytime by just typing in `pkg load new_package`. For example, the following code snippet installs and loads the `video` package:

 ```
pkg install -forge video
pkg load video
```

```{tip}
*Python* provides comes with many more options for data processing and analyses. So instead of trying to tweak *Matlab*&reg; code, consider reading and using the *Python* tutorial with its {ref}`numpy` library descriptions. The tutorial also highlights the {ref}`differences between *Matlab*&reg; and *Python*'s *NumPy* <numpy-matlab>`) notation.
```


*MATLAB&reg; is a registered trademark of The MathWorks.*

[libreoffice]: https://www.libreoffice.org/
