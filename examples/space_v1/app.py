"""
uv sync
uv pip install Flask
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx
wget https://huggingface.co/thewh1teagle/phonikud-tts-checkpoints/resolve/main/model.onnx
wget https://huggingface.co/thewh1teagle/phonikud-tts-checkpoints/resolve/main/model.config.json
uv run ./examples/space_v1/app.py
"""

from flask import Flask, render_template, request, jsonify
from phonikud_tts import Phonikud, phonemize, Piper
import soundfile as sf
import base64
import io

app = Flask(__name__)
phonikud = Phonikud("phonikud-1.0.int8.onnx")
piper = Piper("model.onnx", "model.config.json")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    mode = request.form["mode"]
    text = request.form.get("text", "")
    phonemes = request.form.get("phonemes", "")

    if mode == "text":
        with_diacritics = phonikud.add_diacritics(text)
        phonemes = phonemize(with_diacritics)
    elif mode == "diacritics":
        with_diacritics = text
        phonemes = phonemize(with_diacritics)
    else:
        with_diacritics = None

    samples, sample_rate = piper.create(phonemes, is_phonemes=True, length_scale=1.20, noise_scale=0.640, noise_w=1.0) # noise_w=0.8, noise_scale=0.667
    
    # Volume up
    volume_factor = 2
    samples = samples * volume_factor
    samples = samples.clip(-1.0, 1.0)  # Ensure values are still in valid [-1, 1] range
    
    buffer = io.BytesIO()
    sf.write(buffer, samples, sample_rate, format="WAV")
    buffer.seek(0)
    b64_audio = base64.b64encode(buffer.read()).decode("utf-8")
    data_uri = f"data:audio/wav;base64,{b64_audio}"

    return jsonify({
        "diacritics": with_diacritics,
        "phonemes": phonemes,
        "audio": data_uri
    })

@app.route("/audio/<filename>")
def serve_audio(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7860)
