import pandas as pd
import config as cfg
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

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

