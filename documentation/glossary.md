# Glossary

Using common and consistent vocabulary is vital for working in teams. This section exemplifies a glossary with technical terms recurring in this eBook.

```{glossary}
CFL
  In the field of hydrodynamics, the abbreviation CFL commonly refers to the **Courant-Friedrichs-Lewy** condition, which represents a convergence criterion for the numerical solution to the *Navier-Stokes* partial differential equations. The CFL applies to explicit time integration schemes that may become unstable for large time steps as a function of the size of mesh cells. Today, most numerical software uses an internal value for the CFL to adaptively calculate the maximum time step that is required for the stability of explicit solvers. In 2d modelling, the CFL condition is defined as $c_{CFL}={u_x + \Delta t}/\delta x + {u_y + \Delta t}/\delta y$, where $\Delta t$ is the time step, $\Delta x$ and $\Delta y$ are grid cell sizes in $x$ and $y$ directions of the coordinate reference system, and $u_x$ and $u_y$ are the flow velocities in the $x$ and $y$ directions. An explicit solver is assumed to be stable when $c_{CFL} \leq c_{CFL, crit}$, where the critical value $c_{CFL, crit}$ for the CFL condition must be smaller than 1.0. To this end, numerical modelling software, such as BASEMENT, uses a default value of $c_{CFL, crit} = 0.9$.

DEM
  A Digital Elevation Model (DEM) represents the bare Earth's topographic surface excluding objects such as buildings or trees. In contrast, a Digital Surface Model (DSM) includes objects such as trees or buildings. In addition, a Digital Terrain Model (DTM) represents similar data to a DEM and both DEM and DTM can be used synonymously in many regions of the world. However, in the United States, a DTM refers to a {ref}`Vector <vector>` (regularly spaced points) dataset while a DEM is a {ref}`raster` dataset. The translation into other languages does not go along with the same definition of a DEM, DSM, and DTM, and the following translations refer to the English definitions rather than the same (translated) words.

  *German for DSM: Digitales Höhenmodell (DHM) <br>French for DSM: Modèle numérique d'élévation (MNE)*

  *German for DEM: Digitales Oberflächenmodell (DOM) <br>French for DEM: Modèle numérique de terrain (MNT)*

  *German for DTM: Digitales Geländemodell (DGM) <br>French for DTM: Modèle numérique d'élévation (MNE)*

  Thus, there are many options for *correct* DEM-terminology depending on the region where you are. Now, what is the correct term in which language? There is no universal answer to this question and a good choice is to be patient with the communication partner.

GeoTIFF
  The Georeferenced Tag Image File Format (GeoTIFF) links geographic positions to {ref}`raster` images. A GeoTIFF involves multiple files containing the tagged image itself (`*.tif` file), a world file (`*.tfw` file) containing information about the geographic reference and projection system, and potentially an `*.ovr` file that links the GeoTIFF with other resource data. Read more at the *Open Geospatial Consortium*'s [standard for GeoTIFF](https://www.ogc.org/standards/geotiff).

Operating System
  An Operating System (OS) manages the hardware of a computer, software (resources), and services for any program you want to install.

  *German: Betriebssystem <br>French: Système d'exploitation*

Rich Text Format
  The proprietary Rich Text Format (RTF) wraps raw text in functional blocks that enable graphically flavored *Word*-like processors to identify document properties such as font size and type. Common RTFs are, for instance, *docx* or *odf* and enable exchanging text files between different *Word*-like processors on different operating systems.

SMS 2dm
  SMS (Surface-water Modeling System) is a proprietary software suite from *Aquaveo* for surface water modeling. `2dm` file format is natively produced with SMS and represents a computational grid with x, y, and z coordinates of nodes along with node ids. The [developer's wiki](https://www.xmswiki.com/wiki/SMS:2D_Mesh_Files_*.2dm) provides a comprehensive description of the file format.

Stage-discharge relation
  A stage-discharge relation (also referred to as **rating curve**) plots discharge (in m$^3$/s or CFS) as a function of water surface elevation function (in m above sea level or ft) at a specific river cross-section. Most stream gauging stations have a regularly calibrated stage-discharge relation that is often maintained by a state authority. This is why, it is mostly state authorities that provide stage-discharge functions for their gauging stations online, such as the state of Bavaria at the [Mühldorf am Inn gauge](https://www.hnd.bayern.de/pegel/donau_bis_passau/muehldorf-18004506/abflusstafel?).

STL
  The Standard Tessellation Language (STL) file format is native to a three-dimensional (3d) printing CAD software type called [stereolithography](https://en.wikipedia.org/wiki/Stereolithography). An STL file describes 3d structures in the form of unstructured triangulated surfaces with arbitrary units.

```
