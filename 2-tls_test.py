import requests
import concurrent.futures
import time
from datetime import datetime
import urllib3
import warnings

# 인증서 경고 숨기기
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

PROXY_HOST = "192.168.0.40"
PROXY_PORT = "50000"

proxies = {
    "http": f"http://{PROXY_HOST}:{PROXY_PORT}",
    "https": f"http://{PROXY_HOST}:{PROXY_PORT}"
}

sites = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.facebook.com",
    "https://www.amazon.com",
    "https://www.cloudflare.com"
]

def fetch_site(url):
    start = time.time()
    try:
        requests.get(url, proxies=proxies, verify=False, timeout=10)
    except Exception as e:
        return url, None, str(e)
    end = time.time()
    return url, round((end - start) * 1000, 2), None

def run_single_tests():
    print(f"단일 TLS 연결 테스트 시작: {datetime.now()}")
    for site in sites:
        print(f"사이트: {site} 테스트 중...")
        url, duration, error = fetch_site(site)
        if error:
            print(f"오류 발생: {error}")
        else:
            print(f"응답 시간: {duration} ms")
        time.sleep(1)

def run_concurrent_test(concurrency):
    print(f"\n====== {concurrency} 동시 TLS 연결 테스트 ======")
    start = time.time()
    urls = [sites[i % len(sites)] for i in range(concurrency)]
    durations = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(fetch_site, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            _, duration, error = future.result()
            if duration:
                durations.append(duration)
    end = time.time()
    total_duration = round((end - start) * 1000, 2)
    avg_duration = round(total_duration / concurrency, 2)
    print(f"{concurrency} 동시 연결 총 소요 시간: {total_duration} ms")
    print(f"연결당 평균 시간: {avg_duration} ms")
    time.sleep(2)

print(f"TLS 프록시 성능 테스트 시작: {datetime.now()}")
run_single_tests()
for count in [10, 50, 100]:
    run_concurrent_test(count)
print(f"TLS 프록시 성능 테스트 완료: {datetime.now()}")
