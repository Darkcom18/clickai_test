"""Drive agent using Drive MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from utils.llm import get_default_llm
from mcp_servers.drive_mcp import get_drive_mcp


class DriveAgent:
    """Agent for Google Drive operations."""
    
    def __init__(self):
        """Initialize Drive agent."""
        self.llm = get_default_llm()
        self.drive_mcp = get_drive_mcp()
        self.tools = self._create_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Google Drive assistant. Use tools to perform Drive operations."),
            ("human", "{input}"),
        ])
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def list_files(query: Optional[str] = None, max_results: int = 10) -> str:
            """List files in Google Drive."""
            try:
                files = self.drive_mcp.list_files(query, max_results)
                return f"Found {len(files)} files: {[f['name'] for f in files]}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def upload_file(file_path: str, folder_id: Optional[str] = None, name: Optional[str] = None) -> str:
            """Upload a file to Google Drive."""
            try:
                file = self.drive_mcp.upload_file(file_path, folder_id, name)
                return f"Uploaded: {file['name']} at {file['url']}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def download_file(file_id: str, output_path: str) -> str:
            """Download a file from Google Drive."""
            try:
                result = self.drive_mcp.download_file(file_id, output_path)
                return f"Downloaded to: {result['output_path']}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def create_folder(name: str, parent_id: Optional[str] = None) -> str:
            """Create a folder in Google Drive."""
            try:
                folder = self.drive_mcp.create_folder(name, parent_id)
                return f"Created folder: {folder['name']} at {folder['url']}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        return [list_files, upload_file, download_file, create_folder]
    
    def execute(self, query: str) -> Dict[str, Any]:
        """Execute a Drive operation."""
        try:
            response = self.llm_with_tools.invoke(self.prompt.format(input=query))
            
            if hasattr(response, 'tool_calls') and response.tool_calls:
                tool_results = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get("name", "")
                    tool_args = tool_call.get("args", {})
                    
                    for tool in self.tools:
                        if tool.name == tool_name:
                            result = tool.invoke(tool_args)
                            tool_results.append(f"{tool_name}: {result}")
                            break
                
                final_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a Google Drive assistant. Summarize the tool results."),
                    ("human", f"User asked: {query}\n\nTool results: {', '.join(tool_results)}"),
                ])
                final_response = (final_prompt | self.llm | StrOutputParser()).invoke({})
                
                return {
                    "result": final_response,
                    "agent": "drive",
                    "success": True,
                }
            else:
                return {
                    "result": response.content if hasattr(response, 'content') else str(response),
                    "agent": "drive",
                    "success": True,
                }
        except Exception as e:
            return {
                "result": f"Error: {str(e)}. Google Drive may not be configured. See SETUP.md for instructions.",
                "agent": "drive",
                "success": False,
                "error": str(e),
            }


def get_drive_agent() -> DriveAgent:
    """Get Drive agent instance."""
    return DriveAgent()
