"""
Module for evaluating the performance of trained models
using both Sklearn and FHE implementations.
"""


import time
import pandas as pd
from sklearn.metrics import accuracy_score
import joblib


def evaluate_models(models, datasets, training_times):
    """
    Evaluate trained models and compare performance.

    Args:
        models (dict): Dictionary containing Sklearn and FHE models.
        datasets (dict): Dictionary with training and validation datasets.
        training_times (dict): Training times for Sklearn models.

    Returns:
        list: A list of dictionaries containing evaluation results.
    """
    x_train, y_train = datasets['x_train'], datasets['y_train'].astype(int)
    x_val, y_val = datasets['x_val'], datasets['y_val'].astype(int)

    results = []
    for model_name, (sk_model, fhe_model) in models.items():
        obj = {
            "Model": model_name
        }
        # Predict with Sklearn model
        sk_y_pred = sk_model.predict(x_val)
        obj["Sklearn Accuracy"] = accuracy_score(y_val, sk_y_pred)

        # Train FHE model
        start_time = time.time()
        fhe_model.fit(x_train, y_train)
        obj["FHE Time"] = time.time() - start_time
        # Predict with FHE model
        fhe_y_pred = fhe_model.predict(x_val)
        obj["FHE Accuracy"] = accuracy_score(y_val, fhe_y_pred)

        # Calculate ratios
        obj["Sklearn Time"] = training_times[model_name]
        obj["Time Ratio (FHE/Sklearn)"] = obj["FHE Time"] / obj["Sklearn Time"]
        obj["Accuracy Ratio (FHE/Sklearn)"] = \
            obj["FHE Accuracy"] / obj["Sklearn Accuracy"]

        # Store results
        results.append(obj)

    return results


def main():
    """
    Main function to load data, evaluate models, and save results.
    """
    # Load data and models
    x_train, x_val, _, y_train, y_val, _ = \
        joblib.load('library/data/processed_data.pkl')

    datasets = {
        "x_train": x_train,
        "x_val": x_val,
        "y_train": y_train,
        "y_val": y_val
    }

    trained_models, training_times = \
        joblib.load('trained_and_times_models.pkl')

    # Evaluate models
    results = evaluate_models(trained_models, datasets, training_times)

    # Save results to a CSV file
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)


if __name__ == "__main__":
    main()
