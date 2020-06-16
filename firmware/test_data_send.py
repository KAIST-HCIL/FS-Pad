import serial
import struct
import numpy as np
port_name = '/dev/ttyACM0'
baud_rate = 9600

x_data = [\
    [1,2,3],\
    [4,5,6],\
    [7,8,9]
]

y_data = [\
    [-10,-20,-30],\
    [-40,-50,-60],\
    [-70,-80,-90]
]

def send_map(ser, force_map):
    flat_data = np.array(force_map).flatten().tolist()
    pack_pattern = '<'+'i'*len(flat_data)
    print(pack_pattern)
    bytes_to_write = struct.pack(pack_pattern, *flat_data)
    print(bytes_to_write)
    ser.write(bytes_to_write)
    while True:
        recv = ser.readline()
        print(recv)
    ser.close()

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

    force_map = join_as_map(x_data, y_data)
    send_map(ser, force_map)

if __name__ =='__main__':
    main()
