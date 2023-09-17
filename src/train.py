import os
import argparse
import datetime
from load import load_preprocessed
from models import train_RF, train_SVM
import joblib


if __name__ == '__main__':

    start = datetime.datetime.now()

    # Get model choice
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--model_type", type=str, help="RF / SVM / KNN", required=True)
    parser.add_argument("-n", "--model_name", type=str, help="Saved name of model", required=True)
    args = parser.parse_args()

    # Load data
    file_path = os.path.join("output", "preprocessed.csv")
    X_train, X_test, y_train, y_test = load_preprocessed(file_path)

    # Train and save model
    if args.model_type == "RF":
        print("Training Random Forest model...")
        model = train_RF(X_train, y_train)
        print("Saving Random Forest model...")
    elif args.model_type == "SVM":
        print("Training Support Vector Machine model...")
        model = train_SVM(X_train, y_train)
        print("Saving Support Vector Machine model...")
    else:
        print("WARNING: Choose a valid model: RF / SVM / KNN")
    joblib.dump(model, os.path.join("output", args.model_name+".pkl"))

    # Computing time
    stop = datetime.datetime.now()
    t = stop - start
    m, s = divmod(t.total_seconds(), 60)
    h, m = divmod(m, 60)
    print('Completed in: {} h {} min {} s'.format(round(h), round(m), round(s)))
