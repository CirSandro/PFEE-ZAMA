.PHONY: requirements train run_server run_client test

train:
	python models/fhe_model.py

run_server:
	uvicorn src.server.server:app --host 0.0.0.0 --port 8000

run_client:
	uvicorn src.client.client:app --host 127.0.0.1 --port 8001

test:
	PYTHONPATH=. pytest tests/test_api.py

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
# SPHINXOPTS    ?=
# SPHINXBUILD   ?= sphinx-build
# SOURCEDIR     = docsource
# BUILDDIR      = build
DATASETDIR    = dataset/
DATASETFILE   = dataset/credit-card-fraud.zip

# # Put it first so that "make" without argument is like "make help".
# help:
# 	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# .PHONY: help Makefile

# clean:
# 	find . -type f -name "*.py[co]" -delete
# 	find . -type d -name "__pycache__" -delete

all: requirements setup-dataset

requirements:
	pip install -r requirements.txt

# Recipe to create the data directory if it doesn't exist
create-data-dir:
	@mkdir -p $(DATASETDIR)

# Recipe to download the dataset from Kaggle (only if it doesn't already exist)
download-dataset: create-data-dir
	@if [ ! -f "$(DATASETFILE)" ]; then \
		echo "Downloading dataset..."; \
		kaggle datasets download dhanushnarayananr/credit-card-fraud -p $(DATASETDIR); \
	else \
		echo "Dataset already downloaded."; \
	fi

# Recipe to unzip the downloaded dataset (only if it hasn't been unzipped yet)
unzip-dataset: download-dataset
	@if [ ! -f "$(DATASETDIR)card_transdata.csv" ]; then \
		echo "Unzipping dataset..."; \
		unzip $(DATASETFILE) -d $(DATASETDIR); \
	else \
		echo "Dataset already unzipped."; \
	fi

# Complete recipe that downloads and unzips the dataset
setup-dataset: download-dataset unzip-dataset

# # Catch-all target: route all unknown targets to Sphinx using the new
# # "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
