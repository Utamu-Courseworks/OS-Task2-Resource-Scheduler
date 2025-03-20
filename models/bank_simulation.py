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

#function to add a new customer 
    def add_customer(self):
        with self.lock:
            customer = Customer(len(self.customers) + 1)
            self.customers.append(customer)
            self.queue.append(customer)

#function to assign an algorthm to the customer
    def assign_task(self, algorithm):
        if algorithm == 'priority':
            self.priority_scheduling()
        elif algorithm == 'round_robin':
            self.round_robin_scheduling()

    #priority scheduling functionality 
    def priority_scheduling(self):
        with self.lock:
            self.queue.sort(key=lambda x: {'VIP': 1, 'Corporate': 2, 'Normal': 3}[x.priority])
            available_agents = [a for a in self.agents if a.status == 'Free']  # Find available agents

        for customer in self.queue:
            if available_agents:
                agent = available_agents.pop(0)
                threading.Thread(target=self.assign_customer_to_agent, args=(agent, customer), daemon=True).start()  

   #Function implementation for round robin: fairness scheduling
    def round_robin_scheduling(self):
        with self.lock:
            if not self.queue:
                return
            customer = self.queue.pop(0)
            agent = self.agents[self.agent_index]
            self.agent_index = (self.agent_index + 1) % len(self.agents)
            threading.Thread(target=self.assign_customer_to_agent, args=(agent, customer), daemon=True).start()

    #Function to assign agents automatically to customers in the simulation
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
            agent.workload -= 1
            agent.customers_served += 1  # Incrementing the number of customers served by the agent
            agent.total_busy_time += time.time() - customer.start_service_time
            agent.start_busy_time = None                  