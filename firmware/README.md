# FS-Pad Teensy 3.6 firmware

## Upload the firmware
Upload the firmware to your Teensy through [Teensyduino](https://www.pjrc.com/teensy/td_download.html).

## Calibrating position
Once you set up the hardware, you should update the potentiometer range in the firmware.
- In *firmware.ino*, set *debugMode* as *DEBUG_STICK*
- Open Arduino's Serial monitor.
- Check the raw potentiometer values (0~1023). Record the min/max values of X/Y axes inside your HW configuration's workspace.
- In *firmware.ino*, modify the parameters: *minX, maxX, minY, maxY*.

## Map Test

The map test code [test_forcemaps.py](test_forcemaps.py) can make various kinds of force maps. It shows visualization of a force map and sends it to the Teensy board.

### Quick Start
Below is an example of simulating a spring thumbstick on the FS-Pad.

Be sure to use your port number instead of COM26.

Windows:
```console
$ python -m venv venv
$ venv\Scripts\activate
(venv) $ python -m pip install -r requirements.txt
(venv) $ python .\test_forcemaps.py -f 60 -t spring -p COM26
```
Output:
![](/images/test_example.jpg)

You can directly setup your environment instead of using [venv](https://docs.python.org/3/tutorial/venv.html).

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

## Troubleshooting
### Out of RAM
```shell
/home/keunwoo/arduino-1.8.9/arduino-1.8.9/hardware/tools/arm/bin/../lib/gcc/arm-none-eabi/5.4.1/../../../../arm-none-eabi/bin/ld: /tmp/arduino_build_569459/firmware.ino.elf section `.bss' will not fit in region `RAM'
/home/keunwoo/arduino-1.8.9/arduino-1.8.9/hardware/tools/arm/bin/../lib/gcc/arm-none-eabi/5.4.1/../../../../arm-none-eabi/bin/ld: region `RAM' overflowed by 4208 bytes
collect2: error: ld returned 1 exit status
Error compiling for board Teensy 3.6.
```
If you see this kind of error, assign global arrays to *static* ([ref])(https://forum.pjrc.com/archive/index.php/t-24449.html).
