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

if [ $? -ne 0 ]; then
  echo "Pylint found issues."
  exit 1
fi

echo "Running Flake8 on notebooks using nbqa..."
nbqa flake8 src/

if [ $? -ne 0 ]; then
  echo "Flake8 found issues in notebooks."
  exit 1
fi

echo "Running Pylint on notebooks using nbqa..."
nbqa pylint src/

if [ $? -ne 0 ]; then
  echo "Pylint found issues in notebooks."
  exit 1
fi

echo "Checking notebook format with nbqa black..."
nbqa black src/ --check

if [ $? -ne 0 ]; then
  echo "Notebooks are not formatted correctly. Please run nbqa black."
  exit 1
fi

echo "Linting passed successfully."
