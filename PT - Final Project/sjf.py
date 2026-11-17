# sjf.py
# Shortest Job First (SJF) - Non-Preemptive CPU Scheduling

from utils import copy_processes, calculate_metrics


def run_sjf(processes):
    """
    Simulates Non-Preemptive SJF scheduling.
    Selection rule: Shortest Burst Time among arrived processes.
    Tie-breaker: Earliest Arrival Time, then Process ID.
    """
    procs = copy_processes(processes)
    n = len(procs)
    completed_count = 0
    current_time = 0
    timeline = []

    for p in procs:
        p["done"] = False

    while completed_count < n:
        # Find all processes that have arrived and are not yet finished
        available = []
        for p in procs:
            if not p["done"] and p["at"] <= current_time:
                available.append(p)

        # If no process is ready, advance CPU clock to the next earliest arrival
        if len(available) == 0:
            next_arrival = min(p["at"] for p in procs if not p["done"])
            timeline.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Pick process with smallest Burst Time (tie-break: AT, then PID)
        available.sort(key=lambda p: (p["bt"], p["at"], p["pid"]))
        chosen = available[0]

        chosen["start_time"] = current_time
        end_time = current_time + chosen["bt"]
        chosen["ct"] = end_time
        chosen["done"] = True

        timeline.append((chosen["pid"], current_time, end_time))
        current_time = end_time
        completed_count += 1

    results, averages = calculate_metrics(procs)
    return {
        "algorithm": "SJF (Non-Preemptive)",
        "results": results,
        "averages": averages,
        "timeline": timeline,
        "trace": []
    }