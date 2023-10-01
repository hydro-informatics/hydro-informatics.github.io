(chpt-telemac2d)=
# Telemac2d

Telemac2d iteratively solves the depth-averaged {term}`Navier-Stokes equations` (i.e., the {term}`Shallow water equations`). The Telemac2d tutorials in this eBook use the SELAFIN (`*.slf`) and Conlim boundary condition (`*.cli`) files that result from the {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>` and the descriptions refer to the {{ tm2d }}.

The {ref}`steady 2d <telemac2d-steady>` tutorial is the baseline for almost all other TELEMAC-related chapters in this eBook. On top, the {ref}`unsteady 2d <chpt-unsteady>` tutorial features the adaption of quasi-steady (near-census unsteady) flow conditions, which is important, for instance, for modeling a flood hydrograph.

Beyond hydrodynamic models, {term}`Sediment transport` (i.e., morphodynamics) can be modeled using the Gaia module in a TELEMAC simulation. The necessary coupling of hydrodynamics and morphodynamics is described in detail and in general for Selafin-based TELEMAC models in the {ref}`Gaia chapter <tm-gaia>`.
