---
description: Fondements de classification linéaire utilisant l'algorithme de Perceptron et classificateurs de marge avec régularisation pour les applications d'apprentissage automatique dans l'ingénierie des ressources en eau.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearclassification)=
# Classement linéaire

Dans cette section, nous aborderons les fondamentaux de la classification linéaire à travers un simple algorithme ML, le Perceptron. En outre, nous étendrons les concepts derrière l'algorithme de Perceptron en examinant des aspects de *régularisation* pour construire un classificateur linéaire de marge.

```{admonition} Requirements
:class: warning
* Vous connaissez les termes d'apprentissage automatique. Nous vous recommandons de lire notre [introduction à ML](https://hydro-informatics.com/datascience/machinelearning.html) section pour vous familiariser avec la nomenclature que nous utilisons dans tout le site Web.
* Vous connaissez les concepts fondamentaux de l'algèbre linéaire (comme un produit à point, des projections vectorielles, des plans, des vecteurs et des valeurs propres). Veuillez consulter les vidéos de [3Blue1Brown](https://youtu.be/kjBOesZCoqc) pour une révision appropriée si nécessaire.
* Connaissances de base en Python et calcul de tableau avec NumPy.
```


## Hyperplans

Supposons que nous souhaitions classer les objets positifs et négatifs à partir de l'ensemble de points d'entraînement ci-dessous (figure à gauche):

```{figure} ../img/datascience/decision-boundary.png
:alt: decisionbound
:name: cloud-points-ml

Ensemble de points de formation avec étiquettes binaires (+1, -1) et deux dimensions $(x_1, x_2)$ fonctionnalités. La limite de décision (ligne grise) est définie par le vecteur de paramètre $\theta$, qui est normal à la limite de décision, et le paramètre offset $\theta_0$ qui sépare linéairement les données.
```

L'ensemble de données ci-dessus est considéré linéairement séparable parce qu'il existe au moins une limite de décision linéaire capable de diviser correctement l'ensemble de données. Par exemple, nous pourrions passer une limite de décision comme la ligne grise au-dessus (figure à droite)


Dans ce cas, puisque les fonctionnalités $(x_1, x_2) \in \mathbb{R}^2 $, c'est-à-dire que l'ensemble de fonctionnalités appartient à l'espace bidimensionnel, la limite de décision constitue une ligne. Si nous avions affaire à un ensemble de caractéristiques dans l'espace tridimensionnel $(x_1, x_2, x_3)$, la limite de décision serait un plan. Pareillement, si notre ensemble de caractéristiques se trouvait dans un espace de dimension supérieure, la limite de décision constituerait un *hyperplan*.


Un hyperplan aux dimensions $d$ est habituellement indiqué par le vecteur normal du plan, $\theta \in \mathbb{R}^d$, et le paramètre offset (scalar) $\theta_0$. Dans l'exemple ci-dessus, nous définirions l'hyperplan (ou la limite de décision) comme suit :

  $$
	\theta \cdot X + \theta_0 =0 \equiv \begin{bmatrix} \theta_1 & \theta_2 \end{bmatrix} \cdot \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} + \theta_0 = 0
  $$


```{note}
Notez que $\theta$ contrôle l'orientation (pente, ou inclinaison) de la limite, alors que $\theta_0$ contrôle l'emplacement (ou l'offset, ou biais) de la limite. Ainsi, si $\theta_0 = 0$, alors la limite de décision franchit l'origine. $\theta_0$ est aussi souvent appelé le terme *bias*.
```
 
