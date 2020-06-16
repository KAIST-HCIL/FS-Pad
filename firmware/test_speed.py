import serial
import struct
import numpy as np
import time
port_name = 'COM26'
baud_rate = 115200

def send_map(ser, force_map):
    flat_data = np.array(force_map).flatten().tolist()
    pack_pattern = '<'+'b'*len(flat_data)
    bytes_to_write = struct.pack(pack_pattern, *flat_data)
    bytes_to_write = b'm' + bytes_to_write
    ser.write(bytes_to_write)
    while True:
        recv = ser.read()
        if(recv == b's'):
            break

def send_point(ser, x, y, use_map = 1):
    data = [x, y, use_map]
    pack_pattern = '<'+'i'*len(data)
    bytes_to_write = struct.pack(pack_pattern, *data)
    bytes_to_write = b'p' + bytes_to_write
    ser.write(bytes_to_write)
    while True:
        recv = ser.read()
        if(recv == b's'):
            break

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


def main():
    ser = serial.Serial(port_name, baud_rate, timeout = 1)
    map_size = (16,16)
    num_repeat = 100
    '''
    x_data = np.random.randint(low=-128, high=127, size=map_size)
    y_data = np.random.randint(low=-128, high=127, size=map_size)

    force_map = join_as_map(x_data, y_data)
    '''

    t_start = time.perf_counter()
    for i in range(num_repeat):
        send_point(ser, 0, 0, 0)
        print("sent")
    t_end = time.perf_counter()

    t_per_map = (t_end-t_start) / num_repeat
    print("force map size: ({0},{1})".format(*map_size))
    print("time per sending a single map:{0} ms".format(t_per_map * 1000))

if __name__ =='__main__':
    main()
