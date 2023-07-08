"""Command line script to do the acid-kaleidoscope effect"""
from typing import Dict
from image import ImageProcess
from logger import Logger
from stream_input import InputStream, InputQueue
from stream_output import OutputStream

config: Dict = {
    "input_pattern": "raw-video/done/candles-00005.mp4",
    "output_template": "video/just-testing.mp4",
    "output_seconds": 60,
    "input_frames": 1,
    "image_blend": 0.2,
    "scope_adjust": 36.0,
    "rotation_increment": 0.12,
    "scaler_steps": 800,
    "scaler_min": 1.0,
    "scaler_max": 3.0,
    "scaler_start_pos": 3.0,
}

logger = Logger()
stream_input = InputStream(InputQueue(config["input_pattern"]), logger.input_finished)
output_stream = OutputStream(config, stream_input.attributes, logger.output_finished)
image_process = ImageProcess(config, stream_input.attributes)
while True:
    in_bytes = stream_input.read()
    if len(in_bytes) == 0:
        break
    image_process.process(in_bytes, output_stream.write)
output_stream.close()
image_process.clean_up()
