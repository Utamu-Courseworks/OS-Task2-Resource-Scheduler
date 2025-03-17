#Customer model
class Customer:
    def __init__(self, customer_id, service_time, priority, arrival_time):
        self.id = customer_id
        self.service_time = service_time
        self.priority = priority
        self.arrival_time = arrival_time  # Track when the customer arrives