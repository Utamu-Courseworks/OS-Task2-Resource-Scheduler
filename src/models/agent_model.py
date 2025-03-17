#Importing required modules
import time

# Defines classes for Customer, Agent, and task handling

#Agent class with its required attributes
#  (agentId,availability, number of tasks, max workload) and agent functions
class Agent:
  
  #Agent constructor for new objects
    def __init__(self,id, max_workload):
        self.id = id
        self.workload = 0
        self.max_workload = max_workload
        self.current_tasks = []  # List of assigned customers
        self.busy = False    
        self.total_busy_time = 0
     
    def can_take_task(self):
        return not self.busy and self.workload < self.max_workload    

    #Function to assign an agent automatically to the customer
    def assign_task(self, customer):
        if len(self.current_tasks) < self.max_workload:
            self.current_tasks.append(customer)
            self.busy = True
            return True
        return False
    
    #Releasing a customer after
    def release_task(self, customer):
        if customer in self.current_tasks:
            self.current_tasks.remove(customer)
        self.busy = len(self.current_tasks) > 0    
    
