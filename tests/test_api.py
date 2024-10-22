import pytest
import pandas as pd
import os
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Client API URL
CLIENT_URL = "http://127.0.0.1:8001/predict"

@pytest.fixture(scope="module")
def test_data():
    """
    Loads the dataset, performs preprocessing, and returns 10 test samples with their labels.
    """
    # Path to the dataset
    DATA_PATH = os.path.join(os.path.abspath(os.getcwd()), 'dataset', 'card_transdata.csv')
    
    # Load the data (limited to 100,000 rows)
    df = pd.read_csv(DATA_PATH, nrows=100000)
    
    # Remove missing values
    df = df.dropna()
    
    # Handle class imbalance
    fraud = df[df['fraud'] == 1]
    non_fraud = df[df['fraud'] == 0].sample(n=len(fraud), random_state=42)
    balanced_df = pd.concat([fraud, non_fraud])
    
    # Split features and target
    X = balanced_df.drop(columns=['fraud'])
    y = balanced_df['fraud'].astype(int)
    
    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Select 10 random samples from the test set
    X_sample = X_test.sample(n=10, random_state=42)
    y_sample = y_test.loc[X_sample.index].values
    
    # Apply the scaler
    scaler_path = os.path.join(os.path.abspath(os.getcwd()), 'models', 'scaler.pkl')
    scaler = StandardScaler()
    scaler.fit(X_train)  # Train the scaler on the training set
    X_scaled = scaler.transform(X_sample)
    
    return X_scaled, y_sample

def test_api_accuracy(test_data):
    """
    Sends 10 predictions via the client API and checks the accuracy.
    """
    X_scaled, y_true = test_data
    predictions = []
    
    for i in range(len(X_scaled)):
        # Prepare the payload
        payload = {
            "distance_from_home": float(X_scaled[i][0]),
            "distance_from_last_transaction": float(X_scaled[i][1]),
            "ratio_to_median_purchase_price": float(X_scaled[i][2]),
            "repeat_retailer": int(X_scaled[i][3]),
            "used_chip": int(X_scaled[i][4]),
            "used_pin_number": int(X_scaled[i][5]),
            "online_order": int(X_scaled[i][6])
        }
        
        # Send POST request to the client API
        response = requests.post(CLIENT_URL, json=payload)
        
        # Verify the request was successful
        assert response.status_code == 200, f"Request failed with status {response.status_code}"
        
        # Retrieve the prediction
        pred = response.json().get('prediction')
        assert pred is not None, "Prediction is None"
        predictions.append(pred)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_true, predictions)
    print(f"Accuracy on 10 predictions: {accuracy * 100:.2f}%")
    
    # Verify the accuracy is acceptable (e.g., at least 70%)
    assert accuracy >= 0.7, f"Accuracy too low: {accuracy * 100:.2f}%"
