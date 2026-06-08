---
description: Supervisé les réseaux neuronaux artificiels pour l'informatique scientifique, couvrant la propagation avant et arrière, l'optimisation du poids, et les applications scikit-apprendre pour les prévisions des ressources en eau.
---

```{admonition} Contributor
:class: tip
This chapter is being written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(neuralnetworks)=
# Réseaux neuronaux (supervisés)


Le processus de formation des réseaux neuronaux artificiels consiste non seulement à trouver les meilleures représentations de caractéristiques pour nos données, mais aussi à optimiser les paramètres du modèle (poids) vers une classification correcte.

[Scikat-learn reference](https://scikit-learn.org/stable/modules/neural_networks_supervised.html).

## Transmission vers l'avant


La propagation vers l'avant est le processus ...

Nous additionnons la sortie de la couche précédente multipliée par le poids de chaque fil. La rétropropagation fonctionne en utilisant les dérivés partiels de la fonction de coût par rapport à chaque terme de poids ou de biais pour transmettre des mises à jour de signal de la couche de sortie à la couche d'entrée (donc en arrière).
