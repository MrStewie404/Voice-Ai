# pip install vosk
# pip install pyaudio
# модели для распознавания (маленькая): https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbnZMWW5pOWRVZUJtNXFNcm4tTXhZNnhwVEtnQXxBQ3Jtc0tuRmdaanJaemJBdjZsR1Z0eVhJS3p3YUxBdXNjT1ZLVEl4RzNjemd4RmJYRkljQzVsVVdqYWFGUTZkRjJVcFdhenA3LU53eXI5dERMUzE4cThEc2VaNHc3bmJBd2NpaTZhZ09LWEZ3NUI5cHlteTNlRQ&q=https%3A%2F%2Fvk.com%2Faway.php%3Fto%3Dhttps%253A%252F%252Falphacephei.com%252Fkaldi%252Fmodels%252Fvosk-model-small-ru-0.4.zip%26cc_key%3D&v=XF2WVUVxAGQ
# (большая): https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqblVVVjBwM1dBOFM0M0s1ZGVfMURPUjcyeU1NUXxBQ3Jtc0tsNUt3WnVJMW93aUIyZnRaTjcxN1BSZVdkS3hkMFVDemd2WlJtY0NqM1R2Sk94Vm1EMHRJczVMNTdMZDlKczc1UTc2YUJnVUI0UDdSTThCNUJxSlpYVER0bFZuUHVvUWY4N2gtdzNudVlETXVOZUVTMA&q=https%3A%2F%2Fvk.com%2Faway.php%3Fto%3Dhttp%253A%252F%252Falphacephei.com%252Fkaldi%252Fmodels%252Fvosk-model-ru-0.10.zip%26cc_key%3D&v=XF2WVUVxAGQ

from vosk import Model, KaldiRecognizer
import pyaudio, json
import os
import playsound
import ai
from gtts import gTTS
import pygame
import random


model = Model('small')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data)>0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']

def voice(text):
    tts = gTTS(text=text, lang='ru')
    name_r = random.randint(0,100000000)
    tts.save(f'{name_r}.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load(f'{name_r}.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()

for text in listen():
    text = text + '.'
    os.system('cls')
    print(f'Запрос: {text}')
    text_gen = ai.generate_text(text)
    print(f'Ответ: {text_gen}')
    voice(text_gen)
