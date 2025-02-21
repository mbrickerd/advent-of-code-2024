"""Advent of Code CLI Runner.

This module provides a command-line interface for running and managing Advent of Code
solutions. It handles running solutions, creating template files, downloading inputs,
running tests, benchmarking performance, and submitting answers to adventofcode.com.

The CLI supports various arguments to control execution. Users can specify which day
and part to run, customize how inputs are handled, create necessary solution files,
control test execution and performance benchmarking, and submit answers directly to
the Advent of Code website.
"""

from argparse import ArgumentParser
import datetime

from loguru import logger

from aoc.models.file import File
from aoc.models.submission import Submission
from aoc.utils.initalise import initialise


def main() -> None:
    """Execute the Advent of Code CLI workflow.

    Parses command-line arguments and performs the requested operation:
    1. Validates day number is 1-25
    2. If creation flags used:
       - Creates solution files, test files, or downloads inputs
    3. If solving puzzle:
       - Validates part number is 1 or 2
       - Runs tests unless skipped
       - Executes solution and displays answer
       - Submits answer if requested

    Exit codes:
        0: Success
        1: Invalid day/part number (implicit through exit())
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
        solution = initialise(
            args.day, args.part, raw=args.raw, skip_test=args.skip_test, benchmark=args.benchmark
        )
        logger.info(
            f"The test answer is {answer}\n"
            if (answer := solution.solve(part_num=args.part)) is not None
            else ""
        )
        solution.benchmark(_print=True)

    else:
        logger.info(f"Solving day {args.day} part {args.part}\n")
        solution = initialise(
            args.day, args.part, raw=args.raw, skip_test=args.skip_test, benchmark=args.benchmark
        )
        logger.info(
            f"The answer is {answer}\n"
            if (answer := solution.solve(part_num=args.part)) is not None
            else ""
        )
        solution.benchmark(_print=True)

        if answer and args.submit is True:
            Submission.submit(args.day, args.part, answer)


if __name__ == "__main__":
    main()
