from PIL import Image
from typing import Tuple, Dict
import scope


_size: Tuple[int, int]
_overlay: Image
_config: Dict


def initialise(config: Dict, attributes: Dict[str, int]):
    global _size, _overlay, _config
    _config = config
    _size = (attributes["width"], attributes["height"])
    scope.initialise(config, attributes)
    _overlay = Image.new("RGB", _size, (0, 0, 0))


def _blend_in(input_image: Image):
    global _config
    blended = Image.blend(_overlay, input_image, _config["image_blend"])
    try:
        _overlay.paste(blended)
    finally:
        del blended


def process(in_raw: bytes) -> bytes:
    global _size, _config
    incoming: Image = Image.frombytes("RGB", _size, in_raw)
    try:
        incoming.save("tmp/flat.png")
    finally:
        del incoming
    for frame in range(0, _config["input_frames"]):
        scope.render()
        scope_image: Image = Image.open("tmp/scope.png")
        try:
            _blend_in(scope_image)
        finally:
            del scope_image
    return _overlay.tobytes()


def clean_up():
    scope.clean_up()


if __name__ == "__main__":
    input_image = Image.open("test-data/test-in.jpg")
    initialise(
        {
            "input_frames": 1,
            "image_blend": 0.2,
            "scaler_steps": 100,
            "scaler_min": 1.5,
            "scaler_max": 5.0,
            "scaler_start_pos": 3.0,
            "rotation_increment": 0.08,
        },
        {
            "width": input_image.size[0],
            "height": input_image.size[1],
            "aspect_x": 5,
            "aspect_y": 4,
        },
    )
    raw = process(input_image.tobytes())
    output_image = Image.frombytes("RGB", _size, raw)
    output_image.save("test-data/test-out.jpg")
    clean_up()
