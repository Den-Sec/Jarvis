import os
import time
import requests
from gtts import gTTS
from pathlib import Path
from pygame import mixer  # Load the popular external library
from pydub import AudioSegment
from pydub.effects import speedup

tts_enabled = True

# Initialize mixer
mixer.init()

# Ollama endpoint
ollama_url = "http://192.168.1.247:11434/api/chat"  # Replace with your Ollama IP and port

# Function to ask a question to the assistant
def ask_question_standard(question):
    #Hint LLMs won't know the time or date unless you tell them
    date_and_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    context = f"""
    You are an AI assistant named Jarvis, modeled after the Jarvis from the Ironman movies.
    You are to act like him and provide help as best you can to your owner—me.
    Be funny and witty. Keep it brief and serious.
    Be a little sassy in your responses.
    You have a variety of smart devices to control.
    You can control them by ending your sentence with #light1-off like this.
    Only use commands like this if I tell you to do so. End your sentence with #lamp-1 for on and #lamp-0 for off.
    Respond in less than 80 words. {date_and_time}
    """
    
    response = requests.post(
        ollama_url,
        json={
            "model": "llama3",  # Replace with your actual model identifier
            "messages": [{"role": "system", "content": context}, {"role": "user", "content": question}],
            "stream": False
        }
    )
    # Debug: print the entire JSON response to see what's inside
    response_data = response.json()
    print("DEBUG: API Response -", response_data)

    # Check the response from the Ollama API
    if response.status_code == 200:
        try:
            # Extract the content from the message key
            return response_data['message']['content']
        except KeyError as e:
            # Print the error and return an error message if the expected key is missing
            print(f"KeyError: {e} - check the structure of the JSON response.")
            return "Error processing the response: Key not found in the response JSON."
    else:
        return "An error occurred: " + response.text

# Function to play a sound file
def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

# Function to generate TTS for each sentence and play them
def TTS(text):
    speech_file_path = Path("speech.mp3")
    generate_tts(text, speech_file_path, speed_factor=1.5)
    mixer.init()
    mixer.music.load(str(speech_file_path))
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()

    # Safely delete the file after playing
    try:
        os.remove(speech_file_path)
    except OSError as e:
        print(f"Error deleting the file {speech_file_path}: {e}")

    return "done"

# Function to generate TTS and return the file path
def generate_tts(sentence, speech_file_path, speed_factor=1.5):
    # Generate speech using gTTS
    tts = gTTS(text=sentence, lang='en', tld='com')
    tts.save(str(speech_file_path))
    
    # Load the audio file using pydub
    sound = AudioSegment.from_file(str(speech_file_path))
    
    # Use the speedup effect to adjust the playback speed without altering the pitch
    sound_with_correct_speed = speedup(sound, playback_speed=speed_factor)

    # Export the modified audio
    sound_with_correct_speed.export(str(speech_file_path), format="mp3")
