"""LangGraph orchestrator for multi-agent system."""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm import get_default_llm
from orchestrator.nodes import (
    chat_node,
    github_node,
    drive_node,
    n8n_node,
    ml_node,
)


class AgentState(TypedDict):
    """State for the agent orchestrator."""
    query: str
    agent_type: Literal["chat", "github", "drive", "n8n", "ml", "unknown"]
    result: str
    agent_used: str
    success: bool


def create_orchestrator():
    """Create the LangGraph orchestrator."""
    
    # Create router node
    def router_node(state: AgentState) -> AgentState:
        """Route query to appropriate agent based on keywords."""
        query_lower = state["query"].lower()
        
        # GitHub keywords
        github_keywords = ["github", "repo", "repository", "commit", "issue", "pull request"]
        if any(keyword in query_lower for keyword in github_keywords):
            return {**state, "agent_type": "github"}
        
        # Drive keywords
        drive_keywords = ["drive", "google drive", "upload", "download", "file", "folder"]
        if any(keyword in query_lower for keyword in drive_keywords):
            return {**state, "agent_type": "drive"}
        
        # n8n keywords
        n8n_keywords = ["n8n", "workflow", "webhook", "trigger", "automation"]
        if any(keyword in query_lower for keyword in n8n_keywords):
            return {**state, "agent_type": "n8n"}
        
        # ML keywords
        ml_keywords = [
            "train", "model", "predict", "machine learning", "ml", "dataset",
            "salary", "prediction", "regression", "classification"
        ]
        if any(keyword in query_lower for keyword in ml_keywords):
            return {**state, "agent_type": "ml"}
        
        # Default to chat
        return {**state, "agent_type": "chat"}
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("chat", chat_node)
    workflow.add_node("github", github_node)
    workflow.add_node("drive", drive_node)
    workflow.add_node("n8n", n8n_node)
    workflow.add_node("ml", ml_node)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        lambda state: state["agent_type"],
        {
            "chat": "chat",
            "github": "github",
            "drive": "drive",
            "n8n": "n8n",
            "ml": "ml",
        }
    )
    
    # All agent nodes go to END
    workflow.add_edge("chat", END)
    workflow.add_edge("github", END)
    workflow.add_edge("drive", END)
    workflow.add_edge("n8n", END)
    workflow.add_edge("ml", END)
    
    return workflow.compile()


# Global orchestrator instance
_orchestrator = None


def get_orchestrator():
    """Get or create orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = create_orchestrator()
    return _orchestrator


def process_query(query: str) -> dict:
    """
    Process a query through the orchestrator.
    
    Args:
        query: User query
        
    Returns:
        Result dictionary
    """
    orchestrator = get_orchestrator()
    
    initial_state = {
        "query": query,
        "agent_type": "unknown",
        "result": "",
        "agent_used": "",
        "success": False,
    }
    
    result = orchestrator.invoke(initial_state)
    return result

