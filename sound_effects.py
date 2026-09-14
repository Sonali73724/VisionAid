import os
import wave
import struct
import math
import time
import winsound
import threading

SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")
os.makedirs(SOUNDS_DIR, exist_ok=True)

def _generate_wav(filepath, duration_sec, freq_left=0, freq_right=0, sample_rate=44100):
    """Generate a clean 16-bit stereo WAV file with smooth attack/decay envelope."""
    n_samples = int(sample_rate * duration_sec)
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(2)      # Stereo
        wav_file.setsampwidth(2)     # 16-bit
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        for i in range(n_samples):
            t = float(i) / sample_rate
            # Smooth trapezoidal/cosine envelope to prevent popping
            envelope = math.sin(math.pi * (i / float(n_samples)))

            val_l = 0
            if freq_left > 0:
                val_l = int(32767 * 0.7 * envelope * math.sin(2 * math.pi * freq_left * t))

            val_r = 0
            if freq_right > 0:
                val_r = int(32767 * 0.7 * envelope * math.sin(2 * math.pi * freq_right * t))

            frames.extend(struct.pack("<hh", max(-32767, min(32767, val_l)), max(-32767, min(32767, val_r))))

        wav_file.writeframes(frames)


def _generate_two_tone_wav(filepath, duration_sec=0.20, f1=987, f2=1318, sample_rate=44100):
    """Generate harmonic two-tone lock chime."""
    n_samples = int(sample_rate * duration_sec)
    half = n_samples // 2
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        for i in range(n_samples):
            t = float(i) / sample_rate
            env = math.sin(math.pi * (i / float(n_samples)))
            freq = f1 if i < half else f2
            val = int(32767 * 0.75 * env * math.sin(2 * math.pi * freq * t))
            frames.extend(struct.pack("<hh", val, val))
        wav_file.writeframes(frames)


def ensure_all_sounds():
    """Ensure all required sound assets exist."""
    files = {
        "radar_left.wav": lambda p: _generate_wav(p, 0.08, freq_left=880, freq_right=0),
        "radar_right.wav": lambda p: _generate_wav(p, 0.08, freq_left=0, freq_right=880),
        "radar_center.wav": lambda p: _generate_wav(p, 0.10, freq_left=1200, freq_right=1200),
        "beacon_ping.wav": lambda p: _generate_wav(p, 0.06, freq_left=1050, freq_right=1050),
        "beacon_lock.wav": lambda p: _generate_two_tone_wav(p, 0.18, 987, 1318),
    }
    for filename, generator in files.items():
        target = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(target) or os.path.getsize(target) == 0:
            generator(target)


class SoundManager:
    """Non-blocking audio effects engine for Spatial Audio Radar and Target Beacon."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        ensure_all_sounds()
        self.last_sound_time = 0
        self.min_interval = 0.08
        self.lock = threading.Lock()

    def play_wav(self, filename):
        """Play WAV file asynchronously without blocking UI."""
        path = os.path.join(SOUNDS_DIR, filename)
        if os.path.exists(path):
            try:
                winsound.PlaySound(path, winsound.SND_ASYNC | winsound.SND_FILENAME)
            except Exception as e:
                print("Audio playback error:", e)

    def play_spatial_radar(self, position):
        """Play directional spatial sound for obstacles."""
        now = time.time()
        with self.lock:
            if now - self.last_sound_time < 0.15:
                return
            self.last_sound_time = now

        if position == "left":
            self.play_wav("radar_left.wav")
        elif position == "right":
            self.play_wav("radar_right.wav")
        else:
            self.play_wav("radar_center.wav")

    def play_beacon(self, is_locked=False):
        """Play radar target beacon pulse."""
        now = time.time()
        with self.lock:
            interval = 0.18 if is_locked else 0.12
            if now - self.last_sound_time < interval:
                return
            self.last_sound_time = now

        if is_locked:
            self.play_wav("beacon_lock.wav")
        else:
            self.play_wav("beacon_ping.wav")


# Global singleton instance
sound_manager = SoundManager()

if __name__ == "__main__":
    ensure_all_sounds()
    print("All spatial audio assets generated successfully in:", SOUNDS_DIR)
