import rtmidi

r = rtmidi.MidiIn()
print(r.get_ports())