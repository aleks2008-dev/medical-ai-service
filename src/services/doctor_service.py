"""Service for recommending doctors based on symptoms."""

from src.models.symptom_data import SYMPTOM_DOCTOR_MAP


def recommend_doctor(symptoms: str) -> str:
    """Recommends a doctor profile based on entered symptoms.
    
    Args:
        symptoms: String with symptom description
        
    Returns:
        String with doctor recommendation
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
