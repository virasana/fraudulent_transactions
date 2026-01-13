import subprocess
import time
import psutil
import sys
from tabulate import tabulate  # pip install tabulate

# List of your Python scripts
scripts = [
    "fraud-pandas-iterrows.py",
    "fraud-pandas-merge.py",
    "fraud-pandas-one-liner.py",
    "fraud-simple.py"
]

# Cache results
results = []

def run_and_profile(script):
    start_time = time.time()
    
    # Start the script as a subprocess
    proc = subprocess.Popen([sys.executable, script])
    p = psutil.Process(proc.pid)
    
    peak_memory = 0
    
    # Poll until process finishes
    while proc.poll() is None:
        try:
            mem = p.memory_info().rss  # in bytes
            if mem > peak_memory:
                peak_memory = mem
        except psutil.NoSuchProcess:
            break
        time.sleep(0.1)  # check memory every 0.1s
    
    elapsed_time = time.time() - start_time
    return peak_memory / 1024 / 1024, elapsed_time  # MB, seconds

if __name__ == "__main__":
    for script in scripts:
        print(f"Running {script}...")
        peak_mem, elapsed = run_and_profile(script)
        results.append({
            "Script": script,
            "Peak Memory (MB)": f"{peak_mem:.2f}",
            "Elapsed Time (s)": f"{elapsed:.2f}"
        })

    # Print summary table
    print("\nSummary:")
    print(tabulate(results, headers="keys", tablefmt="grid"))
