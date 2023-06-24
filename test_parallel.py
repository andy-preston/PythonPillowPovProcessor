"""Test to process input streams into an output stream in parallel"""
from imports.stream_input import InputStream, InputQueue
from imports import stream_output


def finished_in(filename: str):
    """dummy callback for the input stream finished event"""
    print(f"\n\n\nfinished input {filename}\n\n\n")


# call backs should also provide a frame number?
def finished_out(filename: str):
    """dummy callback for the output stream finished event"""
    print(f"\n\n\nfinished output {filename}\n\n\n")


input_queue = InputQueue("raw-video/dock*")
input1 = InputStream(input_queue, finished_in)
input2 = InputStream(input_queue, finished_in)
stream_output.initialise(
    {
        "output_template": "video/test.mp4",
        "output_seconds": 60,
    },
    input1.attributes,  # We need to make sure both streams match!
    finished_out,
)
while True:
    raw_bytes = input1.read()
    if len(raw_bytes) == 0:
        break
    stream_output.write(raw_bytes)

    raw_bytes = input2.read()
    if len(raw_bytes) == 0:
        break
    stream_output.write(raw_bytes)

stream_output.close()
input2.close()
input1.close()
