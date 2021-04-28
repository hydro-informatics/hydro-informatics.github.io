# Numerical Models

Setting up a numerical model implemented in commercial or non-commercial codes may cause a lot of headache. This page features some basic principles to avoid problems with numerical models.



## Mesh generation and quality

The hints for meshing are extracted from [Olsen (1999)](http://folk.ntnu.no/nilsol/cfd/class2.pdf) and [Olsen (2012)](http://folk.ntnu.no/nilsol/tvm4155/flures6.pdf).

General:

* Mesh transition: Cells should not be smaller or larger than 50% or 200%, respectively of the size of neighbouring cells.
* Prefer triangular meshes over rectangular meshes (computational efficiency).


Triangular meshes:

* Avoid wide or acute triangles (optimum: equilateral triangles). No internal angle should be less than 22°.

Rectangular meshes:

* All internal angle should be close to 90°.
