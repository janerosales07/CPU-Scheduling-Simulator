# srtf.py
# Shortest Remaining Time First (SRTF) - Preemptive CPU Scheduling

from utils import copy_processes, calculate_metrics, merge_timeline


def run_srtf(processes):
    """
    Simulates Preemptive SRTF scheduling using 1-unit time steps.
    Selection rule: Shortest Remaining Burst Time among arrived processes.
    Tie-breaker: Earliest Arrival Time, then Process ID.
    """
    procs = copy_processes(processes)
    n = len(procs)
    completed_count = 0
    current_time = 0
    raw_timeline = []

    for p in procs:
        p["remaining"] = p["bt"]
        p["start_time"] = None

    while completed_count < n:
        # Gather all arrived processes that still have burst time left
        available = []
        for p in procs:
            if p["at"] <= current_time and p["remaining"] > 0:
                available.append(p)

        # If CPU is idle, record 1 unit of IDLE time
        if len(available) == 0:
            raw_timeline.append(("IDLE", current_time, current_time + 1))
            current_time += 1
            continue

        # Sort by remaining time, then arrival time, then Process ID
        available.sort(key=lambda p: (p["remaining"], p["at"], p["pid"]))
        chosen = available[0]

        # Record first response time if this is the first time getting CPU
        if chosen["start_time"] is None:
            chosen["start_time"] = current_time

        # Execute for 1 time unit
        raw_timeline.append((chosen["pid"], current_time, current_time + 1))
        chosen["remaining"] -= 1
        current_time += 1

        # Check if the process finished at this time unit
        if chosen["remaining"] == 0:
            chosen["ct"] = current_time
            completed_count += 1

    # Merge adjacent 1-unit slices into clean Gantt chart blocks
    timeline = merge_timeline(raw_timeline)
    results, averages = calculate_metrics(procs)

    return {
        "algorithm": "SRTF (Preemptive)",
        "results": results,
        "averages": averages,
        "timeline": timeline,
        "trace": []
    }