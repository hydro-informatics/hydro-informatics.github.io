---
description: Introduction à la programmation Python pour les ingénieurs de l'hydraulique et de l'éco-morphodynamique, couvrant JupyterLab, Binder et Google Colab pour la gestion interactive des carnets Python.
---

(about-python)=
# Premières étapes

<div style="text-align: center"><img src="https://www.python.org/static/img/python-logo.png"></div>

```{admonition} Watch this section and the Python tutorials in video formats
:class: tip, dropdown
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/Hcdizd-699I" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Watch this section as a video on the <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

## A propos de Python

[*Python*](https://www.python.org) est un langage de programmation flexible et populaire qui est facile à apprendre et peut être utilisé sur presque tous les [systèmes d'exploitation](https://en.wikipedia.org/wiki/Operating_system) tels que [*Linux*](https://www.linux.org/), *Windows* ou *macOS*. Une grande et forte communauté de développeurs fournit de nombreuses bibliothèques gratuitement, qui peuvent être installées et utilisées comme paquets dans *Python*. Outre l'ingénierie et l'analyse des données scientifiques, *Python* soutient également le développement d'applications et de services Web, d'applications de bureau (interfaces utilisateur graphiques - IGU), de scripts et de [*Jupyter notebooks*](https://jupyter.org/). *Python* est utilisé par de nombreuses institutions scientifiques et développeurs de logiciels, mais aussi de plus en plus dans d'autres industries. Ce tutoriel *Python* est adapté aux ingénieurs et aux scientifiques dans le domaine de l'hydraulique et de l'éco-morphodynamique.

Le contenu des pages suivantes est basé sur [Jupyter notebooks](https://jupyter.org/) et aromatisé avec des informations de [python.org](https://docs.python.org/3/tutorial/index.html). Les descriptions visent à fournir des connaissances solides pour l'utilisation efficace de *Python*.

```{admonition} Just one way to learn Python
:class: tip
Ce livre électronique est conçu pour fournir aux chercheurs et aux ingénieurs des ressources en eau une base pour l'automatisation des flux de travail basée sur Python. Pourtant, il y a toujours beaucoup de possibilités d'écrire du code avec beaucoup de gimmicks plus sophistiqués, qui ne sont pas tous listés et expliqués dans ce livre électronique.
```

(inline-jupyter)=
## Commencez par JupyterLab

Ce livre électronique s'appuie sur les carnets *Jupyter* qui sont liés à *mybinder.org*. Ainsi, il y a quelques options pour travailler avec les tutoriels suivants:

* Run the Jupyter notebooks in your webbrowser by clicking on the [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hydro-informatics/hydro-informatics.github.io/main?filepath=jupyter) buttons at the top of the every page. Clicking on the rocket button at the top of every page and on *Binder* has the same effect. Important: **this option does not enable saving your changes**.
* Le service de Google [Colab](https://colab.research.google.com/) permet également d'exécuter les carnets Jupyter à partir de ce livre électronique en ligne. Pour ouvrir l'un des cahiers Jupyter de cet eBook dans Google Colab, cliquez sur le bouton **rocket** en haut de la page et sur **Colab**. Si vous avez un compte avec google, vous pouvez également enregistrer vos modifications dans Google Drive.
* Run the Jupyter notebooks locally on your own computer by cloning [https://github.com/hydro-informatics/jupyter-python-course](https://github.com/hydro-informatics/jupyter-python-course): <b> `git clone https://github.com/hydro-informatics/jupyter-python-course.git`<b>
Notez que cette option nécessite une installation locale de {ref}`Jupyter (Lab) <jupyter>`.

