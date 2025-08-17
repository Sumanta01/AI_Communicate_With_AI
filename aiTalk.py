
import pyttsx3
import speech_recognition as sr
import time
import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv


# Load Gemini API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file!")
genai.configure(api_key=GEMINI_API_KEY)

# Text-to-speech
tts = pyttsx3.init()

# Speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()


# Strategy Pattern for Agent Behavior
class AgentStrategy:
    def __init__(self, name):
        self.name = name
    def speak(self, text):
        print(f"{self.name} 🗣️:", text)
        try:
            tts.say(text)
            tts.runAndWait()
        except Exception as e:
            print(f"[TTS ERROR for {self.name}]:", e)
    def think(self, message):
        system_prompt = f"You are {self.name}, having a conversation."
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])
        response = chat.send_message(message)
        return response.text

def think(agent_name, message):
    system_prompt = f"You are {agent_name}, having a conversation."
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])
    response = chat.send_message(message)
    return response.text


# Create agent strategies
agent_a = AgentStrategy("Agent A")
agent_b = AgentStrategy("Agent B")

# Fully automatic AI-to-AI conversation
message = "Hello, how are you?"  # Initial message from Agent A
while True:
    agent_a.speak(message)
    reply_b = agent_b.think(message)
    agent_b.speak(reply_b)
    message = agent_a.think(reply_b)
    time.sleep(1)
    print("--- Press Ctrl+C to stop the conversation ---")
