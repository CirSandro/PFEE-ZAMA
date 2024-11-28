import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


def load_data(path):
    """
    Load dataset from the given path.
    """
    df = pd.read_csv(path)
    return df


def preprocess_data(df):
    """
    Balance the dataset to have equal numbers of fraud and non-fraud cases.
    Split the dataset into training, validation, and test sets.
    Scale the features using StandardScaler.
    """

    fraud = df[df['fraud'] == 1]
    non_fraud = df[df['fraud'] == 0].sample(n=len(fraud), random_state=42)
    df = pd.concat([fraud, non_fraud])
    X = df.drop(columns=['fraud'])
    y = df['fraud']

    # Split into training, validation, and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2,
                                                      random_state=42, stratify=y_train)

    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # save the preprocessed data
    joblib.dump((X_train_scaled, X_val_scaled, X_test_scaled,
                 y_train, y_val, y_test), 'library/data/processed_data.pkl')

    return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test


def main():
    # load the proprecessed data
    data_path = "library/data/card_transdata.csv"
    data = load_data(data_path)
    preprocess_data(data)


if __name__ == "__main__":
    main()
