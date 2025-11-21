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
import traceback
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import tempfile
import shutil
from typing import Optional
import importlib.util
import importlib

# Import our modules
from github_repo_handler import GitHubRepoHandler
from dotnet_parser import DotNetParser
from ai_doc_generator import AIDocGenerator
from language_parser import get_parser_for_language

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


def prepare_docs_workspace() -> Path:
    """Prepare an isolated Sphinx workspace inside a writable temporary directory."""
    workspace = Path(tempfile.mkdtemp(prefix='docs_web_'))
    source_dir = workspace / "source"
    static_dir = source_dir / "_static"
    templates_dir = source_dir / "_templates"

    source_dir.mkdir(parents=True, exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    templates_dir.mkdir(exist_ok=True)

    conf_src = Path("docs/source/conf.py")
    conf_dest = source_dir / "conf.py"
    if conf_src.exists():
        shutil.copy(conf_src, conf_dest)
    else:
        conf_content = """
project = 'DotNet AI Doc'
release = '1.0'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
"""
        conf_dest.write_text(conf_content.strip(), encoding='utf-8')

    return workspace


def ensure_package(module_name: str, package_name: Optional[str] = None):
    """Install a missing package at runtime if needed."""
    if importlib.util.find_spec(module_name):
        return
    pkg = package_name or module_name
    subprocess.run(
        [sys.executable, "-m", "pip", "install", pkg],
        capture_output=True,
        text=True,
        check=True
    )


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
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/repo/files', methods=['POST'])
def get_repo_files():
    """Clone repository and list files based on language."""
    global current_repo_path
    
    try:
        data = request.json
        repo_url = data.get('repo_url')
        branch = data.get('branch', 'main')
        language = data.get('language', 'dotnet')
        
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
        
        # Parse files based on language
        lang_parser = get_parser_for_language(language, repo_path)
        try:
            files = lang_parser.find_files()
        except Exception as e:
            return jsonify({'error': f'Parsing failed: {e}'}), 500
        
        files_list = []
        for file_info in files:
            try:
                parsed = lang_parser.parse_file(file_info['path'])
            except Exception as e:
                print(f"Warning: failed to parse {file_info['path']}: {e}")
                parsed = {}
            file_data = {
                'path': file_info['relative_path'],
                'type': file_info.get('type', 'unknown')
            }
            
            # Add language-specific metadata
            if language == 'dotnet':
                file_data.update({
                    'namespace': parsed.get('namespace', 'N/A'),
                    'classes': parsed.get('classes_count', 0),
                    'interfaces': 0,
                    'enums': 0
                })
            elif language == 'angular':
                file_data.update({
                    'class_name': parsed.get('class_name', 'N/A'),
                    'is_component': parsed.get('is_component', False),
                    'is_service': parsed.get('is_service', False)
                })
            elif language == 'html':
                if file_info['type'] == 'js':
                    file_data.update({
                        'functions': parsed.get('functions_count', 0),
                        'classes': parsed.get('classes_count', 0)
                    })
                else:
                    file_data.update(parsed)
            
            files_list.append(file_data)
        
        return jsonify({
            'success': True,
            'files': files_list,
            'total': len(files_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/code', methods=['POST'])
def generate_from_code():
    """Generate documentation from pasted code."""
    global current_docs_dir, generation_status
    
    try:
        data = request.json
        code = data.get('code', '').strip()
        filename = data.get('filename', 'Code.cs')
        language = data.get('language', 'dotnet')
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400
        
        # Reset status
        generation_status = {
            'status': 'generating',
            'progress': 0,
            'message': 'Generating documentation from code...',
            'files_processed': 0,
            'total_files': 1
        }
        
        # Run generation in background thread
        thread = threading.Thread(
            target=generate_code_docs_background,
            args=(code, filename, language)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Documentation generation started'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/file', methods=['POST'])
def generate_from_file():
    """Generate documentation from uploaded file."""
    global current_docs_dir, generation_status
    
    try:
        data = request.json
        code = data.get('code', '').strip()
        filename = data.get('filename', 'uploaded.cs')
        language = data.get('language', 'dotnet')
        
        if not code:
            return jsonify({'error': 'File content is required'}), 400
        
        # Reset status
        generation_status = {
            'status': 'generating',
            'progress': 0,
            'message': 'Generating documentation from file...',
            'files_processed': 0,
            'total_files': 1
        }
        
        # Run generation in background thread
        thread = threading.Thread(
            target=generate_code_docs_background,
            args=(code, filename, language)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Documentation generation started'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_code_docs_background(code, filename, language='dotnet'):
    """Background task to generate documentation from code."""
    global current_docs_dir, generation_status
    
    try:
        docs_workspace = prepare_docs_workspace()
        output_dir = docs_workspace / "source"
        
        # Initialize AI generator
        generator = AIDocGenerator()
        
        generation_status['message'] = 'Generating documentation...'
        generation_status['progress'] = 30
        
        # Generate documentation based on language
        try:
            if language == 'dotnet':
                doc_content = generator.generate_class_documentation(
                    code=code,
                    file_path=filename,
                    namespace=None
                )
            elif language == 'angular':
                doc_content = generator.generate_angular_documentation(
                    code=code,
                    file_path=filename
                )
            elif language == 'html':
                doc_content = generator.generate_html_documentation(
                    code=code,
                    file_path=filename
                )
            else:
                doc_content = generator.generate_class_documentation(
                    code=code,
                    file_path=filename,
                    namespace=None
                )
        except Exception as e:
            error_msg = str(e)
            if "No AI API key" in error_msg or "API key" in error_msg:
                generation_status['status'] = 'error'
                generation_status['message'] = error_msg
                return
            else:
                raise
        
        generation_status['progress'] = 60
        generation_status['message'] = 'Creating documentation file...'
        
        # Create RST file
        safe_name = filename.replace("\\", "_").replace("/", "_").replace(".cs", "")
        rst_file = output_dir / f"{safe_name}.rst"
        
        title = filename.replace("\\", " / ").replace("/", " / ")
        title_line = "=" * len(title)
        
        rst_content = f"""{title}
{title_line}

**File:** ``{filename}``

{doc_content}
"""
        
        with open(rst_file, "w", encoding="utf-8") as f:
            f.write(rst_content)
        
        # Update index
        index_content = f"""Documentation
==============

Welcome to the AI-generated documentation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   {safe_name}
"""
        
        index_file = output_dir / "index.rst"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(index_content)
        
        generation_status['progress'] = 80
        generation_status['message'] = 'Building HTML documentation...'
        
        # Build HTML
        docs_dir = docs_workspace
        ensure_package('sphinx')
        result = subprocess.run(
            [sys.executable, "-m", "sphinx", "-b", "html", "source", "build/html"],
            cwd=docs_dir,
            capture_output=True,
            text=True
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


@app.route('/api/generate', methods=['POST'])
def generate_documentation():
    """Generate documentation for selected files."""
    global current_repo_path, current_docs_dir, generation_status
    
    try:
        data = request.json
        repo_url = data.get('repo_url')
        branch = data.get('branch', 'main')
        selected_files = data.get('files', [])  # List of file paths
        language = data.get('language', 'dotnet')
        
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
            args=(repo_url, branch, selected_files, language)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Documentation generation started'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_docs_background(repo_url, branch, selected_files, language='dotnet'):
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
        
        docs_workspace = prepare_docs_workspace()
        output_dir = docs_workspace / "source"
        
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
                try:
                    doc_content = generator.generate_class_documentation(
                        code=code,
                        file_path=csharp_file.relative_path,
                        namespace=csharp_file.namespace
                    )
                except Exception as e:
                    error_msg = str(e)
                    if "No AI API key" in error_msg or "API key" in error_msg:
                        generation_status['status'] = 'error'
                        generation_status['message'] = error_msg
                        raise
                    else:
                        raise
                
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
        try:
            overview_content = generator.generate_project_overview(project_structure)
        except Exception as e:
            error_msg = str(e)
            if "No AI API key" in error_msg or "API key" in error_msg:
                generation_status['status'] = 'error'
                generation_status['message'] = error_msg
                raise
            else:
                raise
        
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
        
        docs_dir = docs_workspace
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
            generation_status['message'] = 'Documentation generated successfully! PDF download available.'
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
    """Serve the generated documentation files."""
    global current_docs_dir
    if current_docs_dir and current_docs_dir.exists():
        return send_from_directory(str(current_docs_dir), filename)
    return "Documentation not found", 404




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

