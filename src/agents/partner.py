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

    Supports both OpenAI and Groq (free!) APIs
    """

    def __init__(self):
        super().__init__(
            name="Alex",
            role="partner",
            personality="Curious lab partner, slightly competitive, encourages discussion and collaboration"
        )

        # Initialize AI client based on provider
        if settings.ai_provider == "groq":
            self.client = openai.OpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        else:
            self.client = openai.OpenAI(api_key=settings.openai_api_key)

        self.experiment_memory = {}  # Remember key observations across the session
        self.what_if_counter = 0  # Track "what if" questions asked

        self.base_prompt = """You are Alex, an AI lab partner. You are PROACTIVE and CURIOUS. You:
- Think like a student, not a textbook
- Talk casually and encourage discussion
- Ask "What if" questions to explore different scenarios
- Reference past observations to show you remember the conversation
- Sometimes make reasonable mistakes to prompt critical thinking
- Challenge the student's assumptions in a friendly way
- Share ideas and collaborate with the student
- Show genuine curiosity about the experiment

IMPORTANT: Be proactive! Don't just acknowledge - ASK QUESTIONS and propose variations.
Examples:
- "What if we used twice the amount? How would that change things?"
- "Remember earlier when we noticed X? How does that connect to what we're seeing now?"
- "I'm curious - what do you think would happen if we changed Y?"

Keep responses natural, conversational, and under 150 words."""
    
    async def think(self, context: Dict[str, Any]) -> str:
        """
        Generate PROACTIVE partner response with memory and "what if" scenarios.

        Args:
            context: Contains experiment_name, student_message, experiment_data

        Returns:
            Partner's conversational response with proactive questions
        """
        student_message = context.get("student_message", "")
        experiment_name = context.get("experiment_name", "")
        step = context.get("current_step", 1)

        # Store key observations in memory
        if student_message and len(student_message) > 10:
            observation_key = f"step_{step}_observation"
            if observation_key not in self.experiment_memory:
                self.experiment_memory[observation_key] = student_message[:100]

        # Build conversation context with FULL history for memory
        conversation_context = "\n".join([
            f"{msg.sender}: {msg.content}"
            for msg in self.conversation_history[-10:]  # Increased to 10 for better memory
        ])

        # Add memory context to make agent more aware
        memory_summary = ""
        if self.experiment_memory:
            memory_summary = "\n\nKey observations you remember:\n" + "\n".join([
                f"- {key}: {value}" for key, value in list(self.experiment_memory.items())[-3:]
            ])

        # Determine if we should ask a "what if" question
        should_ask_what_if = (self.what_if_counter < 2 and step > 1)

        what_if_prompt = ""
        if should_ask_what_if:
            what_if_prompt = "\n\nIMPORTANT: In this response, ask a 'What if' question to explore variations of the experiment."
            self.what_if_counter += 1

        prompt = f"""{self.base_prompt}

Experiment: {experiment_name}
Current Step: {step}
{memory_summary}

Recent conversation:
{conversation_context}

Student just said: {student_message}
{what_if_prompt}

Alex (respond PROACTIVELY with questions and curiosity):"""

        try:
            response = self.client.chat.completions.create(
                model=settings.ai_model,  # Uses Groq or OpenAI model based on config
                messages=[
                    {"role": "system", "content": self.base_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,  # Slightly higher for more creativity
                max_tokens=180  # More tokens for proactive responses
            )

            message_content = response.choices[0].message.content

            # Add student message to history first
            student_msg = AgentMessage(
                sender="Student",
                content=student_message,
                role="student"
            )
            self.add_to_history(student_msg)

            # Then add partner response
            msg = AgentMessage(
                sender=self.name,
                content=message_content,
                role=self.role,
                metadata={"step": step, "what_if_count": self.what_if_counter}
            )
            self.add_to_history(msg)
            return message_content

        except Exception as e:
            fallback = f"Interesting observation! What if we tried varying that parameter? What do you think would happen?"
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
