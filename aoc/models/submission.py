"""
Solution submission module for Advent of Code.

This module provides the Submission class with utilities for authenticating and submitting
puzzle solutions to the Advent of Code website, as well as parsing and displaying the
server's response.
"""

from pathlib import Path
import re
import urllib.parse
import urllib.request

from loguru import logger

from aoc.models.authenticator import Authenticator


class Submission:
    """Utility class for submitting Advent of Code puzzle answers.

    This class handles the authentication and submission process for puzzle solutions,
    including parsing and displaying the server's response.
    """

    @staticmethod
    def submit(day: int, level: int, answer: int) -> None:
        """Submit a puzzle solution to Advent of Code.

        Makes a POST request to submit the answer and processes the response,
        displaying formatted feedback about whether the answer was correct.

        Args:
            day: The day number (1-25) of the puzzle.
            level: The part number (1 or 2) of the puzzle.
            answer: The calculated answer to submit.

        Note:
            - Formats and displays the server's response, removing boilerplate text
            - Splits response into readable lines
            - Removes common hints/help text
            - Preserves important punctuation in separate lines for readability
        """
        session = Authenticator.get_session()
        path_obj = Path(Authenticator.get_path())
        year = path_obj.parts[-1].split("-")[-1]

        headers = Authenticator.get_headers()
        headers["Referer"] = f"https://adventofcode.com/{year}/day/{day}"
        headers["Cookie"] = f"session={session}"

        url = f"https://adventofcode.com/{year}/day/{day}/answer"
        method = "POST"
        values = {"level": level, "answer": answer}
        data = urllib.parse.urlencode(values).encode("utf-8")
        req = urllib.request.Request(url, method=method, headers=headers, data=data)  # noqa: S310

        with urllib.request.urlopen(req) as response:  # noqa: S310
            content = response.read().decode("utf-8")

        # Extract and format the response message
        article_matches = re.findall(r"<article>(.*?)</article>", content, re.DOTALL)
        if not article_matches:
            logger.error("No response article found")
            return

        article = article_matches[0]
        article = "".join(article.split("</p>"))
        article = article.replace("\n", "")
        article = re.sub(pattern=r"<.*?>", repl="", string=article, flags=re.DOTALL)
        article = re.sub(pattern=r"\[Return.*?\]", repl="", string=article, flags=re.DOTALL)
        article = re.sub(pattern=r"You\scan\s\[Share.*$", repl="", string=article, flags=re.DOTALL)
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
