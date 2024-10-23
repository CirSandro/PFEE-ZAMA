from sklearn.metrics import accuracy_score
# from . import evaluate_models
from library.models import get_models
import pandas as pd
import time
def evaluate_models(models, X_train, y_train, X_val, y_val, training_times):
    """
    Evaluate trained models and compare performance.
    """
    y_val = y_val.astype(int)
    y_train = y_train.astype(int)
    
    results = []
    for model_name, (sk_model, fhe_model) in models.items():
        # Predict with Sklearn model
        sk_y_pred = sk_model.predict(X_val)
        sk_accuracy = accuracy_score(y_val, sk_y_pred)

        # Train FHE model
        start_time = time.time()
        fhe_model.fit(X_train, y_train)
        fhe_training_time = time.time() - start_time
        # Predict with FHE model
        fhe_y_pred = fhe_model.predict(X_val)
        fhe_accuracy = accuracy_score(y_val, fhe_y_pred)

        # Calculate ratios
        sk_training_time= training_times[model_name] #, fhe_training_time 
        time_ratio = fhe_training_time / sk_training_time
        accuracy_ratio = fhe_accuracy / sk_accuracy

        # Store results
        results.append({
            "Model": model_name,
            "Sklearn Accuracy": sk_accuracy,
            "Sklearn Time": sk_training_time,
            "FHE Accuracy": fhe_accuracy,
            "FHE Time": fhe_training_time,
            "Time Ratio (FHE/Sklearn)": time_ratio,
            "Accuracy Ratio (FHE/Sklearn)": accuracy_ratio
        })

    return results

import joblib

def main():
    X_train, X_val, X_test, y_train, y_val, y_test = joblib.load('library/data/processed_data.pkl')
    # charger les modèles entrainés et les temps d'entrainement
    trained_models, training_times = joblib.load('trained_and_times_models.pkl')
    results = evaluate_models(trained_models, X_train, y_train, X_val, y_val, training_times)
    # stocker les résultats dans un fichier csv
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)

if __name__ == "__main__":
    main()
