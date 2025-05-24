from pygame import mixer
import os
from pathlib import Path

# Sound effects and music made using Leshy Labs (https://www.leshylabs.com/)

def load_sounds():
    root_dir = Path(__file__).parent.parent
    sound_path = root_dir / "sounds"
    sounds = {
        "ping": mixer.Sound(os.path.join(sound_path, "ping.wav")),
        "pong": mixer.Sound(os.path.join(sound_path, "pong.wav")),
        "loss": mixer.Sound(os.path.join(sound_path, "loss(1).wav")),
        "alien_crickets": mixer.Sound(os.path.join(sound_path, "alien_crickets.wav")),
        "winner" :mixer.Sound(os.path.join(sound_path, "winner.wav")),
        "get_ready" :mixer.Sound(os.path.join(sound_path, "ready(4).wav")),
        "loser" :mixer.Sound(os.path.join(sound_path, "loser.wav"))
    }

    for sound in sounds.values():
        sound.set_volume(0.1)  
    mixer.music.load(os.path.join(sound_path, "background_sounds(1).wav"))
    mixer.music.set_volume(0.25)

    return sounds
