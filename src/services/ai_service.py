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

    def analyze_and_respond(self, user_input: str) -> str:
        """Analyzes user input and returns response.

        Args:
            user_input: User input

        Returns:
            AI assistant response
        """
        # Строгая валидация входных данных
        if not isinstance(user_input, str):
            return "Ошибка: входные данные должны быть строкой."

        if not user_input or not user_input.strip():
            detected_language = self._detect_language(user_input) if user_input else DEFAULT_LANGUAGE
            return self._get_message('empty_input', detected_language)

        user_input_stripped = user_input.strip()

        # Определяем язык для валидации
        detected_language = self._detect_language(user_input_stripped)

        # Проверка минимальной длины
        if len(user_input_stripped) < 3:
            return self._get_message('short_input', detected_language)

        # Проверка максимальной длины
        if len(user_input_stripped) > 1000:
            return self._get_message('long_input', detected_language)

        # Проверка на наличие только пробелов или специальных символов
        if not any(char.isalnum() for char in user_input_stripped):
            return self._get_message('empty_input', detected_language)

        # Проверка на слишком много повторяющихся символов (спам)
        if len(set(user_input_stripped.lower())) < len(user_input_stripped) * 0.3:
            return self._get_message('empty_input', detected_language)

        # Rate limiting
        if not self._check_rate_limit():
            return self._get_message('rate_limit', detected_language)

        # Замер общего времени начала
        total_start_time = time.time()

        # Проверка кэша
        cache_key = user_input_stripped.lower()
        if cache_key in self.response_cache:
            total_time = time.time() - total_start_time
            log_info(f"Response from cache in {total_time:.3f}s")
            return self.response_cache[cache_key]

        try:
            if self._has_symptoms(user_input):
                response = self._handle_symptoms(user_input, total_start_time)
            else:
                response = self._handle_general_chat(user_input, total_start_time)

            # Сохранить в кэш
            if len(self.response_cache) < self.cache_max_size:
                self.response_cache[cache_key] = response

            # Финальный замер времени
            final_time = time.time() - total_start_time
            log_info(f"Response generated successfully in {final_time:.3f}s")

            return response
        except Exception as e:
            error_time = time.time() - total_start_time
            log_error(f"Error processing request in {error_time:.3f}s: {e}")
            return self._get_message('error', detected_language)
    
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
    
    def _handle_symptoms(self, user_input: str, start_time: float = None) -> str:
        """Handles input with symptoms.

        Args:
            user_input: User input with symptoms
            start_time: Start time for performance tracking

        Returns:
            Response with doctor recommendation
        """
        method_start_time = time.time() if start_time is None else start_time

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

            # Замер времени обработки AI модели
            ai_start_time = time.time()
            response = self.model.invoke(messages)
            ai_processing_time = time.time() - ai_start_time

            total_time = time.time() - method_start_time
            return response.content
        except Exception as e:
            error_time = time.time() - method_start_time
            log_error(f"Error handling symptoms in {error_time:.3f}s: {e}")
            return f"На основе ваших симптомов рекомендую: {recommend_doctor(user_input)}"
    
    def _handle_general_chat(self, user_input: str, start_time: float = None) -> str:
        """Handles general conversation.

        Args:
            user_input: User input
            start_time: Start time for performance tracking

        Returns:
            General assistant response
        """
        method_start_time = time.time() if start_time is None else start_time

        try:
            messages = [
                SystemMessage(content=GENERAL_ASSISTANT_PROMPT),
                HumanMessage(content=user_input)
            ]

            # Замер времени обработки AI модели
            ai_start_time = time.time()
            response = self.model.invoke(messages)
            ai_processing_time = time.time() - ai_start_time

            total_time = time.time() - method_start_time
            return response.content
        except Exception as e:
            error_time = time.time() - method_start_time
            log_error(f"Error in general chat in {error_time:.3f}s: {e}")
            # Получаем язык из входных данных
            detected_language = self._detect_language(user_input)
            return self._get_message('no_symptoms', detected_language)