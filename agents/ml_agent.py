"""ML agent using ML MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from utils.llm import get_default_llm
from mcp_servers.ml_mcp import get_ml_mcp


class MLAgent:
    """Agent for ML model operations."""
    
    def __init__(self):
        """Initialize ML agent."""
        self.llm = get_default_llm()
        self.ml_mcp = get_ml_mcp()
        self.tools = self._create_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an ML assistant. Use tools to train models, make predictions, and manage ML models."),
            ("human", "{input}"),
        ])
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def find_datasets(task_type: str, description: Optional[str] = None) -> str:
            """Find datasets for ML training."""
            try:
                datasets = self.ml_mcp.find_datasets(task_type, description)
                return f"Found {len(datasets)} datasets: {[d['name'] for d in datasets]}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def train_model(dataset_path: str, target_column: str, model_name: str, task_type: Optional[str] = None) -> str:
            """Train a ML model from dataset."""
            try:
                result = self.ml_mcp.train_model(dataset_path, target_column, model_name, task_type)
                return f"Trained model '{model_name}': {result['task_type']} with score {result['score']:.4f}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def predict(model_name: str, features: dict) -> str:
            """Make prediction with a trained model."""
            try:
                result = self.ml_mcp.predict(model_name, features)
                return f"Prediction: {result['prediction']}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def list_models() -> str:
            """List all trained models."""
            try:
                models = self.ml_mcp.list_models()
                return f"Available models: {[m['name'] for m in models]}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def create_sample_salary_dataset() -> str:
            """Create a sample salary prediction dataset."""
            try:
                path = self.ml_mcp.create_sample_salary_dataset()
                return f"Created sample dataset at: {path}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        return [find_datasets, train_model, predict, list_models, create_sample_salary_dataset]
    
    def execute(self, query: str) -> Dict[str, Any]:
        """Execute an ML operation."""
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
                    ("system", "You are an ML assistant. Summarize the tool results."),
                    ("human", f"User asked: {query}\n\nTool results: {', '.join(tool_results)}"),
                ])
                final_response = (final_prompt | self.llm | StrOutputParser()).invoke({})
                
                return {
                    "result": final_response,
                    "agent": "ml",
                    "success": True,
                }
            else:
                return {
                    "result": response.content if hasattr(response, 'content') else str(response),
                    "agent": "ml",
                    "success": True,
                }
        except Exception as e:
            return {
                "result": f"Error: {str(e)}",
                "agent": "ml",
                "success": False,
                "error": str(e),
            }


def get_ml_agent() -> MLAgent:
    """Get ML agent instance."""
    return MLAgent()
