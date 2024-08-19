# DevOps Dependency Checker

## Description
DevOps Dependency Checker is a Python tool designed to help DevOps engineers quickly check and report on dependencies across their Python projects. It scans directories for `requirements.txt` files, checks each dependency against the latest available version on PyPI, and generates a report highlighting outdated dependencies.

## Features
- Recursively scan directories for `requirements.txt` files
- Parse requirements files to extract dependency information
- Check each dependency against the latest version on PyPI
- Generate a report of outdated dependencies

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/devops-dependency-checker.git
   cd devops-dependency-checker
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line:

```
python dependency_checker.py
```

When prompted, enter the directory you want to scan. The tool will recursively search for `requirements.txt` files in this directory and its subdirectories, then check each dependency and report any outdated packages.

## Sample Output

```
Enter the directory to scan: /path/to/your/projects
Checking /path/to/your/projects/project1/requirements.txt...
Outdated dependencies:
requests: current 2.25.1, latest 2.31.0
Checking /path/to/your/projects/project2/requirements.txt...
All dependencies are up to date!
```

## Contributing

Contributions to improve DevOps Dependency Checker are welcome! Here are some ways you can contribute:

- Report bugs
- Suggest new features
- Add support for other package managers
- Improve error handling and logging
- Enhance the user interface

Please feel free to submit a Pull Request.

## Future Enhancements

- Add support for other languages and package managers (e.g., npm, gem)
- Implement vulnerability checking using a security database API
- Add an option to automatically update dependencies
- Create a simple web interface for the tool

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.