from automatic_spectral_acquisition.calibration import Calibration

class Config:
    def __init__(self,
                 arduino_port:str|None=None,
                 oscilloscope_port:str|None=None,
                 m:float|None=None,
                 c:float|None=None) -> None:
        self.arduino_port:str = arduino_port
        self.oscilloscope_port:str = oscilloscope_port
        
        self.m:float = m
        self.c:float = c
    
class ConfigHandler:
    def __init__(self,
                 arduino_port:str|None=None,
                 oscilloscope_port:str|None=None,
                 m:float|None=None,
                 c:float|None=None,
                 wavelengths:list[float]=None,
                 positions:list[float]=None) -> None:
        
        self.config = Config(arduino_port, oscilloscope_port, m, c)
        self.calibration = Calibration(wavelengths, positions)
        
    def save_config(self) -> None:
        ...
    
    def load_config(self) -> None:
        ...
        
    def calibrate(self) -> None:
        ...
    
    # ...
        
    def position(self, wavelength:float) -> float:
        return self.calibration.position(wavelength)