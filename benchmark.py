import time
import requests
import numpy as np

URL = "http://127.0.0.1:5000/api/answer"
QUERIES = [
    "What wood types do you use?",
    "How long does shipping take?",
    "What is the warranty policy?",
    "Can I return custom furniture?",
    "Do you offer international shipping?"
]

def benchmark_api(num_runs=20):
    latencies = []
    print(f"--- Running Performance Benchmark ({num_runs} requests) ---")
    
    for i in range(num_runs):
        query = QUERIES[i % len(QUERIES)]
        start_time = time.perf_counter()
        
        try:
            res = requests.post(URL, json={"question": query})
            elapsed = time.perf_counter() - start_time
            if res.status_code == 200:
                latencies.append(elapsed)
                print(f"Run {i+1:02d}: {elapsed:.4f}s | Status: {res.status_code}")
            else:
                print(f"Run {i+1:02d}: Failed (Status {res.status_code})")
        except Exception as e:
            print(f"Run {i+1:02d}: Request Error - {e}")

    if latencies:
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        print("\n=== Benchmark Results ===")
        print(f"Total Successful Runs: {len(latencies)}/{num_runs}")
        print(f"Average Response Time: {avg_latency:.4f} seconds")
        print(f"95th Percentile (P95): {p95_latency:.4f} seconds")
        assert avg_latency <= 2.0, "Benchmark failed: Average latency exceeds 2.0 seconds!"
        print("✅ Performance Requirement Passed (< 2 seconds)")

if __name__ == "__main__":
    benchmark_api()