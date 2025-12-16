"""Tests for health check functionality."""

import pytest
from src.utils.health import health_check, quick_health_check, check_dependencies


def test_health_check():
    """Test comprehensive health check."""
    result = health_check()
    
    assert isinstance(result, dict)
    assert result["status"] == "healthy"
    assert result["service"] == "Medical AI Service"
    assert "version" in result
    assert result["version"] == "1.0.0"
    assert "timestamp" in result
    assert "components" in result
    assert "environment" in result


def test_quick_health_check():
    """Test quick health check."""
    result = quick_health_check()
    
    assert isinstance(result, dict)
    assert result["status"] == "healthy"
    assert result["service"] == "Medical AI Service"
    assert "timestamp" in result


def test_check_dependencies():
    """Test dependency checking."""
    result = check_dependencies()
    
    assert isinstance(result, dict)
    assert "langchain" in result
    assert "pytest" in result
    assert isinstance(result["langchain"], bool)
    assert isinstance(result["pytest"], bool)


def test_health_check_components():
    """Test health check components structure."""
    result = health_check()
    
    components = result["components"]
    assert "ai_model" in components
    assert "ollama_connection" in components
    assert "doctor_service" in components
    
    # Check AI model component
    ai_model = components["ai_model"]
    assert "name" in ai_model
    assert "provider" in ai_model
    assert "status" in ai_model


def test_health_check_environment():
    """Test health check environment information."""
    result = health_check()
    
    environment = result["environment"]
    assert "python_version" in environment
    assert "platform" in environment
    assert isinstance(environment["python_version"], str)
    assert isinstance(environment["platform"], str)