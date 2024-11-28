"""
This file contains the configuration for the Sphinx documentation builder.
It is used to generate the documentation for the PFEE-ZAMA project.
"""

# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

PROJECT = "PFEE-ZAMA" # UPERCASE
COPYRIGHT = "2024, CARDI-FERRONI-GIRAUD-HOLARD-MOYO-SKALLI" # UPERCASE
AUTHOR = "CARDI-FERRONI-GIRAUD-HOLARD-MOYO-SKALLI" # UPERCASE

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

HTML_THEME = "alabaster" # UPERCASE
html_static_path = ["_static"]
