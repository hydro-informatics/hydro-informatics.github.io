---
description: Introduction à des modèles statistiques linéaires pour prédire et expliquer les variables hydrologiques, couvrant la régression linéaire simple et multiple et leurs hypothèses.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearmodels)=

# Modèles linéaires

Les modèles linéaires sont une classe de modèles statistiques qui visent à établir une relation linéaire entre une variable dépendante et une ou plusieurs variables indépendantes. Ces modèles supposent que la relation entre les variables peut être représentée par une ligne droite dans un espace multidimensionnel.

Dans un modèle de régression linéaire simple, il n'y a qu'une seule variable indépendante, alors que dans plusieurs modèles de régression linéaire, il y a plusieurs variables indépendantes. La variable dépendante, également appelée variable cible ou variable de réponse, est la variable que nous voulons prédire ou expliquer en fonction des variables indépendantes.

Les modèles linéaires ont plusieurs avantages. Ils sont relativement simples à comprendre et à interpréter, et ils fournissent des renseignements sur les relations entre les variables. De plus, les modèles linéaires sont efficaces par calcul et peuvent être appliqués à de grands ensembles de données. Cependant, les modèles linéaires supposent une relation linéaire entre les variables, ce qui peut ne pas être vrai dans tous les cas. Nous aborderons cette question en détail dans la section sur les erreurs de structure et d'estimation à {ref}`linearregression`. Ainsi, si la relation est non linéaire, d'autres techniques de modélisation peuvent être plus appropriées.