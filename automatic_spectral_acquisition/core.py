import logging 
import os

from rich import print
import pyinputplus as pyin

from automatic_spectral_acquisition.arduino import Arduino
from automatic_spectral_acquisition.oscilloscope import Oscilloscope
from automatic_spectral_acquisition.file_manager import FileManager
from automatic_spectral_acquisition.config import ConfigHandler
from automatic_spectral_acquisition.constants import *
from automatic_spectral_acquisition.helper import error_message, info_message


class Core:
    ################################################## not complete ##################################################
    def __init__(self,
                 output_directory:str=OUTPUT_DIRECTORY, 
                 output_file:str=OUTPUT_FILE,
                 temp_directory:str=TEMP_DIRECTORY,
                 log_file:str=LOG_FILE,
                 output_header:list[str]=['wavelength(nm)', 'voltage(mV)', 'uncertainty(mV)'],
                 arduino_port:str|None=None,
                 oscilloscope_port:str|None=None,
                 m:float|None=None,
                 c:float|None=None,
                 wavelengths:list[float]=None,
                 positions:list[float]=None) -> None:

        self.file_manager = FileManager(output_directory, output_file, temp_directory, log_file, output_header)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=self.file_manager.log_file_directory,
                            filemode='w')
        
        self.config_handler = ConfigHandler(arduino_port, oscilloscope_port, m, c, wavelengths, positions)
        
    ################################################## not complete ##################################################
    
    
    @staticmethod
    def check_parameters_spectrum(start: float, end: float, step: float, number_of_measurements: int) -> None:
        """Check if the parameters for spectral acquisition are valid.

        Args:
            start (float): The starting wavelength.
            end (float): The ending wavelength.
            step (float): The step size between measurements.
            number_of_measurements (int): The number of measurements to take for each wavelength.

        Raises:
            TypeError: If any of the parameters are not of the expected type.
            ValueError: If any of the parameters are invalid.
        """
        # check type of parameters
        if not isinstance(start, (int, float)):
            error_message('TypeError', 'Start wavelength must be a number.')
        if not isinstance(end, (int, float)):
            error_message('TypeError', 'End wavelength must be a number.')
        if not isinstance(step, (int, float)):
            error_message('TypeError', 'Step must be a number.')
        if not isinstance(number_of_measurements, int):
            error_message('TypeError', 'Number of measurements must be an integer.')
        
        # check if the wavelength parameters are valid
        if start < WAVELENGTH_MIN:
            error_message('ValueError', f'Start wavelength must be greater than {WAVELENGTH_MIN}.')
        if end > WAVELENGTH_MAX:
            error_message('ValueError', f'End wavelength must be less than {WAVELENGTH_MAX}.')
        if start >= end:
            error_message('ValueError', 'Start wavelength must be less than end wavelength.')
        if step <= 0:
            error_message('ValueError', 'Step must be greater than 0.')
        if (end - start) < step:
            error_message('ValueError', 'Step must be less than the difference between start and end wavelength.')
        
        # check if the number of measurements is valid
        if number_of_measurements <= 0:
            error_message('ValueError', 'Number of measurements must be greater than 0.')


    @staticmethod
    def check_parameters_single(wavelength: float, number_of_measurements: int) -> None:
        """Check if the parameters for a single measurement are valid.

        Args:
            wavelength (float): The wavelength to measure.
            number_of_measurements (int): The number of measurements to take.

        Raises:
            TypeError: If any of the parameters are not of the expected type.
            ValueError: If any of the parameters are invalid.
        """
        # check type of parameters
        if not isinstance(wavelength, (int, float)):
            error_message('TypeError', 'Wavelength must be a number.')
        if not isinstance(number_of_measurements, int):
            error_message('TypeError', 'Number of measurements must be an integer.')
        
        # check if the wavelength is valid
        if wavelength < WAVELENGTH_MIN:
            error_message('ValueError', f'Wavelength must be greater than {WAVELENGTH_MIN}.')
        if wavelength > WAVELENGTH_MAX:
            error_message('ValueError', f'Wavelength must be less than {WAVELENGTH_MAX}.')
        
        # check if the number of measurements is valid
        if number_of_measurements <= 0:
            error_message('ValueError', 'Number of measurements must be greater than 0.')


    @staticmethod
    def create_wavelengths(start: float, end: float, step: float) -> None:
        """Create a list of wavelengths.

        Args:
            start (float): The starting wavelength.
            end (float): The ending wavelength.
            step (float): The step size between wavelengths.

        Raises:
            ValueError: If the step size is smaller than 0.

        Returns:
            list: A list of wavelengths.
        """
        
        if step <= 0:
            error_message('ValueError', 'Step must be greater than 0.')
        
        wavelengths = []
        current_wavelength = start
        while current_wavelength <= end:
            wavelengths.append(current_wavelength)
            current_wavelength += step
        return wavelengths


    def perform_measurement(self, 
                            wavelength:float, 
                            number_of_measurements:int=DEFAULT_NUMBER_OF_MEASUREMENTS) -> None:
        logging.info(f'Performing measurement at wavelength {wavelength:.2f}nm {number_of_measurements} times.')
        print('performing measurement - not implemented')
        # arduino.change_wavelength()
        # y, yerr = oscilloscope.take_measurement()
        # file_manager.add_buffer([wl, y, terr])
    
    
    def connect_arduino(self) -> None:
        print('Connect Arduino - not implemented')
        
        
    def connect_oscilloscope(self) -> None:
        print('Connect Oscilloscope - not implemented')
        

    def record_spectrum(self, 
                        start:float, 
                        end:float, 
                        step:float, 
                        number_of_measurements:int=DEFAULT_NUMBER_OF_MEASUREMENTS) -> None:
        """Perform spectral acquisition.

        Args:
            start (float): The starting wavelength.
            end (float): The ending wavelength.
            step (float): The step size between measurements.
            number_of_measurements (int, optional): The number of measurements to take for each wavelength. Defaults to DEFAULT_NUMBER_OF_MEASUREMENTS.
        """
        self.check_parameters_spectrum(start, end, step, number_of_measurements)
        wavelengths = self.create_wavelengths(start, end, step)
        for wl in wavelengths:
            self.perform_measurement(wl, number_of_measurements)
        self.file_manager.save_buffer()

    def get_arduino_port(self) -> str:
        ports = self.config_handler.list_serial_ports()
        
        if len(ports) == 0:
            error_message('Error', 'No port was detected.')
            
        arduino_port = pyin.inputMenu(prompt='Select the Arduino port:\n', 
                                      choices=[i.description for i in ports]+['Exit',], 
                                      numbered=True)
        
        if arduino_port == 'Exit':
            info_message('Configuration not saved.', 'Exit')
            exit()
        
        for i in ports:
            if arduino_port == i.description:
                arduino_port = i.name
                break
        
        if arduino_port is None:
            error_message('Error', 'Port not valid.')
            
        return arduino_port
    
    def get_oscilloscope_port(self) -> str:
        instruments = self.config_handler.list_pyvisa_instruments()
        if len(instruments) == 0:
            error_message('Error', 'No instrument was detected.')

        oscilloscope_port = pyin.inputMenu(prompt='Select the oscilloscope port:\n', 
                                           choices=instruments+('Exit',), 
                                           numbered=True)
        
        if oscilloscope_port == 'Exit':
            info_message('Configuration not saved.', 'Exit')
            exit()
            
        return oscilloscope_port

