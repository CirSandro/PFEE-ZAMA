"""
This module contains functions to load and preprocess the dataset for training.
It includes functions to load the dataset, balance the class distribution,
split the data into training, validation, and test sets, and scale the features
using StandardScaler. The preprocessed data is then saved for later use.

Functions:
    - load_data: Loads the dataset from a specified path.
    - split_data: Balances the dataset and separates features and target variable.
    - preprocess_data: Splits the data into training, validation, and test sets,
      scales the features, and saves the processed data.
    - main: Loads and preprocesses the data.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


def load_data(path):
    """
    Load dataset from the given path.
    Args:
        path (str): Path to the CSV file containing the dataset.

    Returns:
        pd.DataFrame: Loaded dataset as a pandas DataFrame.
    """
    return pd.read_csv(path)


def split_data(dataframe):
    """
    Balance the dataset to have equal numbers of fraud and non-fraud cases.
    Separates the dataset into features and target variables.
    Args:
        dataframe (pd.DataFrame): The dataset to be split.

    Returns:
        tuple: A tuple containing the features (X) and the target (y).
    """
    fraud = dataframe[dataframe["fraud"] == 1]
    non_fraud = dataframe[dataframe["fraud"] == 0].sample(n=len(fraud), random_state=42)
    balanced_df = pd.concat([fraud, non_fraud])

    features = balanced_df.drop(columns=["fraud"])
    target = balanced_df["fraud"]
    return features, target


def preprocess_data(dataframe):
    """
    Preprocess the dataset by balancing the class distribution, splitting it into
    training, validation, and test sets, and scaling the features using StandardScaler.

    Args:
        dataframe (pd.DataFrame): The raw dataset to be preprocessed.

    Returns:
        tuple: A tuple containing the scaled training, validation, and test features
               and their corresponding target variables.
    """

    features, target = split_data(dataframe)

    # Split into training, validation, and test sets
    train_features, test_features, train_target, test_target = train_test_split(
        features, target, test_size=0.2, random_state=42, stratify=target
    )
    train_features, val_features, train_target, val_target = train_test_split(
        train_features,
        train_target,
        test_size=0.2,
        random_state=42,
        stratify=train_target,
    )

    # Feature scaling
    scaler = StandardScaler()
    train_features_scaled = scaler.fit_transform(train_features)
    val_features_scaled = scaler.transform(val_features)
    test_features_scaled = scaler.transform(test_features)

    # Save the preprocessed data
    joblib.dump(
        (
            train_features_scaled,
            val_features_scaled,
            test_features_scaled,
            train_target,
            val_target,
            test_target,
        ),
        "library/data/processed_data.pkl",
    )

    return (
        train_features_scaled,
        val_features_scaled,
        test_features_scaled,
        train_target,
        val_target,
        test_target,
    )


def main():
    """
    Main function to load the data and preprocess it.
    """
    data_path = "library/data/card_transdata.csv"
    data = load_data(data_path)
    preprocess_data(data)


if __name__ == "__main__":
    main()
