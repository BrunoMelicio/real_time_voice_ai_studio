# CLAUDE.md - AI Assistant Guidelines

This document provides context and guidelines for AI assistants working with this repository.

## Project Overview

**Repository**: Voice Chat MVP
**Type**: Real-time voice conversation with LLM
**Language**: Python (Backend), HTML/CSS/JS (Frontend)
**Last Updated**: 2026-02-01

A web-based application that enables real-time voice conversations with an AI assistant. Users can type messages or use voice input, and receive both text and spoken responses.

### Key Features

- Text chat with LLM
- Push-to-talk voice recording
- Live conversation mode (continuous voice chat)
- Speech-to-text via Groq Whisper API
- Text-to-speech for AI responses
- Conversation history tracking

## Codebase Structure

```
claude_code_test/
├── CLAUDE.md           # AI assistant guidelines (this file)
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── main.py             # FastAPI backend server
└── static/
    └── index.html      # Web UI (single-page app)
```

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI server with all API endpoints (chat, transcribe, TTS, WebSocket) |
| `static/index.html` | Complete frontend UI with chat interface and audio recording |
| `requirements.txt` | Python package dependencies |
| `.env.example` | Template for required environment variables |

## Development Workflow

### Getting Started

```bash
# Clone the repository
git clone <repository-url>
cd claude_code_test

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Groq API key

# Run the server
python main.py
# Or: uvicorn main:app --reload

# Open http://localhost:8000 in your browser
```

### Common Commands

```bash
# Run development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run production server
python main.py

# Install new dependency
pip install <package> && pip freeze > requirements.txt
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve main web UI |
| `/api/health` | GET | Health check, verify API configuration |
| `/api/chat` | POST | Send text message, receive LLM response |
| `/api/transcribe` | POST | Upload audio, receive transcription |
| `/api/speak` | POST | Send text, receive audio (base64) |
| `/api/voice-chat` | POST | Full pipeline: audio -> transcribe -> LLM -> TTS |
| `/api/clear-history` | POST | Clear conversation history |
| `/ws/chat` | WebSocket | Real-time bidirectional chat |

## Code Conventions

### Python Style

- Use type hints for function parameters and returns
- Keep functions focused and under 50 lines when possible
- Use descriptive variable names
- Handle exceptions gracefully with appropriate error responses
- Use async/await for I/O operations

### Frontend Style

- Vanilla JavaScript (no frameworks for MVP)
- CSS variables for theming
- Mobile-responsive design
- Semantic HTML elements

### Commit Messages

Use conventional commits:
```
<type>: <short description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Dependencies

### Core Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework for API |
| `uvicorn` | ASGI server |
| `groq` | Groq API client (LLM + Whisper) |
| `pyttsx3` | Offline text-to-speech |
| `python-multipart` | File upload handling |
| `python-dotenv` | Environment variable loading |
| `websockets` | WebSocket support |

### External APIs

| API | Model | Purpose | Cost |
|-----|-------|---------|------|
| Groq LLM | `llama-3.1-8b-instant` | Chat responses | Free tier with limits |
| Groq Whisper | `distil-whisper-large-v3-en` | Speech-to-text | Lowest rate usage |

**Note**: We use `distil-whisper-large-v3-en` instead of larger models to minimize API rate usage.

## Security

### Critical Security Principles

**NEVER commit secrets to the repository.** This includes:
- API keys (Groq, OpenAI, etc.)
- Passwords and tokens
- Private keys or certificates
- Database connection strings

### Environment Variables

All sensitive configuration MUST be stored in environment variables:

```bash
# .env file (NEVER commit this file)
GROQ_API_KEY=gsk_xxxxxxxxxxxx
```

### Security Checklist

- [ ] `.env` is in `.gitignore` (prevents accidental commits)
- [ ] Only `.env.example` with placeholder values is committed
- [ ] API keys are loaded via `os.getenv()` or `python-dotenv`
- [ ] No hardcoded secrets in source code
- [ ] No secrets in comments or documentation

### When Adding New APIs

1. Add the variable name to `.env.example` with a placeholder
2. Document the variable in this file's Configuration section
3. Load via `os.getenv("VARIABLE_NAME")` in code
4. Handle missing keys gracefully (check if None before use)

### What to Avoid

- **NEVER** hardcode API keys: `client = Groq(api_key="gsk_xxx")`
- **NEVER** commit `.env` files
- **NEVER** log or print API keys
- **NEVER** expose keys in error messages or responses
- **NEVER** store keys in frontend JavaScript

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key from console.groq.com | Yes |

### Getting a Groq API Key

1. Go to https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Add it to your `.env` file

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│   FastAPI   │────▶│  Groq API   │
│  (Web UI)   │◀────│   Server    │◀────│ (LLM/STT)   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   pyttsx3   │
                    │    (TTS)    │
                    └─────────────┘
```

### Data Flow

1. **Text Chat**: User types → API → Groq LLM → Response text → pyttsx3 → Audio
2. **Voice Chat**: User speaks → Record → Groq Whisper → Text → Groq LLM → Response → pyttsx3 → Audio

## AI Assistant Guidelines

### Before Making Changes

1. Read `main.py` to understand the API structure
2. Check `static/index.html` for frontend state management
3. Understand the Groq API integration patterns

### When Making Changes

1. Maintain the simple MVP architecture
2. Keep the single-file backend structure unless complexity demands splitting
3. Test voice recording in browser (requires HTTPS or localhost)
4. Ensure error handling for API failures

### Things to Avoid

- Don't add complex state management frameworks
- Don't split the frontend into multiple files unnecessarily
- Don't store sensitive data in conversation history
- Don't remove the health check endpoint
- **NEVER hardcode API keys or secrets in code**
- **NEVER commit .env files or expose credentials**
- Don't log sensitive data (API keys, user audio, etc.)

## Troubleshooting

### Common Issues

1. **"Groq API key not configured"**
   - Ensure `.env` file exists with `GROQ_API_KEY`
   - Restart the server after adding the key

2. **Microphone not working**
   - Check browser permissions
   - Must use HTTPS or localhost (not IP address)
   - Try a different browser

3. **TTS not working (Linux)**
   - Install espeak: `sudo apt-get install espeak`
   - Install required audio libraries

4. **Audio format errors**
   - Browser may not support webm; the server handles conversion

## Future Enhancements

Potential improvements for future development:

- [ ] Better TTS (ElevenLabs, Coqui, or OpenAI TTS)
- [ ] Streaming LLM responses
- [ ] Voice activity detection for live mode
- [ ] Multiple conversation threads
- [ ] User authentication
- [ ] Persistent chat history

## Resources

- [Groq Documentation](https://console.groq.com/docs)
- [Groq Whisper API](https://console.groq.com/docs/speech-to-text)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)

---

*This CLAUDE.md should be updated as the project evolves.*
