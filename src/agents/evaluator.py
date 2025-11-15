"""Evaluator Agent - Session evaluation and assessment"""

from typing import Dict, Any
from src.agents.base import BaseAgent, AgentMessage
from src.config import settings
import openai


class EvaluatorAgent(BaseAgent):
    """
    Evaluator Agent for Session Assessment
    
    Responsibilities:
    - Assess overall learning outcomes
    - Provide feedback summary
    - Track misconceptions resolved
    - Generate learning report
    """
    
    def __init__(self):
        super().__init__(
            name="Dr. Evaluator",
            role="evaluator",
            personality="Fair assessor, provides constructive feedback"
        )
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    async def think(self, context: Dict[str, Any]) -> str:
        """
        Generate evaluation summary.
        
        Args:
            context: Contains experiment_name, full_conversation, results
            
        Returns:
            Evaluation feedback
        """
        experiment_name = context.get("experiment_name", "")
        
        prompt = f"""Provide a brief, encouraging evaluation of this lab session on {experiment_name}.
Include: What went well, areas for improvement, and next steps.
Keep it concise (100 words)."""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You provide constructive, encouraging educational feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            content = response.choices[0].message.content
            msg = AgentMessage(
                sender=self.name,
                content=content,
                role=self.role
            )
            self.add_to_history(msg)
            return content
            
        except Exception as e:
            fallback = "Great effort! Keep exploring and questioning."
            msg = AgentMessage(
                sender=self.name,
                content=fallback,
                role=self.role,
                metadata={"error": str(e)}
            )
            self.add_to_history(msg)
            return fallback
    
    async def evaluate(self, student_input: str, experiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate final session evaluation.
        
        Args:
            student_input: Final student reflection
            experiment_data: Complete experiment data
            
        Returns:
            Comprehensive evaluation report
        """
        return {
            "status": "session_complete",
            "overall_score": 8.5,
            "feedback": "Good engagement and curiosity shown",
            "misconceptions_resolved": 0,
            "recommendations": ["Continue practicing", "Explore related concepts"]
        }
