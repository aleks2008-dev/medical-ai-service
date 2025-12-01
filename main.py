from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

SYMPTOM_DOCTOR_MAP = {
    "голова": ["невролог", "терапевт"],
    "температура": ["терапевт"],
    "кашель": ["пульмонолог", "терапевт"],
    "живот": ["гастроэнтеролог"],
    "глаз": ["офтальмолог"],
    "зуб": ["стоматолог"]
}    

SYSTEM_PROMPT = """
Ты — медицинский ассистент. 
Когда пациент описывает симптомы, ты должен проанализировать их и дать рекомендацию врача.
Используй функцию recommend_doctor для анализа симптомов.
"""



def recommend_doctor(symptoms: str) -> str:
    """Рекомендует профиль врача по введенным симптомам."""
    matches = []
    for word, doctors in SYMPTOM_DOCTOR_MAP.items():
        if word in symptoms.lower():
            matches.extend(doctors)
    if matches:
        unique_doctors = ', '.join(set(matches))
        return f"Вам стоит обратиться к следующему специалисту: {unique_doctors}."
    else:
        return "Рекомендую для начала обратиться к терапевту."


model = init_chat_model(
    "llama3.2:3b",
    model_provider="ollama",
    temperature=0,
    base_url="http://localhost:11434"
)

def analyze_and_respond(user_input: str) -> str:
    """Анализирует ввод пользователя и возвращает ответ."""
    # Проверяем на наличие симптомов
    symptom_keywords = ["болит", "боль", "температура", "кашель", "симптом", "плохо", "живот", "голова", "глаз", "зуб"]
    
    if any(keyword in user_input.lower() for keyword in symptom_keywords):
        # Если найдены симптомы, используем функцию recommend_doctor
        doctor_recommendation = recommend_doctor(user_input)
        
        # Используем модель для формирования ответа
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Пациент говорит: {user_input}\nРекомендация врача: {doctor_recommendation}\nСформулируй дружелюбный ответ пациенту.")
        ]
        
        response = model.invoke(messages)
        return response.content
    else:
        # Обычный разговор
        messages = [
            SystemMessage(content="Ты дружелюбный медицинский ассистент. Отвечай кратко и вежливо."),
            HumanMessage(content=user_input)
        ]
        
        response = model.invoke(messages)
        return response.content

# Тестовые примеры
try:
    response = analyze_and_respond("У меня болит голова и температура")
    print(f"Ответ ИИ: {response}")
except Exception as e:
    print(f"Ошибка: {e}")

try:
    response2 = analyze_and_respond("thank you!")
    print(f"Второй ответ ИИ: {response2}")
except Exception as e:
    print(f"Ошибка: {e}")

# Интерактивный режим
print("\nИнтерактивный режим (введи 'quit' для выхода):")

while True:
    user_input = input("\nВопрос: ")
    if user_input.lower() in ['quit', 'выход', 'q']:
        break
    
    try:
        response = analyze_and_respond(user_input)
        print(f"Ответ: {response}")
    except Exception as e:
        print(f"Ошибка: {e}")