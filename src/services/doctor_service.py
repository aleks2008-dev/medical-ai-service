"""Сервис для рекомендации врачей по симптомам."""

from src.models.symptom_data import SYMPTOM_DOCTOR_MAP


def recommend_doctor(symptoms: str) -> str:
    """Рекомендует профиль врача по введенным симптомам.
    
    Args:
        symptoms: Строка с описанием симптомов
        
    Returns:
        Строка с рекомендацией врача
    """
    matches = []
    for word, doctors in SYMPTOM_DOCTOR_MAP.items():
        if word in symptoms.lower():
            matches.extend(doctors)
    
    if matches:
        unique_doctors = ', '.join(set(matches))
        return f"Вам стоит обратиться к следующему специалисту: {unique_doctors}."
    else:
        return "Рекомендую для начала обратиться к терапевту."