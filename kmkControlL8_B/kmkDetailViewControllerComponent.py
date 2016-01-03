# emacs-mode: -*- python-*-
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
SHOW_PLAYING_CLIP_DELAY = 5
class DetailViewControllerComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Component that can toggle the device chain- and clip view of the selected track '

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._device_clip_toggle_button = None
        self._detail_toggle_button = None
        """ WAC addition...................................."""
        self._browser_toggle_button = None
        self._arrange_toggle_button = None
        """------------------------------------------------"""
        self._left_button = None
        self._right_button = None
        self._shift_button = None
        self._shift_pressed = False
        self._show_playing_clip_ticks_delay = -1
        self.application().view.add_is_view_visible_listener('Detail', self._detail_view_visibility_changed)
        self._register_timer_callback(self._on_timer)



    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self.application().view.remove_is_view_visible_listener('Detail', self._detail_view_visibility_changed)
        if (self._device_clip_toggle_button != None):
            self._device_clip_toggle_button.remove_value_listener(self._device_clip_toggle_value)
            self._device_clip_toggle_button = None
        if (self._detail_toggle_button != None):
            self._detail_toggle_button.remove_value_listener(self._detail_toggle_value)
            self._detail_toggle_button = None
        if (self._left_button != None):
            self._left_button.remove_value_listener(self._nav_value)
            self._left_button = None
        if (self._right_button != None):
            self._right_button.remove_value_listener(self._nav_value)
            self._right_button = None
        if (self._shift_button != None):
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        """ WAC addition...................................."""
        if (self._browser_toggle_button != None):
            self._browser_toggle_button.remove_value_listener(self._browser_toggle_value)
            self._browser_toggle_button = None
        if (self._arrange_toggle_button != None):
            self._arrange_toggle_button.remove_value_listener(self._arrange_toggle_value)
            self._arrange_toggle_button = None
        """------------------------------------------------"""



    def set_device_clip_toggle_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._device_clip_toggle_button != None):
            self._device_clip_toggle_button.remove_value_listener(self._device_clip_toggle_value)
        self._device_clip_toggle_button = button
        if (self._device_clip_toggle_button != None):
            self._device_clip_toggle_button.add_value_listener(self._device_clip_toggle_value)



    def set_detail_toggle_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._detail_toggle_button != None):
            self._detail_toggle_button.remove_value_listener(self._detail_toggle_value)
        self._detail_toggle_button = button
        if (self._detail_toggle_button != None):
            self._detail_toggle_button.add_value_listener(self._detail_toggle_value)



    """ WAC addition...................................."""
    def set_browser_toggle_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._browser_toggle_button != None):
            self._browser_toggle_button.remove_value_listener(self._browser_toggle_value)
        self._browser_toggle_button = button
        if (self._browser_toggle_button != None):
            self._browser_toggle_button.add_value_listener(self._browser_toggle_value)

    def set_arrange_toggle_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._arrange_toggle_button != None):
            self._arrange_toggle_button.remove_value_listener(self._arrange_toggle_value)
        self._arrange_toggle_button = button
        if (self._arrange_toggle_button != None):
            self._arrange_toggle_button.add_value_listener(self._arrange_toggle_value)
    """ ------------------------------------------------"""



    def set_device_nav_buttons(self, left_button, right_button):
        assert ((left_button == None) or isinstance(left_button, ButtonElement))
        assert ((right_button == None) or isinstance(right_button, ButtonElement))
        identify_sender = True
        if (self._left_button != None):
            self._left_button.remove_value_listener(self._nav_value)
        self._left_button = left_button
        if (self._left_button != None):
            self._left_button.add_value_listener(self._nav_value, identify_sender)
        if (self._right_button != None):
            self._right_button.remove_value_listener(self._nav_value)
        self._right_button = right_button
        if (self._right_button != None):
            self._right_button.add_value_listener(self._nav_value, identify_sender)



    def set_shift_button(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if (self._shift_button != None):
            self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = button
        if (self._shift_button != None):
            self._shift_button.add_value_listener(self._shift_value)



    def on_enabled_changed(self):
        self.update()



    def update(self):
        if self.is_enabled():
            if (not self._shift_pressed):
                if (self._left_button != None):
                    self._left_button.turn_off()
                if (self._right_button != None):
                    self._right_button.turn_off()
                if (self._device_clip_toggle_button != None):
                    self._device_clip_toggle_button.turn_off()
                self._detail_view_visibility_changed()



    def _detail_view_visibility_changed(self):
        if (self.is_enabled() and ((not self._shift_pressed) and (self._detail_toggle_button != None))):
            if self.application().view.is_view_visible('Detail'):
                self._detail_toggle_button.turn_on()
            else:
                self._detail_toggle_button.turn_off()



    def _device_clip_toggle_value(self, value):
        assert (self._device_clip_toggle_button != None)
        assert (value in range(128))
        if (self.is_enabled() and (not self._shift_pressed)):
            button_is_momentary = self._device_clip_toggle_button.is_momentary()
            if ((not button_is_momentary) or (value != 0)):
                if (not self.application().view.is_view_visible('Detail')):
                    self.application().view.show_view('Detail')
                if (not self.application().view.is_view_visible('Detail/DeviceChain')):
                    self.application().view.show_view('Detail/DeviceChain')
                else:
                    self.application().view.show_view('Detail/Clip')
            if (button_is_momentary and (value != 0)):
                self._show_playing_clip_ticks_delay = SHOW_PLAYING_CLIP_DELAY
            else:
                self._show_playing_clip_ticks_delay = -1



    def _detail_toggle_value(self, value):
        assert (self._detail_toggle_button != None)
        assert (value in range(128))
        if (self.is_enabled() and (not self._shift_pressed)):
            if ((not self._detail_toggle_button.is_momentary()) or (value != 0)):
                if (not self.application().view.is_view_visible('Detail')):
                    self.application().view.show_view('Detail')
                else:
                    self.application().view.hide_view('Detail')



    """WAC addition...................................."""
    def _browser_toggle_value(self, value):
        assert (self._browser_toggle_button != None)
        assert (value in range(128))
        if (self.is_enabled() and (not self._shift_pressed)):
            if ((not self._browser_toggle_button.is_momentary()) or (value != 0)):
                if (not self.application().view.is_view_visible('Browser')):
                    self.application().view.show_view('Browser')
                    self._browser_toggle_button.turn_on()
                else:
                    self.application().view.hide_view('Browser')
                    self._browser_toggle_button.turn_off()



    def _arrange_toggle_value(self, value):
        assert (self._arrange_toggle_button != None)
        assert (value in range(128))
        if (self.is_enabled() and (not self._shift_pressed)):
            button_is_momentary = self._arrange_toggle_button.is_momentary()
            if ((not button_is_momentary) or (value != 0)):
                if (not self.application().view.is_view_visible('Arranger')):
                    self.application().view.show_view('Arranger')
                    self._arrange_toggle_button.turn_on()
                else:
                    self.application().view.show_view('Session')
                    self._arrange_toggle_button.turn_off()
    """ ------------------------------------------------"""


    def _shift_value(self, value):
        assert (self._shift_button != None)
        assert (value in range(128))
        self._shift_pressed = (value != 0)
        self.update()



    def _nav_value(self, value, sender):
        assert ((sender != None) and (sender in (self._left_button,
         self._right_button)))
        if (self.is_enabled() and (not self._shift_pressed)):
            if ((not sender.is_momentary()) or (value != 0)):
                modifier_pressed = True
                if ((not self.application().view.is_view_visible('Detail')) or (not self.application().view.is_view_visible('Detail/DeviceChain'))):
                    self.application().view.show_view('Detail')
                    self.application().view.show_view('Detail/DeviceChain')
                else:
                    direction = Live.Application.Application.View.NavDirection.left
                    if (sender == self._right_button):
                        direction = Live.Application.Application.View.NavDirection.right
                    self.application().view.scroll_view(direction, 'Detail/DeviceChain', (not modifier_pressed))



    def _on_timer(self):
        if (self.is_enabled() and (not self._shift_pressed)):
            if (self._show_playing_clip_ticks_delay > -1):
                if (self._show_playing_clip_ticks_delay == 0):
                    song = self.song()
                    playing_slot_index = song.view.selected_track.playing_slot_index
                    if (playing_slot_index > -1):
                        song.view.selected_scene = song.scenes[playing_slot_index]
                        if song.view.highlighted_clip_slot.has_clip:
                            self.application().view.show_view('Detail/Clip')
                self._show_playing_clip_ticks_delay -= 1




# local variables:
# tab-width: 4
