# emacs-mode: -*- python-*-
import Live
from _Framework.ButtonElement import *
from kmkSysexLookup import *

class SysexButtonElement(ButtonElement):
    __module__ = __name__
    __doc__ = ' Special button class that send on- and off-values as sysex formatted for the KMK in native mode '

    def __init__(self, is_momentary, msg_type, channel, identifier):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)

# OVERRIDEN.....(from InputControlElement)
# Changed to wrap replies in KMK sysex

    def send_value(self, value, force_send = False):
        assert (value != None)
        assert isinstance(value, int)
        assert (value in range(128))
        if (force_send or ((value != self._last_sent_value) and self._is_being_forwarded)):
            data_byte1 = self._original_identifier
            data_byte2 = (value > 0) * 32
            self.send_midi(SYSEX_KMK_HEADER + (KMK_LED_COMMAND, data_byte1, data_byte2, 0xF7))
            self._last_sent_value = value
            if self._report_output:
                is_input = True
                self._report_value(value, (not is_input))


# local variables:
# tab-width: 4
