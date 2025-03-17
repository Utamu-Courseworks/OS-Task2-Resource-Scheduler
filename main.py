#Runs the scheduling simulation and manages customer-agent interactions.
from flask import Flask, jsonify, render_template
import random
import threading
import time

from app.models.agent_model import Agent
from app.scheduler import Scheduler

app = Flask(__name__)

# Defining customer priorities
CUSTOMER_PRIORITIES = {"VIP": 3, "Corporate": 2, "Normal": 1}

# Performance Metrics
PERFORMANCE_METRICS = {
    "total_customers_served": 0,
    "total_waiting_time": 0,
    "total_service_time": 0,
    "agent_utilization": {},
}

# Initializing some agents and  the scheduler
agents = [Agent(i) for i in range(5)]
scheduler = Scheduler(agents)


