# import necessary libraries
import os
import wave
import pyaudio
import pyttsx3
from pynput import keyboard
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Initialize the Groq client (replace with your API key)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Chat Groq model
model = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-70b-versatile")

# Initialize the TTS engine
engine = pyttsx3.init()

# Set the speech rate
engine.setProperty('rate', 150)  # Adjust this value to make the voice slower or faster

# Define recording parameters
CHUNK = 1024  # number of audio frames per buffer
FORMAT = pyaudio.paInt16  # each audio sample is stored as a 16-bit signed integer (2 bytes per sample)
CHANNELS = 1  # number of audio channels to be recorded
RATE = 44100  # how many audio samples are captured per second

recording = False  # Track recording state
frames = []  # To store audio frames

# function for stop when press enter or esc
def on_press(key):
    """
    Callback function to handle key presses.
    Stops the recording when Enter or Esc is pressed.
    """
    global recording
    if key == keyboard.Key.enter or key == keyboard.Key.esc:
        recording = False
        print("\nRecording stopped.")
        return False  # Stop listening for key presses

# function to record the audio
def record_audio():
    """
    Records audio and stops based on key press.
    """
    global recording, frames
    frames = []  # Reset frames before recording
    recording = True  # Start recording

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording... Press 'Enter' or 'Esc' to stop.")

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

# function to save the audio
def save_audio():
    """
    Saves the recorded audio to a file named 'audio.wav'.
    """
    global frames  # Declare frames as global to modify it
    filename = 'audio.wav'  # Use .wav extension since you're using the wave module
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio saved as: {filename}")
    frames = []  # Clear frames after saving
    return filename

# conversion of audio to text and then text to audio
def transcribe_audio(audio_file):
    """
    Transcribes the saved audio using Groq API.
    """
    try:
        with open(audio_file, 'rb') as f:
            transcription = client.audio.transcriptions.create(
                file=f,
                model="distil-whisper-large-v3-en",
                prompt="Specify context or spelling",  # Optional
                response_format="json",  # Optional
                language="en",  # Optional
                temperature=0.0  # Optional
            )

        print(f"Transcription: {transcription.text}")
        return transcription.text

    except Groq.APIError as e:
        print(f"Groq API Error: {e}")
        return ""

# Prompt template
template = """
Answer the question below.Don't add * in the headings of the output.

Here is the conversation history:{context}

Question: {question}

Answer: 
"""
prompt = ChatPromptTemplate.from_template(template)

# chain the model and prompt
chain = prompt | model

# handle conversation and model response
def process_with_model(user_input, context=""):
    """
    Pass the user input to the LLM and get the response.
    """
    result = chain.invoke({"context": context, "question": user_input})
    print("Bot:", result.content)

    # Append the conversation to context
    new_context = f"{context}\nUser: {user_input}\nAI: {result.content}"

    return result.content, new_context

# Main function to handle everything: voice, model interaction, and text-to-speech
def handle_conversation():
    context = ""
    print("Welcome to the AI chatbot. How may I help you?")

    while True:
        # Listen for key presses to stop recording
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        # Start recording audio
        record_audio()

        # Wait for listener to finish (when recording stops)
        listener.join()

        # Save and process the recorded audio
        saved_audio = save_audio()
        user_input = transcribe_audio(saved_audio)

        if user_input.strip():  # If transcription is not empty
            # Get response from the model
            response, context = process_with_model(user_input, context)

            # Speak the response
            engine.say(response)
            engine.runAndWait()

        # Optional: Clean up the saved file
        # os.remove(saved_audio)

#if __name__ == "__main__":



handle_conversation()   
