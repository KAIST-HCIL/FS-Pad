import serial
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse
import sys
import math
import datetime as dt
import socket
import threading

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--map-size', type=int,\
        help="Number of grids for the force map.", default=16)
    parser.add_argument('-f', '--force', type=int,\
        help="Max force value to use. Negative of this value is used for min force value.", required=True)
    parser.add_argument('-q', '--frequency', type=int,\
        help="Frequency of a sinusoidal movement.", required=True)
    parser.add_argument('-p', '--port', type=str, default='COM26',\
        help="USB port name.")
    parser.add_argument('-a', '--tcp-address', type=str, default='127.0.0.1',\
        help="Address of TCP sender.")
    parser.add_argument('-b', '--baud-rate', type=int, default=115200,\
        help="Baudrate of USB.")
    parser.add_argument('--debug', action='store_true',\
        help="Print output of Teensy")
    parser.add_argument('--test-point', action='store_true',\
        help="Test force ponit sending")

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(-1)

    return parser.parse_args()

def join_as_map(x_data, y_data):
    X = np.expand_dims(np.array(x_data), axis = 2)
    Y = np.expand_dims(np.array(y_data), axis = 2)
    F = np.concatenate((X,Y), axis = 2)
    """
        format of F:

        F[0] = X[0,0]
        F[1] = Y[0,0]
        F[2] = X[0,1]
        F[3] = Y[0,1]
        .
        .
        .
        F[2*(i*n + j)] = X[i,j]
        F[2*(i*n + j)+1] = Y[i,j]
    """
    return F

def send_map(ser, force_map):
    flat_data = np.array(force_map, dtype=np.int8).flatten().tolist()
    pack_pattern = '<'+'b'*len(flat_data)
    bytes_to_write = struct.pack(pack_pattern, *flat_data)
    bytes_to_write = b'm' + bytes_to_write
    ser.write(bytes_to_write)

def create_control_map(center_x, center_y, force, n_grid):
    x = np.zeros(n_grid)
    y = np.zeros(n_grid)
    xv, yv = np.meshgrid(x, y)

    for i in range(n_grid):
        for j in range(n_grid):
            dist_x = center_y - i
            dist_y = center_x - j
            dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

            if abs(dist_x) < 1 and abs(dist_y) < 1:
                xv[i, j] = force * dist_y / dist * dist_x ** 2
                yv[i, j] = force * dist_x / dist * dist_y ** 2
            else:
                xv[i, j] = force * dist_y / dist
                yv[i, j] = force * dist_x / dist

    xv.astype(int)
    yv.astype(int)

    return xv, yv

def plot_map(xv, yv, n_grid):
    max_pwm = 30
    X, Y = np.meshgrid(np.arange(0, n_grid, 1), np.arange(0, n_grid, 1))
    fig = plt.figure("Forcemap viewer", figsize=(5,5))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_facecolor('grey')
    M = np.hypot(xv, yv)
    if(np.max(np.abs(xv)) == 0 and np.max(np.abs(yv)) == 0):
        ax1.clear()
    else:
        ax1.clear()
        Q = ax1.quiver(X, Y, xv, yv, M, scale=max_pwm, scale_units='xy')
    ax1.scatter(X, Y, color='k', s=1)
    circle = plt.Circle((7.5, 7.5), 8, color='r', fill=False)
    ax1.add_artist(circle)

    plt.show()

def send_control_map(center_x, center_y, max_force, map_size, ser):
    rowv, colv = create_control_map(center_x, center_y, max_force, map_size)
    force_map = join_as_map(colv, rowv)
    send_map(ser, force_map)

str_log = ""
log_on = False
conn_on = False
lock = threading.Lock()

def log_handler(tcp_socket, client_addr):
    print("Connected with ", client_addr)
    global conn_on, log_on, str_log, start_time
    sof_double = 8
    nof_data = 1

    while True:
        lock.acquire()
        try:
            if not conn_on:
                print("connection break")
                tcp_socket.close()
                break
        finally:
            lock.release()

        data = tcp_socket.recv(sof_double * nof_data)

        if not data:
            continue

        lock.acquire()
        try:
            if log_on and start_time is not None:
                curr_time = (dt.datetime.now() - start_time).microseconds
                str_data = str(struct.unpack(str(nof_data) + 'd', data)[0] / 1e6)
                str_log += str(curr_time) + ',' + str_data + '\n'
            elif log_on and start_time is None:
                print("ERROR: start_time not synced")
        finally:
            lock.release()

        tcp_socket.sendall(data)


def main(args):
    global conn_on, log_on, str_log, start_time
    map_size = args.map_size
    min_force = -args.force
    max_force = args.force
    freq = args.frequency
    start_time = None

    # Open serial port and send inital position
    ser = serial.Serial(args.port, args.baud_rate, timeout = 1)
    send_control_map(7.5, 7.5, max_force, map_size, ser)

    # TCP server
    print("socket setting: " + args.tcp_address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_address = (args.tcp_address, 9998)
    sock.bind(recv_address)

    print("socket listen")
    sock.listen()

    print("Accept")
    conn, addr = sock.accept()
    lock.acquire()
    try:
        conn_on = True
    finally:
        lock.release()
    log_t = threading.Thread(target=log_handler, args=(conn, addr))
    log_t.daemon = True
    log_t.start()

    print("Count down: 2")
    time.sleep(1)
    print("Count down: 1")
    time.sleep(1)
    print("START")

    lock.acquire()
    try:
        start_time = dt.datetime.now()
    finally:
        lock.release()
    tmp_time = start_time
    log_on = True

    print("Position control signal start")

    while True:
        elapsed_time = (dt.datetime.now() - tmp_time).microseconds
        total_time = dt.datetime.now() - start_time
        if elapsed_time > 2000:
            y_position = (np.sin(2 * math.pi * freq * total_time.microseconds / 1e6) + 1) * (map_size - 1) / 2
            send_control_map(7.5, y_position, max_force, map_size, ser)
            tmp_time = dt.datetime.now()
        if total_time.seconds >= 2:
            send_control_map(7.5, 7.5, 0, map_size, ser)
            break

    print("Position control finished")

    lock.acquire()
    try:
        conn_on = False
        log_on = False
        print("log write")
        f = open("Freq_" + str(freq) + ".csv", 'w')
        f.write(str_log)
        f.close()
    finally:
        lock.release()

    print(str_log)

    sock.close()
    ser.close()


if __name__ =='__main__':
    args = parse_args()
    main(args)
