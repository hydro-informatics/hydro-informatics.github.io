---
description: Übersicht über Telemac2d Tutorials für Tiefengemittelte 2D hydrodynamische und morphodynamische Flusssimulationen mit Flachwassergleichungen, SELAFIN-Mesh-Format und GAIA-Kopplung.
---

(chpt-telemac2d)=
# Telemac2d

Telemac2d iteratively solves the depth-averaged {term}`Navier-Stokes-Gleichungen <Navier-Stokes equations>` (i.e., the {term}`Flachwassergleichungen <Shallow water equations>`). The Telemac2d tutorials in this eBook use the SELAFIN (`*.slf`) and Conlim boundary condition (`*.cli`) files that result from the {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>` and the descriptions refer to the [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).

Das {ref}`steady 2d <telemac2d-steady>` Tutorial ist die Basis für fast alle anderen TELEMAC-bezogenen Kapitel in diesem eBook. Darüber hinaus bietet das {ref}`unsteady 2d <chpt-unsteady>`-Tutorial die Anpassung quasistationärer (nahezu instationärer) Strömungsbedingungen, was zum Beispiel für die Modellierung eines Hochwasser-Hydragraphen wichtig ist.

Beyond hydrodynamic models, {term}`Sedimenttransport <Sediment transport>` (i.e., morphodynamics) can be modeled using the Gaia module in a TELEMAC simulation. The necessary coupling of hydrodynamics and morphodynamics is described in detail and in general for Selafin-based TELEMAC models in the {ref}`Gaia chapter <tm-gaia>`.
