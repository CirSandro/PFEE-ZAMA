.PHONY: setup train run_server run_client test

setup:
	pip install -r requirements.txt

train:
	python models/FHEModel.py

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
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docsource
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

requirements:
	pip install -r requirements.txt

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)