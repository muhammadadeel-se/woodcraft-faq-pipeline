import time
import requests

BASE_URL = "http://127.0.0.1:8080"
ENDPOINT = f"{BASE_URL}/api/answer"

def run_benchmark(num_requests=20):
    print(f"Running benchmark against {ENDPOINT}...")
    latencies = []
    payload = {"query": "What types of wood are used in your furniture products?"}
    
    for i in range(num_requests):
        start_time = time.time()
        try:
            response = requests.post(ENDPOINT, json=payload, timeout=5)
            elapsed = time.time() - start_time
            if response.status_code == 200:
                latencies.append(elapsed)
                print(f"Request {i+1}: {elapsed:.3f}s")
            else:
                print(f"Request {i+1}: Failed with status {response.status_code}")
        except Exception as e:
            print(f"Request {i+1}: Error connecting to server ({e})")

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print("----------------------------------------")
        print(f"Average Latency: {avg_latency:.3f}s")
        if avg_latency < 2.0:
            print("BENCHMARK PASSED (< 2s)")
        else:
            print("BENCHMARK FAILED (>= 2s)")
    else:
        print("No successful requests. Is your Flask app running on port 8080?")

if __name__ == "__main__":
    run_benchmark()