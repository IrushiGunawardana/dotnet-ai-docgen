"""Setup script for web application directories."""
from pathlib import Path
import shutil

# Create directories
dirs = [
    "web_static",
    "docs_web/source/_static",
    "docs_web/source/_templates"
]

for dir_path in dirs:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    print(f"Created: {dir_path}")

# Copy custom CSS if it exists
css_source = Path("docs/source/_static/custom.css")
css_dest = Path("docs_web/source/_static/custom.css")

if css_source.exists():
    shutil.copy2(css_source, css_dest)
    print(f"Copied CSS: {css_dest}")

print("\nWeb application setup complete!")

