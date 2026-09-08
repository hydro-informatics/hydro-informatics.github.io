---
description: Classification non linéaire avec les méthodes du noyau et Support Vector Machines (SVM) dans l'apprentissage automatique, couvrant la transformation des fonctionnalités et les astuces du noyau pour des limites de décision complexes.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(nonlinearclassification)=
# Amandes
 
Dans cette section, nous aborderons les concepts fondamentaux de classification non linéaire en introduisant le concept de noyaux. Tout d'abord, rappelons ce que nous avons vu jusqu'ici dans notre section sur {ref}`linearclassification`. Dans la classification linéaire, notre tâche consistait à classer les points de données à travers un hyperplan qui pourrait séparer linéairement l'ensemble de données dans l'espace de coordonnées des caractéristiques. Par exemple, dans un espace de fonctionnalités 3d, donc un vecteur de fonctionnalités comme $(x_1, x_2, x_3) \in \mathbb{R}^3 $, rappelez-vous que nos données sont considérées linéairement séparables s'il y a au moins un plan (pas une ligne) qui peut diviser les points. Contrairement à la classification linéaire, qui suppose une relation linéaire entre les caractéristiques d'entrée et les étiquettes de classe, les algorithmes de classification non linéaires utilisent diverses techniques pour saisir les modèles complexes et les limites de décision dans les données. En particulier, nous examinerons comment nous pouvons transformer nos données en un nouvel espace de coordination de dimension supérieure à travers *kernels*, qui nous aide à transformer le problème non linéaire en un problème linéaire.
 
Les noyaux nous permettent de transformer les données en un espace de caractéristiques de dimension supérieure où la séparation linéaire devient possible. Un exemple d'algorithme ML qui s'appuie sur des noyaux pour trouver le modèle complexe et les limites de décision dans les données est Support Vector Machine (SVM).


```{note}
D'autres algorithmes de classification non linéaires comprennent les arbres de décision, les forêts aléatoires, les voisins k-nearest (KNN) et les réseaux neuronaux. Ces algorithmes utilisent différentes techniques, allant de la kermisation à la modélisation et capturent des relations non linéaires entre les caractéristiques d'entrée et les étiquettes de classe, leur permettant de gérer des tâches de classification complexes.
```

## Transformation des caractéristiques

Nous allons maintenant voir comment la transformation des fonctionnalités fonctionne à travers un exemple 1d, c'est-à-dire, nous avons une fonctionnalité $x \in \mathbb{R}$. La figure ci-dessous illustre les points de formation ($n=3$).

Noter à partir de la figure que l'ensemble de données n'est pas séparable linéairement, du moins pas dans l'espace de caractéristique donné dans une dimension. Pour transformer ce problème en problème linéaire, nous pouvons effectuer une transformation de fonctionnalités ($\phi (x)$) pour rechercher une limite de décision dans un espace à dimension supérieure. Dans cet exemple particulier, notez que nous pouvons transformer la fonctionnalité 1d en un nouveau vecteur de fonctionnalités 2d, où la dimension supplémentaire peut être vue comme une sorte de nouvelle fonctionnalité.

  $$
    x \to \Phi(x) = [\Phi_1 \; \; \; \Phi_2] = [x \; \; \; x^2]
  $$

`````{tab-set}
````{tab-item} Original feature space 
```{figure} ../img/datascience/feat-transform-1.JPG
:height: 400px
:alt: initial problem before feature transformation
:name: feat-transform-1

1 : Formation des données dans l'espace initial.
```
````

````{tab-item} New feature space
```{figure} ../img/datascience/feat-transform-2.JPG
:height: 400px
:alt: problem after feature transformation
:name: feat-transform-2
:class: with-shadow

2: Formation de données dans le nouvel espace de fonctionnalités $\Phi(x)$.
```
````

````{tab-item} Decision boundary in the new feature space
```{figure} ../img/datascience/feat-transform-3.JPG
:height: 400px
:alt: decision boundary linearly separating the dataset in the new feature space
:name: feat-transform-3

3: Ensemble de données de formation et limite de décision dans le nouvel espace de fonctionnalités $\Phi(x)$
```
````
`````

En effectuant la transformation des fonctionnalités comme l'illustre l'étape 2 : formation des données dans le nouvel espace de fonctionnalités $\Phi(x)$ (voir figure ci-dessus), nous pouvons trouver un classificateur $h(x, \theta, \theta_o)$ avec une limite de décision définie par $\theta$ et le paramètre offset $\theta_0$ :

  $$
    h (x, \theta, \theta_0) = sign(\theta \cdot \Phi(x) + \theta_0)\\
	\therefore h (x, \theta, \theta_0) = sign(\theta_1 x + \theta_2 x^2 + \theta_0)
  $$


`````{admonition} Exercise 1: Feature transformation with kernels
:class: tip
La figure ci-dessous montre un ensemble de données qui n'est pas linéairement séparable dans l'espace d'origine $x = [x_1, x_2]$. Pouvez-vous penser à une fonction du noyau pour créer un espace de fonctionnalités plus haute dimension où il y a une limite de décision solvable par la classification linéaire ?

````{figure} ../img/datascience/exercise-1-kernels.jpg
:height: 400px
:alt: ex-kernels-1
:name: exercise-kernels-1

Exercice 1 sur les grains
````

````{admonition} Hint
:class: dropdown, important
Conseil: Les points sont clairement séparables par une circonférence dans l'espace d'origine $x \in \mathbb{R}^2$. Essayez maintenant de dessiner un espace de fonctionnalités en noyau $\Phi \in \mathbb{R}^3$.
````

````{admonition} Solution
:class: dropdown

Nous commençons à résoudre ce problème en rappelant l'équation d'une circonférence non centrée dans l'origine:

  $$
    (x_1+a)^2+(x_2+b)^2 = c
  $$
Nous obtenons :

  $$
    x_1^2 + 2 a x_1 + a^2 + x_2^2 + 2 b x_2 + b^2 -c = 0 \\
  $$
  
Les termes $a$, $b$ et $c$ sont des constantes, donc nous pouvons simplifier l'équation à:

  $$
    2 a x_1 + 2 b x_2 + x_1^2 + x_2^2 + C = 0 \\
  $$
où $C = (a^2 + b^2 - c)$.

Notez que l'équation ci-dessus indique notre limite de décision non linéaire dans l'espace d'origine $x \in \mathbb{R}^2$ et devrait donc égaler l'expression $\theta \cdot \Phi(x) +\theta_0$:

  $$
    \theta \cdot \Phi(x) + \theta_0 = x_1^2 + 2 a x_1 + x_2^2 + 2 b x_2  + C
  $$
  
ce qui signifie que $\theta_0 = C$, $\Phi(x) = [x_1 \;\; x_2 \;\; x_1^2 \;\; x_2^2]$, et donc nous pouvons également trouver $\theta$ en termes de paramètres de circonférence:

  $$
    \theta = [2a \;\; 2b \;\; 1 \;\; 1]
  $$

````
`````

## Plus bientôt...



