"""GitHub MCP Server - provides GitHub operations."""

from typing import Dict, List, Any, Optional
from github import Github
from utils.config import config


class GitHubMCPServer:
    """MCP Server for GitHub operations."""
    
    def __init__(self):
        """Initialize GitHub client."""
        self.github = None
        self.user = None
        self.initialized = False
        
        if config.GITHUB_TOKEN:
            try:
                self.github = Github(config.GITHUB_TOKEN)
                self.user = self.github.get_user()
                self.initialized = True
            except Exception as e:
                print(f"Warning: Failed to initialize GitHub client: {e}")
        else:
            print("Warning: GITHUB_TOKEN not configured. GitHub features will be disabled.")
    
    def _check_initialized(self):
        """Check if GitHub client is initialized."""
        if not self.initialized:
            raise ValueError(
                "GitHub is not configured. Please set GITHUB_TOKEN in .env file. "
                "See SETUP.md for instructions."
            )
    
    def list_repositories(self, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List repositories for a user.
        
        Args:
            username: GitHub username (default: authenticated user)
            
        Returns:
            List of repository information
        """
        self._check_initialized()
        user = self.github.get_user(username) if username else self.user
        repos = []
        for repo in user.get_repos():
            repos.append({
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "private": repo.private,
                "language": repo.language,
            })
        return repos
    
    def create_repository(
        self,
        name: str,
        description: Optional[str] = None,
        private: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new repository.
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether repository is private
            
        Returns:
            Repository information
        """
        self._check_initialized()
        repo = self.user.create_repo(
            name=name,
            description=description,
            private=private
        )
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "url": repo.html_url,
            "private": repo.private,
        }
    
    def get_repository(self, repo_name: str) -> Dict[str, Any]:
        """
        Get repository information.
        
        Args:
            repo_name: Repository full name (owner/repo)
            
        Returns:
            Repository information
        """
        self._check_initialized()
        repo = self.github.get_repo(repo_name)
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "url": repo.html_url,
            "private": repo.private,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
        }
    
    def list_files(self, repo_name: str, path: str = "") -> List[Dict[str, Any]]:
        """
        List files in a repository.
        
        Args:
            repo_name: Repository full name
            path: Path in repository (default: root)
            
        Returns:
            List of file information
        """
        self._check_initialized()
        repo = self.github.get_repo(repo_name)
        contents = repo.get_contents(path)
        files = []
        for content in contents:
            files.append({
                "name": content.name,
                "path": content.path,
                "type": content.type,
                "size": content.size,
                "url": content.html_url,
            })
        return files
    
    def create_file(
        self,
        repo_name: str,
        path: str,
        content: str,
        message: str = "Add file"
    ) -> Dict[str, Any]:
        """
        Create a file in repository.
        
        Args:
            repo_name: Repository full name
            path: File path
            content: File content
            message: Commit message
            
        Returns:
            File information
        """
        self._check_initialized()
        repo = self.github.get_repo(repo_name)
        file = repo.create_file(path, message, content)
        return {
            "path": file["content"].path,
            "url": file["content"].html_url,
            "sha": file["content"].sha,
        }
    
    def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str = ""
    ) -> Dict[str, Any]:
        """
        Create an issue in repository.
        
        Args:
            repo_name: Repository full name
            title: Issue title
            body: Issue body
            
        Returns:
            Issue information
        """
        self._check_initialized()
        repo = self.github.get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body)
        return {
            "number": issue.number,
            "title": issue.title,
            "url": issue.html_url,
            "state": issue.state,
        }


# Global instance
_github_mcp: Optional[GitHubMCPServer] = None


def get_github_mcp() -> GitHubMCPServer:
    """Get or create GitHub MCP server instance."""
    global _github_mcp
    if _github_mcp is None:
        try:
            _github_mcp = GitHubMCPServer()
        except Exception as e:
            print(f"Warning: Could not initialize GitHub MCP: {e}")
            _github_mcp = GitHubMCPServer()  # Will have initialized=False
    return _github_mcp

