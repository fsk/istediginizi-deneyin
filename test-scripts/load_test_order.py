#!/usr/bin/env python3
"""
Order Create Endpoint Load Test
10,000 concurrent order create request gönderir ve performans metriklerini toplar.
"""

import requests
import time
import uuid
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import statistics

# API Configuration
BASE_URL = "http://localhost:7070"
ORDER_ENDPOINT = f"{BASE_URL}/api/orders/create-order"

# Test Configuration
TOTAL_REQUESTS = 10000
CONCURRENT_WORKERS = 100  # Aynı anda çalışacak thread sayısı


def get_test_data_pools_from_db():
    """Get pools of test data from database for random selection"""
    import psycopg
    import random
    try:
        conn = psycopg.connect(
            host="localhost",
            port=2345,
            dbname="ecommerce",
            user="fsk",
            password="fsk"
        )
        if not conn:
            raise Exception("Failed to connect to database")
        cur = conn.cursor()
        if not cur:
            raise Exception("Failed to create cursor")
        
        # En az 1000 stoklu ürünleri al (load test için yeterli stok)
        cur.execute("SELECT product_id FROM products WHERE stock_quantity >= 1000 ORDER BY stock_quantity DESC")
        product_rows = cur.fetchall()
        if not product_rows:
            # Eğer 1000'den fazla stoklu ürün yoksa, stoklu olanları al
            cur.execute("SELECT product_id FROM products WHERE stock_quantity > 0 ORDER BY stock_quantity DESC LIMIT 1000")
            product_rows = cur.fetchall()
        
        if not product_rows:
            print("No products with stock found in database")
            cur.close()
            conn.close()
            return None, None, None
        
        product_ids = [str(row[0]) for row in product_rows]
        
        # Kullanıcı ID'lerini al
        cur.execute("SELECT user_id FROM users LIMIT 5000")
        user_rows = cur.fetchall()
        if not user_rows:
            print("No users found in database")
            cur.close()
            conn.close()
            return None, None, None
        
        user_ids = [str(row[0]) for row in user_rows]
        
        # Address ID'lerini al
        cur.execute("SELECT address_id FROM addresses LIMIT 5000")
        address_rows = cur.fetchall()
        if not address_rows:
            print("No addresses found in database")
            cur.close()
            conn.close()
            return None, None, None
        
        address_ids = [str(row[0]) for row in address_rows]
        
        cur.close()
        conn.close()
        
        print(f"✅ Test data pools loaded:")
        print(f"   Users: {len(user_ids)}")
        print(f"   Products (with stock): {len(product_ids)}")
        print(f"   Addresses: {len(address_ids)}")
        
        return user_ids, product_ids, address_ids
    except Exception as e:
        print(f"Error getting test data from database: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


def create_order_request(user_ids, product_ids, address_ids):
    """Send an order create request with random data and return the result"""
    import random
    
    # Rastgele seçim yap
    user_id = random.choice(user_ids)
    product_id = random.choice(product_ids)
    shipping_address_id = random.choice(address_ids)
    billing_address_id = random.choice(address_ids)
    
    payload = {
        "userId": user_id,
        "items": [
            {
                "productId": product_id,
                "quantity": 1
            }
        ],
        "notes": "Load test order",
        "shippingAddressId": shipping_address_id,
        "billingAddressId": billing_address_id
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            ORDER_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # milliseconds
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response_time": response_time,
            "error": None if response.status_code == 200 else response.text[:200]
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": 0,
            "response_time": 30000,  # 30 saniye timeout
            "error": "Request timeout"
        }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "status_code": 0,
            "response_time": (end_time - start_time) * 1000,
            "error": str(e)[:200]
        }


