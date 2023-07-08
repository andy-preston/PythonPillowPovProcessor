"""module to provide ImageProcess class"""
from typing import Tuple, Dict, Callable
from PIL import Image
from pov_scope import PovScope


class ImageProcess:
    """Blend kaleidoscopic images into output buffer"""

    _size: Tuple[int, int]
    _overlay: Image
    _config: Dict
    _pov_scope: PovScope

    def __init__(self, config: Dict, attributes: Dict[str, int]):
        self._config = config
        self._size = (attributes["width"], attributes["height"])
        self._pov_scope = PovScope(config, attributes)
        self._overlay = Image.new("RGB", self._size, (0, 0, 0))

    def _save_flat(self, in_raw: bytes):
        incoming: Image
        with Image.frombytes("RGB", self._size, in_raw) as incoming:
            incoming.save("tmp/flat.png")

    def _blend_in(self):
        with Image.open("tmp/scope.png") as scope_image:
            with Image.blend(
                self._overlay, scope_image, self._config["image_blend"]
            ) as blended:
                self._overlay.paste(blended)

    def process(self, in_raw: bytes, sink: Callable[[bytes], None]):
        """blend the new 'scoped' image with the buffer and send it on to a sink"""
        self._save_flat(in_raw)
        for _ in range(0, self._config["input_frames"]):
            self._pov_scope.render()
            self._blend_in()
            sink(self._overlay.tobytes())


def testing():
    """Basic test routine for ImageProcess"""
    input_image: Image = Image.open("test-data/picture.jpg")
    test_config = {
        "input_frames": 1,
        "image_blend": 0.2,
        "scaler_steps": 100,
        "scaler_min": 1.5,
        "scaler_max": 5.0,
        "scaler_start_pos": 3.0,
        "rotation_increment": 0.08,
        "scope_adjust": 1,
    }
    test_attributes = {
        "width": input_image.size[0],
        "height": input_image.size[1],
        "aspect_x": 5,
        "aspect_y": 4,
    }
    image_process = ImageProcess(test_config, test_attributes)

    def sink(raw: bytes):
        """Save the test image - mock image sink"""
        Image.frombytes("RGB", input_image.size, raw).save("test-data/test-out.jpg")

    image_process.process(input_image.tobytes(), sink)


if __name__ == "__main__":
    testing()
