import numpy as np


class Calibration:
    def __init__(self, 
                 wavelengths:list[float]|None=None, 
                 positions:list[float]|None=None,
                 m:float|None=None,
                 c:float|None=None) -> None:
        
        self.m:float = m
        self.c:float = c
        
        if wavelengths is not None and positions is not None:
            self.calibrate(np.asarray(wavelengths), np.asarray(positions))
    
    def _line(self, x:float, m:float, c:float) -> float:
        return m*x + c
    
    def calibrate(self, wavelengths:np.ndarray, positions:np.ndarray) -> None:
        """Calculates the parameters m and c for the calibration.
        position = m*wavelength + c

        Args:
            wavelengths (np.ndarray): Array of wavelengths.
            positions (np.ndarray): Array of positions.
        """
        self.m, self.c = np.polyfit(wavelengths, positions, 1)
        
    def position(self, wavelength:float) -> float:
        return self._line(wavelength, self.m, self.c)