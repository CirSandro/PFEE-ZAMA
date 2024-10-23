import requests
import numpy as np
import os
from concrete.ml.deployment import FHEModelClient
import joblib
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
import uvicorn

app = FastAPI()

# Load the scaler
scaler_path = os.path.join(os.path.abspath(os.getcwd()), 'models', 'scaler.pkl')
scaler = joblib.load(scaler_path)

# Initialize the FHE client (only once)
fhe_directory = os.path.join(os.path.abspath(os.getcwd()), 'models', 'fhe_files')
client = FHEModelClient(path_dir=fhe_directory, key_dir=fhe_directory)
serialized_evaluation_keys = client.get_serialized_evaluation_keys()

# Send evaluation keys to the server (only once)
def send_evaluation_keys():
    requests.post(
        'http://127.0.0.1:8000/evaluation_keys',
        json={'keys': serialized_evaluation_keys.hex()}
    )

# Send the keys on application startup
@app.on_event("startup")
async def startup_event():
    send_evaluation_keys()

class PredictionRequest(BaseModel):
    distance_from_home: float
    distance_from_last_transaction: float
    ratio_to_median_purchase_price: float
    repeat_retailer: int
    used_chip: int
    used_pin_number: int
    online_order: int
@app.post('/predict')
async def predict(request: PredictionRequest):
    # Retrieve user-input data
    input_data = np.array([
        request.distance_from_home,
        request.distance_from_last_transaction,
        request.ratio_to_median_purchase_price,
        request.repeat_retailer,
        request.used_chip,
        request.used_pin_number,
        request.online_order
    ]).reshape(1, -1)

    # Apply the scaler
    input_data_scaled = scaler.transform(input_data)

    # Encrypt the data
    encrypted_data = client.quantize_encrypt_serialize(input_data_scaled)

    # Send encrypted data to the server for prediction
    response = requests.post(
        'http://127.0.0.1:8000/predict',
        json={'data': encrypted_data.hex()}
    )
    encrypted_prediction = bytes.fromhex(response.json()['prediction'])

    # Decrypt the result
    prediction = client.deserialize_decrypt_dequantize(encrypted_prediction)
    
    # Extract the scalar value
    prediction_value = prediction[0]
    print(f"Type of prediction_value: {type(prediction_value)}")
    print(f"Value of prediction_value: {prediction_value}")
    
    # If the array contains two elements, choose the highest value
    binary_prediction = int(np.argmax(prediction_value))
    
    return {'prediction': binary_prediction}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)