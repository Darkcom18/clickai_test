"""ML agent using ML MCP server."""

from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from utils.llm import get_default_llm
from mcp_servers.ml_mcp import get_ml_mcp


class MLAgent:
    """Agent for ML model operations."""
    
    def __init__(self):
        """Initialize ML agent."""
        self.llm = get_default_llm()
        self.ml_mcp = get_ml_mcp()
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """Create LangChain tools from MCP functions."""
        
        @tool
        def find_datasets(task_type: str, description: Optional[str] = None) -> str:
            """Find datasets for ML training."""
            datasets = self.ml_mcp.find_datasets(task_type, description)
            return f"Found {len(datasets)} datasets: {[d['name'] for d in datasets]}"
        
        @tool
        def train_model(dataset_path: str, target_column: str, model_name: str, task_type: Optional[str] = None) -> str:
            """Train a ML model from dataset."""
            result = self.ml_mcp.train_model(dataset_path, target_column, model_name, task_type)
            return f"Trained model '{model_name}': {result['task_type']} with score {result['score']:.4f}"
        
        @tool
        def predict(model_name: str, features: dict) -> str:
            """Make prediction with a trained model."""
            result = self.ml_mcp.predict(model_name, features)
            return f"Prediction: {result['prediction']}"
        
        @tool
        def list_models() -> str:
            """List all trained models."""
            models = self.ml_mcp.list_models()
            return f"Available models: {[m['name'] for m in models]}"
        
        @tool
        def create_sample_salary_dataset() -> str:
            """Create a sample salary prediction dataset."""
            path = self.ml_mcp.create_sample_salary_dataset()
            return f"Created sample dataset at: {path}"
        
        return [find_datasets, train_model, predict, list_models, create_sample_salary_dataset]
    
    def _create_agent(self):
        """Create agent executor."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an ML assistant. Use tools to train models, make predictions, and manage ML models."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute an ML operation.
        
        Args:
            query: User query about ML operations
            
        Returns:
            Result and metadata
        """
        try:
            result = self.agent.invoke({"input": query})
            return {
                "result": result.get("output", ""),
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

