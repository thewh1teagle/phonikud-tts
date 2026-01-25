"""
wget https://github.com/thewh1teagle/style-onnx/releases/download/model-files-v1.0/636_female_style.npy
wget https://github.com/thewh1teagle/style-onnx/releases/download/model-files-v1.0/libritts_hebrew.onnx
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx

uv run examples/styletts2.py
"""

import soundfile as sf
from style_onnx import StyleTTS2
from phonikud_onnx import Phonikud
from phonikud import phonemize

model_path = "libritts_hebrew.onnx"
nikud_model_path = 'phonikud-1.0.int8.onnx'
styles_path = "636_female_style.npy"
audio_path = "audio.wav"

# Phonemizer setup
phonikud_model = Phonikud(nikud_model_path)


tts = StyleTTS2(model_path, styles_path)

# Text to phonemes
text = "שימו לב נוסעים יקרים, הרכבת תכנס לתחנת תל אביב מרכז בעוד מספר דקות, אנא התרחקו מקצה הרציף והמתינו מאחורי הקו הצהוב, תודה."
vocalized = phonikud_model.add_diacritics(text)
phonemes = phonemize(vocalized)

# Create audio
samples, sr = tts.create(phonemes, speed=1.32)

# Save audio
sf.write(audio_path, samples, sr)
print(f"Saved {audio_path} ({len(samples) / sr:.2f}s)")