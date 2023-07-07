"""Module provides the Logger class"""
from typing import List
from pathlib import Path


class Logger:
    """Log the progress of stream reading and writing to text files"""

    _file_list: List

    def __init__(self):
        self._file_list = []

    def input_finished(self, filename: str):
        """Logging function for when an input stream has finished"""
        self._file_list.append(filename)

    def output_finished(self, filename: str):
        """Logging function for when an output stream has finished"""
        path = Path(filename)
        with open(path.with_suffix(".log"), "w", encoding="utf-8") as log_file:
            log_file.write("\n".join(self._file_list) + "\n")
        self._file_list = []


def testing():
    """test the Logger class"""
    logger = Logger()
    out: int
    for out in range(1, 4):
        out_name: str = f"test-data/dummy-{out}.log"
        inp: int
        for inp in range(1, 4):
            inp_name: str = f"test-data/dummy{inp}.vid"
            logger.input_finished(inp_name)
        logger.output_finished(out_name)


if __name__ == "__main__":
    testing()
