import mido
import adafruit_mcp4725
import board
import busio

i2c_1 = busio.I2C(board.SCL, board.SDA)
#i2c_2 = busio.I2C(24, 23)

dac_PITCH = adafruit_mcp4725.MCP4725(i2c_1, address= 0x60)
dac_HOLD = adafruit_mcp4725.MCP4725(i2c_1, address= 0x61)
#dac_MOD = adafruit_mcp4725.MCP4725(i2c_2, address= 0x60)
#dac_TRIG = adafruit_mcp4725.MCP4725(i2c_2, address= 0x61)


from midi_handler import *
from port_manager import *



p = PortManager()
m = MidiHandler()

try:
    while True:
        if not p.is_scanning:
            with mido.open_input(p.input_name) as port:
                while not port.closed:
                    for msg in port.iter_pending():
                        m.input_signal(msg)
                    if p.is_scanning:
                        port.close()
                    dac_PITCH.normalized_value = m.PITCH_V
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nExiting..")

