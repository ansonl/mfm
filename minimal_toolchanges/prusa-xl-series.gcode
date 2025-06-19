; MFM MINIMAL XL TOOLCHANGE START
M104 S70 TYY ; set temperature ;cooldown
M104 S170 TXX ; start heating up new nozzle

G1 E-20 F2100 ; retract

; Change ToolYY -> ToolXX (MFM inserted)
G1 F21000
P0 S1 M1 L2 D0 ; Park tool. Remove M1 to use tool mapping
;
M109 S240 TXX ; YOUR PRINTING TEMP HERE
TXX M1 S1 L0 D0 ; Toolchange Remove M1 to use tool mapping


M900 K0.05 ; Filament gcode ; YOUR CUSTOM LINEAR ADVANCE K VALUE HERE


M572 S0.036 ; Filament gcode ; YOUR PRESSURE ADVANCE HERE


M142 S36 ; set heatbreak target temp
M109 S240 TXX ; set temperature and wait for it to be reached

G4 S0
M591 

G1 E20 F1500
G1 F24000
M204 P500
; MFM MINIMAL TOOLCHANGE END
