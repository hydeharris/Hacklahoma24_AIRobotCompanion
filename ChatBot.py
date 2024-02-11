import os
import json 
from openai import OpenAI
import whisper
import elevenlabs
from dotenv import load_dotenv

#To allow this program to properly run create a .env file with the following API Keys. 
#OPENAI_API_KEY = ????, and ELEVENLABS_API_KEY = ????.
load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs.set_api_key(elevenlabs_api_key)

elevenlabs_voice = elevenlabs.Voice(
    voice_id="e5WbeGWUv6qtI4YtN188", #VoiceID from the ElevenLabs Voice library.
    settings=elevenlabs.VoiceSettings(
        stability = 1, 
        similarity_boost = 0.75
    )
)

#fastest and smallest version of Whisper for responses as quick as possible.
whisper_model = whisper.load_model("tiny") 

with open("config.json") as config_file:
    config_contents = json.load(config_file)


class Chatbot: 
    def __init__(self, model="gpt-3.5-turbo", input_mode="text"):
        self.client = OpenAI()
        self.model = model
        self.messages = []
    def set_system_message(self, system_message):
        self.messages.append({"role": "system", "content": system_message})
    
    def ask(self, user_message):
        self.messages.append({"role": "user", "content": user_message})

        response =  self.client.chat.completions.create(
            model = self.model,
            messages=self.messages
        )

        assisstant_message = response.choices[0].message.content

        return assisstant_message
    
    def transcribe_audio(self, audiofile):
        result = whisper_model.transcribe(audiofile)
        return result
        
    def set_communication_mode(self, mode): # this may be unneeded tbh depends on how the website ends up working. 
        self.input_mode = mode

    def generate_audio(self, text):
        audio = elevenlabs.generate(
            text = text,
            voice = elevenlabs_voice
        )
        return audio
    