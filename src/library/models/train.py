"""
This script trains multiple models and stores them in a dictionary.

This script loads a set of machine learning models, trains them on a given
training dataset, and stores both the trained models and their corresponding
training times in a dictionary. The trained models include both Sklearn and
Fully Homomorphic Encryption (FHE) versions of various classifiers.
"""

import time
import os
import sys
import joblib

from library.models.model_comparaison import get_models  # pylint: disable=import-error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def train_models(models, x_train, y_train):
    """
    This function takes a dictionary of models and their corresponding Sklearn
    and FHE versions, trains the Sklearn models on the provided training data,
    and stores the trained models and their training times.

    Args:
        models (dict): A dictionary where each key is a model name and each value is a
                       tuple containing the Sklearn model and the FHE model.
        x_train (array-like): The training feature set (input data).
        y_train (array-like): The training target set (labels).

    Returns:
        tuple: A tuple containing:
            - trained_models (dict): A dictionary where each key is a model name, and each value is
                                     a tuple containing the trained Sklearn and FHE models.
            - training_times (dict): A dictionary where each key is a model name, and each value is
                                     the time taken to train the Sklearn model.
    """
    y_train = y_train.astype(int)

    trained_models = {}
    training_times = {}

    for model_name, (sk_model, fhe_model) in models.items():
        # Train Sklearn model
        start_time = time.time()
        sk_model.fit(x_train, y_train)
        sk_training_time = time.time() - start_time

        # Store trained models and times
        trained_models[model_name] = (sk_model, fhe_model)
        training_times[model_name] = sk_training_time

    return trained_models, training_times


def main():
    """
    Main function to train models.

    This function loads the training data, trains the models using the
    `train_models` function, and stores the trained models and their
    training times in a file.

    Returns:
        None
    """
    models = get_models()
    x_train, _, _, y_train, _, _ = joblib.load("library/data/processed_data.pkl")
    trained_models, training_times = train_models(models, x_train, y_train)
    # load models and training times
    joblib.dump((trained_models, training_times), "trained_and_times_models.pkl")


if __name__ == "__main__":
    main()
