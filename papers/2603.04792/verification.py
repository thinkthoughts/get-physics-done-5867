"""
verification.py
arXiv:2603.04792

Fourier-based signal detection (positive frequency only).
"""

import numpy as np

def generate_signal(freq=5, noise_level=0.5, duration=2, sample_rate=100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    signal = np.sin(2 * np.pi * freq * t)
    noise = noise_level * np.random.randn(len(t))
    return t, signal + noise

def compute_fft(data, sample_rate):
    fft = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1/sample_rate)
    return freqs, np.abs(fft)

def main():
    sample_rate = 100
    t, data = generate_signal()

    freqs, fft_vals = compute_fft(data, sample_rate)

    # 🔑 Only consider positive frequencies
    positive = freqs > 0
    freqs_pos = freqs[positive]
    fft_pos = fft_vals[positive]

    peak_freq = freqs_pos[np.argmax(fft_pos)]

    print("Verification: Fourier signal detection")
    print(f"Detected peak frequency: {peak_freq:.2f} Hz")

if __name__ == "__main__":
    main()
