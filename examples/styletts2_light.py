"""
wget https://huggingface.co/thewh1teagle/phonikud-onnx/resolve/main/phonikud-1.0.int8.onnx
wget https://huggingface.co/thewh1teagle/phonikud-tts-checkpoints/resolve/main/saspeech_automatic_stts2-light_epoch_00010.pth
wget https://raw.githubusercontent.com/thewh1teagle/StyleTTS2-lite/refs/heads/hebrew2/Configs/config.yaml
wget https://github.com/thewh1teagle/StyleTTS2-lite/raw/refs/heads/hebrew2/Demo/Audio/10_michael.wav
git clone https://github.com/thewh1teagle/StyleTTS2-lite -b hebrew2

uv pip install ./StyleTTS2-lite
PYTHONPATH=./StyleTTS2-lite uv run --extra styletts2 examples/styletts2_light.py
"""
from phonikud_tts import Phonikud, phonemize
from phonikud_tts.styletts2_light import StyleTTS2Light
import soundfile as sf


phonikud = Phonikud('phonikud-1.0.int8.onnx')
styletts2 = StyleTTS2Light('config.yaml', 'saspeech_automatic_stts2-light_epoch_00010.pth')

# Phonemize text
text = """
ירושלים היא עיר עתיקה וחשובה במיוחד, שמכילה בתוכה שכבות רבות של היסטוריה, תרבות ורוחניות שנמשכות אלפי שנים, והיא מהווה מוקד מרכזי לשלושת הדתות הגדולות, יהדות, נצרות, ואסלאם. שמתחברות יחד במקום אחד ייחודי, מלא אנרגיה ומורכבות, שם אפשר למצוא אתרים קדושים, שכונות עתיקות ושווקים צבעוניים, וכל פינה מספרת סיפור של תקופות שונות, אנשים שונים ואירועים שהשפיעו על ההיסטוריה של העולם כולו, מה שהופך את ירושלים לא רק לעיר גאוגרפית, אלא גם למרכז של זהות, אמונה, וזיכרון קולקטיבי שממשיך לעורר השראה ולחבר בין אנשים מרקע שונה מכל קצוות תבל.
""".strip()
with_diacritics = phonikud.add_diacritics(text)
phonemes = phonemize(with_diacritics)

# Create audio
samples, sample_rate = styletts2.create(phonemes, speaker_path='10_michael.wav')
sf.write('audio.wav', samples, sample_rate)
print("Created audio.wav")