#Implements scheduling algorithms (Round Robin, Priority Scheduling, Shortest Job Next).

import random
import time
import threading

from app.main import CUSTOMER_PRIORITIES
from app.models.customer_model import Customer


# Scheduler Class
class Scheduler:
    def __init__(self, agents):
        self.agents = agents
        self.customer_queue = []
        self.lock = threading.Lock()

    def generate_customers(self):
        """Simulates random customer arrivals."""
        while True:
            customer = Customer(
                customer_id=random.randint(1000, 9999),
                service_time=random.randint(3, 10),
                priority=random.choice(list(CUSTOMER_PRIORITIES.keys())),
                arrival_time=time.time()
            )
            with self.lock:
                self.customer_queue.append(customer)
            time.sleep(random.randint(2, 5))

#Added function that automatically assigns a customer to an agent
    def assign_customer(self):
        """Assign customers to agents based on scheduling algorithms."""
        while True:
            if self.customer_queue:
                with self.lock:
                    self.customer_queue.sort(key=lambda x: CUSTOMER_PRIORITIES[x.priority], reverse=True)
                    customer = self.customer_queue.pop(0)
                    available_agent = next((a for a in self.agents if a.can_take_task()), None)
                    if available_agent:
                        waiting_time = time.time() - customer.arrival_time
                        performance_metrics["total_waiting_time"] += waiting_time
                        available_agent.busy = True
                        available_agent.workload += 1
                        available_agent.current_task = customer  # Track the customer being served
                        threading.Thread(target=self.process_customer, args=(available_agent, customer)).start()
            time.sleep(1)        

    def process_customer(self, agent, customer):
        """Processes a customer request."""
        start_time = time.time()
        time.sleep(customer.service_time)
        agent.total_busy_time += customer.service_time
        performance_metrics["agent_utilization"][agent.id] += customer.service_time
        performance_metrics["total_service_time"] += customer.service_time
        performance_metrics["total_customers_served"] += 1
        agent.busy = False
        agent.current_task = None  # Clear the task after completion         