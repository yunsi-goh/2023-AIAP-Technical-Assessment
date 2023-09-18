# General parameters
test_size = 0.3
random_state = 42

# Random forest parameters
RF_params = {
    'n_estimators': [100, 200, 500, 1000],
    'max_depth': [None, 2, 5, 10],
    'max_features': ['sqrt', 'log2'],
    'random_state': [random_state]
}

# Support vector machine parameters
SVM_params = {
    'C': [1e-2, 1e-1, 1e-0, 1e1, 1e2],
    'gamma': [1e-2, 1e-1, 1e-0, 1e1, 1e2],
    'kernel': ['rbf', 'sigmoid', 'poly', 'linear'],
    'random_state': [random_state]
}

# Support vector machine parameters
KNN_params = {
    'n_neighbors': [5, 10, 15, 20],
    'weights': ['uniform', 'distance'],
    'metric' : ['minkowski', 'euclidean', 'manhattan']
}
