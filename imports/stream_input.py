"""Module providing StreamInput class"""

import glob
import subprocess
from typing import Dict, Callable
import ffmpeg


class InputQueue:
    """A list of files to be read by InputStream either in series or parallel"""

    _files: iter

    def __init__(self, glob_pattern: str):
        file_list = glob.glob(glob_pattern)
        file_list.sort()
        self._files = iter(file_list)

    def next(self) -> str:
        """Give the next filename in the list"""
        return next(self._files)


class InputStream:
    """An input stream from ffmpeg"""

    attributes: Dict[str, int]
    _process: subprocess.Popen
    _buffer: bytes
    _finished: Callable
    _filename: str
    _input_queue: InputQueue

    def __init__(self, input_queue: InputQueue, finished: Callable):
        self._input_queue = input_queue
        self._finished = finished
        self._process = None
        self._open()

    def _probe_attributes(self):
        probe = ffmpeg.probe(self._filename)
        info = next(s for s in probe["streams"] if s["codec_type"] == "video")
        width = int(info["width"])
        height = int(info["height"])
        if "display_aspect_ration" in info:
            aspect = info["display_aspect_ratio"].split(":")
        else:
            aspect = (width / height, 1)
        self.attributes = {
            "width": width,
            "height": height,
            "buffer_size": width * height * 3,
            "aspect_x": int(aspect[0]),
            "aspect_y": int(aspect[1]),
            "frame_rate": int(info["r_frame_rate"].split("/")[0]),
        }

    def _open(self):
        self.close()
        self._filename = self._input_queue.next()
        if self._process is None:
            self._probe_attributes()
        args = (
            ffmpeg.input(self._filename)
            .output("pipe:", format="rawvideo", pix_fmt="rgb24")
            .compile()
        )
        self._process = subprocess.Popen(args, stdout=subprocess.PIPE)

    def read(self):
        """Read the next frame from the current stream"""
        self._buffer = self._process.stdout.read(self.attributes["buffer_size"])
        if len(self._buffer) != 0:
            return self._buffer

        try:
            self._open()
        except StopIteration:
            return b""
        # Recursion is a bit "terrifying" - but this should (SHOULD)
        # only ever go to 2 levels. Does Python have tail calls?
        return self.read()

    def close(self):
        """Close the current stream if it's open - wait for process to finish"""
        if self._process is None:
            return

        self._process.wait()

        if self._finished is not None:
            self._finished(self._filename)
