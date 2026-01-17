"""Pytest configuration and fixtures for Medical AI Service tests."""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.services.ai_service import AIService
from src.services.doctor_service import recommend_doctor
from src.models.symptom_data import SYMPTOM_DOCTOR_MAP


@pytest.fixture
def sample_symptoms():
    """Sample symptoms for testing."""
    return {
        "головная_боль": "у меня болит голова",
        "зубная_боль": "зубная боль",
        "температура": "высокая температура",
        "кашель": "сильный кашель",
        "неизвестный": "просто плохо себя чувствую"
    }


@pytest.fixture
def expected_doctors():
    """Expected doctor recommendations."""
    return {
        "головная_боль": ["невролог", "терапевт"],
        "зубная_боль": ["стоматолог"],
        "температура": ["терапевт"],
        "кашель": ["пульмонолог", "терапевт"]
    }


@pytest.fixture
def mock_ollama_model():
    """Mock for Ollama model."""
    with patch('src.services.ai_service.init_chat_model') as mock_model:
        mock_instance = Mock()
        mock_instance.invoke.return_value.content = "Тестовый ответ от AI"
        mock_model.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def ai_service_with_mock(mock_ollama_model):
    """AI service with mocked model."""
    return AIService()


@pytest.fixture(scope="session")
def test_config():
    """Test configuration."""
    return {
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "MODEL_NAME": "llama3.2:3b-instruct-q4_0",
        "MODEL_PROVIDER": "ollama",
        "MODEL_TEMPERATURE": 0
    }


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Automatic test environment setup."""
    # Set test environment variables
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("PYTHONPATH", os.path.join(os.path.dirname(__file__), '..'))


# Pytest hooks for configuration
def pytest_configure(config):
    """Pytest configuration."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
