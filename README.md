# Automatic spectral acquisition

Python command line interface for the automatic data acquisition of spectral data. Connects to an Arduino running a custom program and to an oscilloscope. 


## Experimental setup

An Arduino running the code on `arduino_code.ino` ([GitHub repository](https://github.com/HugoG16/automatic-spectral-acquisition)) is connected to a stepper motor controller (using a DVR8825 breakout board driver). The stepper motor is connected to a manual monochromator with a timing belt and two gears.
For the detection, a PMT is connected to an oscilloscope **or** an ADC (MCP3421).
All components can then be controlled using this CLI.

Experimental setup when using the oscilloscope:
<p align="center">
<img src="https://github.com/HugoG16/automatic-spectral-acquisition/blob/main/images/setup_schematic.png?raw=true)" width=60%>
</p>

Experimental setup when using the ADC:
<p align="center">
<img src="https://github.com/HugoG16/automatic-spectral-acquisition/blob/main/images/setup_schematic_adc.png?raw=true)" width=60%>
</p>

The diagram for the stepper motor controller is shown next. 

<p align="center">
<img src="https://github.com/HugoG16/automatic-spectral-acquisition/blob/main/images/circuit_diagram.png?raw=true)" width=60%>
</p>

The diagram for the ADC board is:

<p align="center">
<img src="https://github.com/HugoG16/automatic-spectral-acquisition/blob/main/images/circuit_diagram_adc.png?raw=true)" width=60%>
</p>

## Installation

Install using
```
pip install automatic-spectral-acquisition
```

## Calibration process

An initial calibration is necessary for setting the `DEFAULT_POSITION` (default=0) and `CALIBRATION_POSITIONS` in `automatic_spectral_acquisition\constants.py`. This calibration has to be done manually for now, and requires the user to choose a set of points that will be used for further calibrations:
 1. Define a default position and a default wavelength. Ideally `DEFAULT_POSITION=0` and a wavelength in the middle of the available range, e.g., 650 nm.
 2. Select a set of wavelengths (e.g.: [350, 500, 650, 800, 950] nm)
 3. Manually set the monochromator to the default wavelength and start the Arduino code.
 3. Find the associated position by trial and error with `spectral moveto <position>`. Use these values to populate `CALIBRATION_POSITIONS`.

As long as the following measurements conclude successfully, redefining these constants won't be necessary. Even if there is some problem and the motor doesn't return to the default position, if `DEFAULT_POSITION=0`, the monochromator can be manually set to the default wavelength associated with the default position to return to normal functionality.

After that, the calibration process can be performed using, e.g., `spectral config calibrate`. The motor will be moved to the set positions and the user will be asked to input the current wavelength value. 

At the end of a measurement, the motor will return to the default position to guarantee the correct behaviour of further measurements.

The calibration parameters are saved to a file and can be reused for every measurement. However, it is recommended to recalibrate the system every session.


## Options
The options for the program are contained in the file `automatic_spectral_acquisition\constants.py` and should be edited when necessary.
You can select whether you are using an oscilloscope or the ADC.


## How to use

To call the program, use the command `spectral`.
To get help using the CLI, use the command `spectral --help` or `spectral <subcommand> --help`.

To create a configuration file, use
```
spectal config create
```
You will be asked to select the serial ports for the Arduino and oscilloscope, as well as, to calibrate the stepper motor.

If a configuration file already exists, you can choose to just re-calibrate the stepper motor using
```
spectral config calibrate
```

You can see the current configuration using
```
spectral config show
```
Or delete it using
```
spectral config delete
```

To record a spectrum use
```
spectral spectrum <start> <end> <step> [options]
``` 
- `<start>` is the wavelength of the start of the spectrum 
- `<end>` is the wavelength of the end of the spectrum 
- `<step>` is the space between measurements

`[options]` can contain:
- `-n <number of measurements>` is used to select how many measurements are taken and averaged for each wavelength
- `-f <name of output file>` is used to change the name of the output file
- `-p` if this options is present, the spectrum will be plotted at the end of acquisition

You can also take a single measurement using
```
spectral single <wavelength> [options]
``` 

`[options]` can contain:
- `-n <number of measurements>` is used to select how many measurements are taken and averaged for each wavelength
- `-f <name of output file>` is used to change the name of the output file
- `-p` if this options is present, the values measured will be printed on the terminal

Use
```
spectral live <wavelength> [options]
```
To perform continuous measurements that are printed on the screen.

`[options]` can contain:
- `-d <delay>` changes the delay (in seconds) between measurements.
