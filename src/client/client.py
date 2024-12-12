"""
Client module for FHE-based prediction system.

This module provides a FastAPI application that handles secure predictions using
Fully Homomorphic Encryption (FHE). The app includes an endpoint to process
prediction requests by sending encrypted data to a server and decrypting the result.

Modules:
- FastAPI for API creation and routing.
- Concrete-ML for FHE operations.
- Scikit-learn for preprocessing.
- Requests for HTTP requests.

Endpoints:
- POST /predict: Handles prediction requests.
"""

import os
import requests
import numpy as np
import joblib
from concrete.ml.deployment import FHEModelClient
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Load the scaler
scaler_path = os.path.join(os.path.abspath(os.getcwd()), "models", "scaler.pkl")
scaler = joblib.load(scaler_path)

# Initialize the FHE client (only once)
fhe_directory = os.path.join(os.path.abspath(os.getcwd()), "models", "fhe_files")
client = FHEModelClient(path_dir=fhe_directory, key_dir=fhe_directory)
serialized_evaluation_keys = client.get_serialized_evaluation_keys()


def send_evaluation_keys():
    """
    Sends the FHE evaluation keys to the server.

    This function retrieves the serialized evaluation keys from the FHE client
    and sends them to the server via an HTTP POST request.

    :raises:
        requests.exceptions.RequestException: If the POST request fails.
    """
    requests.post(
        "http://127.0.0.1:8000/evaluation_keys",
        json={"keys": serialized_evaluation_keys.hex()},
        timeout=500,
    )


@app.on_event("startup")
async def startup_event():
    """
    Event triggered on application startup to send evaluation keys to the server.

    This ensures the server has the necessary keys for encrypted predictions
    before handling any requests.
    """
    send_evaluation_keys()


class PredictionRequest(BaseModel):
    """
    Pydantic model for validating prediction request inputs.

    Attributes:
        distance_from_home (float): Distance from home where the transaction occurred.
        distance_from_last_transaction (float): Distance from the previous transaction location.
        ratio_to_median_purchase_price (float): Ratio of the transaction amount to the median price.
        repeat_retailer (int): Whether the retailer is a repeat retailer (1 for yes, 0 for no).
        used_chip (int): Whether the transaction used a chip (1 for yes, 0 for no).
        used_pin_number (int): Whether a PIN number was used (1 for yes, 0 for no).
        online_order (int): Whether the transaction was an online order (1 for yes, 0 for no).
    """

    distance_from_home: float
    distance_from_last_transaction: float
    ratio_to_median_purchase_price: float
    repeat_retailer: int
    used_chip: int
    used_pin_number: int
    online_order: int


@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Endpoint to handle prediction requests.

    This endpoint accepts input data, processes it, and uses an FHE-based system
    to make secure predictions. The process involves scaling the data, encrypting it,
    sending it to a server for computation, and decrypting the result.

    :param request: Input data for prediction, wrapped in a `PredictionRequest` object.

    :return:
        dict: A dictionary containing the binary prediction result, in the format:
            {
                "prediction": <int>
            }
        where the prediction is 0 or 1 (binary classification).
    """
    # Retrieve user-input data
    input_data = np.array(
        [
            request.distance_from_home,
            request.distance_from_last_transaction,
            request.ratio_to_median_purchase_price,
            request.repeat_retailer,
            request.used_chip,
            request.used_pin_number,
            request.online_order,
        ]
    ).reshape(1, -1)

    # Apply the scaler
    input_data_scaled = scaler.transform(input_data)

    # Encrypt the data
    encrypted_data = client.quantize_encrypt_serialize(input_data_scaled)

    # Send encrypted data to the server for prediction
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={"data": encrypted_data.hex()},
        timeout=500,
    )
    encrypted_prediction = bytes.fromhex(response.json()["prediction"])

    # Decrypt the result
    prediction = client.deserialize_decrypt_dequantize(encrypted_prediction)

    # Extract the scalar value
    prediction_value = prediction[0]
    print(f"Type of prediction_value: {type(prediction_value)}")
    print(f"Value of prediction_value: {prediction_value}")

    # If the array contains two elements, choose the highest value
    binary_prediction = int(np.argmax(prediction_value))

    return {"prediction": binary_prediction}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
