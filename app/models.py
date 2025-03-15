#Importing required modules
import time

# Defines classes for Customer, Agent, and task handling

#Agent class with its required attributes
#  (agentId,availability, number of tasks, max workload) and agent functions
class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.available = True
        self.tasks = []
        self.workload = 0
    
    #function that assigns a new task to an agent
    def assign_task(self, task):
        self.tasks.append(task) #adds new task to the tasks list
        self.available = False #once task added, the agent becomes unavailable
        self.workload += 1 #we increase agent workload to 1
    
    def complete_task(self):
        if self.tasks:
            time.sleep(self.tasks[0]['service_time'])  # Simulate work
            self.tasks.pop(0)
            self.workload -= 1
        self.available = len(self.tasks) == 0