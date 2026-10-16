import time
import requests

# Live URL banne ke baad yahan replace kar dijiyega
BASE_URL = "http://127.0.0.1:8080"  
ENDPOINT = f"{BASE_URL}/api/answer"
PAYLOAD = {"query": "What is the return policy for custom furniture?"}

times = []
print("Running 20 latency benchmark requests...")

for i in range(20):
    start = time.time()
    try:
        res = requests.post(ENDPOINT, json=PAYLOAD)
        elapsed = time.time() - start
        if res.status_code == 200:
            times.append(elapsed)
            print(f"Req {i+1}: {elapsed:.3f}s")
        else:
            print(f"Req {i+1}: Failed with status {res.status_code}")
    except Exception as e:
        print(f"Req {i+1}: Error - {e}")

if times:
    avg_latency = sum(times) / len(times)
    print(f"\nAverage Latency over 20 requests: {avg_latency:.3f} seconds")