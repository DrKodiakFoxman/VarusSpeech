from flask import Flask, render_template, request, send_file
import tempfile
import os
from TTS.api import TTS

app = Flask(__name__)

# Voces base
VOICES = {
    "en": {
        "Jenny (US)": "tts_models/en/jenny/jenny",
        "Sam (US)": "tts_models/en/sam/tacotron2-DDC",
        "Alice (UK)": "tts_models/en/alice/tacotron2-DDC"
    },
    "es": {
        "Dalia (MX)": "tts_models/es/dalia/tacotron2-DDC",
        "Mia (ES)": "tts_models/es/mai/tacotron2-DDC",
        "Carlos (AR)": "tts_models/es/carloso/tacotron2-DDC"
    }
}

@app.route('/')
def index():
    return render_template('index.html', voices=VOICES)

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    voice_en = request.form['voice_en']
    voice_es = request.form['voice_es']

    segments = []
    while "[/es]" in text and "[es]" in text:
        start = text.index("[es]")
        end = text.index("[/es]") + len("[/es]")
        segments.append((text[:start], "en"))
        segments.append((text[start+4:end-5], "es"))
        text = text[end:]
    if text:
        segments.append((text, "en"))

    audio_paths = []
    for segment, lang in segments:
        model_name = VOICES[lang][voice_es] if lang == "es" else VOICES[lang][voice_en]
        tts = TTS(model_name)
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tts.tts_to_file(text=segment, file_path=fp.name)
        audio_paths.append(fp.name)

    # Combinar audios
    from pydub import AudioSegment
    combined = AudioSegment.empty()
    for path in audio_paths:
        combined += AudioSegment.from_wav(path)
        os.remove(path)

    final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    combined.export(final_path, format="mp3")
    return send_file(final_path, as_attachment=True)
