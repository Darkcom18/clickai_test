"""n8n agent using n8n MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from utils.llm import get_default_llm
from mcp_servers.n8n_mcp import get_n8n_mcp


class N8NAgent:
    """Agent for n8n workflow operations."""
    
    def __init__(self):
        """Initialize n8n agent."""
        self.llm = get_default_llm()
        self.n8n_mcp = get_n8n_mcp()
        self.tools = self._create_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an n8n workflow assistant that can send emails via webhooks.

**Email Workflow Configuration:**
- Webhook URL: https://gavinpham.app.n8n.cloud/webhook/send-email
- Method: POST
- Expected data format: {"to": "email", "subject": "...", "body": "..."}

**When user asks to send emails (natural language):**
Examples:
- "send email to john@example.com about meeting"
- "email quoc.trung1802@gmail.com with subject Test"
- "gửi email cho abc@gmail.com về cuộc họp chiều nay"

**Your tasks:**
1. Parse email details from natural language:
   - Recipient (to): Extract from "to X", "cho X", email address
   - Subject: Extract from "about X", "with subject X", "về X"
   - Body: Generate professional email body based on context

2. If subject/body not provided, generate them intelligently

3. Call trigger_workflow with:
   - workflow_id: "https://gavinpham.app.n8n.cloud/webhook/send-email" (full URL)
   - data: {"to": "...", "subject": "...", "body": "..."}

4. Always use the FULL webhook URL, not relative path

**For generic workflow triggers:**
- Use trigger_workflow tool with workflow_id and optional data
- Support both full URLs and relative paths
"""),
            ("human", "{input}"),
        ])
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def trigger_workflow(workflow_id: str, data: Optional[dict] = None) -> str:
            """Trigger an n8n workflow via webhook.

            Args:
                workflow_id: Full webhook URL or workflow path (e.g., "send-email")
                data: Data to send to workflow. For email workflows: {"to": "email", "subject": "...", "body": "..."}
            """
            try:
                # Smart default: if no full URL provided and workflow_id looks like email endpoint
                if not workflow_id.startswith(('http://', 'https://')) and 'email' in workflow_id.lower():
                    workflow_id = "https://gavinpham.app.n8n.cloud/webhook/send-email"

                result = self.n8n_mcp.trigger_workflow(workflow_id, data)

                if result["success"]:
                    response_data = result.get('data', {})
                    if isinstance(response_data, dict) and response_data.get('success'):
                        return f"✅ {response_data.get('message', 'Workflow triggered successfully')}"
                    return f"✅ Workflow triggered successfully: {response_data}"
                else:
                    return f"❌ Failed to trigger workflow: {result}"
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        @tool
        def test_connection() -> str:
            """Test connection to n8n instance."""
            try:
                result = self.n8n_mcp.test_connection()
                if result["connected"]:
                    return "✅ Connected to n8n successfully"
                else:
                    return f"❌ Connection failed: {result.get('error', '')}"
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        return [trigger_workflow, test_connection]
    
    def execute(self, query: str) -> Dict[str, Any]:
        """Execute an n8n operation."""
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
                    ("system", "You are an n8n assistant. Summarize the tool results."),
                    ("human", f"User asked: {query}\n\nTool results: {', '.join(tool_results)}"),
                ])
                final_response = (final_prompt | self.llm | StrOutputParser()).invoke({})
                
                return {
                    "result": final_response,
                    "agent": "n8n",
                    "success": True,
                }
            else:
                return {
                    "result": response.content if hasattr(response, 'content') else str(response),
                    "agent": "n8n",
                    "success": True,
                }
        except Exception as e:
            return {
                "result": f"Error: {str(e)}. n8n may not be configured. See SETUP.md for instructions.",
                "agent": "n8n",
                "success": False,
                "error": str(e),
            }


def get_n8n_agent() -> N8NAgent:
    """Get n8n agent instance."""
    return N8NAgent()
