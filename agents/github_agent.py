"""GitHub agent using GitHub MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from utils.llm import get_default_llm
from mcp_servers.github_mcp import get_github_mcp


class GitHubAgent:
    """Agent for GitHub operations."""
    
    def __init__(self):
        """Initialize GitHub agent."""
        self.llm = get_default_llm()
        self.github_mcp = get_github_mcp()
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def list_repos(username: Optional[str] = None) -> str:
            """List GitHub repositories for a user."""
            repos = self.github_mcp.list_repositories(username)
            return f"Found {len(repos)} repositories: {[r['name'] for r in repos]}"
        
        @tool
        def create_repo(name: str, description: Optional[str] = None, private: bool = False) -> str:
            """Create a new GitHub repository."""
            repo = self.github_mcp.create_repository(name, description, private)
            return f"Created repository: {repo['name']} at {repo['url']}"
        
        @tool
        def get_repo_info(repo_name: str) -> str:
            """Get information about a repository."""
            repo = self.github_mcp.get_repository(repo_name)
            return f"Repository: {repo['name']}, Stars: {repo['stars']}, Language: {repo['language']}"
        
        @tool
        def list_files(repo_name: str, path: str = "") -> str:
            """List files in a repository."""
            files = self.github_mcp.list_files(repo_name, path)
            return f"Found {len(files)} items: {[f['name'] for f in files]}"
        
        @tool
        def create_file(repo_name: str, path: str, content: str, message: str = "Add file") -> str:
            """Create a file in a repository."""
            file = self.github_mcp.create_file(repo_name, path, content, message)
            return f"Created file: {file['path']} at {file['url']}"
        
        return [list_repos, create_repo, get_repo_info, list_files, create_file]
    
    def _create_agent(self):
        """Create agent executor."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a GitHub assistant. Use tools to perform GitHub operations."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute a GitHub operation.
        
        Args:
            query: User query about GitHub operations
            
        Returns:
            Result and metadata
        """
        try:
            result = self.agent.invoke({"input": query})
            return {
                "result": result.get("output", ""),
                "agent": "github",
                "success": True,
            }
        except Exception as e:
            return {
                "result": f"Error: {str(e)}",
                "agent": "github",
                "success": False,
                "error": str(e),
            }


def get_github_agent() -> GitHubAgent:
    """Get GitHub agent instance."""
    return GitHubAgent()

