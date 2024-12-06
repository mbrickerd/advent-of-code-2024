import json
import os
import re
import sys
import urllib.parse
import urllib.request
from typing import Dict

from loguru import logger


class Submission:
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
        path = Submission.get_path()
        session_path = os.path.realpath(f"{path}/aoc_session")

        with open(session_path, "r") as f:
            session = f.read().strip()

        return session

    @staticmethod
    def get_headers() -> Dict[str, str]:
        headers = {}
        path = Submission.get_path()
        headers_config_path = os.path.realpath(f"{path}/aoc_headers.json")

        with open(headers_config_path, "r") as f:
            headers = json.loads(f.read().strip())

        return headers

    @staticmethod
    def submit(day: int, level: int, answer: int) -> None:
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
