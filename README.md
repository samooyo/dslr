# dslr - School 42 Paris

## Datascience X Logistic Regression

In this project, I implemented a linear classification model focusing on two main points:

- Learning how to read and visualize a dataset in different ways, selecting and cleaning unnecessary information.
- Training a logistic regression model to solve a classification problem.

## Data visualization :

### Histogram : 
![](graphs/histogram.png)

The histogram shows a homogeneous score distribution for the Arithmancy and Care of Magical Creatures courses across all four houses. Therefore, these courses are not good candidates for our classification.

### Scatter plot :
![](graphs/scatter_plot.png)

Based on the scatter plot, it is evident that the Astronomy and Defense Against the Dark Arts courses are very similar. Including both in our regression model is unnecessary.


### Pair plot :
![](graphs/pair_plot.png)

From the pair plot, we can determine the most relevant features:
- Divination for separating Slytherin from the other houses.
- Transfiguration for Gryffindor.
- Astronomy to distinguish between Hufflepuff and Ravenclaw.

## Logistic regression :

### Theory :

Logistic regression is a statistical model that uses a logistic function to model a binary dependent variable. The concept is similar to linear regression, but with a different cost function that behaves as follows:
- If the correct answer 'y' is 0, the cost function will be 0 if the hypothesis function also outputs 0. As the hypothesis approaches 1, the cost function will approach infinity.
- If the correct answer 'y' is 1, the cost function will be 0 if the hypothesis function outputs 1. As the hypothesis approaches 0, the cost function will approach infinity.

This way, we penalize the algorithm heavily when the result is incorrect.

The cost function is :
$$J(θ) =−\frac1m \sum_{i=1}^m y^ilog(h_θ(x^i)) + (1−y^i) log(1−h_θ(x^i))$$
And the vectorized form is :
$$h=g(Xθ)$$
$$J(θ)= \frac1m⋅−y^Tlog⁡(h)−(1−y)^Tlog⁡(1−h)$$
Finally for the hypothesis we will have the Sigmoid function :
$$g(x) = \frac{1}{1+e^{-x}}$$

The model is binary, with outputs of 0 or 1. The chosen classification method is "One-vs-all," which means we classify one class and group all others into a single second class.

### Application :

When the theory is implemented, we have a complete classifier capable of providing the probability of a new student belonging to each house, ranging from 0 to 1. We assign the student to the house with the highest probability.

We can plot the outputs to better understand the logistic regression:

![](graphs/results.png)

The program achieves an accuracy score of 98.23%.

## Usage :

Create virtual environment by running `python3 -m venv venv` then activate it with `source venv/bin/activate`.  

Install all dependencies by running `pip install -r requirements.txt`.  

Then `python logreg_train.py` to train the algorithm and `python logreg_predict.py` for the prediction.

Similarly, all utilities can be used with :
```
python utilities/describe.py
python utilities/histogram.py
python utilities/scatter_plot.py
python utilities/pair_plot.py
```

In [graphs directory](graphs/) there are HTML files that can be opened directly from a browser to see all graphs along with PNG.
