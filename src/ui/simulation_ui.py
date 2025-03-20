import tkinter as tk
from tkinter import ttk
import threading
import time


class SimulationUI:
    def __init__(self, root, simulation):
        self.root = root
        self.simulation = simulation
        self.root.title("Bank Simulation")

        # Customer Section
        self.customer_frame = ttk.Frame(self.root, padding="10")
        self.customer_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.customer_label = tk.Label(self.customer_frame, text="Customer Queue", font=("Arial", 12, "bold"), bg="#D3D3D3")
        self.customer_label.pack(fill="x")
        self.customer_tree = ttk.Treeview(self.customer_frame, columns=("ID", "Priority", "Service Time", "Arrival Time", "Wait Time", "Status", "Finish Time"), show="headings")

        # Setting the  column widths for responsiveness
        self.customer_tree.column("ID", width=50, anchor="center")
        self.customer_tree.column("Priority", width=100, anchor="center")
        self.customer_tree.column("Service Time", width=100, anchor="center")
        self.customer_tree.column("Arrival Time", width=120, anchor="center")
        self.customer_tree.column("Wait Time", width=100, anchor="center")
        self.customer_tree.column("Status", width=150, anchor="center")
        self.customer_tree.column("Finish Time", width=120, anchor="center")

        for col in ["ID", "Priority", "Service Time", "Arrival Time", "Wait Time", "Status", "Finish Time"]:
            self.customer_tree.heading(col, text=col)
        self.customer_tree.pack(fill="both", expand=True)

        # Agent Section
        self.agent_frame = ttk.Frame(self.root, padding="10")
        self.agent_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.agent_label = tk.Label(self.agent_frame, text="Agent Status", font=("Arial", 12, "bold"), bg="#D3D3D3")
        self.agent_label.pack(fill="x")
        self.agent_tree = ttk.Treeview(self.agent_frame, columns=("ID", "Status", "Workload", "Customers Served"), show="headings")
        for col in ["ID", "Status", "Workload", "Customers Served"]:
            self.agent_tree.heading(col, text=col)
        self.agent_tree.pack(fill="both", expand=True)

        # Performance Metrics Section
        self.metrics_label = tk.Label(self.root, text="Performance Metrics", font=("Arial", 12, "bold"))
        self.metrics_label.pack()
        self.metrics_text = tk.Label(self.root, text="", font=("Arial", 10))
        self.metrics_text.pack()

        # Buttons Section
        self.start_button = ttk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)

        self.restart_button = ttk.Button(self.root, text="Restart Simulation", command=self.restart_simulation)
        self.restart_button.pack(pady=10)

        self.update_ui()

    def start_simulation(self):
        threading.Thread(target=self.simulate, daemon=True).start()

    def restart_simulation(self):
        self.simulation.reset_simulation()
        self.update_ui()

    def simulate(self):
        for _ in range(20):
            self.simulation.add_customer()
            self.simulation.assign_task('round_robin')
            self.root.after(100, self.update_ui)
            time.sleep(3)

    def update_ui(self):
        self.customer_tree.delete(*self.customer_tree.get_children())
        for customer in self.simulation.get_customer_data():
            self.customer_tree.insert("", "end", values=customer)

        self.agent_tree.delete(*self.agent_tree.get_children())
        for agent in self.simulation.get_agent_data():
            # Set color based on agent's status
            status_color = "green" if agent[1] == "Free" else "orange"
            item = self.agent_tree.insert("", "end", values=agent)
            self.agent_tree.item(item, tags=(status_color,))

        # Apply status colors for agents
        self.agent_tree.tag_configure("green", background="lightgreen")
        self.agent_tree.tag_configure("orange", background="orange")

        avg_wait, utilization, fairness = self.simulation.calculate_metrics()

        # Create a string with agent numbers and their respective utilization percentages
        utilization_text = ""
        for i, (agent_id, utilization_percentage) in enumerate(utilization, start=1):
            utilization_text += f"Agent {agent_id}: {utilization_percentage}% | "

        self.metrics_text.config(text=f"Avg Waiting Time: {avg_wait:.2f} sec | Fairness: {fairness} | {utilization_text}")
