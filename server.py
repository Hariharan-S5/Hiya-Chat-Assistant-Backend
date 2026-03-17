import subprocess
import threading
import time
import requests

OLLAMA_EXE = r"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "phi3"


def is_ollama_running():
    try:
        requests.get("http://127.0.0.1:11434")
        return True
    except:
        return False


def start_ollama():
    if is_ollama_running():
        print("Ollama already running.")
        return

    def _run():
        print("Starting Ollama server...")

        process = subprocess.Popen(
            [OLLAMA_EXE, "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        for line in process.stdout:
            print(line, end="")

    threading.Thread(target=_run, daemon=True).start()


start_ollama()

time.sleep(5)

try:
    subprocess.run([OLLAMA_EXE, "pull", MODEL_NAME], check=True)
    print(f"Model '{MODEL_NAME}' is ready.")
except Exception as e:
    print("Failed to pull model:", e)

while True:
    time.sleep(1)