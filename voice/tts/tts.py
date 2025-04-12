import subprocess
import asyncio
import websockets
import sys

# Input text
text = "Oczywiście, chętnie Ci pomogę, Basiu! Napisz tylko, z czym dokładnie masz problem. Chodzi o coś technicznego, zdrowotnego, dokumenty, komputer, telefon, czy może coś zupełnie innego? Postaram się wszystko wytłumaczyć spokojnie i krok po kroku."

# Set the Piper model path
model_path = "pl_PL-darkman-medium.onnx"

# Run the pipeline: echo -> piper -> aplay

URI = f"wss://halina.wmlynik.ovh/ws/{sys.argv[1]}"

async def listen():
    async with websockets.connect(URI) as websocket:
        print(f"Connected to {URI}")
        while True:
            try:
                text = await websocket.recv()
                
                piper_process = subprocess.Popen(
                    ['piper', '--model', model_path, '--output-raw'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE
                )

                aplay_process = subprocess.Popen(
                    ['aplay', '-r', '22050', '-f', 'S16_LE', '-t', 'raw'],
                    stdin=piper_process.stdout
                )

                # Send the text to Piper's stdin
                piper_process.stdin.write(text.encode('utf-8'))
                piper_process.stdin.close()

                # Wait for both processes to finish
                aplay_process.wait()
                piper_process.wait()
            except websockets.ConnectionClosed:
                print("Connection closed.")
                break

asyncio.run(listen())
