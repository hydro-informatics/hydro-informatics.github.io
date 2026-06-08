---
description: Guide détaillé de la configuration de l'état des frontières et de l'analyse de la convergence de masse dans TELEMAC, couvrant les nombres de Froude, l'analyse des flux et les flux de travail pour la modélisation robuste de la rivière de conservation de masse.
---

(foc-mass-bc)=
# Limites et convergence de masse

La conservation de la masse et la définition des conditions limites vont de pair, car les limites liquides surdéterminées ou indûment limitées entraînent des masses d'eau ou de sédiments déséquilibrées, ou d'autres problèmes de calcul, tels que les débits supercritiques (résultant d'une forte {term}`Froude numbers <Froude number>`). Ce chapitre examine sous le capot des conditions limites, comment elles affectent le bilan massique, l'analyse de la convergence des flux et ce qui peut être fait pour obtenir un modèle numérique de Telemac robuste et respectueux de la masse. Un workflow ** complet pour la modélisation robuste est fourni à l'adresse {ref}`end of this chapter <tm-foc-mass-workflow>`**.

