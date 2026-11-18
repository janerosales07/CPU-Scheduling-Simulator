CPU Scheduling Simulator

A desktop application built with Python and Tkinter that simulates four classic CPU scheduling algorithms. Enter your processes once, run every algorithm at the same time, and compare their Gantt charts and performance metrics side by side.

Created for PT 101 Final Project, Topic 2: CPU Scheduling Simulator.

Features
- Interactive GUI with a process input panel and one tab per algorithm
- Four scheduling algorithms run with a single click
- Color-coded, scrollable Gantt chart with start and end timestamps
- Per-process metrics table (CT, TAT, WT, RT) and average metrics
- Idle time shown on the Gantt chart when the CPU waits for the next arrival
- Round Robin quantum trace that shows each time slice and the remaining burst time
- Compare All tab that ranks the algorithms by average TAT, WT, and RT
- Input validation (duplicate IDs, negative arrival times, zero or negative burst times, invalid quantum)
- One-click sample data loader

  Supported Algorithms
Algorithm	                            Type	            Selection rule
FCFS (First-Come, First-Served)	      Non-preemptive	  Earliest arrival runs first
SJF (Shortest Job First)	            Non-preemptive	  Shortest burst time among arrived processes
SRTF (Shortest Remaining Time First)	Preemptive	      Shortest remaining time, checked every 1 time unit
RR (Round Robin)	                    Preemptive	      FIFO ready queue with a user-defined time quantum

Tie-breaking: when processes tie, the earlier arrival time wins, then the process ID.

Requirements
- Python 3.8 or newer
- Tkinter (included with the standard Python installer on Windows and macOS)

No third-party packages are needed.

On some Linux distributions Tkinter must be installed separately:
bash
sudo apt install python3-tk

Getting Started
bash
# Clone the repository
git clone https://github.com/janerosales07/CPU-Scheduling-Simulator.git
cd CPU-Scheduling-Simulator

# Run the app
python main.py

How to Use
1. Enter a Process ID (e.g., P1), Arrival Time, and Burst Time, then click + Add Process.
2. Set the RR Time Quantum (default is 3).
3. Repeat for each process. To remove one, select it in the list and click Delete Selected.
4. Click Load Sample Data to fill in a ready-made example, or Clear All to start over.
5. Click ▶ RUN ALL SIMULATIONS.
6. Open the FCFS, SJF, SRTF, and Round Robin tabs to see each Gantt chart and metrics table.
7. Open Compare All to see which algorithm performs best.

Input rules
Field	                 Rule
Process ID	           Required, unique (automatically converted to uppercase)
Arrival Time	         Whole number, 0 or greater
Burst Time	           Whole number, greater than 0
Time Quantum	         Whole number, greater than 0



Sample Run

Using the built-in sample data and a quantum of 3:

Process	      Arrival	     Burst
P1	             0	         7
P2	             1	         4
P3	             2	         3
P4	             3	         5

Gantt charts

FCFS   | P1 (0-7) | P2 (7-11) | P3 (11-14) | P4 (14-19) |

SJF    | P1 (0-7) | P3 (7-10) | P2 (10-14) | P4 (14-19) |

SRTF   | P1 (0-1) | P2 (1-5) | P3 (5-8) | P4 (8-13) | P1 (13-19) |

RR     | P1 (0-3) | P2 (3-6) | P3 (6-9) | P4 (9-12) | P1 (12-15) | P2 (15-16) | P4 (16-18) | P1 (18-19) |


Comparison
Algorithm	             Avg Turnaround	        Avg Waiting	         Avg Response
FCFS	                      11.25                 6.50	               6.50
SJF (Non-Preemptive)	      11.00	                6.25	               6.25
SRTF (Preemptive)	          9.75	                5.00	               2.00
Round Robin (Q = 3)	        14.00	                9.25	               3.00


On this data set, SRTF has the lowest average turnaround and waiting time. It also has the lowest response time.

Metrics
Metric	                  Formula
Turnaround Time (TAT)	    Completion Time − Arrival Time
Waiting Time (WT)	        Turnaround Time − Burst Time
Response Time (RT)	      First CPU Start Time − Arrival Time

Project Structure

CPU-Scheduling-Simulator/
├── main.py     # Tkinter GUI, Gantt chart drawing, comparison tab
├── fcfs.py     # First-Come, First-Served
├── sjf.py      # Non-preemptive Shortest Job First
├── srtf.py     # Preemptive Shortest Remaining Time First
├── rr.py       # Round Robin with quantum trace
├── utils.py    # Input validation, metric calculation, timeline merging
└── README.md

Each algorithm module exposes a run_* function that takes the process list and returns a dictionary with algorithm, results, averages, timeline, and trace. The GUI only displays that data, so adding a new algorithm means adding a new module and a new tab.

Notes and Limitations
Times are whole numbers only.
Priority scheduling is not included.
Context-switch overhead is not simulated.

## Authors

- Name One: [GitHub](https://github.com/username1)
- Baby Jane Delen: [GitHub](https://github.com/username2)
