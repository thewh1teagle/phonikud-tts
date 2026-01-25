# phonikud-tts

Text to speech in Hebrew

Based on [Phonikud](https://github.com/thewh1teagle/phonikud)

# Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation)

## Install

```console
git clone https://github.com/thewh1teagle/phonikud-tts
cd phonikud-tts
uv sync
```

## Examples

See [examples](examples)

In each example you'll find a guide on top of the code to run it.

## GPU Support

To use with GPU, you can initiate the models with `from_session` method and initiate the session with `CUDAExecutionProvider`. Make sure to install the correct onnxruntime package, e.g. `onnxruntime-gpu` for CUDA. validate with 

```console
uv run python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
```

## License

Non commercial. See [LICENSE](LICENSE)

## Play 🕹️

See [TTS with Hebrew Space](https://huggingface.co/spaces/thewh1teagle/phonikud-tts)
