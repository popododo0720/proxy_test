import subprocess
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# 프록시 정보
PROXY_HOST = "192.168.0.40"
PROXY_PORT = "50000"

# 테스트할 동시 다운로드 수
concurrent_counts = [5, 10, 20]

# 테스트할 Node.js 파일 정보
node_download_targets = [
    {
        "url": "https://nodejs.org/dist/v18.17.0/node-v18.17.0-win-x64.zip",
        "name": "node-v18.17.0-win-x64.zip"
    }
]

def download_file(proxy_host, proxy_port, url, output_path):
    try:
        proxy = f"{proxy_host}:{proxy_port}"
        start = time.time()
        result = subprocess.run(
            ["curl", "-x", proxy, "-k", "-o", output_path, "-s", url],
            capture_output=True
        )
        end = time.time()

        if os.path.exists(output_path):
            size_mb = round(os.path.getsize(output_path) / (1024 * 1024), 2)
            duration = round(end - start, 2)
            speed = round(size_mb / duration, 2) if duration > 0 else 0
            print(f"✅ 다운로드 완료: {output_path} ({size_mb} MB, {duration}초, {speed} MB/s)")
            return True, size_mb
        else:
            print(f"❌ 다운로드 실패: {url}")
            return False, 0
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False, 0

def node_download_test():
    print(f"\n========== Node.js 다운로드 테스트 시작: {datetime.now()} ==========\n")

    # 단일 다운로드 테스트
    print("===== [단일 다운로드 테스트] =====")
    for target in node_download_targets:
        download_file(PROXY_HOST, PROXY_PORT, target["url"], target["name"])
        time.sleep(2)

    # 병렬 다운로드 테스트
    for target in node_download_targets:
        for count in concurrent_counts:
            print(f"\n===== [{count} 개 동시 다운로드 테스트] ({target['name']}) =====")
            start_time = time.time()

            with ThreadPoolExecutor(max_workers=count) as executor:
                futures = [
                    executor.submit(download_file, PROXY_HOST, PROXY_PORT, target["url"], f"{target['name']}_concurrent_{i+1}.tmp")
                    for i in range(count)
                ]
                results = [f.result() for f in as_completed(futures)]

            end_time = time.time()
            duration = round(end_time - start_time, 2)
            total_success = sum(1 for r in results if r[0])
            total_size = sum(r[1] for r in results)
            avg_speed = round(total_size / duration, 2) if duration > 0 else 0

            print(f"\n📥 성공 다운로드: {total_success}/{count}")
            print(f"⏱️ 총 소요 시간: {duration}초")
            print(f"📊 총 다운로드 크기: {total_size} MB")
            print(f"🚀 예상 총 처리량: {avg_speed} MB/s\n")

            # 임시 파일 정리
            for i in range(count):
                try:
                    os.remove(f"{target['name']}_concurrent_{i+1}.tmp")
                except:
                    pass
            time.sleep(2)

    # 단일 다운로드 파일 정리
    print("\n===== 다운로드 파일 정리 중 =====")
    for target in node_download_targets:
        try:
            os.remove(target["name"])
            print(f"삭제 완료: {target['name']}")
        except:
            pass

    print(f"\n========== Node.js 다운로드 테스트 완료: {datetime.now()} ==========")

if __name__ == "__main__":
    node_download_test()
