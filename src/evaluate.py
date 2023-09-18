import os
import argparse
import datetime
import logging
from load import load_preprocessed
from metrics import confusion_matrix, mean_accuracy
import joblib


if __name__ == '__main__':

    start = datetime.datetime.now()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=os.path.join("output", "evaluate.log")
    )

    # Get model
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--model_name", type=str, help='Saved name of model', required=True)
    args = parser.parse_args()
    model = joblib.load(os.path.join("output", args.model_name+".pkl"))

    # Load data
    file_path = os.path.join("output", "preprocessed.csv")
    X_train, X_test, y_train, y_test = load_preprocessed(file_path)

    # Evaluate training
    print("\n\n##### TRAINING LOG #####")
    logging.info("##### TRAINING LOG  #####")
    print("\nMODEL:", model)
    logging.info(f"MODEL: {model}")
    y_train_pred = model.predict(X_train)
    confusion_matrix(model, y_train, y_train_pred)
    mean_accuracy(y_train, y_train_pred)

    # Evaluate testing
    print('\n\n##### TESTING LOG #####')
    logging.info("##### TESTING LOG #####")
    y_test_pred = model.predict(X_test)
    confusion_matrix(model, y_test, y_test_pred)
    mean_accuracy(y_test, y_test_pred)

    # Computing time
    stop = datetime.datetime.now()
    t = stop - start
    m, s = divmod(t.total_seconds(), 60)
    h, m = divmod(m, 60)
    print("\nCompleted in: {} h {} min {} s".format(round(h), round(m), round(s)))
    logging.info("Completed in: {} h {} min {} s".format(round(h), round(m), round(s)))
