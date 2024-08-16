import serial
from time import sleep

import pyinputplus as pyin
from statemachine import State, StateMachine
from statemachine.exceptions import TransitionNotAllowed

from automatic_spectral_acquisition.config import ConfigHandler
from automatic_spectral_acquisition.helper import error_message
from automatic_spectral_acquisition.constants import *


class ArduinoStateMachine(StateMachine):
    # Define states
    start = State('Start', initial=True)
    connected = State('Connected') 
    requested = State('Requested') # Requested a change in position
    completed = State('Completed') # Received confirmation by the arduino
    disconnected = State('Disconnected')

    # Define transitions
    connect = start.to(connected) | disconnected.to(connected)
    request = connected.to(requested) | completed.to(requested)
    wait = requested.to.itself()
    complete = requested.to(completed)
    disconnect = completed.to(disconnected)
    
    # Define transition actions
    def on_connect(self, *args, **kwargs):
        if INGORE_CONNECTIONS:
            return
        
        # Check if config_handler is passed
        config_handler:ConfigHandler = kwargs.get('config_handler')
        if not isinstance(config_handler, ConfigHandler):
            error_message('TypeError', 'ConfigHandler object not passed.')

        # Check if arduino port is set
        arduino_port = config_handler.config.arduino_port
        if arduino_port is None:
            error_message('ValueError', 'Arduino port not set.')
        
        # Connect to arduino
        try:
            self.serial = serial.Serial(arduino_port, ARDUINO_BAUDRATE, timeout=ARDUINO_TIMEOUT)
            sleep(2)
        except serial.SerialException:
            error_message('SerialException', f'Could not connect to arduino on port {arduino_port}.')
        
        
    def on_request(self, *args, **kwargs):
        position:float = kwargs.get('position')
        if not isinstance(position, float):
            error_message('TypeError', 'Position not passed.')
        print('sending request.... 🐸')
        
    def on_complete(self, *args, **kwargs):
        print('received confirmation.... 🐸')
        
    def on_disconnect(self, *args, **kwargs):
        print('Disconnecting.... 🐸')
        
    def on_wait(self, *args, **kwargs):
        print('Waiting.... 🐸')
        


class Arduino:
    def __init__(self, config_handler:ConfigHandler) -> None:
        self.config_handler = config_handler
        self.state_machine = ArduinoStateMachine()

    def _send(self, transition:str, *args, **kwargs) -> None:
        try:
            self.state_machine.send(transition, *args, **kwargs)
        except TransitionNotAllowed as e:
            error_message('TransitionNotAllowed', e)
            
    def connect(self) -> None:
        self._send('connect', config_handler=self.config_handler)
        
    def request(self, wavelength:float) -> None:
        self._send('request', position=self.config_handler.position(wavelength))
        
    
