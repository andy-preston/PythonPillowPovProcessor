import glob
import ffmpeg
import subprocess
from typing import Dict, Callable


attributes: Dict[str, int]
_process: subprocess.Popen
_buffer: bytes
_files: iter
_finished: Callable
_filename: str


def initialise(glob_pattern: str, finished: Callable):
    global _process, _files, _finished
    fileList = glob.glob(glob_pattern)
    fileList.sort()
    _files = iter(fileList)
    _finished = finished
    _process = None
    _open()


def _probe_attributes():
    global attributes, _filename
    probe = ffmpeg.probe(_filename)
    info = next(s for s in probe["streams"] if s["codec_type"] == "video")
    width = int(info["width"])
    height = int(info["height"])
    if "display_aspect_ration" in info:
        aspect = info["display_aspect_ratio"].split(":")
    else:
        aspect = (width / height, 1)
    attributes = {
        "width": width,
        "height": height,
        "buffer_size": width * height * 3,
        "aspect_x": int(aspect[0]),
        "aspect_y": int(aspect[1]),
        "frame_rate": int(info["r_frame_rate"].split("/")[0]),
    }


def _open():
    global _process, _files, _filename
    close()
    _filename = next(_files)
    if _process is None:
        _probe_attributes()
    args = (
        ffmpeg.input(_filename)
        .output("pipe:", format="rawvideo", pix_fmt="rgb24")
        .compile()
    )
    _process = subprocess.Popen(args, stdout=subprocess.PIPE)


def read():
    global _process, _buffer
    _buffer = _process.stdout.read(attributes["buffer_size"])
    if len(_buffer) != 0:
        return _buffer
    else:
        try:
            _open()
        except StopIteration:
            return b""
        # Recursion is a bit "terrifying" - but this should (SHOULD)
        # only ever go to 2 levels. Does Python have tail calls?
        return read()


def close():
    global _process, _finished, _filename
    if _process is not None:
        _process.wait()
        if _finished is not None:
            _finished(_filename)
