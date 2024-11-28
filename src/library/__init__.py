"""
Module to initialize the package and load preprocessed data for training models.
"""

from .preprocessing import data_preprocessing


def load_and_preprocess_data(data_path):
    """
    Load and preprocess the data from the given path.

    Args:
        data_path (str): Path to the data file.

    Returns:
        tuple: A tuple containing the preprocessed training, validation, and test sets
               for features (X_train, X_val, X_test) and targets (y_train, y_val, y_test).
    """
    data = data_preprocessing.load_data(data_path)
    x_train, x_val, x_test, y_train, y_val, y_test = data_preprocessing.preprocess_data(data)
    return x_train, x_val, x_test, y_train, y_val, y_test

# # Model training
# def train_models(X_train, y_train):
#     models = train.get_models()
#     train.train_models(models, X_train, y_train)
#     return models

# # Model evaluation
# def evaluate_models(models, X_val, y_val):
#     evaluation_results = evaluate.evaluate_model(models, X_val, y_val)
#     return evaluation_results
