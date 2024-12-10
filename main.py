import datetime
from argparse import ArgumentParser
from importlib import import_module

from loguru import logger

from aoc.models.file import File
from aoc.models.submission import Submission


def main():
    """
    Command-line interface for running and managing Advent of Code solutions.

    Provides functionality to:
    - Run solutions for specific days/parts
    - Create solution files and download inputs
    - Run tests and benchmarks
    - Submit answers to adventofcode.com

    The CLI accepts various arguments to control execution:

    Required arguments:
        -d/--day: Day number (1-25), defaults to current day
        -p/--part: Part number (1 or 2), defaults to 1

    Optional flags:
        --raw: Use raw input (preserve newlines)
        --add: Create solution files for specified day
        --add-test-input: Download test input for specified day/part
        --add-test-file: Create test file for specified day
        --skip-test: Skip running tests before solution
        --benchmark: Enable performance timing
        --submit: Submit answer to Advent of Code

    Command Flow:
    1. Validates day number is 1-25
    2. If `--add` flags used:
       - Creates necessary files/downloads inputs
    3. If solving puzzle:
       - Validates part number is 1 or 2
       - Runs tests unless `--skip-test` used
       - Executes solution and displays answer
       - If `--submit`, sends answer to AoC

    Exit codes:
        0: Success
        1: Invalid day/part number

    Example usage:
        # Run solution for current day, part 1:
        $ python main.py

        # Run day 5 part 2 with benchmarking:
        $ python main.py -d 5 -p 2 --benchmark

        # Create files for day 10:
        $ python main.py -d 10 --add

    Note:
        Solution modules must be in `solutions/dayXX.py` where `XX` is zero-padded day number
    """
    _today = datetime.date.today().day

    parser = ArgumentParser(description="Advent of Code solution runner")
    parser.add_argument(
        "-d",
        "--day",
        dest="day",
        default=_today,
        metavar="day_number",
        type=int,
        help="Required, day number of the AoC event. Must be between 1 and 25.",
    )
    parser.add_argument(
        "-p",
        "--part",
        dest="part",
        default=1,
        metavar="part_number",
        type=int,
        help="Required, part number of the day of the AoC event. Possible values are 1 or 2.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Optional, use raw input instead of stripped input.",
    )
    parser.add_argument("--add", action="store_true", help="Optional, create daily file.")
    parser.add_argument(
        "--add-test-input",
        action="store_true",
        help="Optional, download additional test input files.",
    )
    parser.add_argument(
        "--add-test-file",
        action="store_true",
        help="Optional, create test files.",
    )
    parser.add_argument("--skip-test", action="store_true", help="Optional, skipping tests.")
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Optional, benchmarking the code, and also skipping tests.",
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Optional, submit your answer to Advent of Code.",
    )
    args = parser.parse_args()

    if not 0 < args.day < 26:
        logger.info("Day number must be between 1 and 25")
        exit()

    elif args.add:
        logger.info(f"Adding day {args.day}")
        File.add_day(args.day)

    elif args.add_test_input:
        logger.info(f"Adding test input file for day {args.day}")
        File.add_test_input(args.day, args.part)

    elif args.add_test_file:
        logger.info(f"Adding test file for day {args.day}")
        File.add_test_file(args.day)

    elif args.part not in [1, 2]:
        logger.info("Part number must be 1 or 2")
        exit()

    elif not args.skip_test:
        logger.info(f"Testing day {args.day} part {args.part}\n")
        solution = import_module(f"solutions.day{args.day:02d}").Solution(
            args.day, args.part, args.raw, args.skip_test, args.benchmark
        )
        logger.info(
            f"The test answer is {answer}\n" if (answer := solution.solve(part_num=args.part)) is not None else ""
        )
        solution.benchmark(_print=True)

    else:
        logger.info(f"Solving day {args.day} part {args.part}\n")
        solution = import_module(f"solutions.day{args.day:02d}").Solution(
            args.day, args.part, args.raw, args.skip_test, args.benchmark
        )
        logger.info(f"The answer is {answer}\n" if (answer := solution.solve(part_num=args.part)) is not None else "")
        solution.benchmark(_print=True)

        if answer and args.submit is True:
            Submission.submit(args.day, args.part, answer)


if __name__ == "__main__":
    main()
