"""Drive agent using Drive MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from utils.llm import get_default_llm
from mcp_servers.drive_mcp import get_drive_mcp


class DriveAgent:
    """Agent for Google Drive operations."""
    
    def __init__(self):
        """Initialize Drive agent."""
        self.llm = get_default_llm()
        self.drive_mcp = get_drive_mcp()
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def list_files(query: Optional[str] = None, max_results: int = 10) -> str:
            """List files in Google Drive."""
            files = self.drive_mcp.list_files(query, max_results)
            return f"Found {len(files)} files: {[f['name'] for f in files]}"
        
        @tool
        def upload_file(file_path: str, folder_id: Optional[str] = None, name: Optional[str] = None) -> str:
            """Upload a file to Google Drive."""
            file = self.drive_mcp.upload_file(file_path, folder_id, name)
            return f"Uploaded: {file['name']} at {file['url']}"
        
        @tool
        def download_file(file_id: str, output_path: str) -> str:
            """Download a file from Google Drive."""
            result = self.drive_mcp.download_file(file_id, output_path)
            return f"Downloaded to: {result['output_path']}"
        
        @tool
        def create_folder(name: str, parent_id: Optional[str] = None) -> str:
            """Create a folder in Google Drive."""
            folder = self.drive_mcp.create_folder(name, parent_id)
            return f"Created folder: {folder['name']} at {folder['url']}"
        
        return [list_files, upload_file, download_file, create_folder]
    
    def _create_agent(self):
        """Create agent executor."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Google Drive assistant. Use tools to perform Drive operations."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute a Drive operation.
        
        Args:
            query: User query about Drive operations
            
        Returns:
            Result and metadata
        """
        try:
            result = self.agent.invoke({"input": query})
            return {
                "result": result.get("output", ""),
                "agent": "drive",
                "success": True,
            }
        except Exception as e:
            return {
                "result": f"Error: {str(e)}",
                "agent": "drive",
                "success": False,
                "error": str(e),
            }


def get_drive_agent() -> DriveAgent:
    """Get Drive agent instance."""
    return DriveAgent()

