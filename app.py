from multiprocessing import Process
import os
import app
import worker
import data_generator

def run_app():
    port = int(os.getenv("APP_PORT", 5000))
    app.app.run(host="0.0.0.0", port=port)

def run_worker():
    worker.main()

def run_data_generator():
    port = int(os.getenv("DATA_PORT", 6000))
    data_generator.app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Create separate processes for each service
    p1 = Process(target=run_app)
    p2 = Process(target=run_worker)
    p3 = Process(target=run_data_generator)

    p1.start()
    p2.start()
    p3.start()

    # Wait for all processes to finish (they won’t, services run indefinitely)
    p1.join()
    p2.join()
    p3.join()
