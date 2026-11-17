# rr.py
# Round Robin (RR) - Preemptive Time-Sliced CPU Scheduling

from utils import copy_processes, calculate_metrics


def run_rr(processes, quantum):
    """
    Simulates Round Robin scheduling with a given Time Quantum.
    Also records step-by-step quantum execution and remaining burst time.
    """
    procs = copy_processes(processes)
    # Sort initially by Arrival Time, then Process ID
    procs.sort(key=lambda p: (p["at"], p["pid"]))

    n = len(procs)
    for p in procs:
        p["remaining"] = p["bt"]
        p["start_time"] = None
        p["in_queue"] = False

    ready_queue = []
    timeline = []
    trace_log = []  # Stores quantum step and remaining burst time details
    current_time = 0
    completed_count = 0
    step_num = 1

    # Helper to add newly arrived processes up to current_time into the ready queue
    def enqueue_arrivals(up_to_time):
        for p in procs:
            if not p["in_queue"] and p["remaining"] > 0 and p["at"] <= up_to_time:
                ready_queue.append(p)
                p["in_queue"] = True

    enqueue_arrivals(current_time)

    while completed_count < n:
        # Handle CPU idle gap if queue is empty
        if len(ready_queue) == 0:
            next_arrival = min(p["at"] for p in procs if p["remaining"] > 0)
            timeline.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            enqueue_arrivals(current_time)
            continue

        # Pop the front process from the FIFO ready queue
        current_proc = ready_queue.pop(0)

        if current_proc["start_time"] is None:
            current_proc["start_time"] = current_time

        # Run for either the full quantum or remaining burst time (whichever is smaller)
        exec_time = min(quantum, current_proc["remaining"])
        start_slice = current_time
        end_slice = current_time + exec_time

        current_proc["remaining"] -= exec_time
        current_time = end_slice
        timeline.append((current_proc["pid"], start_slice, end_slice))

        # Log this quantum slice and remaining burst time (Topic 2 requirement)
        status = "Completed" if current_proc["remaining"] == 0 else "Re-queued"
        trace_log.append(
            f"Step {step_num}: {current_proc['pid']} ran [{start_slice} -> {end_slice}] "
            f"(Used: {exec_time}s / Q={quantum}) | Remaining BT: {current_proc['remaining']} ({status})"
        )
        step_num += 1

        # Enqueue any processes that arrived during this execution slice BEFORE re-queuing current_proc
        enqueue_arrivals(current_time)

        if current_proc["remaining"] > 0:
            ready_queue.append(current_proc)
        else:
            current_proc["ct"] = current_time
            completed_count += 1

    results, averages = calculate_metrics(procs)
    return {
        "algorithm": f"Round Robin (Quantum = {quantum})",
        "results": results,
        "averages": averages,
        "timeline": timeline,
        "trace": trace_log
    }