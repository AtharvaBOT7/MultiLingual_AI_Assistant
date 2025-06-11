import os
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

def voice_input():
    pass

def llm_model(user_text):
    pass

def text_to_speech(text):
    pass