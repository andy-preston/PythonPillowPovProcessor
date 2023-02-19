from typing import Tuple, Dict, TextIO
import scaler
import subprocess


_fixed_options: Tuple
_rotation: float
_log_file: TextIO = None
_config: Dict


def initialise(config: Dict, attributes: Dict[str, int]):
    global _config, _fixed_options, _rotation, _log_file
    _config = config
    flat_scale_x: float = float(attributes["aspect_x"]) * 3.0
    flat_scale_y: float = float(attributes["aspect_y"]) * 3.0
    _fixed_options = (
        "Display=off",
        "Verbose=off",
        "Antialias=on",
        "Sampling_Method=1",
        "Antialias_Threshold=0.5",
        "Antialias_Depth=2",
        "Pause_when_Done=off",
        "Input_File_Name=scope.pov",
        "Output_File_name=tmp/scope.png",
        f"Width={attributes['width']}",
        f"Height={attributes['height']}",
        f"Declare=flat_scale_x={flat_scale_x}",
        f"Declare=flat_scale_y={flat_scale_y}",
    )
    scaler.initialise(config)
    _rotation = 0.0
    _log_file = open("tmp/scope.log", "w")


def _variable_options():
    global _rotation
    _rotation = _rotation + _config["rotation_increment"]
    if _rotation > 360.0:
        _rotation = _rotation - 360.0
    scope_scale = scaler.scale()
    return (
        f"Declare=scope_scale={scope_scale}",
        f"Declare=scope_rotation={_rotation}",
    )


def clean_up():
    global _log_file
    _log_file.close()


def render():
    global _fixed_options, _log_file
    file: TextIO = open("tmp/scope.ini", "w")
    file.write("\n".join(_fixed_options + _variable_options()) + "\n")
    file.close()
    subprocess.run(["povray", "tmp/scope.ini"], stderr=_log_file)
