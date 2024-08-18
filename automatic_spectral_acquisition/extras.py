import matplotlib.pyplot as plt
import numpy as np

from automatic_spectral_acquisition.file_manager import FileManager

def plot_spectrum(display:bool=True, 
                  file_name:str='plot.png', 
                  dpi:int=300) -> None:
    """Plot recorded spectrum. Assumes DEFAULT_HEADER structure.

    Args:
        title (str, optional): The title of the plot. Defaults to None.
    """
    file_manager = FileManager()
    file_manager.load_output()
    data = np.asarray(file_manager.get_buffer())
    data = np.transpose(data)
    
    plt.errorbar(data[0], data[1], yerr=data[2], fmt='o')
    
    plt.xlabel(file_manager.output_header[0])
    plt.ylabel(file_manager.output_header[1])
    
    plt.tight_layout()
    
    if display:
        plt.show()
    else:
        plt.savefig(f'{file_manager.temp_directory}/{file_name}', dpi=dpi)