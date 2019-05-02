import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.linear_model import SGDRegressor, Ridge, Lasso, LinearRegression, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR

def main():
    all_data_file = 'data/data/all.csv'
    names = ['down', 'distance', 'yardsToGo', 'driveScore']
    all_data = pd.read_csv(all_data_file, names=names, quotechar='"')
    array = all_data.values
    independent_vars = array[:,0:3]
    dependent_vars = array[:,3]

    seed = 8 # Need some random seed
    check_models(independent_vars, dependent_vars, seed)


def check_models(independent_vars, dependent_vars, seed):
    models = []
    models.append(('LNR', LinearRegression()))
    models.append(('SGD', SGDRegressor(max_iter=5, tol=-np.infty)))
    models.append(('LSO', Lasso()))
    models.append(('ELN', ElasticNet()))
    models.append(('RR', Ridge()))
    models.append(('KNN', KNeighborsRegressor()))
    models.append(('DTR', DecisionTreeRegressor()))
    models.append(('SVR', SVR(gamma='scale')))

    scoring = 'neg_mean_squared_error'
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        results = model_selection.cross_val_score(model, independent_vars, dependent_vars, cv=kfold, scoring=scoring)
        print("{}: {}".format(name, results.mean()))


if __name__ == "__main__":
    main()
