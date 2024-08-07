import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
from groq import Groq
import google.generativeai as genai
from pydub.playback import play

# Initialize the recognizer
r = sr.Recognizer()
play_obj = None


# Initialize clients with your API keys
groq_client = Groq(api_key="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")
genai.configure(api_key="AIzaSyBwMwo1r2qQ3walNFTn6dGfJaVHv_ukAzE")

model_name = 'llama3-8b-8192'

# System message for the AI model
sys_msg = (
    'You are Science Density, an AI English speaking coach. Your task is to help the user practice and improve their spoken English. '
    'Provide constructive feedback on their grammar, vocabulary, and pronunciation. Encourage the user and give them '
    'tips on how to improve their spoken English skills. Make sure your responses are clear and easy to understand.'
)

# Generation configuration
generation_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048
}

# Safety settings
safety_settings = [
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_NONE'
    }
]

# Initialize the Generative Model
model = genai.GenerativeModel(
    'gemini-1.5-flash-latest',
    generation_config=generation_config,
    safety_settings=safety_settings
)


# Function to generate a prompt response
def groq_prompt(prompt):
    convo = [
        {'role': 'system', 'content': sys_msg},
        {'role': 'user', 'content': prompt}
    ]
    chat_completion = groq_client.chat.completions.create(messages=convo, model=model_name)
    response = chat_completion.choices[0].message
    return response.content  # Correctly accessing the content attribute

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
        response = groq_prompt(text)
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