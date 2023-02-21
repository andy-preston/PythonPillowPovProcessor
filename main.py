from typing import Dict
import image
import logger
import stream_input
import stream_output

config: Dict = {
    "input_pattern": "raw-video/*.MTS",
    "output_template": "video/scope.mp4",
    "output_seconds": 60,
    "input_frames": 3,
    "image_blend": 0.2,
    "rotation_increment": 0.08,
    "scaler_steps": 1000,
    "scaler_min": 1.5,
    "scaler_max": 5.0,
    "scaler_start_pos": 3.0,
}

logger.initialise()
stream_input.initialise(config["input_pattern"], logger.input_finished)
stream_output.initialise(config, stream_input.attributes, logger.output_finished)
image.initialise(config, stream_input.attributes)
while True:
    in_bytes = stream_input.read()
    if len(in_bytes) == 0:
        break
    image.process(in_bytes, stream_output.write)
stream_output.close()
stream_input.close()
image.clean_up()
