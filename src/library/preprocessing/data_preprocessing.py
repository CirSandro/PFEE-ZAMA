"""
This module contains functions to load and preprocess the dataset.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


def load_data(path):
    """
    Load dataset from the given path.
    """
    return pd.read_csv(path)


def split_data(dataframe):
    """
    Balance the dataset to have equal numbers of fraud and non-fraud cases.
    Split the dataset into features and target.
    """
    fraud = dataframe[dataframe["fraud"] == 1]
    non_fraud = dataframe[dataframe["fraud"] == 0].sample(n=len(fraud), random_state=42)
    balanced_df = pd.concat([fraud, non_fraud])

    features = balanced_df.drop(columns=["fraud"])
    target = balanced_df["fraud"]
    return features, target


def preprocess_data(dataframe):
    """
    Balance the dataset to have equal numbers of fraud and non-fraud cases.
    Split the dataset into training, validation, and test sets.
    Scale the features using StandardScaler.
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
