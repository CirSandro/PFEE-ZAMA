#!/bin/bash

# Run Flake8
echo "Running Flake8..."
flake8 src/

if [ $? -ne 0 ]; then
  echo "Flake8 found issues."
  exit 1
fi

# Run Pylint
echo "Running Pylint..."
pylint src/

if [ $? -ne 0 ]; then
  echo "Pylint found issues."
  exit 1
fi

echo "Linting passed successfully."
