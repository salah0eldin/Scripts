# Scripts

This folder contains various scripts for different purposes, including running simulations and viewing waveforms. Below are the details and usage instructions for the available scripts.

## Files

- `compileSimulate.py`: A Python script to run ModelSim simulations and optionally view waveforms with GTKWave.
- `compileSimulate.bat`: A batch file to execute the `compileSimulate.py` script with appropriate arguments.

## Usage

### compileSimulate.bat

This batch file is used to run the `compileSimulate.py` script. It accepts one or two arguments:

1. **Top-level testbench module name** (required)
2. **`-w`** (optional): If provided, the waveform will be shown at the end of the simulation.

#### Examples

To run the simulation without showing the waveform:
```
compileSimulate.bat top_level_tb_name
```

To run the simulation and show the waveform:
```
compileSimulate.bat top_level_tb_name -w
```

### compileSimulate.py

This Python script runs ModelSim simulations and optionally opens GTKWave to view the generated waveforms.

#### Command-line Arguments

- `top_level_tb`: The top-level testbench module name (required).
- `--show_waveform`: Show waveform at the end of the simulation (optional).

#### Examples

To run the simulation without showing the waveform:
```
python compileSimulate.py top_level_tb_name
```

To run the simulation and show the waveform:
```
python compileSimulate.py top_level_tb_name --show_waveform
```

## Configuration

- **GTKWAVE_PATH**: Path to the GTKWave executable directory (currently commented out in the script).
- **WORK_DIR**: The working directory for the simulation (default is the current directory).
- **LOG_FILE**: The log file for the simulation output.
- **VCD_FILE**: The VCD file for waveform generation.
- **SIM_DO_FILE**: The do file for simulation.

## Notes

- Ensure that ModelSim and GTKWave are installed and properly configured in your system's PATH.
- The scripts use ANSI escape sequences for coloring text, which works in most terminals.

## Future Scripts

This folder will be updated with more scripts in the future. Stay tuned for more functionalities and automation tools.
