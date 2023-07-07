"""Module to provide Scope class"""
import subprocess
from typing import Tuple, Dict, TextIO
from imports.scaler import Scaler


class Scope:
    """Pov-Ray Kaleidoscope"""

    _fixed_options: Tuple
    _rotation: float
    _log_file: TextIO = None
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
        self._log_file = open("tmp/scope.log", "w", encoding="utf-8")

    def _variable_options(self):
        self._rotation = self._rotation + self._config["rotation_increment"]
        if self._rotation > 360.0:
            self._rotation = self._rotation - 360.0
        scope_scale = self._scaler.scale()
        return (
            f"Declare=scope_scale={scope_scale}",
            f"Declare=scope_rotation={self._rotation}",
        )

    def clean_up(self):
        """close the log file before finishing"""
        self._log_file.close()

    def render(self):
        """render a single frame"""
        file: TextIO
        with open("tmp/scope.ini", "w", encoding="utf-8") as file:
            file.write("\n".join(self._fixed_options + self._variable_options()) + "\n")
        subprocess.run(["povray", "tmp/scope.ini"], stderr=self._log_file, check=True)
