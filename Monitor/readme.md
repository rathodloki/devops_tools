# Container and Host Metric Collector

## Overview

This Python script provides a flexible and extensible system for collecting metrics from Docker containers and the host system. It uses Prometheus for metrics exposure, allowing easy integration with existing monitoring systems.

## Features

- Collects CPU and memory usage metrics from Docker containers
- Gathers CPU and memory usage metrics from the host system
- Exposes metrics in Prometheus format
- Extensible design using abstract base classes
- Scheduled metric collection

## Prerequisites

- Python 3.7+
- Docker
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/container-metrics-collector.git
   cd container-metrics-collector
   ```

2. Install the required dependencies:
   ```
   pip install docker psutil schedule prometheus_client
   ```

## Usage

Run the script with:

```
python metric_collector.py
```

The script will start collecting metrics every 10 seconds and expose them on port 8000.

## Components

### MetricCollector (ABC)

An abstract base class that defines the interface for metric collectors.

### ContainerMetricCollector

Collects CPU and memory usage metrics from Docker containers.

### HostMetricCollector

Collects CPU and memory usage metrics from the host system.

### AdvancedContainerManager

Manages the metric collectors and schedules the metric collection.

## Metrics

The following metrics are collected:

- `container_cpu_usage`: CPU usage per container (percentage)
- `container_memory_usage`: Memory usage per container (MB)
- `host_cpu_usage`: Host CPU usage (percentage)
- `host_memory_usage`: Host memory usage (percentage)

## Extending the Tool

To add new metric collectors:

1. Create a new class that inherits from `MetricCollector`
2. Implement the `collect_metrics` method
3. Add an instance of your new collector to the `AdvancedContainerManager`

Example:

```python
class NetworkMetricCollector(MetricCollector):
    def __init__(self):
        self.network_io = Gauge('network_io', 'Network I/O')

    def collect_metrics(self):
        # Implement network I/O collection logic here
        pass

# In main:
manager.add_collector(NetworkMetricCollector())
```

## Prometheus Integration

Metrics are exposed in Prometheus format at `http://localhost:8000`. You can configure your Prometheus server to scrape this endpoint.

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Implement your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue on the GitHub repository or contact the maintainer at maintainer@example.com.