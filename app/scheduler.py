#Implements scheduling algorithms (Round Robin, Priority Scheduling, Shortest Job Next).

import time
import threading

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
                priority=random.choice(list(PRIORITY_MAP.keys())),
                arrival_time=time.time()
            )
            with self.lock:
                self.customer_queue.append(customer)
            time.sleep(random.randint(2, 5))