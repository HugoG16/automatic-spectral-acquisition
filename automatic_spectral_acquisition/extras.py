import matplotlib.pyplot as plt
import numpy as np

from automatic_spectral_acquisition.file_manager import FileManager


def plot_spectrum(display:bool=True, 
                  file_name:str='plot.png', 
                  dpi:int=300) -> None:
    """Plot recorded spectrum. Assumes DEFAULT_HEADER structure!

    Args:
        display (bool, optional): Whether to display the plot. Defaults to True. If false image will be saved instead.
        file_name (str, optional): The name of the output file. Defaults to 'plot.png'.
        dpi (int, optional): The resolution of the output file. Defaults to 300.
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