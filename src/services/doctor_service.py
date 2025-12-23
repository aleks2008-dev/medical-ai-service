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


def assess_severity(symptoms: str) -> dict:
    """Assesses the severity level of symptoms.

    Args:
        symptoms: String with symptom description

    Returns:
        Dict containing severity level, score, and advice
    """
    urgent_words = ['острая', 'сильная', 'тяжелая', 'невыносимая', 'кровотечение', 'потеря сознания']
    moderate_words = ['боль', 'температура', 'тошнота', 'рвота', 'кашель']

    symptoms_lower = symptoms.lower()
    urgent_count = sum(1 for word in urgent_words if word in symptoms_lower)

    if urgent_count >= 2:
        return {"level": "critical", "score": 9, "advice": "СРОЧНО обратитесь к врачу!"}
    elif urgent_count == 1 or any(word in symptoms_lower for word in moderate_words):
        return {"level": "moderate", "score": 6, "advice": "Рекомендуется обратиться к врачу в ближайшее время"}
    else:
        return {"level": "low", "score": 3, "advice": "Можно обратиться к врачу при первой возможности"}