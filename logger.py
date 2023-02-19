from typing import List
from pathlib import Path


_file_list: List


def initialise():
    global _file_list
    _file_list = []


def input_finished(filename: str):
    global _file_list
    _file_list.append(filename)


def output_finished(filename: str):
    global _file_list
    path = Path(filename)
    with open(path.with_suffix(".log"), "w") as log_file:
        log_file.write("\n".join(_file_list) + "\n")
    _file_list = []


if __name__ == "__main__":
    initialise()
    out: int
    for out in range(1, 4):
        out_name: str = f"test-data/dummy-{out}.log"
        inp: int
        for inp in range(1, 4):
            inp_name: str = f"test-data/dummy{inp}.vid"
            input_finished(inp_name)
        output_finished(out_name)
