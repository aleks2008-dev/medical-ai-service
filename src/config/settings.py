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