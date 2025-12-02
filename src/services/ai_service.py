"""Service for working with AI model."""

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from src.config.settings import (
    MODEL_NAME, MODEL_PROVIDER, MODEL_TEMPERATURE, OLLAMA_BASE_URL,
    SYSTEM_PROMPT, GENERAL_ASSISTANT_PROMPT, SYMPTOM_KEYWORDS
)
from src.services.doctor_service import recommend_doctor


class AIService:
    """Service for working with AI model."""
    
    def __init__(self):
        """Initialize AI service."""
        self.model = init_chat_model(
            MODEL_NAME,
            model_provider=MODEL_PROVIDER,
            temperature=MODEL_TEMPERATURE,
            base_url=OLLAMA_BASE_URL
        )
    
    def analyze_and_respond(self, user_input: str) -> str:
        """Analyzes user input and returns response.
        
        Args:
            user_input: User input
            
        Returns:
            AI assistant response
        """
        if self._has_symptoms(user_input):
            return self._handle_symptoms(user_input)
        else:
            return self._handle_general_chat(user_input)
    
    def _has_symptoms(self, user_input: str) -> bool:
        """Checks for symptoms in user input.
        
        Args:
            user_input: User input
            
        Returns:
            True if symptoms found, False otherwise
        """
        return any(keyword in user_input.lower() for keyword in SYMPTOM_KEYWORDS)
    
    def _handle_symptoms(self, user_input: str) -> str:
        """Handles input with symptoms.
        
        Args:
            user_input: User input with symptoms
            
        Returns:
            Response with doctor recommendation
        """
        doctor_recommendation = recommend_doctor(user_input)
        
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Пациент говорит: {user_input}\nРекомендация врача: {doctor_recommendation}\nСформулируй дружелюбный ответ пациенту.")
        ]
        
        response = self.model.invoke(messages)
        return response.content
    
    def _handle_general_chat(self, user_input: str) -> str:
        """Handles general conversation.
        
        Args:
            user_input: User input
            
        Returns:
            General assistant response
        """
        messages = [
            SystemMessage(content=GENERAL_ASSISTANT_PROMPT),
            HumanMessage(content=user_input)
        ]
        
        response = self.model.invoke(messages)
        return response.content