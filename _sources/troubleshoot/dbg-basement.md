# Debugging BASEMENT

Since its early development, *BASEMENT* has become a robust an reliable tool for the numerically modelling of rivers. Yet there are a few little challenges and this page provides some answers (under development).

(dbg-bm-xdmf)=
## Import of XDMF Model Output Fails


### XDMF error of wrong versions

Depending on the system environment, the header of `results.xmdf` may not be readable for QGIS. The two below tabs show the wrong and correct header lines. To fix the issue, open `results.xmdf` in a text editor (e.g., {ref}`Notepad++ <npp>` on Windows), replace the wrong with the correct header, and save the corrected `results.xmdf`.

`````{tab-set}
````{tab-item} Wrong header
```html
<?xml version="1.0"?>
<Xdmf Version="3.0">
```
````

````{tab-item} Correct header
```html
<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
```
````
`````

### XDMF error of wrong simulation directories
The `results.xdmf` contains geospatially explicit data (e.g., of flow velocity and water depth), which can be theoretically directly imported in *QGIS* with the *Crayfish* plugin (read more in the {ref}`BASEMENT post-processing <qgis-imp-steps>` section). However, there is a little issue: QGIS may crash because of an invalid directory. To fix it:

1. Open `results.xdmf` in a text editor (e.g., {ref}`Notepad++ <npp>` on Windows).
1. Use the find-and-replace tool (`CTRL` + `H` keys in Notepad++) to remove file paths before `results_aux.h5`.
    * Search the `results_aux.h5` string and identify the path written in front of it (e.g., `C:\temp\`).
    * Find and replace that user path, for example: `Find` = `C:\temp\results_aux.h5` and `Replace with` = `results_aux.h5`.
1. After having removed all path occurrences in the document, save and close `results.xdmf`.


This issue is also discussed in the [BASEMENT User Forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?id=5261)).
