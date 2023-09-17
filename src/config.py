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
