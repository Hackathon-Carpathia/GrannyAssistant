#!/usr/bin/env python3

import subprocess
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 48000

SetLogLevel(0)

model = Model(lang="pl")
rec = KaldiRecognizer(model, SAMPLE_RATE)
partial_last = ""

# works only with pulseaudio for now and uses default microphone
with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-f", "pulse", "-i",
                            "default",
                            "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                            stdout=subprocess.PIPE) as process:

    while True:
        data = process.stdout.read(1000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        elif rec.PartialResult() != partial_last:
            partial_last = rec.PartialResult()
            print(rec.PartialResult())

    print(rec.FinalResult())
