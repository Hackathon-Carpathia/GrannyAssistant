#!/usr/bin/env python3

import subprocess
import sys
import json
import requests

from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 48000
API_URL = "https://halina.wmlynik.ovh/api/user_request"

SetLogLevel(0)

model = Model(lang="pl")
rec = KaldiRecognizer(model, SAMPLE_RATE)
partial_last = ""
partials = []
user_id = int(sys.argv[1])

# Works only with PulseAudio and uses the default microphone
with subprocess.Popen([
    "ffmpeg", "-loglevel", "quiet", "-f", "pulse", "-i", "default",
    "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"
], stdout=subprocess.PIPE) as process:

    while True:
        data = process.stdout.read(1000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result())["text"]
            if text == "":
                continue
            payload = {
                "user_id": user_id,
                "question": text
            }
            try:
                print(payload)
                requests.post(API_URL, data=json.dumps(payload, ensure_ascii=False), timeout=2)
            except requests.RequestException as e:
                print(f"Failed to send POST request: {e}", file=sys.stderr)
            partials = []
        elif rec.PartialResult() != partial_last:
            partial_last = rec.PartialResult()
            partial = json.loads(partial_last)
            if partial["partial"] == "":
                continue
            partials.append(partial["partial"])

