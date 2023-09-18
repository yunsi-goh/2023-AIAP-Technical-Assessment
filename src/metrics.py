import logging
import pandas as pd
from sklearn import metrics


def confusion_matrix(model, y_actual, y_pred):

    # Get confusion matrix
    cm = metrics.confusion_matrix(y_actual, y_pred, labels=model.classes_)

    # Change labels back to string
    labels = pd.DataFrame(model.classes_).replace({1.0: "Standard",
                                                   2.0: "Deluxe",
                                                   3.0: "Luxury"})
    labels = [i[0] for i in labels.values.tolist()]
    cm_disp = pd.DataFrame(cm, columns=labels, index=labels)

    # Print confusion matrix
    print("\nCONFUSION MATRIX:\n", cm_disp)
    logging.info(f"CONFUSION MATRIX:\n {cm_disp}")

    # Normalize confusion matrix by number of data in each class
    cm_norm = cm / cm.astype(float).sum(axis=1)

    # Change labels back to string
    cm_norm_disp = pd.DataFrame(cm_norm, columns=labels, index=labels)

    # Print normalized confusion matrix
    print("\nNORMALIZED CONFUSION MATRIX:\n", cm_norm_disp)
    logging.info(f"NORMALIZED CONFUSION MATRIX:\n {cm_norm_disp}")


def mean_accuracy(y_actual, y_pred):

    # Calculate mean accuracy
    accuracy = metrics.accuracy_score(y_actual, y_pred)

    # Print mean accuracy
    print("\nMEAN ACCURACY:", accuracy)
    logging.info(f"MEAN ACCURACY: {accuracy}")
