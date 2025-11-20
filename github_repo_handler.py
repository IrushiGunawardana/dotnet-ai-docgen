"""
GitHub Repository Handler
Handles cloning and accessing GitHub repositories for documentation generation.
"""
import os
import subprocess
import shutil
import tempfile
import stat
import time
from pathlib import Path
from typing import Optional, List
import requests


class GitHubRepoHandler:
    """Handles GitHub repository operations."""
    
    def __init__(self, repo_url: str, branch: str = "main", token: Optional[str] = None):
        """
        Initialize GitHub repository handler.
        
        Args:
            repo_url: GitHub repository URL (https://github.com/owner/repo or owner/repo)
            branch: Branch to clone (default: main)
            token: GitHub personal access token (optional, for private repos)
        """
        self.repo_url = repo_url
        self.branch = branch
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.temp_dir = None
        self.repo_path = None
        
    def _normalize_repo_url(self) -> str:
        """Normalize repository URL."""
        if self.repo_url.startswith("http"):
            return self.repo_url
        elif "/" in self.repo_url:
            return f"https://github.com/{self.repo_url}"
        else:
            raise ValueError(f"Invalid repository URL: {self.repo_url}")
    
    def clone_repository(self, target_dir: Optional[str] = None) -> str:
        """
        Clone the GitHub repository to a temporary or specified directory.
        
        Args:
            target_dir: Optional target directory. If None, uses temp directory.
            
        Returns:
            Path to the cloned repository
        """
        repo_url = self._normalize_repo_url()
        
        if target_dir:
            self.repo_path = Path(target_dir)
            if self.repo_path.exists():
                shutil.rmtree(self.repo_path)
        else:
            self.temp_dir = tempfile.mkdtemp(prefix="docgen_")
            self.repo_path = Path(self.temp_dir) / "repo"
        
        # Prepare clone URL with token if provided
        clone_url = repo_url
        if self.token and "github.com" in repo_url:
            # Insert token into URL for authentication
            clone_url = repo_url.replace("https://", f"https://{self.token}@")
        
        try:
            # Clone repository
            cmd = ["git", "clone", "--depth", "1", "--branch", self.branch, clone_url, str(self.repo_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✓ Successfully cloned repository: {repo_url} (branch: {self.branch})")
            return str(self.repo_path)
        except subprocess.CalledProcessError as e:
            # If branch doesn't exist, try default branch
            if self.branch != "main":
                print(f"Branch '{self.branch}' not found, trying 'main'...")
                self.branch = "main"
                cmd = ["git", "clone", "--depth", "1", "--branch", self.branch, clone_url, str(self.repo_path)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"✓ Successfully cloned repository: {repo_url} (branch: {self.branch})")
                return str(self.repo_path)
            raise Exception(f"Failed to clone repository: {e.stderr}")
    
    def get_repo_info(self) -> dict:
        """
        Get repository information from GitHub API.
        
        Returns:
            Dictionary with repository information
        """
        repo_url = self._normalize_repo_url()
        if not repo_url.startswith("https://github.com/"):
            return {}
        
        # Extract owner and repo name
        parts = repo_url.replace("https://github.com/", "").split("/")
        if len(parts) < 2:
            return {}
        
        owner, repo = parts[0], parts[1].replace(".git", "")
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": data.get("name"),
                    "description": data.get("description"),
                    "language": data.get("language"),
                    "stars": data.get("stargazers_count"),
                    "forks": data.get("forks_count"),
                    "default_branch": data.get("default_branch")
                }
        except Exception as e:
            print(f"Warning: Could not fetch repo info: {e}")
        
        return {}
    
    def get_branches(self) -> List[str]:
        """
        Get list of branches from GitHub API.
        
        Returns:
            List of branch names
        """
        repo_url = self._normalize_repo_url()
        if not repo_url.startswith("https://github.com/"):
            return []
        
        # Extract owner and repo name
        parts = repo_url.replace("https://github.com/", "").split("/")
        if len(parts) < 2:
            return []
        
        owner, repo = parts[0], parts[1].replace(".git", "")
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            branches = []
            page = 1
            per_page = 100
            
            while True:
                params = {"page": page, "per_page": per_page}
                response = requests.get(api_url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if not data:  # No more branches
                        break
                    
                    branches.extend([branch["name"] for branch in data])
                    
                    # If we got fewer than per_page, we're done
                    if len(data) < per_page:
                        break
                    
                    page += 1
                elif response.status_code == 404:
                    # Repository not found or no access
                    break
                else:
                    # Rate limit or other error
                    if response.status_code == 403:
                        # Try without auth for public repos
                        if self.token:
                            headers.pop("Authorization", None)
                            continue
                    break
            
            # Sort branches: default branch first, then alphabetically
            repo_info = self.get_repo_info()
            default_branch = repo_info.get("default_branch", "main")
            
            if default_branch in branches:
                branches.remove(default_branch)
                branches.insert(0, default_branch)
            
            return branches if branches else ["main", "master"]  # Fallback
            
        except Exception as e:
            print(f"Warning: Could not fetch branches: {e}")
            # Return common default branches as fallback
            return ["main", "master", "develop"]
    
    def cleanup(self):
        """Clean up temporary directory if created."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                # On Windows, files might be locked, so try multiple times
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        # Change file permissions first (Windows)
                        if os.name == 'nt':  # Windows
                            def handle_remove_readonly(func, path, exc):
                                os.chmod(path, stat.S_IWRITE)
                                func(path)
                            shutil.rmtree(self.temp_dir, onerror=handle_remove_readonly)
                        else:
                            shutil.rmtree(self.temp_dir)
                        print(f"✓ Cleaned up temporary directory: {self.temp_dir}")
                        return
                    except PermissionError:
                        if attempt < max_attempts - 1:
                            time.sleep(0.5)  # Wait before retry
                            continue
                        raise
            except Exception as e:
                # Don't fail if cleanup fails - just warn
                print(f"Warning: Could not clean up temporary directory: {e}")
                print(f"  You may need to manually delete: {self.temp_dir}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()

