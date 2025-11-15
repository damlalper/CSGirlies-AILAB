"""Base agent class for multi-agent system"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class AgentMessage:
    """Message format for agent communication"""
    sender: str
    content: str
    role: str
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str, role: str, personality: str):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            role: Agent role (partner, mentor, evaluator)
            personality: Agent personality description
        """
        self.name = name
        self.role = role
        self.personality = personality
        self.conversation_history = []
    
    @abstractmethod
    async def think(self, context: Dict[str, Any]) -> str:
        """
        Process context and generate response.
        
        Args:
            context: Contextual information for decision making
            
        Returns:
            Agent's response
        """
        pass
    
    @abstractmethod
    async def evaluate(self, student_input: str, experiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate student input or experiment data.
        
        Args:
            student_input: Student's response or action
            experiment_data: Current experiment data
            
        Returns:
            Evaluation results
        """
        pass
    
    def add_to_history(self, message: AgentMessage) -> None:
        """Add message to conversation history"""
        self.conversation_history.append(message)
    
    def get_history(self, limit: Optional[int] = None) -> list:
        """Get conversation history"""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
