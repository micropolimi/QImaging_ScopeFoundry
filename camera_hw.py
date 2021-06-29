# -*- coding: utf-8 -*-
"""
Created on wed Jun 16 01:33:32 2021

@authors: Andrea Bassi. Politecnico di Milano
"""
from ScopeFoundry import HardwareComponent
from QImaging_ScopeFoundry.camera_device import QImagingDevice

class QImagingHW(HardwareComponent):
    name = 'QImaginghw'
    
    def setup(self):
        # create Settings (aka logged quantities)
        # self.infos = self.add_logged_quantity('name', dtype=str)     
        self.infos = self.settings.New(name='name', dtype=str)
        self.cooled = self.settings.New(name='cooled', dtype=bool, ro=True)
        self.image_width = self.settings.New(name='image_width', dtype=int, ro=True,unit='px')
        self.image_height = self.settings.New(name='image_height', dtype=int, ro=True,unit='px')
        self.gain = self.settings.New(name='gain', initial=0., dtype=float,
                                      vmax = 1000., vmin = 0., spinbox_step = 1.,
                                      ro=False, unit='dB', reread_from_hardware_after_write=True)
        self.frame_rate = self.settings.New(name='frame_rate', initial= 5,
                                            vmax = 1000., vmin = 0.01, spinbox_step = 0.1,
                                            unit = 'fps', dtype=float, ro=False, reread_from_hardware_after_write=True)
        self.frame_num = self.settings.New(name='frame_num',initial= 10, spinbox_step = 1,
                                           dtype=int, ro=False)
        self.exposure_time = self.settings.New(name='exposure_time', initial=100, vmax =5000.,
                                               vmin = 0.02, spinbox_step = 0.1,dtype=float, ro=False, unit='ms',reread_from_hardware_after_write=True)
        self.acquisition_mode = self.settings.New(name='acquisition_mode', dtype=str,
                                                  choices=['Continuous', 'MultiFrame'], initial = 'Continuous', ro=False)
        
    def connect(self):
        # create an instance of the Device
        self.camera = QImagingDevice(debug=self.debug_mode.val)      
        
        # connect settings to Device methods
        self.cooled.hardware_read_func = self.camera.read_temperature
        self.image_width.hardware_read_func = self.camera.get_width
        self.image_height.hardware_read_func = self.camera.get_height
        self.infos.hardware_read_func = self.camera.get_idname
        self.exposure_time.hardware_read_func = self.camera.get_exposure
        self.exposure_time.hardware_set_func = self.camera.set_exposure
        self.frame_rate.hardware_read_func = self.camera.get_rate
        self.frame_rate.hardware_set_func = self.camera.set_rate
        self.frame_num.hardware_set_func = self.camera.set_framenum
        self.gain.hardware_read_func = self.camera.get_gain
        self.gain.hardware_set_func = self.camera.set_gain
        self.read_from_hardware()
        
    def disconnect(self):
        if hasattr(self, 'camera'):
            self.camera.close() 
            del self.camera
            
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None

