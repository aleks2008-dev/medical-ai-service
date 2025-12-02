"""Утилиты для командной строки."""

from src.config.settings import EXIT_COMMANDS
from src.services.ai_service import AIService


class CLI:
    """Интерфейс командной строки для медицинского ассистента."""
    
    def __init__(self):
        """Инициализация CLI."""
        self.ai_service = AIService()
    
    def run_tests(self):
        """Запускает тестовые примеры."""
        print("🧪 Запуск тестовых примеров...\n")
        
        test_cases = [
            "У меня болит голова и температура",
            "thank you!"
        ]
        
        for i, test_input in enumerate(test_cases, 1):
            try:
                response = self.ai_service.analyze_and_respond(test_input)
                print(f"Тест {i}: {test_input}")
                print(f"Ответ ИИ: {response}\n")
            except Exception as e:
                print(f"Ошибка в тесте {i}: {e}\n")
    
    def run_interactive(self):
        """Запускает интерактивный режим."""
        print("💬 Интерактивный режим (введи 'quit' для выхода):")
        
        while True:
            user_input = input("\nВопрос: ")
            
            if user_input.lower() in EXIT_COMMANDS:
                print("👋 До свидания!")
                break
            
            try:
                response = self.ai_service.analyze_and_respond(user_input)
                print(f"Ответ: {response}")
            except Exception as e:
                print(f"Ошибка: {e}")
    
    def run(self):
        """Запускает полный цикл: тесты + интерактивный режим."""
        self.run_tests()
        self.run_interactive()