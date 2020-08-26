# FS-Pad
![](/temporary/images/FSPad_windgodfist.gif)
FS-Pad is a gamepad with a force feedback thumbstick module. New type of video game interactions are enabled on the FS-Pad since the thumbstick can actively move by itself, block or thrust the player's thumb, and generate millions of passive profiles. For example, the FS-Pad could mimic an automobile's gear lever so that you could seize that feeling of shifting the gear manually for racing games. You could feel the external force through your hands when your car crashes, when your avatar gets attacked by an enemy, or when you fire a giant bazooka. You can even learn how to play the game with the FS-Pad. The FS-Pad will lead your thumb to a desired position at an exact timing.

[Paper] [Citation format]
> To be added.

## FS Module
![](/temporary/images/assembly_stopmotion.gif)
The core of the FS-Pad. The force feedback thumbstick module.
**[Assembly guide](/Assembly guide.md)**

## Circuitry
![](/temporary/images/schematic.jpg)
  - **Components needed**
    + Teensy 3.6
    + 2 * Motor driver (DRV8801 Breakout board) [[Site]](https://www.pololu.com/product/2136/resources)
    + DC power jack
    + Voltage regulator (LM1117)
    + 4 * 10k Ohm resistors
    + 1 mF capacitor
  - **[Schematic](/circuitry/FSPad_sch.sch)** (Created with Autodesk EAGLE)

## Firmware
**[firmware.ino](/firmware/firmware.ino)**
* Upload the firmware through [Teensyduino](https://www.pjrc.com/teensy/td_download.html).
* You could find out some test scripts and explanations in the [firmware directory](/firmware).

## Announcement
We are currently building a bi-manual version of the FS-Pad; including exclusive housing, custom PCB & schematic, and easy-to-follow documentations. If you have any requests or questions, please directly contact us.

youngbo.shim@kaist.ac.kr
