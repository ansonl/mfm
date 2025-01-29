; This file is a reference file for the extra purge Gcode that is actually used in mfm/extra_purge.py

G91
G1 X3 F12000; move aside to extrude
G90
M83

; FLUSH_START
G1 E11.2253 F299
G1 E1.24726 F50
G1 E11.2253 F299
G1 E1.24726 F50
G1 E11.2253 F299
G1 E1.24726 F50
G1 E11.2253 F299
G1 E1.24726 F50
G1 E11.2253 F299
G1 E1.24726 F50
; FLUSH_END
G1 E-2 F1800
G1 E2 F300