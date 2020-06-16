import serial
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--map-size', type=int,\
        help="Number of grids for the force map.", required = True)
    parser.add_argument('-f', '--force', type=int,\
        help="Max force value to use. Negative of this value is used for min force value.", required=True)
    parser.add_argument('-t', '--map-type', type=str, choices=['spring','blackwhole','whitehole', 'wall'],\
        help="Choose which force map to use.", required=True)
    parser.add_argument('-p', '--port', type=str, default='COM26',\
        help="USB port name.")
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

def send_map(ser, force_map):
    flat_data = np.array(force_map, dtype=np.int8).flatten().tolist()
    pack_pattern = '<'+'b'*len(flat_data)
    bytes_to_write = struct.pack(pack_pattern, *flat_data)
    bytes_to_write = b'm' + bytes_to_write
    ser.write(bytes_to_write)


def send_point(ser, x, y, use_map = 1):
    data = [x, y, use_map]
    pack_pattern = '<'+'b'*len(data)
    bytes_to_write = struct.pack(pack_pattern, *data)
    bytes_to_write = b'p' + bytes_to_write
    ser.write(bytes_to_write)
    """
    while True:
        recv = ser.read()
        if(recv == b's'):
            break
    """

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

def create_map(map_type, min_val, max_val, n_grid):
    if map_type == "spring":
        return create_spring_map(min_val, max_val, n_grid)
    if map_type == "blackwhole":
        return create_blackwhole_map(min_val, max_val, n_grid)
    if map_type == "whitehole":
        return create_whtewhole_map(min_val, max_val, n_grid)
    if map_type == "wall":
        return create_wall_map(min_val, max_val, n_grid)


def create_spring_map(min_val, max_val, n_grid):
    # range of x and y should be 0 to 1
    x = np.linspace(1, 0, n_grid)
    y = np.linspace(1, 0, n_grid)
    xv, yv = np.meshgrid(x, y)

    xv = xv * (max_val - min_val) + min_val
    yv = yv * (max_val - min_val) + min_val
    xv.astype(int)
    yv.astype(int)

    return xv, yv

def create_blackwhole_map(min_val, max_val, n_grid):

    dist = np.linspace(-1, 1, n_grid)
    x = -dist**3
    y = -dist**3
    xv, yv = np.meshgrid(x, y)

    xv = xv * (max_val)
    yv = yv * (max_val)
    xv.astype(int)
    yv.astype(int)

    return xv, yv

def create_whtewhole_map(min_val, max_val, n_grid):

    dist = np.linspace(-1, 1, n_grid)
    x = dist**3
    y = dist**3
    xv, yv = np.meshgrid(x, y)

    xv = xv * (max_val)
    yv = yv * (max_val)
    xv.astype(int)
    yv.astype(int)

    return xv, yv

def create_wall_map(min_val, max_val, n_grid):

    # range of x and y should be 0 to 1
    x = np.zeros(n_grid)
    x[:int(n_grid / 2)] = [max_val] * int(n_grid / 2)
    y = np.zeros(n_grid)

    xv, yv = np.meshgrid(x, y)

    xv.astype(int)
    yv.astype(int)

    return xv, yv

def show(xv, yv):

    plt.subplot(121)
    plt.imshow(xv)
    plt.title("x force")
    plt.colorbar()
    plt.subplot(122)
    plt.imshow(yv)
    plt.title("y force")
    plt.colorbar()

    print("Close window to send the data")
    plt.show()


def main(args):
    map_size = args.map_size
    min_force = -args.force
    max_force = args.force
    rowv, colv = create_map(args.map_type, min_force, max_force, map_size)
    print(rowv.shape, colv.shape)
    show(rowv, colv)

    # for the force map, meshgrid should be flpped
    fx = colv
    fy = rowv

    force_map = join_as_map(fx, fy)
    ser = serial.Serial(args.port, args.baud_rate, timeout = 1)
    send_map(ser, force_map)

    send_point_toggle = True
    use_map = 1
    while True:
        #time.sleep(0.1)
        if args.test_point:
            if not args.debug:
                time.sleep(0.1)
            if send_point_toggle:
                send_point(ser, int(max_force / 2), int(max_force / 2), use_map = use_map)
                send_point_toggle = False
            else:
                send_point(ser, 0, 0, use_map = use_map)
                send_point_toggle = True

        if args.debug:
            recv = ser.readline()
            if recv:
                print(recv)

        if not args.debug and not args.test_point:
            break

    ser.close()

if __name__ =='__main__':
    args = parse_args()
    main(args)
