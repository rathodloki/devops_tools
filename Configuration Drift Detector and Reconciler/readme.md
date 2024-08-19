# Configuration Drift Detector and Reconciler

This Python script detects and reconciles configuration drifts across different environments. It compares configurations from various environments against a base configuration, identifies differences, and optionally applies reconciliation plans.

## Features

- Detect configuration drifts across multiple environments
- Generate reconciliation plans for detected drifts
- Apply reconciliation plans automatically (optional)
- Schedule automatic drift detection and reconciliation
- Generate detailed reports of drifts and reconciliation plans
- Log activities and changes

## Requirements

- Python 3.6+
- Required Python packages:
  - PyYAML
  - GitPython
  - Jinja2
  - croniter

You can install these packages using pip:

```
pip install pyyaml gitpython jinja2 croniter
```

## Usage

### Basic Usage

```
python config_drift_detector.py <base_config> <environment_config1> [<environment_config2> ...]
```

- `<base_config>`: Path to the base configuration file
- `<environment_config1>`, `<environment_config2>`, etc.: Paths to environment-specific configuration files

### Options

- `--reconcile`: Automatically apply reconciliation plans
- `--schedule`: Set a cron schedule for automatic runs

### Examples

1. Detect drifts without reconciliation:
   ```
   python config_drift_detector.py base_config.yaml env1_config.yaml env2_config.yaml
   ```

2. Detect drifts and apply reconciliation:
   ```
   python config_drift_detector.py base_config.yaml env1_config.yaml env2_config.yaml --reconcile
   ```

3. Schedule automatic runs:
   ```
   python config_drift_detector.py base_config.yaml env1_config.yaml --schedule "0 * * * *" --reconcile
   ```

## Configuration Files

This script requires YAML configuration files for the base configuration and each environment. Here's an explanation of these files:

### Base Configuration File

The base configuration file serves as the reference point. It should contain the expected configuration that all environments should ideally match.

Example `base_config.yaml`:

```yaml
app_settings:
  name: "MyApp"
  version: "1.0.0"
database:
  host: "db.example.com"
  port: 5432
  name: "myapp_db"
features:
  feature_a: true
  feature_b: false
```

### Environment Configuration Files

Each environment (e.g., development, staging, production) should have its own configuration file. These files should follow the same structure as the base configuration file, but may have different values.

Example `env1_config.yaml` (Development):

```yaml
app_settings:
  name: "MyApp-Dev"
  version: "1.0.1"
database:
  host: "db-dev.example.com"
  port: 5432
  name: "myapp_dev_db"
features:
  feature_a: true
  feature_b: true
```

Example `env2_config.yaml` (Production):

```yaml
app_settings:
  name: "MyApp"
  version: "1.0.0"
database:
  host: "db-prod.example.com"
  port: 5432
  name: "myapp_prod_db"
features:
  feature_a: true
  feature_b: false
```

The script will compare these environment-specific configurations against the base configuration to detect drifts.

### Configuration Structure

- The configuration files should be valid YAML.
- The structure should be consistent across all files (base and environments).
- Nested structures are supported and will be compared recursively.
- Values can be strings, numbers, booleans, lists, or nested dictionaries.

When running the script, provide the paths to these configuration files as arguments:

```
python config_drift_detector.py path/to/base_config.yaml path/to/env1_config.yaml path/to/env2_config.yaml
```

## How It Works

1. The script loads the base configuration and configurations for each specified environment.
2. It compares each environment's configuration with the base configuration to detect drifts.
3. If drifts are detected, it generates a reconciliation plan.
4. If the `--reconcile` option is used, it applies the reconciliation plan, updating the environment configurations.
5. The script generates a report detailing the detected drifts and reconciliation plans.
6. All activities are logged for future reference.

## Output

The script provides a detailed report of detected drifts and reconciliation plans. If reconciliation is applied, it also commits the changes to the repository.

## Logging

All activities are logged to `config_drift.log` in the same directory as the script.

## Contributing

Contributions to improve the script are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Specify your license here]

## Contact

[Your contact information or where to report issues]