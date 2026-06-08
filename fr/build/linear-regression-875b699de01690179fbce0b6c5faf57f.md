---
description: régression linéaire pour prédire les variables continues dans l'ingénierie des ressources en eau, couvrant les paramètres du modèle, la descente en gradient, la régularisation et les erreurs structurales par rapport à l'estimation.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearregression)=
# Régression linéaire

Dans cette section, nous explorerons plus avant les concepts d'algorithmes ML linéaires, mais maintenant notre tâche sera de prédire les réponses en termes de valeurs continues, au lieu de classes discrètes comme nous l'avons fait en classification linéaire. En prenant l'application ML mentionnée dans l'introduction à ML](https://hydro-informatics.com/datascience/machinelearning.html), par exemple, nous pouvons maintenant vouloir prédire *combien* est la quantité d'une substance chimique dissoute dans l'eau, plutôt que simplement si elle est dissoute ou non (classification binaire).

```{admonition} Requirements
:class: warning
* Vous connaissez les termes d'apprentissage automatique. Nous vous recommandons de lire la section [introduction à ML](https://hydro-informatics.com/datascience/machinelearning.html) pour vous familiariser avec la nomenclature que nous utilisons dans tout le site Web.
* Vous connaissez les concepts fondamentaux de l'algèbre linéaire (comme un produit à point, des projections vectorielles, des plans, des vecteurs et des valeurs propres). Veuillez consulter les vidéos de [3Blue1Brown](https://youtu.be/kjBOesZCoqc) pour une révision appropriée si nécessaire.
* Connaissances de base en calcul différentiel (dérivation par la règle de la chaîne, gradients).
```

La régression linéaire se concentre sur la modélisation de la relation entre les variables d'entrée (caractéristiques) et une variable cible continue. Il suppose une relation linéaire entre les fonctionnalités d'entrée et la variable cible.

```{note}
Une relation linéaire est toute relation entre deux variables qui suit une ligne dans l'espace de coordonnées. En revanche, les relations non linéaires impliquent une non-proportionnalité entre les entrées et les sorties, qui peut être liée à des seuils, des boucles ou toute fonction qui ne suit pas l'équation d'une ligne ($y = a \cdot x + b$).
```

Ici encore, notre objectif est de trouver la ligne la mieux adaptée (ou hyperplane dans des dimensions plus élevées) qui minimise la différence entre les valeurs prévues et les valeurs cibles réelles. À cette fin, nous couvrirons :

* Le critère des moindres carrés pour quantifier l'erreur de formation en régression linéaire
* L'algorithme de descente du gradient stochastique (SDG), utilisé dans le processus d'entraînement d'un modèle de régression linéaire
* Terme de régularisation pour la régression linéaire
* Les sources d'erreur dans la régression linéaire


## Réduction des risques empiriques

### Fonction objective

Comme nous l'avons vu dans l'introduction à ML](https://hydro-informatics.com/datascience/machinelearning.html), le but de ML est de minimiser la fonction objective en ajustant les paramètres du modèle par des techniques (par exemple, des algorithmes d'optimisation) telles que la descente du gradient.

Une des fonctions objectives que nous pouvons utiliser en régression linéaire est *Risque empirique ($R$*). Nous exprimons le risque empirique en termes de mesure des pertes, qui ne reflète que l'écart entre les prévisions du modèle et les valeurs cibles (ou les étiquettes) de notre ensemble de données de formation, et ne tient donc pas compte de la régularisation. L'objectif de la minimisation empirique du risque ($R$) est de trouver un modèle qui minimise l'écart entre les prévisions et les observations sur les données de formation, en supposant qu'il généralisera bien les données invisibles. Ainsi, nous pouvons définir $R$ comme suit:

  $$
	R(\theta) = \frac{1}{n} \sum_{t=1}^n Loss(y^{(t)}-\theta \cdot x^{(t)})
  $$
où $n$ est le nombre d'exemples de formation, $(x^{(t)}, y^{(t)})$ est l'exemple de formation $t$-th (vectorielle et étiquette, respectivement), et $Loss$ est une fonction de perte générique. Notez que $\cdot§ indique un produit point.


```{important}
Notez également que dans notre définition du risque empirique ($R$) ci-dessus, nous ignorons le terme de partialité ($\theta_0$) pour plus de simplicité.
```

Une façon courante d'exprimer les écarts entre les prédictions et les observations sur les données de formation est de calculer l'erreur carrée, $(y^{(t)}-\theta \cdot x^{(t)})^2$, qui donne la fonction normale des moindres carrés (OLS) objectif:

  $$
	R(\theta) = \frac{1}{n} \sum_{t=1}^n (y^{(t)}-\theta \cdot x^{(t)})^2/2
  $$

```{note}
Les écarts entre les prédictions du modèle et les valeurs d'étiquette en tant que fonction de perte sont une pratique courante pour résoudre les problèmes d'optimisation en raison de sa simplicité, de sa différenciation et de son comportement convexe. Si les écarts sont en moyenne grands, la fonction d'erreur carrée pénalisera fortement notre modèle.
```

```{admonition} Know more
:class: seealso, dropdown

La mesure des écarts entre les prévisions du modèle et les valeurs d'étiquette à utiliser comme fonction de perte est une pratique courante dans les problèmes d'optimisation pour plusieurs raisons :
* Simplicité : Le quadrillage des écarts simplifie la formulation mathématique de la fonction perte. Il élimine la nécessité de considérer la direction de l'écart (positif ou négatif) et veille à ce que tous les écarts contribuent positivement à la perte. En outre, la quadrature préserve les belles propriétés mathématiques nécessaires à l'optimisation, comme être différentiable et convexe.
* Mettre l'accent sur les erreurs importantes : le quadrillage des écarts amplifie l'impact des erreurs plus importantes par rapport aux erreurs plus petites. En classant les écarts, la fonction de perte pénalise les écarts significatifs plus sévèrement, ce qui peut être souhaitable dans de nombreuses applications. Cet accent mis sur les erreurs importantes peut amener le processus d'optimisation à se concentrer sur la réduction des aberrations et l'amélioration de la précision globale.
* Différenciabilité : le quadrillage des écarts rend la fonction de perte différentiable, ce qui est crucial pour les algorithmes d'optimisation qui comptent sur les gradients pour mettre à jour les paramètres du modèle. La capacité de calculer les dérivés permet une optimisation efficace en utilisant des méthodes basées sur le gradient comme la descente du gradient ou la descente du gradient stochastique. Ces méthodes ajuster itérativement les paramètres du modèle dans la direction qui minimise la perte.
* Convexité: La perte carrée est une fonction convexe, ce qui signifie qu'elle a un minimum global unique. Convexity simplifie le processus d'optimisation car il garantit que la fonction de perte a une solution unique, et les algorithmes d'optimisation peuvent converger vers cette solution de manière fiable. Les fonctions de perte non convexes peuvent avoir plusieurs minima locaux, ce qui peut rendre l'optimisation plus difficile.

```


### Algorithme d'apprentissage

Maintenant, nous allons utiliser l'algorithme de descente de gradient stochastique (SDG) pour mettre à jour notre modèle $\theta$. Rappelons que nous le faisons en ajustant les paramètres du modèle $\theta$ avec le gradient de notre fonction objective, c'est-à-dire le risque empirique, évalué à chaque exemple de formation. Ainsi, nous renvoyons $\theta$ vers la direction opposée au gradient $\nabla_\theta R(\theta)$. Notez que la fonction $R$ ci-dessus, définie avec l'erreur carrée comme fonction de perte, est différentiable partout. Nous calculons le gradient du risque empirique, qui donne:

  $$
	\nabla_\theta R(\theta) = -(y^{(t)}-\theta \cdot x^{(t)}) \cdot x^{(t)}
  $$

Ainsi, nous pouvons résumer notre algorithme d'apprentissage comme suit:

1. Initialiser $\theta = 0$
2. Choisir aléatoirement $t = {1, ..., n}$
3. Mettre à jour $\theta$, de sorte que :
	
	$$
		\theta = \theta - \eta (- (y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}) \\
		\therefore \theta = \theta + \eta (y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}
	$$
où $\eta$ est le taux d'apprentissage.


Notez que cet algorithme d'apprentissage est très semblable à celui du classement linéaire.

````{admonition} Exercise 1: Difference between learning algorithms for regression and classification
:class: tip
Il y a une différence majeure entre cet algorithme d'apprentissage et celui que nous avons couvert pour former un classificateur linéaire. Tu peux le repérer ? Conseil: Regardez attentivement comment fonctionne la mise à jour de $\theta$ pour la régression linéaire.


```{admonition} Solution
:class: dropdown
L'algorithme d'apprentissage pour la régression linéaire est d'ajuster $\theta$ à chaque étape où il y avait une certaine différence ($y^{(t)}-\theta \cdot x^{(t)} \neq 0$). Ainsi, nous ne sommes pas préoccupés de savoir s'il y a une erreur ou non, que nous avons vérifié avec une clause ``if`` {ref}`linearclassification`, mais nous cherchons plutôt *combien* était la différence.
Si la prédiction et la valeur correcte s'écartent beaucoup, alors l'algorithme s'assurera de corriger $\theta$ plus fortement et, si les écarts sont faibles, l'algorithme corrigera moins.

```
````


## Régularisation : régression de la crête

### Fonction objective

Jusqu'à présent, notre problème d'optimisation pour la formation d'un modèle de régression linéaire ne vise qu'à minimiser l'erreur de formation (minimisation du risque empirique ou MCE). Cependant, un terme de régularisation est crucial dans la plupart des cas sinon notre modèle ne peut pas généraliser pour d'autres ensembles de données (en plus de l'ensemble de données de formation entre les mains). Ainsi, nous allons maintenant introduire un terme de régularisation à notre fonction objective, qui constitue maintenant un problème de régression *ridge*. La régression de la crête introduit un terme de régularisation, souvent appelé « pénalité de ridge » ou « pénalité de L2 » à la fonction objective ordinaire des moindres carrés (SLO). Ce terme de pénalité ($\frac{1}{2} \| \theta \|^2$) contrôle la complexité du modèle en rétrécissant $\theta$ (i.e., coefficients de régression) vers zéro. Ainsi, la fonction objective $J(\theta)$ pour la régression des crêtes est :

  $$
	J(\theta) = \frac{\lambda}{2} \| \theta \|^2 + R(\theta) 
  $$

où $\lambda$ est le paramètre de régularisation que nous avons couvert dans le {ref}`linearclassification`.

### Algorithme d'apprentissage

Comme nous l'avons fait dans la méthode Empirical Risk Minimization (ERM), nous pouvons également appliquer l'algorithme de descente stochastique dans la régression des crêtes, seulement maintenant nous devons prendre le gradient de la nouvelle fonction objective ($\nabla_\theta J(\theta)$) et l'utiliser pour mettre à jour $\theta$ à chaque itération à travers l'ensemble de données de formation.

D'abord élargissons tous les termes de $J(\theta)$:

  $$
	J (\theta)= \frac{\lambda}{2} \| \theta \|^2 + R (\theta) = \frac{\lambda}{2} \| \theta \|^2 + \frac{1}{n} \sum_{t=1}^n \frac{(y^{(t)}- \theta \cdot x^{(t)})^2}{2}  
  $$
  
	
Le gradient peut maintenant être calculé comme suit:

  $$
	\nabla_\theta J(\theta) = \lambda \theta - (y^{(t)}- \theta \cdot x^{(t)}) x^{(t)}
  $$
	
Ainsi, nous pouvons résumer notre algorithme d'apprentissage comme suit:

1. Initialiser $\theta = 0$
2. Choisir aléatoirement $t = {1, ..., n}$
3. Mettre à jour $\theta$, de sorte que :
	
	$$
		\theta = \theta - \eta (\lambda \theta - (y^{(t)} - \theta \cdot x^{(t)}) x^{(t)}) \\
	$$
où $\eta$ est le taux d'apprentissage.
	
	
````{admonition} Exercise 2: Simplify and understand the expression of the update of $\theta$ for ridge regression
:class: tip

Essayez de simplifier l'expression ci-dessus qui met à jour la valeur de $\theta$ à chaque itération. Conseil: Vous finirez avec une somme de deux termes. Qu'est-ce que chacun de ces termes essaie de réaliser pendant l'optimisation ?

```{admonition} Solution
:class: dropdown
Simplifier l'expression de mise à jour donne:

  $$
	\theta = (1 - \eta \lambda) \theta + \eta (y^{(t)} - \theta \cdot x^{(t)}) x^{(t)}
  $$

Le deuxième terme de l'expression, $(y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}$, est exactement ce que nous avions vu dans le MCE (avant d'ajouter la régularisation). Le premier terme, $(1-\eta \lambda)$, essaie de garder $\theta$ le plus près possible de zéro, puisque les deux $\lambda$ (terme de régularisation) et $\eta$ (taux d'apprentissage) sont des nombres positifs. Ainsi, le deuxième terme corrige nos paramètres de modèle $\theta$ pour minimiser la perte d'entraînement, alors que le premier terme essaie de garder $\theta$ le plus petit possible.
```
````

Notez qu'en ajoutant un terme de régularisation à notre fonction objective, nous sommes maintenant préoccupés par la recherche d'un modèle optimal qui, plutôt que d'adapter parfaitement les données de formation, est capable de généraliser aussi d'autres ensembles de données. Nous le faisons parce que nous croyons que le modèle ne devrait pas être adapté à chaque élément de preuve faible ou de bruit contenu dans l'ensemble de données de formation. Au lieu de cela, nous introduisons le paramètre de régularisation $\lambda$, ce qui évite les changements $\theta$, sauf lorsque les preuves sont suffisamment solides pour qu'une augmentation de $\theta$. Au fur et à mesure que la valeur de $\lambda$ augmente, l'erreur d'entraînement augmente, mais avec l'espoir que notre modèle généralisera mieux, donnant une erreur de test plus faible.

## Erreur structurelle par rapport à l'estimation

Lors de la sélection d'un algorithme ML, nous faisons certaines hypothèses sur la relation entre les caractéristiques et les étiquettes. Dans le cas de la régression linéaire, l'hypothèse est que la relation entre les caractéristiques et les étiquettes peut être représentée par une équation linéaire. Si cette hypothèse est violée, comme lorsque la vraie relation est non linéaire, alors notre modèle aura une grande *erreur structurelle* car il ne peut pas saisir avec précision les modèles sous-jacents dans les données. Ainsi, l'erreur structurelle englobe les limites ou hypothèses faites par le modèle choisi, et elle représente l'erreur irréductible qui ne peut être éliminée quelle que soit la quantité de données de formation. * L'erreur d'estimation* est due à la nature finie des données d'entraînement et à l'incapacité de notre modèle à s'adapter ou à généraliser à partir de ces données. Des erreurs d'estimation peuvent se produire lorsque les données de formation disponibles sont limitées ou ne représentent pas adéquatement la véritable distribution sous-jacente du problème. Dans de tels cas, le modèle peut avoir du mal à saisir les vrais modèles et relations présents dans les données, entraînant des erreurs d'estimation plus élevées.

`````{admonition} Exercise 3: Sources of error in linear regression
:class: tip
Lequel des chiffres ci-dessous illustre mieux les erreurs de structure et d'estimation, respectivement? Les points bleus indiquent l'ensemble de données d'entraînement et la ligne orange le modèle de régression linéaire.

````{figure} ../img/datascience/struc-vs-estimation-error.jpg
:alt: strucure versus estimation error
:name: truc-vs-est-errors

Exemple d'erreurs structurelles et d'estimation.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 3.
:header-rows: 1
:name: tab-ml-ex1-solutionx
* - Emplacement
- une
- b
* - Type d'erreur
- Structurel
- Estimation
```

````
`````

 
 
 
 
 