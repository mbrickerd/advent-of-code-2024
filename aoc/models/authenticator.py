"""
Utility for managing Advent of Code authentication credentials.

Provides methods to retrieve project paths and authentication details
for interacting with the Advent of Code platform.
"""

import json
import os
from pathlib import Path
import sys


class Authenticator:
    """Utility class for retrieving Advent of Code authentication details."""

    @staticmethod
    def get_path() -> Path:
        """
        Determine the absolute path to the project directory.

        Returns
        -------
            Path to the directory containing the current script or script's parent.
        """
        path = os.path.realpath(sys.argv[0])
        return Path(path).parent if not Path(path).is_dir() else Path(path)

    @staticmethod
    def get_session() -> str:
        """
        Retrieve the Advent of Code session token from a local file.

        Returns
        -------
            Stripped session token for authentication.

        Raises
        ------
            FileNotFoundError: If the session file is missing.
            IOError: If there are issues reading the session file.
        """
        session_path = Authenticator.get_path() / "aoc_session"
        return session_path.read_text().strip()

    @staticmethod
    def get_headers() -> dict[str, str]:
        """
        Load HTTP headers configuration from a JSON file.

        Returns
        -------
            Dictionary of HTTP headers for API requests.

        Raises
        ------
            FileNotFoundError: If the headers configuration file is missing.
            json.JSONDecodeError: If the JSON is malformed.
        """
        headers_config_path = Authenticator.get_path() / "aoc_headers.json"
        headers: dict[str, str] = json.loads(headers_config_path.read_text().strip())
        return headers
