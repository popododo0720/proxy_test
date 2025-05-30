import subprocess
import time
from datetime import datetime

# 프록시 서버 주소 및 테스트 설정
proxy = "192.168.0.40:50000"
concurrent_list = [50, 100, 200, 500]
requests = 1000
ab_path = r"C:\Users\popod\Downloads\httpd-2.4.63-250207-win64-VS17\Apache24\bin\ab.exe"
target_url = "http://httpbin.org/get"

print(f"Apache Bench 프록시 부하 테스트 시작: {datetime.now()}")

for c in concurrent_list:
    print(f"\n====== HTTP 테스트: {c} 동시 요청, {requests} 총 요청 ======")
    try:
        result = subprocess.run(
            [ab_path, "-X", proxy, "-n", str(requests), "-c", str(c), target_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        print(result.stdout)
        if result.stderr:
            print("에러 메시지:", result.stderr)
    except subprocess.TimeoutExpired:
        print(f"⚠️ 요청이 타임아웃되었습니다: 동시 {c} 요청")
    time.sleep(2)

print(f"\nApache Bench 프록시 부하 테스트 완료: {datetime.now()}")
