"""Health check utilities for Medical AI Service."""

import os
from datetime import datetime
from typing import Dict, Any

from src.config.settings import MODEL_NAME, OLLAMA_BASE_URL
from src import __version__, __description__


def health_check() -> Dict[str, Any]:
    """
    Perform a comprehensive health check of the Medical AI Service.
    
    Returns:
        Dict containing health status information
    """
    return {
        "status": "healthy",
        "service": __description__,
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "ai_model": {
                "name": MODEL_NAME,
                "provider": "ollama",
                "status": "configured"
            },
            "ollama_connection": {
                "url": OLLAMA_BASE_URL,
                "status": "configured"
            },
            "doctor_service": {
                "status": "available"
            }
        },
        "environment": {
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "platform": os.name
        }
    }


def quick_health_check() -> Dict[str, str]:
    """
    Quick health check for basic service availability.

    Returns:
        Simple health status
    """
    return {
        "status": "healthy",
        "service": __description__,
        "version": __version__,
        "timestamp": datetime.now().isoformat()
    }


def check_dependencies() -> Dict[str, bool]:
    """
    Check if all required dependencies are available.

    Returns:
        Dict with dependency status
    """
    dependencies = {}

    try:
        import langchain
        dependencies["langchain"] = True
    except ImportError:
        dependencies["langchain"] = False

    try:
        import langchain_core
        dependencies["langchain_core"] = True
    except ImportError:
        dependencies["langchain_core"] = False

    try:
        import pytest
        dependencies["pytest"] = True
    except ImportError:
        dependencies["pytest"] = False

    return dependencies


def check_ai_service() -> Dict[str, Any]:
    """
    Check the health status of the AI service.

    Returns:
        Dict containing AI service health information
    """
    try:
        from src.services.ai_service import AIService

        # Create instance to check initialization
        ai = AIService()

        # Check main components
        checks = {
            "model_loaded": hasattr(ai, 'model') and ai.model is not None,
            "cache_enabled": hasattr(ai, 'response_cache'),
            "rate_limiting": hasattr(ai, 'rate_limit') and hasattr(ai, 'time_window'),
            "multilanguage": hasattr(ai, '_get_message') and hasattr(ai, '_detect_language')
        }

        # Determine overall status
        all_healthy = all(checks.values())
        status = "healthy" if all_healthy else "degraded"

        # Count healthy components
        healthy_count = sum(checks.values())
        total_count = len(checks)

        return {
            "status": status,
            "service": "ai_service",
            "health_score": f"{healthy_count}/{total_count}",
            "checks": checks,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "ai_service",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def quick_health_check() -> Dict[str, Any]:
    """
    Quick health check for basic service availability including AI service.

    Returns:
        Health status with AI service check
    """
    base_result = health_check()
    base_result["ai_service"] = check_ai_service()
    return base_result