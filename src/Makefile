PYTHON = python3
LIB_DIR = library
DATA = $(LIB_DIR)/data/card_transdata.csv
MODULES = $(LIB_DIR)/__init__.py
MODELS = $(LIB_DIR)/models

# Add library to PYTHONPATH
export PYTHONPATH := $(shell pwd)

.PHONY: all data preprocess train evaluate

# Default rule
all: preprocess compare_train compare_evaluate

preprocess: $(MODULES)
	@echo "Preprocessing data..."
	$(PYTHON) -c "from library import load_and_preprocess_data; X_train, X_val, X_test, y_train, y_val, y_test = load_and_preprocess_data('$(DATA)')"

compare_train: preprocess
	@echo "Training multiple models on concrete_ml and sklearn to compare ..."
	$(PYTHON) $(MODELS)/train.py

compare_evaluate: train
	@echo "Evaluation of all trainning models concrete_ml vs sklearn ..."
	$(PYTHON) $(MODELS)/evaluate.py

train_fhe: preprocess
	@echo "Train Random Forest model in FHE for deployment ..."
	$(PYTHON) $(MODELS)/FHEModel.py

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;

pkl_clean:
	find . -name "*.pkl" -exec rm -f {} \;