"""This module contains tests for the client API."""

import os
import time
from dataclasses import dataclass
from typing import Tuple, List

import pytest
import pandas as pd
import requests
from requests.exceptions import RequestException
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Client API URL
CLIENT_URL = "http://127.0.0.1:8001/predict"


@dataclass
class PredictionData:
    """Class to store prediction data and reduce local variables."""
    predictions: List[int]
    max_retries: int
    retry_delay: int
    success: bool
    last_exception: Exception = None


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the dataset by removing missing values
    and handling class imbalance.
    Args:
        df (pandas.DataFrame): Input data.
    Returns:
        balanced_df (pandas.DataFrame): Preprocessed data.
    """
    df = df.dropna()
    fraud = df[df["fraud"] == 1]
    non_fraud = df[df["fraud"] == 0].sample(n=len(fraud), random_state=42)
    return pd.concat([fraud, non_fraud])


def split_data(df: pd.DataFrame) -> Tuple:
    """
    Splits the dataset into features and target,
    and then into training and test sets.
    Args:
        df (pandas.DataFrame): Input data.
    Returns:
        x_train (pandas.DataFrame): Training features.
        x_test (pandas.DataFrame): Test features.
        y_train (pandas.Series): Training target.
        y_test (pandas.Series): Test target.
    """
    x = df.drop(columns=["fraud"])
    y = df["fraud"].astype(int)
    return train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)


def check_server() -> bool:
    """
    Verify if the server is accessible.

    Returns:
        bool: True if server is accessible, False otherwise.
    """
    try:
        response = requests.get("http://127.0.0.1:8001/docs", timeout=5)
        return response.status_code == 200
    except RequestException:
        return False


@pytest.fixture(scope="module", name="samples_data")
def _samples_data_fixture() -> Tuple:
    """
    Loads the dataset, performs preprocessing,
    and returns 100 test samples with their labels.
    Args:
        None
    Returns:
        x_scaled (numpy.ndarray): Scaled test features.
        y_sample (numpy.ndarray): Test labels.
    """
    data_path = os.path.join(
        os.path.abspath(os.getcwd()), "dataset", "card_transdata.csv"
    )
    df = pd.read_csv(data_path, nrows=100000)
    balanced_df = preprocess_data(df)
    _, x_test, _, y_test = split_data(balanced_df)
    x_sample = x_test.sample(n=100, random_state=42)
    y_sample = y_test.loc[x_sample.index].values
    return x_sample, y_sample


def process_prediction(sample: pd.Series, idx: int, pred_data: PredictionData) -> None:
    """
    Process a single prediction request.

    Args:
        sample: Input sample to process.
        idx: Sample index.
        pred_data: PredictionData instance to store results.
    """
    payload = {
        "distance_from_home": float(sample["distance_from_home"]),
        "distance_from_last_transaction": float(sample["distance_from_last_transaction"]),
        "ratio_to_median_purchase_price": float(sample["ratio_to_median_purchase_price"]),
        "repeat_retailer": int(sample["repeat_retailer"]),
        "used_chip": int(sample["used_chip"]),
        "used_pin_number": int(sample["used_pin_number"]),
        "online_order": int(sample["online_order"]),
    }

    for attempt in range(pred_data.max_retries):
        try:
            response = requests.post(CLIENT_URL, json=payload, timeout=500)
            response.raise_for_status()
            pred = response.json().get("prediction")
            if pred is not None:
                pred_data.predictions.append(pred)
                pred_data.success = True
                break
        except RequestException as e:
            pred_data.last_exception = e
            print(f"Attempt {attempt + 1} failed for sample {idx}. Error: {str(e)}")
            if attempt < pred_data.max_retries - 1:
                time.sleep(pred_data.retry_delay)


def test_api_accuracy(samples_data: Tuple) -> None:
    """
    Sends 100 predictions via the client API and checks the accuracy.

    Args:
        samples_data: Tuple containing test samples and their true labels.
    """
    x_samples, y_true = samples_data
    pred_data = PredictionData(
        predictions=[],
        max_retries=3,
        retry_delay=5,
        success=False
    )

    for i in range(30):
        if check_server():
            break
        if i == 29:
            pytest.fail("Server not accessible after 30 attempts")
        time.sleep(1)

    for idx, sample in enumerate(x_samples.iterrows()):
        pred_data.success = False
        process_prediction(sample[1], idx, pred_data)

        if not pred_data.success:
            error_msg = f"Failed to get prediction for sample {idx} after "
            error_msg += f"{pred_data.max_retries} attempts."
            if pred_data.last_exception:
                error_msg += f" Last error: {str(pred_data.last_exception)}"
            pytest.fail(error_msg)

    assert len(pred_data.predictions) == len(x_samples), (
        f"Expected {len(x_samples)} predictions but got {len(pred_data.predictions)}"
    )

    accuracy = accuracy_score(y_true, pred_data.predictions)
    print(f"\n{'='*50}")
    print(f"Accuracy on {len(pred_data.predictions)} predictions: {accuracy * 100:.2f}%")
    print(f"{'='*50}\n")

    assert accuracy >= 0.8, f"Accuracy too low: {accuracy * 100:.2f}%"
