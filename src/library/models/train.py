import time
import joblib
import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library.models.model_comparaison import get_models
def train_models(models, X_train, y_train):
    """
    Train multiple models.
    """
    y_train = y_train.astype(int)
    
    trained_models = {}
    training_times = {}

    
    
    for model_name, (sk_model, fhe_model) in models.items():
        # Train Sklearn model
        start_time = time.time()
        sk_model.fit(X_train, y_train)
        sk_training_time = time.time() - start_time
        
        # Store trained models and times
        trained_models[model_name] = (sk_model, fhe_model)
        training_times[model_name] = sk_training_time
    
    return trained_models, training_times

def main():
    models = get_models()
    X_train, X_val, X_test, y_train, y_val, y_test = joblib.load('library/data/processed_data.pkl')
    trained_models, training_times = train_models(models, X_train, y_train)
    # stoquer les modèles entrainés et les temps d'entrainement
    joblib.dump((trained_models, training_times), 'trained_and_times_models.pkl')

if __name__ == '__main__':
    main()