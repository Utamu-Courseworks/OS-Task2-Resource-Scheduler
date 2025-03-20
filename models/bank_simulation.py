import time
import threading
from datetime import datetime
from models.agent_model import Agent
from models.customer_model import Customer

class BankSimulation:
    def __init__(self):
        self.customers = []
        self.agents = [Agent(1, 5), Agent(2, 5), Agent(3, 5)]  # 3 agents with max 5 capacity
        self.queue = []
        self.lock = threading.Lock()
        self.agent_index = 0  # Track Round Robin allocation

    # Function to add a new customer
    def add_customer(self):
        with self.lock:
            customer = Customer(len(self.customers) + 1)
            self.customers.append(customer)
            self.queue.append(customer)

    # Function to assign an algorithm to the customer
    def assign_task(self, algorithm):
        if algorithm == 'priority':
            self.priority_scheduling()
        elif algorithm == 'round_robin':
            self.round_robin_scheduling()

    # Priority scheduling functionality
    def priority_scheduling(self):
        with self.lock:
            self.queue.sort(key=lambda x: {'VIP': 1, 'Corporate': 2, 'Normal': 3}[x.priority])
            available_agents = [a for a in self.agents if a.status == 'Free']  # Find available agents

        for customer in self.queue:
            if available_agents:
                agent = available_agents.pop(0)
                threading.Thread(target=self.assign_customer_to_agent, args=(agent, customer), daemon=True).start()

    # Round Robin scheduling functionality
    def round_robin_scheduling(self):
        with self.lock:
            if not self.queue:
                return
            customer = self.queue.pop(0)
            agent = self.agents[self.agent_index]
            self.agent_index = (self.agent_index + 1) % len(self.agents)
            threading.Thread(target=self.assign_customer_to_agent, args=(agent, customer), daemon=True).start()

    # Function to assign agents automatically to customers in the simulation
    def assign_customer_to_agent(self, agent, customer):
        with self.lock:
            agent.status = 'Busy'
            agent.workload += 1
            customer.start_service_time = time.time()

        time.sleep(customer.service_time)  # Simulated service time

        with self.lock:
            customer.served = True
            customer.wait_time = time.time() - customer.arrival_time  # Calculating wait time when served
            agent.status = 'Free'
            if agent.workload > 0:  # Prevent workload from going negative
                agent.workload -= 1
            agent.customers_served += 1  # Incrementing the number of customers served by the agent
            agent.total_busy_time += time.time() - customer.start_service_time
            agent.start_busy_time = None

    # Function to get customer data
    def get_customer_data(self):
        with self.lock:
            customer_data = []
            for c in self.customers:
                if c.served:
                    # If customer has been served, show finish time and wait time
                    finish_time = datetime.fromtimestamp(c.arrival_time + c.service_time).strftime("%H:%M:%S")  # Assuming service time is when finished
                    wait_time = round(c.wait_time, 2) if c.wait_time else 'N/A'
                    status = "Finished"
                elif c.start_service_time:
                    # If customer is being served
                    finish_time = "Being Served"
                    wait_time = "Calculating..."  # Wait time in process
                    status = "Being Served"
                else:
                    # If customer is waiting
                    finish_time = "Still Waiting"
                    wait_time = "Still Waiting"
                    status = "Waiting"

                customer_data.append((c.id, c.priority, c.service_time, c.formatted_arrival, wait_time, status, finish_time))

            return customer_data

    # Function to get agent data
    def get_agent_data(self):
        with self.lock:
            return [(a.id, a.status, a.workload, a.customers_served) for a in self.agents]  # Include customers_served    

    # Performance metrics function
    def calculate_metrics(self):
        with self.lock:
            served_customers = [c for c in self.customers if c.served]
            avg_waiting_time = sum(c.wait_time for c in served_customers if c.wait_time) / len(served_customers) if served_customers else 0
            total_work = sum(a.total_busy_time for a in self.agents) if self.agents else 1  # Prevent division by zero
            utilization_rates = [(a.id, round((a.total_busy_time / total_work) * 100, 2) if total_work else 0) for a in self.agents]
            fairness = max(a.workload for a in self.agents) - min(a.workload for a in self.agents) if self.agents else 0
            return avg_waiting_time, utilization_rates, fairness

    # Function to restart the simulation
    def reset_simulation(self):
        with self.lock:
            self.customers = []
            self.queue = []
            for agent in self.agents:
                agent.workload = 0
                agent.status = 'Free'
                agent.total_busy_time = 0
                agent.customers_served = 0
                agent.start_busy_time = None
