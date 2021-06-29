# -*- coding: utf-8 -*-
"""
Created on wed Jun 16 01:33:32 2021

@authors: Andrea Bassi. Politecnico di Milano
"""
from ScopeFoundry import BaseMicroscopeApp

class camera_app(BaseMicroscopeApp):
    
    name = 'camera_app'
    
    def setup(self):
        
        #Add hardware components
        print("Adding Hardware Components")
        from camera_hw import QImagingHW
        self.add_hardware(QImagingHW(self))
           
        # Add measurement components
        print("Create Measurement objects")
        from camera_measure import QImagingMeasure
        self.add_measurement(QImagingMeasure(self))

        self.ui.show()
        self.ui.activateWindow()

if __name__ == '__main__':
    import sys
    
    app = camera_app(sys.argv)
    sys.exit(app.exec_())