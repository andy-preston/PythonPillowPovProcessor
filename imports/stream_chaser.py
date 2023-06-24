""""module that provides the StreamChaser class"""
from typing import Tuple
from imports.stream_input import InputStream


class StreamChaser:
    """A list of input streams that we switch between on so many frames processed"""

    _streams: Tuple[InputStream]
    _chunk_frames: int
    _frame: int
    _stream: int

    def __init__(self, chunk_frames: int, streams: Tuple[InputStream]):
        self._streams = streams
        self._chunk_frames = chunk_frames
        self._frame = 0
        self._stream = 0

    def _switch(self):
        self._frame = self._frame + 1
        if self._frame == self._chunk_frames:
            self._frame = 0
            return True
        return False

    def _stream_index(self):
        if not self._switch():
            return self._stream
        self._stream = self._stream + 1
        if self._stream >= len(self._streams):
            self._stream = 0
        return self._stream

    def first_stream(self) -> InputStream:
        """the first stream in the list, so you can get attributes and stuff"""
        return self._streams[0]

    def stream(self) -> InputStream:
        """the stream we're expecting input from"""
        return self._streams[self._stream_index()]
