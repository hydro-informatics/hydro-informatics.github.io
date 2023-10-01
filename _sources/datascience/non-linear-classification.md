```{admonition} Contributor
:class: tip
This chapter was written and developed by {{ negreiros }} <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(nonlinearclassification)=
## Non-linear Classification
 
In this section, we will cover fundamental concepts of non-linear classification by introducing the concept of kernels. First, let us recall what we have seen so far about linear classification. In linear classification, our task consisted of classifying data points through a hyperplane that could linearly separate the dataset in the features coordinate space. For instance, in a 3d feature space, thus a feature vector such as $(x_1, x_2, x_3) \in \mathbb{R}^3 $, recall that our data is considered linearly separable if there is at least one plane (not line) who can split the points. Unlike linear classification, which assumes a linear relationship between input features and class labels, non-linear classification algorithms use various techniques to capture complex patterns and decision boundaries in the data. 

In particular, we will look at how we can transform our data into a new coordinate space of higher dimension that can help us turning the non-linear problem into a linear one.
 
Kernels allow us to transform data into a higher-dimensional feature space where linear separation becomes possible. One example of ML algorithm that relies on kernels for finding complex pattern and decision boundaries in the data is Support Vector Machine (SVM). By computing the similarity between data points in the transformed feature space, SVMs can effectively classify non-linear data.


```{note}
Other non-linear classification algorithms include decision trees, random forests, k-nearest neighbors (KNN), and neural networks. These algorithms employ different techniques different from kernelization to model and capture non-linear relationships between input features and class labels, enabling them to handle complex classification tasks.```
