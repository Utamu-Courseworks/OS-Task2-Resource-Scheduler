import random
import time
from datetime import datetime

#Customer model 
class Customer:
    def __init__(self, id):
        self.id = id
        self.arrival_time = time.time()
        self.formatted_arrival = datetime.fromtimestamp(self.arrival_time).strftime("%H:%M:%S")
        self.service_time = random.randint(1, 5)  # Service time between 1 and 5 minutes
        self.priority = random.choice(['VIP', 'Corporate', 'Normal']) #customer priorities
        self.served = False  # Tracking if the customer has been served
        self.start_service_time = None
        self.wait_time = None
