import os
import requests
from packaging import version
from pathlib import Path

def find_requirement_files(directory):
    """Find all requirements.txt files in the given directory."""
    return list(Path(directory).rglob("requirements.txt"))

def parse_requirements(file_path):
    """Parse a requirements.txt file and return a list of dependencies."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

def check_latest_version(package):
    """Check the latest version of a package on PyPI."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package}/json")
        return response.json()['info']['version']
    except:
        return None

def generate_report(dependencies):
    """Generate a report of outdated dependencies."""
    report = []
    for dep in dependencies:
        name, current_version = dep.split('==')
        latest_version = check_latest_version(name)
        if latest_version and version.parse(current_version) < version.parse(latest_version):
            report.append(f"{name}: current {current_version}, latest {latest_version}")
    return report

def main(directory):
    req_files = find_requirement_files(directory)
    for file in req_files:
        print(f"Checking {file}...")
        deps = parse_requirements(file)
        report = generate_report(deps)
        if report:
            print("Outdated dependencies:")
            for item in report:
                print(item)
        else:
            print("All dependencies are up to date!")

if __name__ == "__main__":
    directory = input("Enter the directory to scan: ")
    main(directory)