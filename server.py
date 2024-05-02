import socket
import threading
from _thread import *
import sys

# Khởi tạo máy chủ
HOST = "192.168.1.50"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
except socket.error as e:
    str(e)

# Lắng nghe kết nối từ client
server.listen(2)

print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

def threaded_client(conn, player):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            # Nhận dữ liệu từ client
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("Disconnected!")
                break 
            else:
                print("Recieved: ", reply)

            # Gửi dữ liệu đến client còn lại
            other_player = 1 if player == 0 else 0
            players[other_player].sendall(str.encode(reply))
        except:
            break

    print("lost connection!!")
    conn.close()

players = [None, None]
player_count = 0

while True:
    conn, addr = server.accept()
    print("conected to:", addr)

    # Gán người chơi cho client
    players[player_count] = conn
    player_count += 1

    # Bắt đầu một thread mới cho client mới kết nối
    start_new_thread(threaded_client, (conn, player_count - 1))





