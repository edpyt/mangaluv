# inspired by https://github.com/sparckles/Robyn/blob/ffb7ebc1e9abfc7767649985a2edb6ca81b2e87f/integration_tests/conftest.py
import socket
import time
from concurrent.futures import Future


def check_server_startup(
    future: Future[None],
    domain: str,
    port: int,
) -> Future[None]:
    timeout = 15
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > timeout:
            future.cancel()
            raise ConnectionError("Could not reach Robyn server")
        try:
            sock = socket.create_connection((domain, port), timeout=2)
            sock.close()
            break
        except Exception:
            time.sleep(0.5)
    time.sleep(1)
    return future
