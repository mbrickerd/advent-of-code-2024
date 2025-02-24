# advent-of-code-2024

Advent of Code is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as interview prep, company training, university coursework, practice problems, a speed contest, or to challenge each other.

## Getting started

#### Clone the Repository:

```bash
https://github.com/mbrickerd/advent-of-code-2024
```

#### Install Dependencies:

This project uses `uv` for dependency management and `pre-commit` for maintaining code quality. Follow these steps to set up your development environment:

1. First, install `uv`:

   **On Unix-like systems (Linux, macOS):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **On Windows:**
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   For more installation options, visit [uv's installation guide](https://github.com/astral-sh/uv).

2. Install project dependencies:

   ```bash
   make install
   ```

   This command will:
   - Install all project dependencies using `uv`
   - Set up pre-commit hooks for code quality

3. Individual development tools can be managed using make commands:

   ```bash
   make help              # Show all available commands
   make lint              # Run ruff linting checks
   make format            # Format code and organize imports
   make type-check        # Run mypy type checking
   make test              # Run pytest
   make all               # Run format, lint, type-check, and test
   ```

## Project structure

This repository is a modular and efficient framework designed to manage and solve Advent of Code challenges. It streamlines daily task setup, input handling, and solution submission while offering comprehensive testing and benchmarking capabilities.

```hcl
.
├── .github
│   └── workflows
│       └── python-ci.yml
├── aoc
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── authenticator.py   # Manages Advent of Code authentication credentials
│   │   ├── base.py            # Base class definitions for shared functionality
│   │   ├── file.py            # Handles file operations (e.g., input files, test files)
│   │   ├── reader.py          # Reads and parses input data for the solution
│   │   ├── submission.py      # Logic for submitting answers to AoC
│   │   └── tester.py          # Utilities for testing solutions
│   └── utils
│       ├── __init__.py
│       └── initialise.py      # Utilities for initializing daily solution files
├── solutions
│   ├── day01.py               # Example solution for Day 1
│   ├── day02.py               # Example solution for Day 2
│   └── ...
├── templates
│   ├── solutions
│   │   └── sample.py          # Template for new daily solution files
│   └── tests
│       └── sample.txt         # Template for test cases
├── tests
│   ├── __init__.py
│   ├── test_01.py             # Tests for Day 1 solutions
│   ├── test_02.py             # Tests for Day 2 solutions
│   └── ...
├── .gitignore
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── main.py                    # Main script to manage tasks and run solutions
├── Makefile                   # Development workflow automation
├── pyproject.toml             # Project dependencies and configuration
└── README.md
```

### Key Directories and Files

#### `aoc/`

This is the core package for the project. It includes:

- Models: Classes to manage input/output handling, submission logic, and testing frameworks.
- Utils: Helper functions to set up new challenges, such as generating boilerplate solution files.

#### `solutions/`

Contains the solution files for each day's challenge. Each file represents a self-contained solution where you implement logic for both parts of the day's task.

#### `templates/`

Stores reusable templates for generating boilerplate code and test cases. These templates help standardize the structure of solution and test files.

#### `tests/`

Houses the test files for validating daily solutions. Users can provide expected values to ensure solution accuracy before submission.

#### `main.py`

The central script to perform various tasks such as:

- Downloading daily puzzle input.
- Generating boilerplate code for solutions and test cases.
- Running solutions and tests.
- Benchmarking solution performance.
- Submitting answers directly to the Advent of Code website.

#### `Makefile`

Provides convenient commands for common development tasks:
- Installing dependencies
- Setting up pre-commit hooks
- Running code quality checks (ruff, mypy)
- Executing tests
- Formatting code

#### `.pre-commit-config.yaml`

Configures pre-commit hooks that run automatically before each commit to ensure code quality:
- Code formatting
- Import sorting
- Linting
- Type checking

#### `.github/workflows/python-ci.yml`

GitHub Actions workflow configuration that automates:
- Code quality checks on every push and pull request
- Test execution after successful linting
- Dependency caching for faster builds

## Usage

```bash
python main.py [-h] [-d day_number] [-p part_number] [--raw] [--add] [--add-test-file test_number] [--skip-test] [--benchmark] [--submit]
```

## Advent of Code solution runner

```hcl
options:
  -h, --help                            show this help message and exit
  -d day_number, --day day_number       Required, day number of the AoC event
  -p part_number, --part part_number    Optional, part number of the day of the AoC event
  --raw                                 Optional, use raw input instead of stripped input
  --add                                 Optional, create daily solution file and downloads puzzle input
  --add-test-file                       Optional, create additional test files
  --add-test-input                      Optional, download test input
  --skip-test                           Optional, skipping tests
  --benchmark                           Optional, benchmarking the code, and also skipping tests
  --submit                              Optional, submit your answer to AoC
```

## Example workflow

Follow these steps to work on and solve a specific Advent of Code day using this project:

#### Create a new daily solution file and download puzzle input data

To scaffold a new Solution class for a specific day:

```bash
python main.py --day [day_number] --add
```

This will create a new solution file in the `solutions/` directory (e.g., `solutions/dayXX.py`) and download the test input data for the specified day and create the corresponding `test_ZZ_input.txt` file in the `data/dayXX/` directory. Add your logic for `part1` and `part2` methods in the generated solution file.

#### Test your solution

To validate a specific part of your solution (e.g., `part1` or `part2`), follow these steps:

1. Download Test Input:

Use the following command to fetch the test input for the desired part:

```bash
python main.py --day [day_number] --part [part_number] --add-test-input
```

This will create a test input file in the appropriate location (e.g., `data/dayXX/test_ZZ_input.txt`).

2. Run Your Solution with the Test Input:

Execute your solution for the specified day and part to verify its correctness:

```bash
python main.py --day [day_number] --part [part_number]
```

The framework will load the test input file and run the corresponding method from the `Solution` class for that part.

3. Verify the Output:

Compare the output produced by your solution with the expected results. If discrepancies arise, review your logic or test input for potential issues.

By ensuring your solution matches the expected output during these tests, you can confidently proceed to full input runs or submissions.

#### Solve using full puzzle input

To run your solution on the full puzzle input after testing:

```bash
python main.py --day [day_number] --part [part_number] --skip-test
```

This bypasses the test phase and directly runs the solution on the full input dataset (`data/dayXX/puzzle_input.txt`).

#### Submit your answer

If you're confident in your solution and want to submit the result to Advent of Code:

```bash
python main.py --day [day_number] --part [part_number] --skip-test --submit
```

This will submit your answer for the specified day and part directly to Advent of Code.


## Testing

Testing your solutions ensures that your logic is accurate and aligns with the problem's requirements. This framework also integrates with PyTest to streamline the validation process for each day's challenge.

#### Setting Up Test Files

When you are ready to add test cases for a specific day, you can generate a test file using the following command:

```bash
python main.py --day [day_number] --add-test-file
```

This command will create a template test file in the `tests/` directory, named `test_<day_number>.py`. The template is pre-configured to match the structure of the Solution class for that day, making it easier to insert test cases.

#### Writing Test Cases

Navigate to the `tests/` directory and open the corresponding test file. Populate the test methods with the expected outputs from the Advent of Code problem description.

#### Running the Tests

To run all tests, simply execute the following command from the root directory:

```bash
pytest
```

You can also run tests for a specific day by specifying the file:

```bash
pytest tests/test_<day_number>.py
```

This will output detailed results, showing which tests passed, failed, or encountered errors.

## Acknowledgments

This project structure was inspired by [nitekat1124's Advent of Code 2024 repository](https://github.com/nitekat1124/advent-of-code-2024).
