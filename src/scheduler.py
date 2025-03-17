import random
import time
import threading
from src.models.customer_model import Customer

class Scheduler:
    def __init__(self, agents):
        self.agents = agents
        self.customer_queue = []
        self.lock = threading.Lock()

    def generate_customers(self):
        """Simulates random customer arrivals."""
        from main import CUSTOMER_PRIORITIES  # Import inside method
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

    def assign_customer(self):
        """Assign customers to agents based on scheduling algorithms."""
        from main import CUSTOMER_PRIORITIES, PERFORMANCE_METRICS  # Import inside method
        while True:
            if self.customer_queue:
                with self.lock:
                    self.customer_queue.sort(key=lambda x: CUSTOMER_PRIORITIES[x.priority], reverse=True)
                    customer = self.customer_queue.pop(0)
                    available_agent = next((a for a in self.agents if a.can_take_task()), None)
                    if available_agent:
                        waiting_time = time.time() - customer.arrival_time
                        PERFORMANCE_METRICS["total_waiting_time"] += waiting_time
                        available_agent.busy = True
                        available_agent.workload += 1
                        available_agent.current_task = customer  
                        threading.Thread(target=self.process_customer, args=(available_agent, customer)).start()
            time.sleep(1)

    def process_customer(self, agent, customer):
        """Processes a customer request."""
        from main import PERFORMANCE_METRICS  # Import inside method
        start_time = time.time()
        time.sleep(customer.service_time)
        agent.total_busy_time += customer.service_time
        PERFORMANCE_METRICS["agent_utilization"][agent.id] += customer.service_time
        PERFORMANCE_METRICS["total_service_time"] += customer.service_time
        PERFORMANCE_METRICS["total_customers_served"] += 1
        agent.busy = False
        agent.current_task = None  
