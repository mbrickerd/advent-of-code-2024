import json
import os
import sys
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Dict
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from loguru import logger


class File:
    """
    Utility class for managing Advent of Code file operations and puzzle input retrieval.

    This class provides static methods for handling file paths, session management,
    downloading puzzle/test inputs, and setting up solution files. It manages the
    directory structure and timing for puzzle input availability.
    """

    @staticmethod
    def get_path() -> str:
        """
        Get the absolute path to the project directory.

        Returns:
            str: Absolute path to either the directory containing the script or
                the script's directory if it is itself a directory.
        """
        return (
            path
            if os.path.isdir(path := os.path.realpath(sys.argv[0]))
            else os.path.dirname(path)
        )

    @staticmethod
    def get_session() -> str:
        """
        Retrieve the Advent of Code session token from a local file.

        Returns:
            str: The session token stripped of whitespace.

        Note:
            Expects a file named `aoc_session` in the project root directory.
        """
        session = ""
        path = File.get_path()
        session_path = os.path.realpath(f"{path}/aoc_session")

        with open(session_path, "r") as f:
            session = f.read().strip()

        return session

    @staticmethod
    def get_headers() -> Dict[str, str]:
        """
        Load HTTP headers configuration from a JSON file.

        Returns:
            Dict[str, str]: Dictionary of HTTP headers for AoC API requests.

        Note:
            Expects a file named `aoc_headers.json` in the project root directory.
        """
        headers = {}
        path = File.get_path()
        headers_config_path = os.path.realpath(f"{path}/aoc_headers.json")

        with open(headers_config_path, "r") as f:
            headers = json.loads(f.read().strip())

        return headers

    @staticmethod
    def download_puzzle_input(day: int) -> str:
        """
        Download the puzzle input for a specific day from Advent of Code.

        Args:
            day (int): The day number (1-25) of the puzzle.

        Returns:
            str: The puzzle input content.

        Note:
            Requires valid session token and headers configuration.
            Year is determined from the project directory name.
        """
        session = File.get_session()
        year = File.get_path().split(os.sep)[-1].split("-")[-1]

        headers = File.get_headers()
        headers["Referer"] = f"https://adventofcode.com/{year}/day/{day}"
        headers["Cookie"] = f"session={session}"

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        method = "GET"

        request = Request(url, method=method, headers=headers)

        with urlopen(request) as response:
            content = response.read().decode("utf-8")

        return content

    @staticmethod
    def download_test_input(day: int, part_num: int) -> str | None:
        """
        Download test input from the puzzle description for a specific day and part.

        Args:
            day (int): The day number (1-25) of the puzzle.
            part_num (int): The puzzle part number (1 or 2).

        Returns:
            str | None: The test input content if found, `None` if download fails.

        Note:
            Extracts test input from code blocks in the puzzle description.
            Part number determines which code block to use.
        """
        session = File.get_session()
        year = File.get_path().split(os.sep)[-1].split("-")[-1]

        headers = File.get_headers()
        headers["Referer"] = f"https://adventofcode.com/{year}/day/{day}"
        headers["Cookie"] = f"session={session}"

        url = f"https://adventofcode.com/{year}/day/{day}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            code_elements = [
                element
                for element in soup.find_all("code")
                if element.text.count("\n") > 0
            ]
            return code_elements[part_num - 1].text

        else:
            logger.error(f"Error: {response.status_code}")
            return None

    @staticmethod
    def add_day(day: int) -> None:
        """
        Set up the file structure for a new puzzle day.

        Creates solution file from template and downloads puzzle input when available.
        Waits for puzzle unlock time (5:00 UTC) if necessary.

        Args:
            day (int): The day number (1-25) to set up.

        Note:
            Creates following structure:
            - `solutions/dayXX.py` (from template)
            - `data/dayXX/puzzle_input.txt`
        """
        path = File.get_path()
        solution = os.path.realpath(f"{path}/solutions/day{day:02}.py")
        solution_path = Path(solution)

        if not solution_path.exists():
            sample_file = f"{path}/templates/solutions/sample.py"
            with open(sample_file, "r") as file:
                content = file.read()

            with open(solution, "w+") as f:
                f.write(content)
                logger.info(f"Created file: {solution}")

        folder = os.path.realpath(f"{path}/data/day{day:02}")
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)

        file_path = Path(f"{folder}/puzzle_input.txt")
        if not file_path.exists():
            file_path.touch()
            logger.info(f"Created file: {file_path}")

        if file_path.stat().st_size == 0:
            now = datetime.now()
            available_to_download = datetime(
                int(path.split(os.sep)[-1].split("-")[-1]), 12, day, 5, 0, 0
            )

            if now < available_to_download:
                logger.info(
                    "Puzzle input not available to download until",
                    available_to_download.strftime("%Y-%m-%d %H:%M:%S"),
                    "UTC\n",
                )

            while now < available_to_download:
                logger.info(
                    "\033[Fnow:", now.strftime(
                        "%Y-%m-%d %H:%M:%S.%f")[:-3], "UTC"
                )
                sleep(1)
                now = datetime.now()

            logger.info("Downloading puzzle input...")
            with open(file_path, "w+") as f:
                f.write(File.download_puzzle_input(day))
                logger.info(f"Downloaded puzzle input to: {file_path}")

    @staticmethod
    def add_test_input(day: int, part_num: int) -> None:
        """
        Set up and download test input for a specific puzzle part.

        Creates test input file and downloads content when available.
        Waits for puzzle unlock time (5:00 UTC) if necessary.

        Args:
            day (int): The day number (1-25) of the puzzle.
            part_num (int): The puzzle part number (1 or 2).

        Note:
            Creates file at: `data/dayXX/test_XX_input.txt`
        """
        path = File.get_path()
        folder = os.path.realpath(f"{path}/data/day{day:02}")
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)

        file_path = Path(f"{folder}/test_{part_num:02d}_input.txt")
        if not file_path.exists():
            file_path.touch()
            logger.info(f"Created test input file: {file_path}")

        if file_path.stat().st_size == 0:
            now = datetime.now()
            available_to_download = datetime(
                int(path.split(os.sep)[-1].split("-")[-1]), 12, day, 5, 0, 0
            )

            if now < available_to_download:
                logger.info(
                    "Test input not available to download until",
                    available_to_download.strftime("%Y-%m-%d %H:%M:%S"),
                    "UTC\n",
                )

            while now < available_to_download:
                logger.info(
                    "\033[Fnow:", now.strftime(
                        "%Y-%m-%d %H:%M:%S.%f")[:-3], "UTC"
                )
                sleep(1)
                now = datetime.now()

            logger.info("Downloading test input...")
            with open(file_path, "w+") as f:
                f.write(File.download_test_input(day, part_num))
                logger.info(f"Downloaded test input to: {file_path}")

    @staticmethod
    def add_test_file(day: int) -> None:
        """
        Create a test file for a specific puzzle day from template.

        Args:
            day (int): The day number (1-25) to create test file for.

        Note:
            Creates test file at: `tests/test_XX.py` using template from `templates/tests/sample.txt`
            Replaces placeholders in template with actual day number.

        Raises:
            FileNotFoundError: If the template file is not found.
        """
        path = File.get_path()
        test = os.path.realpath(f"{path}/tests/test_{day:02}.py")

        logger.info(f"Test file path: {test}")

        test_path = Path(test)

        if not test_path.exists():
            sample_file = f"{path}/templates/tests/sample.txt"
            if not os.path.exists(sample_file):
                raise FileNotFoundError(
                    f"Template file not found: {sample_file}")

            with open(sample_file, "r") as file:
                content = file.read()

            if content:
                logger.info("Content loaded successfully")

            content = content.format(day=day)
            with open(test, "w+") as f:
                f.write(content)
                logger.info(f"Created file: {test}")
