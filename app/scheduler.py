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