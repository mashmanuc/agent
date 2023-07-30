#!/usr/bin/env python3
import queue
import sounddevice as sd
import vosk
import json
model=vosk.Model('vosk_nano')
q = queue.Queue()
device=sd.default.device
samplerate=int(sd.query_devices(device[0], 'input')['default_samplerate'])

def callback(indata, frames, time, status):
  
    q.put(bytes(indata))


with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device, dtype="int16", channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            data= json.loads(rec.Result())['text']
            print(data)
        # else:
        #     print(rec.PartialResult())
        