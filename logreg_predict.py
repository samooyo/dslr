import sys, os.path
from numpy.core.fromnumeric import mean, std
import pandas as pd
import numpy as np
from utilities.conf import HOUSES, SELECTED_COURSES

def sigmoid(x : np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))

def standarizer(values : list) -> list:
    return (values - mean(values)) / std(values)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('\nUsage : logreg_train.py PathToDatasetFile PathToWeights\n')
        exit(1)
    
    if not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        print("\nWrong path for files\n")
        exit(1)

    try:
        data_test   = pd.read_csv(sys.argv[1], index_col=0)              # TO DO : protect
        wheights    = pd.read_csv(sys.argv[2], index_col=0) # TO DO : protect
    except:
        print("\nSorry, wrong files\n")
        exit(1)

    x           = data_test.drop(columns=['Hogwarts House'])
    x           = x.loc[:, SELECTED_COURSES]
    x           = x.dropna()
    stand_x     = standarizer(x)
    results     = pd.DataFrame(index=x.index)
    
    for house in HOUSES:
        test            = sigmoid(np.dot(wheights[house], stand_x.T))
        results[house]  = test

    results['Hogwarts House'] = results.idxmax(axis=1)
    results.drop(results.columns[[0, 1, 2, 3]], axis=1, inplace=True)
    results.index.name = 'Index'
    results.to_csv('files/houses.csv')