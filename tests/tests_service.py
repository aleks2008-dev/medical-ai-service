import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.services.doctor_service import recommend_doctor

def test_recommend_doctor_basic():
    """Тест базовой функциональности рекомендации врача."""
    result = recommend_doctor("зубная боль")
    assert isinstance(result, str)
    assert "стоматолог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_headache():
    """Тест для головной боли."""
    result = recommend_doctor("головная боль")
    assert isinstance(result, str)
    assert "невролог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_cough():
    """Тест для кашля."""
    result = recommend_doctor("кашель")
    assert isinstance(result, str)
    assert "пульмонолог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_unknown_symptom():
    """Тест для неизвестного симптома."""
    result = recommend_doctor("что-то непонятное")
    assert isinstance(result, str)
    assert "терапевт" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_empty_input():
    """Тест для пустого ввода."""
    result = recommend_doctor("")
    assert isinstance(result, str)
    assert "терапевт" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_multiple_symptoms():
    """Тест для нескольких симптомов."""
    result = recommend_doctor("головная боль и температура")
    assert isinstance(result, str)
    # Проверяем, что есть хотя бы один врач
    assert any(doctor in result.lower() for doctor in ["невролог", "терапевт"])
    assert len(result) > 0