import csv
import os
from time import localtime, strftime

from automatic_spectral_acquisition.constants import *


class FileManager:
    """Class to manage the output file for the spectral acquisition system.
    """
    def __init__(self, 
                 output_directory:str=OUTPUT_DIRECTORY, 
                 output_file:str=OUTPUT_FILE,
                 temp_directory:str=TEMP_DIRECTORY,
                 log_file:str=LOG_FILE,
                 output_header:list[str]=DEFAULT_HEADER) -> None:
        """Initialize the FileManager class.

        Args:
            output_directory (str, optional): The directory to save the output file. Defaults to OUTPUT_DIRECTORY.
            output_file (str, optional): The name of the output file. Defaults to OUTPUT_FILE. {time} will be replaced by the current time.
            temp_directory (str, optional): The directory to save the temporary file. Defaults to TEMP_DIRECTORY.
            log_file (str, optional): The name of the log file. Defaults to LOG_FILE.
            output_header (list[str], optional): The header for the output file. Defaults to DEFAULT_HEADER.
        """
        self.output_directory = output_directory
        self.temp_directory = temp_directory
        self.output_header = output_header
        
        # Create directories if they do not exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory)
        
        output_file.format(time=strftime(TIME_FORMAT, localtime()))
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
        """Return the buffer."""
        return self.buffer
    
    
    def save_buffer(self) -> None:
        """Saves the buffer to the output file specified in the output_directory attribute."""
        with open(self.output_file_directory, 'w', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(self.output_header)
            writer.writerows(self.buffer)
         
            
    def load_output(self, file:str|None=None) -> list[list[float]]:
        """Load the output file into the buffer.

        Args:
            file (str | None, optional): The path of the output file to load. Defaults to None.

        Returns:
            list[list[float]]: The loaded buffer as a list of lists of floats.
        """
        if file is None:
            file = self.output_file_directory
        
        with open(file, 'r') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            next(reader, None)  # skip the header
            self.buffer = [row for row in reader]