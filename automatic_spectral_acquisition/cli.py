from typer import Typer, Argument, Option
from typing_extensions import Annotated

from automatic_spectral_acquisition.core import Core
from automatic_spectral_acquisition.constants import *

def create_config_subcommands() -> Typer:
    app = Typer(no_args_is_help=True, help='Configuration management.')

    @app.command()
    def create():
        """
        Create a new configuration file interactively.
        """
        core = Core()
        core.cli_config_create()
        
    @app.command()
    def delete():
        """
        Deletes the configuration file.
        """
        core = Core()
        core.cli_config_delete()
    
    @app.command()
    def show():
        """
        Show the current configuration.
        """
        core = Core()
        core.cli_config_show()
    
    @app.command()
    def calibrate():
        """
        Updates the calibration in the configuration file.
        """
        core = Core()
        core.cli_config_calibrate()
    
    return app
    
def create_app(app_name:str='Spectral data acquisition') -> Typer:
    app = Typer(name=app_name, add_completion=False, no_args_is_help=True)
   
    @app.command(short_help='Record a spectrum.')
    def spectrum(start:Annotated[float, Argument(help='Start wavelength')],
                 end:Annotated[float, Argument(help='End wavelength')],
                 step:Annotated[float, Argument(help='Step size')],
                 number_of_measurements:Annotated[int, Option('--number_of_measurements', '-n', help='Number of measurements')]=DEFAULT_NUMBER_OF_MEASUREMENTS,
                 plot:Annotated[bool, Option('--plot', help='Plot spectrum afterwards')] = False):
        """
        Record a spectrum.
        If --plot is passed, the spectrum will be plotted after the measurements.
        """
        core = Core()
        core.cli_record_spectrum(start, end, step, number_of_measurements, plot)        
        
    @app.command()
    def single(wavelength:Annotated[float, Argument(help='Wavelength to measure')],
               number_of_measurements:Annotated[int, Option('--number_of_measurements', '-n', help='Number of measurements')]=DEFAULT_NUMBER_OF_MEASUREMENTS):
        """
        Measure a single wavelength.
        """
        core = Core()
        core.cli_record_single(wavelength, number_of_measurements)
    
    app.add_typer(create_config_subcommands(), name='config')
    
    
    return app
