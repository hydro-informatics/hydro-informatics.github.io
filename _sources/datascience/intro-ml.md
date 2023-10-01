This chapter is developed by {{ negreiros }}.

# Introduction to Machine Learning (ML)

Machine learning (ML) is argually one of the most prominent tools in data science to advance water resources research. ML models are capable of learning complex underlying relationships of a natural system, and thus finds its application in various water resources topics: from river ecosystem to water distribution nets. This section has the following objectives:

* Understand the overall concept of machine learning
* Understand elements of supervised learning


## The goal of machine learning

Machine learning aims at computationally learning complex relationships from experience (i.e., data). *Computational learning* because programs are created (or coded) to learn from example data. This task may be, for instance, predicting or modelling complex phenomena. Note that predicting here does not refers only to the future but to any non-identified event. For instance, we can predict whether a chemical substance will be, or was (or is), dissolved in water given a set of conditions.

Contrary to popular thinking, ML algorithms have been around for several decades. However, they were only given stark attention in the last decade when limitations in computing power were no longer an impecile for applying such *algorithms* for making helpful *ML models*. We refer to *algorithms* as the baseline commands that instruct a model *how to learn* from data, whereas a *ML model* is the result (i.e., the learned program) of learning the target task from the selected set of rules (*ML algorithm*) and examples (i.e., data). 

Existing ML algorithms are various and their applicability depends on the target task (or *mapping*) to be learned. Perceptron, Support Vector Machine, Pegasos, Decision trees, Random Forests, Neural Networks, are all examples of ML algorithms that follow a *supervised learning* approach.


## Elements of supervised learning

In supervised learning, we are given examples (i.e., measurements) along with the target solution (i.e., labels) that we wish the ML model to learn how to map. By contrast, in unsupervised learning problems, we are given examples but we do not know the target solution, or *labels*. A typical example of unsupervised learning problem is clustering.

### Training and testing
The goal of a ML algorithm following a supervised learning approach is to find out how to reproduce the target solution from *training* examples. Thus, a ML model is a function that maps the target solution from the set of parameters of the examples. We begin by hypothesizing a set of possible mappers (or functions) that take a set of parameters (or *features*) as arguments/input to yield the target solutions. We thus define the *hypothesis space* as the set of possible models (classifiers, regressors). The algorithm will then automate the process of finding the best *model parameters* (or the best model) that agree with the example-label pairs. This is done by optimizing the model with the  training dataset ($S$).

Our machine’s target is to find an in-to-output rule, which is noting by a mathematical function $F(x)$ so that:

  $$
	F(x) \rightarrow y
  $$
  
where $x$ are our attributes, also know as *features*, $y$ are the dataset labels, the target values we aim to map.

Our task is to find the best hypothesis (or best model) $h_{best}$ among the set of hypotheses $\mathcal{H}$. We do this by updating our hypothesis every time we loop through a training example, thus computing an improved hypothesis $h_{t+1}$ from our current hypothesis $h_t$. Intuitively, if $h_t$ misclassifies a particular training pair $(x_i, y_i) \in S$(training dataset), then we would like $h_{t+1}$ to be like $h_t$ but nudged toward accurately classifying $(x_i, y_i)$. To make $h_t$ less bad on a training example $(x_i, y_i)$, we will nudge $h_t$ in a tiny bit along the negative of the derivative of the optimization function ($\nabla C_t$). Such optimization method is called Gradient Descent (GD), because we use the gradient of the optimization function to update our hypothesis toward a better version. 

This is how the update would look like:

  $$
	\vec{h_{t+1}} = \vec{h_t} - \eta_t \cdot \nabla C_t
  $$

Note that the hypothesis is here a vector with model parameters (not features), or weights. 

### Optimization function: Loss and Regularization terms

The process of improving our hypothesis (or model) consists of an optimization problem, where we wish to minimize an optimization function ($C$). Intuitively, we would like to minimize discrepancies between predicted and actual values of $y$. These discrepancies are expressed in terms of a *loss function* that quantifies how well our model performed at a given example pair. At the same time, we do not wish that our model minimizes so much the loss function, and thus is so fitted to the training data, to the point that it is not applicable to a grand new dataset anymore. For this reason, we introduce a regularization term that aims at minimizing the complexity of the model. Finally, our optimization function would be:


  $$
	C(h_t) = \sum_{i}^{n} Loss_i + Regularizer 
  $$
  
	
where $n$ is the number of training examples. 

There some reasons why we do not wish to overfit our model to the training dataset. First, our training dataset may contain statistical noise that we do not wish to capture with our classifier. The figure below illustrates the concept:

![overfitting in ML](https://elitedatascience.com/wp-content/uploads/2017/09/Overfitting-Data-Points.png)

In the figure, we can clearly see that the green line is overfitted to the training datapoints denoted by two classes (blue and red points). The black line is probably a satisfactory decision boundary to split the red and blue points. 

The second reason why we do not wish to overfit our model is because, at the heart of machine learning problems, our goal is to be able to apply a model the learned from a training dataset to the world data. Thus, we wish that our model *generalizes* or applies correctly what was learned to a broader, unseen dataset. To verify if our model is performind well, it is not enough to minimize the training error. We must test the learned parameters on an unseen dataset, the so-called testing dataset.

It is unlikely that our model will deliver better results in the testing than in the training data, but there is an ideal scenario that we wish to achieve, that is, to minimize both the training and testing error. We will cover this topic in the section about *cross-validation*. 

### Classification and regression

More broadly, a ML model can be trained to learn how to predict categories or continuous values. In both these approaches, we will use the concepts above to build a *classifier* or a *regressor*, respectively. The main difference will be in the way how we compute the *training error*, or *loss*. In the next sections, we will cover both problems from a supervised learning perspective.

## Types of machine learning

In this section, we dealed mainly with supervised learning, but note that there are several other types of ML problems. Some of which are:
* Unsupervised learning: we do not specific any correct behaviors (i.e., labels). Here we have some observations, but the task itself, is not well-defined.
* Semi-supervised learning: we may specify some parts of our model with some labels, but other parts need to be learned without explicit targets. For instance, we can use unsupervised learning to obtain clusters that define features to a supervised learning problem.
* Active learning: the algorithm itself can ask for additional, useful examples. For instance, learn to select only examples that are actually needed for learning.
* Transfer learning: when a methods is trained for an individual scenario and you wish to use it in a different scenario. This translates into: how to make use of what was learned from A on B? 
* Reinforcement learning: the methods is trained to act, rather than jst to predict, and the algorithm itself uses outcomes from its experimented acts as feedback or *reinforcement* to achieve an optimized result of actions (e.g., a robot learning to walk).