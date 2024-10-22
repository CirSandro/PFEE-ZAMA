import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from concrete.ml.sklearn.rf import RandomForestClassifier
from concrete.ml.deployment import FHEModelDev

# Charger les données (100 000 lignes uniquement)
DATA_PATH = os.path.join(os.path.abspath(os.getcwd()), 'dataset', 'card_transdata.csv')
df = pd.read_csv(DATA_PATH, nrows=100000)  # Limiter à 100 000 lignes

# Vérifier les valeurs manquantes
if df.isnull().sum().any():
    df = df.dropna()

# Gestion du déséquilibre des classes
fraud = df[df['fraud'] == 1]
non_fraud = df[df['fraud'] == 0].sample(n=len(fraud), random_state=42)
df_equilibre = pd.concat([fraud, non_fraud])

# Séparer les features et la cible
X = df_equilibre.drop(columns=['fraud'])
y = df_equilibre['fraud'].astype(int)

# Séparer en ensembles d'entraînement et de validation
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Prétraitement : mise à l'échelle des données
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Sauvegarder le scaler pour l'utiliser plus tard
scaler_path = os.path.join(os.path.abspath(os.getcwd()), 'models', 'scaler.pkl')
joblib.dump(scaler, scaler_path)

# Entraîner le modèle Random Forest de Concrete ML
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Compiler le modèle pour le chiffrement homomorphe
model.compile(X_train_scaled)

# Sauvegarder le modèle et les fichiers nécessaires pour le client et le serveur
fhe_directory = os.path.join(os.path.abspath(os.getcwd()), 'models', 'fhe_files')
dev = FHEModelDev(path_dir=fhe_directory, model=model)
dev.save()

print("Modèle entraîné, compilé et sauvegardé.")
