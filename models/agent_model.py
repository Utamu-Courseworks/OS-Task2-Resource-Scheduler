import time

class Agent:
    def __init__(self, id, max_workload):
        self.id = id
        self.workload = 0
        self.max_workload = max_workload
        self.current_tasks = []  # List of assigned customers
        self.busy = False    
        self.total_busy_time = 0
        self.current_task = None

    def can_take_task(self):
        """Check if the agent can take a new task"""
        return self.workload < self.max_workload    

    def assign_task(self, customer):
        """Assign a task to the agent if workload allows"""
        if self.can_take_task():
            self.current_tasks.append(customer)
            self.workload += 1  # Increase workload
            self.busy = self.workload >= self.max_workload  # Update busy status
            return True
        return False

    def release_task(self, customer):
        """Release a customer after task completion"""
        if customer in self.current_tasks:
            self.current_tasks.remove(customer)
            self.workload -= 1  # Reduce workload
        self.busy = self.workload >= self.max_workload  # Update busy status
