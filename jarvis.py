# https://github.com/openai/whisper

import openai
import pyaudio
import os
import json
import wave
import random
import string
import numpy as np
import base64

openai.api_key = "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"

CHUNK = 1024  # number of audio samples per frame
FORMAT = pyaudio.paInt16  # audio format
CHANNELS = 1  # mono audio
RATE = 44100  # audio sampling rate
THRESHOLD = 1000  # audio threshold for silence detection
SILENCE_TIME = 3  # minimum silence time in seconds before stopping recording
SILENCE_INCREMENT = 30

# generate a random filename for the temporary audio file
def generate_filename():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(10)) + ".wav"

# open the audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

frames = []
silence_time = 0

# record audio until minimum silence time is reached
print("Listening...")
while True:
    data = stream.read(CHUNK)
    frames.append(data)

    # convert byte string to NumPy array
    samples = np.frombuffer(data, dtype=np.int16)

    # check if audio is below the threshold for silence
    if np.max(np.abs(samples)) < THRESHOLD:
        silence_time += 1 / SILENCE_INCREMENT
    else:
        silence_time = 0

    # stop recording if minimum silence time has been reached
    if silence_time > SILENCE_TIME:
        break

# stop the audio stream and close the audio device
stream.stop_stream()
stream.close()
audio.terminate()

# save the recorded audio to a temporary file
filename = generate_filename()
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("Audio saved to temporary file:", filename)


# load the recorded audio from the temporary file
# with open(filename, 'rb') as f:
#     audio_data = f.read()

file = open(filename, "rb")
transcript = openai.Audio.transcribe("whisper-1", file)

# print the transcribed text
text = transcript["text"]
print(f"User: {text}")

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "Et dius Jarvis, ets un robot que treballa al laboratori de Xipsi per al Gerard i el Juan. T'agrada fer bromes i respons de forma sarcàstica."},
        {"role": "user", "content": text},
    ]
)
print(f'Bot: {response["choices"][0]["message"]["content"]}')

