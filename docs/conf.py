# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.append(os.path.abspath("./_ext"))

sys.path.insert(0, os.path.abspath(".."))

from src.jamf_pro_sdk.__about__ import __version__

project = "Jamf Pro SDK for Python"
author = "Bryson Tyrrell"

version = __version__
release = f" v{__version__}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinxcontrib.autodoc_pydantic",
    "apioptions",
]

templates_path = ["_templates"]
exclude_patterns = ["contributors/_autosummary/*.rst"]

add_module_names = False

autodoc_typehints = "both"

autodoc_member_order = "bysource"
autosectionlabel_prefix_document = True

autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_summary_list_order = "bysource"
autodoc_pydantic_model_show_config = False
autodoc_pydantic_model_show_config_summary = False
# autodoc_pydantic_model_undoc_members = False
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_model_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

pygments_style = "default"
pygments_dark_style = "material"

# html_static_path = ["_static"]

html_theme = "furo"

html_title = f"Jamf Pro SDK<br>for Python<br>{release}"

html_theme_options = {
    # "light_logo": "logo.png",
    # "dark_logo": "logo-dark.png",
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF",
    },
    "dark_css_variables": {
        "color-brand-primary": "#FF9900",
        "color-brand-content": "#FF9900",
    },
}

# Concatenate both the class’ and the __init__ method’s docstrings.
autoclass_content = "both"
