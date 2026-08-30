---
description: Aperçu des conférences, exercices et cours vidéo en libre accès sur l'hydro-informatique, le Python, la modélisation numérique et l'analyse géospatiale à l'Université de Stuttgart.
---

# Conférences et exercices

## Conférences

La majorité des cours ont lieu devant un écran sous forme de vidéoconférences, de streaming vidéo, de documentation wiki ou d'exercices interactifs.
Pendant les périodes sans pandémie, des ordinateurs sont à la disposition des étudiants directement sur le campus de l'Université de Stuttgart. Cependant, pour améliorer les capacités de travail indépendantes, il est fortement recommandé que les étudiants apprennent à mettre en place un environnement de travail efficace sur un ordinateur portable ou un ordinateur de bureau.

```{tip}
Les étudiants de l'Université de Stuttgart voudront peut-être explorer le compte GitHub de TIK et se connecter à la page](https://github.tik.uni-stuttgart.de/login) (utiliser votre ID institutionnel, par exemple, `st9009133`) pour tirer parti du travail collaboratif avec le code.
```

Le chapitre {ref}`software` guide à travers l'installation de logiciels pertinents pour les conférences.

## Ouvrir les vidéos

Certains contenus de ce site sont accompagnés de vidéos publiques hébergées sur *YouTube*. Pour en savoir plus, visitez le canal YouTube [@hydroinformatique (Hydro-Morphodynamique)](https://www.youtube.com/@hydroinformatics).

## Exercices

Les exercices font partie intégrante de ce livre électronique et des matériaux supplémentaires sont fournis sur les dépôts git externes, tels que:

* les instructions d'affectation,
* modèles de code, et
* Fichiers de données.

Le lien vers le dépôt git de chaque exercice est fourni en haut de chaque page d'exercice.

(pywrm)=
## Programmation Python pour l'ingénierie et la recherche des ressources en eau

### À propos
Ce cours introduit le système de contrôle de version git et le langage de programmation Python 3. Les étudiants apprennent à utiliser les méthodes de programmation pour les tâches d'ingénierie, le traitement des données, y compris les évaluations statistiques de base, et les analyses géospatiales. Exercices axés sur la pratique avec petit guide de devoirs à travers la solution programmatique aux défis typiques dans l'ingénierie des ressources en eau et la recherche, comme les analyses écohydrauliques et le transport des sédiments. La communication entre des algorithmes efficaces et différents types de données (par exemple, les cahiers de travail *JSON* ou *xlsx*) fait également partie des conférences et des exercices. La dernière partie du cours introduit des méthodes de programmation géospatiale et des analyses de données.

Des conférences interactives familiarisent les étudiants avec le contrôle de version via git, langage de balisage pour la documentation et la programmation *Python*. Le cours est organisé par le département [IWS-LWW](https://www.iws.uni-stuttgart.de/en/lww/) à l'Université de Stuttgart](https://www.uni-stuttgart.de/) dans les semestres d'hiver pour le programme [Eau Resources Engineering and Management (WAREM)](https://www.warem.uni-stuttgart.de/). Le cours s'appuie sur des documents internes et externes à accès libre, qui servent de guide de référence et de soutien aux études indépendantes.


### Exigences

L'exigence primordiale est la volonté d'investir régulièrement du temps dans les conférences parce que ce cours ne se limite pas à passer un examen : les étudiants acquerront de nouvelles capacités.

Une expérience de programmation antérieure n'est pas nécessaire et le cours s'adresse aussi explicitement aux étudiants qui n'ont pas encore utilisé les outils de programmation.

Différentes solutions logicielles fonctionnent pour le cours et la section sur {ref}`sec-ide` guides à travers leur installation:

Installation minimale
: Tous les étudiants auront besoin d'un minimum de logiciels pour participer au cours. Le logiciel minimum implique:

  - {ref}`qgis-install`
  - Un éditeur de texte de base (toute solution fonctionne); *Les utilisateurs de Windows* peuvent vouloir utiliser {ref}`npp`.
  - *Les utilisateurs de Windows* devront également {ref}`dl`.
  - Un éditeur de fichiers de bureau de texte riche, comme {ref}`lo`, sera également très utile.

L'installation d'Anaconda permet l'utilisation de différents IDE qui utilisent des environnements *conda* pour Python. C'est l'option *all inclusive* en termes de fonctionnalité, mais elle est assez lourde en ce qui concerne le stockage et la consommation des ressources du système. Cette solution complète nécessite l'installation des éléments suivants:

  - Principalement {ref}`anaconda` avec ses interfaces *Anaconda Navigator* et *Anaconda Prompt*, ce qui facilite l'installation des IDE.
  - Soit {ref}`pycharm` (inteface externe) soit *Spyder* (directement disponible dans *Anaconda*) IDE.
  - Optionally {ref}`jupyter` for editing and running jupyter notebooks (alternatively, use the [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hydro-informatics/hydro-informatics.github.io/main?filepath=jupyter) buttons that enable running jupyter notebooks online)



### Objectifs d'apprentissage

Les étudiants acquièrent des compétences de base et avancées en programmation Python, contrôle de version git, traitement des données et analyses géospatiales. L'apprenant spécialisé approfondit la capacité de penser logiquement et de traduire les processus de travail en algorithmes structurés orientés objet. Grâce à l'application de logiciels à accès libre et de git, les étudiants pourront soutenir efficacement toute équipe dans le monde et stimuler tout projet. Les exercices axés sur la pratique permettent de transférer des connaissances supplémentaires sur la façon de relever les défis en matière de gestion des ressources en eau.

(irme)=
## Planification intégrée de la protection contre les inondations (IFP2)

### À propos


Les matériaux fournis ici appuient les travaux des laboratoires et du projet. Au-delà des descriptions fournies dans les documents ainsi que les laboratoires et les exercices, ces descriptions sont également disponibles ici pour faciliter le travail en ligne qui a gagné en importance en raison des événements récents.

### Exigences

Assurez-vous d'installer (ou d'avoir installé sur tout ordinateur accessible) les programmes suivants:

* {ref}QGIS <qgis-tutorial>` aide à visualiser et à modifier (édition) les ensembles de données géospatiales.
* {ref}`Notepad++ <npp>` pour modifier les conditions limites et les types de fichiers de données similaires.
* [ParaView](https://www.paraview.org/) est un outil de visualisation puissant pour les sorties de modèles (non obligatoire).
* {ref}`Libre Office <lo>` (ou tout autre logiciel) pour modifier les cahiers de travail (non obligatoire).


### Matériel en ligne

Le matériel fourni en ligne guide les exercices de simulation numérique. Les lignes directrices décrivent :

- Données de pré-processus: Du nuage de points aux maillages de calcul
- Configurer et exécuter une simulation numérique
- Résultats de simulation post-processus : Visualiser, comprendre et analyser la sortie du modèle.
- L'étalonnage et la validation font partie intégrante des études numériques.
