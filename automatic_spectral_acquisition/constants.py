############################# Debug options #############################
DEBUG:bool = False # Changes how exceptions are dealt with.
IGNORE_CONNECTIONS:bool = False # Ignore connections and fakes parts in order to test the program without the hardware.
IGNORE_REQUESTS:bool = True # Ignore requests.

############################# Arduino connection #############################
ARDUINO_BAUDRATE = 9600 # Baudrate for the arduino
ARDUINO_TIMEOUT = 0.1 # Timeout for the arduino

############################# Arduino commands #############################
GOTO    = "GOTO"     # Send
DONE    = "DONE"     # Receive - completed request
INVALID = "INVALID"  # Receive - invalid request
RUNNING = "RUNNING"  # Receive - motor is moving
STOP    = "STOP"     # Receive - stop button was pressed

############################# Oscilloscope settings #############################


############################# Measurements options #############################
DEFAULT_NUMBER_OF_MEASUREMENTS:int = 3 # Default number of measurements to take for take for each wavelength.
WAVELENGTH_MIN:float = 200 # Minimum wavelength that can be measured.
WAVELENGTH_MAX:float = 1050 # Maximum wavelength that can be measured.
DEFAULT_POSITION:float = 0 # Default position for the motor.
CALIBRATION_POSITIONS:list[float] = [-4000 ,-2000 , 0, 2000, 4000] # Position of wavelengths used for calibration.

############################# File options #############################
OUTPUT_DIRECTORY:str = 'automatic_spectral_acquisition/output' 
TEMP_DIRECTORY:str = 'automatic_spectral_acquisition/temp'
OUTPUT_FILE:str = 'output.csv'
LOG_FILE:str = 'log.txt'
CONFIG_FILE:str = 'config.pkl'
DEFAULT_HEADER:list[str]=['wavelength(nm)', 'voltage(mV)', 'uncertainty(mV)']
