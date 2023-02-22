import ffmpeg
import subprocess
from typing import Tuple, Dict, Callable


_process: subprocess.Popen
_buffer_size: int
_size_string: str
_frame_count: int
_a_minute: int
_file_parts: Tuple
_file_index: int
_finished: Callable
_filename: str
_config: Dict


def initialise(config: Dict, attributes: Dict, finished: Callable):
    global _process, _finished, _config
    _config = config
    _set_attributes(attributes)
    _file_list(config["output_template"])
    _finished = finished
    _process = None


def _set_attributes(attributes: Dict):
    global _buffer_size, _size_string, _a_minute, _frame_count, _config
    _size_string = f"{attributes['width']}x{attributes['height']}"
    _buffer_size = attributes["buffer_size"]
    _a_minute = attributes["frame_rate"] * _config["output_seconds"]
    _frame_count = 0


def _file_list(base: str):
    global _file_index, _file_parts
    _file_parts = tuple(base.split("."))
    _file_index = 0


def _open():
    global _process, _size_string, _file_parts, _file_index, _filename
    close()
    _file_index = _file_index + 1
    _filename = _file_parts[0] + f"-{_file_index:05d}." + _file_parts[1]
    args = (
        ffmpeg.input("pipe:", format="rawvideo", pix_fmt="rgb24", crf="0", s=_size_string)
        .output(_filename, pix_fmt="yuv420p")
        .overwrite_output()
        .compile()
    )
    _process = subprocess.Popen(args, stdin=subprocess.PIPE)


def write(frame_bytes: bytes):
    global _process, _frame_count, _a_minute
    if _frame_count >= _a_minute or _process is None:
        _open()
        _frame_count = 0
    _frame_count = _frame_count + 1
    _process.stdin.write(frame_bytes)


def close():
    global _process, _finished, _filename
    if _process is not None:
        _process.stdin.close()
        _process.wait()
        if _finished is not None:
            _finished(_filename)
