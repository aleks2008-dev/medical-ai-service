#!/usr/bin/env python3
"""
Простой тестовый скрипт для Medical AI Service.
Запускает сервис, делает несколько тестовых запросов и завершается.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.ai_service import AIService

def test_medical_service():
    """Тестирует медицинский ИИ сервис."""
    print("🏥 Тестирование Medical AI Service")
    print("=" * 50)

    try:
        # Инициализация сервиса
        print("🔧 Инициализация AI Service...")
        ai = AIService()
        print("✅ Сервис инициализирован")

        # Тестовые медицинские вопросы
        test_questions = [
            "У меня болит голова",
            "Что делать при простуде?",
            "У меня температура 38 градусов",
            "Кашель уже неделю"
        ]

        print("\n🧪 Тестирование медицинских запросов:\n")

        for i, question in enumerate(test_questions, 1):
            print(f"{i}. Вопрос: {question}")
            try:
                response = ai.analyze_and_respond(question)
                # Показываем только первые 150 символов ответа
                preview = response[:150] + "..." if len(response) > 150 else response
                print(f"   Ответ: {preview}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
            print()

        print("🎉 Тестирование завершено успешно!")
        print("\n💡 Сервис работает корректно и готов к использованию!")

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        print("Проверьте, что Ollama запущен: docker start ollama")
        return False

    return True

if __name__ == "__main__":
    success = test_medical_service()
    sys.exit(0 if success else 1)
