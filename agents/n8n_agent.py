"""n8n agent using n8n MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from utils.llm import get_default_llm
from mcp_servers.n8n_mcp import get_n8n_mcp


class N8NAgent:
    """Agent for n8n workflow operations."""
    
    def __init__(self):
        """Initialize n8n agent."""
        self.llm = get_default_llm()
        self.n8n_mcp = get_n8n_mcp()
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def trigger_workflow(workflow_id: str, data: Optional[dict] = None) -> str:
            """Trigger an n8n workflow via webhook."""
            result = self.n8n_mcp.trigger_workflow(workflow_id, data)
            if result["success"]:
                return f"Workflow triggered successfully: {result.get('data', '')}"
            else:
                return f"Failed to trigger workflow: {result}"
        
        @tool
        def test_connection() -> str:
            """Test connection to n8n instance."""
            result = self.n8n_mcp.test_connection()
            if result["connected"]:
                return "Connected to n8n successfully"
            else:
                return f"Connection failed: {result.get('error', '')}"
        
        return [trigger_workflow, test_connection]
    
    def _create_agent(self):
        """Create agent executor."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an n8n workflow assistant. Use tools to trigger workflows."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute an n8n operation.
        
        Args:
            query: User query about n8n operations
            
        Returns:
            Result and metadata
        """
        try:
            result = self.agent.invoke({"input": query})
            return {
                "result": result.get("output", ""),
                "agent": "n8n",
                "success": True,
            }
        except Exception as e:
            return {
                "result": f"Error: {str(e)}",
                "agent": "n8n",
                "success": False,
                "error": str(e),
            }


def get_n8n_agent() -> N8NAgent:
    """Get n8n agent instance."""
    return N8NAgent()

