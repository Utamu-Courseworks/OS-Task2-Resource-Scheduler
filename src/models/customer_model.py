class Customer:
    def __init__(self, customer_id, service_time, priority, arrival_time):
        self.id = customer_id
        self.service_time = service_time
        self.priority = priority
        self.arrival_time = arrival_time  # Track when the customer arrives

# List to hold customers
customers = []

# Function to generate and return all customers
def generate_customers():
    """Simulate creating customers with random service times and priorities."""
    global customers
    customers = []
    for i in range(10):  # Generate 10 customers for example
        priority = random.choice(["VIP", "Corporate", "Normal"])
        service_time = random.randint(5, 15)  # Random service time between 5 and 15 minutes
        arrival_time = random.randint(0, 60)  # Random arrival time within an hour
        customer = Customer(i, service_time, priority, arrival_time)
        customers.append(customer)

# Function to get all customers
def get_all_customers():
    """Fetch all customers."""
    return customers
