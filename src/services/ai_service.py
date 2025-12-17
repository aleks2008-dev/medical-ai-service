"""Service for working with AI model."""

import logging
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from src.config.settings import (
    MODEL_NAME, MODEL_PROVIDER, MODEL_TEMPERATURE, OLLAMA_BASE_URL,
    SYSTEM_PROMPT, GENERAL_ASSISTANT_PROMPT, SYMPTOM_KEYWORDS
)
from src.services.doctor_service import recommend_doctor, assess_severity

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    """Service for working with AI model."""
    
    def __init__(self):
        """Initialize AI service."""
        try:
            self.model = init_chat_model(
                MODEL_NAME,
                model_provider=MODEL_PROVIDER,
                temperature=MODEL_TEMPERATURE,
                base_url=OLLAMA_BASE_URL
            )
            self.response_cache = {}
            self.cache_max_size = 100
        except Exception as e:
            print(f"Error initializing AI model: {e}")
            print("Please ensure Ollama is running and the model is available.")
            raise
    
    def analyze_and_respond(self, user_input: str) -> str:
        """Analyzes user input and returns response.

        Args:
            user_input: User input

        Returns:
            AI assistant response
        """
        logger.info(f"Processing input: {user_input[:50]}...")

        if not user_input or not user_input.strip():
            return "Please provide your symptoms or question."

        # Проверка кэша
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            logger.info("Response from cache")
            return self.response_cache[cache_key]

        try:
            if self._has_symptoms(user_input):
                response = self._handle_symptoms(user_input)
            else:
                response = self._handle_general_chat(user_input)

            # Сохранить в кэш
            if len(self.response_cache) < self.cache_max_size:
                self.response_cache[cache_key] = response

            logger.info("Response generated successfully")
            return response
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return "Извините, произошла ошибка. Попробуйте еще раз."
    
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
        try:
            doctor_recommendation = recommend_doctor(user_input)

            # Оценка срочности
            urgent_indicators = ['острая', 'сильная', 'тяжелая', 'кровь', 'потеря сознания']
            is_urgent = any(indicator in user_input.lower() for indicator in urgent_indicators)
            urgency_note = "⚠️ Это может быть срочно!" if is_urgent else ""

            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=f"Пациент: {user_input}\nРекомендация: {doctor_recommendation}\n{urgency_note}\nДай дружелюбный ответ.")
            ]

            response = self.model.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error handling symptoms: {e}")
            return f"На основе ваших симптомов рекомендую: {recommend_doctor(user_input)}"
    
    def _handle_general_chat(self, user_input: str) -> str:
        """Handles general conversation.
        
        Args:
            user_input: User input
            
        Returns:
            General assistant response
        """
        try:
            messages = [
                SystemMessage(content=GENERAL_ASSISTANT_PROMPT),
                HumanMessage(content=user_input)
            ]
            
            response = self.model.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error in general chat: {e}")
            return "I'm here to help with medical questions. Please describe your symptoms or ask a health-related question."