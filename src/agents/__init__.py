"""Multi-agent system for CSGirlies-AILAB"""

from src.agents.base import BaseAgent, AgentMessage
from src.agents.partner import PartnerAgent
from src.agents.mentor import MentorAgent
from src.agents.evaluator import EvaluatorAgent

__all__ = [
    "BaseAgent",
    "AgentMessage",
    "PartnerAgent",
    "MentorAgent",
    "EvaluatorAgent"
]
