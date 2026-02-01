# Voice Chat MVP

A real-time voice conversation app with an AI assistant. Talk or type to chat with an LLM.

## Features

- **Text Chat**: Type messages and get AI responses
- **Voice Recording**: Hold the microphone button to record and send voice messages
- **Live Mode**: Continuous voice conversation - the AI listens and responds automatically
- **Text-to-Speech**: Hear the AI's responses spoken aloud

## Quick Start

### 1. Get a Groq API Key (Free)

1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Create an API key

### 2. Setup

```bash
# Clone and enter the project
git clone <repository-url>
cd claude_code_test

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Run

```bash
python main.py
```

Open http://localhost:8000 in your browser.

## How to Use

| Action | How |
|--------|-----|
| Send text | Type in the input box and press Enter or click Send |
| Record voice | Hold the red microphone button |
| Live conversation | Click the green checkmark to toggle live mode |
| Clear chat | Click the X button |

## Tech Stack

- **Backend**: Python, FastAPI
- **LLM**: Groq API (Llama 3.1)
- **Speech-to-Text**: Groq Whisper API
- **Text-to-Speech**: pyttsx3 (offline)
- **Frontend**: Vanilla HTML/CSS/JS

## Requirements

- Python 3.8+
- Microphone (for voice features)
- Modern browser (Chrome, Firefox, Edge)
- Groq API key (free tier available)

## Troubleshooting

**Microphone not working?**
- Allow microphone access in browser
- Use `localhost` not an IP address

**No audio output?**
- On Linux, install espeak: `sudo apt install espeak`

**API errors?**
- Check your `.env` file has a valid `GROQ_API_KEY`
- Restart the server after adding the key

## License

MIT
