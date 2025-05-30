; MFM MINIMAL X1/P1 TOOLCHANGE START
; 24DEC24
M220 S100
M106 P3 S0
G1 E-.1 F1800

M620 SXXA
M204 S9000

G17
;G2 ZINITIALLIFT I0.86 J0.86 P1 F10000 ; spiral lift a little from second lift
G91
G2 Z0.4 I0.86 J0.86 P1 F10000 ; spiral lift a little from second lift
G90
M83

G91
G1 Z2.6 F1200
G90
M83

G1 X70 F21000
G1 Y245
G1 Y265 F3000
M400
M106 P1 S0
M106 P2 S0

M104 S220


M620.11 S0

M400
G1 X90
G1 Y255 F4000
G1 X100 F5000
G1 X120 F15000
G1 X20 Y50 F21000
G1 Y-3

M620.1 E F299 T240
TXX
M620.1 E F299 T240



M620.11 S0

G92 E0

M83
; FLUSH_START
; always use highest temperature to flush
M400

M109 S240


G1 E23.7 F299 ; do not need pulsatile flushing for start part
G1 E0.773255 F50
G1 E8.89243 F299
G1 E0.773255 F50
G1 E8.89243 F299
G1 E0.773255 F50
G1 E8.89243 F299
G1 E0.773255 F50
G1 E8.89243 F299

; FLUSH_END
G1 E-2 F1800
G1 E2 F300

; FLUSH_START
M400
M109 S220
G1 E2 F523 ;Compensate for filament spillage during waiting temperature
; FLUSH_END
M400
G92 E0
G1 E-2 F1800
M106 P1 S255
M400 S3

G1 X70 F5000
G1 X90 F3000
G1 Y255 F4000
G1 X105 F5000
G1 Y265
G1 X70 F10000
G1 X100 F5000
G1 X70 F10000
G1 X100 F5000

G1 X70 F10000
G1 X80 F15000
G1 X60
G1 X80
G1 X60
G1 X80 ; shake to put down garbage
G1 X100 F5000
G1 X165 F15000; wipe and shake
G1 Y256 ; move Y to aside, prevent collision
M400

M204 S10000


M621 SXXA

M106 S200 ; resume fan speed
M106 P2 S0 ; turn off aux fan, leave P3 chamber fan unchanged

;G91
;G1 Z-2.6 F30000
;G90
;M83

;G91
;G1 Z-0.4
;G90
;M83

; MFM will lower Z to original position and extrude E2 during pre-feature restore

M204 S5000
; MFM MINIMAL TOOLCHANGE END