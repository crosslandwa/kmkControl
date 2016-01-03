import Live
from _Framework.ControlSurface import ControlSurface
from kmkControlL8_B.kmkSysexLookup import *

MIDI_NOTE_ON_STATUS = 144
MIDI_CC_STATUS = 176

class kmkControlA(ControlSurface):
    __module__ = __name__
    __doc__ = " Sysex handler script for Korg Microkontrol by WAC "

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.log_message("!!!!!!!!!!!KMK_A sysex handler is go!!!!!!!!!!!")



    # override the handle_sysex() method in the ControlSurface base class
    def handle_sysex(self, midi_bytes):
        if (midi_bytes[0:5] == SYSEX_KMK_HEADER):
            if (midi_bytes[5:8] == (0x40, 0x00, 0x03)):
                self._send_midi(SYSEX_NATIVE_1)
            elif (midi_bytes[5:8] == (0x5F, 0x00, 0x00)):
                self._send_midi(SYSEX_NATIVE_2)
            elif (midi_bytes[5:8] == (0x5F, 0x01, 0x00)):
                self._send_midi(SYSEX_NATIVE_3)
            elif (midi_bytes[5:8] == (0x5F, 0x02, 0x00)):
                self._send_midi(SYSEX_NATIVE_4)
            elif (midi_bytes[5:8] == (0x5F, 0x03, 0x00)):
                self._send_midi(midi_bytes)
            elif (midi_bytes[5] == KMK_PAD_COMMAND):
                pad = midi_bytes[6] & 0x0F
                if (midi_bytes[7] > 0):
                    vel = 127
                else:
                    vel = 0
                vel *= ((midi_bytes[6] >> 6) & 0x01)
                self._send_midi((MIDI_NOTE_ON_STATUS, pad, vel))
            elif (midi_bytes[5] == KMK_ENC_COMMAND):
                if (midi_bytes[6] != KMK_ENCODER[8]):
                    self._send_midi((MIDI_CC_STATUS, midi_bytes[6], midi_bytes[7]))
                else:
                    self._send_midi(midi_bytes)
            elif (midi_bytes[5] == KMK_SLIDER_COMMAND):
                self._send_midi((MIDI_CC_STATUS, KMK_FADER[midi_bytes[6]], midi_bytes[7]))
            elif (midi_bytes[5] == KMK_JOYSTICK_COMMAND):
                pass
            elif (midi_bytes[5] == KMK_BUTTON_COMMAND):
                if (midi_bytes[6] > 1):
                    buttonNumber = KMK_BUTTON[7 - midi_bytes[6]]
                    self._send_midi((MIDI_NOTE_ON_STATUS, buttonNumber, midi_bytes[7]))
            elif (midi_bytes[5] == KMK_PEDAL_COMMAND):
                self._send_midi((MIDI_NOTE_ON_STATUS, 101, midi_bytes[7]))