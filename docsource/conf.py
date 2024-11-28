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

project = "PFEE-ZAMA"  # pylint: disable=C0103
copyright = "2024, CARDI-FERRONI-GIRAUD-HOLARD-MOYO-SKALLI"  # pylint: disable=C0103, W0622
author = "CARDI-FERRONI-GIRAUD-HOLARD-MOYO-SKALLI"  # pylint: disable=C0103

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"  # pylint: disable=C0103
html_static_path = ["_static"]

autodoc_typehints = "description"  # pylint: disable=C0103
