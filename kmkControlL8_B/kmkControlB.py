import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.MixerComponent import MixerComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ChannelTranslationSelector import ChannelTranslationSelector
from EncoderMixerModeSelectorComponent import EncoderMixerModeSelectorComponent
from kmkDetailViewControllerComponent import DetailViewControllerComponent
from kmkDisplayingDeviceComponent import kmkDisplayingDeviceComponent
from ShiftableTransportComponent import ShiftableTransportComponent
from ShiftableTranslatorComponent import ShiftableTranslatorComponent
from PedaledSessionComponent import PedaledSessionComponent

from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from kmkSysexButtonElement import SysexButtonElement
from kmkSysexLookup import *
device = None


class kmkControlB (ControlSurface):
    __module__ = __name__
    __doc__ = """ Second part of script for Korg Microkontrol by WAC,
    based on the script for Akai's APC40 Controller """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.log_message("!!!!!!!!!!!KMK_B control surface is go!!!!!!!!!!!")
        self.set_suppress_rebuild_requests(True)
        is_momentary = True
        self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[11])
        mixer = self._setup_mixer_control()
        self._setup_device_and_transport_control()
        self.set_suppress_rebuild_requests(False)



    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._update_hardware)



    def _update_hardware(self):
        self._send_midi(SYSEX_NATIVE_ON)



    def handle_sysex(self, midi_bytes):
        if (midi_bytes[0:8] == (SYSEX_KMK_HEADER + (0x5F, 0x03, 0x00))):
            # when native mode transition complete
            self._on_selected_track_changed()
        elif (midi_bytes[0:7] == (SYSEX_KMK_HEADER + (KMK_ENC_COMMAND, 0x08))):
            # toggle lcd displays using 'main' encoder
            device.set_param_name_value_toggle(midi_bytes[7] < 63)
        else:
            # output any sysex received (from KMK_A) back to hardware
            ControlSurface._send_midi(self, midi_bytes)



    def _setup_mixer_control(self):
        is_momentary = True
        mixer = MixerComponent(1)
        mixer.selected_strip().set_mute_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[9]))
        mixer.selected_strip().set_solo_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[13]))
        mixer.set_select_buttons(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[15]),
                                 SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[14]))
        send_faders = []
        NUM_CONTROLLABLE_SENDS = 4
        for index in range(NUM_CONTROLLABLE_SENDS):
            send_faders.append(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[index + 2]))
        mixer.selected_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[0]))
        mixer.selected_strip().set_pan_control(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[1]))
        mixer.selected_strip().set_send_controls(tuple(send_faders))
        mixer.set_prehear_volume_control(EncoderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[6], Live.MidiMap.MapMode.absolute))
        mixer.master_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[7]))
        return mixer



    def _setup_device_and_transport_control(self):
        is_momentary = True
        device_bank_buttons = []
        device_param_controls = []
        for index in range(8):
            device_bank_buttons.append(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, KMK_PAD[index]))
            device_param_controls.append(EncoderElement(MIDI_CC_TYPE, 0, KMK_ENCODER[index], Live.MidiMap.MapMode.relative_two_compliment))

        global device

        # special component, inherits from ShiftableDeviceController and adds lcds
        device = kmkDisplayingDeviceComponent()
        device.set_bank_buttons(tuple(device_bank_buttons))
        device.set_shift_button(self._shift_button)
        device.set_parameter_controls(tuple(device_param_controls))
        device.set_on_off_button(device_bank_buttons[1])
        device.set_lock_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[10]))
        parameter_displays = []
        for index in range(8):
            parameter_displays.append(PhysicalDisplayElement(8, 1))
            parameter_displays[-1].set_message_parts((SYSEX_KMK_HEADER + (KMK_LCD_COMMAND, 9, (index + 48))), (247,))
        device_name_display = PhysicalDisplayElement(8,1)
        device_name_display.set_message_parts((SYSEX_KMK_HEADER + (KMK_LCD_COMMAND, 9, (8 + 32))), (247,))
        device.set_display(parameter_displays, device_name_display)
        self.set_device_component(device)
        detail_view_toggler = DetailViewControllerComponent()
        detail_view_toggler.set_shift_button(self._shift_button)
        detail_view_toggler.set_device_clip_toggle_button(device_bank_buttons[0])
        detail_view_toggler.set_detail_toggle_button(device_bank_buttons[4])
        detail_view_toggler.set_device_nav_buttons(device_bank_buttons[2], device_bank_buttons[3])
        detail_view_toggler.set_arrange_toggle_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, KMK_PAD[8]))
        detail_view_toggler.set_browser_toggle_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, KMK_PAD[12]))
        transport = ShiftableTransportComponent()
        transport.set_shift_button(self._shift_button)
        transport.set_play_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[4]))
        transport.set_stop_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[5]))
        transport.set_record_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[3]))
        transport.set_seek_buttons(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[1]),
                                   SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[0]))
        transport.set_loop_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[2]))
        transport.set_quant_toggle_button(device_bank_buttons[5])
        transport.set_overdub_button(device_bank_buttons[6])
        transport.set_metronome_button(device_bank_buttons[7])
        bank_button_translator = ShiftableTranslatorComponent()
        bank_button_translator.set_controls_to_translate(tuple(device_bank_buttons))
        bank_button_translator.set_shift_button(self._shift_button)



    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        track = self.song().view.selected_track
        device_to_select = track.view.selected_device
        if ((device_to_select == None) and (len(track.devices) > 0)):
            device_to_select = track.devices[0]
        if (device_to_select != None):
            self.song().view.select_device(device_to_select)
        self._device_component.set_device(device_to_select)



    # Override
    def update_display(self):
        ControlSurface.update_display(self)
        device.update_display( )



    def disconnect(self):
        self.log_message("--------------= KMK_B Bye Bye =--------------")
        self._send_midi(SYSEX_NATIVE_OFF)
        # call disconnect() method in the base class
        ControlSurface.disconnect(self)
        return None