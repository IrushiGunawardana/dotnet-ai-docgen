"""
.NET Project Parser
Discovers and parses .NET projects, solutions, and C# files.
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class CSharpFile:
    """Represents a C# source file."""
    path: str
    relative_path: str
    namespace: Optional[str] = None
    classes: List[Dict] = None
    interfaces: List[Dict] = None
    enums: List[Dict] = None
    
    def __post_init__(self):
        if self.classes is None:
            self.classes = []
        if self.interfaces is None:
            self.interfaces = []
        if self.enums is None:
            self.enums = []


class DotNetParser:
    """Parses .NET projects and extracts code structure."""
    
    def __init__(self, root_path: str):
        """
        Initialize parser.
        
        Args:
            root_path: Root path of the repository or project
        """
        self.root_path = Path(root_path)
        self.csharp_files: List[CSharpFile] = []
        self.solution_files: List[str] = []
        self.project_files: List[str] = []
    
    def find_all_csharp_files(self) -> List[CSharpFile]:
        """
        Find all C# files in the repository.
        
        Returns:
            List of CSharpFile objects
        """
        csharp_files = []
        
        # Exclude common directories
        exclude_dirs = {
            "bin", "obj", "node_modules", ".git", ".vs", 
            "packages", "TestResults", ".idea", ".vscode",
            "docs", "Documentation"
        }
        
        # Debug: Show what we're searching
        if not self.root_path.exists():
            print(f"Error: Root path does not exist: {self.root_path}")
            return []
        
        print(f"Searching for C# files in: {self.root_path}")
        
        # First, let's see what's actually in the directory
        all_files = list(self.root_path.rglob("*"))
        print(f"Total files/folders found: {len(all_files)}")
        
        # Show directory structure (first level)
        try:
            top_level = [item.name for item in self.root_path.iterdir() if item.is_dir()]
            if top_level:
                print(f"Top-level directories: {', '.join(top_level[:10])}")
        except Exception as e:
            print(f"Could not list directories: {e}")
        
        for cs_file in self.root_path.rglob("*.cs"):
            # Skip files in excluded directories
            if any(excluded in cs_file.parts for excluded in exclude_dirs):
                continue
            
            relative_path = cs_file.relative_to(self.root_path)
            csharp_file = CSharpFile(
                path=str(cs_file),
                relative_path=str(relative_path)
            )
            
            # Parse the file
            self._parse_csharp_file(csharp_file)
            csharp_files.append(csharp_file)
        
        self.csharp_files = csharp_files
        print(f"✓ Found {len(csharp_files)} C# files")
        
        if len(csharp_files) == 0:
            # Show what file types we did find
            found_extensions = {}
            for item in self.root_path.rglob("*"):
                if item.is_file():
                    ext = item.suffix.lower()
                    if ext:
                        found_extensions[ext] = found_extensions.get(ext, 0) + 1
            
            if found_extensions:
                print(f"\nFound file types: {dict(sorted(found_extensions.items(), key=lambda x: x[1], reverse=True)[:10])}")
            else:
                print(f"\nNo files found in repository root: {self.root_path}")
        
        return csharp_files
    
    def find_solution_files(self) -> List[str]:
        """Find all .sln files."""
        solution_files = []
        for sln_file in self.root_path.rglob("*.sln"):
            if ".git" not in str(sln_file):
                solution_files.append(str(sln_file))
        self.solution_files = solution_files
        print(f"✓ Found {len(solution_files)} solution files")
        return solution_files
    
    def find_project_files(self) -> List[str]:
        """Find all .csproj files."""
        project_files = []
        for proj_file in self.root_path.rglob("*.csproj"):
            if ".git" not in str(proj_file):
                project_files.append(str(proj_file))
        self.project_files = project_files
        print(f"✓ Found {len(project_files)} project files")
        return project_files
    
    def _parse_csharp_file(self, csharp_file: CSharpFile):
        """Parse a C# file to extract structure."""
        try:
            with open(csharp_file.path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Extract namespace
            namespace_match = re.search(r'namespace\s+([\w.]+)', content)
            if namespace_match:
                csharp_file.namespace = namespace_match.group(1)
            
            # Extract classes
            class_pattern = r'(?:public\s+|private\s+|internal\s+|protected\s+)?(?:static\s+)?(?:abstract\s+)?(?:sealed\s+)?class\s+(\w+)(?:\s*:\s*[\w\s,<>]+)?\s*\{'
            for match in re.finditer(class_pattern, content):
                class_info = self._extract_class_info(content, match)
                csharp_file.classes.append(class_info)
            
            # Extract interfaces
            interface_pattern = r'(?:public\s+|private\s+|internal\s+)?interface\s+(\w+)(?:\s*:\s*[\w\s,<>]+)?\s*\{'
            for match in re.finditer(interface_pattern, content):
                interface_info = self._extract_interface_info(content, match)
                csharp_file.interfaces.append(interface_info)
            
            # Extract enums
            enum_pattern = r'(?:public\s+|private\s+|internal\s+)?enum\s+(\w+)\s*\{'
            for match in re.finditer(enum_pattern, content):
                enum_info = self._extract_enum_info(content, match)
                csharp_file.enums.append(enum_info)
                
        except Exception as e:
            print(f"Warning: Could not parse {csharp_file.path}: {e}")
    
    def _extract_class_info(self, content: str, match: re.Match) -> Dict:
        """Extract information about a class."""
        class_name = match.group(1)
        start_pos = match.start()
        
        # Find class body
        brace_count = 0
        in_class = False
        methods = []
        
        for i in range(start_pos, len(content)):
            if content[i] == '{':
                brace_count += 1
                in_class = True
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0 and in_class:
                    class_body = content[start_pos:i+1]
                    methods = self._extract_methods(class_body)
                    break
        
        return {
            "name": class_name,
            "methods": methods,
            "full_code": match.group(0) + "..."  # Simplified
        }
    
    def _extract_interface_info(self, content: str, match: re.Match) -> Dict:
        """Extract information about an interface."""
        interface_name = match.group(1)
        return {
            "name": interface_name
        }
    
    def _extract_enum_info(self, content: str, match: re.Match) -> Dict:
        """Extract information about an enum."""
        enum_name = match.group(1)
        return {
            "name": enum_name
        }
    
    def _extract_methods(self, class_body: str) -> List[Dict]:
        """Extract methods from a class body."""
        methods = []
        # Pattern for method signatures
        method_pattern = r'(?:public|private|internal|protected|static)\s+(?:static\s+)?(?:async\s+)?([\w<>\[\],\s]+\??)\s+(\w+)\s*\([^)]*\)'
        
        for match in re.finditer(method_pattern, class_body):
            return_type = match.group(1).strip()
            method_name = match.group(2)
            
            # Extract parameters
            param_match = re.search(r'\(([^)]*)\)', match.group(0))
            parameters = []
            if param_match:
                param_str = param_match.group(1)
                if param_str.strip():
                    for param in param_str.split(','):
                        param = param.strip()
                        if param:
                            parts = param.split()
                            if len(parts) >= 2:
                                parameters.append({
                                    "type": parts[0],
                                    "name": parts[1]
                                })
            
            methods.append({
                "name": method_name,
                "return_type": return_type,
                "parameters": parameters
            })
        
        return methods
    
    def get_project_structure(self) -> Dict:
        """Get overall project structure."""
        return {
            "root_path": str(self.root_path),
            "solution_files": self.solution_files,
            "project_files": self.project_files,
            "csharp_files": [
                {
                    "path": f.path,
                    "relative_path": f.relative_path,
                    "namespace": f.namespace,
                    "classes_count": len(f.classes),
                    "interfaces_count": len(f.interfaces),
                    "enums_count": len(f.enums)
                }
                for f in self.csharp_files
            ]
        }

