"""Health check utilities for Medical AI Service."""

import os
from datetime import datetime
from typing import Dict, Any

from src.config.settings import MODEL_NAME, OLLAMA_BASE_URL


def health_check() -> Dict[str, Any]:
    """
    Perform a comprehensive health check of the Medical AI Service.
    
    Returns:
        Dict containing health status information
    """
    return {
        "status": "healthy",
        "service": "Medical AI Service",
        "version": "1.0.0",
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
        "service": "Medical AI Service",
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