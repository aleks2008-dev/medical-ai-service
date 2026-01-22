"""Service for working with AI model."""

import logging
import time
import os
from collections import defaultdict
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from src.config.settings import (
    MODEL_NAME, MODEL_PROVIDER, MODEL_TEMPERATURE, OLLAMA_BASE_URL,
    MODEL_NUM_CTX, MODEL_NUM_PREDICT,
    SYSTEM_PROMPT, GENERAL_ASSISTANT_PROMPT, SYMPTOM_KEYWORDS,
    LANGUAGES, DEFAULT_LANGUAGE
)
from src.services.doctor_service import recommend_doctor, assess_severity

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Оптимизация логирования для производительности
PERFORMANCE_LOGGING = os.getenv("PERFORMANCE_LOGGING", "true").lower() == "true"

def log_info(message: str, *args, **kwargs):
    """Условное INFO логирование"""
    if PERFORMANCE_LOGGING:
        logger.info(message, *args, **kwargs)

def log_error(message: str, *args, **kwargs):
    """ERROR логирование (всегда активно)"""
    logger.error(message, *args, **kwargs)


class AIService:
    """Service for working with AI model."""

    def __init__(self):
        """Initialize AI service."""
        try:
            self.model = ChatOllama(
                model=MODEL_NAME,
                temperature=MODEL_TEMPERATURE,
                base_url=OLLAMA_BASE_URL,
                num_ctx=MODEL_NUM_CTX,
                num_predict=MODEL_NUM_PREDICT
            )
            self.response_cache = {}
            self.cache_max_size = 100
            self.request_times = defaultdict(list)
            self.rate_limit = 10  # запросов в минуту
            self.time_window = 60  # секунд
        except Exception as e:
            print(f"Error initializing AI model: {e}")
            print("Please ensure Ollama is running and the model is available.")
            raise

    def _detect_language(self, text: str) -> str:
        """Простое определение языка по тексту."""
        if not isinstance(text, str) or not text.strip():
            return DEFAULT_LANGUAGE

        text = text.strip()

        # Проверяем кириллицу (русский)
        cyrillic_chars = sum(1 for char in text if '\u0400' <= char <= '\u04FF')
        if cyrillic_chars > len(text) * 0.3:  # >30% кириллицы
            return 'ru'

        # Проверяем испанские символы
        spanish_chars = ['á', 'é', 'í', 'ó', 'ú', 'ü', 'ñ', '¿', '¡']
        if any(char in text.lower() for char in spanish_chars):
            return 'es'

        # По умолчанию английский
        return DEFAULT_LANGUAGE

    def _get_message(self, key: str, language: str = None) -> str:
        """Получить сообщение на нужном языке."""
        if not isinstance(key, str) or not key.strip():
            return "Ошибка валидации сообщения"

        if language is None:
            language = DEFAULT_LANGUAGE

        if not isinstance(language, str):
            language = DEFAULT_LANGUAGE

        language_dict = LANGUAGES.get(language, LANGUAGES.get(DEFAULT_LANGUAGE, {}))
        return language_dict.get(key, key)

    def _check_rate_limit(self, user_id: str = "default") -> bool:
        """Простая проверка rate limiting."""
        if not isinstance(user_id, str) or not user_id.strip():
            user_id = "default"

        now = time.time()
        self.request_times[user_id] = [
            t for t in self.request_times[user_id]
            if now - t < self.time_window
        ]

        if len(self.request_times[user_id]) >= self.rate_limit:
            return False

        self.request_times[user_id].append(now)
        return True

    def _validate_input(self, text: str) -> tuple[bool, str, str]:
        """Быстрая валидация входных данных.
        
        Returns:
            (is_valid, error_message, detected_language)
        """
        if not isinstance(text, str) or not text.strip():
            return False, 'empty_input', DEFAULT_LANGUAGE
        
        text = text.strip()
        lang = self._detect_language(text)
        
        # Базовые проверки
        if len(text) < 3:
            return False, 'short_input', lang
        if len(text) > 1000:
            return False, 'long_input', lang
        if not any(c.isalnum() for c in text):
            return False, 'empty_input', lang
        
        return True, '', lang

    def analyze_and_respond(self, user_input: str) -> str:
        """Analyzes user input and returns response."""
        # Валидация
        is_valid, error_key, lang = self._validate_input(user_input)
        if not is_valid:
            return self._get_message(error_key, lang)
        
        user_input_stripped = user_input.strip()
        
        # Кэш
        cache_key = user_input_stripped.lower()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        # Rate limiting - graceful degradation
        if not self._check_rate_limit():
            # Возвращаем базовую рекомендацию без AI
            if self._has_symptoms(user_input):
                return recommend_doctor(user_input)
            return self._get_message('rate_limit', lang)
        
        try:
            response = self._handle_symptoms(user_input) if self._has_symptoms(user_input) else self._handle_general_chat(user_input)
            
            if len(self.response_cache) < self.cache_max_size:
                self.response_cache[cache_key] = response
            
            return response
        except Exception as e:
            log_error(f"Error processing request: {e}")
            return self._get_message('error', lang)
    
    def _has_symptoms(self, user_input: str) -> bool:
        """Checks for symptoms in user input.

        Args:
            user_input: User input

        Returns:
            True if symptoms found, False otherwise
        """
        if not isinstance(user_input, str) or not user_input.strip():
            return False

        user_input_lower = user_input.lower().strip()
        return any(keyword in user_input_lower for keyword in SYMPTOM_KEYWORDS)
    
    def _handle_symptoms(self, user_input: str) -> str:
        """Handles input with symptoms."""
        try:
            doctor_recommendation = recommend_doctor(user_input)
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
            log_error(f"Error handling symptoms: {e}")
            return f"На основе ваших симптомов рекомендую: {recommend_doctor(user_input)}"
    
    def _handle_general_chat(self, user_input: str) -> str:
        """Handles general conversation."""
        try:
            messages = [
                SystemMessage(content=GENERAL_ASSISTANT_PROMPT),
                HumanMessage(content=user_input)
            ]
            response = self.model.invoke(messages)
            return response.content
        except Exception as e:
            log_error(f"Error in general chat: {e}")
            return self._get_message('no_symptoms', self._detect_language(user_input))