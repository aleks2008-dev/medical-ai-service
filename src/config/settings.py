"""Application configuration."""

# Model settings
MODEL_NAME = "llama3.2:3b"
MODEL_PROVIDER = "ollama"
MODEL_TEMPERATURE = 0
OLLAMA_BASE_URL = "http://localhost:11434"

# System prompts
SYSTEM_PROMPT = """
Ты — медицинский ассистент. 
Когда пациент описывает симптомы, ты должен проанализировать их и дать рекомендацию врача.
Используй функцию recommend_doctor для анализа симптомов.
"""

GENERAL_ASSISTANT_PROMPT = "Ты дружелюбный медицинский ассистент. Отвечай кратко и вежливо."

# Keywords for symptom detection
SYMPTOM_KEYWORDS = [
    "болит", "боль", "температура", "кашель", 
    "симптом", "плохо", "живот", "голова", "глаз", "зуб"
]

# Exit commands
EXIT_COMMANDS = ['quit', 'выход', 'q']