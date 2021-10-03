import os
import time
import requests
import pyaudio
import wave
import random
import string



class AudioFile:
    def __init__(self, chunk_size=5242880):
        self.filename = self.name_generator()
        self.chunk_size = chunk_size
        self.text = ""
        self.currentPath = ""

    def name_generator(self):
        wav_string = ".mp3"
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        name = random_string + wav_string
        return name

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        try:
            start = time.time()
            duration = time.time() - start
            while duration < 8:
                data = stream.read(1024)
                frames.append(data)
                duration = time.time() - start

        except KeyboardInterrupt:
            pass
        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open(self.filename, "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        self.currentPath = os.getcwd()

    def read_file(self):
        with open(self.filename, 'rb') as _file:
            while True:
                data = _file.read(self.chunk_size)
                if not data:
                    break
                yield data

    def upload_file(self):
        # Upload the file
        headers = {
            'authorization': "b49e38afb25249129772496a98c3dd24"
        }
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                 headers=headers,
                                 data=self.read_file())

        print(response.json()['upload_url'])

        # submit it for transcription
        endpoint = "https://api.assemblyai.com/v2/transcript"

        json = {
            "audio_url": response.json()['upload_url']
        }

        headers = {
            "authorization": "24e34319012441728a1995d41af925c0",
            "content-type": "application/json"
        }

        response = requests.post(endpoint, json=json, headers=headers)
        ids = response.json()["id"]

        transcript_id = f'https://api.assemblyai.com/v2/transcript/{ids}'

        headers = {
            "authorization": "24e34319012441728a1995d41af925c0"
        }

        try:
            response = requests.get(transcript_id, headers=headers)
        except Exception as Exc:
            print(Exc)

        while response.json()['status'] not in ['completed', 'error']:
            response = requests.get(transcript_id, headers=headers)
            time.sleep(2)

        self.text = response.json()['text']
        return self.text

    def removeFile(self):
        os.remove(f"{self.currentPath}/{self.filename}")