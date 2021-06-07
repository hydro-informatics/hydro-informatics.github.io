# Glossary

Using common and consistent vocabulary is vital for working in teams. This section exemplifies a glossary with technical terms recurring in this eBook.

```{glossary}
CFL
  In the field of hydrodynamics, the abbreviation CFL commonly refers to the **Courant-Friedrichs-Lewy** condition, which represents a convergence criterion for the numerical solution to the *Navier-Stokes* partial differential equations. The CFL applies to explicit time integration schemes that may become unstable for large time steps as a function of the size of mesh cells. Today, most numerical software uses an internal value for the CFL to adaptively calculate the maximum time step that is required for the stability of explicit solvers. In 2d modelling, the CFL condition is defined as $c_{cfl}={u_x + \Delta t}/\delta x + {u_y + \Delta t}/\delta y$, where $\Delta t$ is the time step, $\Delta x$ and $\Delta y$ are grid cell sizes in $x$ and $y$ directions of the coordinate reference system, and $u_x$ and $u_y$ are the flow velocities in the $x$ and $y$ directions. An explicit solver is assumed to be stable when $c_{cfl} \leq c_{cfl, crit}$, where the critical value $c_{cfl, crit}$ for the CFL condition must be smaller than 1.0. To this end, numerical modelling software, such as BASEMENT, uses a default value of $c_{cfl, crit} = 0.9$.

CSV
  The Comma-Separated Values (CSV) file format describes the structure of a text file storing simply structured data. The file name extension is `*.csv`, which may also contain Tab-Separated Values (TSV). The separator (i.e., comma, semicolon, or tab) sign delimits (or separates) colon values in one line of a `*.csv` file. Spreadsheet software, such as {ref}`Libre Office Calc <lo>`, enables to import and process `*.csv` files for cell-formula based data analyses.

DEM
  A Digital Elevation Model (DEM) represents the bare Earth's topographic surface excluding objects such as buildings or trees. In contrast, a Digital Surface Model (DSM) includes objects such as trees or buildings. In addition, a Digital Terrain Model (DTM) represents similar data to a DEM and both DEM and DTM can be used synonymously in many regions of the world. However, in the United States, a DTM refers to a {ref}`Vector <vector>` (regularly spaced points) dataset while a DEM is a {ref}`raster` dataset. The translation into other languages does not go along with the same definition of a DEM, DSM, and DTM, and the following translations refer to the English definitions rather than the same (translated) words.

  *French for DSM: Modèle numérique d'élévation (MNE) <br>German for DSM: Digitales Höhenmodell (DHM)*

  *French for DEM: Modèle numérique de terrain (MNT) <br>German for DEM: Digitales Oberflächenmodell (DOM)*

  *French for DTM: Modèle numérique d'élévation (MNE) <br>German for DTM: Digitales Geländemodell (DGM)*

  Thus, there are many options for *correct* DEM-terminology depending on the region where you are. Now, what is the correct term in which language? There is no universal answer to this question and a good choice is to be patient with the communication partner.

Echo sounder
  An echo sounder emits an acoustic signal under water, which is reflected by the objects of the underwater landscape. Echo sounding is an active {term}`Sonar` technique and enables the creation of an underwater DEM, which is also referred to as bathymetry. To perform echo sounding a probe must be installed on a boat that requires a minimum navigable water depth. In addition, the use of the echo sounder (probe) itself also requires a minimum water depth to operate with little noise inference. Therefore, by experience, a minimum water depth of 1-2 m is necessary to survey the bathymetry of a river by echo sounding.

  *French: Échosondeur / Sondeur acoustique <br>German: Echolot*

GeoTIFF
  The Georeferenced Tag Image File Format (GeoTIFF) links geographic positions to {ref}`raster` images. A GeoTIFF involves multiple files containing the tagged image itself (`*.tif` file), a world file (`*.tfw` file) containing information about the geographic reference and projection system, and potentially an `*.ovr` file that links the GeoTIFF with other resource data. Read more at the *Open Geospatial Consortium*'s [standard for GeoTIFF](https://www.ogc.org/standards/geotiff).

HDF
  The [Hierarchical Data Format (HDF)](https://www.hdfgroup.org/) provides the `*.h5` (HDF4) and `*.h5` (HDF5) file formats that store large datasets in an organized manner. HDF is often used with high-performance computing (HPC) applications, such as numerical models, to store large amounts of data output. This eBook impinges on HDF datasets in the {ref}`chpt-basement` tutorial where {term}`xdmf` files represent the model output, and in the {ref}`chpt-telemac` tutorials. In particular, TELEMAC builds on mesh and boundary files of the EnSim Core that is described in the user manual of the pre- and post-processing software [BlueKenue](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/2011_UserManual.pdf)<sup>TM</sup> (the newest [BlueKenue installer](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) contains an updated version of the user manual). Understanding the HDF format significantly facilitates troubleshooting structural errors of computational meshes for numerical models.

IAHR
  The International Association for Hydro-Environment Engineering and Research (IAHR) is an independent non-profit organization that unites professionals in the field of water resources. The IAHR has multiple branches and publishes several journals in collaboration with external publishing companies. Read more about the IAHR at [https://www.iahr.org](https://www.iahr.org).

Lidar
  Light Detection and Ranging (*LiDAR* or *lidar*) uses laser pulses to measure earth surface properties such as canopy or terrain elevation. The laser pulses are sent from a remote sensing platform (fix station or airborne) to surfaces, which reflect the pulses with different speed (time-of-flight informs about terrain elevation) and energy pattern (leaves behave differently than rock). In its raw form, lidar data is a point cloud with various, geo-referenced information about the reflected signal. Lidar point clouds for end users are typically stored in *las* format or compressed *laz* format. *las*-formatted data are much faster to process, but also much larger than *laz*-formatted data. For this reason, lidar data are preferably transferred in *laz* format, while the *las* format is preferably used for processing lidar data.

MPI
  In computing, MPI stands for *Message Passing Interface*, which is a portable message passing standard. MPI is implemented in many open-source C, C++, and Fortran applications to enable parallel computing.

Operating System
  An Operating System (OS) manages the hardware of a computer, software (resources), and services for any program you want to install.

  *French: Système d'exploitation <br>German: Betriebssystem*

Rich Text Format
  The proprietary Rich Text Format (RTF) wraps raw text in functional blocks that enable graphically flavored *Word*-like processors to identify document properties such as font size and type. Common RTFs are, for instance, *docx* or *odf* and enable exchanging text files between different *Word*-like processors on different operating systems.

SMS 2dm
  SMS (Surface-water Modeling System) is a proprietary software suite from *Aquaveo* for surface water modeling. `2dm` file format is natively produced with SMS and represents a computational grid with x, y, and z coordinates of nodes along with node ids. The [developer's wiki](https://www.xmswiki.com/wiki/SMS:2D_Mesh_Files_*.2dm) provides a comprehensive description of the file format.

Sonar
  Sound navigation and ranging (*Sonar*) is a technique for locating objects in space and underwater by emitting sound pulses. An active *Sonar* system, such as radio detecting and ranging (*radar*), emits and receives sound signals to map objects underwater (time-of-flight measurement). Passive *Sonar* detects signals emitted by an object itself (e.g., vibrations from fish motion or Whale chant), but cannot accurately map underwater objects.

Stage-discharge relation
  A stage-discharge relation (also referred to as **rating curve**) plots discharge (in m$^3$/s or CFS) as a function of water surface elevation function (in m above sea level or ft) at a specific river cross-section. Most stream gauging stations have a regularly calibrated stage-discharge relation that is often maintained by a state authority. This is why, it is mostly state authorities that provide stage-discharge functions for their gauging stations online, such as the state of Bavaria at the [Mühldorf am Inn gauge](https://www.hnd.bayern.de/pegel/donau_bis_passau/muehldorf-18004506/abflusstafel?).

STL
  The Standard Tessellation Language (STL) file format is native to a three-dimensional (3d) printing CAD software type called [stereolithography](https://en.wikipedia.org/wiki/Stereolithography). An STL file describes 3d structures in the form of unstructured triangulated surfaces with arbitrary units.

xdmf
  The [eXtensible Data Model and Format (XDMF)](https://www.xdmf.org/) library provides standard routines for exchanging (scientific) datasets that result from high performance computing (HPC) tasks. XDMF files redundantly store *light* and *heavy* data in XML and HDF5 format and *Python* interfaces exist for both formats. Thus, XDMF or XMF files are often linked to a `*.h4` or `*.h5` ({term}`HDF`) file that contains heavy simulation datasets.
```
