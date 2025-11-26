"""DeepSeek LLM wrapper for LangChain."""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from utils.config import config


def get_deepseek_llm(
    model: str = "deepseek-chat",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> BaseChatModel:
    """
    Create a DeepSeek LLM instance compatible with OpenAI API.
    
    Args:
        model: Model name (default: deepseek-chat)
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        
    Returns:
        ChatOpenAI instance configured for DeepSeek
    """
    config.validate()
    
    return ChatOpenAI(
        model=model,
        api_key=config.DEEPSEEK_API_KEY,
        base_url=config.DEEPSEEK_API_BASE,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def get_default_llm() -> BaseChatModel:
    """Get default DeepSeek LLM instance."""
    return get_deepseek_llm()

