from datetime import datetime
import json
import os
import sys
import urllib.parse
from urllib.request import Request, urlopen
from pathlib import Path
from time import sleep
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from loguru import logger


class File:
    @staticmethod
    def get_path() -> str:
        return (
            path
            if os.path.isdir(path := os.path.realpath(sys.argv[0]))
            else os.path.dirname(path)
        )

    @staticmethod
    def get_session() -> str:
        session = ""
        path = File.get_path()
        session_path = os.path.realpath(f"{path}/aoc_session")

        with open(session_path, "r") as f:
            session = f.read().strip()

        return session

    @staticmethod
    def get_headers() -> Dict[str, str]:
        headers = {}
        path = File.get_path()
        headers_config_path = os.path.realpath(f"{path}/aoc_headers.json")

        with open(headers_config_path, "r") as f:
            headers = json.loads(f.read().strip())

        return headers

    @staticmethod
    def download_puzzle_input(day: int) -> str:
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
                    "\033[Fnow:", now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], "UTC"
                )
                sleep(1)
                now = datetime.now()

            logger.info("Downloading puzzle input...")
            with open(file_path, "w+") as f:
                f.write(File.download_puzzle_input(day))
                logger.info(f"Downloaded puzzle input to: {file_path}")

    @staticmethod
    def add_test_input(day: int, part_num: int) -> None:
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
                    "\033[Fnow:", now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], "UTC"
                )
                sleep(1)
                now = datetime.now()

            logger.info("Downloading test input...")
            with open(file_path, "w+") as f:
                f.write(File.download_test_input(day, part_num))
                logger.info(f"Downloaded test input to: {file_path}")

    @staticmethod
    def add_test_file(day: int) -> None:
        path = File.get_path()
        test = os.path.realpath(f"{path}/tests/test_{day:02}.py")

        logger.info(f"Test file path: {test}")

        test_path = Path(test)

        if not test_path.exists():
            sample_file = f"{path}/templates/tests/sample.txt"
            if not os.path.exists(sample_file):
                raise FileNotFoundError(f"Template file not found: {sample_file}")

            with open(sample_file, "r") as file:
                content = file.read()

            if content:
                logger.info("Content loaded successfully")

            # Replace placeholders with actual values
            content = content.format(day=day)
            with open(test, "w+") as f:
                f.write(content)
                logger.info(f"Created file: {test}")
