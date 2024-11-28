"""
Module to train and store FHE models for homomorphic encryption.
"""

import os
import sys
import time
import joblib
from concrete.ml.deployment import FHEModelDev
from library.models.model_comparaison \
    import get_models  # pylint: disable=import-error


# Adjust path to include the library directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def train_fhe_models(models, x_train, y_train):
    """
    Train and store FHE models.

    Args:
        models (dict): Dictionary of Sklearn and FHE models.
        x_train (array-like): Training feature set.
        y_train (array-like): Training target set.

    Returns:
        dict: A dictionary with training times for each FHE model.
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
    """
    models = get_models()
    x_train, _, _, y_train, _, _ = \
        joblib.load("library/data/processed_data.pkl")
    training_times = train_fhe_models(models, x_train, y_train)
    print(training_times)


if __name__ == "__main__":
    main()
