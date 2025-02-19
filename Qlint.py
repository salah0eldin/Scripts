import os
import subprocess
import sys

def run_lint(top_module, show_gui=False, reload=False):
    # Get current directory
    current_dir = os.getcwd()
    current_dir = current_dir.replace("\\", "/")  # Ensure forward slashes for compatibility

    # Create the lint directory if it doesn't exist
    lint_dir = os.path.join(current_dir, "lint")
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
    if show_gui:
        subprocess.run(["qverify", "-idegui", "lint.db"], check=True)

if __name__ == "__main__":
    # Ensure at least one argument is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <top_module> [-gui] [-r]")
        sys.exit(1)
    
    top_module = sys.argv[1]
    show_gui = "-gui" in sys.argv
    reload = "-r" in sys.argv
    
    run_lint(top_module, show_gui, reload)
