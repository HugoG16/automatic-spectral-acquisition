import csv

from automatic_spectral_acquisition.constants import *

class FileManager:
    """Class to manage the output file for the spectral acquisition system.
    """
    def __init__(self, 
                 output_directory:str=OUTPUT_DIRECTORY, 
                 output_file:str=OUTPUT_FILE,
                 temp_directory:str=TEMP_DIRECTORY,
                 log_file:str=LOG_FILE,
                 output_header:list[str]=['wavelength(nm)', 'voltage(mV)', 'uncertainty(mV)']) -> None:
        """Initialize the FileManager class.

        Args:
            output_directory (str, optional): The directory to save the output file. Defaults to OUTPUT_DIRECTORY.
            temp_directory (str, optional): The directory to save the temporary file. Defaults to TEMP_DIRECTORY.
            output_header (list[str], optional): The header for the output file. Defaults to ['wavelength(nm)', 'voltage(mV)', 'uncertainty(mV)'].
        """
        self.output_directory = output_directory
        self.temp_directory = temp_directory
        self.output_header = output_header
        
        self.output_file_directory = f'{output_directory}/{output_file}'
        self.log_file_directory = f'{temp_directory}/{log_file}'
        
        self.buffer : list[list[float|None]] = []
        
    def add_buffer(self, measurement:list[float|None]) -> None:
        """Add a measurement to the buffer.

        Args:
            measurement (list[float|None]): The measurement to add to the buffer.
        """
        self.buffer.append(measurement)
        
    def get_buffer(self) -> list[float]:
        return self.buffer
    
    def save_buffer(self) -> None:
        """This method saves the buffer to the output file specified in the output_directory attribute.
        """
        with open(self.output_file_directory, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.output_header)
            writer.writerows(self.buffer)