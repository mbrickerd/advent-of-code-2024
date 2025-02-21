"""
File management utilities for Advent of Code.

This module provides a File class with methods for managing Advent of Code file
operations, including retrieving session credentials, downloading puzzle inputs, and
setting up solution files for each day's challenge.
"""

from datetime import datetime
from pathlib import Path
from time import sleep

from bs4 import BeautifulSoup
from loguru import logger
import requests

from aoc.models.authenticator import Authenticator


class File:
    """Utility class for managing Advent of Code file operations and puzzle input retrieval.

    This class provides methods for handling file paths, session management,
    downloading puzzle/test inputs, and setting up solution files. It manages the
    directory structure and timing for puzzle input availability.
    """

    @staticmethod
    def download_puzzle_input(day: int) -> str:
        """Download the puzzle input for a specific day from Advent of Code.

        Args:
            day: The day number (1-25) of the puzzle.

        Returns
        -------
            The puzzle input content.

        Note:
            Requires valid session token and headers configuration.
            Year is determined from the project directory name.
        """
        session = Authenticator.get_session()
        path_obj = Path(Authenticator.get_path())
        year = path_obj.parts[-1].split("-")[-1]

        headers = Authenticator.get_headers()
        headers["Referer"] = f"https://adventofcode.com/{year}/day/{day}"
        headers["Cookie"] = f"session={session}"

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        method = "GET"
        request = requests.Request(method, url, headers=headers)
        prepped_request = request.prepare()

        with requests.Session() as sess:
            response = sess.send(prepped_request)
            response.raise_for_status()
            return response.text

    @staticmethod
    def download_test_input(day: int, part_num: int) -> str | None:
        """Download test input from the puzzle description for a specific day and part.

        Args:
            day: The day number (1-25) of the puzzle.
            part_num: The puzzle part number (1 or 2).

        Returns
        -------
            The test input content if found, `None` if download fails.

        Note:
            Extracts test input from code blocks in the puzzle description.
            Part number determines which code block to use.
        """
        session = Authenticator.get_session()
        path_obj = Path(Authenticator.get_path())
        year = path_obj.parts[-1].split("-")[-1]

        headers = Authenticator.get_headers()
        headers["Referer"] = f"https://adventofcode.com/{year}/day/{day}"
        headers["Cookie"] = f"session={session}"

        url = f"https://adventofcode.com/{year}/day/{day}"
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            code_elements = [
                element for element in soup.find_all("code") if element.text.count("\n") > 0
            ]
            return code_elements[part_num - 1].text if code_elements else None

        logger.error(f"Error: {response.status_code}")
        return None

    @staticmethod
    def add_day(day: int) -> None:
        """Set up the file structure for a new puzzle day.

        Creates solution file from template and downloads puzzle input when available.
        Waits for puzzle unlock time (5:00 UTC) if necessary.

        Args:
            day: The day number (1-25) to set up.

        Note:
            Creates following structure:
            - `solutions/dayXX.py` (from template)
            - `data/dayXX/puzzle_input.txt`
        """
        path = Authenticator.get_path()
        solution_path = path / f"solutions/day{day:02}.py"

        if not solution_path.exists():
            sample_file = path / "templates/solutions/sample.py"
            content = sample_file.read_text()

            solution_path.write_text(content)
            logger.info(f"Created file: {solution_path}")

        folder_path = path / f"data/day{day:02}"
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / "puzzle_input.txt"
        if not file_path.exists():
            file_path.touch()
            logger.info(f"Created file: {file_path}")

        if file_path.stat().st_size == 0:
            now = datetime.now()
            available_to_download = datetime(int(path.parts[-1].split("-")[-1]), 12, day, 5, 0, 0)

            if now < available_to_download:
                logger.info(
                    "Puzzle input not available to download until",
                    available_to_download.strftime("%Y-%m-%d %H:%M:%S"),
                    "UTC\n",
                )

            while now < available_to_download:
                logger.info("\033[Fnow:", now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], "UTC")
                sleep(1)
                now = datetime.now()

            logger.info("Downloading puzzle input...")
            file_path.write_text(File.download_puzzle_input(day))
            logger.info(f"Downloaded puzzle input to: {file_path}")

    @staticmethod
    def add_test_input(day: int, part_num: int) -> None:
        """Set up and download test input for a specific puzzle part.

        Creates test input file and downloads content when available.
        Waits for puzzle unlock time (5:00 UTC) if necessary.

        Args:
            day: The day number (1-25) of the puzzle.
            part_num: The puzzle part number (1 or 2).

        Note:
            Creates file at: `tests/data/dayXX/test_XX_input.txt`
        """
        path = Authenticator.get_path()
        folder_path = path / f"tests/data/day{day:02}"
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / f"test_{part_num:02d}_input.txt"
        if not file_path.exists():
            file_path.touch()
            logger.info(f"Created test input file: {file_path}")

        if file_path.stat().st_size == 0:
            now = datetime.now()
            available_to_download = datetime(int(path.parts[-1].split("-")[-1]), 12, day, 5, 0, 0)

            if now < available_to_download:
                logger.info(
                    "Test input not available to download until",
                    available_to_download.strftime("%Y-%m-%d %H:%M:%S"),
                    "UTC\n",
                )

            while now < available_to_download:
                logger.info("\033[Fnow:", now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], "UTC")
                sleep(1)
                now = datetime.now()

            logger.info("Downloading test input...")

            # Use the method's return value
            test_input = File.download_test_input(day, part_num)

            # Only write if test input is not None
            if test_input is not None:
                file_path.write_text(test_input)
                logger.info(f"Downloaded test input to: {file_path}")

    @staticmethod
    def add_test_file(day: int) -> None:
        """Create a test file for a specific puzzle day from template.

        Args:
            day: The day number (1-25) to create test file for.

        Note:
            Creates test file at:
                `tests/test_XX.py` using template from `templates/tests/sample.txt`
            Replaces placeholders in template with actual day number.

        Raises
        ------
            FileNotFoundError: If the template file is not found.
        """
        path = Authenticator.get_path()
        test_path = path / f"tests/test_{day:02}.py"

        logger.info(f"Test file path: {test_path}")

        if not test_path.exists():
            sample_file = path / "templates/tests/sample.txt"

            # Explicitly check if the template exists
            if not sample_file.exists():
                error_msg = f"Template file not found: {sample_file}"
                raise FileNotFoundError(error_msg)

            # Read and format content
            content = sample_file.read_text().format(day=day)

            # Write the formatted content
            test_path.write_text(content)
            logger.info(f"Created file: {test_path}")
