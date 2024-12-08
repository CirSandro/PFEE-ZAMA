#!/bin/bash

# Run Flake8
echo "Running Flake8..."
flake8 .

if [ $? -ne 0 ]; then
  echo "Flake8 found issues."
  exit 1
fi

# Run Pylint
echo "Running Pylint..."
pylint .

if [ $? -ne 0 ]; then
  echo "Pylint found issues."
  exit 1
fi

echo "Linting passed successfully."
