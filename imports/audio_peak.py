"""Module providing AudioPeak class"""

from soundfile import SoundFile
import numpy
from numpy.typing import NDArray
import ffmpeg


class AudioPeak:
    """A peak-detecting audio input stream"""

    _samples_per_frame: int
    _audio: SoundFile
    _samples: NDArray
    _peak: int

    def __init__(self, filename: str, frames_per_second: int, peak: int):
        self._audio = SoundFile(filename, "rb")
        self._samples_per_frame = int(self._audio.samplerate / frames_per_second)
        self._peak = peak

    def peak(self) -> bool:
        """Detect peaks in current frame"""
        for sample in self._samples:
            for channel in sample:
                if channel > self._peak:
                    return True
        return False

    def read(self) -> bool:
        """Read the next frame from the current stream"""
        self._samples = self._audio.read(
            frames=self._samples_per_frame, always_2d=True, dtype="int16"
        )
        return len(self._samples) > 0


if __name__ == "__main__":
    audioPeak = AudioPeak("test-data/stereo.wav", 25, 32000)
    count = 0
    while audioPeak.read():
        count = count + 1
        if audioPeak.peak():
            print(f"{count} peak")
    print(count)
