import stream_input
import stream_output


def finished_in(filename: str):
    print(f"\n\n\nfinished input {filename}\n\n\n")


def finished_out(filename: str):
    print(f"\n\n\nfinished output {filename}\n\n\n")


if __name__ == "__main__":
    stream_input.initialise("raw-video/012*", finished_in)
    stream_output.initialise(
        {
            "output_template": "test-data/test.mp4",
            "output_seconds": 60,
        },
        stream_input.attributes,
        finished_out,
    )
    while True:
        in_bytes = stream_input.read()
        if len(in_bytes) == 0:
            break
        stream_output.write(in_bytes)
    stream_output.close()
    stream_input.close()
