"""
Module to train and store FHE models for homomorphic encryption.

This module trains models for Fully Homomorphic Encryption (FHE) and stores
them after training. It supports the training of Sklearn models, compiles them
for homomorphic encryption, and saves the FHE models for later use.
"""

import os
import sys
import time
import joblib
from concrete.ml.deployment import FHEModelDev
from library.models.model_comparaison import get_models  # pylint: disable=import-error


# Adjust path to include the library directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def train_fhe_models(models, x_train, y_train):
    """
    Train and store FHE models for homomorphic encryption.

    This function trains models for homomorphic encryption, compiles them,
    and stores them for future use.

    Args:
        models (dict):
            Dictionary containing model names as keys and model tuples as values.
            The tuples contain the Scikit-learn model and the FHE model:
            {
                "model_name": (sklearn_model, fhe_model)
            }.
        x_train (array-like):
            Feature set used for training the models. Should be a 2D array where
            each row represents a sample and each column represents a feature.
        y_train (array-like):
            Target labels for the training data. Should be a 1D array with the
            same number of elements as the number of samples in `x_train`.

    Returns:
        dict:
            A dictionary with the training times for each FHE model:
            {
                "model_name": training_time
            },
            where `training_time` is the time taken to train and compile the FHE model.
    """
    y_train = y_train.astype(int)
    training_times = {}

    for model_name, (_, fhe_model) in models.items():
        if model_name == "RandomForest":
            # Train FHE model
            start_time = time.time()
            fhe_model.fit(x_train, y_train)
            # Compile the model for homomorphic encryption
            fhe_model.compile(x_train)
            training_time = time.time() - start_time

            # Save the FHE model
            fhe_directory = os.path.join(
                os.path.abspath(os.getcwd()), "models", "fhe_files"
            )
            dev = FHEModelDev(path_dir=fhe_directory, model=fhe_model)
            dev.save()

            # Store the training time
            training_times[model_name] = training_time
            break

    return training_times


def main():
    """
    Main function to train FHE models and print training times.

    This function loads training data, trains the models for homomorphic encryption,
    and prints the training times for each model.

    Outputs:
        Prints the training times for the trained FHE models.
    """
    models = get_models()
    x_train, _, _, y_train, _, _ = joblib.load("library/data/processed_data.pkl")
    training_times = train_fhe_models(models, x_train, y_train)
    print(training_times)


if __name__ == "__main__":
    main()
