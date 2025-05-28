"""
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx
uv run examples/styletts2.py
"""
from phonikud_tts import Phonikud, phonemize, StyleTTS2
import soundfile as sf


phonikud = Phonikud('phonikud-1.0.int8.onnx')
styletts2 = StyleTTS2('en_US-ryan-medium.onnx', 'en_US-ryan-medium.onnx.json')

# Phonemize text
text = "שלום עולם! מה קורה?"
with_diacritics = phonikud.add_diacritics(text)
phonemes = phonemize(with_diacritics)

# Create audio
samples, sample_rate = styletts2.create(phonemes)
sf.write('audio.wav', samples, sample_rate)
print("Created audio.wav")