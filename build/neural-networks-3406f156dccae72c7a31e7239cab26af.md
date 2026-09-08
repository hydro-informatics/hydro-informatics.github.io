---
description: Supervised artificial neural networks for scientific computing, covering forward and back propagation, weight optimization, and scikit-learn implementations for water resources predictions.
---

```{admonition} Contributor
:class: tip
This chapter is being written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(neuralnetworks)=
# Neural Networks (Supervised)


The training process of artificial neural networks consists of not only finding best feature representations for our data, but also optimizing the model parameters (weights) toward a correct classification.

[Scikit-learn reference](https://scikit-learn.org/stable/modules/neural_networks_supervised.html).

## Forward propagation


Forward propagation is the process that ...

We sum the previous layer's output multiplied by the weight of each wire. Backpropagation works by using the partial derivatives of the cost function with respect to every weight or bias terms to transmit signal updates from the output layer to the input layer (thus backwards).
