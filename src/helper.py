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
        r.adjust_for_ambient_noise(source, duration=1)  # Handle background noise

        try:
            # Wait up to 5s for speech to start, then listen for up to 15s
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("🕒 You didn't start speaking in time.")
            return "I didn't hear anything. Please try again."

    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
        return text

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you were trying to say.")
        return "Sorry, I could not understand what you said."

    except sr.RequestError as e:
        print(f"Sorry, I could not request results from Google Speech Recognition Service: {e}")
        return "Sorry, I couldn't reach the speech recognition service."

import google.generativeai as genai
from google.api_core.timeout import ExponentialTimeout
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded, GoogleAPICallError

def llm_model(user_text):
    # Configure Gemini API
    genai.configure(api_key=GOOGLE_API_KEY)

    # Use a fast and free-tier friendly model
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    # Log the prompt being sent
    print(f"[DEBUG] Prompt sent to Gemini: {user_text}")

    # Guard against empty or too-short prompts (likely from voice input)
    if not user_text or len(user_text.strip()) < 5:
        return "🗣️ I didn't catch that clearly. Could you please repeat it?"

    try:
        # Make API call with a timeout to prevent hanging
        response = model.generate_content(
            user_text,
            request_options={"timeout": ExponentialTimeout(initial=5, maximum=10)}
        )
        result = response.text

    except ResourceExhausted:
        result = "🚫 You're hitting your free-tier quota. Please try again later."

    except DeadlineExceeded:
        result = "⏰ Gemini took too long to respond. Try again shortly."

    except GoogleAPICallError as e:
        result = f"⚠️ API error occurred: {str(e)}"

    except Exception as e:
        result = f"🔥 Unexpected error: {str(e)}"

    return result


def text_to_speech(text):
    tts=gTTS(text=text, lang="en")

    tts.save("speech.mp3")