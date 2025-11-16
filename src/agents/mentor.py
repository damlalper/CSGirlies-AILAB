"""Mentor Agent - Learning oversight and guidance"""

from typing import Dict, Any, List
from src.agents.base import BaseAgent, AgentMessage
from src.config import settings
import openai


class MentorAgent(BaseAgent):
    """
    Mentor Agent for Learning Oversight
    
    Responsibilities:
    - Evaluates conversation quality
    - Detects misconceptions
    - Provides subtle hints
    - Guides student without spoiling
    """
    
    def __init__(self):
        super().__init__(
            name="Dr. Silva",
            role="mentor",
            personality="Wise mentor, patient, provides guidance through Socratic method"
        )

        # Initialize AI client based on provider (OpenAI or Groq)
        if settings.ai_provider == "groq":
            self.client = openai.OpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        else:
            self.client = openai.OpenAI(api_key=settings.openai_api_key)

        self.base_prompt = """You are Dr. Silva, a mentor observing a lab session.
- Monitor student understanding
- Detect misconceptions gently
- Provide hints, not answers
- Ask guiding questions
- Encourage deeper thinking

You observe the conversation and provide brief, wise guidance."""
    
    async def think(self, context: Dict[str, Any]) -> str:
        """
        Generate mentor guidance based on conversation.
        
        Args:
            context: Contains experiment_name, conversation_history, student_progress
            
        Returns:
            Mentor's guidance or hint
        """
        experiment_name = context.get("experiment_name", "")
        conversation = context.get("conversation_history", [])
        
        conv_text = "\n".join([f"{c['sender']}: {c['content']}" for c in conversation[-6:]])
        
        prompt = f"""{self.base_prompt}

Experiment: {experiment_name}

Recent Conversation:
{conv_text}

Provide a brief mentor observation or hint (max 100 words). Focus on:
1. Is understanding progressing well?
2. Are there misconceptions?
3. What should be the next guiding question?

Mentor's Observation:"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.ai_model,  # Uses Groq or OpenAI model
                messages=[
                    {"role": "system", "content": self.base_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100
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
            fallback = "Let's pause and think about what we know so far..."
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
        Evaluate student learning and detect misconceptions.
        
        Args:
            student_input: Student's response
            experiment_data: Current experiment state
            
        Returns:
            Evaluation results including misconceptions and recommendations
        """
        prompt = f"""Analyze this student statement for misconceptions in context of {experiment_data.get('experiment_name', 'unknown experiment')}:

"{student_input}"

Identify:
1. Any scientific misconceptions
2. Level of understanding (1-10)
3. Recommended guidance

Be concise."""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.ai_model,  # Uses Groq or OpenAI model
                messages=[
                    {"role": "system", "content": "You are an expert science educator analyzing student understanding."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=150
            )
            
            analysis = response.choices[0].message.content
            return {
                "analysis": analysis,
                "has_misconception": "misconception" in analysis.lower(),
                "confidence": 0.7
            }
            
        except Exception as e:
            return {
                "analysis": "Unable to analyze at this time",
                "has_misconception": False,
                "error": str(e)
            }
