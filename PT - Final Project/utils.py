# utils.py
# Common helper functions for validation, metric computation, and formatting.


def validate_process_input(pid, at_str, bt_str, existing_pids):
    """Validates a single process entry before adding it to the input list."""
    pid = pid.strip().upper()
    if pid == "":
        return False, "Process ID cannot be empty (e.g., P1).", None

    if pid in existing_pids:
        return False, f"Process ID '{pid}' already exists.", None

    try:
        at = int(at_str)
        bt = int(bt_str)
    except ValueError:
        return False, "Arrival Time and Burst Time must be whole numbers.", None

    if at < 0:
        return False, "Arrival Time cannot be negative (must be >= 0).", None

    if bt <= 0:
        return False, "Burst Time must be greater than 0.", None

    process_data = {
        "pid": pid,
        "at": at,
        "bt": bt
    }
    return True, "Valid", process_data


def validate_quantum(quantum_str):
    """Validates the Time Quantum input for Round Robin."""
    try:
        q = int(quantum_str)
        if q <= 0:
            return False, "Time Quantum must be a positive integer (> 0).", None
        return True, "Valid", q
    except ValueError:
        return False, "Time Quantum must be a valid whole number.", None


def copy_processes(processes):
    """Creates a clean copy of the process list so algorithms don't overwrite inputs."""
    copied = []
    for p in processes:
        copied.append({
            "pid": p["pid"],
            "at": p["at"],
            "bt": p["bt"]
        })
    return copied


def calculate_metrics(completed_processes):
    """
    Computes TAT, WT, RT and overall averages using standard OS formulas:
    - TAT = CT - AT
    - WT  = TAT - BT
    - RT  = First Start Time - AT
    """
    total_tat = 0
    total_wt = 0
    total_rt = 0

    for p in completed_processes:
        p["tat"] = p["ct"] - p["at"]
        p["wt"] = p["tat"] - p["bt"]
        p["rt"] = p["start_time"] - p["at"]

        total_tat += p["tat"]
        total_wt += p["wt"]
        total_rt += p["rt"]

    n = len(completed_processes)
    if n == 0:
        averages = {"avg_tat": 0.0, "avg_wt": 0.0, "avg_rt": 0.0}
    else:
        averages = {
            "avg_tat": round(total_tat / n, 2),
            "avg_wt": round(total_wt / n, 2),
            "avg_rt": round(total_rt / n, 2)
        }

    # Sort results cleanly by Process ID (e.g., P1, P2, P3...) for display
    completed_processes.sort(key=lambda item: item["pid"])
    return completed_processes, averages


def merge_timeline(raw_timeline):
    """
    Combines consecutive 1-unit execution slices of the same process into single blocks.
    Example: [('P1', 0, 1), ('P1', 1, 2)] -> [('P1', 0, 2)]
    """
    if not raw_timeline:
        return []

    merged = [list(raw_timeline[0])]
    for current in raw_timeline[1:]:
        last = merged[-1]
        if current[0] == last[0] and current[1] == last[2]:
            last[2] = current[2]
        else:
            merged.append(list(current))

    return [(block[0], block[1], block[2]) for block in merged]