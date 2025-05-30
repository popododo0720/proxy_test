import os
import requests
import threading
import time

# 다운로드 설정
PROXY = {
    "http": "http://192.168.0.40:50000",
    "https": "http://192.168.0.40:50000"
}

NODE_URLS = [
    ("https://nodejs.org/dist/v18.17.0/node-v18.17.0-win-x64.zip", "node-v18.17.0.zip"),
]

CONCURRENCY_LEVELS = [5, 10, 20]

success_count = 0
fail_count = 0
lock = threading.Lock()

session = requests.Session()
session.proxies.update(PROXY)
session.verify = False  # SSL 무시

def download_file(url, out_name, retries=3):
    global success_count, fail_count
    for attempt in range(1, retries+1):
        try:
            start = time.time()
            with session.get(url, stream=True, timeout=15) as response:
                response.raise_for_status()

                with open(out_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            duration = time.time() - start
            size_mb = os.path.getsize(out_name) / (1024 * 1024)
            print(f"[{out_name}] 완료 - 크기: {size_mb:.2f}MB, 시간: {duration:.2f}s, 속도: {size_mb/duration:.2f}MB/s")

            with lock:
                success_count += 1
            return  # 성공 시 함수 종료

        except Exception as e:
            print(f"❌ 다운로드 실패 [{out_name}] 시도 {attempt}: {e}")
            time.sleep(1)  # 재시도 전 짧은 대기

    # 재시도 후에도 실패한 경우
    with lock:
        fail_count += 1

def run_concurrent_downloads(url, filename, count):
    global success_count, fail_count
    print(f"\n=== 동시 {count}개 다운로드 테스트 시작 ({filename}) ===")
    threads = []
    success_count = 0
    fail_count = 0
    start_time = time.time()

    for i in range(count):
        name = f"{filename}_thread_{i}.tmp"
        t = threading.Thread(target=download_file, args=(url, name))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    duration = time.time() - start_time
    first_file = f"{filename}_thread_0.tmp"
    if os.path.exists(first_file):
        size_mb = os.path.getsize(first_file) / (1024 * 1024)
        total_size = size_mb * success_count  # 성공 개수만큼 계산
        print(f"총 소요 시간: {duration:.2f}s")
        print(f"성공: {success_count}개, 실패: {fail_count}개")
        print(f"총 처리량: {total_size:.2f}MB / {duration:.2f}s = {total_size/duration:.2f}MB/s")

    # 파일 정리
    for i in range(count):
        try:
            os.remove(f"{filename}_thread_{i}.tmp")
        except:
            pass

# 단일 다운로드 테스트
print("\n===== 단일 다운로드 테스트 =====")
for url, name in NODE_URLS:
    download_file(url, name)
    os.remove(name)

# 병렬 다운로드 테스트
for url, name in NODE_URLS:
    for count in CONCURRENCY_LEVELS:
        run_concurrent_downloads(url, name, count)
