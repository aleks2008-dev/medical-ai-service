"""Application configuration."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model settings
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_TEMPERATURE = int(os.getenv("MODEL_TEMPERATURE", "0"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Application settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# System prompts
SYSTEM_PROMPT = """
Ты медицинский помощник. При анализе симптомов:
1. Определи срочность обращения к врачу
2. Дай рекомендацию специалиста
3. Объясни почему именно этот врач
4. Посоветуй что делать до визита к врачу

Отвечай empathetically и профессионально.
"""

GENERAL_ASSISTANT_PROMPT = "Ты дружелюбный медицинский ассистент. Отвечай кратко и вежливо."

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
    },
    'es': {
        'empty_input': "Por favor, describe tus síntomas o haz una pregunta.",
        'short_input': "Por favor, describe los síntomas con más detalle (al menos 3 caracteres).",
        'long_input': "Descripción demasiado larga. Por favor, describe los síntomas más brevemente (máximo 1000 caracteres).",
        'rate_limit': "Demasiadas solicitudes. Por favor, espera un minuto.",
        'error': "Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.",
        'processing': "Procesando tu solicitud...",
        'no_symptoms': "No se encontraron síntomas obvios. Si tienes preguntas sobre la salud, describe los síntomas con más detalle.",
        'model_error': "Servicio temporalmente no disponible. Por favor, inténtalo más tarde."
    }
}

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ru")