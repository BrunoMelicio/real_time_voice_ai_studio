"""
Voice Chat MVP - Real-time conversation with an LLM
Uses Groq API for LLM and Whisper STT, pyttsx3 for TTS
"""

import os
import io
import base64
import tempfile
import threading
import subprocess
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from groq import Groq
import pyttsx3

load_dotenv()

app = FastAPI(title="Voice Chat MVP")

@app.middleware("http")
async def log_and_no_cache(request: Request, call_next):
    ua = request.headers.get("user-agent", "")
    print(f"[REQ] {request.method} {request.url.path} | UA: {ua}")
    response = await call_next(request)
    # Prevent aggressive browser caching of static HTML and API responses
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-large-v3-turbo")

# Initialize Groq client
groq_client = None
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)

# Conversation history for context
conversation_history = []

# TTS engine (initialized per-request due to threading issues)
tts_lock = threading.Lock()


def get_tts_engine():
    """Get a new TTS engine instance."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)  # Speed of speech
    engine.setProperty('volume', 0.9)
    return engine


def text_to_speech(text: str) -> bytes:
    """Convert text to speech and return audio bytes."""
    with tts_lock:
        engine = get_tts_engine()

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name

        try:
            engine.save_to_file(text, temp_path)
            engine.runAndWait()

            # Read the file
            with open(temp_path, "rb") as f:
                audio_data = f.read()

            # On macOS, pyttsx3 writes AIFF-C format even with .wav extension.
            # Convert to standard PCM WAV using afconvert if available for browser compatibility.
            if audio_data.startswith(b'FORM'):
                wav_converted = temp_path + ".converted.wav"
                try:
                    subprocess.run(
                        ["afconvert", "-f", "WAVE", "-d", "LEI16", temp_path, wav_converted],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    with open(wav_converted, "rb") as f:
                        audio_data = f.read()
                except Exception:
                    pass
                finally:
                    if os.path.exists(wav_converted):
                        os.remove(wav_converted)

            return audio_data
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
            engine.stop()


def speech_to_text(audio_data: bytes, filename: str = "audio.webm") -> str:
    """Transcribe audio using Groq Whisper API."""
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq API key not configured")

    try:
        transcription = groq_client.audio.transcriptions.create(
            file=(filename, audio_data),
            model=WHISPER_MODEL,
            response_format="text",
        )
        return str(transcription).strip()
    except Exception as e:
        print(f"Speech-to-text error: {e}")
        return ""


def get_llm_response(user_message: str, use_history: bool = True) -> str:
    """Get response from Groq LLM."""
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq API key not configured")

    global conversation_history

    # Build messages
    messages = [
        {
            "role": "system",
            "content": "You are a helpful, friendly voice assistant. Keep your responses concise and conversational since they will be spoken aloud. Avoid using markdown, bullet points, or special formatting."
        }
    ]

    if use_history:
        messages.extend(conversation_history[-10:])  # Keep last 10 exchanges

    messages.append({"role": "user", "content": user_message})

    # Get response
    completion = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    assistant_message = completion.choices[0].message.content

    # Update history
    if use_history:
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": assistant_message})

    return assistant_message


@app.get("/")
async def root():
    """Serve the main page."""
    return FileResponse(
        "static/index.html",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "groq_configured": groq_client is not None,
    }


@app.post("/api/chat")
async def chat(message: dict):
    """Text chat endpoint."""
    user_text = message.get("text", "")
    if not user_text:
        raise HTTPException(status_code=400, detail="No text provided")

    response_text = get_llm_response(user_text)

    return {"response": response_text}


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """Transcribe audio to text."""
    audio_data = await audio.read()

    if len(audio_data) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    text = speech_to_text(audio_data, audio.filename or "audio.webm")

    return {"text": text}


@app.post("/api/speak")
async def speak(message: dict):
    """Convert text to speech."""
    text = message.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    audio_data = text_to_speech(text)
    audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    return {"audio": audio_base64, "format": "wav"}


@app.post("/api/voice-chat")
async def voice_chat(audio: UploadFile = File(...)):
    """Full voice chat: transcribe -> LLM -> TTS."""
    # 1. Transcribe audio
    audio_data = await audio.read()
    if len(audio_data) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    user_text = speech_to_text(audio_data, audio.filename or "audio.webm")
    user_text = user_text.strip() if user_text else ""

    if not user_text:
        return {
            "user_text": "",
            "response_text": "",
            "response_audio": "",
            "audio_format": "wav",
            "empty": True,
        }

    # 2. Get LLM response
    response_text = get_llm_response(user_text)

    # 3. Convert response to speech
    response_audio = text_to_speech(response_text)
    audio_base64 = base64.b64encode(response_audio).decode("utf-8")

    return {
        "user_text": user_text,
        "response_text": response_text,
        "response_audio": audio_base64,
        "audio_format": "wav",
        "empty": False,
    }


@app.post("/api/clear-history")
async def clear_history():
    """Clear conversation history."""
    global conversation_history
    conversation_history = []
    return {"status": "cleared"}


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket for real-time voice chat."""
    await websocket.accept()

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()

            msg_type = data.get("type")

            if msg_type == "text":
                # Text message
                user_text = data.get("text", "")
                response_text = get_llm_response(user_text)

                await websocket.send_json({
                    "type": "response",
                    "user_text": user_text,
                    "response_text": response_text,
                })

            elif msg_type == "audio":
                # Audio message (base64 encoded)
                audio_b64 = data.get("audio", "")
                audio_data = base64.b64decode(audio_b64)

                # Transcribe
                user_text = speech_to_text(audio_data)

                await websocket.send_json({
                    "type": "transcription",
                    "text": user_text,
                })

                # Get LLM response
                response_text = get_llm_response(user_text)

                # Generate TTS
                response_audio = text_to_speech(response_text)
                audio_base64 = base64.b64encode(response_audio).decode("utf-8")

                await websocket.send_json({
                    "type": "response",
                    "user_text": user_text,
                    "response_text": response_text,
                    "response_audio": audio_base64,
                    "audio_format": "wav",
                })

            elif msg_type == "clear":
                global conversation_history
                conversation_history = []
                await websocket.send_json({"type": "cleared"})

    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
