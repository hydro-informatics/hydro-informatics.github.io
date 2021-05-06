# Lectures and Eexercises

## Lectures

The majority of the courses take place in front of a screen in the form of video conferences, video streaming, wiki-like documentation, or interactive exercises.
During pandemic-free times, computers are available to students directly on campus at the University of Stuttgart. To improve independent work capacities, however, it is highly recommended that students learn to setup an efficient work environment an own laptop or desktop computer.

```{tip}
Students of the University of Stuttgart may want to explore the [TIK's GitHub account and login page](https://github.tik.uni-stuttgart.de/login) (use your institutional ID, for example, `st9009133`) to leverage collaborative work with code.
```

 The {ref}`software` chapter guides through the installation of relevant software for lectures.

## Exercises

Exercises are an integral part of this ebook and additional materials are provided on external git repositories, such as:

* Assignment instructions,
* Code templates, and
* Data files.

The link to every exercise's git repository is provided at the top of each exercise page.

(pywrm)=
## Python programming for Water Resources Engineering and Research

### About
This course introduces the version-control system git and the programming language Python 3. Students learn to use programming methods for engineering tasks, data processing including basic statistical evaluations, and geospatial analyses. Practice-oriented exercises with small homeworks guide through the programmatic solution to typical challenges in water resources engineering and research, such as ecohydraulic and sediment transport analyses. The communication between efficient algorithms and various data types (e.g., *JSON* or *xlsx* workbooks) is also part of the lectures and the exercises. The latter part of the course introduces geospatial programming methods and data analyses.

Interactive lectures familiarize students with version control via git, markdown language for documentation and *Python* programming. The course is organized by the [IWS-LWW department](https://www.iws.uni-stuttgart.de/en/lww/) at the [University of Stuttgart](https://www.uni-stuttgart.de/) in winter semesters for the [Water Resources Engineering and Management (WAREM)](https://www.warem.uni-stuttgart.de/) program. The course builds on in-house and external open access materials, which serve as a reference guide and support for independent studies.

```{attention}
To ensure adequate support for every student, the number of participants is limited to 15. For this reason, register as soon as possible on [ILIAS](https://ilias3.uni-stuttgart.de/goto_Uni_Stuttgart_crs_2101155.html) and [C@MPUS](https://campus.uni-stuttgart.de/cusonline/pl/ui/$ctx/wbLv.wbShowLVDetail?pStpSpNr=272592) (decisive is the registration on C@MPUS).
```

### Requirements

The paramount requirement is the willingness to regularly invest time in the lectures because this course is about more than just passing an exam: students will acquire new abilities.

Previous programming experience is not necessary and the course also and explicitly addresses students who have not yet made use of programming tools.

Different software solutions work for the course and the section on {ref}`sec-ide` guides through their installation:

Minimum installation
: All students will need a minimum of software to participate in the course. The minimum software involves:

  - {ref}`qgis-install`
  - A basic text editor (any solution works); *Windows* users may want to use {ref}`npp`; *Linux* users may prefer {ref}`install-atom`.
  - *Windows* users will also need to {ref}`dl`.
  - A rich text office file editor, such as {ref}`lo`, will also be very useful.

Solution 1: Full-stack Python Anaconda Installation
: The installation of Anaconda enables the usage of various IDEs that use so-called *conda* environments for Python. This is the *all-inclusive* option in terms of functionality, but it is quite heavy regarding storage and system resource consumption. This full-stack solution requires to install the following:

  - Primarily {ref}`anaconda` with its *Anaconda Navigator* and *Anaconda Prompt* interfaces, which facilitates the installation of IDEs.
  - Either {ref}`pycharm` (external inteface) or *Spyder* (directly available in *Anaconda* )IDE.
  - Optionally {ref}`jupyter` for editing and running jupyter notebooks (alternatively, use the [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hydro-informatics/hydro-informatics.github.io/main?filepath=jupyter) buttons that enable running jupyter notebooks online)

Solution 2: Atom
: At the core, *Atom* is a text editor, but i can easily extended with many capacities for alomost all popular programming languages.

### Schedule (Winter 2021/22)
Every Wednesday and Thursday morning live in *WebEx*, starting from October/November, 2021, through February, 2022.


```{note}
The exact schedule is available on the University of Stuttgart's [ILIAS](https://ilias3.uni-stuttgart.de/goto_Uni_Stuttgart_crs_2101155.html) and [C@MPUS](https://campus.uni-stuttgart.de/cusonline/pl/ui/$ctx/wbLv.wbShowLVDetail?pStpSpNr=272592&pSpracheNr=) pages.
```

### Learning objectives

Students acquire basic and advanced skills in Python programming, git version control, data handling and geospatial analyses. The dedicated learner deepens the ability to think logically and translate work processes into structured, object-oriented algorithms. Through the application of open-access software and git, students will be able to effectively support any team in the world and boost any project. The practice-oriented exercises transfer additional knowledge on how to leverage challenges in water resources management.

(irme)=
## Integrated River Engineering and Sediment Management

### About

This course is divided into two parts:
1. River Engineering and Sediment Management, and
1. Integrated Flood Protection Measures.

The materials provided here support the exercises in the Integrated Flood Protection Measures part, which encompasses socio-economic aspects of flood damage, calculation of floodwater depths, technical flood protection measures and design and operation of retention basins, among other things.

Beyond the descriptions provided in documents along with the exercises, these descriptions are also made available here to facilitate online work that has gained a rapidly increasing importance due to recent events.

### Requirements

Make sure to install (or having installed on any accessible computer) the following programs:

* [QGIS](../get-started/geo) aids to visualize and modify (edit) geospatial datasets. Add the [BASEmesh](bm-pre.html#get-ready-with-qgis) and [Crayfish](bm-post.html#add-the-crayfish-plugin) plugins.
* [Notepad++](hy_get-started/others.html#npp) to modify boundary conditions and text-alike data file types.
* [ParaView](bm-post.html#visualize-results-with-paraview) is a powerful visualization tool for model outputs (not mandatory).
* [Libre Office](hy_get-started/others.html#lo) (or any other software) to edit workbooks (not mandatory).


### Online materials

The provided online material guides through the numerical simulation exercise with the ETH Zurich's BASEMENT v.3. The guidance describes:

- Pre-process data: From point clouds to computational meshes
- Set up and run a numerical simulation with BASEMENT v.3
- Post-process simulation results: Visualize, understand and analyze the model output.
- Calibration & validation is here mentioned as an integral part of numerical studies.
