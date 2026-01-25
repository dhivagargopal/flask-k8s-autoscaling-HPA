import time
import os
import random

pod_name = os.getenv("HOSTNAME", "worker-pod")

def main():
    print(f"[{pod_name}] Worker started...")
    while True:
        task_id = random.randint(1000, 9999)
        print(f"[{pod_name}] Processing task {task_id}")
        time.sleep(random.randint(2, 5))  # simulate work

if __name__ == "__main__":
    main()
