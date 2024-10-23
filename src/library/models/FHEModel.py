from concrete.ml.sklearn import RandomForestClassifier
from concrete.ml.deployment import FHEModelDev
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import joblib


import time
import joblib
import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library.models.model_comparaison import get_models
def train_fhe_models(models, X_train, y_train):
    """
    Train and store FHE models.
    """
    y_train = y_train.astype(int)
    
    
    for model_name, (sk_model, fhe_model) in models.items():
        if model_name == 'RandomForest':
            # Train FHE model
            fhe_model.fit(X_train, y_train)
            #Compile the model for homomorphic encryption
            fhe_model.compile(X_train)
            # Store trained models
            fhe_directory = os.path.join(os.path.abspath(os.getcwd()), 'models', 'fhe_files')
            
            dev = FHEModelDev(path_dir=fhe_directory, model=fhe_model)
            dev.save()
            break

def main():
    models = get_models()
    X_train, X_val, X_test, y_train, y_val, y_test = joblib.load('library/data/processed_data.pkl')
    training_times = train_fhe_models(models, X_train, y_train)

if __name__ == '__main__':
    main()