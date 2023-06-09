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

Many plugins for enriching Only Office are available on GitHub. To install them, download/clone the plugins (as zip file) from GitHub. Make sure to unzip the repository and package the following files and folders into one `.zip` file: `config.json`, `scripts/`, `pluginCode.js`, `licenses/`, `resources/`, `translations/`, `LICENSE`. Some of these files or directories might not be available in all plugin repos, which you may want to omit in these cases. Also, the `pluginCode.js` file might be hidden in the `scripts/` folder and if this is the case, copy the `.js` file (e.g., `scripts/pluginName.js`) into the head folder and rename it to `pluginCode.js`. Then rename the zip archive to `name.plugin` (replace the `name` of the plugin), open Only Office, go to the **Plugins** tab, **Settings**, and use the **Add** button to locate and add the plugin.


Here is a list of hydro-informatics.com's favorite plugins:

* [Word counter](https://www.onlyoffice.com/en/app-directory/word-counter) helps to count the number of characters, words, spaces, etc. Get it at [GitHub.com/ONLYOFFICE/plugin-wordscounter](https://github.com/ONLYOFFICE/plugin-wordscounter). The plugin is now also part of the standard installation
* [LanguageTool](https://www.onlyoffice.com/app-directory/languagetool) checks your writing in many languages, including spell and grammar checks. The plugin is based on the [LanguageTool](https://languagetool.org/) spell checker. Get it at [GitHub.com/ONLYOFFICE/plugin-languagetool](https://github.com/ONLYOFFICE/plugin-languagetool).
* [Draw.io](https://www.onlyoffice.com/blog/2022/03/onlyoffice-integrates-draw-io/) aids in creating professional diagrams and graphs for any Only Office document. Get it at [GitHub.com/ONLYOFFICE/plugin-drawio](https://github.com/ONLYOFFICE/plugin-drawio).
* [SDKJS](https://github.com/ONLYOFFICE/sdkjs-plugins) enables embedding (YouTube) videos, photo editing, graph generation with Draw.io, organization of lessons, and tweaks into a couple of translators ([read more](https://www.onlyoffice.com/blog/2022/08/best-onlyoffice-plugins-for-online-educators/)). Note: this plugin requires some more tweaking and you may prefer to install singular sdkjs plugins by searching them with your favorite search engine.


### Libre Office

[LibreOffice][libreoffice] is completely free to use (see their [license terms](https://www.libreoffice.org/about-us/licenses)) and works on most popular platforms. However, it is less intuitive to use than, for instance, Only Office.

(octave)=
## GNU Octave (Matlab&reg; alternative)
*Matlab*&reg; still is one of the leading tools in science and engineering. However, license fees and its proprietary nature limit the use of *Matlab*&reg; to privileged entities and users. The good news is that there is a remedy in the shape of [GNU Octave](https://www.gnu.org/software/octave/). *GNU Octave* and *Matlab*&reg; use very similar syntax and `.m` files can be run with both programs.
If error messages occur by running a `.m` file with GNU Octave, make sure to load relevant packages at the top of the script (this is one of the major differences between *GNU Octave* and *Matlab*&reg;). For example:

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
Python provides comes with many more options for data processing and analyses. So instead of trying to tweak `.m` code, consider reading and using the Python tutorial with its {ref}`numpy` library descriptions, which also highlights principal {ref}`differences between Matlab and Python's NumPy <numpy-matlab>`) notation.
```


*MATLAB&reg; is a registered trademark of The MathWorks.*

[libreoffice]: https://www.libreoffice.org/
