"""
Module to initialize the package 
and load preprocessed data for training models.
"""

from .preprocessing import data_preprocessing


def load_and_preprocess_data(data_path):
    """
    Load and preprocess the data from the given path.

    Args:
        data_path (str): Path to the data file.

    Returns:
        tuple: A tuple containing the preprocessed training, 
               validation, and test sets
               for features (X_train, X_val, X_test) and targets
               (y_train, y_val, y_test).
    """
    data = data_preprocessing.load_data(data_path)
    x_train, x_val, x_test, y_train, y_val, y_test = \
        data_preprocessing.preprocess_data(data)
    return x_train, x_val, x_test, y_train, y_val, y_test
