"""
Enhanced .NET Documentation Generator
Connects to GitHub repositories and generates comprehensive documentation.
"""
import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path
from github_repo_handler import GitHubRepoHandler
from dotnet_parser import DotNetParser
from ai_doc_generator import AIDocGenerator


def ensure_docs_structure():
    """Ensure docs directory structure exists."""
    docs_source = Path("docs/source")
    docs_source.mkdir(parents=True, exist_ok=True)
    (docs_source / "_static").mkdir(exist_ok=True)
    (docs_source / "_templates").mkdir(exist_ok=True)


def generate_file_documentation(parser: DotNetParser, generator: AIDocGenerator, output_dir: Path):
    """Generate documentation for each C# file."""
    print("\n" + "="*60)
    print("Generating file documentation...")
    print("="*60)
    
    file_docs = []
    
    for csharp_file in parser.csharp_files:
        print(f"\nProcessing: {csharp_file.relative_path}")
        
        try:
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
            
            # Create title from file path
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
                "name": safe_name,
                "title": title,
                "path": csharp_file.relative_path
            })
            
            print(f"  ✓ Generated: {rst_file.name}")
            
        except Exception as e:
            print(f"  ✗ Error processing {csharp_file.relative_path}: {e}")
            continue
    
    return file_docs


def generate_project_overview(parser: DotNetParser, generator: AIDocGenerator, output_dir: Path, repo_info: dict):
    """Generate project overview documentation."""
    print("\n" + "="*60)
    print("Generating project overview...")
    print("="*60)
    
    project_structure = parser.get_project_structure()
    overview_content = generator.generate_project_overview(project_structure)
    
    # Add repository information if available
    repo_section = ""
    if repo_info:
        repo_section = f"""
Repository Information
-----------------------

- **Name:** {repo_info.get('name', 'N/A')}
- **Description:** {repo_info.get('description', 'N/A')}
- **Language:** {repo_info.get('language', 'N/A')}
- **Stars:** {repo_info.get('stars', 'N/A')}
- **Forks:** {repo_info.get('forks', 'N/A')}

"""
    
    overview_rst = f"""Project Overview
===============

{repo_section}

{overview_content}
"""
    
    overview_file = output_dir / "project_overview.rst"
    with open(overview_file, "w", encoding="utf-8") as f:
        f.write(overview_rst)
    
    print(f"✓ Generated: {overview_file.name}")
    return overview_file


