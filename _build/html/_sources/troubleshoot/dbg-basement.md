# Debugging BASEMENT

Since its early development, *BASEMENT* has become a robust an reliable tool for the numerically modelling of rivers. Yet there are a few little challenges and this page provides some answers (under development).

## Export geospatial model output

The `results.xdmf` contains geospatially explicit data (e.g., of flow velocity and water depth), which can be theoretically directly imported in *QGIS* with the *Crayfish* plugin (read more in the [*BASEMENT* post-processing page](bm-post.html#qgis-imp-steps). However, there is a little issue: *QGIS* will crash because of an invalid directory. To fix it:

1. Open `results.xdmf` in a text editor (e.g., [*Notepad++*](https://notepad-plus-plus.org/downloads/)).
1. Use the find-and-replace tool (`CTRL` + `H` keys in *Notpad++*) to remove file paths before `results_aux.h5`.
    * Search the `results_aux.h5` string and identify the path written in front of it (e.g., `C:\temp\`).
    * Find and replace that user path, for example: `Find` = `C:\temp\results_aux.h5` and `Replace with` = `results_aux.h5` (see [below figure](#npp-xdmf-replace)).
1. After having removed all path occurrences in the document, save and close `results.xdmf`.

    <a name="npp-xdmf-replace"></a>
   ```{figure} ../img/npp-xdmf-replace.png
:alt: bmy

Find the string results_aux.h5 in results.xdmf and remove the file directories.
```

This issue is also discussed in the [*BASEMENT* User Forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?id=5261)).
