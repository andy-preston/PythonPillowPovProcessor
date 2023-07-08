"""Module providing AudioPeak class"""

from soundfile import SoundFile
import numpy
from numpy.typing import NDArray


class AudioPeak:
    """A peak-detecting audio input stream"""

    _audio: SoundFile
    _samples: NDArray
    _frame_index: int
    _samples_per_frame: int
    _debounce: int
    _peak: float

    def __init__(
        self, filename: str, frames_per_second: int, debounce: int, peak: float
    ):
        self._audio = SoundFile(filename, "rb")
        self._frame_index = 0
        self._samples_per_frame = int(self._audio.samplerate / frames_per_second)
        self._debounce = debounce
        self._peak = peak

    def peak(self) -> bool:
        """Detect peaks in current frame"""
        debounce: bool = self._frame_index > self._debounce
        peak: bool = (
            max(abs(numpy.amin(self._samples)), numpy.amax(self._samples)) > self._peak
        )
        result: bool = debounce and peak
        self._frame_index = 0 if result else self._frame_index + 1
        return result

    def read(self) -> bool:
        """Read the next frame from the stream"""
        self._samples = self._audio.read(frames=self._samples_per_frame)
        return len(self._samples) > 0


def testing():
    """simple testing during development"""
    frames_per_second = 25
    audio_debounce = 2
    audio_peak = 0.9
    audio_peak = AudioPeak(
        "test-data/mono.wav", frames_per_second, audio_debounce, audio_peak
    )
    count = 0
    while audio_peak.read():
        count = count + 1
        if audio_peak.peak():
            print(f"{count} peak")
    print(count)


if __name__ == "__main__":
    testing()
