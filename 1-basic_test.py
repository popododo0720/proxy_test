import requests
import datetime
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

def test_proxy():
    print(f"기본 프록시 연결 테스트 시작: {datetime.datetime.now()}")

    # HTTP 테스트
    print("HTTP 프록시 테스트 중...")
    try:
        response = requests.get("http://example.com", proxies=proxies, timeout=5)
        print(f"HTTP 응답 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"HTTP 테스트 실패: {e}")

    # # HTTPS 테스트
    # print("HTTPS 프록시 테스트 중...")
    # try:
    #     response = requests.get("https://example.com", proxies=proxies, verify=False, timeout=5)
    #     print(f"HTTPS 응답 상태 코드: {response.status_code}")
    # except Exception as e:
    #     print(f"HTTPS 테스트 실패: {e}")

    print(f"기본 테스트 완료: {datetime.datetime.now()}")

if __name__ == "__main__":
    test_proxy()
