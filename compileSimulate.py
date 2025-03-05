import os
import subprocess
import time
import argparse

# Argument Parser
parser = argparse.ArgumentParser(description="Run ModelSim simulation and view waveforms with GTKWave.")
parser.add_argument("top_level_tb", help="Top-level testbench module name")
parser.add_argument("--show_waveform", action="store_true", help="Show waveform after simulation")
parser.add_argument("--force_flag", action="store_true", help="Force waveform display even if errors occur")
args = parser.parse_args()

# Extract arguments
TOP_LEVEL_TB = args.top_level_tb
SHOW_WAVEFORM = args.show_waveform
FORCE_WAVE = args.force_flag

# Configuration
SIM_DIR = os.path.join(os.getcwd(), "sim", TOP_LEVEL_TB)
LOG_FILE = os.path.join(SIM_DIR, "simulation_log.txt")
VCD_FILE = os.path.join(SIM_DIR, "simulation.vcd")
SIM_DO_FILE = os.path.join(SIM_DIR, "simulate.do")

# ANSI escape sequences for colored output
RED, GREEN, RESET = "\033[31m", "\033[32m", "\033[0m"

# Ensure the simulation directory exists
os.makedirs(SIM_DIR, exist_ok=True)
os.chdir(SIM_DIR)


def run_command(command, description, check=True):
    """Execute a shell command and stream output in real-time."""
    print(f"\n{description}...")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    output = []
    for line in iter(process.stdout.readline, ""):
        formatted_line = line.replace("Passed", f"{GREEN}Passed{RESET}").replace("Failed", f"{RED}Failed{RESET}")
        output.append(line)
        print(formatted_line, end="")

    process.stdout.close()
    process.wait()

    if check and process.returncode != 0:
        print(f"{RED}Error: {description} failed.{RESET}\n{process.stderr.read()}")
        exit(1)

    return "".join(output)


def generate_do_file(filename, commands):
    """Generate a ModelSim DO file with given commands."""
    with open(filename, "w") as f:
        f.write("\n".join(commands))


def setup_simulation():
    """Prepare the ModelSim environment."""
    if not os.path.exists("work"):
        run_command("vlib work", "Creating ModelSim work library")

    # Check for .sv files
    sv_files_exist = any(f.endswith('.sv') for f in os.listdir('../../'))

    # Compile command
    compile_command = "vlog -work work +acc ../../*.v"
    if sv_files_exist:
        compile_command += " ../../*.sv"

    run_command(compile_command, "Compiling Verilog files")


def run_simulation():
    """Run ModelSim simulation and analyze results."""
    # Generate DO files
    generate_do_file(SIM_DO_FILE, [
        "vcd file simulation.vcd",
        "vcd add -r /*",
        "run -all",
        "vcd flush",
        "quit",
    ])
    
    generate_do_file(f"{TOP_LEVEL_TB}.do", [
        "vlib work",
        "vlog ../*.v",
        f"vsim -voptargs=+acc work.{TOP_LEVEL_TB}",
        "add wave *",
        "run -all",
    ])

    # Run simulation
    sim_output = run_command(f"vsim -c -do {SIM_DO_FILE} -l {LOG_FILE} work.{TOP_LEVEL_TB} -voptargs=+acc",
                             f"Simulating {TOP_LEVEL_TB}")

    # Count errors and check log file
    error_count = sim_output.count("Failed")
    error_color = RED if error_count > 0 else GREEN
    print(f"Simulation Errors: {error_color}{error_count}{RESET}")

    if "Failed" in sim_output and not FORCE_WAVE:
        print(f"{RED}Simulation FAILED.{RESET} Waveform will not be displayed.")
        exit(1)

    print(f"{GREEN}Simulation PASSED.{RESET} Proceeding to waveform display...")


def open_waveform():
    """Open GTKWave if waveform viewing is enabled."""
    if SHOW_WAVEFORM:
        if os.path.exists(VCD_FILE):
            print("\nOpening GTKWave to view waveforms...")
            subprocess.Popen(["gtkwave", VCD_FILE])
            time.sleep(4)  # Allow GTKWave to launch
        else:
            print(f"{RED}Error: VCD file not found.{RESET} Cannot open GTKWave.")


if __name__ == "__main__":
    setup_simulation()
    run_simulation()
    open_waveform()
    print("\nSimulation completed successfully!")