import subprocess
import time
from datetime import datetime
from pathlib import Path

# JMeter 실행 경로
jmeter_path = r"C:\Users\popod\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat"

# 테스트할 동시 접속자 수 목록
concurrent_users = [50, 100, 200, 500]

# 로그 디렉토리 생성
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_dir = Path(f"C:/test/jmeter_jmx/jmeter_logs_{timestamp}")
log_dir.mkdir(parents=True, exist_ok=True)

print(f"📊 JMeter 테스트 시작: {timestamp}\n")

# 각 JMX 테스트 실행
for users in concurrent_users:
    jmx_file = f"jmeter_jmx/jmeter_https_proxy_test_{users}.jmx"
    log_file = log_dir / f"result_{users}.jtl"

    print(f"🧪 동시 접속자 {users}명 테스트 중...")

    result = subprocess.run(
        [jmeter_path, "-n", "-t", jmx_file, "-l", str(log_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode == 0:
        print(f"✅ 완료: {jmx_file} -> {log_file}")
    else:
        print(f"❌ 실패: {jmx_file}")
        print("stderr:", result.stderr)

    time.sleep(2)

print(f"\n🎉 모든 테스트 완료. 결과 로그 위치: {log_dir}")
