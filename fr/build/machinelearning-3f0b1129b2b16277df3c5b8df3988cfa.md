---
description: Introduction à l'apprentissage automatique pour la recherche sur les ressources en eau, couvrant l'apprentissage supervisé et non supervisé, les algorithmes ML, la formation des modèles et les applications en hydrologie et en écosystèmes fluviaux.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(machinelearning)=
# Présentation

L'apprentissage automatique est sans doute l'un des outils les plus importants de la science des données pour faire progresser la recherche sur les ressources en eau. Les modèles ML sont capables d'apprendre les relations sous-jacentes complexes d'un système, et trouvent ainsi ses applications dans divers sujets liés aux ressources en eau : des écosystèmes fluviaux à l'approvisionnement en eau. Nous couvrirons une variété d'algorithmes et de méthodes d'apprentissage pour optimiser les modèles ML afin qu'ils puissent généraliser à des données invisibles, qui comprendront en principe des techniques d'apprentissage supervisées et non supervisées.

## L'objectif de l'apprentissage automatique

L'apprentissage automatique vise à apprendre par calcul des relations complexes à partir de l'expérience (c'est-à-dire des données). *L'apprentissage informatique* est un sous-domaine de l'intelligence artificielle (IA) qui se concentre sur le développement de modèles qui permettent aux ordinateurs d'apprendre et de prendre des prédictions ou des décisions sans être programmés explicitement. Il s'agit de concevoir et de mettre en oeuvre des modèles mathématiques et statistiques qui permettent d'analyser automatiquement les données, d'identifier les modèles et de prendre des décisions ou des prévisions éclairées à partir des données observées. Cette tâche peut être, par exemple, la prédiction ou la modélisation de phénomènes complexes. Notez que la prédiction ici ne se réfère pas seulement à l'avenir, mais à tout événement non identifié. Par exemple, nous pouvons prédire si une substance chimique sera, ou a été, ou est dissoute dans l'eau compte tenu d'un ensemble de conditions environnementales.

Contrairement à la pensée populaire, les algorithmes ML existent depuis plusieurs décennies. Cependant, ils n'ont fait l'objet d'une attention particulière que dans la dernière décennie, lorsque les limites de la puissance de calcul n'ont plus été un obstacle à l'application des ML *algorithmes* pour faire des *modèles ML* utiles. Nous faisons référence à *algorithmes* comme commandes de base qui instruisent un modèle *comment apprendre* des données, alors qu'un modèle *ML* est le résultat (c'est-à-dire le programme appris) de l'apprentissage de la tâche cible à partir de l'ensemble de règles (*algorithmeML*) et d'exemples (c'est-à-dire des données).

## Types d'apprentissage automatique

Dans cette section, nous avons traité principalement des éléments de base de l'apprentissage supervisé, mais notons qu'il existe plusieurs autres types de problèmes de ML. Certaines d'entre elles sont:
* Apprentissage non supervisé : nous ne précisons aucun comportement correct (par exemple, les étiquettes). Nous avons ici quelques observations, mais la tâche elle-même n'est pas bien définie.
* Apprentissage semi-supervisé: nous pouvons spécifier certaines parties de notre modèle avec certaines étiquettes, mais d'autres parties doivent être apprises sans cible explicite. Par exemple, nous pouvons utiliser l'apprentissage non supervisé pour obtenir des grappes qui définissent les caractéristiques d'un problème d'apprentissage supervisé.
* Apprentissage actif: l'algorithme lui-même peut demander des exemples supplémentaires et utiles. Par exemple, apprenez à choisir seulement les exemples qui sont réellement nécessaires à l'apprentissage.
* Transférer l'apprentissage: quand une méthode est formée pour un scénario individuel et que vous souhaitez l'utiliser dans un scénario différent. Cela se traduit par: comment utiliser ce qui a été appris de A sur B?
* Apprentissage du renforcement : le modèle est formé à agir, plutôt qu'à prédire, et l'algorithme lui-même utilise les résultats de ses expériences comme rétroaction ou *renforcement* pour obtenir un résultat optimisé des actions (par exemple, un robot apprenant à marcher).

(data-science)=
## La différence entre l'apprentissage automatique et la science des données

La différence conceptuelle entre la science des données et l'apprentissage automatique peut être imaginée comme le concept de rectangles et de carrés en géométrie, où la science des données correspond à *rectangles* et l'apprentissage automatique à *carrés*. La science des données et l'apprentissage automatique traitent de la programmation (p. ex. en Python, R ou SQL), des statistiques et de la modélisation des données. La science des données englobe en outre la visualisation des données et la manipulation des données.

```{admonition} Recommended course
:class: tip

Gardez à l'esprit de chercher du matériel et d'étudier indépendamment pour votre apprentissage optimal. Par exemple, nous recommandons vivement le cours complet d'apprentissage automatique](https://www.edx.org/course/machine-learning-with-python-from-linear-models-to) offert par le MITx, l'initiative d'apprentissage en ligne de l'Institut de technologie du Massachusetts.
```

