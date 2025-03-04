import os
import subprocess
import sys
import time
# import psutil  # Add this import to check for running processes

def run_lint(top_module, show_gui=False, reload=False):
    # Get current directory
    current_dir = os.getcwd()
    current_dir = current_dir.replace("\\", "/")  # Ensure forward slashes for compatibility

    # Create the lint directory if it doesn't exist
    lint_dir = os.path.join(current_dir, "lint", top_module)
    lint_dir = lint_dir.replace("\\", "/")  # Ensure forward slashes for compatibility
    os.makedirs(lint_dir, exist_ok=True)

    # Find all .v files in the directory
    verilog_files = [f for f in os.listdir(current_dir) if f.endswith(".v")]
    
    if not verilog_files:
        print("No Verilog files found in the current directory.")
        sys.exit(1)
    
    # Format file paths
    verilog_paths = " ".join([os.path.join(current_dir, f) for f in verilog_files])
    verilog_paths = verilog_paths.replace("\\", "/")  # Ensure forward slashes for compatibility

    # Define the TCL commands dynamically
    if reload:
        tcl_script = f"""
        vlog {verilog_paths} -work work
        lint methodology soc -goal start
        configure output directory {lint_dir}
        clear directives
        lint methodology soc -goal start
        lint run -d {top_module} -L work
        clear directives
        """
    else:
        tcl_script = f"""
        configure output directory {lint_dir}
        clear settings -lib
        configure output directory {lint_dir}
        clear directives
        vlib work
        vmap work work
        vlog {verilog_paths} -work work
        lint methodology soc -goal start
        configure output directory {lint_dir}
        clear directives
        lint methodology soc -goal start
        lint run -d {top_module} -L work
        clear directives
        """
    
    # Change directory to lint
    os.chdir(lint_dir)

    # Run the command using subprocess and stream output
    process = subprocess.Popen(
        ["qverify", "-c", "-do", tcl_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Stream output in real-time
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
    
    process.stdout.close()
    process.wait()
    
    if process.returncode != 0:
        print("Linting process failed.")
        sys.exit(1)
    
    # If GUI flag is set, launch the GUI
    print(os.path.join(lint_dir, "lint.db"))
    if show_gui:
        time.sleep(1)
        subprocess.run(["qverify", "-idegui", os.path.join(lint_dir, "lint.db")], check=True)

        # gui_opened = False
        # while not gui_opened:
        #     try:
        #         subprocess.run(["qverify", "-idegui", os.path.join(lint_dir, "lint.db")], check=True)
        #         time.sleep(10)  # Wait for the GUI to open
        #         # Check if the GUI process is running
        #         for proc in psutil.process_iter(['pid', 'name']):
        #             print(proc.info['name'])
        #             if proc.info['name'] == 'qverify.exe':  # Adjust the process name if needed
        #                 print("GUI opened successfully.")
        #                 gui_opened = True
        #                 break
        #         if not gui_opened:
        #             print("GUI did not open, retrying...")
        #     except subprocess.CalledProcessError:
        #         print("Failed to open GUI, retrying...")
        #         time.sleep(2)  # Wait before retrying

if __name__ == "__main__":
    # Ensure at least one argument is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <top_module> [-gui] [-r]")
        sys.exit(1)
    
    top_module = sys.argv[1]
    show_gui = "-gui" in sys.argv
    reload = "-r" in sys.argv
    
    run_lint(top_module, show_gui, reload)
