"""GitHub agent using GitHub MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from utils.llm import get_default_llm
from mcp_servers.github_mcp import get_github_mcp


class GitHubAgent:
    """Agent for GitHub operations."""
    
    def __init__(self):
        """Initialize GitHub agent."""
        self.llm = get_default_llm()
        self.github_mcp = get_github_mcp()
        self.tools = self._create_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a GitHub assistant. Use tools to perform GitHub operations. When user asks about GitHub, use the available tools."),
            ("human", "{input}"),
        ])
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def list_repos(username: Optional[str] = None) -> str:
            """List GitHub repositories for a user."""
            try:
                repos = self.github_mcp.list_repositories(username)
                return f"Found {len(repos)} repositories: {[r['name'] for r in repos]}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def create_repo(name: str, description: Optional[str] = None, private: bool = False) -> str:
            """Create a new GitHub repository."""
            try:
                repo = self.github_mcp.create_repository(name, description, private)
                return f"Created repository: {repo['name']} at {repo['url']}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def get_repo_info(repo_name: str) -> str:
            """Get information about a repository."""
            try:
                repo = self.github_mcp.get_repository(repo_name)
                return f"Repository: {repo['name']}, Stars: {repo['stars']}, Language: {repo['language']}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def list_files(repo_name: str, path: str = "") -> str:
            """List files in a repository."""
            try:
                files = self.github_mcp.list_files(repo_name, path)
                return f"Found {len(files)} items: {[f['name'] for f in files]}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def create_file(repo_name: str, path: str, content: str, message: str = "Add file") -> str:
            """Create a file in a repository."""
            try:
                file = self.github_mcp.create_file(repo_name, path, content, message)
                return f"Created file: {file['path']} at {file['url']}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        return [list_repos, create_repo, get_repo_info, list_files, create_file]
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute a GitHub operation.
        
        Args:
            query: User query about GitHub operations
            
        Returns:
            Result and metadata
        """
        try:
            # Get response with tool calls
            response = self.llm_with_tools.invoke(self.prompt.format(input=query))
            
            # Check if tools were called
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # Execute tools and get results
                tool_results = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get("name", "")
                    tool_args = tool_call.get("args", {})
                    
                    # Find and execute tool
                    for tool in self.tools:
                        if tool.name == tool_name:
                            result = tool.invoke(tool_args)
                            tool_results.append(f"{tool_name}: {result}")
                            break
                
                # Get final response
                final_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a GitHub assistant. Summarize the tool results for the user."),
                    ("human", f"User asked: {query}\n\nTool results: {', '.join(tool_results)}"),
                ])
                final_response = (final_prompt | self.llm | StrOutputParser()).invoke({})
                
                return {
                    "result": final_response,
                    "agent": "github",
                    "success": True,
                }
            else:
                # No tools called, return direct response
                return {
                    "result": response.content if hasattr(response, 'content') else str(response),
                    "agent": "github",
                    "success": True,
                }
        except Exception as e:
            return {
                "result": f"Error: {str(e)}. GitHub may not be configured. See SETUP.md for instructions.",
                "agent": "github",
                "success": False,
                "error": str(e),
            }


def get_github_agent() -> GitHubAgent:
    """Get GitHub agent instance."""
    return GitHubAgent()
