import socket
import threading
from _thread import *
import sys

# Khởi tạo máy chủ
HOST = "192.168.1.49"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
except socket.error as e:
    str(e)

# Lắng nghe kết nối từ client
server.listen(2)

print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

def threaded_client(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply - data.decode("utf-8")
            if not data:
                print("Disconnected!")
            else:
                print("Recieved: ", reply)
                print("Sending: ", reply)
            conn.sendall(str.encode(reply))
        except:
            break

# Lưu trữ danh sách client
clients = []
lock = threading.Lock()  # Lock để đồng bộ hóa truy cập đến danh sách clients

# Chấp nhận kết nối từ client
client_id = 0
while True:
    conn, addr = server.accept()
    print("conected to:", addr)

    start_new_thread(threaded_client, (conn,))


