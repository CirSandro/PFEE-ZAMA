# PFEE-ZAMA

## Table of Contents

- [Introduction](#introduction)
- [About This Project](#about-this-project)
  - [Project Overview](#project-overview)
  - [Project Goals](#project-goals)
  - [Key Technologies](#key-technologies)
  - [Project Contributions](#project-contributions)
- [Deployment](#deployment)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Training the Model](#training-the-model)
  - [Running the Server and Client](#running-the-server-and-client)
- [Workflow](#workflow)
  - [Prediction Process](#prediction-process)
- [Usage](#usage)
  - [Using the Makefile](#using-the-makefile)
  - [Making Predictions via the API Client](#making-predictions-via-the-api-client)
- [Continuous Integration](#continuous-integration)
- [Dataset](#dataset)

## Introduction

As the use of sensitive personal data in machine learning models becomes increasingly prevalent, ensuring data privacy and security is paramount. PFEE-ZAMA addresses these concerns by leveraging advanced techniques such as Privacy-Preserving Machine Learning (PPML) and Fully Homomorphic Encryption (FHE). This project enables secure predictions without compromising the confidentiality of user data.

## About This Project

### Project Overview

PFEE-ZAMA is a capstone project (Projet de Fin d'Études Encadré) developed in collaboration with Zama, a leader in homomorphic encryption. The primary objective is to explore and implement Privacy-Preserving Machine Learning (PPML) and Fully Homomorphic Encryption (FHE) using Concrete ML, an open-source library developed by Zama. The project focuses on creating a machine learning model capable of making secure predictions while ensuring data privacy.

### Project Goals

- **Secure Predictions**: Develop a machine learning model that can make predictions on encrypted data without decrypting it.
- **Data Privacy**: Ensure that all user data remains confidential throughout the prediction process.
- **Scalability**: Create a client-server architecture that can handle multiple prediction requests efficiently.
- **Ease of Use**: Provide a user-friendly interface and deployment process using Makefile for streamlined operations.

### Key Technologies

- **PPML (Privacy-Preserving Machine Learning)**: Techniques that allow machine learning models to be trained and used without exposing sensitive data.
- **FHE (Fully Homomorphic Encryption)**: A form of encryption that enables computations on encrypted data without needing to decrypt it first.
- **Concrete ML**: An open-source library developed by Zama, integrating FHE with machine learning for privacy-preserving predictions.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Uvicorn**: A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.
- **Sphinx**: A tool that makes it easy to create intelligent and beautiful documentation.

### Project Contributions

1. **Understanding and Implementing PPML and FHE**: Conducted an in-depth study of PPML and FHE principles and their practical implementation.
2. **Model Development**: Created and trained a machine learning model using Concrete ML to perform secure predictions.
3. **Data Privacy**: Ensured that all data used in the predictions remained encrypted, maintaining user confidentiality and data integrity.
4. **Client-Server Architecture**: Developed a scalable client-server system to handle encrypted prediction requests.
5. **Documentation**: Provided comprehensive documentation using Sphinx for ease of understanding and deployment.

## Deployment

### Prerequisites

Before deploying PFEE-ZAMA, ensure that you have the following installed on your system:

- **Python**: Version 3.10.12
- **pip**: Python package installer
- **Make**: Build automation tool
- **Git**: Version control system

### Setup

1. **Clone the Repository**

   ```sh
   git clone git@github.com:CirSandro/PFEE-ZAMA.git
   cd PFEE-ZAMA
   ```

2. **Install Dependencies**

   Use the provided Makefile to install all necessary dependencies.

   ```sh
   make all
   ```

   This command will install all packages listed in `requirements.txt` using `pip` and download the dataset.



### Training the Model

Before running the server and client, train the machine learning model using the following command:

```sh
make train
```

This will execute the `models/FHEModel.py` script, which:

- Loads and preprocesses the dataset.
- Trains a Random Forest classifier using Concrete ML.
- Compiles the model for homomorphic encryption.
- Saves the encrypted model and necessary files for deployment.

### Running the Server and Client

PFEE-ZAMA follows a client-server architecture where the server handles encrypted prediction requests, and the client manages user interactions and data encryption.

1. **Run the Server**

   ```sh
   make run_server
   ```

   This command starts the FastAPI server on `http://0.0.0.0:8000`, ready to receive encrypted prediction requests.

2. **Run the Client**

   In a new terminal window, execute:

   ```sh
   make run_client
   ```

   This starts the FastAPI client on `http://127.0.0.1:8001`. The client will send encrypted evaluation keys to the server upon startup.

## Workflow

### Prediction Process

When a user makes a prediction via the API client, the following workflow occurs:

1. **User Input**: The user provides input data through the client’s API endpoint (`/predict`).

2. **Data Preprocessing**: The client application scales the input data using a pre-trained scaler (`scaler.pkl`).

3. **Data Encryption**: The scaled data is encrypted using Concrete ML's FHE capabilities. The encryption process ensures that the data remains confidential during computation.

4. **Sending Encrypted Data**: The encrypted data is sent to the server’s `/predict` endpoint via a POST request.

5. **Server Processing**: The server receives the encrypted data and uses the encrypted model to perform the prediction directly on the encrypted input without decrypting it.

6. **Encrypted Prediction**: The server returns the encrypted prediction result to the client.

7. **Decryption**: The client decrypts the received prediction to obtain the final result.

8. **Result Delivery**: The client returns the decrypted prediction to the user.

This workflow ensures that at no point is the sensitive user data exposed in an unencrypted form, maintaining data privacy and security throughout the process.

## Usage

### Using the Makefile

The Makefile simplifies common tasks such as setting up the environment, training the model, running the server and client, and testing. Below are the available commands:

- **Setup Dependencies**

  ```sh
  make all
  ```

  Installs all required Python packages listed in `requirements.txt`.

- **Train the Model**

  ```sh
  make train
  ```

  Executes the training script to develop and compile the FHE-enabled machine learning model.

- **Run the Server**

  ```sh
  make run_server
  ```

  Starts the FastAPI server on `http://0.0.0.0:8000`. You can have the interface at `http://0.0.0.0:8000/docs`.

- **Run the Client**

  ```sh
  make run_client
  ```

  Starts the FastAPI client on `http://127.0.0.1:8001`. You can have the interface at `http://127.0.0.1:8001/docs`.

- **Run Tests**

  ```sh
  make test
  ```

  Executes the test suite located in `./tests/test_api.py` to ensure the API is functioning correctly.

### Making Predictions via the API Client

To make predictions using the client API, follow these steps:

1. **Ensure Server and Client are Running**

   Make sure both the server and client are up and running using the Makefile commands mentioned above.

2. **Send a Prediction Request**

   You can use tools like `curl`, `HTTPie`, or Postman to send a POST request to the client’s `/predict` endpoint. Below is an example using `curl`:

   ```sh
   curl -X POST "http://127.0.0.1:8001/predict" \
   -H "Content-Type: application/json" \
   -d '{
         "distance_from_home": 10.5,
         "distance_from_last_transaction": 5.2,
         "ratio_to_median_purchase_price": 1.3,
         "repeat_retailer": 1,
         "used_chip": 0,
         "used_pin_number": 1,
         "online_order": 0
       }'
   ```

3. **Receive the Prediction**

   The client will process the input, encrypt it, send it to the server, and return the decrypted prediction. The response will look like:

   ```json
   {
     "prediction": 0
   }
   ```

   Here, `0` could represent a non-fraudulent transaction, and `1` could represent a fraudulent one, depending on your model's encoding.

## Continuous Integration

PFEE-ZAMA utilizes GitHub Actions for continuous integration to ensure code quality and maintainability.

### Configuration

The CI workflow is defined in `.github/workflows/ci.yml`. It includes steps for:

- **Checking Out the Repository**
- **Setting Up Python Environment**
- **Installing Dependencies**
- **Running Tests**
- **Validating Commit Messages**

### Validating Commit Messages

Commit messages must adhere to the following format to maintain consistency and clarity:

- `feat: Feature description`
- `fix: Description of the fix`
- `docs: Description of documentation`
- `style: Description of style changes`
- `refactor: Description of refactoring`
- `test: Description of tests`
- `chore: Description of maintenance tasks`

A commit message validation hook is included and executed during the CI process to enforce these conventions.

### Installation of Dependencies

Dependencies are managed via `requirements.txt`. To install them manually, use:

```sh
pip install -r requirements.txt
```

## Dataset

The project uses the [Credit Card Fraud Detection](https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud) dataset from Kaggle. The dataset contains transactions made by credit cards in September 2013 by European cardholders. It presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions.


This setup ensures that you can deploy the PFEE-ZAMA system efficiently and start making secure predictions with ease.

---

For more detailed documentation, refer to the [PFEE-ZAMA Documentation](./docsource/index.rst).
[![Documentation Status](https://readthedocs.org/projects/pfee-zama/badge/?version=latest)](https://pfee-zama.readthedocs.io/en/latest/)
