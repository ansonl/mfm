# Printer Setup for MFM

You need to find a way to execute the G-code on your 3D printer.

## Sending G-code to the 3D printer

### Most 3D Printers

For most 3D printers you can send or stream G-code directly to your printer with a USB or network serial connection.

You can also copy G-code to an SD card that you put into the printer.

### Bambu Lab Printers

Bambu Studio allows you to **Send** previewed G-code to Bambu Lab printers over a network connection. You can print the sent G-code on the Bambu printer screen itself after ensuring the colors are physically located in the correct AMS slots.

Bambu will not allow you to directly use the Bambu Studio **Print** action to run a G-code file.

Bambu Lab has unreasonably required a printer have LAN Mode turned off to use SD storage features in Bambu Studio.

#### You have LAN Mode turned off

If you do not have LAN Mode enabled, you can remotely print and assign AMS mapping, Bed Leveling, and Timelapse settings to a Bambu Printer through the Device > MicroSD Card > Model screen. This method should work until you upgrade your printer's firmware after January 2025 or Bambu remotely triggers a firmware update on your printer. Newer firmware will require Bambu Cloud authorization to print all files from a computer (even if you turn on LAN mode).

#### You have LAN Mode turned on

Use **Send** in Bambu Studio or [FTPS](https://forum.bambulab.com/t/we-can-now-connect-to-ftp-on-the-p1-and-a1-series/6464) to transfer the G-code file to the printer. Your filament must be placed in the correct indices in the AMS.

Start G-code file using the printer display or an MQTT integration.

## Material Auto Refill

### Bambu AMS

**AMS loaded filaments must be set such that each slot shows a different material type or color**. Bambu printers will try to substitute slots with similar material and a toolchange between slots with the same material and color set may be ignored.

**Auto Refill should be turned off.**

> The actual physical material and colors loaded do not need to be different or accurately reflected in the printer screen or slicer Device tab. Only the material/color shown on the printer or Device tab need to be distinct from each other.

### Bambu AMS out of filament behavior

If you want to swap/save filament by changing out filament in the same AMS slot, you should swap the filament from the AMS slot when it is **not** the active filament.

When the active filament is detected as "run out" by the AMS, the printer will purge the ENTIRE filament tube of filament all the way from the AMS to the extruder. This is a huge waste of material and should be avoided. This behavior is probably because backing out filament that ends inside the first stage feeder is considered unreliable by Bambu.

## Timelapse

### Bambu Studio

Bambu Studio does not allow you to directly Print imported G-code to LAN Mode printers so you cannot enable the timelapse checkbox. You can enable default timelapse in a G-code file by replacing all occurences of

```gcode
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623
```

with

```gcode
M971 S11 C10 O0
```

or replacing `M622 J1` with `M622 J0` for only the conditional timelapse statements that check the timelapse checkbox option normally sent from Bambu Studio.
