import serial
from time import sleep

import pyinputplus as pyin
from statemachine import State, StateMachine


class ArduinoStateMachine(StateMachine):
    # Define states
    start = State('Start', initial=True)
    connect = State('Connect')
    measure = State('Measure')
    close = State('Close', final=True)
    
    # def on_connect(self):
    #     print('Connect Arduino - not implemented')
    #     self.connect_arduino()

    # Define transitions
    connecting = start.to(connect)
    measuring = connect.to(measure)
    closing = measure.to(close)
    
    cycle = connecting | measuring | closing
    
    # Define state actions
    def on_enter_start(self):
        print('State: Start 🐸')
    
    def on_enter_connect(self):
        print('State: Connect 🐸')
    
    def on_enter_measure(self):
        print('State: Measure 🐸')
        
    def on_enter_close(self):
        print('State: Close 🐸')
    
    
    # Define transition actions
    def on_connecting(self):
        print('conecting.... 🐸')
        
    def on_measuring(self):
        print('measuring.... 🐸')
        
    def on_closing(self):
        print('Closing.... 🐸')
        
    def on_cycle(self):
        if self.current_state == self.start:
            self.on_connecting()
        elif self.current_state == self.connect:
            self.on_measuring()
        elif self.current_state == self.measure:
            self.on_closing()




class Arduino:
    def __init__(self) -> None:
        pass
    
