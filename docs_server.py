"""
Enhanced Documentation Server with Download Features
Serves documentation with modern UI and download capabilities.
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
import zipfile
import shutil
from urllib.parse import urlparse, parse_qs


def find_docs_directory():
    """Find the documentation HTML directory."""
    html_dir = Path("docs/build/html")
    if html_dir.exists() and (html_dir / "index.html").exists():
        return html_dir
    return None


def build_docs_if_needed():
    """Build documentation if it doesn't exist."""
    source_dir = Path("docs/source")
    html_dir = Path("docs/build/html")
    
    if not source_dir.exists():
        print("❌ Documentation source not found.")
        print("   Run: python generate_docs.py <repo-url> first")
        return False
    
    if html_dir.exists() and (html_dir / "index.html").exists():
        return True
    
    print("📦 Building documentation...")
    docs_dir = Path("docs")
    
    try:
        if os.name != 'nt':
            result = subprocess.run(
                ["make", "html"],
                cwd=docs_dir,
                capture_output=True,
                text=True
            )
        else:
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


class EnhancedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Enhanced HTTP handler with download support."""
    
    def __init__(self, *args, docs_dir=None, **kwargs):
        self.docs_dir = docs_dir
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests including download endpoints."""
        parsed_path = urlparse(self.path)
        
        # Handle download requests
        if parsed_path.path == '/download-html':
            self.handle_download_html()
            return
        elif parsed_path.path == '/download-pdf':
            self.handle_download_pdf()
            return
        
        # Serve normal files
        super().do_GET()
    
    def handle_download_html(self):
        """Create and serve HTML documentation as ZIP."""
        try:
            # Create temporary zip file
            zip_path = Path(self.docs_dir) / "documentation.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.docs_dir):
                    # Skip certain directories
                    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__']]
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(self.docs_dir)
                        zipf.write(file_path, arcname)
            
            # Send zip file
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="documentation.zip"')
            self.send_header('Content-Length', str(zip_path.stat().st_size))
            self.end_headers()
            
            with open(zip_path, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)
            
            # Clean up
            zip_path.unlink()
            
        except Exception as e:
            self.send_error(500, f"Error creating zip: {str(e)}")
    
    def handle_download_pdf(self):
        """Redirect to print dialog for PDF download."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
        <script>
            window.print();
            window.close();
        </script>
        ''')
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def inject_download_section(html_dir):
    """Inject download section into index.html."""
    index_file = html_dir / "index.html"
    if not index_file.exists():
        return
    
    try:
        content = index_file.read_text(encoding='utf-8')
        
        # Check if download section already exists
        if 'download-section' in content:
            return
        
        # Find insertion point (after main content starts)
        download_html = '''
        <div class="download-section">
            <h2><i class="fas fa-download"></i> Download Documentation</h2>
            <p style="color: #fff; margin-bottom: 1.5em;">Download the complete documentation in various formats</p>
            <div class="download-buttons">
                <a href="javascript:window.print()" class="download-btn">
                    <i class="fas fa-file-pdf"></i> Download as PDF
                </a>
                <a href="/download-html" class="download-btn">
                    <i class="fas fa-file-archive"></i> Download as HTML (ZIP)
                </a>
                <a href="javascript:downloadAsMarkdown()" class="download-btn">
                    <i class="fas fa-file-alt"></i> Download as Markdown
                </a>
            </div>
        </div>
        <script>
        function downloadAsMarkdown() {
            const content = document.querySelector('.rst-content')?.innerText || document.body.innerText;
            const blob = new Blob([content], { type: 'text/markdown' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'documentation.md';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }
        </script>
        '''
        
        # Inject CSS if not present
        if 'custom.css' not in content:
            css_link = '<link rel="stylesheet" href="_static/custom.css" type="text/css" />'
            content = content.replace('</head>', f'{css_link}\n</head>')
        
        # Inject Font Awesome if not present
        if 'fontawesome' not in content.lower() and 'font-awesome' not in content.lower():
            fontawesome = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />'
            content = content.replace('</head>', f'{fontawesome}\n</head>')
        
        # Inject download section before closing body or after main content
        if '<div class="document">' in content:
            content = content.replace(
                '<div class="document">',
                f'{download_html}\n<div class="document">'
            )
        else:
            content = content.replace('</body>', f'{download_html}\n</body>')
        
        index_file.write_text(content, encoding='utf-8')
        
        # Also inject into other pages
        for html_file in html_dir.glob("*.html"):
            if html_file.name != "index.html":
                try:
                    page_content = html_file.read_text(encoding='utf-8')
                    if 'download-section' not in page_content and '<div class="document">' in page_content:
                        page_content = page_content.replace(
                            '<div class="document">',
                            f'{download_html}\n<div class="document">'
                        )
                        if 'custom.css' not in page_content:
                            css_link = '<link rel="stylesheet" href="_static/custom.css" type="text/css" />'
                            page_content = page_content.replace('</head>', f'{css_link}\n</head>')
                        html_file.write_text(page_content, encoding='utf-8')
                except Exception:
                    pass  # Skip files that can't be modified
                    
    except Exception as e:
        print(f"Warning: Could not inject download section: {e}")


def start_server(port=8000, open_browser=True, auto_build=True):
    """Start enhanced HTTP server."""
    if auto_build:
        if not find_docs_directory():
            if not build_docs_if_needed():
                print("\n❌ Cannot start server - documentation not available.")
                sys.exit(1)
    
    docs_dir = find_docs_directory()
    if not docs_dir:
        print("❌ Documentation not found.")
        sys.exit(1)
    
    # Inject download section and CSS
    inject_download_section(docs_dir)
    
    # Copy custom CSS if it exists
    custom_css_source = Path("docs/source/_static/custom.css")
    custom_css_dest = docs_dir / "_static" / "custom.css"
    if custom_css_source.exists():
        custom_css_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(custom_css_source, custom_css_dest)
    
    original_dir = os.getcwd()
    os.chdir(docs_dir)
    
    try:
        handler = lambda *args, **kwargs: EnhancedHTTPRequestHandler(*args, docs_dir=docs_dir, **kwargs)
        
        with socketserver.TCPServer(("", port), handler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print("\n" + "="*60)
            print("📚 Enhanced Documentation Server")
            print("="*60)
            print(f"\n✓ Serving from: {docs_dir}")
            print(f"✓ Server URL: {server_url}")
            print(f"✓ Documentation: {server_url}/index.html")
            print(f"✓ Download features enabled")
            print("\n" + "="*60)
            print("🌐 Opening in your browser...")
            print("="*60)
            print("\nPress Ctrl+C to stop the server\n")
            
            if open_browser:
                def open_browser_delayed():
                    time.sleep(1.5)
                    webbrowser.open(server_url)
                    print("✓ Browser opened!")
                
                browser_thread = threading.Thread(target=open_browser_delayed)
                browser_thread.daemon = True
                browser_thread.start()
            
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port {port} is already in use.")
            print(f"   Try: python docs_server.py {port + 1}")
        else:
            print(f"\n❌ Error: {e}")
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
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == "--no-browser":
                open_browser = False
            elif arg == "--no-build":
                auto_build = False
            elif arg.isdigit():
                port = int(arg)
            elif arg in ["-h", "--help"]:
                print("Usage: python docs_server.py [port] [options]")
                print("\nOptions:")
                print("  [port]              Port number (default: 8000)")
                print("  --no-browser        Don't open browser automatically")
                print("  --no-build          Don't auto-build documentation")
                print("  -h, --help          Show this help")
                sys.exit(0)
    
    start_server(port, open_browser, auto_build)


if __name__ == "__main__":
    main()

