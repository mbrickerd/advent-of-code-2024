# advent-of-code-2024

Advent of Code is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as interview prep, company training, university coursework, practice problems, a speed contest, or to challenge each other.

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
  --add                                 Optional, create daily file
  --add-test-file                       Optional, create additional test files
  --skip-test                           Optional, skipping tests
  --benchmark                           Optional, benchmarking the code, and also skipping tests
  --submit                              Optional, submit your answer to AoC
```

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

## Project structure

TODO

## Solving puzzles

Follow these steps to work on and solve a specific Advent of Code day using this project:

#### Create a new daily solution file and download puzzle input data

To scaffold a new Solution class for a specific day:

```bash
python main.py --day [day_number] --add
```

This will create a new solution file in the `solutions/` directory (e.g., `solutions/dayXX.py`) and download the test input data for the specified day and create the corresponding `test_ZZ_input.txt` file in the `data/dayXX/` directory. Add your logic for `part1` and `part2` methods in the generated solution file.

#### Test your solution

To test a specific part of your solution (e.g., `part1` or `part2`):

```bash
python main.py --day [day_number] --part [part_number]
```

This will load the corresponding test data file (e.g., `data/dayXX/test_ZZ_input.txt`) and execute the specified part method using the test input. Ensure your solution produces the expected output.

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

For PyTests, when you are ready to check the results, you can create a test class:

```hcl
python main.py [--day day_number] --add-test-file
```

You then need to fill in the expected values that you get from running the logic in the respective part methods of the `Solution` class.



