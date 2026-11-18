# CPU Scheduling Simulator

A Python desktop application built with Tkinter that simulates, visualizes, and compares four core Operating System CPU scheduling algorithms: **FCFS**, **SJF (Non-Preemptive)**, **SRTF (Preemptive)**, and **Round Robin (RR)**. Developed for the **PT 101 Final Project (Topic 2)**.

## Features

- **Algorithms Implemented:**
  - **FCFS (First-Come, First-Served):** Non-preemptive scheduling in order of arrival.
  - **SJF (Shortest Job First):** Non-preemptive scheduling based on the shortest burst time.
  - **SRTF (Shortest Remaining Time First):** Preemptive scheduling evaluated per 1 time unit based on remaining burst time.
  - **Round Robin (RR):** Preemptive time-sliced scheduling with a configurable Time Quantum and step-by-step execution trace.
- **Interactive Process Queue:** Add custom processes (`PID`, `AT`, `BT`), delete selected rows, clear the list, or load a 4-process sample dataset.
- **Input Validation:** Prevents duplicate Process IDs, negative arrival times, and non-positive burst times or time quantums.
- **Visualizations & Metrics:** Generates color-coded, scrollable Gantt charts (including `IDLE` gaps), per-process metric tables (`CT`, `TAT`, `WT`, `RT`), overall averages, and a **Compare All** summary tab.

## Technologies Used

- **Python 3.x** (Standard Library only—no external packages required)
- **Tkinter & ttk** (Desktop GUI)

## Project Structure

```text
CPU-Scheduling-Simulator/
├── PT - Final Project/
│   ├── main.py       # Tkinter GUI, Gantt chart renderer, and comparison tab
│   ├── fcfs.py       # FCFS algorithm implementation
│   ├── sjf.py        # Non-preemptive SJF algorithm implementation
│   ├── srtf.py       # Preemptive SRTF algorithm implementation
│   ├── rr.py         # Round Robin algorithm and quantum trace logger
│   └── utils.py      # Input validation, metric calculations, and timeline merging
└── README.md
