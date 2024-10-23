from fastapi import FastAPI
from pydantic import BaseModel
from concrete.ml.deployment import FHEModelServer
import os
import uvicorn
import time

app = FastAPI()

# Load the FHE model
fhe_directory = os.path.join(os.path.abspath(os.getcwd()), 'models', 'fhe_files')
server = FHEModelServer(path_dir=fhe_directory)
server.load()

evaluation_keys = None

class PredictRequest(BaseModel):
    data: str

class EvaluationKeysRequest(BaseModel):
    keys: str

@app.post('/predict')
async def predict(request: PredictRequest):
    global evaluation_keys
    
    # Start measuring time
    total_start_time = time.time()

    # Step 1: Receive and convert encrypted data
    start_time = time.time()
    encrypted_data = bytes.fromhex(request.data)
    print(f"Time to convert encrypted data from hex: {time.time() - start_time} seconds")

    # Step 2: Run prediction
    start_time = time.time()
    encrypted_result = server.run(encrypted_data, serialized_evaluation_keys=evaluation_keys)
    print(f"Time for running prediction on encrypted data: {time.time() - start_time} seconds")

    # Step 3: Convert the result to hex
    start_time = time.time()
    encrypted_result_hex = encrypted_result.hex()
    print(f"Time to convert encrypted result to hex: {time.time() - start_time} seconds")

    # Total time
    print(f"Total time for prediction request: {time.time() - total_start_time} seconds")

    return {'prediction': encrypted_result_hex}

@app.post('/evaluation_keys')
async def receive_evaluation_keys(request: EvaluationKeysRequest):
    global evaluation_keys

    # Start measuring time
    start_time = time.time()

    # Receive and convert evaluation keys
    evaluation_keys = bytes.fromhex(request.keys)
    print(f"Time to convert evaluation keys from hex: {time.time() - start_time} seconds")

    # Step 2: Save the keys
    start_time = time.time()
    with open(os.path.join(fhe_directory, 'serialized_evaluation_keys.ekl'), 'wb') as f:
        f.write(evaluation_keys)
    print(f"Time to save evaluation keys to file: {time.time() - start_time} seconds")

    return {'status': 'Keys received'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
