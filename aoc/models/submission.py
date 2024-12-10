import json
import os
import re
import sys
import urllib.parse
import urllib.request
from typing import Dict

from loguru import logger


class Submission:
    """
    Utility class for submitting Advent of Code puzzle answers.

    This class handles the authentication and submission process for puzzle solutions,
    including parsing and displaying the server's response.
    """

    @staticmethod
    def get_path() -> str:
        """
        Get the absolute path to the project directory.

        Returns:
            str: Absolute path to either the directory containing the script or
                 the script's directory if it is itself a directory.
        """
        return path if os.path.isdir(path := os.path.realpath(sys.argv[0])) else os.path.dirname(path)

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
        path = Submission.get_path()
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
        path = Submission.get_path()
        headers_config_path = os.path.realpath(f"{path}/aoc_headers.json")

        with open(headers_config_path, "r") as f:
            headers = json.loads(f.read().strip())

        return headers

    @staticmethod
    def submit(day: int, level: int, answer: int) -> None:
        """
        Submit a puzzle solution to Advent of Code.

        Makes a POST request to submit the answer and processes the response,
        displaying formatted feedback about whether the answer was correct.

        Args:
            day (int): The day number (1-25) of the puzzle.
            level (int): The part number (1 or 2) of the puzzle.
            answer (int): The calculated answer to submit.

        Note:
            - Formats and displays the server's response, removing boilerplate text
            - Splits response into readable lines
            - Removes common hints/help text
            - Preserves important punctuation in separate lines for readability

        Example:
            >>> Submission.submit(1, 1, 42)
            # Will display something like:
            # "That's the right answer! You earned your first star!"
            # or
            # "That's not the right answer. Your answer is too low."
        """
        session = Submission.get_session()
        year = Submission.get_path().split(os.sep)[-1].split("-")[-1]

        headers = Submission.get_headers()
        headers["Referer"] = f"https://adventofcode.com/{year}/day/{day}"
        headers["Cookie"] = f"session={session}"

        url = f"https://adventofcode.com/{year}/day/{day}/answer"
        method = "POST"
        values = {"level": level, "answer": answer}
        data = urllib.parse.urlencode(values).encode("utf-8")

        req = urllib.request.Request(url, method=method, headers=headers, data=data)

        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")

        # Extract and format the response message
        article = re.findall(r"<article>(.*?)</article>", content, re.DOTALL)[0]
        article = "".join(article.split("</p>"))
        article = article.replace("\n", "")
        article = re.sub(r"<.*?>", "", article, re.DOTALL)
        article = re.sub(r"\[Return.*?\]", "", article, re.DOTALL)
        article = re.sub(r"You\scan\s\[Share.*$", "", article, re.DOTALL)
        article = article.replace("!", "!\n")
        article = article.replace(".", ".\n")
        article = article.replace(".\n)", ".)")

        lines = [
            line
            for line in [line.strip() for line in article.strip().split("\n")]
            if not line.startswith("If you're stuck")
        ]

        for line in lines:
            logger.info(f"\n{line}")
