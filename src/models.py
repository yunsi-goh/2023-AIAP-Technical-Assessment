import pandas as pd
import config as cfg
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier


def train_RF(X_train, y_train):

    # Define model
    model = RandomForestClassifier()

    # Grid search to tune parameters
    grid = cfg.RF_params
    grid_clf = GridSearchCV(estimator=model, param_grid=grid)
    grid_clf.fit(X_train, y_train)
    print("\nBEST RF PARAMETERS:", grid_clf.best_params_)
    print("BEST RF MEAN ACCURACY:", grid_clf.best_score_)

    # Train using best parameters
    best_clf = grid_clf.best_estimator_
    best_clf.fit(X_train, y_train)

    # Get feature importance
    impt_features = pd.DataFrame(best_clf.feature_importances_, index=X_train.columns)\
        .rename(columns={0: "importance"})\
        .sort_values(by="importance", ascending=False)
    print("RF FEATURE IMPORTANCE:")
    print(impt_features)

    return best_clf


def train_SVM(X_train, y_train):

    # SVM works better with normalized data
    X_train = preprocessing.scale(X_train)

    # Define model
    model = svm.SVC()

    # Grid search to tune parameters
    grid = cfg.SVM_params
    grid_clf = GridSearchCV(estimator=model, param_grid=grid)
    grid_clf.fit(X_train, y_train)
    print("\nBEST SVM PARAMETERS:", grid_clf.best_params_)
    print("BEST SVM MEAN ACCURACY:", grid_clf.best_score_)

    # Train using best parameters
    best_clf = grid_clf.best_estimator_
    best_clf.fit(X_train, y_train)

    return best_clf


def train_KNN(X_train, y_train):

    # Define model
    model = KNeighborsClassifier()

    # Grid search to tune parameters
    grid = cfg.KNN_params
    grid_clf = GridSearchCV(estimator=model, param_grid=grid)
    grid_clf.fit(X_train, y_train)
    print("\nBEST KNN PARAMETERS:", grid_clf.best_params_)
    print("BEST KNN MEAN ACCURACY:", grid_clf.best_score_)

    # Train using best parameters
    best_clf = grid_clf.best_estimator_
    best_clf.fit(X_train, y_train)

    return best_clf
