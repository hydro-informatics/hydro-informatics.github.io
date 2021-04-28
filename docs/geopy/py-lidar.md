# LiDAR

## MARKDOWN FILE CONVERTED TO JUPYTER
Available at [https://github.com/sschwindt/lidar-analysis](https://github.com/sschwindt/lidar-analysis)

```{tip}
Use [*QGIS*](../get-started/geo.html#qgis) to display geospatial data products.
```

## Laspy

* [Documentation](https://laspy.readthedocs.io/en/latest/)
* [Tutorials](https://laspy.readthedocs.io/en/latest/tut_background.html)


### Install

Type in *Anaconda Prompt*:

```
conda install -c conda-forge laspy
```

Find advanced installation instructions on [laspy.readthedocs.io](https://laspy.readthedocs.io/en/latest/tut_part_1.html).

### Usage
*laspy* uses *numpy* arrays to store data and this is why both libraries need be imported to read a *las* file:

```python
import numpy
import laspy
file_name = "/path/to/file/vanilla-valley.las"
file_object = laspy.file.File("./path_to_file", mode="rw")
```


```python
import laspy

with laspy.file.File("./path_to_file", mode="rw") as las_file:
    pts = las_file.points

print(pts.dtype)
```

