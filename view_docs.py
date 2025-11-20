"""
Quick Documentation Viewer
Builds and serves documentation in one command.
"""
import subprocess
import sys
from pathlib import Path


def main():
    """Build and serve documentation."""
    # Check if docs source exists
    if not Path("docs/source").exists():
        print("❌ Documentation not generated yet.")
        print("   Run: python generate_docs.py <repo-url> first")
        sys.exit(1)
    
    # Import and run serve_docs (which will auto-build)
    from serve_docs import start_server
    start_server(port=8000, open_browser=True, auto_build=True)


if __name__ == "__main__":
    main()

