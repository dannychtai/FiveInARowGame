import socket
import threading
from _thread import *
import sys
from game import FiveInARow
import pickle

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

games = [FiveInARow(),FiveInARow()]

def threaded_client(conn, player):
    conn.send(pickle.dumps.games[FiveInARow])
    reply = ""
    while True:
        try:
            # Nhận dữ liệu từ client
            data = pickle.loads(conn.recv(2048))
            games[FiveInARow] = data

            if not data:
                print("Disconnected!")
                break 
            else:
                if FiveInARow == 1:
                    reply = games[0]
                else:
                    reply = games[1]

                print("Recieved: ", data)
                print("Sending: ", reply)
            
            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("lost connection!!")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = server.accept()
    print("conected to:", addr)

    # Bắt đầu một thread mới cho client mới kết nối
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1




