import streamlit as st #imports the Streamlit library used to create the UI as st
from gtts import gTTS #imports the gTTS class from the gtts library. Think of it as the engine for the text-to-speech conversion
import base64 #This module is used to encode binary data like the audio into a text-based format
from io import BytesIO #The BytesIO class from the io module allows us to save the audio without storing it to a physical file on a disk
from typing import Optional #This allows us to do the usual type annotation we learnt in Python Beginners. This module is optional: we can do without it.

# The session state for audio is initialized here
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'audio_generated' not in st.session_state:
    st.session_state.audio_generated = False

def get_binary_file_downloader_html(bin_file:bytes, file_label:str='File')-> str:
    """Generates an HTML link to download a binary file.

    :param bin_file: The binary data of the file to be downloaded
    :type bin_file: bytes
    :param file_label: The label for the download link and filename
    :type file_label: str
    :returns: An HTML string with a downloadable link
    :rtype: str
    """
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.mp3">Download audio file</a>'
    return href

def text_to_speech(text:str, language:str='en', slow:bool=False) -> Optional:
    """Converts text to speech using the Google text-to-speech library
    
    :param text: The text to be converted to speech.
    :type text: str
    :param language: The language code for the speech synthesis.
    :type language: str
    :param slow: If True, the speech will be slower.
    :type slow: bool
    :returns: The audio data as a bytes object or None on error.
    :rtype: Optional
    """
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def main() -> None:
    """Main function to run this code-to-speech application.
    
    This function sets up the user interface and handles user input.
    It also triggers the text-to-speech conversion and audio playback
    """
    st.title("Code-to-Speech: A Developer Assistant") #Creates the main title at the top of the app
    st.write("Paste your code below and have it read aloud to you!") #Adds a brief description below the title
    
    # Sidebar controls
    st.sidebar.header("Speech Settings") #Sets the header "Speech Settings" for the sidebar
    language = st.sidebar.selectbox(
        "Select Language",
        ['en', 'es', 'fr', 'de'],
        index=0
    ) #creates a drop down menu for users to select their preferred language
    slow_speech = st.sidebar.checkbox("Slow Speech", False)
    
    # Creates the text area where users can pastes their code
    code = st.text_area(
        "Paste your code here:",
        height=400,
        value="# This is an example code \n def our_message ( ): \n       print('We the members of Group 18 find this project quite difficult')"
    )
    
    
    col1, col2 = st.columns(2) #Create two columns for buttons and places them side by side
    
    with col1:
        if st.button("Read Code Aloud") and code.strip(): # A conditional statement that triggers when the "Read aloud button" is clicked
            with st.spinner("Generating speech..."): #Displays "Generating speech..." while the text_to_speech function is running
                audio_data = text_to_speech(code, language=language, slow=slow_speech)
                if audio_data:
                    st.session_state.audio_bytes = audio_data
                    st.session_state.audio_generated = True
                    st.success("Audio generated successfully!")
    
    with col2:
        if st.button("Test Voice"): #Triggers a test voice message
            with st.spinner("Testing voice..."): #Displays "Testing voice..." while the text_to_speech reads out the test_text
                test_text = "This is a test of the voice settings."
                audio_data = text_to_speech(test_text, language=language, slow=slow_speech) #Calls the text_to_speech data to generate audio
                if audio_data:
                    st.session_state.audio_bytes = audio_data
                    st.session_state.audio_generated = True
                    st.success("Voice test complete!")
    
    # Display audio player if audio exists
    if st.session_state.audio_generated and st.session_state.audio_bytes:
        st.audio(st.session_state.audio_bytes, format='audio/mp3')
        st.markdown(get_binary_file_downloader_html(
            st.session_state.audio_bytes, 
            "code_audio"
        ), unsafe_allow_html=True)


#This displays the instructions on how to use the code-to-speech
        st.markdown("""
            ### How to Use:
            1. Paste your code in the text area
            2. Adjust voice settings in the sidebar
            3. Click "Read Code Aloud" to hear your code
            4. Additionally, you can download the audio file
            ### Note:
            - Maximum ~1000 characters per request
            - Internet connection is required
            """)   
        
#The entry point to the code 
if __name__ == "__main__":
    main()
