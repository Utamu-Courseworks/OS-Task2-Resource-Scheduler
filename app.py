import random
from flask import Flask, jsonify, render_template, request
import threading
from src.models.agent_model import Agent
from src.scheduler import Scheduler  # Import Scheduler here

app = Flask(__name__, template_folder="src/templates")

# Defining customer priorities
CUSTOMER_PRIORITIES = {"VIP": 3, "Corporate": 2, "Normal": 1}

# Performance Metrics
PERFORMANCE_METRICS = {
    "total_customers_served": 0,
    "total_waiting_time": 0,
    "total_service_time": 0,
    "agent_utilization": {},
}

# Initialize agents
agents = [Agent(i, max_workload=random.randint(2, 5)) for i in range(5)]

# Initialize scheduler with default algorithm (priority)
scheduler = Scheduler(agents, scheduling_algorithm="priority")

def start_scheduler():
    global scheduler
    scheduler = Scheduler(agents)

start_scheduler()

@app.route("/")
def index():
    return render_template("dashboard.html")

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
    agent_utilization_rates = {agent.id: (PERFORMANCE_METRICS["agent_utilization"].get(agent.id, 0) / PERFORMANCE_METRICS["total_service_time"]) for agent in agents}

    return jsonify({
        "total_customers_served": PERFORMANCE_METRICS["total_customers_served"],
        "average_waiting_time": avg_waiting_time,
        "average_service_time": avg_service_time,
        "agent_utilization": agent_utilization_rates
    })

@app.route("/set_algorithm", methods=["POST"])
def set_algorithm():
    """Changes the scheduling algorithm dynamically."""
    global scheduler
    data = request.get_json()
    selected_algorithm = data.get('algorithm', 'priority')  # Default to 'priority'
    
    # Update the scheduling algorithm
    scheduler.scheduling_algorithm = selected_algorithm

    return jsonify({"status": "success", "algorithm": scheduler.scheduling_algorithm})

if __name__ == "__main__":
    # Start customer generation and assignment in separate threads
    threading.Thread(target=scheduler.generate_customers, daemon=True).start()
    threading.Thread(target=scheduler.assign_customer, daemon=True).start()

    app.run(debug=True, host='0.0.0.0', port=5000)
