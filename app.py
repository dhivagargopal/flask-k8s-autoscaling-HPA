from flask import Flask
import time
import os

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello from pod {os.getenv('HOSTNAME', 'unknown')}"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/cpu")
def cpu():
    """Generate CPU load for 10 seconds"""
    end = time.time() + 10
    while time.time() < end:
        pass
    return "CPU load generated!"

@app.route("/counter", methods=["GET", "POST"])
def count():
    """Simple in-memory counter"""
    from flask import request, jsonify
    global counter
    try:
        counter
    except NameError:
        counter = 0
    if request.method == "POST":
        increment = request.json.get("increment", 1)
        counter += increment
    return jsonify({"counter": counter})

@app.route("/random")
def random_number():
    import random
    return {"random": random.randint(1, 100)}

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
