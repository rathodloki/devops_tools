# Service Dependency and Impact Analyzer (SDIA)

## Overview

The Service Dependency and Impact Analyzer (SDIA) is a tool designed to help DevOps teams understand and manage complex microservices architectures. It provides real-time analysis of service dependencies, health status, and potential impact of service outages.

## Features

- Automatic dependency mapping based on configuration
- Real-time health monitoring and propagation
- Impact score calculation for each service
- Outage impact prediction
- Scaling suggestions based on service health and impact
- Prometheus integration for metrics exposure
- Web interface for easy visualization

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/service-dependency-analyzer.git
   cd service-dependency-analyzer
   ```

2. Install the required dependencies:
   ```
   pip install networkx pyyaml flask prometheus_client requests
   ```

## Configuration

Create a `service_config.yaml` file in the project root directory. This file defines your services and their dependencies. Example:

```yaml
services:
  web_frontend:
    dependencies:
      - auth_service
      - product_catalog
  auth_service:
    dependencies:
      - user_database
  product_catalog:
    dependencies:
      - product_database
  user_database:
    dependencies: []
  product_database:
    dependencies: []
```

## Usage

1. Start the main Service Dependency and Impact Analyzer:
   ```
   python service_analyzer.py
   ```

2. In a separate terminal, start the health simulator (for demonstration purposes):
   ```
   python service_health_simulator.py
   ```

3. Access the web interface at `http://localhost:5000`

4. Prometheus metrics are exposed at `http://localhost:8000`

## API Endpoints

- `POST /health`: Update the health of a service
  - Body: `{"service": "service_name", "health": 0.95}`
- `GET /impact/<service>`: Get the predicted impact of a service outage
- `GET /suggestions`: Get scaling suggestions based on current system state

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Implement your changes
4. Submit a pull request

## Testing

Run the unit tests with:
```
python -m unittest discover tests
```

## Future Enhancements

- Integration with CI/CD pipelines
- Machine learning for predictive analysis
- Enhanced web UI with interactive service graphs
- Support for multi-cluster environments

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue on the GitHub repository or contact the maintainer at maintainer@example.com.