Notre classificateur $h(x, \theta, \theta_0)$ est donc égal à $sign(\theta \cdot X + \theta_0)$ où $\theta \in \mathbb{R}^2 $ et $\theta_0 \in \mathbb{R}$. Rappelez-vous que la fonction de signe, aussi appelée fonction de signe, est une fonction mathématique qui renvoie le signe ou la direction d'un nombre réel. C'est-à-dire que si le numéro d'entrée est positif, négatif ou 0, la fonction de signe retourne respectivement +1, -1 ou 0.
 
 
`````{admonition} Exercise 1
:class: tip
Essayez de savoir si la paire d'exemples de formation ci-dessous est linéairement séparable. Lesquels sont linéairement séparables par l'origine?

````{figure} ../img/datascience/exercise-decision-bound.png
:alt: ex-decision-bound
:name: exercise-db

Exercice 1 sur des exemples linéairement séparables.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 1.
:header-rows: 1
:name: tab-ml-ex1-solution

* - Ensemble de données
- une
- b
- c
- d
* - Linéairement séparable (LS)?
- Oui.
- Non.
- Oui.
- Non.
* - LS par origine?
- Non.
- Non.
- Oui.
- Non.

```
````
`````

## Algorithme de perceptron

Dans l'algorithme de perceptron, nous initialisons généralement $\theta$ comme zéro (vecteur zéro) et en boucle à travers la paire d'exemples de formation. À chaque itération, nous vérifierons si le classificateur fait une erreur en classifiant cet exemple de formation (i-ème exemple), et si oui, nous mettons à jour les paramètres de $\theta$.


Supposons que $\theta_0 =0$ pour la simplicité (la limite de décision doit passer par l'origine). Notre classificateur perceptron fera une erreur ``if`` $y^{(i)}(\theta \cdot x^{(i)}) \leq 0$. Nous mettrons alors à jour notre $\theta$ pour ne plus mal classifier cet exemple de formation. La façon de le faire est d'ajouter $y^{(i)}x^{(i)}$ à la précédente $\theta$. Ainsi, la mise à jour ressemblerait à:

  $$
	\theta = \theta + y^{(i)}x^{(i)}
  $$


````{admonition} Exercise 2: Understanding the perceptron update
:class: tip
Essayez de comprendre pourquoi cette mise à jour est utile. Conseil: remplacer l'expression pour les mises à jour $\theta$ dans le ``if`` vérifier.

```{admonition} Solution
:class: dropdown

Substituer l'expression pour la mise à jour $\theta$ pour vérifier si le classificateur fait toujours une erreur dans cet exemple:

  $$
	y^{(i)}(\theta + y^{(i)}x^{(i)})x^{(i)}
  $$
  
Nous initialisons $\theta$ comme zéro, donc l'expression est simplifiée pour:
 
  $$
    y^{(i)}(y^{(i)}x^{(i)})x^{(i)}
  $$
  
Comme tout temps d'étiquetage est égal à un (à la fois $1 * 1$ et $-1 * -1$ egal 1), l'expression se transforme en :

  $$
    x^{(i)}x^{(i)} = \| x^{(i)} \|^2 > 0 
  $$
  
Cela signifie que l'expression $y^{(i)}(\theta \cdot x^{(i)}) > 0$ (pas d'erreur). Ainsi, $\theta$ a été mis à jour afin qu'il ne mal classe plus l'exemple i-th.
```
````


Nous avons entre les mains un ensemble d'exemples de formation différents qui ont le potentiel de rafraîchir / mettre à jour notre classificateur dans de nombreuses directions. Ainsi, il est possible et même attendu que les derniers exemples de formation provoquent des mises à jour qui écraseront plus tôt, les mises à jour initiales. Il en résultera que les exemples précédents ne seront plus correctement classés. Pour cette raison, nous devons boucler l'ensemble de la formation ensemble multiple $T$ heures pour nous assurer que tous les exemples sont correctement classifiés. De telles itérations peuvent être effectuées dans l'ordre ou au hasard à partir des exemples de formation.

Nous pouvons coder l'algorithme comme suit:

```python
import numpy as np


