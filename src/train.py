import os
import argparse
import datetime
import logging
from load import load_preprocessed
from models import train_RF, train_SVM, train_KNN
import joblib


if __name__ == '__main__':

    start = datetime.datetime.now()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=os.path.join("output", "train.log")
    )

    # Get model choice
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--model_type", type=str, help="RF / SVM / KNN", required=True)
    parser.add_argument("-n", "--model_name", type=str, help="Saved name of model", required=True)
    args = parser.parse_args()

    # Load data
    file_path = os.path.join("output", "preprocessed.csv")
    X_train, X_test, y_train, y_test = load_preprocessed(file_path)

    # Train model
    if args.model_type == "RF":
        print("\nTraining Random Forest (RF) model...")
        logging.info("Training Random Forest (RF) model...")
        model = train_RF(X_train, y_train)
    elif args.model_type == "SVM":
        print("\nTraining Support Vector Machine (SVM) model...")
        logging.info("Training Support Vector Machine (SVM) model...")
        model = train_SVM(X_train, y_train)
    elif args.model_type == "KNN":
        print("\nTraining K-Nearest Neighbour (KNN) model...")
        logging.info("Training K-Nearest Neighbour (KNN) model...")
        model = train_KNN(X_train, y_train)

    # Save model
    try:
        print("\nSaving final model...")
        logging.info("Saving final model...")
        joblib.dump(model, os.path.join("output", args.model_name+".pkl"))
    except NameError:
        print("\nERROR: Choose a valid model: RF / SVM / KNN")
        logging.error("Choose a valid model: RF / SVM / KNN")

    # Computing time
    stop = datetime.datetime.now()
    t = stop - start
    m, s = divmod(t.total_seconds(), 60)
    h, m = divmod(m, 60)
    print("\nCompleted in: {} h {} min {} s".format(round(h), round(m), round(s)))
    logging.info("Completed in: {} h {} min {} s".format(round(h), round(m), round(s)))
    logging.shutdown()
