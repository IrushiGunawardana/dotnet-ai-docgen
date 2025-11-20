"""
Simple HTTP Server for Viewing Documentation
Serves the generated Sphinx HTML documentation locally with a web UI.
"""
import os
import sys
import webbrowser
import http.server
import socketserver
from pathlib import Path
import threading
import time
import subprocess


def find_docs_directory():
    """Find the documentation HTML directory."""
    # Check if docs are built
    html_dir = Path("docs/build/html")
    if html_dir.exists() and (html_dir / "index.html").exists():
        return html_dir
    
    return None


def build_docs_if_needed():
    """Build documentation if it doesn't exist."""
    source_dir = Path("docs/source")
    html_dir = Path("docs/build/html")
    
    # Check if we have source files
    if not source_dir.exists():
        print("❌ Documentation source not found.")
        print("   Run: python generate_docs.py <repo-url> first")
        return False
    
    # Check if already built
    if html_dir.exists() and (html_dir / "index.html").exists():
        return True
    
    # Try to build
    print("📦 Building documentation...")
    docs_dir = Path("docs")
    
    try:
        # Try make (Linux/Mac)
        if os.name != 'nt':
            result = subprocess.run(
                ["make", "html"],
                cwd=docs_dir,
                capture_output=True,
                text=True
            )
        else:
            # Windows
            result = subprocess.run(
                ["make.bat", "html"],
                cwd=docs_dir,
                capture_output=True,
                text=True,
                shell=True
            )
        
        if result.returncode == 0:
            print("✓ Documentation built successfully!")
            return True
        else:
            print("⚠️  Build command failed. Trying alternative method...")
            # Try direct sphinx-build
            result = subprocess.run(
                ["sphinx-build", "-b", "html", "source", "build/html"],
                cwd=docs_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✓ Documentation built successfully!")
                return True
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False
    except FileNotFoundError:
        print("❌ Sphinx not found. Please install: pip install sphinx sphinx-rtd-theme")
        return False


def start_server(port=8000, open_browser=True, auto_build=True):
    """Start a simple HTTP server to serve the documentation."""
    # Try to build if needed
    if auto_build:
        if not find_docs_directory():
            if not build_docs_if_needed():
                print("\n❌ Cannot start server - documentation not available.")
                print("\nTo generate documentation:")
                print("  1. python generate_docs.py <github-repo-url>")
                print("  2. python serve_docs.py")
                sys.exit(1)
    
    docs_dir = find_docs_directory()
    if not docs_dir:
        print("❌ Documentation not found. Please build it first.")
        sys.exit(1)
    
    # Store original directory
    original_dir = os.getcwd()
    
    # Change to docs directory
    os.chdir(docs_dir)
    
    # Create server with CORS support
    class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            super().end_headers()
        
        def log_message(self, format, *args):
            # Suppress default logging, or customize it
            pass
    
    try:
        with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print("\n" + "="*60)
            print("📚 Documentation Server")
            print("="*60)
            print(f"\n✓ Serving from: {docs_dir}")
            print(f"✓ Server URL: {server_url}")
            print(f"✓ Documentation: {server_url}/index.html")
            print("\n" + "="*60)
            print("🌐 Opening in your browser...")
            print("="*60)
            print("\nPress Ctrl+C to stop the server\n")
            
            # Open browser after a short delay
            if open_browser:
                def open_browser_delayed():
                    time.sleep(1.5)
                    webbrowser.open(server_url)
                    print("✓ Browser opened!")
                
                browser_thread = threading.Thread(target=open_browser_delayed)
                browser_thread.daemon = True
                browser_thread.start()
            
            # Start server
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port {port} is already in use.")
            print(f"   Try: python serve_docs.py {port + 1}")
        else:
            print(f"\n❌ Error starting server: {e}")
        os.chdir(original_dir)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped.")
        os.chdir(original_dir)
        sys.exit(0)


def main():
    """Main function."""
    port = 8000
    open_browser = True
    auto_build = True
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == "--no-browser":
                open_browser = False
            elif arg == "--no-build":
                auto_build = False
            elif arg.isdigit():
                port = int(arg)
            elif arg in ["-h", "--help"]:
                print("Usage: python serve_docs.py [port] [options]")
                print("\nOptions:")
                print("  [port]              Port number (default: 8000)")
                print("  --no-browser        Don't open browser automatically")
                print("  --no-build          Don't auto-build documentation")
                print("  -h, --help          Show this help message")
                print("\nExamples:")
                print("  python serve_docs.py")
                print("  python serve_docs.py 8080")
                print("  python serve_docs.py --no-browser")
                sys.exit(0)
    
    start_server(port, open_browser, auto_build)


if __name__ == "__main__":
    main()
