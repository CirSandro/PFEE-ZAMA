import requests
import numpy as np
import os
from concrete.ml.deployment import FHEModelClient
import joblib
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
import uvicorn

app = FastAPI()

# Charger le scaler
scaler_path = os.path.join(os.path.abspath(os.getcwd()), 'models', 'scaler.pkl')
scaler = joblib.load(scaler_path)

# Initialiser le client FHE (une seule fois)
fhe_directory = os.path.join(os.path.abspath(os.getcwd()), 'models', 'fhe_files')
client = FHEModelClient(path_dir=fhe_directory, key_dir=fhe_directory)
serialized_evaluation_keys = client.get_serialized_evaluation_keys()

# Envoyer les clés d'évaluation au serveur (une seule fois)
def send_evaluation_keys():
    requests.post(
        'http://127.0.0.1:8000/evaluation_keys',
        json={'keys': serialized_evaluation_keys.hex()}
    )

# Envoyer les clés au démarrage de l'application
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
    # Récupérer les données saisies par l'utilisateur
    input_data = np.array([
        request.distance_from_home,
        request.distance_from_last_transaction,
        request.ratio_to_median_purchase_price,
        request.repeat_retailer,
        request.used_chip,
        request.used_pin_number,
        request.online_order
    ]).reshape(1, -1)

    # Appliquer le scaler
    input_data_scaled = scaler.transform(input_data)

    # Chiffrer les données
    encrypted_data = client.quantize_encrypt_serialize(input_data_scaled)

    # Envoyer les données chiffrées au serveur pour la prédiction
    response = requests.post(
        'http://127.0.0.1:8000/predict',
        json={'data': encrypted_data.hex()}
    )
    encrypted_prediction = bytes.fromhex(response.json()['prediction'])

    # Déchiffrer le résultat
    prediction = client.deserialize_decrypt_dequantize(encrypted_prediction)
    
    # Extraire la valeur scalaire
    prediction_value = prediction[0]
    print(f"Type de prediction_value : {type(prediction_value)}")
    print(f"Valeur de prediction_value : {prediction_value}")
    
    # Si le tableau contient deux éléments, choisis la plus grande valeur
    binary_prediction = int(np.argmax(prediction_value))
    
    return {'prediction': binary_prediction}



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
