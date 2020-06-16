import socket
import datetime as dt
import time
import struct

data_size = 8

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9998))

print("Connected to server")
start_time = dt.datetime.now()

while True:
    curr_time = (dt.datetime.now() - start_time).microseconds
    send_data = struct.pack('1d', curr_time)
    print("send_data")
    sock.send(send_data)
    print(send_data)

    recv_data = struct.unpack('1d', sock.recv(data_size))
    print(recv_data)
    time.sleep(0.2)

# connection close
sock.close()
