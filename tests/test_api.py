"""
This module contains tests for the client API.
"""

import os
import pytest
import pandas as pd
import requests

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Client API URL
CLIENT_URL = "http://127.0.0.1:8001/predict"


def preprocess_data(df):
    """
    Preprocesses the dataset by removing missing values and handling class imbalance.
    """
    # Remove missing values
    df = df.dropna()

    # Handle class imbalance
    fraud = df[df["fraud"] == 1]
    non_fraud = df[df["fraud"] == 0].sample(n=len(fraud), random_state=42)
    return pd.concat([fraud, non_fraud])


def split_data(df):
    """
    Splits the dataset into features and target, and then into training and test sets.
    """
    # Split features and target
    x = df.drop(columns=["fraud"])
    y = df["fraud"].astype(int)

    # Split into training and test sets
    return train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)


@pytest.fixture(scope="module")
def test_data():
    """
    Loads the dataset, performs preprocessing, and returns 10 test samples with their labels.
    """
    # Path to the dataset
    data_path = os.path.join(
        os.path.abspath(os.getcwd()), "dataset", "card_transdata.csv"
    )

    # Load the data (limited to 100,000 rows)
    df = pd.read_csv(data_path, nrows=100000)

    # Preprocess the data
    balanced_df = preprocess_data(df)

    # Split into training and test sets
    x_train, x_test, _, y_test = split_data(balanced_df)

    # Select 10 random samples from the test set
    x_sample = x_test.sample(n=10, random_state=42)
    y_sample = y_test.loc[x_sample.index].values

    # Apply the scaler
    # scaler_path = os.path.join(os.path.abspath(os.getcwd()), "models", "scaler.pkl")
    scaler = StandardScaler()
    scaler.fit(x_train)  # Train the scaler on the training set
    x_scaled = scaler.transform(x_sample)

    return x_scaled, y_sample


def test_api_accuracy(data_to_predict):
    """
    Sends 10 predictions via the client API and checks the accuracy.
    """
    x_scaled, y_true = data_to_predict
    predictions = []

    for _, sample in enumerate(x_scaled):
        payload = {
            "distance_from_home": float(sample[0]),
            "distance_from_last_transaction": float(sample[1]),
            "ratio_to_median_purchase_price": float(sample[2]),
            "repeat_retailer": int(sample[3]),
            "used_chip": int(sample[4]),
            "used_pin_number": int(sample[5]),
            "online_order": int(sample[6]),
        }

        # Send POST request to the client API
        response = requests.post(CLIENT_URL, json=payload, timeout=500)

        # Verify the request was successful
        assert (
            response.status_code == 200
        ), f"Request failed with status {response.status_code}"

        # Retrieve the prediction
        pred = response.json().get("prediction")
        assert pred is not None, "Prediction is None"
        predictions.append(pred)

    # Calculate accuracy
    accuracy = accuracy_score(y_true, predictions)
    print(f"Accuracy on 10 predictions: {accuracy * 100:.2f}%")

    # Verify the accuracy is acceptable (e.g., at least 70%)
    assert accuracy >= 0.7, f"Accuracy too low: {accuracy * 100:.2f}%"
