# emacs-mode: -*- python-*-
import Live
from ShiftableDeviceComponent import *
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.LogicalDisplaySegment import LogicalDisplaySegment


class kmkDisplayingDeviceComponent(ShiftableDeviceComponent):
    __module__ = __name__
    __doc__ = """ Special device class that adds physical displays (lcd) to the
                device controller used by the APC40 """
    

    def __init__(self):
        ShiftableDeviceComponent.__init__(self)
        self._main_lcds = None
        self._parameter_data_sources = []
        for index in range(8):
            self._parameter_data_sources.append(DisplayDataSource())
            self._parameter_data_sources[-1].set_display_string('---')
        self._device_name_lcd = None
        # Explicitly NAME the device_name_data_source
        # This is provided and controlled by DeviceComponent
        # I only need to assign it to a display
        self._device_name_data_source = DisplayDataSource()
        self._param_name_value_toggle = False



    def set_param_name_value_toggle(self, falseOrTrue):
        self._param_name_value_toggle = falseOrTrue



    def set_display(self, parameter_displays, device_name_display):
        self._main_lcds = parameter_displays
        self._device_name_lcd = device_name_display
        if (self._main_lcds != None):
            for index in range(8):
                self._main_lcds[index].segment(0).set_data_source(self._parameter_data_sources[index])
        if (self._device_name_lcd != None):
            self._device_name_lcd.segment(0).set_data_source(self._device_name_data_source)

        

    def disconnect(self):
        ShiftableDeviceComponent.disconnect(self)
        self._main_lcds = None
        self._parameter_data_sources = None
        self._device_name_lcd = None
        self._device_name_data_source = None

    def update_display(self):
        self.set_lcd_display_strings()

    def set_lcd_display_strings(self):
        for index in range(len(self._parameter_controls)):
            if (self._parameter_controls[index].mapped_parameter() != None):
                if (self._param_name_value_toggle == True):
                    self._parameter_data_sources[index].set_display_string(self._parameter_controls[index].mapped_parameter().__str__())
                else:
                    self._parameter_data_sources[index].set_display_string(self._parameter_controls[index].mapped_parameter().name)
            else:
                self._parameter_data_sources[index].set_display_string('---')
        
        

# override from DeviceComponent
    def _assign_parameters(self):
        DeviceComponent._assign_parameters(self)
        self.set_lcd_display_strings()



# local variables:
# tab-width: 4
