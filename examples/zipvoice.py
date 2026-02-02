"""
wget https://github.com/thewh1teagle/zipvoice-onnx/releases/download/model-files-v1.0/prompt_hebrew_male1.wav -O prompt.wav
wget https://huggingface.co/thewh1teagle/zipvoice-heb/resolve/main/zipvoice-onnx.tar.gz
tar -xf zipvoice-onnx.tar.gz
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx

uv run --extra zipvoice examples/zipvoice.py
"""

import soundfile as sf
from zipvoice_onnx import ZipVoice, ZipVoiceOptions
from phonikud_onnx import Phonikud
from phonikud import phonemize

# Example usage with zipvoice_distill model
options = ZipVoiceOptions(
    text_encoder_path="./zipvoice-onnx/text_encoder.onnx",
    fm_decoder_path="./zipvoice-onnx/fm_decoder.onnx",
    text_encoder_int8_path="./zipvoice-onnx/text_encoder_int8.onnx",
    fm_decoder_int8_path="./zipvoice-onnx/fm_decoder_int8.onnx",
    model_json_path="./zipvoice-onnx/model.json",
    tokens_path="./zipvoice-onnx/tokens.txt",
    # uncomment to use GPU
    # onnx_providers=["CUDAExecutionProvider"],
)

zipvoice = ZipVoice(options)

# Phonemizer setup
nikud_model_path = "phonikud-1.0.int8.onnx"
phonikud_model = Phonikud(nikud_model_path)

# Text to phonemes
text = "שימו לב נוסעים יקרים, הרכבת תכנס לתחנת תל אביב מרכז בעוד מספר דקות, אנא התרחקו מקצה הרציף והמתינו מאחורי הקו הצהוב, תודה."
vocalized = phonikud_model.add_diacritics(text)
target_phonemes = phonemize(vocalized)

# Reference audio and phonemes
ref_wav = "prompt.wav"
ref_text = "הלכתי למכולת לקנות לחם וחלב, ובדרך פגשתי חבר ישן שלא ראיתי הרבה זמן."
ref_vocalized = phonikud_model.add_diacritics(ref_text)
ref_phonemes = phonemize(ref_vocalized)

samples, sample_rate = zipvoice.create(ref_wav, ref_phonemes, target_phonemes, speed=1.2)

sf.write("audio.wav", samples, sample_rate)
print("Saved to audio.wav")