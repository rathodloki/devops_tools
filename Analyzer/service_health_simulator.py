import time
import random
import requests
import yaml

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def simulate_health(service):
    # Simulate health between 0.5 and 1.0
    return random.uniform(0.5, 1.0)

def report_health(service, health):
    try:
        response = requests.post('http://localhost:5000/health', 
                                 json={'service': service, 'health': health})
        print(f"Reported health for {service}: {health}")
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Failed to report health for {service}: {e}")
        return False

def run_simulation(config):
    while True:
        for service in config['services']:
            health = simulate_health(service)
            report_health(service, health)
        time.sleep(10)  # Wait for 10 seconds before the next round of reports

if __name__ == '__main__':
    config = load_config('service_config.yaml')
    run_simulation(config)