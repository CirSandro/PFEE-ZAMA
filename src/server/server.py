"""
Server module for serving FHE model predictions using FastAPI.

This module exposes two FastAPI endpoints:
    - /predict: Accepts encrypted input data, runs the FHE model, and returns encrypted predictions.
    - /evaluation_keys: Accepts serialized evaluation keys in hex-encoded format and stores them
                                             for later use.

The module uses Concrete ML for serving predictions with homomorphic encryption (FHE).

Modules:
    - FastAPI: Web framework to create the API.
    - pydantic: Used to define request body models.
    - concrete.ml.deployment.FHEModelServer: For loading and running the FHE model.
    - uvicorn: ASGI server for running the FastAPI application.
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
from concrete.ml.deployment import FHEModelServer
import uvicorn


app = FastAPI()

# Load the FHE model
fhe_directory = os.path.join(os.path.abspath(os.getcwd()), "models", "fhe_files")
server = FHEModelServer(path_dir=fhe_directory)
server.load()

# EVALUATION_KEYS = None # ici j'ai changer cétait en minuscule avant
app.state.evaluation_keys = None


class PredictRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Schema for predict endpoint requests. Expects a hex-encoded string representing the encrypted
    input data.

    Attributes:
        data (str): The encrypted input data in hex-encoded format.
    """

    data: str


class EvaluationKeysRequest(BaseModel):
    """
    Schema for evaluation_keys endpoint requests. Expects a hex-encoded string of the serialized
    evaluation keys.

    Attributes:
        keys (str): The serialized evaluation keys in hex-encoded format.
    """

    keys: str


@app.post("/predict")
async def predict(request: PredictRequest):
    """
    Predict endpoint: Receives encrypted input data, runs the FHE model, and returns encrypted
    predictions.

    This endpoint accepts encrypted data, decrypts it, runs the prediction using the FHE model,
    and returns the encrypted prediction in hex format.

    Args:
        request (PredictRequest): The encrypted input data as a hex-encoded string.

    Returns:
        dict: A dictionary containing the encrypted prediction in hex format.
    """
    encrypted_data = bytes.fromhex(request.data)
    encrypted_result = server.run(
        encrypted_data, serialized_evaluation_keys=app.state.evaluation_keys
    )
    return {"prediction": encrypted_result.hex()}


@app.post("/evaluation_keys")
async def receive_evaluation_keys(request: EvaluationKeysRequest):
    """
    Evaluation_keys endpoint: Receives the serialized evaluation keys.

    This endpoint accepts evaluation keys in hex-encoded format, stores them in the server state,
    and writes them to a file for future use during predictions.

    Args:
        request (EvaluationKeysRequest): The serialized evaluation keys as a hex-encoded string.

    Returns:
        dict: A status message indicating that the keys were successfully received and stored.
    """
    app.state.evaluation_keys = bytes.fromhex(request.keys)
    with open(
        os.path.join(fhe_directory, "serialized_evaluation_keys.ekl"), "wb"
    ) as file_handler:
        file_handler.write(app.state.evaluation_keys)
    return {"status": "Keys received"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
