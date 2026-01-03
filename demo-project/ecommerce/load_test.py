import requests
import concurrent.futures
import time
import uuid
import json

BASE_URL = "http://localhost:7070/api/orders/sync"
USER_ID = "00000000-0000-0000-0000-000000000001" # Bu ID'nin DB'de olması gerekir
PRODUCT_ID = "00000000-0000-0000-0000-000000000001" # Bu ID'nin DB'de olması gerekir

payload = {
    "userId": USER_ID,
    "items": [
        {
            "productId": PRODUCT_ID,
            "quantity": 1
        }
    ]
}

def send_request(_):
    try:
        start_time = time.time()
        response = requests.post(BASE_URL, json=payload)
        end_time = time.time()
        return response.status_code, end_time - start_time
    except Exception as e:
        return str(e), 0

def run_load_test(request_count, concurrency):
    print(f"Starting load test: {request_count} requests with concurrency {concurrency}")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(send_request, i) for i in range(request_count)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    success_count = sum(1 for status, _ in results if status == 200)
    failed_count = request_count - success_count
    avg_time = sum(t for _, t in results if t > 0) / len(results) if results else 0
    
    print(f"Test Completed.")
    print(f"Success: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Average Response Time: {avg_time:.4f}s")

if __name__ == "__main__":
    # Not: Uygulamanın çalışıyor olması ve USER_ID/PRODUCT_ID'nin DB'de mevcut olması gerekir.
    # run_load_test(100, 10) 
    pass
