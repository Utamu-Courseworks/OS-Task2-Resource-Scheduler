#Runs the scheduling simulation and manages customer-agent interactions.
from flask import Flask, jsonify, render_template
import threading
from src.models.agent_model import Agent

app = Flask(__name__,template_folder="src/templates")

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
#agents = [Agent(i) for i in range(5)]
agents = [Agent(i, max_workload=3) for i in range(5)] 


def start_scheduler():
    from src.scheduler import Scheduler  # Import inside function
    global scheduler
    scheduler = Scheduler(agents)

start_scheduler()

@app.route("/")
def index():
    """Render the UI."""
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
    agent_utilization_rates = {agent.id: (PERFORMANCE_METRICS["agent_utilization"][agent.id] / threading.current_thread().ident) for agent in agents}

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
