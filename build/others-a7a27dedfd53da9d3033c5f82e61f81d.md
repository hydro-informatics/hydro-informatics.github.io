# Other Software Resources

(npp)=
## NotepadPlusPlus (Text Editor)
[Notepad++](https://notepad-plus-plus.org/) is an all-round text editor for basic coding (*R*, *Python*, *Java*, *C*, *Perl*, ...), markdown/html editing and many many (not a typo) more. Linux alternatives for Notepad++ are, for example, [Sublime text](https://www.sublimetext.com/) (proprietary), [Kate](https://kate-editor.org/) (cross-platform), or [Gedit](https://help.gnome.org/users/gedit/stable/) (simplistic).

(lo)=
## Office Applications

Office applications greatly simplify everyday office life. However, the most popular application from Microsoft has a high price. Here are some free-to-use alternatives.

### Libre Office

[LibreOffice][libreoffice] is completely free to use (see their [license terms](https://www.libreoffice.org/about-us/licenses)) and works on most popular platforms. Recent versions offer greatly improved user interfaces, with the ability to organize menus into tabs, similar to other office suites.

### Only Office

Only Office resembles MS Office a lot, it is very intuitive and enables cloud-based collaboration. It is free to use for non-commercial purposes and comes at an OK price for commercial purposes. On any Ubuntu Linux-based platform (e.g., Ubuntu, Mint, or Lubuntu), it is available through the software manager (or snap, flathub, or whatever you use...). Mint users find more information at [https://community.linuxmint.com](https://community.linuxmint.com/software/view/org.onlyoffice.desktopeditors).

For more installation options (e.g., for other Linux platforms, macOS, or Windows) visit the DesktopEditors section on [https://www.onlyoffice.com](https://www.onlyoffice.com/desktop.aspx).

```{admonition} Look for DesktopEditors to use Only Office for free
:class: tip

Make sure to follow the non-commercial desktop-use installation instructions on [https://www.onlyoffice.com](https://www.onlyoffice.com/desktop.aspx). Other versions are not for free.
```

Many plugins for enriching Only Office are available on GitHub. To install them, download/clone the plugins (as zip file) from GitHub. Make sure to unzip the repository and package the following files and folders into one `.zip` file: `config.json`, `scripts/`, `pluginCode.js`, `licenses/`, `resources/`, `translations/`, `LICENSE`. Some of these files or directories might not be available in all plugin repos, which you may want to omit in these cases. Also, the `pluginCode.js` file might be hidden in the `scripts/` folder and if this is the case, copy the `.js` file (e.g., `scripts/pluginName.js`) into the head folder and rename it to `pluginCode.js`. Then rename the zip archive to `name.plugin` (replace the `name` of the plugin), open Only Office, go to the **Plugins** tab, **Settings**, and use the **Add** button to locate and add the plugin.


Here is a list of useful plugins:

* [Word counter](https://www.onlyoffice.com/en/app-directory/word-counter) helps to count the number of characters, words, spaces, etc. Get it at [GitHub.com/ONLYOFFICE/plugin-wordscounter](https://github.com/ONLYOFFICE/plugin-wordscounter). The plugin is now also part of the standard installation
* [LanguageTool](https://www.onlyoffice.com/app-directory/languagetool) checks your writing in many languages, including spell and grammar checks. The plugin is based on the [LanguageTool](https://languagetool.org/) spell checker. Get it at [GitHub.com/ONLYOFFICE/plugin-languagetool](https://github.com/ONLYOFFICE/plugin-languagetool).
* [Draw.io](https://www.onlyoffice.com/blog/2022/03/onlyoffice-integrates-draw-io/) aids in creating professional diagrams and graphs for any Only Office document. Get it at [GitHub.com/ONLYOFFICE/plugin-drawio](https://github.com/ONLYOFFICE/plugin-drawio).
* [SDKJS](https://github.com/ONLYOFFICE/sdkjs-plugins) enables embedding (YouTube) videos, photo editing, graph generation with Draw.io, organization of lessons, and tweaks into a couple of translators ([read more](https://www.onlyoffice.com/blog/2022/08/best-onlyoffice-plugins-for-online-educators/)). Note: this plugin requires some more tweaking and you may prefer to install singular sdkjs plugins by searching them with your favorite search engine.

## PDF Annotations (Editing) with Xournal++

Xournal++ is a free note-taking software for annotating PDFs, sketching, and writing notes. It is a new version of the original Xournal project and has more features and a modern look. It can layer images, use different pens and highlighters, and import and export files in different formats. Its cross-platform compatibility makes it a powerful tool for students, researchers and professionals looking for a flexible digital note-taking solution. For example, Xournal++ facilitates note-taking on PDFs during meetings, lectures or conferences, and makes it easy to draw on pictures and make sketches.

Windows and MacOS users can find installation instructions at [https://xournalpp.github.io](https://xournalpp.github.io/). Debian/Ubuntu/Mint/Lubuntu (and similar) Linux users can install Xournal++ using

```
sudo apt install xournalpp
```

```{figure} ../img/software/xournalapp.png
:alt: xournal++ PDF image annotation editing
:name: xournalapp

Illustration of the Xournal++ app running on Linux Mint (dark scheme).
```


(install-tex)=
## LaTeX & TeXstudio

TeXStudio is a graphical editor designed to help you write and organize LaTeX code with features like syntax highlighting, spell checking, auto-completion, and an integrated viewer. In addition, a TeX distribution such as [TeX Live](https://tug.org/texlive/) (Linux preference) or [MiKTeX](https://miktex.org/) (Windows preference) is required, since these are the actual LaTeX compilers that provide the packages and fonts needed to transform a `.tex` source file into a PDF document. Both an editor (that is, TeXstudio) and a TeX distribution are required, because the editor alone cannot compile the code, and the distribution alone does not provide an integrated environment for writing and managing LaTeX documents. Therefore, before installing the graphical LaTeX editor, be sure to install a TeX distribution -- the LaTeX editor will try to find the installed TeX distribution during its own installation (next step).


`````{admonition} LaTeX package installation
:class: important

LaTeX packages are collections of additional commands, macros, and formatting instructions that extend the capabilities of the LaTeX system. Packages are typically introduced into a TeX document by including commands such as `\usepackage{...}` in the preamble of a `.tex` file. This allows authors to leverage specialized functionality, such as enhanced math notations, improved bibliography management, or particular typographic styles, without having to redefine or recode basic LaTeX commands. A TeX distribution comes bundled with a large set of commonly used packages and is often configured to retrieve more packages as needed. If a source file calls for a package that is not installed locally, the distribution can automatically download and install it from a central repository, ensuring that you have the resources required to compile the `.tex` file into a PDF document without manually searching and installing additional files.

````{tab-set}
```{tab-item} Linux (Debian)
Debian Linux users can simplify package installation by bulk installing all available TeX Live packages with `sudo apt install texlive-full`, although this will take up 3-4 GB of disk space.
```

```{tab-item} Windows

Windows users are advised to install MiKTeX using a standard user account rather than administrator privileges. Doing so allows MiKTeX to download and install new packages *on-the-fly* without repeatedly requesting system-wide permissions. If MiKTeX were installed by an administrator, any additional package installation would require elevated rights and prompt the user to authenticate as an administrator each time, a process that is both inconvenient and potentially less secure. Instead, performing a user-level installation ensures that MiKTeX can write packages directly into the current user directories. During the installation, select the user-only installation option and answer "No" when prompted about using administrator rights. After setup, open the MiKTeX settings panel and confirm that *on-the-fly* package installation is enabled.

```
````
````` 


[TeXstudio](https://www.texstudio.org/) is an open-source LaTeX editor available on both Windows and Linux. It can be installed on Windows by downloading the installer from the official website. Most Linux distributions provide TeXstudio through their package managers. After installation, opening TeXstudio represents a user-friendly interface that helps you create, edit, and manage LaTeX documents in one place. You can start a new document or open existing `.tex` files, use the integrated PDF viewer to check your compiled output, and run LaTeX or BibTeX tools directly from the toolbar or menu. For more detailed installation instructions, working with TeXstudio, and setting up LaTeX documents, please have a look at our LaTeX thesis template at [https://github.com/Ecohydraulics/latex-thesis-template](https://github.com/Ecohydraulics/latex-thesis-template). We also provide more tips in the *Science Life Hacks* section on {ref}`LaTeX <debug-tex>`.


(octave)=
## GNU Octave (Matlab&reg; alternative)
*Matlab*&reg; still is one of the leading tools in science and engineering. However, license fees and its proprietary nature limit the use of *Matlab*&reg; to privileged entities and users. The good news is that there is a remedy in the shape of [GNU Octave](https://www.gnu.org/software/octave/). *GNU Octave* and *Matlab*&reg; use very similar syntax and `.m` files can be run with both programs.
If error messages occur by running a `.m` file with GNU Octave, make sure to load relevant packages at the top of the script (this is one of the major differences between *GNU Octave* and *Matlab*&reg;). For example:

```
pkg load io
# ... some script with console output
pkg unload io
```

All stable *GNU Octave* packages can be found at [https://packages.octave.org](https://packages.octave.org). To install one of these packages, open *GNU Octave* and type in the command window:

```
pkg install "<package-link>"  # installs the package
pkg load <package-name>  # loads the package in the active session
```

 Afterward, the new package can be loaded anytime by just typing in `pkg load <package-name>`. For example, the following code snippet installs and loads the `statistics` package:

 ```
pkg install "https://github.com/gnu-octave/statistics/archive/refs/tags/release-1.6.6.tar.gz"
pkg load statistics
```

```{tip}
Python provides comes with many more options for data processing and analyses. So instead of trying to tweak `.m` code, consider reading and using the Python tutorial with its {ref}`numpy` library descriptions, which also highlights principal {ref}`differences between Matlab and Python's NumPy <numpy-matlab>`) notation.
```

*MATLAB&reg; is a registered trademark of The MathWorks.*


[Hydrop](https://bwsyncandshare.kit.edu/s/CjrWzDCfpemMQTg)


[libreoffice]: https://www.libreoffice.org/
