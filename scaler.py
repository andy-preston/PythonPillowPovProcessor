from typing import Dict
import math

_direction: int
_position: int
_min_log: float
_scale: float
_config: Dict


def initialise(config: Dict):
    global _config, _min_log, _scale, _direction, _position
    _config = config
    _min_log = math.log(_config["scaler_min"])
    _scale = (math.log(_config["scaler_max"]) - _min_log) / _config["scaler_steps"]
    _direction = 1
    _position = _config["scaler_start_pos"]


def scale():
    global _config, _min_log, _scale, _direction, _position
    if _position >= _config["scaler_steps"] or _position <= 0:
        _direction = -_direction
    _position = _position + _direction
    return math.exp(_min_log + _scale * _position)


if __name__ == "__main__":
    initialise(
        {
            "scaler_steps": 100,
            "scaler_min": 1.5,
            "scaler_max": 5.0,
            "scaler_start_pos": 3.0,
        }
    )
    for step in range(0, _config["scaler_steps"] * 3):
        value = scale()
        print(f"{step} {value}")
