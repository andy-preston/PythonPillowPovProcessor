"""Module for stream output classes"""
import subprocess
from typing import Tuple, Dict, Callable
import ffmpeg


class OutputSequence:
    """Class to handle outputting in chunks rather than 1 big file"""

    _file_parts: Tuple
    _file_index: int
    _frame_count: int
    _a_minute: int

    def __init__(self, file_template: str, frame_rate: int, output_seconds: int):
        self._file_parts = tuple(file_template.split("."))
        self._file_index = 0
        self._frame_count = -1
        self._a_minute = frame_rate * output_seconds

    def new_file_required(self) -> bool:
        """check to see if a new file is required"""
        self._frame_count = self._frame_count + 1
        result = self._frame_count > self._a_minute or self._frame_count < 1
        if result:
            self._frame_count = 0
        return result

    def filename(self):
        """return the next filename in the sequence"""
        self._file_index = self._file_index + 1
        return self._file_parts[0] + f"-{self._file_index:05d}." + self._file_parts[1]


class OutputStream:
    """Class to handle Output streams"""

    _process: subprocess.Popen
    _buffer_size: int
    _size_string: str
    _finished: Callable
    _filename: str
    _config: Dict
    _output_sequence: OutputSequence

    def __init__(self, config: Dict, attributes: Dict, finished: Callable):
        self._config = config
        self._set_attributes(attributes)
        self._finished = finished
        self._process = None

    def _set_attributes(self, attributes: Dict):
        self._size_string = f"{attributes['width']}x{attributes['height']}"
        self._buffer_size = attributes["buffer_size"]
        self._output_sequence = OutputSequence(
            self._config["output_template"],
            attributes["frame_rate"],
            self._config["output_seconds"],
        )

    def _open(self):
        """open the next stream in the sequence"""
        self.close()
        self._filename = self._output_sequence.filename()
        args = (
            ffmpeg.input(
                "pipe:", format="rawvideo", pix_fmt="rgb24", s=self._size_string
            )
            .output(self._filename, crf="0", pix_fmt="yuv420p")
            .overwrite_output()
            .compile()
        )
        self._process = subprocess.Popen(args, stdin=subprocess.PIPE)

    def write(self, frame_bytes: bytes):
        """write a frame to the stream"""
        if self._output_sequence.new_file_required():
            self._open()
        self._process.stdin.write(frame_bytes)

    def close(self):
        """close the open stream and run the finished callback"""
        if self._process is None:
            return

        self._process.stdin.close()
        self._process.wait()
        if self._finished is None:
            return

        self._finished(self._filename)
