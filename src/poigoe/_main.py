from typing import Any

import sounddevice as sd
from numpy import ndarray
from parselmouth import Sound
from parselmouth.praat import call


def change_pitch(sound: Sound, factor: float) -> Sound:
    manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(manipulation, "Extract pitch tier")
    call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, factor)
    call([pitch_tier, manipulation], "Replace pitch tier")
    return call(manipulation, "Get resynthesis (overlap-add)")


def main(pitch: float) -> None:
    def callback(
        indata: ndarray,
        outdata: ndarray,
        frames: int,
        time: Any,
        status: sd.CallbackFlags,
    ) -> None:
        if status:
            print(status)

        sound = Sound(indata.T, sampling_frequency=44100)
        sound = change_pitch(sound, pitch)
        outdata[:] = sound.values.T

    with sd.Stream(channels=2, callback=callback, latency=0.3, samplerate=44100):
        while True:
            sd.sleep(1)
