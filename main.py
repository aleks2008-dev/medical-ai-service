from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy

SYMPTOM_DOCTOR_MAP = {
    "голова": "невролог, терапевт",
    "температура": "терапевт",
    "кашель": "пульмонолог, терапевт",
    "живот": "гастроэнтеролог",
    "глаз": "офтальмолог",
    "зуб": "стоматолог"
}    

SYSTEM_PROMPT = """
Ты — медицинский ассистент.
Если пациент описывает свои симптомы — используй только инструмент recommend_doctor для рекомендации подходящего специалиста-врача.
"""

@dataclass
class Context:
    user_id: str

@tool
def recommend_doctor (symptoms: str) -> str:
    """Рекомендует профиль врача по введенным симптомам."""
    matches = []
    for word, doctor in SYMPTOM_DOCTOR_MAP.items():
        if word in symptoms.lower():
            matches.append(doctor)
    if matches:
        doctors = ', '.join(set(matches))
        return f"Вам стои обратиться к следующему специалисту: {doctors}."
    else:
        return "Рекомендую для начала обратиться к терапевту."


model = init_chat_model(
    "llama3.2:3b",
    model_provider="ollama",
    temperature=0,
    base_url="http://localhost:11434"
)

@dataclass
class ResponseFormat:
    doctor_recommendation: str | None = None

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[recommend_doctor],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"message": [{"role": "user", "content": "У меня болит голова и температура"}]},
    config=config,
    context=Context(user_id="1")
)

# Извлекаем ответ из messages
if 'messages' in response and response['messages']:
    ai_message = response['messages'][-1]
    print(f"Ответ ИИ: {ai_message.content}")
else:
    print("Нет сообщений в ответе")

response2 = agent.invoke(
    {"message": [{"role": "user", "content": "thank you!"}]},
    config=config,
    context=Context(user_id="1")
)

if 'messages' in response2 and response2['messages']:
    ai_message2 = response2['messages'][-1]
    print(f"Второй ответ ИИ: {ai_message2.content}")

# Интерактивный режим
print("\nИнтерактивный режим (введи 'quit' для выхода):")

while True:
    user_input = input("\nВопрос: ")
    if user_input.lower() in ['quit', 'выход', 'q']:
        break
    
    try:
        response = agent.invoke(
            {"message": [{"role": "user", "content": user_input}]},
            config=config,
            context=Context(user_id="1")
        )
        
        if 'messages' in response and response['messages']:
            ai_message = response['messages'][-1]
            print(f"Ответ: {ai_message.content}")
        else:
            print("Нет ответа от ИИ")
            
    except Exception as e:
        print(f"Ошибка: {e}")