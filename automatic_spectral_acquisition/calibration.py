import numpy as np


class Calibration:
    def __init__(self, wavelengths:list[float], positions:list[float]) -> None:
        self.m:float = None
        self.c:float = None
        self.calibrate(np.asarray(wavelengths), np.asarray(positions))
    
    def _line(self, x:float, m:float, c:float) -> float:
        return m*x + c
    
    def calibrate(self, wavelengths:np.ndarray, positions:np.ndarray) -> None:
        self.m, self.c = np.polyfit(wavelengths, positions, 1)
        
    def position(self, wavelength:float) -> float:
        return self._line(wavelength, self.m, self.c)