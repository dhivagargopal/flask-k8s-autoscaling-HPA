from flask import Flask, jsonify
import random
import os

app = Flask(__name__)

@app.route("/")
def home():
    pod_name = os.getenv("HOSTNAME", "data-pod")
    return f"Data generator running in pod {pod_name}"

@app.route("/metrics")
def metrics():
    """Return random metrics"""
    data = {
        "temperature": round(random.uniform(20, 40), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "pressure": round(random.uniform(900, 1100), 2)
    }
    return jsonify(data)

@app.route("/random")
def random_number():
    """Return a random number"""
    return jsonify({"value": random.randint(1, 100)})

if __name__ == "__main__":
    port = int(os.getenv("DATA_PORT", 6000))
    app.run(host="0.0.0.0", port=port)
