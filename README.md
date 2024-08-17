# Automatic spectral acquisition
Python interface for the automatic data acquisition of spectral data. Connects to an arduino running a custom program and to an oscilloscope. 


## Arduino and motor controller
The diagram for the controller of the stepper motor is shown next. 

<p align="center">
<img src="https://github.com/HugoG16/automatic-spectral-acquisition/blob/main/images/circuit_diagram.png?raw=true)" width=60%>
</p>

A schematic of the setup:
<p align="center">
<img src="https://github.com/HugoG16/automatic-spectral-acquisition/blob/main/images/setup_schematic.png?raw=true)" width=60%>
</p>


## Calibration process

A initial calibration is necessary for setting the `DEFAULT_POSITION` (default=0) and `CALIBRATION_POSITIONS` in `automatic_spectral_acquisition\constants.py`. This calibration has to be done manually for now, and requires the user to choose a set of points that will be used for further calibrations:
 1. Define a default position and a default wavelength. Ideally `DEFAULT_POSITION=0` and a wavelength in the middle of the available range, e.g., 650 nm.
 2. Choose a set of wavelengths (e.g.: [250, 450, 650, 750, 950] nm)
 3. Manually set the monochromator to the default wavelength and start the Arduino code.
 3. Find the associated position by trial and error. Use this values to populate `CALIBRATION_POSITIONS`.

As long as the following measurements conclude successfully, there won't be necessary to redefine this constants. Even if there is some problem and the motor doesn't return to the default position, if `DEFAULT_POSITION=0`, the monochromator can be manually set to the default wavelength associated with the default position to return to normal functionality.

After that, the calibration process can be performed using, e.g., `spectral config calibrate`. The motor will be moved to the set positions and the user will be asked to input the current wavelength value. 

At the end of a measurement the motor will return to the default position to guarantee the correct behavior of further measurements.

The calibration parameters are saved to a file and can be reused for every measurement. However, it is recommended to recalibrate the system every session.