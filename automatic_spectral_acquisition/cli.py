from typer import Typer

from automatic_spectral_acquisition.core import Core
from automatic_spectral_acquisition.constants import *

def create_config_subcommands() -> Typer:
    app = Typer(no_args_is_help=True)

    @app.command()
    def create():
        core = Core()
        core.cli_config_create()
        
    @app.command()
    def delete():
        core = Core()
        core.cli_config_delete()
    
    @app.command()
    def list():
        core = Core()
        core.cli_config_list()
    
    @app.command()
    def calibrate():
        core = Core()
        core.cli_config_calibrate()
    
    return app
    
    
def create_app(app_name:str='Spectral data acquisition') -> Typer:
    app = Typer(name=app_name, add_completion=False, no_args_is_help=True)
   
    @app.command()
    def spectrum(start:float, 
                 end:float, 
                 step:float, 
                 number_of_measurements:int=DEFAULT_NUMBER_OF_MEASUREMENTS):
        core = Core()
        core.cli_initialize()
        core.record_spectrum(start, end, step, number_of_measurements)
        core.cli_finalize()
        
        
    @app.command()
    def single(wavelength:float,
               number_of_measurements:int=DEFAULT_NUMBER_OF_MEASUREMENTS):
        core = Core()
        core.cli_initialize()
        core.cli_record_single(wavelength, number_of_measurements)
        core.cli_finalize()
    
    app.add_typer(create_config_subcommands(), name='config')
    
    
    return app
