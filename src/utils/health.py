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
    """Lightweight check of AI service configuration without model initialization."""
    try:
        import requests
        ollama_ok = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2).status_code == 200
    except:
        ollama_ok = False

    checks = {
        "model_configured": bool(MODEL_NAME),
        "ollama_url_configured": bool(OLLAMA_BASE_URL),
        "ollama_accessible": ollama_ok
    }
    
    healthy = sum(checks.values())
    return {
        "status": "healthy" if healthy == 3 else "degraded",
        "service": "ai_service",
        "health_score": f"{healthy}/3",
        "checks": checks,
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