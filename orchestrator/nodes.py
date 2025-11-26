"""Orchestrator nodes for routing to agents."""

from typing import Dict, Any
from agents.chat_agent import get_chat_agent
from agents.github_agent import get_github_agent
from agents.drive_agent import get_drive_agent
from agents.n8n_agent import get_n8n_agent
from agents.ml_agent import get_ml_agent


def chat_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle chat queries."""
    agent = get_chat_agent()
    result = agent.answer(state["query"])
    return {
        "result": result["answer"],
        "agent_used": "chat",
        "success": result["success"],
    }


def github_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GitHub operations."""
    agent = get_github_agent()
    result = agent.execute(state["query"])
    return {
        "result": result["result"],
        "agent_used": "github",
        "success": result["success"],
    }


def drive_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Drive operations."""
    agent = get_drive_agent()
    result = agent.execute(state["query"])
    return {
        "result": result["result"],
        "agent_used": "drive",
        "success": result["success"],
    }


def n8n_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle n8n operations."""
    agent = get_n8n_agent()
    result = agent.execute(state["query"])
    return {
        "result": result["result"],
        "agent_used": "n8n",
        "success": result["success"],
    }


def ml_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ML operations."""
    agent = get_ml_agent()
    result = agent.execute(state["query"])
    return {
        "result": result["result"],
        "agent_used": "ml",
        "success": result["success"],
    }

