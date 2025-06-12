from src.helper import llm_model, voice_input, text_to_speech
import streamlit as st

def main():
    st.title("MultiLingual AI Assistant 🤖")

    if st.button("You can ask me anything..."):
        with st.spinner("Listening..."):
            text = voice_input()
            response = llm_model(text)
            text_to_speech(response)

            audio_file = open("speech.mp3",'rb')
            audio_bytes = audio_file.read()

            st.text_area(label="Response: ", value=response, height = 350)
            st.audio(audio_bytes)
            st.download_button(label="Download Speech",
                               data=audio_bytes,
                               file_name="speech.mp3",
                               mime="auido/mp3")

    