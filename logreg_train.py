from plotly.subplots import make_subplots
from pandas.core.frame import DataFrame
import plotly.graph_objects as go
from numpy.core.fromnumeric import mean, std
import numpy as np
import pandas as pd
import sys, os.path
from utilities.conf import HOUSES, SELECTED_COURSES_AND_HOUSES

class LogReg:

    def __init__(self, path_data : str, epochs : int=2000, learning_rate : float=0.1) -> None:
        self.epochs         = epochs
        self.learning_rate  = learning_rate
        
        self.x          : DataFrame
        self.stand_x    : DataFrame
        self.df         : DataFrame
        self.all_thetas = pd.DataFrame()

        self.processData(path_data)
        self.initialize_training()
        self.save_thetas()
        self.get_precision()

    def processData(self, path_data : str) -> None:
        if not os.path.isfile(path_data):
            print("\nWrong path for the data file\n")
            exit(1)
        try:
            self.df = pd.read_csv(path_data, index_col='Index')
        except:
            print("\nThe file is not a dataset !\n")
            exit(1)
        if type(self.df['Hogwarts House'][1]) != str:
            print("\nWrong dataset format !\n")
            exit(1)

############################## Gradient Section ##############################
    def standarizer(self, values : list) -> list:
        return (values - mean(values)) / std(values)

    def gradient(self, thetas : np.ndarray, x : np.ndarray, y : np.ndarray) -> np.ndarray:
        m = x.shape[0]  # m is the number of elements
        return (1.0 / m) * np.dot(x.T, self.probability(thetas, x) - y)

    def probability(self, thetas : np.ndarray, x : np.ndarray) -> np.ndarray:   ## h(x)
        return self.sigmoid(self.z(thetas, x))                                  ##

    def z(self, thetas, x : np.ndarray) -> np.ndarray:                          ## (z) = theta.T * x
        return np.dot(x, thetas)                                                ##

    def sigmoid(self, x : np.ndarray) -> np.ndarray:                            ## g(z)
        return 1.0 / (1.0 + np.exp(-x))                                         ##

    def cost_function(self, thetas, x : DataFrame, y : np.ndarray) -> float:    ##
        m = x.shape[0]                                                          ##
        total_cost = -(1.0 / m) * np.sum(                                       ##
            y * np.log(self.probability(thetas, x)) + (1.0 - y) *               ## cost function
            np.log(1.0 - self.probability(thetas, x)))                          ##
                                                                                ##
        return total_cost                                                       ##

    def train(self, x : DataFrame, y : np.ndarray) -> np.ndarray:               # x is course and y = 'Hogwarts House'
        thetas  = np.random.randn(x.shape[1])
        cost    = []
        for i in range(self.epochs):
            j   = self.cost_function(thetas, x, y)
            g   = self.gradient(thetas, x, y)

            thetas -= self.learning_rate * g
            cost.append(j)

        return thetas, j

    def initialize_training(self) -> None:
        tmp_df          = self.df.dropna()
        self.x          = tmp_df.loc[:, SELECTED_COURSES_AND_HOUSES]
        self.stand_x    = self.standarizer(self.x.iloc[:, 1:])

        for house in HOUSES:
            y           = np.where(self.x['Hogwarts House'] == house, 1, 0)
            thetas,cost = self.train(self.stand_x, y)
            self.all_thetas[house] = thetas


############################## Utilities ##############################
    def save_thetas(self) -> None:
        self.all_thetas.to_csv('files/weights.csv')

    def get_precision(self) -> None:
        results = pd.DataFrame(index=self.x.index)

        for house in HOUSES:
            test            = self.sigmoid(np.dot(self.all_thetas[house], self.stand_x.T))
            results[house]  = test

        results['Predicted House']  = results.idxmax(axis=1)
        results['Actual House']     = self.x['Hogwarts House']
        results['Prediction']       = results['Predicted House'] == results['Actual House']
        self.precision = (len(results[results['Prediction'] == True]) / len(self.x)) * 100
        print(f'Precision = {self.precision:.2f}%')


############################## Graph Section ##############################
    def show_graph(self) -> None:
        fig = make_subplots(rows=2, cols=2, vertical_spacing=0.05, horizontal_spacing= 0.05,
            subplot_titles=('Ravenclaw VS all', 'Slytherin VS all', 'Gryffindor VS all', 'Hufflepuff VS all'))
        row     = col = 1
        show    = True
        for house_sub in HOUSES:
            if col  == 3:
                col = 1
                row = 2

            for house in HOUSES:
                test    = self.sigmoid(np.dot(self.all_thetas[house_sub], self.stand_x.T))
                results = pd.DataFrame()
                results['Hogwarts House']   = self.x.iloc[:, 0:1]
                results['results']          = test
                results = results[results['Hogwarts House'] == house]
                fig.add_trace(go.Scatter(x=results['results'], y=results.index, mode='markers',
                    marker_color=self.get_color(house), showlegend=show, name=house), row=row, col=col)
            show = False
            col += 1
        fig.show()

    def get_color(self, house : str) -> str:
        if house == 'Ravenclaw'     : return 'red'
        if house == 'Slytherin'     : return 'blue'
        if house == 'Gryffindor'    : return 'yellow'
        if house == 'Hufflepuff'    : return 'green'


############################## Main ##############################
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('\nUsage : logreg_train.py PathToDatasetFile\n')
        exit(1)

    learn = LogReg(sys.argv[1])
    learn.show_graph()
