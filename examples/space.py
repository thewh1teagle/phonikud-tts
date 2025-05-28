"""
uv sync
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/medium/en_US-ryan-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/medium/en_US-ryan-medium.onnx.json

uv pip install gradio
uv run examples/space.py
uv run gradio examples/space.py
"""
import gradio as gr
from phonikud_tts import Phonikud, phonemize, Piper
import soundfile as sf
import tempfile

css = """
#title { text-align: center; }
.input textarea {
    font-size: 22px;
    padding: 15px;
    height: 200px;
}
.phonemes {
    background: var(--input-background-fill);
    padding: 5px;
    min-height: 50px;
}
.phonemes textarea {
    font-size: 22px !important;
}

"""

def full_pipeline(mode, text, phonemes_in, phonikud, piper):
    if mode == "From Text":
        with_diacritics = phonikud.add_diacritics(text)
        phonemes = phonemize(with_diacritics)
    else:
        with_diacritics = ""
        phonemes = phonemes_in

    samples, sample_rate = piper.create(phonemes, is_phonemes=True)
    tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmpfile.name, samples, sample_rate)
    return f"<div dir='rtl' style='font-size: 22px;'>{with_diacritics}</div>", phonemes, tmpfile.name

def demo():
    DEFAULT_TEXT = "מה שבהגדרה משאיר את הכלכלה ההונגרית מאחור, אפילו ביחס למדינות כמו פולין."
    phonikud = Phonikud('phonikud-1.0.int8.onnx')
    piper = Piper('tts-model.onnx', 'tts-model.config.json')

    theme = gr.themes.Default(font=[gr.themes.GoogleFont("Noto Sans Hebrew")])
    with gr.Blocks(theme=theme, css=css) as demo:
        gr.Markdown("### Hebrew TTS with Phonikud G2P", elem_id="title")

        mode = gr.Radio(["From Text", "From Phonemes"], value="From Text", label="Input Mode")
        text_input = gr.Textbox(label="Hebrew Text", value=DEFAULT_TEXT, elem_classes=["input"], rtl=True)
        phoneme_input = gr.Textbox(label="Phonemes", lines=2, elem_classes=["phonemes"])
        with_diacritics = gr.Markdown(label="Text with Diacritics", elem_classes=["phonemes"])
        audio_output = gr.Audio(label="Audio Output", autoplay=True)

        submit_btn = gr.Button("Generate Audio", variant='primary')

        submit_btn.click(
            fn=lambda mode, text, phonemes: full_pipeline(mode, text, phonemes, phonikud, piper),
            inputs=[mode, text_input, phoneme_input],
            outputs=[with_diacritics, phoneme_input, audio_output]
        )

        gr.Markdown('<div style="text-align: center;"><a href="https://github.com/thewh1teagle/phonikud" target="_blank">Phonikud G2P on GitHub</a></div>')

    demo.launch(share=True)

if __name__ == "__main__":
    demo()
