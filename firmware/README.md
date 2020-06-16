# Fumbstick Teensy 3.6 firmware

## How to use?
Set parameters of *firmware.ino*. Then just upload the code to a Teensy board.
- Size of a force map grid
- Debug mode

## Data format
Every data packet should have a mode indicator byte at the beginning. 'm' is for force map update and 'p' is for force point update.

### Force map
Data should be send as follows. *F* is a list of bytes that contains all data of a force map. *X* is a force map of x direction values and *Y* is for y direction.
Therefore, the size of X and Y is '*# of grid X # of grid*'.
```python
F[0] = X[0,0]
F[1] = Y[0,0]
F[2] = X[0,1]
F[3] = Y[0,1]
.
.
.
F[2*(i*n + j)] = X[i,j]
F[2*(i*n + j)+1] = Y[i,j]
```
The length of F is '*# of grid X # of grid X 2*'. If F is converted to a byte array, the size would be '*# of grid X # of grid X 2 X 4*'. **sizeof(int) == 4 for both Teensy and python**. Teensy reads '*# of grid X # of grid X 2 X 4*' length of bytes when a serial buffer is filled.

If you are not sure how to send data, please see [test_data_send.py](test_data_send.py) or [test_forcemaps.py](test_forcemaps.py).

### Force point
A packet should have the following three values in order.
- force value of x direction
- force value of y direction
- whether to use a saved force map or not (0 = not use, 1 = use)

## Test
### Data send and recv test
Set the firmware to debug mode and Use [test_data_send.py](test_data_send.py). The firmware echoes data sent from the python script

### Speed test
The speed test is done with [test_speed.py](test_speed.py). The firmware sends a success code 's' when it receives whole data and updates the force map. The test code sends a random map and measures until it gets the success code. The code repeats 100 times and calculates an average.

#### Result 1
Ubuntu 16.04

| Size of map   | Time per a map (ms) |
| ------------- | -------------             |
| 8 X 8     | 0.733  |
| 16 X 16   | 3.857 |
| 32 X 32   | 18.084 |
| 64 X 64   | 48.164 |
| 128 X 128   | 177.899 |

### Map Test
The map test code [test_forcemaps.py](test_forcemaps.py) can make various kinds of force maps. It shows visualization of a force map and sends it to a Teensy board.

## Troubleshooting
### Out of RAM
```shell
/home/keunwoo/arduino-1.8.9/arduino-1.8.9/hardware/tools/arm/bin/../lib/gcc/arm-none-eabi/5.4.1/../../../../arm-none-eabi/bin/ld: /tmp/arduino_build_569459/firmware.ino.elf section `.bss' will not fit in region `RAM'
/home/keunwoo/arduino-1.8.9/arduino-1.8.9/hardware/tools/arm/bin/../lib/gcc/arm-none-eabi/5.4.1/../../../../arm-none-eabi/bin/ld: region `RAM' overflowed by 4208 bytes
collect2: error: ld returned 1 exit status
Error compiling for board Teensy 3.6.
```
If you see this kind of error, assign global arrays to *static* ([ref])(https://forum.pjrc.com/archive/index.php/t-24449.html).
