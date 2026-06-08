---
description: Concepts d'apprentissage automatique supervisés pour les applications des ressources en eau, couvrant Perceptron, SVM, arbres de décision, réseaux neuraux, formations/essais et optimisation de l'espace hypothétique.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(supervisedlearning)=

# Apprentissage supervisé

Les algorithmes ML existants sont divers et leur applicabilité dépend de la tâche cible (ou *mapping*) à apprendre. Perceptron, Support Vector Machine, Pegasos, Decision trees, Random Forests, Neural Networks, sont tous des exemples d'algorithmes ML qui suivent une approche *supervised learning*, qui est au centre de cette section. Cette section a les objectifs suivants :

* Comprendre le concept global d'apprentissage automatique
* Comprendre les éléments de l'apprentissage supervisé

## Éléments de l'apprentissage supervisé

Dans l'apprentissage supervisé, on nous donne des exemples (c.-à-d. des mesures) ainsi que la solution cible (c.-à-d. des étiquettes) que nous souhaitons que le modèle ML apprend à cartographier. En revanche, dans les problèmes d'apprentissage non supervisés, on nous donne des exemples, mais on ne connaît pas la solution cible, ni les *étiquettes*. Un exemple typique de problème d'apprentissage non supervisé est le regroupement.

### Formation et essais
L'objectif d'un algorithme ML suivant une approche d'apprentissage supervisé est de trouver comment reproduire la solution cible à partir d'exemples *training*. Ainsi, un modèle ML est une fonction qui cartographie la solution cible à partir de l'ensemble des paramètres des exemples. Nous commençons par hypothéquer un ensemble de mappers (ou de fonctions) possibles qui prennent un ensemble de paramètres (ou *caractéristiques*) comme arguments/input pour produire les solutions cibles. Nous définissons ainsi l'espace *hypothèse* comme l'ensemble des modèles possibles (classificateurs, régresseurs). L'algorithme automatisera ensuite le processus de recherche des meilleurs paramètres *modèle* (c.-à-d. le meilleur modèle) qui sont en accord avec les paires d'étiquettes-exemples. Ceci est fait en optimisant le modèle sur les mains d'un ensemble de données de formation ($S$).

Notre cible machine est de trouver une règle in-to-output, qui est notée par une fonction mathématique $F(x)$, de sorte que:

  $$
	F(x) \rightarrow y
  $$
  
où $x$ sont nos attributs, également connus sous le nom de *features*, $y$ sont les étiquettes de dataset, les valeurs cibles que nous visons à cartographier.

Notre tâche est de trouver la meilleure hypothèse (ou le meilleur modèle) $h_{best}$ parmi les hypothèses $\mathcal{H}$. Nous le faisons en mettant à jour notre hypothèse à chaque fois que nous parcourons un certain nombre d'exemples de formation, calculant ainsi une hypothèse améliorée $h_{t+1}$ à partir de notre hypothèse actuelle $h_t$. Intuitivement, si $h_t$ mal classe une paire de formation particulière $(x_i, y_i) \in S $(dataset de formation), alors nous aimerions $h_{t+1}$ pour être comme $h_t$ mais nudgé vers le classement exact $(x_i, y_i)$. Pour rendre $h_t$ moins mauvais sur un exemple d'entraînement $(x_i, y_i)$, nous nudgerons $h_t$ dans un petit peu le long du négatif de la dérivée de la fonction d'optimisation ($\nabla C_t$). Cette méthode d'optimisation s'appelle Gradient Descent (GD), car nous utilisons le gradient de la fonction d'optimisation pour mettre à jour notre hypothèse vers une meilleure version.

Voici à quoi ressemblerait la mise à jour :

  $$
	\vec{h_{t+1}} = \vec{h_t} - \eta_t \cdot \nabla C_t 
  $$

où $\eta_t$ est le taux d'apprentissage*.

Notez que l'hypothèse (modèle) est ici un vecteur de paramètres du modèle (à ne pas confondre avec les caractéristiques), appelé aussi poids pour certains algorithmes *ML*.

### Fonction d'optimisation : Termes de perte et de régularisation

Le processus d'amélioration de notre hypothèse (ou modèle) consiste en un problème d'optimisation, où nous souhaitons minimiser une fonction d'optimisation ($C$). Intuitivement, nous aimerions minimiser les écarts entre les valeurs prévues et les valeurs réelles de $y$. Ces écarts sont exprimés en termes d'une fonction *loss* qui quantifie la performance de notre modèle à une paire d'exemples donnée. Dans le même temps, nous ne souhaitons pas que notre modèle minimise tant la fonction de perte, et donc est tellement adapté aux données de formation, au point qu'il ne s'applique plus à un tout nouveau jeu de données. C'est pourquoi nous introduisons un terme de régularisation qui vise à minimiser la complexité du modèle. Enfin, notre fonction d'optimisation serait :


  $$
	C(h_t) = \sum_{i}^{n} Loss_i + Regularizer 
  $$
  
	
où $n$ est le nombre d'exemples de formation.

Il y a quelques raisons pour lesquelles nous ne souhaitons pas trop adapter notre modèle à l'ensemble de données de formation. Premièrement, notre ensemble de données de formation peut contenir du bruit statistique que nous ne souhaitons pas capturer avec notre classificateur. La figure ci-dessous illustre le concept :

[surmonter à ML](https://elitedatascience.com/wp-content/uploads/2017/09/Overfitting-Data-Points.png)

Dans la figure, on peut clairement voir que la ligne verte est suradaptée aux points de données d'entraînement désignés par deux classes (points bleus et rouges). La ligne noire est probablement une limite de décision satisfaisante pour diviser les points rouges et bleus.

La deuxième raison pour laquelle nous ne voulons pas surpasser notre modèle est que, au cœur des problèmes d'apprentissage automatique, notre objectif est de pouvoir appliquer un modèle qui a appris d'un ensemble de données de formation aux données mondiales. Ainsi, nous souhaitons que notre modèle *généralise* ou applique correctement ce qui a été appris à un ensemble de données plus large et invisible. Pour vérifier si notre modèle fonctionne bien, il ne suffit pas de minimiser l'erreur d'entraînement. Nous devons tester les paramètres appris sur un ensemble de données invisible, ce qu'on appelle l'ensemble de données de test.


```{admonition} Keep in mind
:class: tip

Il est peu probable que notre modèle produise de meilleurs résultats dans les essais que dans les données de formation, mais il y a un scénario idéal que nous souhaitons réaliser, c'est-à-dire minimiser l'erreur de formation et de test. Nous aborderons ce sujet dans la section sur *la validation croisée*.
```


### Classification et régression

Plus généralement, un modèle ML peut être formé pour apprendre à prédire des catégories ou des valeurs continues. Dans ces deux approches, nous utiliserons les concepts ci-dessus pour construire un *classificateur* ou un *résistant*, respectivement. La principale différence sera dans la façon dont nous calculons l'erreur *formation* ou *perte*. Dans les prochaines sections, nous aborderons les deux problèmes dans une perspective d'apprentissage supervisé.