# FS module assembly guide
## Preparation
![](/images/components.jpg)
- **Components needed**<br>
Modifying the components will require you to directly modify the CAD files to fit the 3D printable parts.
  + 2 * Coreless motor (16DCT Athlonix 219E) [[Site]](https://www.portescap.com/en/products/brush-dc-motors/athlonix-motors/16dct-athlonix-precious-metal-brush-dc-motor)
  + 2 * Rotary potentiometer (Took apart from a Xbox One controller's thumbstick module)
  + 2 * Large spur gear (70 teeth, modulus 0.3, diameter 21.45 mm, width 1.2 mm) [[Site]](https://ko.aliexpress.com/item/4000099888614.html?spm=a2g0o.detail.1000014.45.234470a0vl6pO6&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.14976.178076.0&scm_id=1007.14976.178076.0&scm-url=1007.14976.178076.0&pvid=82aaac0b-55b4-41d3-aa16-17b92ed123fd&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.14976.178076.0,pvid:82aaac0b-55b4-41d3-aa16-17b92ed123fd,tpp_buckets:668%230%23131923%2358_668%23808%237756%23631_668%23888%233325%2317_4976%230%23178076%230_4976%232711%237538%23352_4976%233223%2310815%237_4976%233104%239653%235_4976%233141%239887%234_668%232846%238116%23949_668%232717%237561%23318__668%233422%2315392%23468)
  + 2 * Small spur gear (11 teeth, modulus 0.3, diameter 3.9 mm, width 2 mm) [[Site]](https://www.aliexpress.com/item/33023736047.html?spm=a2g0o.productlist.0.0.400917d9ZYoi95&algo_pvid=bf7dee53-2d2b-4fe4-aff9-6fe93fa2e007&algo_expid=bf7dee53-2d2b-4fe4-aff9-6fe93fa2e007-22&btsid=0ab6f83115922884623618375e73a7&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_)
  + 2 * Shaft M1.5
  + 2 * Shaft holder M1.5
  + 6 * Bolt M1.6 (2.5 mm)
  + 4 * Bolt M2 (10 mm)

<br>

- **Printable parts**<br>
We used a SLA 3D printer ([Form 3](https://formlabs.com/3d-printers/form-3/)). Parts are printed with Tough resin (which is deprecated now by Formlabs) at 0.05 mm resolution. If you use different 3D printers with different settings, you may need some modifications on the CAD file to make a perfect fit for the assembly. Intensive stress is applied to these parts during actuation, so we recommend to use the most durable engineering material for your 3D printer. You could either directly use the .stl files below or export models into printable formats from the Fusion 360 file.
  + [Module body](/CAD%20files/Module%20body.stl)
  + [X axis guide](/CAD%20files/X%20axis%20guide.stl)
  + [X axis motor mount](/CAD%20files/X%20axis%20motor%20mount.stl)
  + [Y axis guide](/CAD%20files/Y%20axis%20guide.stl)
  + [Y axis motor mount](/CAD%20files/Y%20axis%20motor%20mount.stl)
  + **[CAD file](/CAD%20files/FS%20Module.f3d)** (Created with Autodesk Fusion 360)

<br>

- **Stick - laser cut**<br>
We laser cut stainless steel to produce sticks with low friction and durability. You should grind the sharp edges to fit the stick with the components before assembly.
  + [Stick](/CAD%20files/Stick.dxf) (.dxf file)

<br>

- **Tools**<br>
You may need tools listed below while assembling the parts.
  + Screwdriver
  + Tapping tool
  + Rotary tool
  + Instant glue
  + Sandpaper

<br>

## Assembling process
  1. Use the tap to make threads on the module body and X axis guide as indicated below.
  <img src="/images/assembly1.jpg" width="400" alt="Module body and X axis guide with thread holes indicated.">
  2. Stick the shafts with the large spur gears, and then attach the gears with the axes guide parts. Note that aligning the shaft and the guide part is important, since this determines the inner friction.
  <img src="/images/assembly2.jpg" width="250" alt="Axes guide parts with large spur gears attached.">
  3. Install the stick inside the X axis guide (7mm flat M2 bolt). Ensure that the stick moves freely with minimum friction. Try to loosen the bolt or grind the stick if the stick hardly moves.
  <img src="/images/assembly3.jpg" width="250" alt="Stick placing inside the X axis guide part.">
  4. Cross the axes guide parts and fit into the module body.
  <img src="/images/assembly4.jpg" width="400" alt="Axes guides fit inside the module body.">
  5. Push in the potentiometers until they click into the module body. Check if the tips of the axes guides are well inserted.
  <img src="/images/assembly5.jpg" width="400" alt="Module body with the potentiometers attached.">
  6. Connect the motors with the motor mounts (M1.6 bolts).
  <img src="/images/assembly6.jpg" width="400" alt="Two motors with motor mounts attached for each.">
  7. Put the shaft holders first.
  <img src="/images/assembly7.jpg" width="400" alt="Shaft holders put on the shafts.">
  8. Connect the motor mounts with the module body (M2 bolts). Check if the stick moves smoothly inside the working space (It may get stuck in diagonal border area inside the module body, but it's OK since the stick won't use that area during actuation).
  <img src="/images/assembly8.jpg" width="400" alt="Module body and motors connected.">
  9. Put the stick cap on.
  <img src="/images/assembly9.jpg" width="400" alt="Stick cap added on the module body's stick.">
