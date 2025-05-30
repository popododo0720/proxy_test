import subprocess
import time
from datetime import datetime, timedelta

# 💡 설정: 총 테스트 실행 시간 (시간 단위)
TEST_DURATION_HOURS = 2

# 테스트할 스크립트 목록
scripts = [
    "1-basic_test.py",
    "2-tls_test.py",
    "3-ab_proxy_test_http.py",
    "4-jmeter_https_test.py",
    "5-tls_handshake_test.py",
    "6-http_large_tranfer_test.py",
    "7-https_large_transfer_test.py"
]

# 총 실행 시간 계산
total_seconds = TEST_DURATION_HOURS * 60 * 60
interval_seconds = total_seconds // len(scripts)

start_time = datetime.now()
end_time = start_time + timedelta(seconds=total_seconds)

log = []

print(f"🟢 장기 안정성 테스트 시작: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"총 실행 시간: {TEST_DURATION_HOURS}시간\n")

# 전체 실행 루프
while datetime.now() < end_time:
    for script in scripts:
        current_time = datetime.now()
        if current_time >= end_time:
            break

        print(f"▶ {current_time.strftime('%H:%M:%S')} - {script} 실행 중...")

        try:
            result = subprocess.run(["python", script], capture_output=True, text=True, timeout=300)
            output = result.stdout.strip().splitlines()[-5:] if result.stdout else ["(출력 없음)"]
            status = "성공" if result.returncode == 0 else "실패"
        except Exception as e:
            output = [f"예외 발생: {str(e)}"]
            status = "오류"

        log.append((script, current_time.strftime('%H:%M:%S'), status, output))

        remaining = interval_seconds
        next_time = datetime.now() + timedelta(seconds=remaining)
        print(f"⏳ {remaining}초 대기 후 다음 테스트 (예정: {next_time.strftime('%H:%M:%S')})...\n")
        time.sleep(remaining)

print(f"\n✅ 테스트 종료 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("📋 실행 요약:")

for entry in log:
    script, time_str, status, lines = entry
    print(f"\n🔹 {time_str} - {script} [{status}]")
    for line in lines:
        print("   ", line)
