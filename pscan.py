import time
import socket
import threading
from queue import Queue
from sys import argv

DEFAULT_TIMEOUT = 3
SUCCESS = 0
HOST = argv[1]
THREADS = int(argv[2])
open_ports = []

start_time = time.time()


def check_port(host, port, timeout=DEFAULT_TIMEOUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    global open_ports

    try:
        connected = sock.connect_ex((host, port)) is SUCCESS
        if connected:
            open_ports.append(port)
        sock.close()
    except Exception as e:
        with threading.Lock():
            print(host, e)
        pass


def threader():
    while True:
        in_worker = q.get()
        check_port(in_worker[0], in_worker[1])
        q.task_done()


q = Queue()

for x in range(THREADS):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for port in range(1, 65535):
    worker = (HOST, port)
    q.put(worker)

q.join()

end_time = time.time() - start_time
print(open_ports)
print(end_time)
