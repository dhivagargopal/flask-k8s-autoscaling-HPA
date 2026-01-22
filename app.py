from flask import Flask
import time
import os

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello from pod {os.getenv('HOSTNAME')}"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/cpu")
def cpu():
    end = time.time() + 10
    while time.time() < end:
        pass
    return "CPU load generated!"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
