"""
wget https://github.com/thewh1teagle/zipvoice-onnx/releases/download/model-files-v1.0/prompt_hebrew_male1.wav -O prompt.wav
wget https://huggingface.co/thewh1teagle/zipvoice-heb/resolve/main/zipvoice-onnx.tar.gz
tar -xf zipvoice-onnx.tar.gz

uv run --extra zipvoice examples/zipvoice.py
"""

import soundfile as sf
from zipvoice_onnx import ZipVoice, ZipVoiceOptions

# Example usage with zipvoice_distill model
options = ZipVoiceOptions(
    text_encoder_path="./zipvoice-onnx/text_encoder.onnx",
    fm_decoder_path="./zipvoice-onnx/fm_decoder.onnx",
    text_encoder_int8_path="./zipvoice-onnx/text_encoder_int8.onnx",
    fm_decoder_int8_path="./zipvoice-onnx/fm_decoder_int8.onnx",
    model_json_path="./zipvoice-onnx/model.json",
    tokens_path="./zipvoice-onnx/tokens.txt",
)

zipvoice = ZipVoice(options)

# Example usage
ref_wav = "prompt.wav"
ref_phonemes = "halˈaχti lamakˈolet liknˈot lˈeχem veχalˈav, ubadˈeʁeχ paɡˈaʃti χavˈeʁ jaʃˈan ʃelˈo ʁaʔˈiti haʁbˈe zmˈan."
target_phonemes = "halˈaχti lamakˈolet liknˈot lˈeχem veχalˈav, ubadˈeʁeχ paɡˈaʃti χavˈeʁ jaʃˈan ʃelˈo ʁaʔˈiti haʁbˈe zmˈan."

samples, sample_rate = zipvoice.create(ref_wav, ref_phonemes, target_phonemes)
print(f"Generated audio: {samples.shape} samples at {sample_rate} Hz")

sf.write("audio.wav", samples, sample_rate)
print("Saved to audio.wav")