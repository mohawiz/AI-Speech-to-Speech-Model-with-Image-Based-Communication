 AI Chatbot with Speech-to-Text and Text-to-Speech

This project is an AI-powered chatbot that allows users to interact using voice input. It utilizes speech recognition, text generation using Groq AI, and text-to-speech to deliver responses. The chatbot is capable of recording audio, transcribing it into text, processing it through a language model, and then providing a spoken response. 

 Features

- Voice Input: Record audio using a microphone.
- Speech Recognition: Transcribe the recorded audio into text using the Groq API.
- Language Model Integration: Process the text through the Groq LLM (`llama-3.1-70b-versatile`).
- Text-to-Speech: Convert the chatbot's response into audio using the `pyttsx3` library.
- Conversation History: Maintain context of the conversation for more coherent interactions.
  
Tech Stack

- Python: Core programming language.
- Groq API: Used for both text generation and audio transcription.
- Pyttsx3: Text-to-speech engine to provide spoken responses.
- Pyaudio: For recording audio input.
- Pynput: To handle key press events for controlling the recording.

 Setup

Requirements

Make sure you have the following libraries installed:

bash
pip install pyaudio pyttsx3 pynput groqapi langchain_core langchain_groq
