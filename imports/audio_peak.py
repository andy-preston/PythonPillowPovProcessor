"""Module providing AudioPeak class"""

from soundfile import SoundFile
import numpy
from numpy.typing import NDArray


class AudioPeak:
    """A peak-detecting audio input stream"""

    _samples_per_frame: int
    _audio: SoundFile
    _samples: NDArray
    _peak: float

    def __init__(self, filename: str, frames_per_second: int, peak: float):
        self._peak = peak
        self._audio = SoundFile(filename, "rb")
        self._samples_per_frame = int(self._audio.samplerate / frames_per_second)

    def peak(self) -> bool:
        """Detect peaks in current frame"""
        return (
            max(abs(numpy.amin(self._samples)), numpy.amax(self._samples)) > self._peak
        )

    def read(self) -> bool:
        """Read the next frame from the stream"""
        self._samples = self._audio.read(frames=self._samples_per_frame)
        return len(self._samples) > 0


def testing():
    """simple testing during development"""
    audio_peak = AudioPeak("test-data/mono.wav", 25, 0.9)
    count = 0
    while audio_peak.read():
        count = count + 1
        if audio_peak.peak():
            print(f"{count} peak")
    print(count)


if __name__ == "__main__":
    testing()
