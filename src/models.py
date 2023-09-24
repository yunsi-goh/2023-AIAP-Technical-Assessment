import pandas as pd
import config as cfg
import logging
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


def train_RF(X_train, y_train):

    # Define model
    model = RandomForestClassifier()

    # Grid search to tune parameters
    grid = cfg.RF_params
    grid_clf = GridSearchCV(estimator=model, param_grid=grid)
    grid_clf.fit(X_train, y_train)

    # Log grid search results
    print("\nPARAMETERS TESTED:\n", grid)
    logging.info(f"PARAMETERS TESTED: {grid}")
    print("\nBEST PARAMETERS:\n", grid_clf.best_params_)
    logging.info(f"BEST PARAMETERS: {grid_clf.best_params_}")
    print("\nBEST ACCURACY:\n", grid_clf.best_score_)
    logging.info(f"BEST ACCURACY: {grid_clf.best_score_}")

    # Train using best parameters
    best_clf = grid_clf.best_estimator_
    best_clf.fit(X_train, y_train)

    # Get feature importance
    impt_features = pd.DataFrame(best_clf.feature_importances_, index=X_train.columns)\
        .rename(columns={0: " "})\
        .sort_values(by=" ", ascending=False)\
        .rename(index=cfg.rename_columns)

    # Log feature importance
    print("\nFEATURE IMPORTANCE:\n", impt_features)
    logging.info(f"FEATURE IMPORTANCE: {impt_features}")

    # Log final model
    print("\nFINAL MODEL:\n", best_clf)
    logging.info(f"FINAL MODEL: {best_clf}")

    return best_clf


def train_SVM(X_train, y_train):

    # Define model
    model = SVC()

    # Grid search to tune parameters
    # NOTE: SVM works better with normalized data
    grid = cfg.SVM_params
    grid_clf = make_pipeline(StandardScaler(),
                             GridSearchCV(estimator=model, param_grid=grid, refit=True))
    grid_clf.fit(X_train, y_train)

    # Log grid search results
    print("\nPARAMETERS TESTED:\n", grid)
    logging.info(f"PARAMETERS TESTED: {grid}")
    print("\nBEST PARAMETERS:\n", grid_clf.best_params_)
    logging.info(f"BEST PARAMETERS: {grid_clf.best_params_}")
    print("\nBEST ACCURACY:\n", grid_clf.best_score_)
    logging.info(f"BEST ACCURACY: {grid_clf.best_score_}")

    # Train using best parameters
    best_clf = grid_clf.best_estimator_
    best_clf.fit(X_train, y_train)

    # Log final model
    print("\nFINAL MODEL:\n", best_clf)
    logging.info(f"FINAL MODEL: {best_clf}")

    return best_clf


def train_KNN(X_train, y_train):

    # Define model
    model = KNeighborsClassifier()

    # Grid search to tune parameters
    grid = cfg.KNN_params
    grid_clf = GridSearchCV(estimator=model, param_grid=grid)
    grid_clf.fit(X_train, y_train)

    # Log grid search results
    print("\nPARAMETERS TESTED:\n", grid)
    logging.info(f"PARAMETERS TESTED: {grid}")
    print("\nBEST PARAMETERS:\n", grid_clf.best_params_)
    logging.info(f"BEST PARAMETERS: {grid_clf.best_params_}")
    print("\nBEST ACCURACY:\n", grid_clf.best_score_)
    logging.info(f"BEST ACCURACY: {grid_clf.best_score_}")

    # Train using best parameters
    best_clf = grid_clf.best_estimator_
    best_clf.fit(X_train, y_train)

    # Log final model
    print("\nFINAL MODEL:\n", best_clf)
    logging.info(f"FINAL MODEL: {best_clf}")

    return best_clf
