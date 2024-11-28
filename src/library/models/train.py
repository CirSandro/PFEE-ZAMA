"""
This script trains multiple models and stores them in a dictionary.
"""

import time
import os
import sys
import joblib

from library.models.model_comparaison \
    import get_models  # pylint: disable=import-error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def train_models(models, x_train, y_train):
    """
    Train multiple models.
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
    """
    models = get_models()
    x_train, _, _, y_train, _, _ = \
        joblib.load("library/data/processed_data.pkl")
    trained_models, training_times = train_models(models, x_train, y_train)
    # load models and training times
    joblib.dump((trained_models, training_times), 
                "trained_and_times_models.pkl")


if __name__ == "__main__":
    main()
