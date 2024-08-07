from groq import Groq
import google.generativeai as genai
import Google_audio_process
from pydub.playback import play
from pydub import AudioSegment

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