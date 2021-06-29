# -*- coding: utf-8 -*-
"""
Created on wed Jun 16 01:33:32 2021

@authors: Andrea Bassi. Politecnico di Milano
"""
import QImaging_ScopeFoundry.qimaging_dll as qi
import numpy as np

class QImagingDevice(object):
    '''
    Scopefoundry compatible class to run QImaging
    '''
    
    def __init__(self,debug = False):
        self.debug = debug
        qi.LoadDriver()
        self.cam = qi.OpenCamera(qi.ListCameras()[0])
        self.cam.settings.readoutSpeed = 0 # 0=20MHz, 1=10MHz, 7=40MHz
        self.cam.settings.imageFormat = 'mono16'
        self.cam.settings.binning = 1
        self.cam.settings.triggerType = 0
    
    def close(self):
        self.cam.CloseCamera()
        qi.ReleaseDriver()
        
    def set_framenum(self, Nframes):
        pass
                    
    def read_temperature(self):
        cooled = self.cam.info.cooled
        return cooled
    
    def get_width(self):
        w = self.cam.info.ccdWidth
        ###w = self.cam.settings.roiWidth
        # w = 0 # TODO use parameter
        # if hasattr(self, 'buf'):
        #     w = self.buf.shape[0]    
        return w    
    
    def get_height(self):
        h =  self.cam.info.ccdHeight
        # h = 0 # TODO use parameter
        # if hasattr(self, 'buf'):
        #     h = self.buf.shape[1]    
        return h      
    
    def acq_start(self):
        self.cam.settings.Flush()
        self.cam.StartStreaming()
    
    def get_nparray(self):
        frame = self.cam.GrabFrame()
        dtype = np.uint16
        buf = np.frombuffer(frame.stringBuffer,
                            dtype = dtype).reshape((frame.height,frame.width))
       
        assert frame.width == self.cam.settings.roiWidth
        # self.buf = buf
        return(buf)
    
    def acq_stop(self):
        self.cam.StopStreaming()
        
    def get_exposure(self):
        "get the exposure time in ms"
        return(self.cam.settings.exposure/1000) # TODO use parameter

    def set_exposure(self, desired_time):
        "set the exposure time in ms"
        estimated_readout_lag = 1257 # microseconds
        exposure = desired_time*1000 # microseconds
        self.cam.settings.exposure = exposure - estimated_readout_lag
    
    def get_rate(self):
        return 0.0 # TODO use parameter

    def set_rate(self, desired_framerate):
        print('set frame rate not implemented')
        pass # TODO use parameter
    
    def get_gain(self):
        return self.cam.settings.gain
    
    def set_gain(self, desired_gain):
        self.cam.settings.gain = desired_gain
        
    def get_idname(self):
        cam_name = self.cam.info.cameraType
        return cam_name  
        
if __name__ == '__main__':  
    
    c = QImagingDevice()
    try:
        c.acq_start()
        frame = c.get_nparray()
        print((c.cam.info.ccdWidth))
        tmp = c.read_temperature()
        print((tmp))
        c.acq_stop()
    finally:
        c.close()
    
    
    
    