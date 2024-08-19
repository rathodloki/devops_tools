import networkx as nx
import yaml
import json
import time
from flask import Flask, jsonify, request, render_template_string
from prometheus_client import start_http_server, Counter, Gauge

class ServiceDependencyAnalyzer:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.graph = nx.DiGraph()
        self.build_dependency_graph()
        self.service_health = {service: 1.0 for service in self.graph.nodes()}
        self.impact_scores = self.calculate_impact_scores()

    def build_dependency_graph(self):
        for service, deps in self.config['services'].items():
            self.graph.add_node(service)
            for dep in deps['dependencies']:
                self.graph.add_edge(service, dep)

    def calculate_impact_scores(self):
        scores = {}
        for node in self.graph.nodes():
            descendants = nx.descendants(self.graph, node)
            scores[node] = len(descendants) / (len(self.graph.nodes()) - 1)
        return scores

    def update_health(self, service, health):
        self.service_health[service] = health
        self.propagate_health_impact(service)

    def propagate_health_impact(self, service):
        for dependent in self.graph.predecessors(service):
            dep_health = min(self.service_health[dep] for dep in self.graph.successors(dependent))
            self.service_health[dependent] = dep_health

    def predict_outage_impact(self, service):
        impacted_services = nx.ancestors(self.graph, service)
        return {s: self.impact_scores[s] for s in impacted_services}

    def suggest_scaling(self):
        suggestions = {}
        for service in self.graph.nodes():
            if self.service_health[service] < 0.7 and self.impact_scores[service] > 0.5:
                suggestions[service] = "Consider scaling up due to low health and high impact"
        return suggestions

app = Flask(__name__)
analyzer = ServiceDependencyAnalyzer('service_config.yaml')

# Prometheus metrics
service_health_gauge = Gauge('service_health', 'Health of each service', ['service'])
impact_score_gauge = Gauge('impact_score', 'Impact score of each service', ['service'])

@app.route('/health', methods=['POST'])
def update_health():
    data = request.json
    analyzer.update_health(data['service'], data['health'])
    service_health_gauge.labels(service=data['service']).set(data['health'])
    return jsonify({"status": "updated"})

@app.route('/impact/<service>')
def get_impact(service):
    return jsonify(analyzer.predict_outage_impact(service))

@app.route('/suggestions')
def get_suggestions():
    return jsonify(analyzer.suggest_scaling())

@app.route('/')
def home():
    return render_template_string('''
        <h1>Service Dependency and Impact Analyzer</h1>
        <h2>Service Health</h2>
        <ul>
        {% for service, health in health.items() %}
            <li>{{ service }}: {{ health }}</li>
        {% endfor %}
        </ul>
        <h2>Impact Scores</h2>
        <ul>
        {% for service, score in impact.items() %}
            <li>{{ service }}: {{ score }}</li>
        {% endfor %}
        </ul>
        <h2>Scaling Suggestions</h2>
        <ul>
        {% for service, suggestion in suggestions.items() %}
            <li>{{ service }}: {{ suggestion }}</li>
        {% endfor %}
        </ul>
    ''', health=analyzer.service_health, impact=analyzer.impact_scores, suggestions=analyzer.suggest_scaling())

if __name__ == '__main__':
    start_http_server(8000)  # Prometheus metrics
    for service, score in analyzer.impact_scores.items():
        impact_score_gauge.labels(service=service).set(score)
    app.run(debug=True, use_reloader=False)