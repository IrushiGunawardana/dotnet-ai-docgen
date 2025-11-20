"""
Web Application for .NET Documentation Generator
Provides a web UI for generating documentation from GitHub repositories.
"""
import os
import sys
import json
import subprocess
import webbrowser
import threading
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import tempfile
import shutil

# Import our modules
from github_repo_handler import GitHubRepoHandler
from dotnet_parser import DotNetParser
from ai_doc_generator import AIDocGenerator

app = Flask(__name__, 
            template_folder='web_templates',
            static_folder='web_static',
            static_url_path='')
CORS(app)

# Global state
current_repo_path = None
current_docs_dir = None
generation_status = {
    'status': 'idle',
    'progress': 0,
    'message': '',
    'files_processed': 0,
    'total_files': 0
}


@app.route('/')
def index():
    """Serve the main UI."""
    return render_template('index.html')


@app.route('/api/repo/info', methods=['POST'])
def get_repo_info():
    """Get repository information and list branches."""
    try:
        data = request.json
        repo_url = data.get('repo_url')
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Get repo info and branches
        handler = GitHubRepoHandler(repo_url)
        repo_info = handler.get_repo_info()
        branches = handler.get_branches()
        
        return jsonify({
            'success': True,
            'repo_info': repo_info,
            'branches': branches
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/repo/files', methods=['POST'])
def get_repo_files():
    """Clone repository and list C# files."""
    global current_repo_path
    
    try:
        data = request.json
        repo_url = data.get('repo_url')
        branch = data.get('branch', 'main')
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Clean up previous repo if exists
        if current_repo_path and os.path.exists(current_repo_path):
            try:
                shutil.rmtree(current_repo_path)
            except:
                pass
        
        # Clone repository
        temp_dir = tempfile.mkdtemp(prefix='docgen_web_')
        handler = GitHubRepoHandler(repo_url, branch)
        repo_path = handler.clone_repository(temp_dir)
        current_repo_path = repo_path
        
        # Parse files
        parser = DotNetParser(repo_path)
        parser.find_all_csharp_files()
        
        files_list = []
        for cs_file in parser.csharp_files:
            files_list.append({
                'path': cs_file.relative_path,
                'namespace': cs_file.namespace or 'N/A',
                'classes': len(cs_file.classes),
                'interfaces': len(cs_file.interfaces),
                'enums': len(cs_file.enums)
            })
        
        return jsonify({
            'success': True,
            'files': files_list,
            'total': len(files_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def generate_documentation():
    """Generate documentation for selected files."""
    global current_repo_path, current_docs_dir, generation_status
    
    try:
        data = request.json
        repo_url = data.get('repo_url')
        branch = data.get('branch', 'main')
        selected_files = data.get('files', [])  # List of file paths
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        if not selected_files:
            return jsonify({'error': 'Please select at least one file'}), 400
        
        # Reset status
        generation_status = {
            'status': 'generating',
            'progress': 0,
            'message': 'Starting documentation generation...',
            'files_processed': 0,
            'total_files': len(selected_files)
        }
        
        # Run generation in background thread
        thread = threading.Thread(
            target=generate_docs_background,
            args=(repo_url, branch, selected_files)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Documentation generation started'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_docs_background(repo_url, branch, selected_files):
    """Background task to generate documentation."""
    global current_repo_path, current_docs_dir, generation_status
    
    try:
        # Clone repo if not already cloned
        if not current_repo_path or not os.path.exists(current_repo_path):
            temp_dir = tempfile.mkdtemp(prefix='docgen_web_')
            handler = GitHubRepoHandler(repo_url, branch)
            current_repo_path = handler.clone_repository(temp_dir)
        
        # Parse files
        parser = DotNetParser(current_repo_path)
        parser.find_all_csharp_files()
        
        # Filter selected files
        selected_cs_files = [
            f for f in parser.csharp_files 
            if f.relative_path in selected_files
        ]
        
        # Create output directory
        output_dir = Path("docs_web/source")
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "_static").mkdir(exist_ok=True)
        (output_dir / "_templates").mkdir(exist_ok=True)
        
        # Initialize AI generator
        generator = AIDocGenerator()
        
        # Generate documentation for each file
        total = len(selected_cs_files)
        file_docs = []
        
        for idx, csharp_file in enumerate(selected_cs_files):
            try:
                generation_status['message'] = f'Processing {csharp_file.relative_path}...'
                generation_status['files_processed'] = idx
                generation_status['progress'] = int((idx / total) * 100)
                
                # Read file content
                with open(csharp_file.path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
                
                # Generate documentation
                doc_content = generator.generate_class_documentation(
                    code=code,
                    file_path=csharp_file.relative_path,
                    namespace=csharp_file.namespace
                )
                
                # Create RST file
                safe_name = csharp_file.relative_path.replace("\\", "_").replace("/", "_").replace(".cs", "")
                rst_file = output_dir / f"{safe_name}.rst"
                
                title = csharp_file.relative_path.replace("\\", " / ").replace("/", " / ")
                title_line = "=" * len(title)
                
                rst_content = f"""{title}
{title_line}

**File:** ``{csharp_file.relative_path}``

**Namespace:** ``{csharp_file.namespace or "N/A"}``

{doc_content}
"""
                
                with open(rst_file, "w", encoding="utf-8") as f:
                    f.write(rst_content)
                
                file_docs.append({
                    'name': safe_name,
                    'title': title,
                    'path': csharp_file.relative_path
                })
                
            except Exception as e:
                generation_status['message'] = f'Error processing {csharp_file.relative_path}: {str(e)}'
                continue
        
        # Generate project overview
        generation_status['message'] = 'Generating project overview...'
        project_structure = parser.get_project_structure()
        overview_content = generator.generate_project_overview(project_structure)
        
        overview_rst = f"""Project Overview
===============

{overview_content}
"""
        
        overview_file = output_dir / "project_overview.rst"
        with open(overview_file, "w", encoding="utf-8") as f:
            f.write(overview_rst)
        
        # Update index
        update_index_rst(output_dir, file_docs, has_overview=True)
        
        # Build HTML
        generation_status['message'] = 'Building HTML documentation...'
        generation_status['progress'] = 90
        
        docs_dir = Path("docs_web")
        if os.name != 'nt':
            result = subprocess.run(
                ["sphinx-build", "-b", "html", "source", "build/html"],
                cwd=docs_dir,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["sphinx-build", "-b", "html", "source", "build/html"],
                cwd=docs_dir,
                capture_output=True,
                text=True,
                shell=True
            )
        
        if result.returncode == 0:
            current_docs_dir = docs_dir / "build" / "html"
            generation_status['status'] = 'completed'
            generation_status['progress'] = 100
            generation_status['message'] = 'Documentation generated successfully!'
        else:
            generation_status['status'] = 'error'
            generation_status['message'] = f'Build failed: {result.stderr}'
            
    except Exception as e:
        generation_status['status'] = 'error'
        generation_status['message'] = f'Error: {str(e)}'


def update_index_rst(output_dir, file_docs, has_overview=False):
    """Update the main index.rst file."""
    index_content = """DotNet AI Documentation
======================

Welcome to the AI-generated technical documentation for your .NET codebase.
This documentation is automatically generated using AI and Sphinx.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

"""
    
    if has_overview:
        index_content += "   project_overview\n\n"
    
    index_content += "   API Reference\n   :caption: API Reference:\n\n"
    
    for doc in file_docs:
        index_content += f"   {doc['name']}\n"
    
    index_file = output_dir / "index.rst"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(index_content)


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get generation status."""
    return jsonify(generation_status)


@app.route('/api/view', methods=['GET'])
def view_docs():
    """Check if docs are ready and return URL."""
    global current_docs_dir
    
    if current_docs_dir and (current_docs_dir / "index.html").exists():
        return jsonify({
            'success': True,
            'url': '/docs/index.html'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Documentation not ready yet'
        }), 404


@app.route('/docs/<path:filename>')
def serve_docs(filename):
    """Serve generated documentation files."""
    global current_docs_dir
    
    if current_docs_dir and current_docs_dir.exists():
        return send_from_directory(str(current_docs_dir), filename)
    else:
        return "Documentation not found", 404


@app.route('/api/download/<format>', methods=['GET'])
def download_docs(format):
    """Download documentation in various formats."""
    global current_docs_dir
    
    if not current_docs_dir or not current_docs_dir.exists():
        return jsonify({'error': 'Documentation not found'}), 404
    
    if format == 'html':
        # Create ZIP
        import zipfile
        zip_path = tempfile.mktemp(suffix='.zip')
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(current_docs_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(current_docs_dir)
                    zipf.write(file_path, arcname)
        
        return send_file(zip_path, as_attachment=True, download_name='documentation.zip')
    
    return jsonify({'error': 'Invalid format'}), 400


if __name__ == '__main__':
    # Create necessary directories
    Path("docs_web/source/_static").mkdir(parents=True, exist_ok=True)
    Path("docs_web/source/_templates").mkdir(parents=True, exist_ok=True)
    
    # Copy Sphinx config if needed
    if not Path("docs_web/source/conf.py").exists():
        if Path("docs/source/conf.py").exists():
            shutil.copy("docs/source/conf.py", "docs_web/source/conf.py")
        else:
            # Create basic config
            with open("docs_web/source/conf.py", "w") as f:
                f.write("""
project = 'DotNet AI Doc'
copyright = '2025'
author = 'AI Generated'
release = '1.0'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
""")
    
    print("="*60)
    print("🌐 Web UI Server Starting...")
    print("="*60)
    print("Open your browser to: http://localhost:5000")
    print("="*60)
    
    # Open browser after delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://localhost:5000")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