def update_index_rst(output_dir: Path, file_docs: list, has_overview: bool):
    """Update the main index.rst file."""
    index_content = """DotNet AI Documentation
======================

Welcome to the AI-generated technical documentation for your .NET codebase.
This documentation is automatically generated using AI (Azure OpenAI/OpenAI/OpenRouter) and Sphinx.

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
    
    print(f"✓ Updated: {index_file.name}")


def main():
    """Main function to generate documentation from GitHub repository."""
    # Load environment variables
    if os.getenv("GITHUB_ACTIONS") != "true":
        from dotenv import load_dotenv
        load_dotenv()
    
    # Get repository URL from environment or command line
    repo_url = os.getenv("GITHUB_REPO_URL") or (sys.argv[1] if len(sys.argv) > 1 else None)
    branch = os.getenv("GITHUB_BRANCH", "main")
    
    if not repo_url:
        print("Usage: python generate_docs.py <github_repo_url> [branch]")
        print("   or set GITHUB_REPO_URL environment variable")
        print("\nExamples:")
        print("  python generate_docs.py https://github.com/owner/repo")
        print("  python generate_docs.py https://github.com/owner/repo main")
        print("  python generate_docs.py https://github.com/owner/repo develop")
        print("  python generate_docs.py https://github.com/owner/repo feature/docs")
        sys.exit(1)
    
    if len(sys.argv) > 2:
        branch = sys.argv[2]
    
    print("="*60)
    print(".NET AI Documentation Generator")
    print("="*60)
    print(f"Repository: {repo_url}")
    print(f"Branch: {branch}")
    print("="*60)
    
    # Ensure docs structure
    ensure_docs_structure()
    output_dir = Path("docs/source")
    
    # Clone repository
    with GitHubRepoHandler(repo_url, branch) as repo_handler:
        repo_path = repo_handler.clone_repository()
        repo_info = repo_handler.get_repo_info()
        
        # Parse .NET project
        print("\n" + "="*60)
        print("Parsing .NET project...")
        print("="*60)
        parser = DotNetParser(repo_path)
        parser.find_solution_files()
        parser.find_project_files()
        parser.find_all_csharp_files()
        
        if not parser.csharp_files:
            print("\n" + "="*60)
            print("ERROR: No C# files found in the repository!")
            print("="*60)
            print("\nPossible reasons:")
            print("  1. Repository might be empty or only contain non-C# files")
            print("  2. C# files might be in a subdirectory (check the output above)")
            print("  3. Wrong branch - try specifying a different branch")
            print("  4. Repository structure might be different than expected")
            print("\nTo specify a different branch:")
            print(f"  python generate_docs.py {repo_url} <branch-name>")
            print("\nExample:")
            print(f"  python generate_docs.py {repo_url} develop")
            print(f"  python generate_docs.py {repo_url} feature/docs")
            sys.exit(1)
        
        # Initialize AI generator
        generator = AIDocGenerator()
        
        # Generate project overview
        overview_file = generate_project_overview(parser, generator, output_dir, repo_info)
        
        # Generate file documentation
        file_docs = generate_file_documentation(parser, generator, output_dir)
        
        # Update index
        update_index_rst(output_dir, file_docs, has_overview=True)
        
        print("\n" + "="*60)
        print("Documentation generation complete!")
        print("="*60)
        print(f"\nGenerated {len(file_docs)} file documentation(s)")
        
        # Auto-build and open browser
        print("\n" + "="*60)
        print("🚀 Building and opening documentation...")
        print("="*60)
        
        try:
            # Build documentation
            docs_dir = Path("docs")
            print("📦 Building HTML documentation...")
            
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
                
                # Start server
                print("\n🌐 Starting enhanced documentation server...")
                print("   (This will open your browser automatically)")
                
                server_script = Path(__file__).parent / "docs_server.py"
                if server_script.exists():
                    print(f"\n✓ Server will be available at: http://localhost:8000")
                    print(f"   Features: Modern UI, Download options, Search")
                    print("\n" + "="*60)
                    
                    # Start server in new process
                    if os.name == 'nt':
                        # Windows - open in new console window
                        subprocess.Popen(
                            [sys.executable, str(server_script)],
                            creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
                        )
                    else:
                        # Linux/Mac - run in background
                        subprocess.Popen(
                            [sys.executable, str(server_script)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    
                    # Give server time to start, then open browser
                    print("⏳ Starting server...")
                    time.sleep(3)
                    webbrowser.open("http://localhost:8000")
                    
                    print("\n✅ Documentation server started!")
                    print("   ✓ Browser opened automatically")
                    print("   ✓ Visit: http://localhost:8000")
                    print("   ✓ Press Ctrl+C in server window to stop")
                else:
                    print("⚠️  Enhanced server not found. Using basic server...")
                    from serve_docs import start_server
                    import threading
                    server_thread = threading.Thread(
                        target=start_server,
                        args=(8000, True, False),
                        daemon=False
                    )
                    server_thread.start()
                    time.sleep(2)
                    webbrowser.open("http://localhost:8000")
            else:
                print("⚠️  Build had issues. You can manually build with:")
                print("   cd docs && make html")
                print("\nThen view with: python docs_server.py")
        except Exception as e:
            print(f"⚠️  Could not auto-start server: {e}")
            print("\nYou can manually start the server:")
            print("   python docs_server.py")


if __name__ == "__main__":
    main()
