---
description: Übersicht über Telemac2d Tutorials für tiefgemittelte 2D hydrodynamische und morphodynamische Flusssimulationen mit flachen Wassergleichungen, SELAFIN-Netzformat und GAIA-Kopplung.
---

(chpt-telemac2d)=
# Telemac2d

Telemac2d löst iterativ die tiefe gemittelte {term}`Navier-Stokes equations` (d.h. die {term}`Shallow water equations`). Die Telemac2d Tutorials in diesem eBook verwenden die SELAFIN (`*.slf`) und Conlim Randbedingung (`*.cli`) Dateien, die aus den {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>` resultieren und die Beschreibungen beziehen sich auf die [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).

Das {ref}`steady 2d <telemac2d-steady>` tutorial ist die Basis für fast alle anderen TELEMAC-bezogenen Kapitel in diesem eBook. Darüber hinaus bietet das {ref}`unsteady 2d <chpt-unsteady>` Tutorial die Adaption von quasi-steady (near-census unsteady) Strömungsbedingungen, die beispielsweise für die Modellierung eines Flut-Hydrographen wichtig ist.

Neben hydrodynamischen Modellen kann {term}`Sediment transport` (d.h. morphodynamics) mit dem Gaia-Modul in einer TELEMAC-Simulation modelliert werden. Die notwendige Kopplung von Hydrodynamik und Morphodynamik ist im Detail und im Allgemeinen für Selafin-basierte TELEMAC Modelle in der {ref}`Gaia chapter <tm-gaia>` beschrieben.
