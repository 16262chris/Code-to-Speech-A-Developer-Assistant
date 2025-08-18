"""
Code-to-Speech Developer Assistant

This Streamlit application takes a code snippet as input and uses the Google
Text-to-Speech (gTTS) library to convert the text into an audible voice.
The generated audio is then played back directly within the application,
allowing developers to listen to their code while multitasking.
"""

import streamlit as st
from gtts import gTTS
import io


class CodeToSpeechConverter:
    """
    A class to handle the conversion of text to speech.
    """

    def __init__(self, text: str, lang: str = 'en', slow: bool = False):
        """
        Initializes the converter with text, language, and speech speed.

        :param text: The code snippet to be converted.
        :param lang: The language of the speech.
        :param slow: A boolean to determine if speech should be slow.
        """
        self.text = text
        self.lang = lang
        self.slow = slow

    def generate_audio(self) -> io.BytesIO:
        """
        Generates audio from the stored text and returns it as a BytesIO object.

        :return: An in-memory binary stream of the audio data.
        :raises Exception: If there is an error during audio generation.
        """
        if not self.text.strip():
            raise ValueError("The text to convert cannot be empty.")

        try:
            tts = gTTS(text=self.text, lang=self.lang, slow=self.slow)
            audio_stream = io.BytesIO()
            tts.write_to_fp(audio_stream)
            audio_stream.seek(0)
            return audio_stream
        except Exception as e:
            raise Exception(f"Failed to generate audio: {e}")

# --- Streamlit UI and App Logic ---


def main():
    """
    The main function to run the Streamlit application.
    """
    st.title("Code-to-Speech Developer Assistant 🗣️")
    st.markdown("Enter your code snippet below and I'll read it aloud for you!")

    st.sidebar.header("Speech Settings")
    language = st.sidebar.selectbox(
        "Select Language", ['en', 'es', 'fr', 'de'], index=0)
    slow_speech = st.sidebar.checkbox("Slow Speech", False)

    code_snippet = st.text_area("Paste your code here:", height=250)

    if st.button("Read Code Aloud"):
        if code_snippet:
            with st.spinner("Generating audio..."):
                try:
                    # Create an instance of the converter class
                    converter = CodeToSpeechConverter(
                        text=code_snippet,
                        lang=language,
                        slow=slow_speech
                    )

                    # Call the method to get the audio data
                    audio_stream = converter.generate_audio()

                    st.audio(audio_stream, format='audio/mp3')
                    st.success("Playback started!")
                except ValueError as ve:
                    st.warning(f"Warning: {ve}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter some code to convert.")


if __name__ == "__main__":
    main()
