import yaml
import difflib
import argparse
import os
from git import Repo
from jinja2 import Template
from croniter import croniter
from datetime import datetime
import logging, time

class ConfigDriftDetector:
    def __init__(self, base_config, environments):
        self.base_config = self.load_config(base_config)
        self.environments = {env: self.load_config(path) for env, path in environments.items()}
        self.setup_logging()

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename='config_drift.log')

    def detect_drift(self):
        drifts = {}
        for env, config in self.environments.items():
            drift = self.compare_configs(self.base_config, config)
            if drift:
                drifts[env] = drift
        return drifts

    def compare_configs(self, base, compare):
        drift = {}
        for key in base:
            if key not in compare:
                drift[key] = f"Missing in {compare}"
            elif isinstance(base[key], dict):
                nested_drift = self.compare_configs(base[key], compare[key])
                if nested_drift:
                    drift[key] = nested_drift
            elif base[key] != compare[key]:
                drift[key] = f"Base: {base[key]}, Compare: {compare[key]}"
        return drift

    def generate_reconciliation_plan(self, drifts):
        plans = {}
        for env, drift in drifts.items():
            plans[env] = self.create_plan(drift, env)
        return plans

    def create_plan(self, drift, env, parent_key=""):
        plan = []
        for key, value in drift.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                plan.extend(self.create_plan(value, env, full_key))
            else:
                plan.append(f"Update {full_key} in {env}")
        return plan

    def apply_reconciliation(self, plans):
        for env, plan in plans.items():
            logging.info(f"Applying reconciliation for {env}")
            config_path = self.environments[env]
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            
            for action in plan:
                key = action.split(" ")[1]
                value = self.get_nested_value(self.base_config, key.split("."))
                self.set_nested_value(config, key.split("."), value)
            
            with open(config_path, 'w') as file:
                yaml.dump(config, file)
            
            self.commit_changes(config_path, f"Reconciled configuration for {env}")

    def get_nested_value(self, config, keys):
        for key in keys:
            config = config[key]
        return config

    def set_nested_value(self, config, keys, value):
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value

    def commit_changes(self, file_path, commit_message):
        repo = Repo(os.path.dirname(file_path))
        repo.index.add([file_path])
        repo.index.commit(commit_message)

    def generate_report(self, drifts, plans):
        template = Template("""
        # Configuration Drift Report
        {% for env, drift in drifts.items() %}
        ## {{ env }}
        ### Detected Drifts:
        ```
        {{ drift | pprint }}
        ```
        ### Reconciliation Plan:
        {% for action in plans[env] %}
        - {{ action }}
        {% endfor %}
        {% endfor %}
        """)
        return template.render(drifts=drifts, plans=plans)

def main():
    parser = argparse.ArgumentParser(description="Configuration Drift Detector and Reconciler")
    parser.add_argument("base_config", help="Path to base configuration file")
    parser.add_argument("environments", nargs="+", help="Paths to environment configuration files")
    parser.add_argument("--reconcile", action="store_true", help="Automatically reconcile drifts")
    parser.add_argument("--schedule", help="Cron schedule for automatic runs")
    args = parser.parse_args()

    env_configs = {f"env_{i}": path for i, path in enumerate(args.environments, 1)}
    detector = ConfigDriftDetector(args.base_config, env_configs)

    def run_detection():
        drifts = detector.detect_drift()
        if drifts:
            plans = detector.generate_reconciliation_plan(drifts)
            report = detector.generate_report(drifts, plans)
            print(report)
            if args.reconcile:
                detector.apply_reconciliation(plans)
        else:
            print("No configuration drift detected.")

    if args.schedule:
        cron = croniter(args.schedule, datetime.now())
        while True:
            next_run = cron.get_next(datetime)
            time.sleep((next_run - datetime.now()).total_seconds())
            run_detection()
    else:
        run_detection()

if __name__ == "__main__":
    main()