def run_load_test(total_requests, concurrent_workers, user_ids, product_ids, address_ids):
    """Run the load test and collect the results"""
    print(f"\n{'='*60}")
    print(f"LOAD TEST STARTING")
    print(f"{'='*60}")
    print(f"Total Requests: {total_requests}")
    print(f"Concurrent Workers: {concurrent_workers}")
    print(f"Endpoint: {ORDER_ENDPOINT}")
    print(f"{'='*60}\n")
    
    results = []
    status_codes = defaultdict(int)
    errors = defaultdict(int)
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
        # Tüm request'leri submit et (her biri rastgele data kullanacak)
        futures = [
            executor.submit(create_order_request, user_ids, product_ids, address_ids)
            for _ in range(total_requests)
        ]
        
        # Sonuçları topla
        completed = 0
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1
            
            status_codes[result["status_code"]] += 1
            if not result["success"]:
                error_key = result["error"][:50] if result["error"] else "Unknown error"
                errors[error_key] += 1
            
            # İlerleme göster
            if completed % 100 == 0:
                print(f"Tamamlanan: {completed}/{total_requests} ({completed*100/total_requests:.1f}%)")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # İstatistikleri hesapla
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    
    response_times = [r["response_time"] for r in successful_requests]
    
    print(f"\n{'='*60}")
    print(f"LOAD TEST RESULTS")
    print(f"{'='*60}")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Total Requests: {len(results)}")
    print(f"Successful Requests: {len(successful_requests)} ({len(successful_requests)*100/len(results):.2f}%)")
    print(f"Failed Requests: {len(failed_requests)} ({len(failed_requests)*100/len(results):.2f}%)")
    
    if response_times:
        print(f"\nResponse Time Statistics (ms):")
        print(f"  Average: {statistics.mean(response_times):.2f} ms")
        print(f"  Median: {statistics.median(response_times):.2f} ms")
        print(f"  Minimum: {min(response_times):.2f} ms")
        print(f"  Maximum: {max(response_times):.2f} ms")
        if len(response_times) > 1:
            print(f"  Standard Deviation: {statistics.stdev(response_times):.2f} ms")
            print(f"  95. Percentile: {sorted(response_times)[int(len(response_times) * 0.95)]:.2f} ms")
            print(f"  99. Percentile: {sorted(response_times)[int(len(response_times) * 0.99)]:.2f} ms")
    
    print(f"\nThroughput: {len(successful_requests)/total_time:.2f} request/second")
    print(f"Successful Throughput: {len(successful_requests)/total_time:.2f} successful request/second")
    
    print(f"\nHTTP Status Codes:")
    for code, count in sorted(status_codes.items()):
        print(f"  {code}: {count} ({count*100/len(results):.2f}%)")
    
    if errors:
        print(f"\nMost Common Errors (Top 10):")
        sorted_errors = sorted(errors.items(), key=lambda x: x[1], reverse=True)[:10]
        for error, count in sorted_errors:
            print(f"  [{count}x] {error}")
    
    print(f"\n{'='*60}")
    
    # Darboğaz analizi
    if len(failed_requests) > 0:
        print(f"\nBOTTLENECK DETECTION:")
        print(f"   Failed request count: {len(failed_requests)}")
        
        timeout_count = sum(1 for r in failed_requests if r.get("error") == "Request timeout")
        if timeout_count > 0:
            print(f"Timeout count: {timeout_count} (Server not responding)")
        
        error_500_count = status_codes.get(500, 0)
        if error_500_count > 0:
            print(f"500 Internal Server Error: {error_500_count} (Server error)")
        
        error_400_count = status_codes.get(400, 0)
        if error_400_count > 0:
            print(f"400 Bad Request: {error_400_count} (Request error)")
        
        if response_times and max(response_times) > 5000:
            print(f"High response times detected (max: {max(response_times):.2f} ms)")
            print(f"This may indicate database or transaction lock issues.")
    
    return results


if __name__ == "__main__":
    print("Getting test data pools from database...")
    user_ids, product_ids, address_ids = get_test_data_pools_from_db()
    
    if not user_ids or not product_ids or not address_ids:
        print("❌ Test data not found in database!")
        print("Please make sure the database is running and the ecommerce database exists.")
        exit(1)
    
    # Load test'i çalıştır
    results = run_load_test(
        TOTAL_REQUESTS,
        CONCURRENT_WORKERS,
        user_ids,
        product_ids,
        address_ids
    )

