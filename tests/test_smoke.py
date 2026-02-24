"""Simple smoke tests for CI/CD."""

import sys
import os


def test_python_version():
    """Test Python version is 3.8+."""
    assert sys.version_info >= (3, 8)


def test_project_structure():
    """Test that project structure exists."""
    assert os.path.exists("src")
    assert os.path.exists("src/api")
    assert os.path.exists("src/services")
    assert os.path.exists("src/config")
    assert os.path.exists("tests")


def test_imports():
    """Test that basic imports work."""
    from src.api import models
    from src.config import settings
    
    assert hasattr(models, 'SymptomRequest')
    assert hasattr(models, 'AnalysisResponse')
    assert hasattr(settings, 'MODEL_NAME')


def test_pydantic_models():
    """Test Pydantic models validation."""
    from src.api.models import SymptomRequest, AnalysisResponse, HealthResponse
    
    # Test SymptomRequest
    request = SymptomRequest(text="Test symptom")
    assert request.text == "Test symptom"
    
    # Test AnalysisResponse
    response = AnalysisResponse(
        response="Test response",
        language="en",
        processing_time=1.5
    )
    assert response.response == "Test response"
    assert response.language == "en"
    
    # Test HealthResponse
    health = HealthResponse(
        status="healthy",
        service="Test Service",
        version="1.0.0"
    )
    assert health.status == "healthy"
