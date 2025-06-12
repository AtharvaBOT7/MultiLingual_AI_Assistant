import os
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

os.environ["FLAC_CONVERTER"] = "/opt/homebrew/bin/flac"

def voice_input():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you were trying to say.")
    except sr.RequestError as e:
        print("Sorry, I could not request results from Google Speech Recognition Service: {0}".format(e))

def llm_model(user_text):
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    response = model.generate_content(user_text)

    result = response.text

    return result

def text_to_speech(text):
    tts=gTTS(text=text, lang="en")

    tts.save("speech.mp3")