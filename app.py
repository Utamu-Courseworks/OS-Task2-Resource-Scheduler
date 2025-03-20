
import threading
import time
from flask import Flask, jsonify, render_template
from models.bank_simulation import BankSimulation



app = Flask(__name__)
simulation = BankSimulation()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    threading.Thread(target=simulate, daemon=True).start()
    return jsonify(status='Simulation Started')

@app.route('/restart_simulation', methods=['POST'])
def restart_simulation():
    simulation.reset_simulation()
    return jsonify(status='Simulation Restarted')

@app.route('/get_customer_data')
def get_customer_data():
    return jsonify(customers=simulation.get_customer_data())

@app.route('/get_agent_data')
def get_agent_data():
    return jsonify(agents=simulation.get_agent_data())

@app.route('/get_metrics')
def get_metrics():
    avg_wait, utilization, fairness = simulation.calculate_metrics()
    return jsonify(avg_wait=avg_wait, utilization=utilization, fairness=fairness)


def simulate():
    for _ in range(20):  # Simulating 20 customer arrivals
        simulation.add_customer()  # Add a new customer
        simulation.assign_task('round_robin')  # Assign tasks using Round Robin scheduling
        time.sleep(3)  # Wait for 3 seconds before adding the next customer
    print("Simulation Finished")


if __name__ == '__main__':
    app.run(debug=True)