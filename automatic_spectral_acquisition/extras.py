import matplotlib.pyplot as plt
from rich import print

from automatic_spectral_acquisition.file_manager import FileManager

def plot_spectrum(title:str=None):
    """Plot recorded spectrum. Assumes DEFAULT_HEADER structure.

    Args:
        title (str, optional): The title of the plot. Defaults to None.
    """
    file_manager = FileManager()
    
    file_manager.load_output()
    
    buffer = file_manager.get_buffer()
    
    print(buffer)
    
    