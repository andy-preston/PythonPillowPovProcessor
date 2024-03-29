"""Module to provide PovScope class"""
import subprocess
from typing import Tuple, Dict, TextIO
from scaler import Scaler


class PovScope:
    """Pov-Ray Kaleidoscope"""

    _fixed_options: Tuple
    _rotation: float
    _config: Dict
    _scaler: Scaler

    def __init__(self, config: Dict, attributes: Dict[str, int]):
        self._config = config
        flat_scale_x: float = float(attributes["aspect_x"]) * config["scope_adjust"]
        flat_scale_y: float = float(attributes["aspect_y"]) * config["scope_adjust"]
        self._fixed_options = (
            "Display=off",
            "Verbose=off",
            "Antialias=on",
            "Sampling_Method=1",
            "Antialias_Threshold=0.5",
            "Antialias_Depth=2",
            "Pause_when_Done=off",
            "Input_File_Name=povray/scope.pov",
            "Output_File_name=tmp/scope.png",
            f"Width={attributes['width']}",
            f"Height={attributes['height']}",
            f"Declare=flat_scale_x={flat_scale_x}",
            f"Declare=flat_scale_y={flat_scale_y}",
        )
        self._scaler = Scaler(config)
        self._rotation = 0.0
        with self._log_file("w") as log_file:
            log_file.write("")

    def _log_file(self, mode: str):
        return open("tmp/scope.log", mode, encoding="utf-8")

    def _variable_options(self):
        self._rotation = self._rotation + self._config["rotation_increment"]
        if self._rotation > 360.0:
            self._rotation = self._rotation - 360.0
        scope_scale = self._scaler.scale()
        return (
            f"Declare=scope_scale={scope_scale}",
            f"Declare=scope_rotation={self._rotation}",
        )

    def render(self):
        """render a single frame"""
        file: TextIO
        with open("tmp/scope.ini", "w", encoding="utf-8") as file:
            file.write("\n".join(self._fixed_options + self._variable_options()) + "\n")
        with self._log_file("a") as log_file:
            subprocess.run(["povray", "tmp/scope.ini"], stderr=log_file, check=True)
