"""Edit, switching from multiple input streams on the beat"""
from typing import Dict
from imports import logger
from imports.stream_input import InputStream, InputQueue
from imports.stream_output import OutputStream
from imports.stream_chaser import StreamChaser
from imports.audio_peak import AudioPeak

config: Dict = {
    "audio_track": "raw-video/side2-track2.wav",
    "audio_peak": 0.6,
    "input_pattern": "raw-video/edit-test*",
    "output_template": "video/edit.mp4",
    "output_seconds": 60,
}

logger.initialise()
input_queue = InputQueue(config["input_pattern"])
streams = list(
    map(
        (lambda _: InputStream(input_queue, logger.input_finished)),
        range(input_queue.number_of_streams),
    )
)
stream_chaser = StreamChaser(streams)
attributes = stream_chaser.first_stream().attributes
audio_peak = AudioPeak(
    config["audio_track"], attributes["frame_rate"], config["audio_peak"]
)
output_stream = OutputStream(config, attributes, logger.output_finished)
while audio_peak.read():
    raw_bytes = stream_chaser.stream(audio_peak.peak()).read()
    if len(raw_bytes) == 0:
        break
    output_stream.write(raw_bytes)

output_stream.close()
