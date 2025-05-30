import subprocess
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 프록시 서버 정보
PROXY_HOST = "192.168.0.40"
PROXY_PORT = "50000"

# 테스트 파일 정보
TEST_FILE_URL = "http://ipv4.download.thinkbroadband.com/100MB.zip"
FILE_NAME = "100MB_http.zip"
FILE_SIZE_MB = 100

# 동시 다운로드 수
concurrent_counts = [4, 10]

def download_file(proxy_host, proxy_port, url, output_path):
    try:
        proxy = f"{proxy_host}:{proxy_port}"
        result = subprocess.run(
            ["curl", "-x", proxy, "-k", "-o", output_path, "-s", url],
            capture_output=True
        )
        if os.path.exists(output_path):
            size = round(os.path.getsize(output_path) / (1024 * 1024), 2)
            return True, size
        return False, 0
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False, 0

# 단일 다운로드 테스트
print(f"\n🌐 단일 HTTP 다운로드 시작: {TEST_FILE_URL}")
success, size = download_file(PROXY_HOST, PROXY_PORT, TEST_FILE_URL, FILE_NAME)
if success:
    print(f"✅ 다운로드 성공: {FILE_NAME} ({size} MB)")
else:
    print(f"❌ 다운로드 실패: {FILE_NAME}")

# 동시 다운로드 테스트
for count in concurrent_counts:
    print(f"\n🔁 {count} 개 동시 HTTP 다운로드 테스트 시작")
    start = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=count) as executor:
        futures = [
            executor.submit(download_file, PROXY_HOST, PROXY_PORT, TEST_FILE_URL, f"{FILE_NAME}_{i}.tmp")
            for i in range(count)
        ]
        for future in as_completed(futures):
            results.append(future.result())

    duration = round(time.time() - start, 2)
    success_count = sum(1 for r in results if r[0])
    total_downloaded = sum(r[1] for r in results)

    print(f"📥 성공 다운로드: {success_count}/{count}")
    print(f"⏱️ 총 소요 시간: {duration}초")
    if duration > 0:
        print(f"📊 평균 처리량: {round(total_downloaded / duration, 2)} MB/s")

    # 임시 파일 정리
    for i in range(count):
        try:
            os.remove(f"{FILE_NAME}_{i}.tmp")
        except:
            pass

# 단일 다운로드 파일 정리
try:
    os.remove(FILE_NAME)
except:
    pass

print("\n✅ HTTP 다운로드 테스트 완료")
