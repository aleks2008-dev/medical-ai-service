import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.services.doctor_service import recommend_doctor

def test_recommend_doctor_basic():
    result = recommend_doctor("зубная боль")
    assert isinstance(result, str)
    assert "стоматолог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_unknown_symptom():
    """Тест для неизвестного симптома."""
    result = recommend_doctor("что-то непонятное")
    assert "терапевт" in result.lower()
    assert isinstance(result, str)