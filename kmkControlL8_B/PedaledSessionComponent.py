# emacs-mode: -*- python-*-
import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement
class PedaledSessionComponent(SessionComponent):
    __module__ = __name__
    __doc__ = ' Special SessionComponent with a button (pedal) to fire the selected clip slot '

    def __init__(self, num_tracks, num_scenes):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self._slot_launch_button = None



    def disconnect(self):
        SessionComponent.disconnect(self)
        if (self._slot_launch_button != None):
            self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = None



    def set_slot_launch_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._slot_launch_button != None):
            self._slot_launch_button.remove_value_listener(self._slot_launch_value)
        self._slot_launch_button = button
        if (self._slot_launch_button != None):
            self._slot_launch_button.add_value_listener(self._slot_launch_value)



    def _slot_launch_value(self, value):
        assert (value in range(128))
        assert (self._slot_launch_button != None)
        if self.is_enabled():
            if ((value != 0) or (not self._slot_launch_button.is_momentary())):
                self.song().view.highlighted_clip_slot.fire()




# local variables:
# tab-width: 4
