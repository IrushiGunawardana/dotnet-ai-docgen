# Configuration file for the Sphinx documentation builder.

project = 'DotNet AI Doc'
copyright = '2025'
author = 'AI Generated'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# Custom CSS for enhanced UI
html_css_files = [
    'custom.css',
]

# Theme options
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980b9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

