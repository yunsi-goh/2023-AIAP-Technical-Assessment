import os
import argparse
import datetime
from load import load_preprocessed
from metrics import confusion_matrix, mean_accuracy
import joblib


if __name__ == '__main__':

    start = datetime.datetime.now()

    # Get model
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--model_name", type=str, help='Saved name of model', required=True)
    args = parser.parse_args()
    model = joblib.load(os.path.join("../output", args.model_name+".pkl"))

    # Load data
    file_path = os.path.join("../output", "preprocessed.csv")
    X_train, X_test, y_train, y_test = load_preprocessed(file_path)

    # Evaluate training
    print('##### TRAINING #####\n')
    y_train_pred = model.predict(X_train)
    confusion_matrix(model, y_train, y_train_pred)
    mean_accuracy(y_train, y_train_pred)
    print("")

    # Evaluate testing
    print('##### TESTING #####\n')
    y_test_pred = model.predict(X_test)
    confusion_matrix(model, y_test, y_test_pred)
    mean_accuracy(y_test, y_test_pred)
    print("")

    # Computing time
    stop = datetime.datetime.now()
    t = stop - start
    m, s = divmod(t.total_seconds(), 60)
    h, m = divmod(m, 60)
    print('Completed in: {} h {} min {} s'.format(round(h), round(m), round(s)))
