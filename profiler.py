import subprocess
import time
import psutil
import sys
import gc
from tabulate import tabulate  # pip install tabulate

# -----------------------------
# Configuration
# -----------------------------
scripts = [
    "fraud-pandas-iterrows.py",
    "fraud-pandas-merge.py",
    "fraud-pandas-one-liner.py",
    "fraud-simple.py"
]

# Memory stabilization parameters
baseline_tolerance_mb = 50    # MB within baseline considered stabilized
poll_interval = 0.1            # seconds between memory checks
max_wait_stabilize = 15        # maximum seconds to wait for stabilization

# -----------------------------
# Helper functions
# -----------------------------
def get_memory_baseline():
    """Return current memory of the main process in MB"""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024

def wait_for_memory_stabilization(baseline_mb, tolerance_mb=50, max_wait=max_wait_stabilize):
    """Wait until memory usage returns close to baseline or max_wait seconds"""
    start = time.time()
    process = psutil.Process()
    while True:
        mem = process.memory_info().rss / 1024 / 1024
        if mem <= baseline_mb + tolerance_mb:
            break
        if time.time() - start > max_wait:
            print(f"Memory did not fully stabilize after {max_wait}s, proceeding anyway...")
            break
        time.sleep(poll_interval)

def cleanup_memory(proc_pid=None):
    """Kill lingering child processes and force Python garbage collection"""
    # Kill child processes if any
    if proc_pid:
        try:
            parent = psutil.Process(proc_pid)
            children = parent.children(recursive=True)
            for child in children:
                child.kill()
            psutil.wait_procs(children, timeout=3)
        except psutil.NoSuchProcess:
            pass

    # Force Python garbage collection
    gc.collect()

def run_and_profile(script):
    """Run script and return (peak_memory_MB, elapsed_time_s, pid)"""
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
        time.sleep(poll_interval)
    
    elapsed_time = time.time() - start_time
    return peak_memory / 1024 / 1024, elapsed_time, proc.pid  # MB, seconds, pid

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    results = []

    # Record initial baseline memory
    pre_run_baseline = get_memory_baseline()
    print(f"Initial memory baseline: {pre_run_baseline:.2f} MB")

    for script in scripts:
        print(f"\nRunning {script}...")
        peak_mem, elapsed, pid = run_and_profile(script)
        results.append({
            "Script": script,
            "Peak Memory (MB)": f"{peak_mem:.2f}",
            "Elapsed Time (s)": f"{elapsed:.2f}"
        })

        # Cleanup leftover memory/processes
        cleanup_memory(proc_pid=pid)

        # Wait until memory stabilizes to pre-run baseline
        print("Waiting for memory to stabilize...")
        wait_for_memory_stabilization(pre_run_baseline, tolerance_mb=baseline_tolerance_mb)
        stabilized_mem = get_memory_baseline()
        print(f"Memory stabilized at {stabilized_mem:.2f} MB")

    # Print summary table
    print("\nSummary:")
    print(tabulate(results, headers="keys", tablefmt="grid"))
