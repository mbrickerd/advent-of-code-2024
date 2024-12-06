import datetime
from importlib import import_module
from argparse import ArgumentParser

from loguru import logger

from aoc.models.file import File
from aoc.models.submission import Submission


def main():
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
    parser.add_argument(
        "--add", action="store_true", help="Optional, create daily file."
    )
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
    parser.add_argument(
        "--skip-test", action="store_true", help="Optional, skipping tests."
    )
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
        logger.info(
            f"Adding test input file for day {args.day}"
        )
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
            f"The test answer is {answer}\n"
            if (answer := solution.solve(part_num=args.part)) is not None
            else ""
        )
        solution.benchmark(_print=True)

    else:
        logger.info(f"Solving day {args.day} part {args.part}\n")
        solution = import_module(f"solutions.day{args.day:02d}").Solution(
            args.day, args.part, args.raw, args.skip_test, args.benchmark
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
