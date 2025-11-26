"""Simple chat agent for Q&A."""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm import get_default_llm


class ChatAgent:
    """Simple chat agent for answering questions."""
    
    def __init__(self):
        """Initialize chat agent."""
        self.llm = get_default_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Answer questions clearly and concisely."),
            ("human", "{question}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def answer(self, question: str) -> Dict[str, Any]:
        """
        Answer a question.
        
        Args:
            question: User question
            
        Returns:
            Answer and metadata
        """
        try:
            answer = self.chain.invoke({"question": question})
            return {
                "answer": answer,
                "agent": "chat",
                "success": True,
            }
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "agent": "chat",
                "success": False,
                "error": str(e),
            }


def get_chat_agent() -> ChatAgent:
    """Get chat agent instance."""
    return ChatAgent()

