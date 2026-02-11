"""Application configuration."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model settings
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b-instruct-q4_0")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_TEMPERATURE = int(os.getenv("MODEL_TEMPERATURE", "0"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Оптимизация производительности
MODEL_NUM_CTX = int(os.getenv("MODEL_NUM_CTX", "512"))  # Уменьшен контекст для скорости
MODEL_NUM_PREDICT = int(os.getenv("MODEL_NUM_PREDICT", "192"))  # Развернутые ответы

# Application settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# System prompts
SYSTEM_PROMPT = """
Ты медицинский помощник. Отвечай кратко:
1. Рекомендуй специалиста
2. Укажи срочность
3. Дай базовый совет
"""

GENERAL_ASSISTANT_PROMPT = "Ты медицинский ассистент. Отвечай кратко."

# Keywords for symptom detection
SYMPTOM_KEYWORDS = [
    "болит", "боль", "температура", "кашель", 
    "симптом", "плохо", "живот", "голова", "глаз", "зуб"
]

# Exit commands
EXIT_COMMANDS = ['quit', 'выход', 'q']

# Language support
LANGUAGES = {
    'ru': {
        'empty_input': "Пожалуйста, опишите свои симптомы или задайте вопрос.",
        'short_input': "Пожалуйста, опишите симптомы более подробно (минимум 3 символа).",
        'long_input': "Слишком длинное описание. Пожалуйста, опишите симптомы короче (максимум 1000 символов).",
        'rate_limit': "Слишком много запросов. Пожалуйста, подождите минуту.",
        'error': "Извините, произошла ошибка. Попробуйте еще раз.",
        'processing': "Обрабатываю ваш запрос...",
        'no_symptoms': "Не найдено явных симптомов. Если у вас есть вопросы о здоровье, опишите симптомы подробнее.",
        'model_error': "Сервис временно недоступен. Попробуйте позже."
    },
    'en': {
        'empty_input': "Please describe your symptoms or ask a question.",
        'short_input': "Please describe symptoms in more detail (at least 3 characters).",
        'long_input': "Description too long. Please describe symptoms shorter (maximum 1000 characters).",
        'rate_limit': "Too many requests. Please wait a minute.",
        'error': "Sorry, an error occurred. Please try again.",
        'processing': "Processing your request...",
        'no_symptoms': "No obvious symptoms found. If you have health questions, please describe symptoms in more detail.",
        'model_error': "Service temporarily unavailable. Please try later."
    }
}

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ru")
