# 🏥 Medical AI Service

Intelligent medical assistant for symptom analysis and specialist doctor recommendations.

## 🚀 Features

- **Symptom Analysis** - AI-powered recognition of medical complaints
- **Doctor Recommendations** - suggests appropriate specialists based on symptoms
- **Multilingual Support** - Russian and English languages
- **Interactive CLI** - console chat interface with the assistant
- **Local Processing** - works with Ollama without sending data to the cloud
- **Performance Optimized** - fast responses with caching and graceful degradation
- **Production Ready** - comprehensive testing, Docker support, health checks

## 🛠️ Technologies

- **Python 3.8+**
- **LangChain** - framework for working with LLM
- **Ollama** - local language model execution
- **Llama 3.2:3b** - optimized language model
- **Clean Architecture** - proper separation of concerns
- **Singleton Pattern** - optimized model loading

## 📋 Supported Symptoms

100+ symptoms mapped to appropriate specialists:

| Category | Examples | Recommended Doctors |
|----------|----------|--------------------|
| Neurological | Headache, dizziness, weakness | Neurologist, General Practitioner |
| Respiratory | Cough, shortness of breath | Pulmonologist, General Practitioner |
| Gastrointestinal | Abdominal pain, nausea | Gastroenterologist |
| Cardiovascular | Chest pain, heart palpitations | Cardiologist |
| Dermatological | Rash, itching | Dermatologist |
| Ophthalmological | Eye problems, vision issues | Ophthalmologist |
| Dental | Toothache, gum problems | Dentist |
| ENT | Throat pain, ear problems | Otolaryngologist |

## 🔧 Installation

### 1. Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Download the model

```bash
ollama pull llama3.2:3b-instruct-q4_0
```

### 3. Clone the repository

```bash
git clone https://github.com/aleks2008-dev/medical-ai-service.git
cd medical-ai-service
```

### 4. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### 1. Start Ollama

```bash
ollama serve
```

### 2. Run the assistant

```bash
python main.py
```

## 💬 Usage Examples

```
Вопрос: У меня болит голова и температура
Ответ: Понимаю, что вам нехорошо. При головной боли и температуре рекомендую обратиться к терапевту или неврологу. Они проведут необходимое обследование и назначат подходящее лечение.

Вопрос: Кашель уже неделю
Ответ: При длительном кашле следует обратиться к пульмонологу или терапевту для диагностики и лечения.

Question: Thank you for your help!
Answer: You're welcome! Take care of yourself and don't delay visiting a doctor when necessary.
```

## ⚙️ Configuration

Model settings in `src/config/settings.py`:

```python
MODEL_NAME = "llama3.2:3b-instruct-q4_0"
MODEL_PROVIDER = "ollama"
MODEL_TEMPERATURE = 0
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NUM_CTX = 512  # Optimized context
MODEL_NUM_PREDICT = 192  # Balanced response length
```

## 🏗️ Architecture

### Clean Architecture Implementation
```
src/
├── config/           # Configuration layer
├── models/           # Domain models
├── services/         # Business logic
└── utils/           # Infrastructure
```

### Key Features
- **Singleton Pattern** - Model loads once per session
- **Caching** - Responses cached for performance
- **Rate Limiting** - Graceful degradation under load
- **Health Checks** - Lightweight system monitoring
- **Error Handling** - Comprehensive exception management

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## 🐳 Docker Support

```bash
# Build and run
docker-compose up --build

# Or run with Docker
docker build -t medical-ai-service .
docker run -it medical-ai-service
```

## 📊 Performance

- **Response Time**: 2-5 seconds (optimized)
- **Memory Usage**: ~200MB (with model loaded)
- **Supported Load**: 10 requests/minute per user
- **Cache Hit Rate**: ~30% for common symptoms

## 🔍 Project Structure

```
medical-ai-service/
├── src/                    # Source code
│   ├── config/            # Configuration
│   │   └── settings.py    # Application settings
│   ├── models/            # Data models
│   │   └── symptom_data.py # Symptom-doctor mapping
│   ├── services/          # Business logic
│   │   ├── ai_service.py  # AI service (Singleton)
│   │   └── doctor_service.py # Doctor recommendations
│   └── utils/             # Utilities
│       ├── cli.py         # CLI interface
│       └── health.py      # Health checks
├── tests/                 # Test suite
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
├── Dockerfile           # Container configuration
├── docker-compose.yaml  # Multi-service setup
└── README.md           # Documentation
```

## ⚠️ Important Notes

- **Medical Disclaimer** - This tool is for initial consultation only, not a replacement for professional medical advice
- **Privacy** - All processing is local, no data sent to external services
- **Requirements** - Requires Ollama service running locally
- **Languages** - Supports Russian and English

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

Common issues and solutions:

1. **Ollama not running**
   ```bash
   ollama serve
   ```

2. **Model not found**
   ```bash
   ollama pull llama3.2:3b-instruct-q4_0
   ```

3. **Port conflicts**
   - Check if port 11434 is available
   - Modify OLLAMA_BASE_URL in .env if needed

4. **Performance issues**
   - Reduce MODEL_NUM_CTX in settings
   - Close other resource-intensive applications

---

**⚕️ Medical Disclaimer: This assistant provides general information only and does not replace professional medical consultation. Always consult qualified healthcare providers for medical advice.**