# Slicer Setup for MFM

## G-code coordinate positioning mode

All printing G-code must use [Relative Positioning for Extrusion](https://www.ideamaker.io/dictionaryDetail.html?name=Relative%20Extrusion&category_name=Printer%20Settings).

Printhead XYZE absolute positioning mode can be set with `G91` and only the Extruder (E) can be set to relative positioning with `M83`. If too little/too much filament is extruded, check to see if your extrusion positioning is incorrectly set to absolute in the slicer.

## Set Printer G-code

Add markers in your slicer software G-code for the end of new layer change and start and end of toolchange.

Save the printer profile with a new name and select the new printer profile for your prints.

![mfm slicer setup](assets/bambustudio-printer-settings.jpg)

### PrusaSlicer / BambuStudio / Orca Slicer steps

1. Printer > Settings > **Custom G-code / Machine G-code**

2. Add `; MFM LAYER CHANGE END` on a new line at the end of **After layer change G-code / Layer change G-code**.

3. Add `; MFM TOOLCHANGE START`  on a new line at the beginning of **Tool change G-code / Change filament G-code**.

4. Add `; MFM TOOLCHANGE END`  on a new line at the end of **Tool change G-code / Change filament G-code**.

5. The resulting settings text fields should have an order like below

#### After layer change G-code

```gcode
; Existing layer change G-code stays HERE

; MFM LAYER CHANGE END
```

#### Tool change G-code

```gcode
; MFM TOOLCHANGE START

; Existing toolchange G-code stays HERE

; MFM TOOLCHANGE END
```

## Set Filament Settings

### Disable `Long retraction when cut` (Bambu Studio/Orca Slicer)

Bambu Slicer and Orca Slicer have a conditional section in the toolchange that uses a proprietary G-code `M620.11` to perform a longer retraction before cutting filament. This command requires the previous extruder index for an unknown purpose. 

I assume that this previous extruder index is used to simultaneously retract the previous extruder index filament feeder inside the AMS and the printhead extruder. This may be for reliability if the new longer retraction distance being greater than what the filament buffer was initially designed to buffer. 

Before the toolchange

```gcode
{if long_retractions_when_cut[previous_extruder]}
M620.11 S1 I[previous_extruder] E-{retraction_distances_when_cut[previous_extruder]} F{old_filament_e_feedrate}
{else}
M620.11 S0
{endif}
```

After the toolchange, before flushing

```gcode
{if long_retractions_when_cut[previous_extruder]}
M620.11 S1 I[previous_extruder] E{retraction_distances_when_cut[previous_extruder]} F{old_filament_e_feedrate}
M628 S1
G92 E0
G1 E{retraction_distances_when_cut[previous_extruder]} F[old_filament_e_feedrate]
M400
M629 S1
{else}
M620.11 S0
{endif}
```

For every filament used:

1. Filament > **Setting Overrides**
2. Uncheck `Long retraction when cut`

## Set Post-processing Scripts *(optional)*

Add MFM as a post-processing script if you want to automatically run MFM in your Slicer. 

If you plan to do the processing through the standalone MFM GUI app, you can skip this step.

### PrusaSlicer

1. Set the settings view to **Expert Mode** in the upper right.

1. Print Settings > Output options > **Post-processing scripts**

![PrusaSlicer postprocessing script printer setting option](assets/prusaslicer-post-processing-script-option.png)

### Bambu Studio / Orca Slicer

1. Enable **Advanced** view for Process

1. Process > Others > **Post-processing scripts**

### Next Steps for All Slicers

3. Create the MFM command text as described in [MFM Command Setup](terminal-setup.md)

4. Add the final command text to **Post-processing scripts** 
