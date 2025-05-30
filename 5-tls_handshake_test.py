import ssl
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

PROXY_HOST = "192.168.0.40"
PROXY_PORT = 50000
TARGET_HOST = "www.google.com"
TARGET_PORT = 443
connections = [10, 50, 100, 200]

def create_ssl_context_with_ca(ca_cert_path):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=ca_cert_path)
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    return context

def perform_tls_handshake_via_proxy(context):
    try:
        sock = socket.create_connection((PROXY_HOST, PROXY_PORT), timeout=5)
        connect_req = f"CONNECT {TARGET_HOST}:{TARGET_PORT} HTTP/1.1\r\nHost: {TARGET_HOST}\r\n\r\n"
        sock.sendall(connect_req.encode())
        resp = sock.recv(4096)
        if b"200 Connection Established" not in resp:
            raise Exception("프록시 CONNECT 실패: " + resp.decode(errors='ignore'))

        ssl_sock = context.wrap_socket(sock, server_hostname=TARGET_HOST)
        ssl_sock.getpeercert()
        ssl_sock.close()
        return True
    except Exception as e:
        print("오류 발생:", e)
        return False

if __name__ == "__main__":
    ca_cert_path = os.path.join(os.path.dirname(__file__), "ca_cert.pem")  # PEM 형식 CA 인증서
    ssl_context = create_ssl_context_with_ca(ca_cert_path)

    print(f"🔒 TLS 핸드셰이크 성능 테스트 시작: {datetime.now()}\n")

    for count in connections:
        print(f"====== {count} TLS 핸드셰이크 테스트 ======")
        start = time.time()
        success = 0

        with ThreadPoolExecutor(max_workers=count) as executor:
            futures = [executor.submit(perform_tls_handshake_via_proxy, ssl_context) for _ in range(count)]
            for future in as_completed(futures):
                if future.result():
                    success += 1

        duration = time.time() - start
        print(f"✅ 완료: {success}/{count} 성공")
        print(f"⏱️ 총 소요 시간: {duration:.2f}초")
        print(f"📊 평균 핸드셰이크 시간: {(duration / count):.3f}초\n")
        time.sleep(2)

    print(f"🎉 TLS 핸드셰이크 성능 테스트 완료: {datetime.now()}")
