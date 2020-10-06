# FS-Pad
![](/images/FSPad_windgodfist.gif)
<br>
**FS-Pad** is a gamepad with a force feedback thumbstick module.
<br>
You can now feel the external force through your hands when your car crashes, when your avatar gets attacked by an enemy, or when you fire a giant bazooka.
<br>
This is an open source project. Anyone can customize, test, and play with these tiny modules.

[Paper] [Citation format]
> To be added.

## FS Module
![](/images/assembly_stopmotion.gif)
<br>
Force feedback thumbstick module. The core of the FS-Pad.
<br>
**[Assembly guide](/Assembly%20guide.md)**

## Circuitry
<img src="/images/schematic.jpg" width="500" alt="schematic.jpg">

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
