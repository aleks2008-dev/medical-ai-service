"""Pytest configuration and fixtures for Medical AI Service tests."""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Добавляем src в Python path для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.services.ai_service import AIService
from src.services.doctor_service import recommend_doctor
from src.models.symptom_data import SYMPTOM_DOCTOR_MAP


@pytest.fixture
def sample_symptoms():
    """Тестовые симптомы для проверки."""
    return {
        "головная_боль": "у меня болит голова",
        "зубная_боль": "зубная боль",
        "температура": "высокая температура",
        "кашель": "сильный кашель",
        "неизвестный": "просто плохо себя чувствую"
    }


@pytest.fixture
def expected_doctors():
    """Ожидаемые рекомендации врачей."""
    return {
        "головная_боль": ["невролог", "терапевт"],
        "зубная_боль": ["стоматолог"],
        "температура": ["терапевт"],
        "кашель": ["пульмонолог", "терапевт"]
    }


@pytest.fixture
def mock_ollama_model():
    """Мок для Ollama модели."""
    with patch('src.services.ai_service.init_chat_model') as mock_model:
        mock_instance = Mock()
        mock_instance.invoke.return_value.content = "Тестовый ответ от AI"
        mock_model.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def ai_service_with_mock(mock_ollama_model):
    """AI сервис с замоканной моделью."""
    return AIService()


@pytest.fixture(scope="session")
def test_config():
    """Тестовая конфигурация."""
    return {
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "MODEL_NAME": "llama3.2:3b",
        "MODEL_PROVIDER": "ollama",
        "MODEL_TEMPERATURE": 0
    }


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Автоматическая настройка тестового окружения."""
    # Устанавливаем тестовые переменные окружения
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("PYTHONPATH", os.path.join(os.path.dirname(__file__), '..'))


# Pytest хуки для настройки
def pytest_configure(config):
    """Конфигурация pytest."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
