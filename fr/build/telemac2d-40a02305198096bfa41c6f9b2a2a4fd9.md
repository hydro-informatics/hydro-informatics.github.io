---
description: Aperçu des tutoriels Telemac2d pour les simulations de rivières hydrodynamiques et morphodynamiques 2D en moyenne de profondeur à l'aide d'équations d'eau peu profonde, du format du maillage SELAFIN et du couplage GAIA.
---

(chpt-telemac2d)=
# Télémac2d

Telemac2d résout la moyenne de profondeur {term}`Équations de Navier-Stokes <Navier-Stokes equations>` (c.-à-d. {term}`Équations <Shallow water equations>`). Les didacticiels Telemac2d de ce livre électronique utilisent les fichiers SELAFIN (`*.slf`) et Conlim (`*.cli`) qui résultent des fichiers {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>` et les descriptions se réfèrent au manuel [Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).

Le tutoriel {ref}`steady 2d <telemac2d-steady>` est le point de départ de presque tous les autres chapitres de ce livre électronique. En outre, le tutoriel {ref}`unsteady 2d <chpt-unsteady>` présente l'adaptation des conditions d'écoulement quasi stationnaires (près de census instables), ce qui est important, par exemple, pour modéliser un hydrographe d'inondation.

Au-delà des modèles hydrodynamiques, {term}`Transport solide <Sediment transport>` (i.e., morphodynamique) peut être modélisé en utilisant le module Gaia dans une simulation TELEMAC. Le couplage nécessaire de l'hydrodynamique et de la morphodynamique est décrit en détail et en général pour les modèles TELEMAC basés sur Selafin dans le {ref}`Gaia chapter <tm-gaia>`.
