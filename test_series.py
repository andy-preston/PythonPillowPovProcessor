"""Test to process input streams into an output stream in series"""

from stream_input import InputStream, InputQueue
from stream_output import OutputStream


def finished_in(filename: str):
    """dummy callback for the input stream finished event"""
    print(f"\n\n\nfinished input {filename}\n\n\n")


def finished_out(filename: str):
    """dummy callback for the output stream finished event"""
    print(f"\n\n\nfinished output {filename}\n\n\n")


input_stream = InputStream(InputQueue("raw-video/dock*"), finished_in)
output_stream = OutputStream(
    {
        "output_template": "test-data/video.mp4",
        "output_seconds": 60,
    },
    input_stream.attributes,
    finished_out,
)
while True:
    raw_bytes = input_stream.read()
    if len(raw_bytes) == 0:
        break
    output_stream.write(raw_bytes)
output_stream.close()
