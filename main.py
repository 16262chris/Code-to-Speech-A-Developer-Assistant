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

# Set the title and a brief description for the Streamlit app
st.title("Code-to-Speech Developer Assistant 🗣️")
st.markdown("Enter your code snippet below and I'll read it aloud for you!")

st.sidebar.header("Speech Settings")
language = st.sidebar.selectbox("Select Language", ['en', 'es', 'fr', 'de'], index=0)

slow_speech = st.sidebar.checkbox("Slow Speech", False)

# Create a text area for the user to paste their code
code_snippet = st.text_area("Paste your code here:", height=250)

# Create a button that triggers the text-to-speech conversion
if st.button("Read Code Aloud"):
	# Check if the text area is not empty
	if code_snippet:
		# Display a spinner to show that audio is being generated
		with st.spinner("Generating audio..."):
			try:
				# Use gTTS to convert the text into an MP3 audio stream
				tts = gTTS(text=code_snippet, lang=language, slow=slow_speech)

				# Use BytesIO to store the audio data in memory
				# This avoids creating a temporary file on the disk
				audio_stream = io.BytesIO()
				tts.write_to_fp(audio_stream)

				# Move the stream's cursor to the beginning
				# so the Streamlit audio player can read from the start
				audio_stream.seek(0)

				# Play the generated audio using Streamlit's built-in audio player
				st.audio(audio_stream, format='audio/mp3')

				st.success("Playback started!")

			except Exception as e:
				# Catch and display any errors that occur during the conversion
				st.error(f"An error occurred: {e}")
	else:
		# Display a warning if the user tries to convert an empty text area
		st.warning("Please enter some code to convert.")

