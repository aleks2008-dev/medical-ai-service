import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.services.doctor_service import recommend_doctor

def test_recommend_doctor_basic():
    """Test basic doctor recommendation functionality."""
    result = recommend_doctor("зубная боль")
    assert isinstance(result, str)
    assert "стоматолог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_headache():
    """Test headache symptom recommendation."""
    result = recommend_doctor("головная боль")
    assert isinstance(result, str)
    assert "невролог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_cough():
    """Test cough symptom recommendation."""
    result = recommend_doctor("кашель")
    assert isinstance(result, str)
    assert "пульмонолог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_unknown_symptom():
    """Test unknown symptom handling."""
    result = recommend_doctor("что-то непонятное")
    assert isinstance(result, str)
    assert "терапевт" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_empty_input():
    """Test empty input handling."""
    result = recommend_doctor("")
    assert isinstance(result, str)
    assert "терапевт" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_multiple_symptoms():
    """Test multiple symptoms recommendation."""
    result = recommend_doctor("головная боль и температура")
    assert isinstance(result, str)
    # Check that at least one doctor is recommended
    assert any(doctor in result.lower() for doctor in ["невролог", "терапевт"])
    assert len(result) > 0

def test_recommend_doctor_heart_symptoms():
    """Test heart-related symptoms recommendation."""
    result = recommend_doctor("боль в сердце и давление")
    assert isinstance(result, str)
    assert "кардиолог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_skin_symptoms():
    """Test skin-related symptoms recommendation."""
    result = recommend_doctor("сыпь и зуд")
    assert isinstance(result, str)
    assert "дерматолог" in result.lower()
    assert len(result) > 0

def test_recommend_doctor_case_insensitive():
    """Test case insensitive symptom matching."""
    result_lower = recommend_doctor("головная боль")
    result_upper = recommend_doctor("ГОЛОВНАЯ БОЛЬ")
    result_mixed = recommend_doctor("ГоЛоВнАя БоЛь")
    
    # All variants should contain neurologist
    assert "невролог" in result_lower.lower()
    assert "невролог" in result_upper.lower()
    assert "невролог" in result_mixed.lower()

def test_recommend_doctor_partial_match():
    """Test partial symptom matching in context."""
    result = recommend_doctor("у меня болит голова очень сильно")
    assert isinstance(result, str)
    assert "невролог" in result.lower()
    assert len(result) > 0