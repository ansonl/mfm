# Printer Setup for MFM

## Material Auto Refill

### Bambu AMS

**AMS loaded filaments must be set such that each slot shows a different material type or color**. Bambu printers will try to substitute slots with similar material and a toolchange between slots with the same material and color set may be ignored. 

**Auto Refill should be turned off.**

> The actual physical material and colors loaded do not need to be different or accurately reflected in the printer screen or slicer Device tab. Only the material/color shown on the printer or Device tab need to be distinct from each other.

## Timelapse

### Bambu Studio

Bambu Studio does not allow you to directly Print imported G-code to the printer so you cannot enable the timelapse checkbox. You can enable timelapse in a G-code file by replacing all occurences of

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
