from fastapi import FastAPI
from pydantic import BaseModel
from concrete.ml.deployment import FHEModelServer
import os
import uvicorn

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
    encrypted_data = bytes.fromhex(request.data)
    encrypted_result = server.run(encrypted_data, serialized_evaluation_keys=evaluation_keys)
    return {'prediction': encrypted_result.hex()}

@app.post('/evaluation_keys')
async def receive_evaluation_keys(request: EvaluationKeysRequest):
    global evaluation_keys
    evaluation_keys = bytes.fromhex(request.keys)
    with open(os.path.join(fhe_directory, 'serialized_evaluation_keys.ekl'), 'wb') as f:
        f.write(evaluation_keys)
    return {'status': 'Keys received'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
