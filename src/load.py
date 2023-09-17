import os
import pandas as pd
import config as cfg
from sklearn.model_selection import train_test_split


def load_preprocessed(file_path):

    # Load data
    data = pd.read_csv(file_path)
    data = data.head(100)

    # Split features and target
    target = "ticket"
    X = data.drop([target], axis="columns")
    y = data[target]

    # Split data into training (70%) and testing (30%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=cfg.test_size,
                                                        random_state=cfg.random_state)

    return X_train, X_test, y_train, y_test
