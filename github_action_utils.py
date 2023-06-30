# type: ignore
"""
Github Action Utils
"""
import os
import subprocess
from typing import Any


class GithubActionUtils:

    @staticmethod
    def markdown_line(line: str) -> None:
        if os.getenv("ENVIRONMENT") != "GITHUB":
            return
        subprocess.run(
            f"echo \"{line}\" >> $GITHUB_STEP_SUMMARY",
            shell=True,
            check=True
        )

    @staticmethod
    def tabulate(headers: list, data: list[list[Any]]) -> None:
        if os.getenv("ENVIRONMENT") != "GITHUB":
            return
        GithubActionUtils.markdown_line("|".join(headers))
        GithubActionUtils.markdown_line("|".join(["---" for _ in headers]))
        for row in data:
            GithubActionUtils.markdown_line("|".join([str(item) for item in row]))
