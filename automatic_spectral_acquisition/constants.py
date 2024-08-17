############################# Debug options #############################
DEBUG:bool = False # Changes how exceptions are dealt with.
IGNORE_CONNECTIONS:bool = True # Ignore connections and fakes parts in order to test the program without the hardware.


############################# Arduino connection #############################
ARDUINO_BAUDRATE = 9600 # Baudrate for the arduino
ARDUINO_TIMEOUT = 0.1 # Timeout for the arduino

############################# Oscilloscope settings #############################


############################# Measurements options #############################
DEFAULT_NUMBER_OF_MEASUREMENTS:int = 3 # Default number of measurements to take for take for each wavelength.
WAVELENGTH_MIN:float = 200 # Minimum wavelength that can be measured.
WAVELENGTH_MAX:float = 1050 # Maximum wavelength that can be measured.
DEFAULT_POSITION:float = 0 # Default position for the motor.
CALIBRATION_POSITIONS:list[float] = [-4000 ,-2000 , 0, 2000, 4000] # Wavelengths used for calibration.

############################# File options #############################
OUTPUT_DIRECTORY:str = 'automatic_spectral_acquisition/output' 
TEMP_DIRECTORY:str = 'automatic_spectral_acquisition/temp'
OUTPUT_FILE:str = 'output.csv'
LOG_FILE:str = 'log.txt'
CONFIG_FILE:str = 'config.pkl'

