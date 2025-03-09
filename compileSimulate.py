import os
import subprocess
import time
import argparse

# Argument Parser
parser = argparse.ArgumentParser(
    description="Run ModelSim simulation, view waveforms with GTKWave, and generate coverage reports."
)
parser.add_argument("top_level_tb", help="Top-level testbench module name")
parser.add_argument(
    "--show_waveform", action="store_true", help="Show waveform after simulation"
)
parser.add_argument(
    "--force_flag",
    action="store_true",
    help="Force waveform display even if errors occur",
)
parser.add_argument(
    "--html_flag",
    action="store_true",
    help="Generate HTML coverage report",
)
args = parser.parse_args()

# Extract arguments
TOP_LEVEL_TB = args.top_level_tb
SHOW_WAVEFORM = args.show_waveform
FORCE_WAVE = args.force_flag
GENERATE_HTML = args.html_flag

# Configuration
SIM_DIR = os.path.join(os.getcwd(), "sim", TOP_LEVEL_TB)
LOG_FILE = os.path.join(SIM_DIR, "simulation_log.txt")
VCD_FILE = os.path.join(SIM_DIR, "simulation.vcd")
SIM_DO_FILE = os.path.join(SIM_DIR, "simulate.do")
# Build a normalized UCDB file path; note that we wrap it in quotes to handle spaces
UCDB_FILE = os.path.join(SIM_DIR, "coverage.ucdb").replace("\\", "/")
UCDB_FILE = '"' + UCDB_FILE + '"'
COVERAGE_REPORT_FILE = os.path.join(SIM_DIR, "coverage_report.txt")

FULL_DO_FILE = os.path.join(SIM_DIR, f"{TOP_LEVEL_TB}.do")

# ANSI escape sequences for colored output
RED, GREEN, RESET = "\033[31m", "\033[32m", "\033[0m"

# Ensure the simulation directory exists and change to it
os.makedirs(SIM_DIR, exist_ok=True)
os.chdir(SIM_DIR)


def run_command(command, description, check=True):
    """Execute a shell command and stream output in real-time."""
    print(f"Running command: {command}")
    print(f"\n{description}...")

    generate_do_file(FULL_DO_FILE, [command])

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )

    output = []
    for line in iter(process.stdout.readline, ""):
        # Replace keywords for improved visibility in the terminal
        formatted_line = line.replace("Passed", f"{GREEN}Passed{RESET}").replace(
            "Failed", f"{RED}Failed{RESET}"
        )
        output.append(line)
        print(formatted_line, end="")

    process.stdout.close()
    process.wait()

    if check and process.returncode != 0:
        print(f"{RED}Error: {description} failed.{RESET}\n{process.stderr.read()}")
        exit(1)

    return "".join(output)


def generate_do_file(filename, commands):
    """Generate a ModelSim DO file with the given commands."""
    with open(filename, "a") as f:
        f.write("\n".join(commands) + "\n")


def setup_simulation():
    """Prepare the ModelSim environment by creating a work library and compiling design files with coverage enabled."""
    lib_command = "vlib work"
    run_command(lib_command, "Creating ModelSim work library")

    # Check for SystemVerilog (.sv) files
    sv_files_exist = any(f.endswith(".sv") for f in os.listdir("../../"))

    # Compile command with coverage options enabled (-cover bcesfx for branch, condition, expression, statement, and toggle coverage)
    compile_command = 'vlog -work work +acc +cover -covercells "../../*.v"'
    if sv_files_exist:
        compile_command += ' "../../*.sv"'

    run_command(compile_command, "Compiling Verilog files")


def run_simulation():
    """Run ModelSim simulation, generate the DO file with module-specific commands, and analyze results."""
    # Generate the DO file that includes VCD setup, simulation run, and coverage saving
    generate_do_file(
        SIM_DO_FILE,
        [
            "vcd file simulation.vcd",
            "vcd add -r /*",
            "run -all",
            "coverage save -onexit coverage.ucdb",
            "quit",
        ],
    )

    # Run simulation with coverage enabled using the generated DO file
    # sim_output = run_command(f"vsim -c -voptargs=+acc -coverage -do \"{SIM_DO_FILE}\" -l \"{LOG_FILE}\" work.{TOP_LEVEL_TB}",
    #                          f"Simulating {TOP_LEVEL_TB}")
    sim_output = run_command(
        f"vsim -c -voptargs=+acc -cover -do simulate.do -l simulation_log.txt work.{TOP_LEVEL_TB}",
        f"Simulating {TOP_LEVEL_TB}",
    )

    generate_do_file(
        FULL_DO_FILE,
        [
            "vcd file simulation.vcd",
            "vcd add -r /*",
            "run -all",
            "coverage save -onexit coverage.ucdb",
            "quit -sim",
        ],
    )
    # Count errors by checking the output for 'Failed'
    error_count = sim_output.count("Failed")
    error_color = RED if error_count > 0 else GREEN
    print(f"Simulation Errors: {error_color}{error_count}{RESET}")

    if "Failed" in sim_output and not FORCE_WAVE:
        print(f"{RED}Simulation FAILED.{RESET} Waveform will not be displayed.")
        exit(1)

    print(f"{GREEN}Simulation PASSED.{RESET} Proceeding to waveform display...")


def generate_coverage_report():
    """Generate a coverage report from the UCDB file using the vcover tool."""
    # Strip quotes from UCDB_FILE for checking file existence
    if os.path.exists(UCDB_FILE.strip('"')):
        print("\nGenerating coverage report...")
        # run_command(f"vcover report -details -file {COVERAGE_REPORT_FILE} {UCDB_FILE}",
        #             "Generating coverage report")
        run_command(
            f"vcover report coverage.ucdb -details -annotate -all -output coverage_report.txt",
            "Generating coverage report",
        )
        print(f"Coverage report generated: {COVERAGE_REPORT_FILE}")
        if GENERATE_HTML:
            print("\nGenerating HTML coverage report...")
            # Generate an HTML coverage report
            run_command(
                f"vcover report -html -output coverage_report.html {UCDB_FILE}",
                "Generating HTML coverage report",
            )
            print("Coverage report generated: coverage_report.html")
    else:
        print(
            f"{RED}Error: UCDB file not found.{RESET} Cannot generate coverage report."
        )


def open_waveform():
    """Open GTKWave to display the waveform if the --show_waveform flag is set."""
    if SHOW_WAVEFORM:
        if os.path.exists(VCD_FILE):
            print("\nOpening GTKWave to view waveforms...")
            subprocess.Popen(["gtkwave", VCD_FILE])
            time.sleep(4)  # Allow GTKWave to launch
        else:
            print(f"{RED}Error: VCD file not found.{RESET} Cannot open GTKWave.")


if __name__ == "__main__":
    with open(FULL_DO_FILE, "w") as f:
        f.write("")
    with open(SIM_DO_FILE, "w") as f:
        f.write("")

    setup_simulation()
    run_simulation()
    generate_coverage_report()
    open_waveform()
    print("\nSimulation completed successfully!")