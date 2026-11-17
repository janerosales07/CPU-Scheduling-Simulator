# main.py
# Main Tkinter Desktop GUI for Topic 2: CPU Scheduling Simulator
# Algorithms: FCFS, Non-Preemptive SJF, Preemptive SRTF, Round Robin

import tkinter as tk
from tkinter import ttk, messagebox

from utils import validate_process_input, validate_quantum
from fcfs import run_fcfs
from sjf import run_sjf
from srtf import run_srtf
from rr import run_rr

# Distinct, clean pastel/professional colors for process blocks on the Gantt chart
PROCESS_COLORS = [
    "#4A90E2", "#50E3C2", "#F5A623", "#9013FE",
    "#E94E77", "#7ED321", "#B8E986", "#417505"
]


class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PT 101 Final Project - Topic 2: CPU Scheduling Simulator")
        self.root.geometry("1080x740")
        self.root.configure(bg="#F4F6F9")

        # Stores user-entered processes: list of dicts [{"pid": "P1", "at": 0, "bt": 7}, ...]
        self.process_list = []

        self.setup_styles()
        self.build_header()
        self.build_main_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#F4F6F9")
        style.configure("Card.TFrame", background="#FFFFFF", relief="solid", borderwidth=1)
        style.configure("TLabel", background="#F4F6F9", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#FFFFFF", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#1E293B", foreground="#FFFFFF",
                        font=("Segoe UI", 14, "bold"))
        style.configure("SubHeader.TLabel", background="#1E293B", foreground="#CBD5E1",
                        font=("Segoe UI", 9))
        style.configure("Title.TLabel", background="#FFFFFF", foreground="#0F172A",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)

    def build_header(self):
        header_frame = tk.Frame(self.root, bg="#1E293B", pady=12, padx=20)
        header_frame.pack(fill="x")

        ttk.Label(
            header_frame,
            text="CPU Scheduling Simulator (Topic 2)",
            style="Header.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Algorithms: FCFS  |  SJF (Non-Preemptive)  |  SRTF (Preemptive)  |  Round Robin (RR)",
            style="SubHeader.TLabel"
        ).pack(anchor="w")

    def build_main_layout(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        # Left Panel: Process Input & Queue Management
        left_panel = ttk.Frame(container, style="Card.TFrame", padding=12, width=320)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        self.build_input_panel(left_panel)

        # Right Panel: Tabs for Each Algorithm + Comparison
        right_panel = ttk.Frame(container)
        right_panel.pack(side="right", fill="both", expand=True)

        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill="both", expand=True)

        self.tabs = {}
        algo_keys = [
            ("FCFS", "FCFS"),
            ("SJF", "SJF (Non-Preemptive)"),
            ("SRTF", "SRTF (Preemptive)"),
            ("RR", "Round Robin (RR)"),
            ("COMPARE", "Compare All")
        ]

        for key, label in algo_keys:
            tab_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=12)
            self.notebook.add(tab_frame, text=f"  {label}  ")
            if key == "COMPARE":
                self.build_compare_tab(tab_frame)
            else:
                self.tabs[key] = self.build_algorithm_tab(tab_frame, is_rr=(key == "RR"))

    def build_input_panel(self, parent):
        ttk.Label(parent, text="1. Process Input", style="Title.TLabel").pack(anchor="w", pady=(0, 8))

        form_frame = ttk.Frame(parent, style="Card.TFrame")
        form_frame.pack(fill="x")
        form_frame.configure(relief="flat", borderwidth=0)

        # Process ID
        ttk.Label(form_frame, text="Process ID (e.g., P1):", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_pid = ttk.Entry(form_frame, width=15)
        self.entry_pid.insert(0, "P1")
        self.entry_pid.grid(row=0, column=1, sticky="e", pady=4)

        # Arrival Time
        ttk.Label(form_frame, text="Arrival Time (AT):", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_at = ttk.Entry(form_frame, width=15)
        self.entry_at.insert(0, "0")
        self.entry_at.grid(row=1, column=1, sticky="e", pady=4)

        # Burst Time
        ttk.Label(form_frame, text="Burst Time (BT):", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=4)
        self.entry_bt = ttk.Entry(form_frame, width=15)
        self.entry_bt.insert(0, "5")
        self.entry_bt.grid(row=2, column=1, sticky="e", pady=4)

        # Round Robin Quantum
        ttk.Label(form_frame, text="RR Time Quantum:", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=4)
        self.entry_quantum = ttk.Entry(form_frame, width=15)
        self.entry_quantum.insert(0, "3")
        self.entry_quantum.grid(row=3, column=1, sticky="e", pady=4)

        # Add / Remove Buttons
        btn_row = tk.Frame(parent, bg="#FFFFFF")
        btn_row.pack(fill="x", pady=8)

        tk.Button(
            btn_row, text="+ Add Process", bg="#2563EB", fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5,
            command=self.add_process
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        tk.Button(
            btn_row, text="Delete Selected", bg="#DC2626", fg="white",
            font=("Segoe UI", 9), relief="flat", padx=10, pady=5,
            command=self.delete_selected_process
        ).pack(side="right", expand=True, fill="x", padx=(4, 0))

        # Input Queue Table
        ttk.Label(parent, text="2. Ready Process List", style="Title.TLabel").pack(anchor="w", pady=(8, 4))

        cols = ("pid", "at", "bt")
        self.input_tree = ttk.Treeview(parent, columns=cols, show="headings", height=10)
        self.input_tree.heading("pid", text="Process ID")
        self.input_tree.heading("at", text="Arrival (AT)")
        self.input_tree.heading("bt", text="Burst (BT)")

        self.input_tree.column("pid", width=85, anchor="center")
        self.input_tree.column("at", width=90, anchor="center")
        self.input_tree.column("bt", width=90, anchor="center")
        self.input_tree.pack(fill="both", expand=True, pady=(0, 8))

        # Utility Buttons: Sample Data & Clear All
        util_row = tk.Frame(parent, bg="#FFFFFF")
        util_row.pack(fill="x", pady=(0, 8))

        tk.Button(
            util_row, text="Load Sample Data", bg="#E2E8F0", fg="#0F172A",
            font=("Segoe UI", 9), relief="flat", pady=5,
            command=self.load_sample_data
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        tk.Button(
            util_row, text="Clear All", bg="#E2E8F0", fg="#0F172A",
            font=("Segoe UI", 9), relief="flat", pady=5,
            command=self.clear_all
        ).pack(side="right", expand=True, fill="x", padx=(4, 0))

        # Run Simulation Button
        tk.Button(
            parent, text="▶ RUN ALL SIMULATIONS", bg="#16A34A", fg="white",
            font=("Segoe UI", 10, "bold"), relief="flat", pady=9,
            command=self.run_all_simulations
        ).pack(fill="x")

    def build_algorithm_tab(self, parent, is_rr=False):
        """Creates the Gantt chart canvas, metrics table, and average labels for one algorithm."""
        title_lbl = ttk.Label(parent, text="Run simulation to view results.", style="Title.TLabel")
        title_lbl.pack(anchor="w", pady=(0, 6))

        # Gantt Chart Section
        ttk.Label(parent, text="Gantt Chart Timeline:", style="Card.TLabel").pack(anchor="w")
        canvas_frame = tk.Frame(parent, bg="#FFFFFF")
        canvas_frame.pack(fill="x", pady=(2, 8))

        gantt_canvas = tk.Canvas(canvas_frame, height=95, bg="#F8FAFC", highlightthickness=1, highlightbackground="#CBD5E1")
        h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=gantt_canvas.xview)
        gantt_canvas.configure(xscrollcommand=h_scroll.set)

        gantt_canvas.pack(fill="x")
        h_scroll.pack(fill="x")

        # Per-Process Metrics Table
        ttk.Label(parent, text="Process Metrics Table:", style="Card.TLabel").pack(anchor="w", pady=(4, 2))
        cols = ("pid", "at", "bt", "ct", "tat", "wt", "rt")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=7)

        headers = {
            "pid": "Process ID",
            "at": "Arrival (AT)",
            "bt": "Burst (BT)",
            "ct": "Completion (CT)",
            "tat": "Turnaround (TAT)",
            "wt": "Waiting (WT)",
            "rt": "Response (RT)"
        }
        for col, text in headers.items():
            tree.heading(col, text=text)
            tree.column(col, width=95, anchor="center")

        tree.pack(fill="x", pady=(0, 8))

        # Summary Averages Banner
        avg_frame = tk.Frame(parent, bg="#EFF6FF", padx=12, pady=8, highlightbackground="#BFDBFE", highlightthickness=1)
        avg_frame.pack(fill="x", pady=(0, 8))

        avg_lbl = tk.Label(
            avg_frame,
            text="Average Turnaround Time: --   |   Average Waiting Time: --   |   Average Response Time: --",
            bg="#EFF6FF", fg="#1E3A8A", font=("Segoe UI", 10, "bold")
        )
        avg_lbl.pack(anchor="w")

        # Optional Quantum Execution Trace Box (for Round Robin)
        trace_box = None
        if is_rr:
            ttk.Label(parent, text="Round Robin Quantum & Remaining Burst Time Trace:", style="Card.TLabel").pack(anchor="w")
            trace_box = tk.Text(parent, height=6, font=("Consolas", 9), bg="#F8FAFC", state="disabled")
            trace_box.pack(fill="both", expand=True, pady=(2, 0))

        return {
            "title": title_lbl,
            "canvas": gantt_canvas,
            "tree": tree,
            "avg_label": avg_lbl,
            "trace_box": trace_box
        }

    def build_compare_tab(self, parent):
        """Creates the side-by-side comparison view for all four scheduling algorithms."""
        ttk.Label(parent, text="Algorithm Performance Comparison", style="Title.TLabel").pack(anchor="w", pady=(0, 8))

        cols = ("algo", "avg_tat", "avg_wt", "avg_rt")
        self.compare_tree = ttk.Treeview(parent, columns=cols, show="headings", height=6)
        self.compare_tree.heading("algo", text="Scheduling Algorithm")
        self.compare_tree.heading("avg_tat", text="Avg Turnaround Time (TAT)")
        self.compare_tree.heading("avg_wt", text="Avg Waiting Time (WT)")
        self.compare_tree.heading("avg_rt", text="Avg Response Time (RT)")

        self.compare_tree.column("algo", width=240, anchor="w")
        self.compare_tree.column("avg_tat", width=160, anchor="center")
        self.compare_tree.column("avg_wt", width=160, anchor="center")
        self.compare_tree.column("avg_rt", width=160, anchor="center")
        self.compare_tree.pack(fill="x", pady=(0, 12))

        self.summary_text = tk.Text(parent, height=12, font=("Segoe UI", 10), bg="#F8FAFC", state="disabled", padx=10, pady=10)
        self.summary_text.pack(fill="both", expand=True)

    # --- Event Handlers ---

    def add_process(self):
        pid = self.entry_pid.get()
        at_str = self.entry_at.get()
        bt_str = self.entry_bt.get()

        existing_pids = [p["pid"] for p in self.process_list]
        valid, msg, proc_data = validate_process_input(pid, at_str, bt_str, existing_pids)

        if not valid:
            messagebox.showerror("Invalid Input", msg)
            return

        self.process_list.append(proc_data)
        self.refresh_input_table()

        # Auto-increment Process ID suggestion (e.g., P1 -> P2) for convenience
        next_num = len(self.process_list) + 1
        self.entry_pid.delete(0, tk.END)
        self.entry_pid.insert(0, f"P{next_num}")
        self.entry_at.delete(0, tk.END)
        self.entry_at.insert(0, str(next_num - 1))

    def delete_selected_process(self):
        selected = self.input_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a process from the list to delete.")
            return

        for item_id in selected:
            values = self.input_tree.item(item_id, "values")
            pid_to_remove = values[0]
            self.process_list = [p for p in self.process_list if p["pid"] != pid_to_remove]

        self.refresh_input_table()

    def load_sample_data(self):
        """Loads a standard 4-process test dataset (matches Project Guide sample)."""
        self.process_list = [
            {"pid": "P1", "at": 0, "bt": 7},
            {"pid": "P2", "at": 1, "bt": 4},
            {"pid": "P3", "at": 2, "bt": 3},
            {"pid": "P4", "at": 3, "bt": 5}
        ]
        self.entry_quantum.delete(0, tk.END)
        self.entry_quantum.insert(0, "3")
        self.refresh_input_table()

    def clear_all(self):
        self.process_list = []
        self.refresh_input_table()
        self.entry_pid.delete(0, tk.END)
        self.entry_pid.insert(0, "P1")

    def refresh_input_table(self):
        for row in self.input_tree.get_children():
            self.input_tree.delete(row)

        for p in self.process_list:
            self.input_tree.insert("", tk.END, values=(p["pid"], p["at"], p["bt"]))

    def run_all_simulations(self):
        if len(self.process_list) == 0:
            messagebox.showwarning("Empty Process List", "Please add at least one process before running.")
            return

        valid_q, q_msg, quantum = validate_quantum(self.entry_quantum.get())
        if not valid_q:
            messagebox.showerror("Invalid Quantum", q_msg)
            return

        # Execute all 4 required Topic 2 algorithms
        fcfs_out = run_fcfs(self.process_list)
        sjf_out = run_sjf(self.process_list)
        srtf_out = run_srtf(self.process_list)
        rr_out = run_rr(self.process_list, quantum)

        all_outputs = {
            "FCFS": fcfs_out,
            "SJF": sjf_out,
            "SRTF": srtf_out,
            "RR": rr_out
        }

        for key, data in all_outputs.items():
            self.populate_algorithm_tab(self.tabs[key], data)

        self.populate_compare_tab([fcfs_out, sjf_out, srtf_out, rr_out])

    def populate_algorithm_tab(self, widgets, data):
        widgets["title"].config(text=f"Algorithm: {data['algorithm']}")

        # Clear and update Treeview table
        tree = widgets["tree"]
        for row in tree.get_children():
            tree.delete(row)

        for p in data["results"]:
            tree.insert("", tk.END, values=(
                p["pid"], p["at"], p["bt"], p["ct"], p["tat"], p["wt"], p["rt"]
            ))

        # Update Averages label
        avgs = data["averages"]
        widgets["avg_label"].config(
            text=(
                f"Average Turnaround Time: {avgs['avg_tat']:.2f}   |   "
                f"Average Waiting Time: {avgs['avg_wt']:.2f}   |   "
                f"Average Response Time: {avgs['avg_rt']:.2f}"
            )
        )

        # Draw block-based Gantt chart
        self.draw_gantt_chart(widgets["canvas"], data["timeline"])

        # Update Round Robin trace box if applicable
        if widgets["trace_box"] is not None:
            box = widgets["trace_box"]
            box.config(state="normal")
            box.delete("1.0", tk.END)
            for line in data["trace"]:
                box.insert(tk.END, line + "\n")
            box.config(state="disabled")

    def draw_gantt_chart(self, canvas, timeline):
        """Renders colored process blocks and timestamps on a scrollable Tkinter Canvas."""
        canvas.delete("all")
        if not timeline:
            return

        # Assign consistent colors per Process ID
        color_map = {}
        color_idx = 0
        for pid, _, _ in timeline:
            if pid != "IDLE" and pid not in color_map:
                color_map[pid] = PROCESS_COLORS[color_idx % len(PROCESS_COLORS)]
                color_idx += 1

        x_cursor = 20
        top_y = 18
        bottom_y = 60
        pixels_per_unit = 32  # Width per 1 unit of burst time

        # Draw initial starting timestamp (e.g., 0)
        first_start = timeline[0][1]
        canvas.create_text(x_cursor, bottom_y + 14, text=str(first_start), font=("Segoe UI", 9, "bold"), fill="#334155")

        for pid, start, end in timeline:
            duration = end - start
            # Minimum block width of 42px ensures labels remain readable even for 1-unit slices
            block_width = max(42, duration * pixels_per_unit)

            if pid == "IDLE":
                fill_color = "#CBD5E1"
                text_color = "#334155"
            else:
                fill_color = color_map[pid]
                text_color = "#FFFFFF"

            # Draw rectangle block
            canvas.create_rectangle(
                x_cursor, top_y, x_cursor + block_width, bottom_y,
                fill=fill_color, outline="#1E293B", width=1
            )

            # Process label centered inside block
            canvas.create_text(
                x_cursor + (block_width / 2), (top_y + bottom_y) / 2,
                text=pid, font=("Segoe UI", 9, "bold"), fill=text_color
            )

            x_cursor += block_width

            # End timestamp below right border of the block
            canvas.create_text(
                x_cursor, bottom_y + 14,
                text=str(end), font=("Segoe UI", 9, "bold"), fill="#334155"
            )

        canvas.configure(scrollregion=(0, 0, x_cursor + 30, 95))

    def populate_compare_tab(self, results_list):
        for row in self.compare_tree.get_children():
            self.compare_tree.delete(row)

        for item in results_list:
            avgs = item["averages"]
            self.compare_tree.insert("", tk.END, values=(
                item["algorithm"],
                f"{avgs['avg_tat']:.2f}",
                f"{avgs['avg_wt']:.2f}",
                f"{avgs['avg_rt']:.2f}"
            ))

        # Identify best algorithms by lowest Average Waiting Time and Turnaround Time
        best_wt = min(results_list, key=lambda x: x["averages"]["avg_wt"])
        best_tat = min(results_list, key=lambda x: x["averages"]["avg_tat"])
        best_rt = min(results_list, key=lambda x: x["averages"]["avg_rt"])

        summary = (
            "SHORT ALGORITHM COMPARISON SUMMARY\n"
            "------------------------------------------------------------\n"
            f"• Lowest Average Waiting Time:    {best_wt['algorithm']} ({best_wt['averages']['avg_wt']:.2f})\n"
            f"• Lowest Average Turnaround Time: {best_tat['algorithm']} ({best_tat['averages']['avg_tat']:.2f})\n"
            f"• Lowest Average Response Time:   {best_rt['algorithm']} ({best_rt['averages']['avg_rt']:.2f})\n\n"
            "Key Observations:\n"
            "- FCFS executes strictly in arrival order; long early jobs can cause the convoy effect.\n"
            "- SJF (Non-Preemptive) reduces waiting time by running shorter jobs first once arrived.\n"
            "- SRTF (Preemptive) typically achieves the lowest average waiting and turnaround times by preempting longer jobs.\n"
            "- Round Robin ensures fair CPU sharing and strong response times across all processes using fixed time slices."
        )

        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()