import os
import subprocess
import time
import argparse
import itertools
import pygetwindow as gw
import pyautogui

# Configuration
# GTKWAVE_PATH = r"C:\\sc\\work"  # Path to GTKWave executable directory
WORK_DIR = os.getcwd()  # Use the current directory as the working directory

LOG_FILE = "simulation_log.txt"
VCD_FILE = "simulation.vcd"  # VCD file for waveform
SIM_DO_FILE = "simulate.do"  # Do file for simulation

# ANSI escape sequences for coloring text (works in most terminals)
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Run ModelSim simulation and view waveforms with GTKWave."
)
parser.add_argument("top_level_tb", help="Top-level testbench module name")
parser.add_argument(
    "--show_waveform",
    action="store_true",
    help="Show waveform at the end of the simulation",
)
args = parser.parse_args()

TOP_LEVEL_TB = args.top_level_tb  # Set the module name from command line argument
SHOW_WAVEFORM = (
    args.show_waveform
)  # Set the show waveform option from command line argument

# Environment setup for GTKWave (add GTKWAVE_PATH to PATH)
# os.environ["PATH"] += os.pathsep + GTKWAVE_PATH

# Change to the working directory
os.chdir(WORK_DIR)

# Function to run simulation with a loading spinner
def run_simulation_with_spinner(command, description):
    print(f"\n{description}...")

    # Start the simulation process
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Spinner animation
    spinner = itertools.cycle(["-", "\\", "|", "/"])

    while process.poll() is None:  # While the process is running
        print(f"\rSimulating... {next(spinner)}", end="", flush=True)
        time.sleep(0.1)  # Update interval

    # Capture and display the output
    stdout, stderr = process.communicate()

    # Color the "Passed" and "Failed" text in the simulation output
    colored_output = stdout.replace("Passed", f"{GREEN}Passed{RESET}").replace(
        "Failed", f"{RED}Failed{RESET}"
    )

    print("\n\nSimulation Output:")
    print(colored_output)  # Print the colored simulation output to the terminal

    # Check for errors
    if process.returncode != 0:
        print(f"Error: {stderr}")
        exit(1)

    return stdout


# Main script execution
if __name__ == "__main__":

    # Step 1: Create a library directory for ModelSim
    if not os.path.exists("work"):
        print("\nCreating work library...")
        subprocess.run(f"vlib work", shell=True, check=True)

    # Step 2: Compile the design with +acc option
    print("\nCompiling Verilog files...")
    compile_command = f"vlog -work work +acc *.v"
    subprocess.run(compile_command, shell=True, check=True)

    # Step 3: Generate simulation do file with VCD commands if SHOW_WAVEFORM is True
    if SHOW_WAVEFORM:
        simulation_commands = [
            f"vcd file {VCD_FILE}",
            "vcd add -r /*",  # Recursive addition of all signals
            "run -all",
            "vcd flush",
            "quit",
        ]
    else:
        simulation_commands = ["run -all", "quit"]
    simulation_command_str = "; ".join(simulation_commands)

    # Step 4: Simulate the design with VCD generation
    simulation_command = f'vsim -c -do "{simulation_command_str}" -l {LOG_FILE} work.{TOP_LEVEL_TB} -voptargs=+acc'

    simulation_output = run_simulation_with_spinner(
        simulation_command, f"Simulating the module: {TOP_LEVEL_TB}..."
    )

    # Step 5: Count the number of "Failed" occurrences in the simulation output
    error_count = simulation_output.count("Failed")
    error_color = RED if error_count > 0 else GREEN
    print(f"Simulation Errors: {error_color}{error_count}{RESET}")

    # Step 6: Check for "Failed" in simulation output
    with open(LOG_FILE, "r") as log_file:
        log_content = log_file.read()

    if "Failed" in log_content:
        print(f"Simulation {RED}FAILED{RESET}. Not generating or displaying waveforms.")
        exit(1)
    else:
        print(f"Simulation {GREEN}PASSED{RESET}. Proceeding to view waveforms.")

    # Step 7: Open GTKWave to view waveforms if SHOW_WAVEFORM is True
    if SHOW_WAVEFORM and os.path.exists(VCD_FILE):
        print("\nOpening GTKWave to view waveforms...")
        gtkwave_process = subprocess.Popen(["gtkwave", VCD_FILE])
        time.sleep(4)  # Wait for GTKWave to open
        # os.send_keys('{TAB}')

        # Simulate pressing the Tab key
        pyautogui.press('tab')

    elif SHOW_WAVEFORM:
        print(f"VCD file {VCD_FILE} not found. Cannot open GTKWave.")

    print("\nSimulation and waveform generation completed successfully!")
