# 🤖 AI Voice Assistant with Groq & LLaMA


An intelligent, voice-activated chatbot that enables natural spoken conversation. This project combines **speech recognition**, **large language model processing** via Groq's ultra-fast API, and **text-to-speech** to create a seamless, real-time voice interaction loop—like having a conversation with a highly capable AI assistant.

## ✨ Features

- **🎤 Real-Time Voice Input**: Start/stop recording with a simple key press (default: `Ctrl+Shift`).
- **🧠 Powerful AI Backend**: Leverages Groq's `llama-3.1-70b-versatile` model for intelligent, context-aware text generation.
- **🗣️ Voice & Text Output**: Receives responses both as synthesized speech and printed text in the terminal.
- **🧵 Contextual Memory**: Maintains conversation history, allowing for coherent multi-turn dialogues.
- **⚡ Low-Latency Design**: Utilizes the Groq API for fast audio transcription and text generation.

## 🏗️ System Architecture

```mermaid
graph LR
    A[User Presses Key] --> B[Record Audio];
    B --> C[Send to Groq<br/>for Transcription];
    C --> D[Transcribed Text];
    D --> E[Append to<br/>Conversation History];
    E --> F[Send History to<br/>LLaMA 3.1 via Groq];
    F --> G[Generate AI Response];
    G --> H[Append Response<br/>to History];
    H --> I[Print to Terminal];
    H --> J[Convert to Speech<br/>via pyttsx3];
    I --> K[User Hears & Sees Response];
    J --> K;
