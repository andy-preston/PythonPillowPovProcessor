"""Edit, switching from multiple input streams on the beat"""
from typing import Dict
from imports import logger
from imports.stream_input import InputStream, InputQueue
from imports import stream_output
from imports.stream_chaser import StreamChaser

config: Dict = {
    "input_pattern": "raw-video/edit-test*",
    "output_template": "video/edit.mp4",
    "output_seconds": 60,
    "chunk_frames": 11,
}

logger.initialise()
input_queue = InputQueue(config["input_pattern"])
streams = list(
    map(
        (lambda _: InputStream(input_queue, logger.input_finished)),
        range(input_queue.number_of_streams),
    )
)
stream_chaser = StreamChaser(config["chunk_frames"], streams)
stream_output.initialise(
    config, stream_chaser.first_stream().attributes, logger.output_finished
)
while True:
    raw_bytes = stream_chaser.stream().read()
    if len(raw_bytes) == 0:
        break
    stream_output.write(raw_bytes)

stream_output.close()
