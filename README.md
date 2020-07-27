# FS-Pad
FS-Pad: Video Game Interactions with a Force Feedback Gamepad

[Project video] [Paper] [Citation format]
> To be added.

## Announcement
We are currently building a bi-manual version of the FS-Pad; including exclusive housing, custom PCB & schematic, and easy-to-follow documentations. If you have any requests or questions, please directly contact us.

youngbo.shim@kaist.ac.kr

## FS Module
  - **Components needed**
    + Coreless motors (16DCT Athlonix 219E) [[Site]](https://www.portescap.com/en/products/brush-dc-motors/athlonix-motors/16dct-athlonix-precious-metal-brush-dc-motor)
    + Rotary potentiometers (Took apart from a Xbox One controller's thumbstick module) [[Site]](https://www.aliexpress.com/item/33011575369.html?spm=a2g0s.9042311.0.0.42674c4dC97u9J)
    + Large spur gear (70 teeth, modulus 0.3, diameter 21.45 mm, width 1.2 mm) [[Site]](https://ko.aliexpress.com/item/4000099888614.html?spm=a2g0o.detail.1000014.45.234470a0vl6pO6&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.14976.178076.0&scm_id=1007.14976.178076.0&scm-url=1007.14976.178076.0&pvid=82aaac0b-55b4-41d3-aa16-17b92ed123fd&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.14976.178076.0,pvid:82aaac0b-55b4-41d3-aa16-17b92ed123fd,tpp_buckets:668%230%23131923%2358_668%23808%237756%23631_668%23888%233325%2317_4976%230%23178076%230_4976%232711%237538%23352_4976%233223%2310815%237_4976%233104%239653%235_4976%233141%239887%234_668%232846%238116%23949_668%232717%237561%23318__668%233422%2315392%23468)
    + Small spur gear (11 teeth, modulus 0.3, diameter 3.9 mm, width 2 mm) [[Site]](https://www.aliexpress.com/item/33023736047.html?spm=a2g0o.productlist.0.0.400917d9ZYoi95&algo_pvid=bf7dee53-2d2b-4fe4-aff9-6fe93fa2e007&algo_expid=bf7dee53-2d2b-4fe4-aff9-6fe93fa2e007-22&btsid=0ab6f83115922884623618375e73a7&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_)
    + Shaft M1.5
    + 6 * Bolt M1.6 (2.5 mm)
    + 4 * Bolt M2 (10 mm)
  - **Printable parts**
    + [Module body](https://github.com/YoungboShim/FS-Pad/blob/master/CAD%20files/Module%20body.stl)
    + [X axis guide](https://github.com/YoungboShim/FS-Pad/blob/master/CAD%20files/X%20axis%20guide.stl)
    + [X axis motor mount](https://github.com/YoungboShim/FS-Pad/blob/master/CAD%20files/X%20axis%20motor%20mount.stl)
    + [Y axis guide](https://github.com/YoungboShim/FS-Pad/blob/master/CAD%20files/Y%20axis%20guide.stl)
    + [Y axis motor mount](https://github.com/YoungboShim/FS-Pad/blob/master/CAD%20files/Y%20axis%20motor%20mount.stl)
  - **[CAD file](https://github.com/YoungboShim/FS-Pad/blob/master/CAD%20files/FS%20module%20Xbox%20fit%20v25.f3d)** (Created with Autodesk Fusion 360)
  
## Circuitry
  - **Components needed**
    + Teensy 3.6
    + 2 * Motor driver (DRV8801 Breakout board) [[Site]](https://www.pololu.com/product/2136/resources)
    + DC power jack
    + Voltage regulator (LM1117)
    + 4 * 10k Ohm resistors
    + 1 mF capacitor
  - **[Schematic](https://github.com/YoungboShim/FS-Pad/blob/master/circuitry/FSPad_sch.sch)** (Created with Autodesk EAGLE)
  
## Firmware
**[firmware.ino](https://github.com/YoungboShim/FS-Pad/blob/master/firmware/firmware.ino)**
* Upload the firmware through [Teensyduino](https://www.pjrc.com/teensy/td_download.html).
* You could find out some test scripts and explanations in the [firmware directory](https://github.com/YoungboShim/FS-Pad/tree/master/firmware).
