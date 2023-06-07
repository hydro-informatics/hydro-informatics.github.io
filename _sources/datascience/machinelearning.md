```{admonition} Contributor
:class: tip
This chapter was written and developed by {{ negreiros }} <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(machinelearning)=

# Machine Learning (ML)

Machine learning (ML) is argually one of the most prominent tools in data science to advance water resources research. ML models are capable of learning complex underlying relationships of a system, and thus finds its applications in various water resources topics: from river ecosystems to water supply. We will cover a variety of learning algorithms and methods to optimize ML models so that they can generalize to unseen data, which will include in principle supervised and unsupervised learning techniques. 

## The goal of machine learning

Machine learning aims at computationally learning complex relationships from experience (i.e., data). *Computational learning* is a subfield of artificial intelligence (AI) that focuses on the development of models that enable computers to learn and make predictions or decisions without being explicitly programmed. It involves designing and implementing mathematical and statistical models that can automatically analyze data, identify patterns, and make informed decisions or predictions based on the observed data. This task may be, for instance, predicting or modelling complex phenomena. Note that predicting here does not refer only to the future but to any non-identified event. For instance, we can predict whether a chemical substance will be, or was, or is, dissolved in water given a set of environmental conditions.

Contrary to popular thinking, ML algorithms have been around for several decades. However, they were only given stark attention in the last decade when limitations in computing power were no longer an obstacle for applying ML *algorithms* for making helpful *ML models*. We refer to *algorithms* as the baseline commands that instruct a model *how to learn* from data, whereas a *ML model* is the result (i.e., the learned program) of learning the target task from the selected set of rules (*ML algorithm*) and examples (i.e., data). 

## Types of machine learning

In this section, we dealt mainly with basic elements of supervised learning, but note that there are several other types of ML problems. Some of which are:
* Unsupervised learning: we do not specify any correct behavior (i.e., labels). Here we have some observations, but the task itself, is not well-defined.
* Semi-supervised learning: we may specify some parts of our model with some labels, but other parts need to be learned without explicit targets. For instance, we can use unsupervised learning to obtain clusters that define features to a supervised learning problem.
* Active learning: the algorithm itself can ask for additional, useful examples. For instance, learn to select only examples that are actually needed for learning.
* Transfer learning: when a methods is trained for an individual scenario and you wish to use it in a different scenario. This translates into: how to make use of what was learned from A on B? 
* Reinforcement learning: the model is trained to act, rather than just to predict, and the algorithm itself uses outcomes from its experimented acts as feedback or *reinforcement* to achieve an optimized result of actions (e.g., a robot learning to walk).



```{admonition} Recommended course
:class: tip

Keep in mind to look for materials and study independently for your optimal learning. For instance, we highly recommend the comprehensive [machine learning course](https://www.edx.org/course/machine-learning-with-python-from-linear-models-to) offered by MITx, the online learning initiative of the Massachusetts Institute of Technology.


```

