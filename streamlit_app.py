import streamlit as st
import SD_Brain
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
import os

# Initialize the recognizer
r = sr.Recognizer()
play_obj = None

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
    global play_obj
    audio = AudioSegment.from_wav(file_path)
    wave_obj = sa.WaveObject(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait for the audio to finish playing

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

# Display history in a traditional format
st.subheader("History")
for user_text, response in st.session_state.history:
    with st.expander(user_text):
        st.write(f"Science Density: {response}")