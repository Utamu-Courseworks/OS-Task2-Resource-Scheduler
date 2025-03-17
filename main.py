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

#Defining routes
@app.route("/")
def index():
    """Render the UI."""
    return render_template("index.html")


#Endpoint that returns the status of agents
@app.route("/status", methods=["GET"])
def get_status():
    """Returns agent workload and queue size."""
    return jsonify({
        "agents": [
            {
                "id": a.id,
                "workload": a.workload,
                "busy": a.busy,
                "current_task": {
                    "id": a.current_task.id,
                    "priority": a.current_task.priority,
                    "service_time": a.current_task.service_time
                } if a.current_task else None
            }
            for a in agents
        ],
        "queue_size": len(scheduler.customer_queue)
    })

@app.route("/performance", methods=["GET"])
def get_performance():
    """Returns system performance metrics."""
    avg_waiting_time = (PERFORMANCE_METRICS["total_waiting_time"] / PERFORMANCE_METRICS["total_customers_served"]) if PERFORMANCE_METRICS["total_customers_served"] else 0
    avg_service_time = (PERFORMANCE_METRICS["total_service_time"] / PERFORMANCE_METRICS["total_customers_served"]) if PERFORMANCE_METRICS["total_customers_served"] else 0
    agent_utilization_rates = {agent.id: (PERFORMANCE_METRICS["agent_utilization"][agent.id] / time.time()) for agent in agents}
    
    return jsonify({
        "total_customers_served": PERFORMANCE_METRICS["total_customers_served"],
        "average_waiting_time": avg_waiting_time,
        "average_service_time": avg_service_time,
        "agent_utilization": agent_utilization_rates
    })

if __name__ == "__main__":
    threading.Thread(target=scheduler.generate_customers, daemon=True).start()
    threading.Thread(target=scheduler.assign_customer, daemon=True).start()
    app.run(debug=True)



