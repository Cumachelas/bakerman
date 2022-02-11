STARTDELAY "_int_" [s]
TRIGGER
LOOP
WAIT "_int_" [s]

LED

TEXT "_string_"
PRINTLN "_string_" - includes std_delay, but for loading apps, add extra

KEY "_key_" - either standard key names, or shortcuts like WIN, CTRL, etc

RUN "_command_" - includes std_delay, but for loading apps, add extra
BATCH "_path_"

&& "_comment" - totally ignored by the interpreter