# Algorithm always starting to loop from x1
def perceptron(X, y, theta, t_times):
    n_mistakes = 0

    # Initialize list to show the progress (updates) of theta
    progress_theta = []

    # Initialize an array with same size as the total number of examples to count how many mistake are made at each training example
    explicit_mistakes = np.zeros(shape=y.shape[0])

    # Loop through the training set T times
    for t in t_times:

        # Loop through the training examples in order
        for index, x in enumerate(X):

            # Check if the algorithm makes a mistake in the i-th (or index-th) example
            if y[index] * np.dot(theta, x) <= 0:
                # Update theta to no longer misclassify the i-th example
                theta = theta + y[index] * x

                # Save the update theta
                progress_theta.append(theta)

                # Update total number of mistakes
                n_mistakes += 1

                # Update total number of mistakes at the i-th training example
                explicit_mistakes[index] += 1
    print('The perceptron did {} mistakes until convergence'.format(n_mistakes))
    return progress_theta, n_mistakes, explicit_mistakes


if __name__ == '__main__':
    X = np.array([[-1, -1], [1, 0], [-1, 1.5]])
    # X = np.array([[-1, -1], [1, 0], [-1, 10]])

    y = np.array([1, -1, 1])

    t_times = range(0, 100)

    theta = np.array([-1, -1])

    a, b, c = perceptron(X, y, theta, t_times)
```

## Limites de la marge et perte de charnière

Comme vous l'avez peut-être remarqué, l'algorithme perceptron ne comporte aucun terme de régularisation. Le but était simplement de trouver toute limite de décision qui peut diviser les données correctement. Ici, nous introduirons le concept de *perte de marge* et de *limites de marge* pour transformer le problème d'apprentissage d'une limite de décision en un problème d'optimisation en tenant compte de la régularisation.

### Motivation derrière les limites de la marge

Jetons un coup d'oeil à notre ensemble de données de formation précédemment présenté (figure ci-dessous). Toute limite de décision à l'intérieur des lignes grises pointillées divise correctement les exemples d'entraînement. Cependant, intuitivement, nous aimerions favoriser une limite de décision qui peut maximiser les distances entre la limite de décision et les points d'entraînement. La raison de le faire est parce qu'il est probable que les points que nous souhaitons classer à l'avenir ont un bruit statistique, de sorte qu'une limite de décision trop proche des exemples de formation est plus susceptible de mal classer les versions légèrement modifiées (bruit) des exemples de formation. Par contre, un classificateur qui détient une marge relativement plus élevée entre la limite de décision et les exemples sera probablement plus efficace pour classer les données futures et invisibles.

```{figure} ../img/datascience/margin-bound.png
:alt: marginbound
:name: margin-bound

