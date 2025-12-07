# 🏥 Medical AI Service

Intelligent medical assistant for symptom analysis and specialist doctor recommendations.

## 🚀 Features

- **Symptom Analysis** - recognizes patient medical complaints
- **Doctor Recommendations** - suggests appropriate specialists
- **AI-powered Responses** - uses LLM to generate friendly responses
- **Interactive Mode** - console chat with the assistant
- **Local Model** - works with Ollama without sending data to the cloud

## 🛠️ Technologies

- **Python 3.8+**
- **LangChain** - framework for working with LLM
- **Ollama** - local language model execution
- **Llama 3.2:3b** - language model

## 📋 Supported Symptoms

| Symptom | Recommended Doctors |
|---------|-------------------|
| Headache | Neurologist, General Practitioner |
| Fever | General Practitioner |
| Cough | Pulmonologist, General Practitioner |
| Abdominal Pain | Gastroenterologist |
| Eye Problems | Ophthalmologist |
| Toothache | Dentist |

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
ollama pull llama3.2:3b
```

### 3. Clone the repository

```bash
git clone https://github.com/your-username/medical-ai-service.git
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
Question: I have a headache and fever
Answer: I understand you're feeling unwell. For headache and fever, I recommend seeing a general practitioner or neurologist. They can conduct the necessary examination and prescribe appropriate treatment.

Question: I've had a cough for a week
Answer: For a persistent cough, you should see a pulmonologist or general practitioner for diagnosis and treatment.

Question: Thank you for your help!
Answer: You're welcome! Take care of yourself and don't delay visiting a doctor when necessary.
```

## ⚙️ Configuration

Model settings are located in `src/config/settings.py`:

```python
MODEL_NAME = "llama3.2:3b"
MODEL_PROVIDER = "ollama"
MODEL_TEMPERATURE = 0
OLLAMA_BASE_URL = "http://localhost:11434"
```

## 🔍 Project Structure

```
medical-ai-service/
├── src/                    # Source code
│   ├── config/            # Configuration
│   │   └── settings.py    # Application settings
│   ├── models/            # Data models
│   │   └── symptom_data.py # Symptom data
│   ├── services/          # Business logic
│   │   ├── ai_service.py  # AI service
│   │   └── doctor_service.py # Doctor service
│   └── utils/             # Utilities
│       └── cli.py         # CLI interface
├── main.py               # Main application file
├── requirements.txt      # Python dependencies
├── .gitignore           # Git exclusions
├── .env                 # Environment variables
└── README.md            # Documentation
```

## ⚠️ Important Notes

- **Does not replace a doctor** - this is a tool for initial consultation
- **Requires Ollama** - make sure the service is running
- **Local processing** - data is not sent to the internet
- **Limited vocabulary** - recognizes basic symptoms

## 🤝 Contributing

1. Fork the repository
2. Create a branch for new feature
3. Make changes
4. Create a Pull Request

## 📝 License

MIT License - see LICENSE file

## 🆘 Support

If you encounter problems:
1. Check that Ollama is running
2. Make sure the llama3.2:3b model is loaded
3. Check dependency versions

---

**⚕️ Remember: this assistant does not replace professional medical consultation!**