"""
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx
wget https://github.com/thewh1teagle/phonikud-chatterbox/releases/download/asset-files-v1/female1.wav
uv run --extra chatterbox examples/with_chatterbox.py
"""
import torchaudio
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from chatterbox.models.utils import get_device
from phonikud_onnx import Phonikud
from phonikud import lexicon
import re


# Initialize the models
device = get_device()
phonikud_model = Phonikud("./phonikud-1.0.int8.onnx")
chatterbox_model = ChatterboxTTS.from_pretrained(device=device)

text = "העברית היא שפה עתיקה ומתחדשת, שמחברת בין ההיסטוריה העמוקה של העם לבין החיים המודרניים."
with_diacritics = phonikud_model.add_diacritics(text)
# remove non standard diacritics
with_diacritics = re.sub(fr"[{lexicon.NON_STANDARD_DIAC}]", "", with_diacritics)
print(f'Input: {with_diacritics}')
ref_path = "female1.wav" # Change to whatever voice you want to use ✨
language_id = "he"
output_path = "audio.wav"

# Generate the audio
multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=device)
wav = multilingual_model.generate(with_diacritics, language_id=language_id, audio_prompt_path=ref_path)
torchaudio.save(output_path, wav, multilingual_model.sr)
print(f"Created {output_path}")