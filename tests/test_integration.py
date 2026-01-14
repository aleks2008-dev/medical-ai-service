"""Integration tests for Medical AI Service with real Ollama."""

import pytest
import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.services.ai_service import AIService
from src.utils.health import check_ai_service


@pytest.mark.integration
def test_ollama_connection():
    """Test that Ollama is running and accessible."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert len(data["models"]) > 0
        print(f"✅ Ollama доступен. Загружено моделей: {len(data['models'])}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ollama не доступен: {e}")


@pytest.mark.integration
def test_ai_service_with_real_ollama():
    """Test AI service with real Ollama connection."""
    try:
        # Create AI service instance
        ai = AIService()
        print("✅ AIService создан")

        # Test basic functionality
        test_input = "У меня болит голова"
        response = ai.analyze_and_respond(test_input)

        # Basic checks
        assert isinstance(response, str)
        assert len(response) > 10  # Response should be meaningful
        # Check that response contains medical advice or doctor recommendation
        response_lower = response.lower()
        has_medical_content = (
            "врач" in response_lower or
            "специалист" in response_lower or
            "рекомендую" in response_lower or
            "симптом" in response_lower or
            "здоровье" in response_lower
        )
        assert has_medical_content, f"Ответ не содержит медицинскую информацию: {response}"
        print(f"✅ Ответ получен: {response[:100]}...")

    except Exception as e:
        pytest.fail(f"AI сервис не работает с Ollama: {e}")


@pytest.mark.integration
def test_ai_service_health_with_real_ollama():
    """Test AI service health check with real Ollama."""
    health_result = check_ai_service()

    assert health_result["status"] == "healthy"
    assert health_result["service"] == "ai_service"
    assert "checks" in health_result

    checks = health_result["checks"]
    assert checks["model_loaded"] is True
    assert checks["cache_enabled"] is True
    assert checks["rate_limiting"] is True
    assert checks["multilanguage"] is True

    print(f"✅ Health check пройден: {health_result['health_score']}")


@pytest.mark.integration
def test_multiple_ai_requests():
    """Test multiple AI requests to ensure stability."""
    ai = AIService()

    test_cases = [
        "У меня температура",
        "Болит горло",
        "Что делать при простуде?"
    ]

    for i, test_input in enumerate(test_cases, 1):
        try:
            response = ai.analyze_and_respond(test_input)
            assert isinstance(response, str)
            assert len(response) > 5
            print(f"✅ Запрос {i}: {response[:50]}...")
        except Exception as e:
            pytest.fail(f"Ошибка в запросе {i} ({test_input}): {e}")


@pytest.mark.integration
def test_ollama_models_available():
    """Test that required Ollama models are available."""
    response = requests.get("http://localhost:11434/api/tags")
    data = response.json()

    models = [model["name"] for model in data["models"]]
    print(f"Доступные модели: {models}")

    # Check for preferred models
    preferred_models = ["llama3.2:3b-instruct-q4_0", "llama3.2:3b", "llama3.1:8b"]
    available_preferred = [model for model in preferred_models if model in models]

    assert len(available_preferred) > 0, f"Нет предпочитаемых моделей. Доступные: {models}"
    print(f"✅ Доступны предпочитаемые модели: {available_preferred}")


if __name__ == "__main__":
    # Allow running integration tests manually
    pytest.main([__file__, "-v", "-m", "integration"])
