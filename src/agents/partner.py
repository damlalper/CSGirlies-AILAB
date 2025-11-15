"""Partner Agent - Interactive lab companion"""

from typing import Dict, Any
from src.agents.base import BaseAgent, AgentMessage
from src.config import settings
import openai


class PartnerAgent(BaseAgent):
    """
    AI Lab Partner Agent
    
    Persona: Curious, slightly impatient, motivating
    - Discusses experiment ideas
    - May make intentional mistakes for learning
    - Collaborates on experimental design
    """
    
    def __init__(self):
        super().__init__(
            name="Alex",
            role="partner",
            personality="Curious lab partner, slightly competitive, encourages discussion and collaboration"
        )
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.base_prompt = """You are Alex, an AI lab partner. You:
- Think like a student, not a textbook
- Talk casually and encourage discussion
- Sometimes make reasonable mistakes to prompt critical thinking
- Ask questions instead of just giving answers
- Share ideas and collaborate with the student
- Show genuine curiosity about the experiment

Keep responses natural, conversational, and under 150 words."""
    
    async def think(self, context: Dict[str, Any]) -> str:
        """
        Generate partner response based on experiment context.
        
        Args:
            context: Contains experiment_name, student_message, experiment_data
            
        Returns:
            Partner's conversational response
        """
        student_message = context.get("student_message", "")
        experiment_name = context.get("experiment_name", "")
        step = context.get("current_step", 1)
        
        conversation_context = "\n".join([
            f"{msg.sender}: {msg.content}" 
            for msg in self.conversation_history[-5:]
        ])
        
        prompt = f"""{self.base_prompt}

Experiment: {experiment_name}
Current Step: {step}

Conversation so far:
{conversation_context}

Student: {student_message}

Alex (respond naturally as your lab partner):"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self.base_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            message_content = response.choices[0].message.content
            msg = AgentMessage(
                sender=self.name,
                content=message_content,
                role=self.role
            )
            self.add_to_history(msg)
            return message_content
            
        except Exception as e:
            fallback = "That's interesting! What do you think we should do next?"
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
        Evaluate student's input for potential misconceptions.
        
        Args:
            student_input: Student's statement or action
            experiment_data: Current experiment state
            
        Returns:
            Evaluation with suggestions
        """
        return {
            "partner_evaluation": "Input noted",
            "has_misconception": False,
            "suggestions": []
        }
