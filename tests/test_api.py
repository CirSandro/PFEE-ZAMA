import pytest
import pandas as pd
import os
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# URL de l'API client
CLIENT_URL = "http://127.0.0.1:8001/predict"

@pytest.fixture(scope="module")
def test_data():
    """
    Charge le dataset, effectue le prétraitement et retourne 10 échantillons de test avec leurs étiquettes.
    """
    # Chemin vers le dataset
    DATA_PATH = os.path.join(os.path.abspath(os.getcwd()), 'dataset', 'card_transdata.csv')
    
    # Charger les données (limitées à 100 000 lignes)
    df = pd.read_csv(DATA_PATH, nrows=100000)
    
    # Supprimer les valeurs manquantes
    df = df.dropna()
    
    # Gestion du déséquilibre des classes
    fraud = df[df['fraud'] == 1]
    non_fraud = df[df['fraud'] == 0].sample(n=len(fraud), random_state=42)
    df_equilibre = pd.concat([fraud, non_fraud])
    
    # Séparer les features et la cible
    X = df_equilibre.drop(columns=['fraud'])
    y = df_equilibre['fraud'].astype(int)
    
    # Séparer en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Sélectionner 10 échantillons aléatoires de l'ensemble de test
    X_sample = X_test.sample(n=10, random_state=42)
    y_sample = y_test.loc[X_sample.index].values
    
    # Appliquer le scaler
    scaler_path = os.path.join(os.path.abspath(os.getcwd()), 'models', 'scaler.pkl')
    scaler = StandardScaler()
    scaler.fit(X_train)  # Entraîner le scaler sur l'ensemble d'entraînement
    X_scaled = scaler.transform(X_sample)
    
    return X_scaled, y_sample

def test_api_accuracy(test_data):
    """
    Envoie 10 prédictions via l'API client et vérifie l'accuracy.
    """
    X_scaled, y_true = test_data
    predictions = []
    
    for i in range(len(X_scaled)):
        # Préparer le payload
        payload = {
            "distance_from_home": float(X_scaled[i][0]),
            "distance_from_last_transaction": float(X_scaled[i][1]),
            "ratio_to_median_purchase_price": float(X_scaled[i][2]),
            "repeat_retailer": int(X_scaled[i][3]),
            "used_chip": int(X_scaled[i][4]),
            "used_pin_number": int(X_scaled[i][5]),
            "online_order": int(X_scaled[i][6])
        }
        
        # Envoyer la requête POST à l'API client
        response = requests.post(CLIENT_URL, json=payload)
        
        # Vérifier que la requête a réussi
        assert response.status_code == 200, f"Requête échouée avec le statut {response.status_code}"
        
        # Récupérer la prédiction
        pred = response.json().get('prediction')
        assert pred is not None, "La prédiction est nulle"
        predictions.append(pred)
    
    # Calculer l'accuracy
    accuracy = accuracy_score(y_true, predictions)
    print(f"Accuracy sur 10 prédictions : {accuracy * 100:.2f}%")
    
    # Vérifier que l'accuracy est acceptable (par exemple, au moins 70%)
    assert accuracy >= 0.7, f"Accuracy trop basse : {accuracy * 100:.2f}%"
