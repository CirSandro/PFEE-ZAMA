"""
Server module for serving FHE model predictions using FastAPI.
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
    Schema for predict endpoint requests. Expects a hex-encoded string.
    """

    data: str


class EvaluationKeysRequest(BaseModel):
    """
    Schema for evaluation_keys endpoint requests. Expects a hex-encoded string.
    """

    keys: str


@app.post("/predict")
async def predict(request: PredictRequest):
    """
    Predict endpoint: receives encrypted input data, runs the FHE model,
    and returns encrypted predictions.
    """
    encrypted_data = bytes.fromhex(request.data)
    encrypted_result = server.run(
        encrypted_data, serialized_evaluation_keys=app.state.evaluation_keys
    )
    return {"prediction": encrypted_result.hex()}


@app.post("/evaluation_keys")
async def receive_evaluation_keys(request: EvaluationKeysRequest):
    """
    Evaluation_keys endpoint: receives the serialized evaluation keys.

    Args:
        request (EvaluationKeysRequest): Serialized evaluation keys in hex-encoded string format.

    Returns:
        dict: Status message.
    """
    # global evaluation_keys
    # evaluation_keys = bytes.fromhex(request.keys)
    # with open(os.path.join(fhe_directory, 'serialized_evaluation_keys.ekl'), 'wb') as f:
    #     f.write(EVALUATION_KEYS)
    # return {'status': 'Keys received'}
    app.state.evaluation_keys = bytes.fromhex(request.keys)
    with open(
        os.path.join(fhe_directory, "serialized_evaluation_keys.ekl"), "wb"
    ) as file_handler:
        file_handler.write(app.state.evaluation_keys)
    return {"status": "Keys received"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
