"""
Language-specific parsers for different programming languages.
"""
from pathlib import Path
from typing import List, Dict, Optional
import re


class LanguageParser:
    """Base class for language parsers."""
    
    def __init__(self, root_path: str, language: str):
        self.root_path = Path(root_path)
        self.language = language
        self.files: List[Dict] = []
    
    def find_files(self) -> List[Dict]:
        """Find files based on language-specific extensions."""
        raise NotImplementedError
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse a file and extract structure."""
        raise NotImplementedError


class DotNetParser(LanguageParser):
    """Parser for .NET/C# files."""
    
    def __init__(self, root_path: str):
        super().__init__(root_path, 'dotnet')
        self.extensions = ['.cs']
        self.exclude_dirs = {
            "bin", "obj", "node_modules", ".git", ".vs", 
            "packages", "TestResults", ".idea", ".vscode",
            "docs", "Documentation"
        }
    
    def find_files(self) -> List[Dict]:
        """Find all C# files."""
        files = []
        try:
            for cs_file in self.root_path.rglob("*.cs"):
                try:
                    if any(excluded in cs_file.parts for excluded in self.exclude_dirs):
                        continue
        
                    relative_path = cs_file.relative_to(self.root_path)
                    files.append({
                        'path': str(cs_file),
                        'relative_path': str(relative_path),
                        'type': 'csharp'
                    })
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            pass
        return files
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse C# file structure."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract namespace
        namespace_match = re.search(r'namespace\s+([\w.]+)', content)
        namespace = namespace_match.group(1) if namespace_match else None
        
        # Extract classes
        classes = []
        class_pattern = r'(?:public\s+|private\s+|internal\s+|protected\s+)?(?:static\s+)?(?:abstract\s+)?(?:sealed\s+)?class\s+(\w+)'
        for match in re.finditer(class_pattern, content):
            classes.append(match.group(1))
        
        return {
            'namespace': namespace,
            'classes': classes,
            'classes_count': len(classes)
        }


class AngularParser(LanguageParser):
    """Parser for Angular/TypeScript files."""
    
    def __init__(self, root_path: str):
        super().__init__(root_path, 'angular')
        self.extensions = ['.ts', '.html', '.css', '.scss']
        self.exclude_dirs = {
            "node_modules", ".git", ".angular", "dist", "build",
            "coverage", ".idea", ".vscode", "docs"
        }
    
    def find_files(self) -> List[Dict]:
        """Find Angular-related files."""
        files = []
        for ext in self.extensions:
            try:
                for file in self.root_path.rglob(f"*{ext}"):
                    try:
                        if any(excluded in file.parts for excluded in self.exclude_dirs):
                            continue
                        
                        relative_path = file.relative_to(self.root_path)
                        files.append({
                            'path': str(file),
                            'relative_path': str(relative_path),
                            'type': ext[1:]  # Remove dot
                        })
                    except (PermissionError, OSError):
                        continue
            except (PermissionError, OSError):
                continue
        return files
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse Angular/TypeScript file structure."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        file_ext = Path(file_path).suffix
        
        if file_ext == '.ts':
            # Extract class/component
            class_match = re.search(r'export\s+class\s+(\w+)', content)
            component_match = re.search(r'@Component', content)
            service_match = re.search(r'@Injectable', content)
            
            return {
                'class_name': class_match.group(1) if class_match else None,
                'is_component': component_match is not None,
                'is_service': service_match is not None,
                'is_module': '@NgModule' in content
            }
        elif file_ext == '.html':
            return {
                'is_template': True,
                'has_components': len(re.findall(r'<[\w-]+', content)) > 0
            }
        else:
            return {}


class HTMLParser(LanguageParser):
    """Parser for HTML/CSS/JavaScript files."""
    
    def __init__(self, root_path: str):
        super().__init__(root_path, 'html')
        self.extensions = ['.html', '.css', '.js']
        self.exclude_dirs = {
            "node_modules", ".git", "dist", "build", ".idea", ".vscode"
        }
    
    def find_files(self) -> List[Dict]:
        """Find HTML/CSS/JS files."""
        files = []
        for ext in self.extensions:
            try:
                for file in self.root_path.rglob(f"*{ext}"):
                    try:
                        if any(excluded in file.parts for excluded in self.exclude_dirs):
                            continue
                        
                        relative_path = file.relative_to(self.root_path)
                        files.append({
                            'path': str(file),
                            'relative_path': str(relative_path),
                            'type': ext[1:]
                        })
                    except (PermissionError, OSError):
                        continue
            except (PermissionError, OSError):
                continue
        return files
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse HTML/CSS/JS file structure."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        file_ext = Path(file_path).suffix
        
        if file_ext == '.html':
            return {
                'has_scripts': '<script' in content,
                'has_styles': '<style' in content or '<link' in content,
                'elements': len(re.findall(r'<[\w-]+', content))
            }
        elif file_ext == '.css':
            return {
                'rules': len(re.findall(r'\{[^}]+\}', content)),
                'has_media_queries': '@media' in content
            }
        elif file_ext == '.js':
            functions = re.findall(r'function\s+(\w+)', content)
            classes = re.findall(r'class\s+(\w+)', content)
            return {
                'functions': functions,
                'classes': classes,
                'functions_count': len(functions),
                'classes_count': len(classes)
            }
        return {}


def get_parser_for_language(language: str, root_path: str):
    """Get appropriate parser for language."""
    if language == 'dotnet':
        return DotNetParser(root_path)
    elif language == 'angular':
        return AngularParser(root_path)
    elif language == 'html':
        return HTMLParser(root_path)
    else:
        # Default to .NET
        return DotNetParser(root_path)

