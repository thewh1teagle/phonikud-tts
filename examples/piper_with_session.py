"""
uv sync
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx -O phonikud-1.0.int8.onnx
wget https://huggingface.co/thewh1teagle/phonikud-tts-checkpoints/resolve/main/model.onnx -O tts-model.onnx
wget https://huggingface.co/thewh1teagle/phonikud-tts-checkpoints/resolve/main/model.config.json -O tts-model.config.json
uv run examples/piper.py
"""
from phonikud_tts import Phonikud, phonemize, Piper
import soundfile as sf
import onnxruntime as ort


sess = ort.InferenceSession('phonikud-1.0.int8.onnx', providers=['CPUExecutionProvider'])
phonikud = Phonikud.from_session(sess)
piper = Piper('tts-model.onnx', 'tts-model.config.json')

# Phonemize text
text = "שלום עולם! מה קורה?"
with_diacritics = phonikud.add_diacritics(text)
phonemes = phonemize(with_diacritics)

# Create audio
samples, sample_rate = piper.create(phonemes)
sf.write('audio.wav', samples, sample_rate)
print("Created audio.wav")