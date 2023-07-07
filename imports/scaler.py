"""Module provides the Scaler class"""
from typing import Dict
import math


class Scaler:
    """Scale the scope based on the current frame position"""

    _direction: int
    _position: int
    _min_log: float
    _scale: float
    _config: Dict

    def __init__(self, config: Dict):
        self._config = config
        self._min_log = math.log(config["scaler_min"])
        self._scale = (math.log(config["scaler_max"]) - self._min_log) / config[
            "scaler_steps"
        ]
        self._direction = 1
        self._position = config["scaler_start_pos"]

    def scale(self):
        """Give the scale factor to pass on to the raytracer"""
        if self._position >= self._config["scaler_steps"] or self._position <= 0:
            self._direction = -self._direction
        self._position = self._position + self._direction
        return math.exp(self._min_log + self._scale * self._position)


def testing():
    """Simple test of the Scaler class"""
    test_config = {
        "scaler_steps": 100,
        "scaler_min": 1.5,
        "scaler_max": 5.0,
        "scaler_start_pos": 3.0,
    }
    scaler = Scaler(test_config)
    for step in range(0, test_config["scaler_steps"] * 3):
        value = scaler.scale()
        print(f"{step} {value}")


if __name__ == "__main__":
    testing()
