from .preprocessing import data_preprocessing


# Chargement et prétraitement des données
def load_and_preprocess_data(data_path):
    data = data_preprocessing.load_data(data_path)
    X_train, X_val, X_test, y_train, y_val, y_test = data_preprocessing.preprocess_data(data)
    return X_train, X_val, X_test, y_train, y_val, y_test

# # Entraînement des modèles
# def train_models(X_train, y_train):
#     models = train.get_models()
#     train.train_models(models, X_train, y_train)
#     return models

# # Évaluation des modèles
# def evaluate_models(models, X_val, y_val):
#     evaluation_results = evaluate.evaluate_model(models, X_val, y_val)
#     return evaluation_results
