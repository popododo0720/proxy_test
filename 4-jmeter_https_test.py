import subprocess
import time
from datetime import datetime
from pathlib import Path

# JMeter 실행 경로
jmeter_path = r"C:\Users\popod\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat"

# 테스트할 동시 접속자 수 목록
concurrent_users = [10000]

# 로그 디렉토리 생성
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_dir = Path(f"C:/test/jmeter_jmx/jmeter_logs_{timestamp}")
log_dir.mkdir(parents=True, exist_ok=True)

print(f"📊 JMeter 테스트 시작: {timestamp}\n")

# 전체 테스트 시작 시간 기록
overall_start_time = time.time()

# 각 JMX 테스트 실행
for users in concurrent_users:
    jmx_file = f"jmeter_jmx/jmeter_https_proxy_test_{users}.jmx"
    log_file = log_dir / f"result_{users}.jtl"

    print(f"🧪 동시 접속자 {users}명 테스트 중...")

    start_time = time.time()  # 개별 테스트 시작 시간 기록

    result = subprocess.run(
        [jmeter_path, "-n", "-t", jmx_file, "-l", str(log_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    end_time = time.time()  # 개별 테스트 종료 시간 기록
    elapsed_time = end_time - start_time  # 테스트 소요 시간 계산

    if result.returncode == 0:
        print(f"✅ 완료: {jmx_file} -> {log_file} (소요 시간: {elapsed_time:.2f}초)")
    else:
        print(f"❌ 실패: {jmx_file}")
        print("stderr:", result.stderr)

    time.sleep(2)

# 전체 테스트 종료 시간 기록
overall_end_time = time.time()
total_elapsed_time = overall_end_time - overall_start_time

print(f"\n🎉 모든 테스트 완료. 총 소요 시간: {total_elapsed_time:.2f}초")
print(f"📂 결과 로그 위치: {log_dir}")