########################### cli commands ###########################
        
    def cli_record_single(self, 
                      wavelength:float,
                      number_of_measurements:int=DEFAULT_NUMBER_OF_MEASUREMENTS) -> None:
        """Perform a single measurement.

        Args:
            wavelength (float): The wavelength to measure.
            number_of_measurements (int, optional): The number of measurements to take. Defaults to DEFAULT_NUMBER_OF_MEASUREMENTS.
        """
        self.check_parameters_single(wavelength, number_of_measurements)
        self.perform_measurement(wavelength, number_of_measurements)
        self.file_manager.save_buffer()
    
    
    def cli_config_create(self) -> None:
        # get arduino port
        if IGNORE_CONNECTIONS:
            arduino_port = pyin.inputMenu(prompt='Select the Arduino port:\n', 
                                          choices=['Fake port Arduino', 'Exit'], 
                                          numbered=True)
            if arduino_port == 'Exit':
                info_message('Configuration not saved.', 'Exit')
                exit()
        else:
            arduino_port = self.get_arduino_port()
            
        # get oscilloscope port
        if IGNORE_CONNECTIONS:
            oscilloscope_port = pyin.inputMenu(prompt='Select the oscilloscope port:\n', 
                                          choices=['Fake port oscilloscope', 'Exit'], 
                                          numbered=True)
            if oscilloscope_port == 'Exit':
                info_message('Configuration not saved.', 'Exit')
                exit()
        else:
            oscilloscope_port = self.get_oscilloscope_port()

        # create config handler        
        self.config_handler = ConfigHandler(arduino_port=arduino_port,
                                            oscilloscope_port=oscilloscope_port)
        
        # save config hanfler
        self.config_handler.save_config()
        
        # calibrate
        self.cli_config_calibrate()
        
    
    def cli_config_delete(self) -> None:
        if not self.config_handler.check_config_exists():
            info_message('No configuration file found.', 'Information')
            return
        os.remove(f'{TEMP_DIRECTORY}/{CONFIG_FILE}')
        info_message('Configuration file deleted.', 'Information')
        

    def cli_config_list(self) -> None:
        if not self.config_handler.check_config_exists():
            info_message('No configuration file found.', 'Information')
            return
        self.config_handler.load_config()
        print(self.config_handler)
        
        
    def cli_config_calibrate(self) -> None:
        if self.config_handler.check_config_exists():
            self.config_handler.load_config()
        else:
            error_message('Error', 'No configuration file found. Use "spectral config create".')

        print('Calibrate - not implemented')
        
        self.config_handler.config.m = 1
        self.config_handler.config.c = 0
        
        self.config_handler.save_config()
    
    def cli_initialize(self) -> None: # deals with connections and basic setup 
        print('\nInitialize - not implemented')
        
        if self.config_handler.check_config_exists():
            self.config_handler.load_config()
        else:
            self.cli_config_create()
            self.config_handler.save_config()
        
        self.connect_arduino()
        self.connect_oscilloscope()
        
        print('End Initialize\n')
        
        
    def cli_finalize(self) -> None:
        # close connections
        # go to known position on arduino
        print('Finalize - not implemented')