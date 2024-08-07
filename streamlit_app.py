import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

# Initialize the recognizer
r = sr.Recognizer()

# Use the microphone as the source for input
def transcriber():
    with sr.Microphone() as source:
        st.write("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source)
        st.write("Say something!")
        audio = r.listen(source)
        
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        st.write("Google Web Speech could not understand the audio")
        return None
    except sr.RequestError as e:
        st.write("Could not request results from Google Web service")
        return None
        
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")

    # Convert to 16-bit PCM format WAV file
    audio = AudioSegment.from_mp3("response.mp3")
    audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
    audio.export("response.wav", format='wav')

def play_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    play(audio)

st.title("Science Density")

# Initialize session state if not already initialized
if 'history' not in st.session_state:
    st.session_state.history = []

# Display current interaction
if st.button("Start Speak"):
    text = transcriber()
    if text:
        st.write(f"USER: {text}")
        response = SD_Brain.groq_prompt(text)
        speak(response)

        # Play new audio
        play_audio("response.wav")
        
        st.write(f"Science Density: {response}")

        # Add current interaction to history
        st.session_state.history.append((text, response))

        # Cleanup old audio files
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")
        if os.path.exists("response.wav"):
            os.remove("response.wav")

# Display history in a traditional format
st.subheader("History")
for user_text, response in st.session_state.history:
    with st.expander(user_text):
        st.write(f"Science Density: {response}")