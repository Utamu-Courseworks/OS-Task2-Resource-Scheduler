class Agent:
    def __init__(self, id, max_capacity):
        self.id = id
        self.max_capacity = max_capacity
        self.workload = 0
        self.status = 'Free'#agent availability
        self.total_busy_time = 0
        self.start_busy_time = None
        self.customers_served = 0  # Tracking the number of customers served
