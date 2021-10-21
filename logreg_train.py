import numpy as np
import os.path
from numpy.core.fromnumeric import mean, std
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

SELECTED_COURSES = ['Hogwarts House', 'Transfiguration', 'Divination', 'Astronomy']
HOUSES = ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']

class LogReg:

    def __init__(self, pathData, epochs=100, learningRate=0.05):
        # self.bias = 0
        # self.weight = 0
        # self.normalizedbias = 0
        # self.normalizedweight = 0
        # self.x = 0
        # self.y = 0
        # self.normalizedX = 0
        # self.normalizedY = 0
        # self.lenData = 0
        # self.costHistory = []
        # self.biasHistory = []
        # self.weightHistory = []
        # self.processData(pathData)

        self.epochs = epochs
        self.learningRate = learningRate
        self.df = pd .read_csv(pathData, index_col='Index')
        # self.df = self.df.dropna()
        
        x = self.df.loc[:, SELECTED_COURSES]

        x = x.dropna()
        stand_x = self.standarizer(x.iloc[:, 1:])
        for house in HOUSES:
            y = np.where(x['Hogwarts House'] == house, 1, 0)
            theta = self.train(stand_x, y)
            test = self.sigmoid(theta * x.iloc[:, 1:])
            print(test)
            test['Hogwarts House'] = x.iloc[:, 0:1]
            # fig = px.scatter(data_frame=test,x=test['Transfiguration'], color='Hogwarts House')
            # fig.show()
        # exit()

        # x['results'] = test['Divination'].values
        # print(mean(x['results']), std(x['results']))
        # print(x)



    def processData(self, pathData):
        if not os.path.isfile(pathData):
            print("Wrong path for the data file")
            exit(1)

        self.data = pd.read_csv(pathData)
        self.x = self.data['km'].values
        self.y = self.data['price'].values
        if (len(self.x) != len(self.y)) or len(self.x) == 0:
            print("Data file is no gooood")
            exit(1)

        self.normalizedX = self.standarizer(self.x)
        self.normalizedY = self.standarizer(self.y)        
        self.lenData = len(self.x)

    def standarizer(self, values):

        standartizedValues = (values - mean(values)) / (std(values))

        return standartizedValues

##################################################################################
    def gradient(self, theta, x, y):
        # Computes the gradient of the cost function at the point theta
        m = x.shape[0]
        return (1 / m) * np.dot(x.T, self.sigmoid(self.net_input(theta,   x)) - y)
                                    #(        == h(x) or probability()      )               
    def cost_function(self, theta, x, y):   # J(theta)

        m = x.shape[0]
        total_cost = -(1 / m) * np.sum(
            y * np.log(self.probability(theta, x)) + (1 - y) * np.log(
                1 - self.probability(theta, x)))
        return total_cost

    def probability(self, theta, x):        #h(x)
        return self.sigmoid(self.net_input(theta, x))

    def net_input(self, theta, x):          # (z) = theta.T * x

        return np.dot(x, theta)

    def sigmoid(self, x):                   # g(z)
        y = 1 / (1 + np.exp(-x))

        return y

    def train(self, x, y): # x is course and y = 'Hogwarts House' == current_house
        theta = np.random.randn(x.shape[1])
        # theta = np.zeros((x.shape[1]))
        print(f'Theta before{theta}')
        for i in range(1000):
            # z = self.net_input(theta, x)
            # h = self.probability(theta, x)
            # j = self.cost_function(theta, x, y)
            g = self.gradient(theta, x, y)
            theta -= 0.01 * g

        print(f'Theta after {theta}')
        return theta

##################################################################################

    # def denormalizer(self):
    #     self.weight = (max(self.y) - min(self.y)) * self.normalizedweight / (max(self.x) - min(self.x))
    #     self.bias = min(self.y) + ((max(self.y) - min(self.y)) * self.normalizedbias) + self.weight * (1 - min(self.x))

    # def addCostHistory(self):        

    #     tot = 0
    #     for i in range(self.lenData):
    #         tot += (self.estimatePrice(self.normalizedX[i], self.normalizedbias, self.normalizedweight) - self.normalizedY[i])**2

    #     cost = tot / (2 * self.lenData)
    #     self.costHistory.append(cost)

    # def saveThetas(self):
    #     with open('files/thetas.txt', 'w') as f:
    #         f.write(str(self.bias))
    #         f.write('\n')
    #         f.write(str(self.weight))



if __name__ == "__main__":

    learn = LogReg('datasets/dataset_train.csv')
