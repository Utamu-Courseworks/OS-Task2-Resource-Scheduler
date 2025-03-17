#Runs the scheduling simulation and manages customer-agent interactions.

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Enabling CORS for all routes
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
