# Library Documentation

Welcome to our project library! This library is designed to process, train, evaluate, and compare machine learning models while providing support for Fully Homomorphic Encryption (FHE).

## Library Structure

### File Organization
- **`library`**: Contains all the main functionalities.
  - **`data`**: Data used for demonstrations.
  - **`models`**: Scripts for training and evaluating models.
  - **`preprocessing`**: Tools for data preprocessing.
- **`results.csv`**: Results from model training or evaluation.
- **`Makefile`**: Automates project steps.
- **`client/` and `server/`**: Scripts to implement client-server communication.

---

## Main Features

### 1. Data Preprocessing
The `data_preprocessing.py` file in `library/preprocessing` is used to load and preprocess data.

### 2. Model Training
The `train.py` file in `library/models` provides a mechanism to train models using `sklearn` and `Concrete ML`.

### 3. Model Comparison
The `model_comparaison.py` file compares the performance of trained models.

### 4. Model Evaluation
The `evaluate.py` file evaluates models on test datasets.

### 5. FHE Model
The `fhe_model.py` file allows training an encrypted model for secure deployment.

---

## How to Use the Library

### 1. Importing the Library
Here’s how to import the library for use in an external notebook or script:

```python
import sys
import os

# Add the library to the Python path
library_path = os.path.abspath(os.path.join(os.getcwd(), 'src'))
if library_path not in sys.path:
    sys.path.append(library_path)

# Import the library
from library import *
```

---

### 2. Using the Makefile

To execute project steps, you can use the provided Makefile:

1. **Data Preprocessing**:
   ```bash
   make preprocess
   ```

2. **Model Training and Comparison**:
   ```bash
   make compare_train
   ```

3. **Model Evaluation**:
   ```bash
   make compare_evaluate
   ```

4. **Training an FHE Model**:
   ```bash
   make train_fhe
   ```

5. **Cleaning Temporary Files**:
   ```bash
   make clean
   ```

---

## Complete Example

Here’s a complete example to understand the workflow:

```python
# Import required modules
from library.preprocessing.data_preprocessing import load_and_preprocess_data
from library.models.train import train_models
from library.models.evaluate import evaluate_models

# Data Preprocessing
data_path = "library/data/card_transdata.csv"
X_train, X_val, X_test, y_train, y_val, y_test = load_and_preprocess_data(data_path)

# Model Training
models = train_models(X_train, y_train, X_val, y_val)

# Model Evaluation
results = evaluate_models(models, X_test, y_test)

# Display Results
print("Model results:", results)
```

---

## Questions or Issues?
For any questions or issues, please refer to the documentation in `docsource/` or contact the development team.