# Scripts

This folder contains various scripts for different purposes, including running simulations, viewing waveforms, and linting Verilog files. Below are the details and usage instructions for the available scripts.

## Files

- `compileSimulate.py`: A Python script to run ModelSim simulations and optionally view waveforms with GTKWave.
- `compileSimulate.bat`: A batch file to execute the `compileSimulate.py` script with appropriate arguments.
- `Qlint.py`: A Python script to run linting on Verilog files using Qverify.
- `qlint.bat`: A batch file to execute the `Qlint.py` script with appropriate arguments.

## Usage

### compileSimulate.bat

This batch file is used to run the `compileSimulate.py` script. It accepts one or more arguments:

1. **Top-level testbench module name** (required)
2. **`-w`** (optional): If provided, the waveform will be shown at the end of the simulation.
3. **`-f`** (optional): If provided, forces the waveform display even if errors occur.

#### Examples

To run the simulation without showing the waveform:
```
compileSimulate.bat top_level_tb_name
```

To run the simulation and show the waveform:
```
compileSimulate.bat top_level_tb_name -w
```

To run the simulation and force the waveform display even if errors occur:
```
compileSimulate.bat top_level_tb_name -f
```

### compileSimulate.py

This Python script runs ModelSim simulations and optionally opens GTKWave to view the generated waveforms.

#### Command-line Arguments

- `top_level_tb`: The top-level testbench module name (required).
- `--show_waveform`: Show waveform at the end of the simulation (optional).
- `--force_flag`: Force waveform display even if errors occur (optional).

#### Examples

To run the simulation without showing the waveform:
```
python compileSimulate.py top_level_tb_name
```

To run the simulation and show the waveform:
```
python compileSimulate.py top_level_tb_name --show_waveform
```

To run the simulation and force the waveform display even if errors occur:
```
python compileSimulate.py top_level_tb_name --force_flag
```

### qlint.bat

This batch file is used to run the `Qlint.py` script. It accepts one or more arguments:

1. **Top-level module name** (required)
2. **`-gui`** (optional): If provided, the GUI will be shown after linting.
3. **`-r`** (optional): If provided, the linting environment will be reloaded.

#### Examples

To run linting without showing the GUI:
```
qlint.bat top_module_name
```

To run linting and show the GUI:
```
qlint.bat top_module_name -gui
```

To run linting with reloading the environment:
```
qlint.bat top_module_name -r
```

### Qlint.py

This Python script runs linting on Verilog files using Qverify.

#### Command-line Arguments

- `top_module`: The top-level module name (required).
- `-gui`: Show the GUI after linting (optional).
- `-r`: Reload the linting environment (optional).

#### Examples

To run linting without showing the GUI:
```
python Qlint.py top_module_name
```

To run linting and show the GUI:
```
python Qlint.py top_module_name -gui
```

To run linting with reloading the environment:
```
python Qlint.py top_module_name -r
```

## Configuration

- **GTKWAVE_PATH**: Path to the GTKWave executable directory (currently commented out in the script).
- **WORK_DIR**: The working directory for the simulation (default is the current directory).
- **LOG_FILE**: The log file for the simulation output.
- **VCD_FILE**: The VCD file for waveform generation.
- **SIM_DO_FILE**: The do file for simulation.

## Notes

- Ensure that ModelSim, GTKWave, and Qverify are installed and properly configured in your system's PATH.
- The scripts use ANSI escape sequences for coloring text, which works in most terminals.

## Future Scripts

This folder will be updated with more scripts in the future. Stay tuned for more functionalities and automation tools.
