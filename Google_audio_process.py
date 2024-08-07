import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment

# initialize the recognizer
r = sr.Recognizer()

# use the microphone as the source for input
def transcriber():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Web Speech could not understand the audio")
    except sr.Request as e:
        print("Could not request results form Google Web service")
        
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")

    # 轉換為 16 位 PCM 格式的 WAV 文件
    audio = AudioSegment.from_mp3("response.mp3")
    audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
    audio.export("response.wav", format='wav')