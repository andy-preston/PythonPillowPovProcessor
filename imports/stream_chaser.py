""""module that provides the StreamChaser class"""
from typing import Tuple
from stream_input import InputStream


class StreamChaser:
    """A list of input streams that we switch between on so many frames processed"""

    _streams: Tuple[InputStream]
    _stream: int

    def __init__(self, streams: Tuple[InputStream]):
        self._streams = streams
        self._stream = 0

    def first_stream(self) -> InputStream:
        """the first stream in the list, so you can get attributes and stuff"""
        return self._streams[0]

    def stream(self, switch: bool) -> InputStream:
        """the stream we're expecting input from"""
        if switch:
            self._stream = self._stream + 1
            if self._stream >= len(self._streams):
                self._stream = 0
        return self._streams[self._stream]
