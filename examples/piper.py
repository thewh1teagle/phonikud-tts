"""
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx
uv run examples/piper.py
"""
from mishel import Phonikud, phonemize, Piper
import soundfile as sf


phonikud = Phonikud('phonikud-1.0.int8.onnx')
piper = Piper('en_US-ryan-medium.onnx', 'en_US-ryan-medium.onnx.json')

# Phonemize text
text = "שלום עולם! מה קורה?"
with_diacritics = phonikud.add_diacritics(text)
phonemes = phonemize(with_diacritics)

# Create audio
samples, sample_rate = piper.create(phonemes)
sf.write('audio.wav', samples, sample_rate)
print("Created audio.wav")