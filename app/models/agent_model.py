#Importing required modules
import time

# Defines classes for Customer, Agent, and task handling

#Agent class with its required attributes
#  (agentId,availability, number of tasks, max workload) and agent functions
class Agent:
  
  #Agent constructor for new objects
    def __init__(self, agent_id, max_workload):
        self.agent_id = agent_id
        self.max_workload = max_workload
        self.current_tasks = []  # List of assigned customers
        self.busy = False    

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
    
