# advent-of-code-2024

Advent of Code is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as interview prep, company training, university coursework, practice problems, a speed contest, or to challenge each other.

## Getting started

#### Clone the Repository:

```
https://github.com/mbrickerd/advent-of-code-2024
```

#### Install Dependencies:

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

For more information on how to install Poetry on your operating system, click [here](https://python-poetry.org/docs/#installation).

Once you have Poetry installed, run the following command from the root directory of this project:

```bash
poetry install
```

This command will also create a `.venv` virtual environment within your local project structure. Be sure to activate your newly created virtual environment before beginning with development with the appropriate command:


| Platform | Shell       | Command to activate virtual environment          |
|----------|-------------|--------------------------------------------------|
| POSIX    | bash/zsh    | `$ source <venv>/bin/activate`                   |
|          | fish        | `$ source <venv>/bin/activate.fish`              |
|          | csh/tcsh    | `$ source <venv>/bin/activate.csh`               |
|          | PowerShell  | `$ <venv>/bin/Activate.ps1`                      |
| Windows  | cmd.exe     | `C:\> <venv>\Scripts\activate.bat`               |
|          | PowerShell  | `PS C:\> <venv>\Scripts\Activate.ps1`            |


If you need to add additional packages or libraries as you develop, run the following command to update the `pyproject.toml`:

```
poetry add <package_name>
```

## Advent of Code configuration

To interact directly with the Advent of Code platform (e.g., for downloading inputs or submitting answers), this framework requires two configuration files: `aoc_headers.json` and `aoc_session`. These files store essential metadata and session information necessary for authenticated requests.

#### `aoc_headers.json`

This file contains HTTP headers used for all requests made to the Advent of Code platform. These headers include metadata such as the User-Agent to identify the source of the request.

Example content:

```json
{
    "User-Agent": "AdventOfCodeHelper/1.0 (+https://example.com; contact@example.com)"
}
```

This ensures requests conform to the platform's API requirements and helps identify your script to the Advent of Code servers.

#### `aoc_session`

This file stores the session token obtained from the Advent of Code website after logging into your account. It is required for authentication and allows access to personalized inputs and submission capabilities.

Example content:

```plaintext
abc123yourlongsessiontokenhere
```

This file provides authentication for downloading your unique puzzle inputs and submitting solutions under your account.

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
│   │   ├── base.py         # Base class definitions for shared functionality
│   │   ├── file.py         # Handles file operations (e.g., input files, test files)
│   │   ├── reader.py       # Reads and parses input data for the solution
│   │   ├── submission.py   # Logic for submitting answers to AoC
│   │   └── tester.py       # Utilities for testing solutions
│   └── utils
│       ├── __init__.py
│       └── initialise.py   # Utilities for initializing daily solution files
├── solutions
│   ├── day01.py            # Example solution for Day 1
│   └── day02.py            # Example solution for Day 2
├── templates
│   ├── solutions
│   │   └── sample.py       # Template for new daily solution files
│   └── tests
│       └── sample.txt      # Template for test cases
├── tests
│   ├── __init__.py
│   ├── test_01.py          # Tests for Day 1 solutions
│   └── test_02.py          # Tests for Day 2 solutions
├── .gitignore
├── main.py                 # Main script to manage tasks and run solutions
├── Makefile
├── poetry.lock
├── pyproject.toml
└── README.md
```

### Key Directories and Files

#### `aoc/`

This is the core package for the project. It includes:

- Models: Classes to manage input/output handling, submission logic, and testing frameworks.
- Utils: Helper functions to set up new challenges, such as generating boilerplate solution files.

#### `solutions/`

Contains the solution files for each day's challenge. Each file represents a self-contained solution where you implement logic for both parts of the day’s task.

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
- Running code quality checks (black, isort, flake8)
- Executing tests
- Formatting code

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





