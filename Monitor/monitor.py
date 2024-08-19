from abc import ABC, abstractmethod
import docker
import psutil
import time
import schedule
from prometheus_client import start_http_server, Gauge

class MetricCollector(ABC):
    @abstractmethod
    def collect_metrics(self):
        pass

class ContainerMetricCollector(MetricCollector):
    def __init__(self, docker_client):
        self.client = docker_client
        self.container_cpu = Gauge('container_cpu_usage', 'CPU usage per container', ['container_name'])
        self.container_memory = Gauge('container_memory_usage', 'Memory usage per container', ['container_name'])

    def collect_metrics(self):
        for container in self.client.containers.list():
            stats = container.stats(stream=False)
            cpu_usage = self._calculate_cpu_percent(stats)
            memory_usage = stats['memory_stats'].get('usage', 0) / (1024 * 1024)  # Convert to MB
            
            self.container_cpu.labels(container.name).set(cpu_usage)
            self.container_memory.labels(container.name).set(memory_usage)
            
            print(f"Container: {container.name}, CPU: {cpu_usage:.2f}%, Memory: {memory_usage:.2f} MB")

    def _calculate_cpu_percent(self, stats):
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        num_cpus = len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
        return (cpu_delta / system_delta) * num_cpus * 100.0

class HostMetricCollector(MetricCollector):
    def __init__(self):
        self.host_cpu = Gauge('host_cpu_usage', 'Host CPU usage')
        self.host_memory = Gauge('host_memory_usage', 'Host memory usage')

    def collect_metrics(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        self.host_cpu.set(cpu_usage)
        self.host_memory.set(memory_usage)
        
        print(f"Host - CPU: {cpu_usage:.2f}%, Memory: {memory_usage:.2f}%")

class AdvancedContainerManager:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.metric_collectors = []

    def add_collector(self, collector: MetricCollector):
        self.metric_collectors.append(collector)

    def collect_all_metrics(self):
        for collector in self.metric_collectors:
            collector.collect_metrics()

    def run(self):
        start_http_server(8000)  # Start Prometheus metrics server
        schedule.every(10).seconds.do(self.collect_all_metrics)
        
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    manager = AdvancedContainerManager()
    manager.add_collector(ContainerMetricCollector(manager.docker_client))
    manager.add_collector(HostMetricCollector())
    manager.run()