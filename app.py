#Runs the scheduling simulation and manages customer-agent interactions.
import random
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
# Assign different workload limits between 2 and 5 for each agent
agents = [Agent(i, max_workload=random.randint(2, 5)) for i in range(5)]


def start_scheduler():
    from src.scheduler import Scheduler  # Import inside function
    global scheduler
    scheduler = Scheduler(agents)

start_scheduler()

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/status", methods=["GET"])
def get_status():
    agents = Agent.get_all_agents()  # assuming you have a method to fetch agents
    customers = get_all_customers()  # This function should return the list of customers

    agents_data = [
        {
            "id": a.id,
            "workload": a.workload,
            "busy": a.busy,
            "current_task": a.current_task,  # you can display customer task here if needed
        } for a in agents
    ]

    customers_data = [
        {
            "id": c.id,
            "service_time": c.service_time,  # Assuming service_time is an attribute of customer
            "priority": c.priority  # Assuming priority is an attribute of customer
        } for c in customers
    ]

    return jsonify({
        "agents": agents_data,
        "customers": customers_data,  # Add the customer data to the response
    })


# @app.route("/status", methods=["GET"])
# def get_status():
#     """Returns agent workload and queue size."""
#     return jsonify({
#         "agents": [
#             {
#                 "id": a.id,
#                 "workload": a.workload,
#                 "busy": a.busy,
#                 "current_task": {
#                     "id": a.current_task.id,
#                     "priority": a.current_task.priority,
#                     "service_time": a.current_task.service_time
#                 } if a.current_task else None
#             }
#             for a in agents
#         ],
#         "queue_size": len(scheduler.customer_queue)
#     })

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
    app.run(debug=True,host='0.0.0.0', port=5000)
    

#test