Ensemble de points d'entraînement avec étiquettes binaires (+1, -1) dans l'espace bidimensionnel $(x_1, x_2)$. Toute limite de décision à l'intérieur des lignes grises pointillées peut diviser correctement les données.
```

### Problème d'optimisation
Rappelons que notre objectif est de trouver un classificateur linéaire qui maximise les distances entre la limite de décision et les points d'entraînement (classificateur linéaire de marge), mais aussi minimise l'erreur d'entraînement. Il s'agit donc d'un problème d'optimisation qui doit contrebalancer ces deux facteurs, que l'on peut dire comme suit :

* Les marges (distances entre la limite de décision et les points d'entraînement) devraient être maximisées.
* L'erreur de formation doit être réduite au minimum. Nous l'exprimerons en termes de perte de poids.


### Limites de marge
Auparavant, nous avons vu que l'équation définissant une limite de décision satisfait $\theta \cdot X + \theta_0 =0$.

```{note}
Notez que selon $\theta \cdot X + \theta_0 =0$, tout point vivant exactement à l'avion serait mal classé.
```

Nous pouvons maintenant définir des limites de marge parallèles (ligne déchiquetée dans la figure précédente) comme suit:

  $$
	\theta \cdot X + \theta_0 = \pm 1
  $$

Notez que nous pouvons définir les limites comme ceci parce que nous avons un certain degré de liberté dans notre définition de la limite de décision, à savoir, l'ampleur du vecteur normal $\| \theta \|$. Autrement dit, quelle que soit la valeur $\| \theta \|$, notre limite de décision reste inchangée.


Rappelez-vous le problème du calcul de la [petite distance d'un point à un plan](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane). Cette distance est:

  $$
	\frac{\theta \cdot x^{(i)} + \theta_0 }{\| \theta \|}
  $$

Nous pouvons maintenant calculer la distance signée entre la limite de décision et le i-ième exemple comme suit:

  $$
	\gamma_i (\theta, \theta_0) = \frac{\theta \cdot x^{(i)} + \theta_0 }{\| \theta \|}
  $$

Ainsi, la distance entre les limites de la marge et la limite de décision est :

  $$
	\gamma_i (\theta, \theta_0) = \frac{1}{\| \theta \|}
  $$


### Perte de charnière

Nous savons jusqu'ici que $sign(\theta \cdot x^{(i)} + \theta_0 )$ classifiera l'exemple i-th. La façon de savoir si la classification est d'accord avec l'étiquette est de la multiplier par $y^{(i)}$. Nous pouvons exprimer cet accord également dans une version légèrement modifiée, en utilisant la perte de charnière:

  $$
	Loss_h(z)= \begin{cases} = 0 \;\; \mbox{if} \;\; z \geq 1 \\ =1-z \;\; \mbox{if} \;\;< 1\end{cases}
  $$

où $z$ est l'accord (distance signée de la limite de décision) $y^{(i)}(\theta \cdot x^{(i)}+\theta_0)$.

La figure ci-dessous illustre le fonctionnement de la perte de charnière le long de l'axe des z (distance par rapport à la limite):

<img src="https://www.researchgate.net/publication/341468721/figure/fig5/AS:963539095257091@1606737030212/The-margin-based-Hinge-loss-function.png" alt="hinge-loss-function" class="bg-primary mb-1" width="400px">


### Fonction objective

Donc maintenant nous pouvons créer une fonction objective qui (1) minimise la perte moyenne de la charnière par rapport aux exemples de formation, et (2) maximise $\frac{1}{\| \theta \|}$. Expression (2) peut également être reformulé pour minimiser $\frac{1}{2}\| \theta \|^2$. Ainsi, nous définissons la fonction objective comme suit:

  $$
	C(\theta, \theta_0) = \frac{1}{n}\sum_{i=1}^n Loss_h(y^{(i)}(\theta \cdot x^{(i)}+\theta_0)) + \frac{\lambda}{2} \| \theta \|^2
  $$
  
où $\lambda$ est le paramètre de régularisation qui équilibre l'importance de minimiser le terme de régularisation $\frac{\lambda}{2}\| \theta \|^2$ au coût de subir plus de pertes (augmentation du terme de perte). Vice versa, plus la valeur de $\lambda$ est faible, plus nous mettrons l'accent sur la réduction de la perte moyenne.

```{note}
Dans l'optimisation, l'objectif est généralement de minimiser la fonction objective, et c'est aussi la convention établie en ML, bien que la maximisation peut également être un objectif valide dans certains cas.
```


 
`````{admonition} Exercise 3: Understanding the influence of $\lambda$
:class: tip
Essayez de comprendre concrètement l'influence du paramètre $\lambda$ sur les limites de marge et de décision. Lequel des tracés montrant des limites de marge optimisées ci-dessous est le plus susceptible de correspondre à un $\lambda = 1, 10, \mbox{and} \;1000$

````{figure} ../img/datascience/exercise-lambda.png
:alt: lambdainfluence
:name: lambda-influence

Effet du paramètre de régularisation $\lambda$ sur la solution d'optimisation.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 3.
:header-rows: 1
:name: tab-ml-ex1-solution3

* - Emplacement
- une
- b
- c
* - Valeur Lambda
- 1
- 10
- 1000

```
````
`````
 
 
 
 
 