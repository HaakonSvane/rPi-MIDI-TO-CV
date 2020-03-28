from parameters import *

class MidiHandler:
    def __init__(self):

        # All values must be between 0 and 1
        self.PITCH_V = 0
        self.MOD_V = 0
        self.HOLD_V = 0
        self.TRIG_V = 0

        self._note_diff = 1/(NOTE_RANGE[1]-NOTE_RANGE[0]-1)

        self._note_stack = []


    def get_pitch(self):
        return 0
    def get_hold(self):
        return self.HOLD_V

    def _set_pitch(self, normed_val):
        self.PITCH_V = 1 if normed_val > 1 else (0 if normed_val < 0 else normed_val)

    def _note_on(self, data):
        self._note_stack.append(data)
        self.HOLD_V = 1
        val = (data-NOTE_RANGE[0])*self._note_diff
        self._set_pitch(val)

    def _note_off(self, data):
        try:
            self._note_stack.remove(data)
        except:
            pass
        if not self._note_stack:
            self.HOLD_V = 0
        else:
            d = self._note_stack[-1]
            val = (d - NOTE_RANGE[0]) / (NOTE_RANGE[1] - NOTE_RANGE[0] - 1)
            self.PITCH_V = 1 if val > 1 else (0 if val < 0 else val)

    def _pitch_wheel(self, data):
        if not self._note_stack:
            return
        mod = data/8192*2*self._note_diff
        val = (self._note_stack[-1]-NOTE_RANGE[0])*self._note_diff + mod
        self._set_pitch(val)


    def _control_change(self, channel, control, value):
        if control == 121:
            self._note_stack.clear()
            self.PITCH_V = 0
            self.HOLD_V = 0


    def input_signal(self, msg):
        if msg.type == "note_on":
            if NOTE_RANGE[0] <= msg.note <= NOTE_RANGE[1]:
                if msg.velocity == 0:
                    self._note_off(msg.note)
                else:
                    self._note_on(msg.note)
        elif msg.type == "pitchwheel":
            self._pitch_wheel(msg.pitch)

        elif msg.type == "control_change":
            self._control_change(msg.channel, msg.control, msg.value)

        else:
            print(msg)



