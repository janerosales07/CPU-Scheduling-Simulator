# fcfs.py
# First-Come, First-Served (FCFS) - Non-Preemptive CPU Scheduling

from utils import copy_processes, calculate_metrics


def run_fcfs(processes):
    """
    Simulates FCFS scheduling.
    Tie-breaker: Earliest Arrival Time first, then Process ID.
    """
    procs = copy_processes(processes)
    # Sort by Arrival Time, then Process ID
    procs.sort(key=lambda p: (p["at"], p["pid"]))

    current_time = 0
    timeline = []

    for p in procs:
        # Handle CPU idle time gap before the next process arrives
        if current_time < p["at"]:
            timeline.append(("IDLE", current_time, p["at"]))
            current_time = p["at"]

        p["start_time"] = current_time
        end_time = current_time + p["bt"]
        p["ct"] = end_time

        timeline.append((p["pid"], current_time, end_time))
        current_time = end_time

    results, averages = calculate_metrics(procs)
    return {
        "algorithm": "FCFS (First-Come, First-Served)",
        "results": results,
        "averages": averages,
        "timeline": timeline,
        "trace": []  # Used specifically by Round Robin for quantum trace
    }